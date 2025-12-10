# Data Model & API Contracts: Integrated RAG Chatbot

This document defines the data structures for the RAG chatbot, including the FastAPI API request/response schemas and the Qdrant vector store schema.

## 1. Qdrant Vector Schema (Collection: `docusaurus_chunks`)

The Qdrant collection will store vectorized content chunks from the Docusaurus book.

-   **Collection Name**: `docusaurus_chunks`
-   **Vector Size**: Determined by Cohere Embed v3 output dimension (e.g., 1024 or 4096, depending on model variant).
-   **Distance Metric**: Cosine Similarity.
-   **Payload Fields (Metadata)**: Each vector will have the following associated metadata:
    -   `id` (string): Unique identifier for the chunk.
    -   `text` (string): The raw text content of the chunk (max ~500 tokens).
    -   `chapter` (string): Title of the chapter.
    -   `section` (string): Title of the section/subsection.
    -   `url` (string): The full URL to the Docusaurus page.
    -   `embedding` (list of floats): The Cohere Embed v3 vector (not directly stored in payload, but associated with the point).
    -   `is_highlight_chunk` (boolean, optional): Flag to indicate if this chunk originated from a user highlight, used during highlight-to-RAG.

## 2. FastAPI API Contracts

The FastAPI backend will expose the following REST endpoints:

### 2.1. `/ingest` (POST)

Endpoint for bulk ingestion of Docusaurus content into Qdrant. This will be a one-time or on-update process.

-   **Description**: Ingests Docusaurus content (MDX files) by chunking, embedding, and storing in Qdrant.
-   **Request Body**:
    ```json
    {
      "files": [
        {
          "path": "/path/to/chapter1.mdx",
          "content": "Markdown content of chapter 1..."
        },
        {
          "path": "/path/to/chapter2.md",
          "content": "Markdown content of chapter 2..."
        }
      ]
    }
    ```
-   **Response Body (Success 200)**:
    ```json
    {
      "status": "success",
      "ingested_count": 500,
      "message": "Successfully ingested 500 chunks into Qdrant."
    }
    ```
-   **Response Body (Error 400/500)**:
    ```json
    {
      "status": "error",
      "message": "Detailed error message"
    }
    ```

### 2.2. `/embed` (POST)

Endpoint for generating embeddings for arbitrary text. Primarily for internal use or testing.

-   **Description**: Generates Cohere embeddings for a given text.
-   **Request Body**:
    ```json
    {
      "text": "The quick brown fox jumps over the lazy dog."
    }
    ```
-   **Response Body (Success 200)**:
    ```json
    {
      "embedding": [0.123, 0.456, ..., 0.789]
    }
    ```
-   **Response Body (Error 400/500)**:
    ```json
    {
      "status": "error",
      "message": "Detailed error message"
    }
    ```

### 2.3. `/query` (POST)

Endpoint for performing vector similarity search in Qdrant.

-   **Description**: Searches Qdrant for relevant chunks based on a query embedding or text.
-   **Request Body**:
    ```json
    {
      "query_text": "What are ROS2 topics?",
      "limit": 5,
      "min_score": 0.7,
      "filters": {
        "chapter": "ROS 2 Architecture",
        "section": "Topics"
      }
    }
    ```
-   **Response Body (Success 200)**:
    ```json
    {
      "results": [
        {
          "id": "chunk_abc123",
          "text": "ROS 2 topics are a publish-subscribe mechanism...",
          "score": 0.85,
          "metadata": {
            "chapter": "ROS 2 Architecture",
            "section": "Topics",
            "url": "https://example.com/docs/ros2-architecture#topics"
          }
        }
      ]
    }
    ```
-   **Response Body (Error 400/500)**:
    ```json
    {
      "status": "error",
      "message": "Detailed error message"
    }
    ```

### 2.4. `/chat` (POST)

Endpoint for generating RAG-powered chat responses.

-   **Description**: Takes a user query, performs RAG using Qdrant, and generates an LLM response.
-   **Request Body**:
    ```json
    {
      "user_message": "How do humanoids use actions?",
      "selected_text_context": "When a humanoid performs a walking action...", // Optional, for highlight-to-RAG
      "chat_history": [
        {"role": "user", "content": "What is ROS?"},
        {"role": "assistant", "content": "ROS is a middleware..."}
      ]
    }
    ```
-   **Response Body (Success 200 - Streaming)**:
    ```json
    {
      "response": "LLM generated response here...",
      "citations": [
        {
          "chapter": "ROS 2 Architecture",
          "section": "Actions",
          "url": "https://example.com/docs/ros2-architecture#actions"
        }
      ],
      "similarity_scores": [
        {"id": "chunk_abc123", "score": 0.85},
        {"id": "chunk_xyz456", "score": 0.78}
      ]
    }
    ```
-   **Response Body (Error 400/500)**:
    ```json
    {
      "status": "error",
      "message": "Detailed error message"
    }
    ```
