import os
from dotenv import load_dotenv

load_dotenv()

print("QDRANT_HOST =", os.getenv("QDRANT_HOST"))
print("QDRANT_API_KEY =", os.getenv("QDRANT_API_KEY"))
