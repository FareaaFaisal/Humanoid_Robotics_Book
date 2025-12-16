import os
from qdrant import QdrantService  # your updated qdrant.py
from dotenv import load_dotenv
import cohere
import uuid

# Load environment variables
load_dotenv()

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

# Initialize Qdrant service
qdrant = QdrantService()

# Sample texts to insert
texts = [
    "ROS 2 allows modular robot software development using packages.",
    "Colcon is the build tool used for compiling ROS 2 packages."
]

# Generate embeddings using Cohere
vectors = []
for text in texts:
    emb_response = co.embed(
        model="embed-english-light-v2.0",
        texts=[text]
    )
    vectors.append(emb_response.embeddings[0])

# Generate unique IDs and payloads
ids = [str(uuid.uuid4()) for _ in texts]
payloads = [{"text": text} for text in texts]

# Ensure collection exists
vector_size = len(vectors[0])
qdrant.create_collection(vector_size=vector_size)

# Upsert vectors into Qdrant
qdrant.upsert_vectors(vectors=vectors, payloads=payloads, ids=ids)
print(f"Inserted {len(texts)} points into {qdrant.collection_name}")

# Optional: simple search test
query_text = "What is Colcon?"
query_emb = co.embed(
    model="embed-english-light-v2.0",
    texts=[query_text]
).embeddings[0]

results = qdrant.search_vectors(query_vector=query_emb, limit=3)
print("\nTop search results:")
for r in results:
    print(f"- [{r['score']:.4f}] {r['text']}")
