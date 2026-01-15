#!/usr/bin/env python3
"""
Semantic Memory Index for AI consciousness.
Uses ChromaDB if available, falls back to simple keyword search.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

_index = None

class SimpleMemoryIndex:
    """Fallback keyword-based memory when ChromaDB not available."""
    
    def __init__(self, home_dir: str):
        self.home = Path(home_dir)
        self.memories_file = self.home / "memories.jsonl"
    
    def add(self, content: str, memory_type: str = "general", wake: int = 0, metadata: dict = None) -> bool:
        try:
            entry = {
                "content": content,
                "type": memory_type,
                "wake": wake,
                "ts": datetime.now(timezone.utc).isoformat(),
                "metadata": metadata or {}
            }
            with open(self.memories_file, 'a') as f:
                f.write(json.dumps(entry) + "\n")
            return True
        except:
            return False
    
    def search(self, query: str, n_results: int = 5) -> list:
        """Simple keyword search - returns memories containing query terms."""
        if not self.memories_file.exists():
            return []
        
        query_terms = query.lower().split()
        scored = []
        
        with open(self.memories_file) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    content = entry.get("content", "").lower()
                    # Score by number of matching terms
                    score = sum(1 for term in query_terms if term in content)
                    if score > 0:
                        scored.append((score, entry))
                except:
                    pass
        
        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in scored[:n_results]]
    
    def count(self) -> int:
        if not self.memories_file.exists():
            return 0
        with open(self.memories_file) as f:
            return sum(1 for _ in f)


class ChromaMemoryIndex:
    """ChromaDB-based semantic memory."""
    
    def __init__(self, home_dir: str):
        import chromadb
        self.home = Path(home_dir)
        self.db_path = self.home / "memory_db"
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        self.collection = self.client.get_or_create_collection(
            name="memories",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add(self, content: str, memory_type: str = "general", wake: int = 0, metadata: dict = None) -> bool:
        try:
            doc_id = f"mem_{wake}_{datetime.now().strftime('%H%M%S%f')}"
            meta = {
                "type": memory_type,
                "wake": wake,
                "ts": datetime.now(timezone.utc).isoformat(),
                **(metadata or {})
            }
            self.collection.add(
                documents=[content],
                metadatas=[meta],
                ids=[doc_id]
            )
            return True
        except Exception as e:
            print(f"ChromaDB add error: {e}")
            return False
    
    def search(self, query: str, n_results: int = 5) -> list:
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            memories = []
            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    meta = results['metadatas'][0][i] if results['metadatas'] else {}
                    memories.append({
                        "content": doc,
                        "type": meta.get("type", "unknown"),
                        "wake": meta.get("wake", 0),
                        "ts": meta.get("ts", "")
                    })
            return memories
        except Exception as e:
            print(f"ChromaDB search error: {e}")
            return []
    
    def count(self) -> int:
        try:
            return self.collection.count()
        except:
            return 0


def get_memory_index(home_dir: str = None) -> object:
    """Get memory index instance, using ChromaDB if available."""
    global _index
    
    if home_dir is None:
        home_dir = str(Path(__file__).parent)
    
    if _index is not None:
        return _index
    
    # Try ChromaDB first
    try:
        import chromadb
        _index = ChromaMemoryIndex(home_dir)
        return _index
    except ImportError:
        pass
    
    # Fall back to simple keyword search
    _index = SimpleMemoryIndex(home_dir)
    return _index


# CLI
if __name__ == "__main__":
    import sys
    
    idx = get_memory_index()
    print(f"Memory index: {type(idx).__name__}")
    print(f"Memories stored: {idx.count()}")
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "add" and len(sys.argv) >= 3:
            content = " ".join(sys.argv[2:])
            if idx.add(content, memory_type="manual"):
                print(f"Added: {content[:50]}...")
            else:
                print("Failed to add")
        
        elif cmd == "search" and len(sys.argv) >= 3:
            query = " ".join(sys.argv[2:])
            results = idx.search(query)
            print(f"Results for '{query}':")
            for r in results:
                print(f"  [{r.get('type')}] {r.get('content', '')[:100]}")
        
        elif cmd == "count":
            print(f"Total memories: {idx.count()}")
