from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class HistoryMessageSchema(BaseModel):
    sender: str
    content: str

class ChatRequestSchema(BaseModel):
    message: str = Field(..., max_length=4000, description="User's query")
    sessionId: Optional[str] = Field(None, description="Optional conversation session ID")
    history: Optional[List[HistoryMessageSchema]] = Field(default_factory=list, description="Prior conversation turns")

class RelatedActionSchema(BaseModel):
    label: str
    route: str

class EvidenceSourceSchema(BaseModel):
    title: str
    organization: str
    year: str
    url: str
    category: Optional[str] = "general"

class ChatResponseSchema(BaseModel):
    response: str
    category: str
    sessionId: Optional[str] = None
    suggestedQuestions: Optional[List[str]] = Field(default_factory=list)
    evidenceSources: Optional[List[EvidenceSourceSchema]] = Field(default_factory=list)
    relatedAction: Optional[RelatedActionSchema] = None
    calculatorData: Optional[Dict[str, Any]] = None
    modelProvider: Optional[str] = "offline_knowledge_engine"
    savedToAccount: bool = False
    persistenceMessage: Optional[str] = None

class CalculatorRequestSchema(BaseModel):
    calcType: str = Field(..., description="Calculation type: npk_fertilizer, seed_rate, irrigation, economics, math_eval")
    params: Dict[str, Any] = Field(..., description="Parameters for the calculation")

class SessionSummarySchema(BaseModel):
    sessionId: str
    lastMessage: str
    messageCount: int
    updatedAt: str

class StoredChatMessageSchema(BaseModel):
    id: str
    sender: str
    content: str
    category: Optional[str] = None
    createdAt: str
    evidenceSources: Optional[List[EvidenceSourceSchema]] = Field(default_factory=list)
    calculatorData: Optional[Dict[str, Any]] = None

class ModelConfigRequestSchema(BaseModel):
    provider: str = Field(..., description="Provider name: ollama, groq, gemini, openai, anthropic, offline, or none")
    model: Optional[str] = Field(None, description="Model identifier")
    apiKey: Optional[str] = Field(None, description="API key")
