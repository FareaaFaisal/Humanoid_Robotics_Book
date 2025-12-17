import os
import re
import uuid
import pathlib
import asyncio
from typing import Dict, Any
from markdown_it import MarkdownIt
from dotenv import load_dotenv

from app.services.chunking import TextChunkingService
from app.services.cohere_embed import CohereEmbedService
from app.services.qdrant import QdrantService

load_dotenv()

def extract_structure_from_path(file_path: pathlib.Path):
    parts = file_path.parts
    module_num = None
    chapter_num = None
    chapter_title = file_path.stem.replace("-", " ").title()

    for p in parts:
        if re.match(r"\d{2}-", p):
            module_num = int(p.split("-")[0])

    if re.match(r"\d{2}-", file_path.stem):
        chapter_num = int(file_path.stem.split("-")[0])
        chapter_title = file_path.stem.split("-", 1)[1].replace("-", " ").title()

    return module_num or 0, chapter_num or 0, chapter_title

def extract_text_and_metadata_from_mdx(mdx_content: str, file_path: pathlib.Path, docs_root: pathlib.Path) -> Dict[str, Any]:
    front_matter_match = re.match(r'^---\n(.*?)\n---\n', mdx_content, re.DOTALL)
    metadata = {}
    content = mdx_content

    if front_matter_match:
        front_matter = front_matter_match.group(1)
        for line in front_matter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip("'\"")
        content = mdx_content[len(front_matter_match.group(0)):].strip()

    md = MarkdownIt()
    tokens = md.parse(content)
    plain_text_parts = []
    for token in tokens:
        if token.type == 'inline' and token.content:
            plain_text_parts.append(token.content)
        elif token.type == 'fence' and token.content:
            plain_text_parts.append(f"\n```\n{token.content}\n```\n")

    plain_text = re.sub(r'\s+', ' ', " ".join(plain_text_parts)).strip()
    module_num, chapter_num, chapter_title = extract_structure_from_path(file_path)
    relative_path = file_path.relative_to(docs_root)
    url = f"/docs/{relative_path.with_suffix('')}".replace("\\", "/")

    return {
        "text": f"Title: {chapter_title}\n\n{plain_text}",
        "module": module_num,
        "chapter_number": chapter_num,
        "chapter_title": chapter_title,
        "section": metadata.get("sidebar_label", chapter_title),
        "url": url,
    }

async def ingest_docusaurus_content(docs_dir: str):
    cohere_embed_service = CohereEmbedService()
    qdrant_service = QdrantService()
    chunking_service = TextChunkingService(chunk_size=800, chunk_overlap=100)
    vector_size = 1024
    qdrant_service.create_collection(vector_size=vector_size)

    docs_root_path = pathlib.Path(docs_dir)
    md_files = list(docs_root_path.rglob("*.md*"))
    total_chunks_ingested = 0

    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            mdx_content = f.read()

        extracted = extract_text_and_metadata_from_mdx(mdx_content, file_path, docs_root_path)
        if not extracted["text"]:
            continue

        chunks = chunking_service.chunk_text(
            extracted["text"],
            {
                "module": extracted["module"],
                "chapter_number": extracted["chapter_number"],
                "chapter_title": extracted["chapter_title"],
                "section": extracted["section"],
                "url": extracted["url"],
            },
        )

        embeddings = await cohere_embed_service.embed_text([c["text"] for c in chunks])

        payloads = [
            {
                "text": c["text"],
                "module": c.get("module", 0),
                "chapter_number": c.get("chapter_number", 0),
                "chapter_title": c.get("chapter_title") or c.get("chapter") or c.get("section"),
                "section": c.get("section", ""),
                "url": c.get("url", "#"),
            }
            for c in chunks
        ]
        ids = [str(uuid.uuid4()) for _ in chunks]
        qdrant_service.upsert_vectors(embeddings, payloads, ids)
        total_chunks_ingested += len(chunks)
        print(f"Ingested {len(chunks)} chunks from {file_path.name}")

    print(f"\nTotal chunks ingested: {total_chunks_ingested}")

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    docs_path = os.path.join(script_dir, "..", "humanoid-robotics-book", "docs")
    print(f"\n--- Starting ingestion from: {os.path.abspath(docs_path)} ---")
    asyncio.run(ingest_docusaurus_content(docs_path))
    print("\n--- Ingestion finished ---")
