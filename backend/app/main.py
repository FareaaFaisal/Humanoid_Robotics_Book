from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import json

from app.models.api_models import (
    EmbedRequest, EmbedResponse, QueryRequest, QueryResponse,
    ChatRequest, ChatCitation, ChatSimilarityScore
)
from app.services.cohere_embed import CohereEmbedService
from app.services.qdrant import QdrantService
from app.services.llm_generation import LLMGenerationService

load_dotenv()
app = FastAPI(title="Humanoid Robotics RAG Backend")

# ---------------------- Services ----------------------
cohere_embed_service = CohereEmbedService()
qdrant_service = QdrantService()
llm_generation_service = LLMGenerationService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "FastAPI RAG Backend is running!"}

# ---------------------- /embed ----------------------
@app.post("/embed", response_model=EmbedResponse)
async def embed_text(request: EmbedRequest):
    try:
        embeddings = await cohere_embed_service.embed_text([request.text])
        return EmbedResponse(embedding=embeddings[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {e}")

# ---------------------- /query ----------------------
@app.post("/query", response_model=QueryResponse)
async def query_vectors(request: QueryRequest):
    try:
        query_embedding = await cohere_embed_service.embed_text([request.query_text])
        results = qdrant_service.query_by_vector(
            query_embedding[0],
            limit=request.limit,
            min_score=request.min_score
        )
        return QueryResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

# ---------------------- /chat ----------------------
@app.post("/chat")
async def chat(request: ChatRequest):
    query_text = request.selected_text_context or request.user_message
    query_embedding = await cohere_embed_service.embed_text([query_text])
    retrieved_chunks = qdrant_service.query_by_vector(query_embedding[0], limit=5, min_score=0.15)

    context_texts = [chunk["text"] for chunk in retrieved_chunks]

    # ------------------- System prompt -------------------
    system_prompt = (
        "You are an academic assistant for the book "
        "'Physical AI & Humanoid Robotics' created by FAREAA FAISAL. "
        "This book has 4 modules, each containing 8 chapters. "
        "Answer the question using ONLY the provided context. "
        "Do NOT add outside information.\n"
    )

    llm_prompt = system_prompt + "\n\n### Context\n" + "\n\n".join(context_texts)
    llm_prompt += f"\n\n### Question\n{request.user_message}\n\n### Answer (Markdown)\n"

    async def generate_and_stream():
        try:
            # ------------------- LLM streaming -------------------
            async for chunk in llm_generation_service.generate_response(
                prompt=llm_prompt,
                retrieved_context=retrieved_chunks,
                chat_history=request.chat_history
            ):
                yield f"data: {json.dumps({'type': 'content', 'value': chunk})}\n\n"

            # ------------------- Citations -------------------
            # ------------------- Citations (single) -------------------
            citations = []
            if retrieved_chunks:
                c = retrieved_chunks[0]  # only the top 1
                url = c["metadata"].get("url", "#")
                chapter_title = (
                    c["metadata"].get("chapter_title")
                    or c["metadata"].get("chapter")
                    or c["metadata"].get("section")
                )

                citations.append(
                    ChatCitation(
                        module=c["metadata"].get("module", 0),
                        chapter_number=c["metadata"].get("chapter_number", 0),
                        chapter_title=chapter_title,
                        section=c["metadata"].get("section", ""),
                        url=url
                    ).dict()
                )

            yield f"data: {json.dumps({'type': 'citations', 'value': citations})}\n\n"

            # ------------------- Similarity scores -------------------
            scores = [
                ChatSimilarityScore(id=c["id"], score=c["score"]).dict()
                for c in retrieved_chunks
            ]
            yield f"data: {json.dumps({'type': 'scores', 'value': scores})}\n\n"

            yield f"data: {json.dumps({'type': 'done'})}\n\n"  # unlock frontend input

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'value': str(e)})}\n\n"

    return StreamingResponse(generate_and_stream(), media_type="text/event-stream")
