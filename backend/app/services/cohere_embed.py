import os
import cohere
from typing import List

class CohereEmbedService:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set.")
        self.co = cohere.Client(self.api_key)
        self.model = "embed-english-v3.0" # User-specified, preferred model

    async def embed_text(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts using Cohere Embed v3.
        """
        if not texts:
            return []
        
        # Cohere's async client might require a different setup or be used in a sync context
        # For simplicity, using sync client in an async function context for now
        # In a real async app, you'd use run_in_threadpool or an async Cohere client
        try:
            response = self.co.embed(
                texts=texts,
                model=self.model,
                input_type="search_document" # Or "search_query" depending on use case
            )
            return response.embeddings
        except cohere.CohereError as e:
            print(f"Cohere API error: {e}")
            raise
