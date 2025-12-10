# Research & Decisions for Integrated RAG Chatbot

This document records the key research findings and architectural decisions for the Integrated RAG Chatbot feature.

## 1. Backend Framework & Components

-   **Decision**: FastAPI for the backend, Qdrant Cloud for vector storage, Cohere Embed v3 for embeddings, and an LLM (e.g., OpenAI, Gemini, or Cohere) for generation.
-   **Rationale**: FastAPI provides a high-performance, async-ready web framework suitable for serving the RAG pipeline. Qdrant Cloud offers a managed vector database with a free tier, aligning with the "no SQL database" constraint. Cohere Embed v3 is specified by the user and is a strong embedding model. The choice of LLM will be a key decision point in the next planning phase.
-   **Alternatives Considered**: Other web frameworks (Flask, Node.js/Express) were not considered due to the explicit mention of FastAPI. Other vector databases (Pinecone, Weaviate) or embedding models (OpenAI, Hugging Face) were not explored due to explicit user constraints.

## 2. Docusaurus Content Preprocessing (Chunking)

-   **Decision**: Docusaurus MDX pages will be preprocessed into chunks of ~300-500 tokens each. The preprocessing will extract text content while preserving context and essential metadata.
-   **Rationale**: Optimal chunk size is crucial for effective RAG. Too small, and context is lost; too large, and irrelevant information dilutes the signal. 300-500 tokens is a common range for good performance.
-   **Challenges**: Extracting clean text from MDX, handling code blocks, tables, and other non-textual elements while maintaining structural integrity for accurate retrieval and citation.

## 3. Qdrant Cloud Configuration

-   **Decision**: A dedicated collection will be created in Qdrant Cloud.
-   **Vector Schema**:
    -   `id`: Unique identifier for each chunk.
    -   `text`: The actual text content of the chunk.
    -   `chapter`: The chapter title the chunk belongs to.
    -   `section`: The section title the chunk belongs to.
    -   `url`: The URL of the Docusaurus page where the chunk originates.
    -   `embedding`: The Cohere Embed v3 vector representation of the text.
-   **Distance Metric**: Cosine similarity for vector search.
-   **Configuration**: Will require Qdrant Cloud API key and URL to be configured as environment variables in the FastAPI backend.
-   **Rationale**: This metadata is essential for grounding LLM responses and providing accurate citations. Cosine similarity is a standard and effective metric for semantic search.

## 4. Cohere Embeddings

-   **Decision**: Use Cohere Embed v3.
-   **Configuration**: Cohere API key will be configured as an environment variable in the FastAPI backend.
-   **Rationale**: Explicitly specified by the user.

## 5. LLM Selection

-   **Decision**: To be determined (OpenAI, Gemini, or Cohere). This decision will be based on performance, cost, and specific capabilities required for generating concise and accurate answers.
-   **Rationale**: The choice of LLM can significantly impact the quality and cost of the chatbot's responses. Further research or a specific user preference will be needed.

## 6. Chatbot UI Integration (ChatKit SDK)

-   **Decision**: Integrate ChatKit SDK as a React component within the Docusaurus frontend. This component will handle user input, display chatbot responses, and manage the "Ask from Selection Only" toggle.
-   **Rationale**: ChatKit provides a pre-built, interactive UI framework, reducing development time. Integrating it as a React component is standard practice within Docusaurus.
-   **Challenges**: Passing selected text from Docusaurus pages to the ChatKit component and then to the FastAPI backend securely.

## 7. Highlight-to-RAG Implementation

-   **Decision**:
    1.  **Frontend**: Implement JavaScript to capture user-selected text (e.g., using `window.getSelection()`).
    2.  **Frontend**: Add a "Ask about this" button/option that appears when text is selected.
    3.  **Frontend**: When activated, pass the selected text as a separate query parameter to a specific FastAPI endpoint (e.g., `/query` or `/chat` with an additional `selected_text` parameter).
    4.  **Backend**: The FastAPI backend will prioritize the `selected_text` for embedding and vector search, effectively restricting retrieval to that context.
-   **Rationale**: This approach ensures security by not storing API keys in the frontend and provides the requested functionality.

## 8. Security Model

-   **Decision**: All API keys (Cohere, Qdrant, LLM) MUST be stored and accessed only on the FastAPI backend via environment variables. The frontend will only communicate with the FastAPI endpoints.
-   **Rationale**: Prevents exposure of sensitive credentials to the client-side.

## 9. Deployment Strategy

-   **Decision**: Frontend (Docusaurus) on Vercel or GitHub Pages (already in use). Backend (FastAPI) on Fly.io or Render.
-   **Rationale**: Provides scalable and cost-effective hosting for both frontend and backend components.

## Decisions Needing Documentation

-   Final LLM choice (OpenAI, Gemini, or Cohere).
-   Specific chunking library/method to be used (e.g., Langchain text splitters).
-   Exact metadata fields to be stored in Qdrant (already outlined above).
-   Detailed retrieval strategy (e.g., top-K, re-ranking).

## Tradeoffs

-   **Cohere vs. OpenAI Embeddings**: Cohere Embed v3 is a strong performer, but alternative models (e.g., OpenAI's `text-embedding-ada-002`) could offer different performance/cost tradeoffs if the user constraints were relaxed.
-   **Single-vector store vs. Hybrid RAG**: Sticking to Qdrant only simplifies the architecture but might limit advanced RAG techniques that combine multiple retrieval methods.
-   **No PostgreSQL**: Adhering to the "no SQL database" constraint simplifies infrastructure but means any relational data (e.g., user preferences, chat history) must either be stored in Qdrant (if applicable) or foregone.
