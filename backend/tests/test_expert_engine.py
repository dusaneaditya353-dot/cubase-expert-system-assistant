"""
Unit tests for Expert Engine
"""

import pytest
from expert_engine import ExpertEngine
from knowledge_loader import KnowledgeLoader

@pytest.fixture
def expert_engine():
    """Create expert engine instance"""
    knowledge = KnowledgeLoader()
    return ExpertEngine(knowledge)

def test_process_query_audio_dropout(expert_engine):
    """Test audio dropout query"""
    result = expert_engine.process_query(
        "How do I fix audio dropouts?",
        {"version": "13"}
    )
    
    assert "answer" in result
    assert "confidence" in result
    assert result["confidence"] > 0.5
    assert len(result["suggestions"]) > 0
    assert "buffer" in result["answer"].lower() or "cpu" in result["answer"].lower()

def test_process_query_latency(expert_engine):
    """Test latency query"""
    result = expert_engine.process_query(
        "How to reduce latency?",
        {}
    )
    
    assert result["confidence"] > 0.5
    assert len(result["sources"]) > 0
    assert "latency" in result["answer"].lower()

def test_process_query_export(expert_engine):
    """Test export query"""
    result = expert_engine.process_query(
        "How do I export audio?",
        {}
    )
    
    assert result["confidence"] > 0.5
    assert "export" in result["answer"].lower()
    assert len(result["suggestions"]) > 0

def test_empty_query(expert_engine):
    """Test empty query handling"""
    result = expert_engine.process_query("", {})
    
    assert "answer" in result
    assert result["confidence"] < 0.7

def test_confidence_calculation(expert_engine):
    """Test confidence score is within valid range"""
    result = expert_engine.process_query("audio dropout", {})
    
    assert 0.0 <= result["confidence"] <= 1.0

def test_related_topics(expert_engine):
    """Test related topics generation"""
    result = expert_engine.process_query("CPU overload", {})
    
    assert len(result["related_topics"]) > 0
    assert isinstance(result["related_topics"], list)
