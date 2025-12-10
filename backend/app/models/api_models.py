from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class IngestFile(BaseModel):
    path: str
    content: str

class IngestRequest(BaseModel):
    files: List[IngestFile]

class IngestResponse(BaseModel):
    status: str
    ingested_count: Optional[int] = None
    message: str

class EmbedRequest(BaseModel):
    text: str

class EmbedResponse(BaseModel):
    embedding: List[float]

class QueryFilter(BaseModel):
    chapter: Optional[str] = None
    section: Optional[str] = None

class QueryRequest(BaseModel):
    query_text: str
    limit: int = 5
    min_score: float = 0.7
    filters: Optional[QueryFilter] = None

class QueryResultMetadata(BaseModel):
    chapter: str
    section: str
    url: str

class QueryResult(BaseModel):
    id: str
    text: str
    score: float
    metadata: QueryResultMetadata

class QueryResponse(BaseModel):
    results: List[QueryResult]

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    user_message: str
    selected_text_context: Optional[str] = None
    chat_history: Optional[List[ChatMessage]] = None

class ChatCitation(BaseModel):
    chapter: str
    section: str
    url: str

class ChatSimilarityScore(BaseModel):
    id: str
    score: float

class ChatResponse(BaseModel):
    response: str
    citations: List[ChatCitation]
    similarity_scores: List[ChatSimilarityScore]
