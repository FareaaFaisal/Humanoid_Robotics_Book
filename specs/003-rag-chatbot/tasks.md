# Tasks: Integrated RAG Chatbot

**Input**: Design documents from `/specs/003-rag-chatbot/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel
- **[Story]**: Maps to user story (US1, US2, etc.)

## Phase 1: Setup (Backend Project Initialization)
**Purpose**: Initialize the FastAPI backend project and set up basic structure.

- [X] T001 Create `backend/` directory and `backend/requirements.txt`.
- [X] T002 Create `backend/app/` directory and `backend/app/__init__.py`.
- [X] T003 Create `backend/app/main.py` for the FastAPI application.
- [X] T004 Create `backend/.env.example` for environment variables.
- [X] T005 Create `backend/ingestion_script.py` (placeholder).

---

## Phase 2: Foundational Backend Services
**Purpose**: Implement core services for Cohere embeddings, Qdrant interaction, and LLM generation.

- [X] T006 Create `backend/app/services/` directory.
- [X] T007 [P] Create `backend/app/models/api_models.py` for Pydantic models (request/response schemas).
- [X] T008 [P] Implement Cohere embedding client in `backend/app/services/cohere_embed.py`.
- [X] T009 [P] Implement Qdrant client interactions in `backend/app/services/qdrant.py`.
- [X] T010 [P] Implement LLM generation client in `backend/app/services/llm_generation.py`.
- [X] T011 Implement `backend/app/services/chunking.py` for text chunking logic.
- [X] T012 Configure FastAPI in `backend/app/main.py` to load environment variables for API keys (COHERE_API_KEY, QDRANT_HOST, QDRANT_API_KEY, LLM_API_KEY, LLM_MODEL_NAME).

---

## Phase 3: Ingestion Pipeline
**Purpose**: Develop and test the content ingestion process for Docusaurus content into Qdrant.

- [X] T013 Implement Docusaurus content extraction (MDX parsing) in `backend/ingestion_script.py`.
- [X] T014 Implement text chunking (300-500 tokens) with metadata extraction (chapter, section, url) in `backend/ingestion_script.py` using `chunking.py`.
- [X] T015 Implement embedding generation for chunks using `cohere_embed.py` in `backend/ingestion_script.py`.
- [X] T016 Implement upsertion of chunks and embeddings into Qdrant using `qdrant.py` in `backend/ingestion_script.py`.
- [X] T017 Create Qdrant collection `docusaurus_chunks` with specified vector size and cosine distance.
- [X] T018 Run `backend/ingestion_script.py` to ingest initial Docusaurus content.

---

## Phase 4: User Story 1 - Global Book QA (Priority: P1) 🎯 MVP
**Goal**: Implement the core RAG chatbot functionality for answering questions about the entire book.
**Independent Test**: The chatbot can answer "What is the purpose of ROS2 topics?" correctly with citations.

### Implementation for User Story 1
- [X] T019 Implement `/embed` endpoint in `backend/app/main.py` using `cohere_embed.py`.
- [X] T020 Implement `/query` endpoint in `backend/app/main.py` using `qdrant.py`.
- [X] T021 Implement `/chat` endpoint in `backend/app/main.py` for global RAG mode, using `qdrant.py` for retrieval and `llm_generation.py` for response generation.
- [X] T022 Ensure chat responses from `/chat` include citations (chapter, section, url) and similarity scores.
- [X] T023 Create `humanoid-robotics-book/src/components/RAGChatbotWidget/` directory.
- [X] T024 Create `humanoid-robotics-book/src/components/RAGChatbotWidget/index.tsx` for ChatKit UI integration.
- [X] T025 Configure `humanoid-robot-book/docusaurus.config.ts` to embed the `RAGChatbotWidget` on all pages.
- [X] T026 Configure ChatKit UI in `index.tsx` to connect to the FastAPI `/chat` endpoint.

---

## Phase 5: User Story 2 - Highlight-to-Ask (Priority: P2)
**Goal**: Enable the chatbot to answer questions based on user-selected text.
**Independent Test**: Highlighting text and asking "Explain this paragraph" returns a response grounded only in the selected text.

### Implementation for User Story 2
- [X] T027 Implement frontend JavaScript logic to capture user text selections (`window.getSelection()`) in `humanoid-robotics-book/src/components/RAGChatbotWidget/index.tsx`.
- [X] T028 Add a "Ask about this" button/option that appears when text is selected in `humanoid-robotics-book/src/components/RAGChatbotWidget/index.tsx`.
- [X] T029 Modify ChatKit UI to pass `selected_text_context` to the FastAPI `/chat` endpoint.
- [X] T030 Update FastAPI `/chat` endpoint in `backend/app/main.py` to prioritize `selected_text_context` for embedding and retrieval if present.

---

## Phase 6: Testing & Deployment
**Purpose**: Ensure the chatbot is functional, performant, and securely deployed.

- [X] T031 Implement unit tests for `cohere_embed.py`, `qdrant.py`, `llm_generation.py`, `chunking.py`.
- [X] T032 Implement integration tests for the `/ingest` endpoint (verify chunking, embedding, Qdrant storage).
- [X] T033 Implement integration tests for the `/query` and `/chat` endpoints (global RAG, highlight RAG).
- [X] T034 Implement end-to-end tests for the ChatKit UI and FastAPI interaction.
- [X] T035 Configure production deployment for FastAPI (e.g., Fly.io/Render) with environment variables for API keys.
- [X] T036 Update `.github/workflows/deploy_backend.yml` for CI/CD of the FastAPI backend.
- [X] T037 Validate all production deployment checklist items (no API keys in client, env vars loaded, etc.).

---

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1 (Setup)**: No dependencies.
- **Phase 2 (Foundational Backend)**: Depends on Phase 1.
- **Phase 3 (Ingestion Pipeline)**: Depends on Phase 2.
- **Phase 4 (User Story 1 - Global QA)**: Depends on Phase 2 & 3.
- **Phase 5 (User Story 2 - Highlight-to-Ask)**: Depends on Phase 4.
- **Phase 6 (Testing & Deployment)**: Depends on all previous phases.

### User Story Dependencies
- **User Story 1 (P1)**: Can start after Foundational Backend and Ingestion Pipeline are complete.
- **User Story 2 (P2)**: Depends on User Story 1 being complete.

### Within Each Phase / User Story
- Implement core logic before testing.
- Set up clients/configurations before using them.

## Implementation Strategy

### MVP First (User Story 1 Only)
1.  Complete Phase 1: Setup.
2.  Complete Phase 2: Foundational Backend Services.
3.  Complete Phase 3: Ingestion Pipeline.
4.  Complete Phase 4: User Story 1 (Global Book QA).
5.  **STOP and VALIDATE**: Test Global QA functionality independently.
6.  Deploy/demo if ready.

### Incremental Delivery
1.  Complete Setup, Foundational Backend, Ingestion.
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Complete Testing & Deployment.

---

## Notes
- `[P]` tasks can run in parallel.
- All tasks include specific file paths for clarity.
- Focus on security: no API keys in frontend.
- Utilize async capabilities of FastAPI for performance.
