"""
Expert System Engine - Core reasoning and inference logic
"""

from typing import Dict, List, Optional
import re
from difflib import SequenceMatcher

class ExpertEngine:
    """
    Expert system engine for Cubase troubleshooting
    Uses rule-based reasoning and pattern matching
    """
    
    def __init__(self, knowledge_loader):
        self.knowledge = knowledge_loader
        self.rules = self._load_rules()
    
    def _load_rules(self) -> List[Dict]:
        """Load inference rules"""
        return [
            {
                "pattern": r"audio.*dropout|dropout.*audio|crackling|popping",
                "category": "performance",
                "keywords": ["buffer", "asio", "latency", "cpu"],
                "priority": 1
            },
            {
                "pattern": r"latency|delay|lag",
                "category": "performance",
                "keywords": ["buffer", "asio", "driver", "monitoring"],
                "priority": 1
            },
            {
                "pattern": r"export|bounce|render",
                "category": "workflow",
                "keywords": ["export", "mixdown", "format", "settings"],
                "priority": 2
            },
            {
                "pattern": r"plugin.*crash|vst.*crash|crash.*plugin",
                "category": "stability",
                "keywords": ["plugin", "vst", "crash", "compatibility"],
                "priority": 1
            },
            {
                "pattern": r"midi.*not.*work|midi.*problem",
                "category": "midi",
                "keywords": ["midi", "controller", "input", "routing"],
                "priority": 2
            },
            {
                "pattern": r"cpu.*high|cpu.*overload|performance",
                "category": "performance",
                "keywords": ["cpu", "optimization", "freeze", "render"],
                "priority": 1
            }
        ]
    
    def process_query(self, query: str, context: Dict) -> Dict:
        """
        Process user query and generate expert response
        """
        query_lower = query.lower()
        
        # Match rules
        matched_rules = self._match_rules(query_lower)
        
        # Search knowledge base
        kb_results = self.knowledge.search(query, limit=5)
        
        # Generate answer
        answer = self._generate_answer(query, matched_rules, kb_results, context)
        
        # Calculate confidence
        confidence = self._calculate_confidence(matched_rules, kb_results)
        
        # Extract sources
        sources = [r["id"] for r in kb_results[:3]]
        
        # Generate suggestions
        suggestions = self._generate_suggestions(matched_rules, kb_results)
        
        # Find related topics
        related_topics = self._find_related_topics(matched_rules, kb_results)
        
        return {
            "answer": answer,
            "confidence": confidence,
            "sources": sources,
            "suggestions": suggestions,
            "related_topics": related_topics
        }
    
    def _match_rules(self, query: str) -> List[Dict]:
        """Match query against inference rules"""
        matched = []
        for rule in self.rules:
            if re.search(rule["pattern"], query, re.IGNORECASE):
                matched.append(rule)
        
        # Sort by priority
        matched.sort(key=lambda x: x["priority"])
        return matched
    
    def _generate_answer(self, query: str, rules: List[Dict], kb_results: List[Dict], context: Dict) -> str:
        """Generate comprehensive answer"""
        
        if not kb_results:
            return "I don't have specific information about that. Please try rephrasing your question or check the Cubase documentation."
        
        # Use top knowledge base result
        top_result = kb_results[0]
        
        # Build answer from knowledge base
        answer_parts = []
        
        # Add context-aware intro
        if "audio" in query.lower() and "dropout" in query.lower():
            answer_parts.append("Audio dropouts in Cubase are typically caused by insufficient buffer size or CPU overload.")
        elif "latency" in query.lower():
            answer_parts.append("Latency issues can be resolved by adjusting your audio interface settings.")
        elif "export" in query.lower():
            answer_parts.append("To export your project in Cubase:")
        else:
            answer_parts.append(f"Regarding {query}:")
        
        # Add main content
        if "content" in top_result:
            answer_parts.append(top_result["content"][:500])
        
        # Add version-specific info if available
        if context.get("version"):
            answer_parts.append(f"\n\nNote: This applies to Cubase {context['version']}.")
        
        return " ".join(answer_parts)
    
    def _calculate_confidence(self, rules: List[Dict], kb_results: List[Dict]) -> float:
        """Calculate confidence score"""
        confidence = 0.5  # Base confidence
        
        if rules:
            confidence += 0.2
        
        if kb_results:
            # Boost based on relevance
            top_relevance = kb_results[0].get("relevance", 0.5)
            confidence += top_relevance * 0.3
        
        return min(confidence, 1.0)
    
    def _generate_suggestions(self, rules: List[Dict], kb_results: List[Dict]) -> List[str]:
        """Generate actionable suggestions"""
        suggestions = []
        
        # Rule-based suggestions
        for rule in rules[:2]:
            if rule["category"] == "performance":
                suggestions.extend([
                    "Increase buffer size to 512 or 1024 samples",
                    "Disable unnecessary plugins and tracks",
                    "Check ASIO driver settings"
                ])
            elif rule["category"] == "workflow":
                suggestions.extend([
                    "Use File > Export > Audio Mixdown",
                    "Select appropriate file format (WAV/MP3)",
                    "Check export settings for sample rate and bit depth"
                ])
        
        # Remove duplicates
        return list(dict.fromkeys(suggestions))[:5]
    
    def _find_related_topics(self, rules: List[Dict], kb_results: List[Dict]) -> List[str]:
        """Find related topics"""
        topics = set()
        
        for rule in rules:
            topics.update(rule["keywords"])
        
        for result in kb_results[:3]:
            if "tags" in result:
                topics.update(result["tags"])
        
        return list(topics)[:5]
