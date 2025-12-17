import os
import cohere
from cohere.errors import TooManyRequestsError, BadRequestError
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

class CohereEmbedService:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set.")
        self.client = cohere.Client(self.api_key)
        self.model = os.getenv("COHERE_MODEL", "embed-english-light-v2.0")

    async def embed_text(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings asynchronously."""
        from asyncio import to_thread
        return await to_thread(self._embed_sync, texts)

    def _embed_sync(self, texts: List[str]) -> List[List[float]]:
        try:
            response = self.client.embed(model=self.model, texts=texts)
            return response.embeddings
        except (TooManyRequestsError, BadRequestError) as e:
            print(f"Error generating embeddings: {e}")
            raise e
