from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import pinecone
import hashlib
import uuid

from .config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME

# --- Models ---
class ScrapeRequest(BaseModel):
    url: str

class TaskResponse(BaseModel):
    task_id: str
    message: str

# --- Initialization ---
print("Initializing Motherboard Service...")

# Initialize model for semantic search
print("Loading embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Embedding model loaded.")

# Initialize connection to Pinecone
print("Connecting to Pinecone...")
if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT:
    raise ValueError("PINECONE_API_KEY and PINECONE_ENVIRONMENT must be set.")

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

if PINECONE_INDEX_NAME not in pinecone.list_indexes():
    print(f"Pinecone index '{PINECONE_INDEX_NAME}' not found. Please create it.")
    # As a safeguard, let's not create it automatically in a production script.
    # pinecone.create_index(PINECONE_INDEX_NAME, dimension=384, metric='cosine')

index = pinecone.Index(PINECONE_INDEX_NAME)
print("Pinecone connection and index ready.")

app = FastAPI(title="Motherboard Service")
print("Motherboard Service initialized.")
# --- End Initialization ---


def process_and_embed_url(url: str):
    """
    Background task to scrape a URL, chunk the text, and embed it into Pinecone.
    """
    print(f"Starting background task to process URL: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Simple text extraction (can be customized)
        text_chunks = [p.get_text() for p in soup.find_all('p') if p.get_text()]

        if not text_chunks:
            print(f"No text chunks found at {url}")
            return

        print(f"Found {len(text_chunks)} text chunks. Embedding...")
        vectors_to_upsert = []
        for chunk in text_chunks:
            if len(chunk) > 50: # Filter out very short/irrelevant chunks
                vector = embedding_model.encode(chunk).tolist()
                chunk_id = hashlib.md5(chunk.encode()).hexdigest()
                vectors_to_upsert.append((chunk_id, vector, {"source": url, "text": chunk}))
        
        if vectors_to_upsert:
            index.upsert(vectors=vectors_to_upsert)
            print(f"Successfully indexed {len(vectors_to_upsert)} chunks from {url}")
        else:
            print(f"No suitable text chunks to index from {url}")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")


@app.post("/ingest-url", response_model=TaskResponse)
async def ingest_url(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Accepts a URL and starts a background task to scrape and embed its content.
    """
    task_id = str(uuid.uuid4())
    print(f"Received request to ingest URL: {request.url}. Task ID: {task_id}")
    background_tasks.add_task(process_and_embed_url, request.url)
    return {"task_id": task_id, "message": "URL ingestion started in the background."}
