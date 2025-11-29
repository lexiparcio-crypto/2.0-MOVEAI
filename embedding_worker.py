from celery import Celery
from sentence_transformers import SentenceTransformer
import pinecone
import hashlib

from .config import REDIS_URL, PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME

# Initialize Celery
app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)

# --- One-time Initialization ---
# These objects are created once per worker process.
print("Initializing embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2') # 384 dimensions
print("Model initialized.")

print("Initializing Pinecone connection...")
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY environment variable not set!")

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

if PINECONE_INDEX_NAME not in pinecone.list_indexes():
    print(f"Creating Pinecone index: {PINECONE_INDEX_NAME}")
    pinecone.create_index(PINECONE_INDEX_NAME, dimension=384, metric='cosine')

index = pinecone.Index(PINECONE_INDEX_NAME)
print("Pinecone connection and index ready.")
# --- End Initialization ---

@app.task(name="embedder.embed_and_index")
def embed_and_index(text_chunk, source_url):
    """
    Takes a chunk of text, generates an embedding, and upserts it to Pinecone.
    """
    try:
        vector = model.encode(text_chunk).tolist()
        chunk_id = hashlib.md5(text_chunk.encode()).hexdigest()

        index.upsert(vectors=[(chunk_id, vector, {"source": source_url, "text": text_chunk})])
        print(f"Indexed chunk from {source_url}")
        return f"Successfully indexed chunk from {source_url}"
    except Exception as e:
        print(f"Error during indexing: {e}")
        return f"Failed to index chunk: {e}"