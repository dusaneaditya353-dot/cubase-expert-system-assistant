"""
Knowledge Base Loader - Loads and manages Cubase knowledge base
"""

import json
import os
from typing import List, Dict, Optional
from difflib import SequenceMatcher

class KnowledgeLoader:
    """
    Loads and manages the Cubase knowledge base
    Provides search and retrieval functionality
    """
    
    def __init__(self, kb_path: str = "../knowledge-base"):
        self.kb_path = kb_path
        self.entries = self._load_knowledge_base()
        self.categories = self._build_categories()
    
    def _load_knowledge_base(self) -> List[Dict]:
        """Load all knowledge base entries"""
        entries = []
        
        # In-memory knowledge base (in production, load from files/database)
        entries = [
            {
                "id": "kb_audio_001",
                "title": "Audio Dropout Troubleshooting",
                "category": "performance",
                "content": "Audio dropouts occur when the CPU cannot process audio in real-time. Solutions: 1) Increase buffer size in Studio > Studio Setup > Audio System. Try 512 or 1024 samples. 2) Freeze or render heavy tracks. 3) Disable unused plugins. 4) Update ASIO drivers. 5) Close background applications.",
                "tags": ["audio", "performance", "troubleshooting", "buffer", "asio"],
                "last_updated": "2025-12-01"
            },
            {
                "id": "kb_latency_001",
                "title": "Reducing Latency in Cubase",
                "category": "performance",
                "content": "Latency is the delay between input and output. To reduce: 1) Lower buffer size (128-256 samples for recording). 2) Enable Direct Monitoring on your audio interface. 3) Use ASIO drivers (Windows) or Core Audio (Mac). 4) Disable Control Room if not needed. 5) Use Constrain Delay Compensation during recording.",
                "tags": ["latency", "performance", "recording", "monitoring", "asio"],
                "last_updated": "2025-12-01"
            },
            {
                "id": "kb_export_001",
                "title": "Exporting Audio from Cubase",
                "category": "workflow",
                "content": "To export audio: 1) Set left/right locators around the section to export. 2) Go to File > Export > Audio Mixdown. 3) Choose file format (WAV for quality, MP3 for sharing). 4) Set sample rate (44.1kHz or 48kHz) and bit depth (24-bit recommended). 5) Select output channels. 6) Click Export.",
                "tags": ["export", "workflow", "mixdown", "audio", "file"],
                "last_updated": "2025-12-01"
            },
            {
                "id": "kb_plugin_001",
                "title": "Plugin Crash Prevention",
                "category": "stability",
                "content": "Plugin crashes can destabilize Cubase. Prevention: 1) Keep plugins updated. 2) Use Plugin Manager to blacklist problematic plugins. 3) Scan plugins on startup (Preferences > Plug-ins). 4) Use VST3 over VST2 when possible. 5) Run plugins in separate processes (Preferences > VST Plug-ins > Run in separate process).",
                "tags": ["plugin", "vst", "crash", "stability", "troubleshooting"],
                "last_updated": "2025-12-01"
            },
            {
                "id": "kb_midi_001",
                "title": "MIDI Setup and Troubleshooting",
                "category": "midi",
                "content": "MIDI setup: 1) Connect MIDI controller. 2) Go to Studio > Studio Setup > MIDI Port Setup. 3) Enable 'In All MIDI Inputs' for the device. 4) Create MIDI track and select input. 5) Enable record and monitor. Troubleshooting: Check MIDI cables, verify driver installation, test in standalone mode.",
                "tags": ["midi", "controller", "input", "setup", "troubleshooting"],
                "last_updated": "2025-12-01"
            },
            {
                "id": "kb_cpu_001",
                "title": "CPU Optimization Techniques",
                "category": "performance",
                "content": "Optimize CPU usage: 1) Freeze tracks with heavy plugins (Track > Freeze). 2) Increase buffer size during mixing. 3) Disable unused tracks. 4) Use track versions instead of duplicates. 5) Render MIDI to audio. 6) Adjust ASIO-Guard settings. 7) Use lower quality settings for reverbs during production.",
                "tags": ["cpu", "performance", "optimization", "freeze", "asio"],
                "last_updated": "2025-12-01"
            },
            {
                "id": "kb_routing_001",
                "title": "Audio Routing Basics",
                "category": "workflow",
                "content": "Audio routing in Cubase: 1) Outputs: Set in Inspector or MixConsole. 2) Groups: Create Group Channel for submixing. 3) Sends: Add FX Channel for reverb/delay. 4) Direct Routing: Route track directly to another track. 5) Sidechain: Use sidechain routing for compression/gating.",
                "tags": ["routing", "workflow", "mixing", "audio", "channels"],
                "last_updated": "2025-12-01"
            },
            {
                "id": "kb_shortcuts_001",
                "title": "Essential Keyboard Shortcuts",
                "category": "workflow",
                "content": "Essential shortcuts: Ctrl+S (Save), Ctrl+D (Duplicate), Ctrl+K (Split), F3 (MixConsole), F4 (Pool), Numpad * (Record), Numpad 0 (Stop), Space (Play/Stop), L (Loop), Ctrl+Z (Undo). Customize in File > Key Commands.",
                "tags": ["shortcuts", "workflow", "productivity", "keyboard"],
                "last_updated": "2025-12-01"
            }
        ]
        
        return entries
    
    def _build_categories(self) -> List[Dict]:
        """Build category index"""
        category_map = {}
        
        for entry in self.entries:
            cat = entry["category"]
            if cat not in category_map:
                category_map[cat] = {"id": cat, "name": cat.title(), "count": 0}
            category_map[cat]["count"] += 1
        
        return list(category_map.values())
    
    def get_entry(self, entry_id: str) -> Optional[Dict]:
        """Get specific knowledge base entry"""
        for entry in self.entries:
            if entry["id"] == entry_id:
                return entry
        return None
    
    def search(self, query: str, category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Search knowledge base with relevance scoring
        """
        query_lower = query.lower()
        results = []
        
        for entry in self.entries:
            # Filter by category if specified
            if category and entry["category"] != category:
                continue
            
            # Calculate relevance score
            relevance = self._calculate_relevance(query_lower, entry)
            
            if relevance > 0.1:  # Threshold
                results.append({
                    **entry,
                    "relevance": relevance,
                    "excerpt": entry["content"][:200] + "..."
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return results[:limit]
    
    def _calculate_relevance(self, query: str, entry: Dict) -> float:
        """Calculate relevance score for search result"""
        score = 0.0
        
        # Title match (highest weight)
        title_lower = entry["title"].lower()
        if query in title_lower:
            score += 1.0
        else:
            score += SequenceMatcher(None, query, title_lower).ratio() * 0.5
        
        # Content match
        content_lower = entry["content"].lower()
        if query in content_lower:
            score += 0.5
        
        # Tag match
        for tag in entry.get("tags", []):
            if query in tag.lower():
                score += 0.3
        
        # Keyword match
        query_words = query.split()
        for word in query_words:
            if len(word) > 3:  # Skip short words
                if word in content_lower:
                    score += 0.1
        
        return min(score, 1.0)
    
    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        return self.categories
