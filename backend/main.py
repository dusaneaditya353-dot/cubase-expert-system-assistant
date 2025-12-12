"""
Cubase Expert System Assistant - Main Backend Server
FastAPI application with expert system engine
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from datetime import datetime
import logging

from expert_engine import ExpertEngine
from knowledge_loader import KnowledgeLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Cubase Expert System API",
    description="AI-powered Cubase troubleshooting and workflow optimization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize expert system
knowledge_loader = KnowledgeLoader()
expert_engine = ExpertEngine(knowledge_loader)

# Request/Response Models
class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, str]] = {}

class QueryResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]
    suggestions: List[str]
    related_topics: List[str]

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

class FeedbackRequest(BaseModel):
    query_id: str
    rating: int
    comment: Optional[str] = ""
    helpful: bool

# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/api/query", response_model=QueryResponse)
async def query_expert_system(request: QueryRequest):
    """
    Query the expert system with a Cubase-related question
    """
    if not request.query or len(request.query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        logger.info(f"Processing query: {request.query}")
        result = expert_engine.process_query(request.query, request.context)
        return result
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/knowledge/{entry_id}")
async def get_knowledge_entry(entry_id: str):
    """Get a specific knowledge base entry"""
    entry = knowledge_loader.get_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    return entry

@app.get("/api/knowledge/search")
async def search_knowledge(q: str, category: Optional[str] = None, limit: int = 10):
    """Search the knowledge base"""
    if not q:
        raise HTTPException(status_code=400, detail="Search query required")
    
    results = knowledge_loader.search(q, category, limit)
    return {
        "results": results,
        "total": len(results),
        "query": q
    }

@app.get("/api/categories")
async def list_categories():
    """List all knowledge base categories"""
    categories = knowledge_loader.get_categories()
    return {"categories": categories}

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback for a query response"""
    logger.info(f"Feedback received for query {feedback.query_id}: {feedback.rating}/5")
    # In production, store this in a database
    return {"success": True, "message": "Feedback recorded"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cubase Expert System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
