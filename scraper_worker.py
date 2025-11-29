import requests
from bs4 import BeautifulSoup
from celery import Celery

from .config import REDIS_URL
from .embedding_worker import embed_and_index

# Initialize Celery
app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)

@app.task(name="scraper.scrape_and_process")
def scrape_and_process(url):
    """
    Scrapes a URL, extracts text, and triggers the embedding task.
    
    This is a conceptual example. A real-world implementation would need
    custom logic for each type of website you want to scrape.
    """
    print(f"Scraping URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Customizable Logic ---
        # This is the part you would customize. For example, finding all
        # paragraph tags.
        text_chunks = [p.get_text() for p in soup.find_all('p')]
        # --- End Customizable Logic ---

        if not text_chunks:
            return f"No text found at {url}"

        # Process each chunk of text found on the page
        for chunk in text_chunks:
            if chunk and len(chunk) > 50: # Only process meaningful chunks
                # Call the embedding task for each chunk
                embed_and_index.delay(chunk, source_url=url)

        return f"Successfully queued {len(text_chunks)} chunks from {url} for indexing."
    except requests.exceptions.RequestException as e:
        return f"Error scraping {url}: {e}"