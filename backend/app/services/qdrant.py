import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Batch, Filter, FieldCondition, Range

class QdrantService:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_HOST")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError("QDRANT_HOST and QDRANT_API_KEY must be set.")

        self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        self.collection_name = "docusaurus_chunks"

    def create_collection(self, vector_size: int):
        if self.client.collection_exists(self.collection_name):
            print(f"Collection '{self.collection_name}' already exists.")
        else:
            print(f"Creating collection '{self.collection_name}'...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            print("Collection created.")

    def upsert_vectors(
        self, 
        vectors: List[List[float]], 
        payloads: List[Dict[str, Any]], 
        ids: List[str]
    ):
        """Insert vectors with payload into Qdrant."""
        self.client.upsert(
            collection_name=self.collection_name,
            points=Batch(ids=ids, vectors=vectors, payloads=payloads),
            wait=True,
        )

    def query_by_vector(
        self,
        query_vector: List[float],
        limit: int = 5,
        min_score: float = 0.0,
        filters: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        """
        Query collection by vector using query_points.
        Applies optional metadata filters.
        Returns points with metadata and score.
        """
        q_filter = None
        if filters:
            must_conditions = []
            for k, v in filters.items():
                must_conditions.append(
                    FieldCondition(
                        key=k,
                        match={"value": v}
                    )
                )
            if must_conditions:
                q_filter = Filter(must=must_conditions)

        try:
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                with_payload=True,
                with_vectors=False,
                score_threshold=min_score,
                query_filter=q_filter
            )

            results = []
            for hit in response.points:
                payload = hit.payload or {}
                results.append({
                    "id": hit.id,
                    "text": payload.get("text", ""),
                    "score": hit.score,
                    "metadata": {
                        "module": payload.get("module", 0),
                        "chapter_number": payload.get("chapter_number", 0),
                        "chapter_title": payload.get("chapter_title", "Unknown Chapter"),
                        "section": payload.get("section", "Unknown Section"),
                        "url": payload.get("url", "#")
                    }
                })
            return results

        except Exception as e:
            print(f"ERROR: Qdrant query failed → {e}")
            return []
