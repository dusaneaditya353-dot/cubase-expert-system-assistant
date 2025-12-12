"""
API Integration Tests
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_query_endpoint_success():
    """Test successful query"""
    response = client.post(
        "/api/query",
        json={
            "query": "How do I fix audio dropouts?",
            "context": {"version": "13"}
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "confidence" in data
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)

def test_query_endpoint_empty_query():
    """Test empty query handling"""
    response = client.post(
        "/api/query",
        json={"query": ""}
    )
    
    assert response.status_code == 400

def test_get_knowledge_entry():
    """Test getting knowledge entry"""
    response = client.get("/api/knowledge/kb_audio_001")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "kb_audio_001"
    assert "title" in data

def test_get_nonexistent_knowledge_entry():
    """Test getting non-existent entry"""
    response = client.get("/api/knowledge/kb_nonexistent")
    
    assert response.status_code == 404

def test_search_knowledge():
    """Test knowledge search"""
    response = client.get("/api/knowledge/search?q=audio")
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total" in data
    assert isinstance(data["results"], list)

def test_search_knowledge_empty_query():
    """Test search with empty query"""
    response = client.get("/api/knowledge/search?q=")
    
    assert response.status_code == 400

def test_list_categories():
    """Test listing categories"""
    response = client.get("/api/categories")
    
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert isinstance(data["categories"], list)

def test_submit_feedback():
    """Test feedback submission"""
    response = client.post(
        "/api/feedback",
        json={
            "query_id": "test_123",
            "rating": 5,
            "comment": "Very helpful!",
            "helpful": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
