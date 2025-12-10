import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient, models

class QdrantService:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_HOST")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError("QDRANT_HOST and QDRANT_API_KEY environment variables must be set.")
        
        self.client = QdrantClient(
            url=self.qdrant_url, 
            api_key=self.qdrant_api_key
        )
        self.collection_name = "docusaurus_chunks"

    def create_collection(self, vector_size: int):
        """Creates the Qdrant collection if it doesn't already exist."""
        try:
            self.client.get_collection(collection_name=self.collection_name)
            print(f"Collection '{self.collection_name}' already exists.")
        except Exception:
            print(f"Collection '{self.collection_name}' not found, creating it...")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
            )
            print(f"Collection '{self.collection_name}' created.")

    def upsert_vectors(self, vectors: List[List[float]], payloads: List[Dict[str, Any]], ids: List[str]):
        """Upserts (inserts or updates) vectors and their payloads into Qdrant."""
        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(ids=ids, vectors=vectors, payloads=payloads),
            wait=True
        )

    def search_vectors(self, query_vector: List[float], limit: int = 5, min_score: float = 0.1) -> List[Dict[str, Any]]:
        """Search vectors using v1.16.1 QdrantClient."""
        try:
            # Correct search method for v1.16.1
            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=min_score,
                query_filter=None  # optional filter if needed later
            )

            results = [
                {
                    "id": hit.id,
                    "text": hit.payload.get("text") if hit.payload else None,
                    "score": hit.score,
                    "metadata": {
                        "chapter": hit.payload.get("chapter") if hit.payload else None,
                        "section": hit.payload.get("section") if hit.payload else None,
                        "url": hit.payload.get("url") if hit.payload else None,
                    },
                }
                for hit in hits
            ]
            return results

        except Exception as e:
            print(f"Error during Qdrant search: {e}")
            return []
