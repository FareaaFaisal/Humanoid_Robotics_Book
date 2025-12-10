import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

print("\n--- QDRANT TEST STARTED ---\n")

# Load .env variables
load_dotenv()

print("QDRANT_HOST =", os.getenv("QDRANT_HOST"))
print("QDRANT_API_KEY =", os.getenv("QDRANT_API_KEY"))


client = QdrantClient(
    url=os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Example vector (length 1024 for your collection)
vector = [0.001] * 1024
payload = {
    "text": "This chapter covers advanced robotics simulation...",
    "chapter": "Robotics Simulation",
    "section": "Introduction",
    "url": "/docs/03-robotics/01-intro"
}

client.upsert(
    collection_name="docusaurus_chunks",
    points=[
        {
            "id": str(uuid.uuid4()),  # unique ID
            "vector": vector,
            "payload": payload
        }
    ]
)

print("Vector successfully upserted!")
