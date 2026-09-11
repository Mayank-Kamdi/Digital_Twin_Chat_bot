"""FastAPI Web Application & REST API for LYRA Business Digital Twin."""

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import APP_NAME, APP_VERSION
from backend.models import (
    ChatRequest, ChatResponse, RetrievedSource, ClearMemoryRequest,
    AddFaqRequest, AddPolicyRequest, AddProductRequest, AddDocumentRequest
)
from backend.rag.knowledge_manager import knowledge_manager
from backend.memory.conversation_memory import memory_manager
from backend.llm.llm_service import llm_service
from backend.profile.business_profile import novatech_profile

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Business Digital Twin REST API for LYRA"
)

# CORS middleware for local frontend interactions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """
    Main Chat RAG Endpoint:
    1. Update conversation memory with user query
    2. Retrieve relevant business knowledge chunks with query enrichment
    3. Run LLM grounding & hallucination guardrails
    4. Store assistant response and return full context
    """
    session_id = req.session_id.strip() or "default_session"
    user_msg = req.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # 1. Update session memory with user turn
    memory_manager.add_user_message(session_id, user_msg)
    active_ctx = memory_manager.get_active_context(session_id)
    history = memory_manager.get_history(session_id)

    # 2. RAG Retrieval
    docs, max_score, is_in_domain = knowledge_manager.retrieve(
        query=user_msg,
        context_products=active_ctx.get("mentioned_products", [])
    )
    context_str = knowledge_manager.format_context_for_prompt(docs)

    # 3. LLM Response Generation
    answer, is_guarded, model_used = llm_service.generate_response(
        query=user_msg,
        retrieved_context=context_str,
        retrieved_docs=docs,
        is_in_domain=is_in_domain,
        conversation_history=history[:-1],  # History prior to this message
        requirements=active_ctx.get("requirements", {}),
        mentioned_products=active_ctx.get("mentioned_products", [])
    )

    # 4. Update session memory with assistant turn
    memory_manager.add_assistant_message(session_id, answer)
    updated_ctx = memory_manager.get_active_context(session_id)

    # Format sources for transparency
    sources = []
    for d in docs:
        sources.append(RetrievedSource(
            id=d.get("id", ""),
            title=d.get("title", ""),
            category=d.get("category", ""),
            score=d.get("score", 0.0),
            excerpt=d.get("content", "")[:150] + "..."
        ))

    return ChatResponse(
        session_id=session_id,
        answer=answer,
        sources=sources,
        active_requirements=updated_ctx.get("requirements", {}),
        mentioned_products=updated_ctx.get("mentioned_products", []),
        is_hallucination_guarded=is_guarded,
        model_used=model_used
    )


@app.post("/api/chat/clear")
async def clear_chat_endpoint(req: ClearMemoryRequest):
    """Clears conversation history and active requirements for a session."""
    session_id = req.session_id or "default_session"
    memory_manager.clear_session(session_id)
    return {"status": "success", "message": f"Session '{session_id}' cleared successfully."}


@app.get("/api/profile")
async def get_business_profile():
    """Returns the full structured business profile for LYRA."""
    return novatech_profile.get_full_profile()


@app.get("/api/knowledge")
async def get_knowledge_items():
    """Returns all current indexed knowledge chunks in the vector store."""
    return {"total": len(knowledge_manager.list_knowledge_items()), "items": knowledge_manager.list_knowledge_items()}


@app.post("/api/admin/faq")
async def add_faq_admin(req: AddFaqRequest):
    """Admin endpoint to add a new FAQ and immediately index it."""
    result = knowledge_manager.add_faq(req.question, req.answer)
    return {"status": "success", "data": result}


@app.post("/api/admin/policy")
async def add_policy_admin(req: AddPolicyRequest):
    """Admin endpoint to add a new company policy and immediately index it."""
    result = knowledge_manager.add_policy(req.title, req.summary, req.details, req.category)
    return {"status": "success", "data": result}


@app.post("/api/admin/product")
async def add_product_admin(req: AddProductRequest):
    """Admin endpoint to add a new product or service and index it."""
    result = knowledge_manager.add_product(
        name=req.name,
        category=req.category,
        summary=req.summary,
        best_for=req.best_for,
        pricing=req.pricing,
        features=req.features
    )
    return {"status": "success", "data": result}


@app.post("/api/admin/document")
async def add_document_admin(req: AddDocumentRequest):
    """Admin endpoint to add a general business document and index it."""
    result = knowledge_manager.add_custom_document(req.title, req.content, req.category)
    return {"status": "success", "data": result}


@app.get("/api/health")
async def health_check():
    """System health check."""
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION,
        "indexed_chunks": len(knowledge_manager.list_knowledge_items())
    }


# Mount frontend static files if directory exists
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(FRONTEND_DIR / "index.html")
