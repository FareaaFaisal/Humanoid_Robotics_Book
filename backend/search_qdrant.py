# search_qdrant.py
import os
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")

# Initialize Cohere embedding client
co = cohere.Client(COHERE_API_KEY)

# Initialize Qdrant client (cloud)
qdrant = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY
)

collection_name = "docusaurus_chunks"

def search_text(query_text, top_k=5):
    # 1. Get embedding for the search query
    query_vector = co.embed(
        model="embed-english-light-v2.0",
        texts=[query_text]
    ).embeddings[0]

    # 2. Perform similarity search in Qdrant
    results = qdrant.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True  # return stored text and metadata
    )

    print(f"\nTop {top_k} results for: '{query_text}'\n")

    if not results.points:
        print("No similar vectors found.")
        return

    for i, point in enumerate(results.points, 1):
        payload = point.payload or {}
        text = payload.get("text", "<no text>")
        score = point.score
        print(f"{i}. [{score:.4f}] {text}")

if __name__ == "__main__":
    query = input("Enter your search query: ")
    search_text(query, top_k=5)
