"""
Unit tests for Knowledge Loader
"""

import pytest
from knowledge_loader import KnowledgeLoader

@pytest.fixture
def knowledge_loader():
    """Create knowledge loader instance"""
    return KnowledgeLoader()

def test_load_knowledge_base(knowledge_loader):
    """Test knowledge base loading"""
    assert len(knowledge_loader.entries) > 0
    assert all("id" in entry for entry in knowledge_loader.entries)
    assert all("title" in entry for entry in knowledge_loader.entries)

def test_get_entry(knowledge_loader):
    """Test getting specific entry"""
    entry = knowledge_loader.get_entry("kb_audio_001")
    
    assert entry is not None
    assert entry["id"] == "kb_audio_001"
    assert "title" in entry
    assert "content" in entry

def test_get_nonexistent_entry(knowledge_loader):
    """Test getting non-existent entry"""
    entry = knowledge_loader.get_entry("kb_nonexistent")
    
    assert entry is None

def test_search_basic(knowledge_loader):
    """Test basic search"""
    results = knowledge_loader.search("audio dropout")
    
    assert len(results) > 0
    assert all("relevance" in r for r in results)
    assert results[0]["relevance"] > 0

def test_search_with_category(knowledge_loader):
    """Test search with category filter"""
    results = knowledge_loader.search("performance", category="performance")
    
    assert len(results) > 0
    assert all(r["category"] == "performance" for r in results)

def test_search_relevance_ordering(knowledge_loader):
    """Test search results are ordered by relevance"""
    results = knowledge_loader.search("audio")
    
    if len(results) > 1:
        for i in range(len(results) - 1):
            assert results[i]["relevance"] >= results[i + 1]["relevance"]

def test_get_categories(knowledge_loader):
    """Test getting categories"""
    categories = knowledge_loader.get_categories()
    
    assert len(categories) > 0
    assert all("id" in cat for cat in categories)
    assert all("count" in cat for cat in categories)

def test_search_limit(knowledge_loader):
    """Test search result limit"""
    results = knowledge_loader.search("cubase", limit=3)
    
    assert len(results) <= 3
