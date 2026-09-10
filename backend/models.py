"""Pydantic data models for requests and responses."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(default="default_session", description="Unique conversation session ID")
    message: str = Field(..., min_length=1, description="User question or statement")


class RetrievedSource(BaseModel):
    id: str
    title: str
    category: str
    score: float
    excerpt: str


class ChatResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    session_id: str
    answer: str
    sources: List[RetrievedSource] = []
    active_requirements: Dict[str, Any] = {}
    mentioned_products: List[str] = []
    is_hallucination_guarded: bool = False
    model_used: str = "gemini-3.5-flash"


class ClearMemoryRequest(BaseModel):
    session_id: str = Field(default="default_session")


class AddFaqRequest(BaseModel):
    question: str = Field(..., min_length=3)
    answer: str = Field(..., min_length=5)


class AddPolicyRequest(BaseModel):
    title: str = Field(..., min_length=3)
    summary: str = Field(..., min_length=5)
    details: str = Field(..., min_length=10)
    category: str = Field(default="general")


class AddProductRequest(BaseModel):
    name: str = Field(..., min_length=3)
    category: str = Field(default="custom_software")
    summary: str = Field(..., min_length=5)
    best_for: str = Field(..., min_length=5)
    pricing: Dict[str, str] = Field(...)
    features: List[str] = Field(default_factory=list)


class AddDocumentRequest(BaseModel):
    title: str = Field(..., min_length=3)
    content: str = Field(..., min_length=10)
    category: str = Field(default="custom_document")
