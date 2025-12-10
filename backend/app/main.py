from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os
import json
from app.models.api_models import (
    EmbedRequest, EmbedResponse, QueryRequest, QueryResponse,
    ChatRequest, ChatCitation, ChatSimilarityScore
)
from app.services.cohere_embed import CohereEmbedService
from app.services.qdrant import QdrantService
from app.services.llm_generation import LLMGenerationService

# ----------------------
# Load environment variables
# ----------------------
load_dotenv()

# ----------------------
# Initialize FastAPI app
# ----------------------
app = FastAPI(title="Humanoid Robotics RAG Backend")

# ----------------------
# Initialize services
# ----------------------
print("Initializing services...")
try:
    cohere_embed_service = CohereEmbedService()
    qdrant_service = QdrantService()
    llm_generation_service = LLMGenerationService()
    print("Services initialized successfully.")
except Exception as e:
    print(f"FATAL: Failed to initialize services: {e}")

# ----------------------
# Configure CORS
# ----------------------
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Root endpoint
# ----------------------
@app.get("/")
async def read_root():
    return {"message": "FastAPI RAG Backend is running!"}

# ----------------------
# /embed endpoint
# ----------------------
@app.post("/embed", response_model=EmbedResponse)
async def embed_text(request: EmbedRequest):
    try:
        embeddings = await cohere_embed_service.embed_text([request.text])
        return EmbedResponse(embedding=embeddings[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {e}")

# ----------------------
# /query endpoint
# ----------------------
@app.post("/query", response_model=QueryResponse)
async def query_vectors(request: QueryRequest):
    try:
        query_embedding = await cohere_embed_service.embed_text([request.query_text])
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Could not generate embedding for query.")

        results = qdrant_service.search_vectors(
            query_vector=query_embedding[0],
            limit=request.limit,
            min_score=request.min_score,
        )
        return QueryResponse(results=results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

# ----------------------
# /chat endpoint
# ----------------------
@app.post("/chat")
async def chat(request: ChatRequest):
    print("\n--- Received new /chat request ---")
    try:
        query_text = request.selected_text_context or request.user_message
        print(f"1. Query text: '{query_text}'")

        print("2. Generating embedding for query...")
        query_embedding = await cohere_embed_service.embed_text([query_text])
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Could not generate embedding for chat query.")
        print("   Embedding generated successfully.")

        print("3. Searching for relevant chunks in Qdrant...")
        retrieved_chunks = qdrant_service.search_vectors(
            query_vector=query_embedding[0],
            limit=5,
            min_score=0.1
        )
        print(f"   Found {len(retrieved_chunks)} relevant chunks.")

        context_texts = [chunk["text"] for chunk in retrieved_chunks]

        print("4. Preparing prompt for LLM...")
        system_prompt = (
            "You are a helpful assistant for the 'Physical AI & Humanoid Robotics' book, made by Fareaa Faisal. "
            "Use only the provided context to answer the question. If the answer is not in the context, say you don't know.\n\n"
            "Additional context:\n"
            "- Overview of Physical AI:\n"
            "  Physical AI focuses on embodied systems where intelligence arises through interaction with the real world. "
            "  It relies on sensors, actuators, and controllers to perceive, reason, and act. Embodied intelligence leverages "
            "  the body and environment to simplify computation, improve adaptability, and enable complex behaviors. "
            "  ROS (Robot Operating System) is a key enabler, providing modular software infrastructure for control, communication, and simulation.\n\n"
            "- Physical AI vs Digital AI:\n"
            "  * Physical AI exists in real-world robots, requires sensors and actuators, interacts with the environment, "
            "and is constrained by hardware and safety.\n"
            "  * Digital AI exists in simulations or cloud systems, may not require sensors/actuators, interacts virtually, "
            "and is limited mainly by computation.\n\n"
            "- Benefits of ROS:\n"
            "  * Simplifies hardware integration\n"
            "  * Enables modular software design\n"
            "  * Facilitates simulation and real-world testing\n"
            "  * Supports rapid prototyping of intelligent behaviors\n\n"
            "- Why Simulations Are Needed:\n"
            "  Robotic systems are complex, involving mechanical structures, sensors, controllers, and software. "
            "  Testing directly on hardware can be risky, expensive, and time-consuming. Simulations provide a safe "
            "  and cost-effective environment to develop and validate:\n"
            "    * Control algorithms before physical implementation\n"
            "    * Motion planning to prevent collisions\n"
            "    * Sensor integration and data fusion strategies\n"
            "    * Human-robot interactions in a risk-free environment\n\n"
            "- URDF (Unified Robot Description Format):\n"
            "  A standard XML format used to describe a robot's physical structure, including links, joints, sensors, and actuators. "
            "  It enables robots to be simulated and controlled consistently in ROS.\n\n"
            "- NVIDIA Isaac Ecosystem:\n"
            "  A comprehensive framework for developing, simulating, and deploying AI-powered robots. It integrates high-fidelity "
            "simulation, AI-powered perception, and robotics middleware to accelerate development and testing. "
            "  Key components include Isaac Sim, Isaac SDK, and Isaac ROS."
        )


        llm_prompt = system_prompt + "\n\nContext:\n"
        for i, text in enumerate(context_texts):
            llm_prompt += f"- {text}\n"
        llm_prompt += f"\nQuestion: {request.user_message}\nAnswer:"
        print("   Prompt prepared.")

        async def generate_and_stream():
            print("5. Generating response from LLM (streaming)...")
            try:
                full_response_content = ""
                async for chunk in llm_generation_service.generate_response(
                    prompt=llm_prompt,
                    retrieved_context=retrieved_chunks,
                    chat_history=request.chat_history
                ):
                    full_response_content += chunk
                    data_chunk = {
                        "type": "content",
                        "value": chunk
                    }
                    yield f"data: {json.dumps(data_chunk)}\n\n"
                print("   LLM stream finished.")

                # Send citations
                citations = [
                    ChatCitation(
                        chapter=c["metadata"]["chapter"],
                        section=c["metadata"]["section"],
                        url=c["metadata"]["url"]
                    ) for c in retrieved_chunks
                ]
                data_citations = {
                    "type": "citations",
                    "value": [c.dict() for c in citations]
                }
                yield f"data: {json.dumps(data_citations)}\n\n"

                # Send similarity scores
                similarity_scores = [
                    ChatSimilarityScore(id=c["id"], score=c["score"]) for c in retrieved_chunks
                ]
                data_scores = {
                    "type": "scores",
                    "value": [s.dict() for s in similarity_scores]
                }
                yield f"data: {json.dumps(data_scores)}\n\n"

                print("6. Sent citations and scores.")

            except Exception as e:
                print(f"   ERROR during LLM generation/streaming: {e}")
                error_data = {
                    "type": "error",
                    "value": str(e)
                }
                yield f"data: {json.dumps(error_data)}\n\n"

            print("--- /chat request finished ---")

        return StreamingResponse(generate_and_stream(), media_type="text/event-stream")

    except Exception as e:
        print(f"FATAL ERROR in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"A fatal error occurred: {e}")
