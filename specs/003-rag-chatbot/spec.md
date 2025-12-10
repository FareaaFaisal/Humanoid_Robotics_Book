# Feature Specification: Integrated RAG Chatbot

**Feature Branch**: `003-rag-chatbot`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description: "Feature Name: Integrated RAG Chatbot for the Docusaurus Book..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Global Book QA (Priority: P1)

As a reader, I want to ask questions about the book's content in a chatbot and receive accurate, context-aware answers, so that I can quickly clarify concepts without searching manually.

**Why this priority**: This is the core functionality of the RAG chatbot and provides the most immediate value to the user.

**Independent Test**: The chatbot is visible on all pages and can answer a question like "What is the purpose of ROS2 topics?" with an accurate, cited answer from the book's content.

**Acceptance Scenarios**:
1. **Given** a user is on any page of the Docusaurus book, **When** they open the chatbot widget and ask a question about the book's content, **Then** the chatbot returns an accurate answer with citations to the source chapters/sections.
2. **Given** the chatbot is open, **When** the user is not highlighting any text, **Then** the chatbot is in "Global QA" mode.

---

### User Story 2 - Highlight-to-Ask (Priority: P2)

As a reader, I want to highlight a specific section of text and ask a question about it, so that I can get a focused explanation of a particular concept or paragraph.

**Why this priority**: This feature provides a more granular and contextual way for users to interact with the content, enhancing the learning experience.

**Independent Test**: A user can highlight a paragraph, click "Ask about this", and ask "Explain this paragraph". The chatbot should respond with an explanation based only on the selected text.

**Acceptance Scenarios**:
1. **Given** a user has highlighted a section of text, **When** they activate the "Ask from Selection Only" mode and ask a question, **Then** the chatbot's answer is based solely on the highlighted text.
2. **Given** the user has asked a question about a selection, **When** they deselect the text and ask another question, **Then** the chatbot reverts to "Global QA" mode.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A floating chatbot widget MUST appear on every page of the published book.
- **FR-002**: The chatbot UI MUST be implemented using the OpenAI ChatKit SDK (or a similar agent-framework UI).
- **FR-003**: The backend MUST be implemented using FastAPI.
- **FR-004**: Vector storage and search MUST be handled by Qdrant Cloud (Free Tier).
- **FR-005**: Text embedding MUST be done using Cohere embeddings (Embed v3 preferred).
- **FR-006**: The FastAPI backend MUST expose `/embed`, `/query`, `/chat`, and `/ingest` endpoints.
- **FR-007**: The chatbot MUST support two modes: global QA and highlight-based QA.
- **FR-008**: All API keys and sensitive credentials MUST NOT be exposed in the frontend.
- **FR-009**: Chat responses MUST cite the source chapters/sections used to generate the answer.
- **FR-010**: No relational database (e.g., PostgreSQL) shall be used; Qdrant is the sole persistent storage.

### Key Entities
- **ChatbotWidget**: The floating UI component embedded in the Docusaurus site.
- **FastAPIBackend**: The server-side application that orchestrates the RAG pipeline.
- **QdrantVectorStore**: The cloud-based vector database that stores and searches the book's content.
- **CohereEmbeddings**: The model used to convert text chunks into vector embeddings.
- **ContentChunk**: A preprocessed chunk of text from the book (300-500 tokens) stored in Qdrant with metadata (id, text, chapter, section, url, embedding).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The chatbot widget successfully loads on 100% of the book's pages.
- **SC-002**: End-to-end latency for a global RAG query is less than 5 seconds.
- **SC-003**: Vector search latency is less than 2 seconds.
- **SC-004**: The "Highlight QA" mode correctly restricts context to the selected text in 100% of tests.
- **SC-005**: The system successfully deploys and runs in a production environment (e.g., Vercel + Fly.io/Render).
