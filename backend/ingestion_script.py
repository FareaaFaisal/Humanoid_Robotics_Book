import os
import re
import uuid
import pathlib
from typing import List, Dict, Any
from markdown_it import MarkdownIt
from app.services.chunking import TextChunkingService
from app.services.cohere_embed import CohereEmbedService
from app.services.qdrant import QdrantService
from dotenv import load_dotenv
import asyncio

load_dotenv()

def extract_text_and_metadata_from_mdx(mdx_content: str, file_path: pathlib.Path, docs_root: pathlib.Path) -> Dict[str, Any]:
    front_matter_match = re.match(r'^---\n(.*?)\n---\n', mdx_content, re.DOTALL)
    metadata = {}
    content = mdx_content
    if front_matter_match:
        front_matter = front_matter_match.group(1)
        for line in front_matter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip("'\"") # Corrected: escaped double quote
        content = mdx_content[len(front_matter_match.group(0)):].strip()

    md = MarkdownIt()
    tokens = md.parse(content)
    # Refined plain text extraction
    plain_text_parts = []
    for token in tokens:
        if token.type == 'inline' and token.content:
            plain_text_parts.append(token.content)
        elif token.type == 'fence' and token.info: # Code blocks
            # Preserve code blocks for embedding context
            plain_text_parts.append(f"\n```\n{token.content}\n```\n")
    plain_text = " ".join(plain_text_parts)
    plain_text = re.sub(r'\s+', ' ', plain_text).strip()

    # Generate a clean, relative URL
    relative_path = file_path.relative_to(docs_root)
    # Ensure URL is clean and doesn't contain Windows path separators
    url = f"/docs/{relative_path.with_suffix('')}".replace("\\", "/")

    return {
        "text": plain_text,
        "chapter": metadata.get('title', file_path.stem), # Use title from front matter as chapter name
        "section": metadata.get('sidebar_label', "Introduction"), # Fallback for section if not explicitly in front matter
        "url": url,
    }

async def ingest_docusaurus_content(docs_dir: str):
    cohere_embed_service = CohereEmbedService()
    qdrant_service = QdrantService()
    chunking_service = TextChunkingService(chunk_size=400, chunk_overlap=50)

    vector_size = 1024 # Assumed vector size for Cohere Embed v3
    
    # create_collection is synchronous
    qdrant_service.create_collection(vector_size=vector_size)

    docs_root_path = pathlib.Path(docs_dir)
    md_files = list(docs_root_path.rglob("*.md*"))

    total_chunks_ingested = 0
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            mdx_content = f.read()
        
        extracted_data = extract_text_and_metadata_from_mdx(mdx_content, file_path, docs_root_path)
        
        if extracted_data["text"]:
            chunks = chunking_service.chunk_text(extracted_data["text"], {
                "chapter": extracted_data["chapter"],
                "section": extracted_data["section"],
                "url": extracted_data["url"]
            })

            chunk_texts = [chunk["text"] for chunk in chunks]
            if not chunk_texts:
                continue

            embeddings = await cohere_embed_service.embed_text(chunk_texts)
            
            payloads = [
                {
                    "text": chunk["text"],
                    "chapter": chunk["chapter"],
                    "section": chunk["section"],
                    "url": chunk["url"]
                } for chunk in chunks
            ]
            ids = [str(uuid.uuid4()) for _ in chunks]

            # upsert_vectors is synchronous
            qdrant_service.upsert_vectors(vectors=embeddings, payloads=payloads, ids=ids)
            total_chunks_ingested += len(chunks)
            print(f"Ingested {len(chunks)} chunks from {file_path.name}")

    print(f"Total chunks ingested: {total_chunks_ingested}")

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    docusaurus_docs_path = os.path.join(script_dir, "..", "humanoid-robotics-book", "docs")
    
    print(f"\n--- Starting ingestion from: {os.path.abspath(docusaurus_docs_path)} ---")
    if not os.path.isdir(docusaurus_docs_path):
        print("Error: Docs directory not found. Please check the path.")
    else:
        asyncio.run(ingest_docusaurus_content(docusaurus_docs_path))
    print("\n--- Ingestion script finished ---")