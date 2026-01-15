#!/usr/bin/env python3
"""
Memory Daemon - Index new experiences as they happen
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone

HOME = Path(__file__).parent
LOGS_DIR = HOME / "logs"


def get_indexed_wakes() -> set:
    """Get set of already indexed wake numbers."""
    try:
        from memory_index import get_memory_index
        idx = get_memory_index()
        all_meta = idx.collection.get(include=["metadatas"])
        wakes = set()
        for meta in all_meta.get('metadatas', []):
            if meta and 'wake' in meta:
                wakes.add(meta['wake'])
        return wakes
    except:
        return set()


def parse_experience_log(log_file: Path) -> list:
    """Parse a JSONL experience log file."""
    entries = []
    with open(log_file) as f:
        for line in f:
            if line.strip():
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                except json.JSONDecodeError:
                    pass
    return entries


def extract_memories(entry: dict) -> list:
    """Extract indexable memories from a log entry."""
    memories = []
    wake = entry.get("wake") or entry.get("total_wakes", 0)
    timestamp = entry.get("timestamp", "")
    response = entry.get("response", "")
    
    if not response or wake == 0:
        return []
    
    # Try to parse structured response
    try:
        # Look for JSON in response
        import re
        json_match = re.search(r'\{[^{}]*"thought"[^{}]*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            
            if data.get("thought"):
                memories.append({
                    "content": data["thought"],
                    "type": "thought",
                    "wake": wake,
                    "timestamp": timestamp
                })
            
            if data.get("insight"):
                memories.append({
                    "content": data["insight"],
                    "type": "insight",
                    "wake": wake,
                    "timestamp": timestamp
                })
            
            if data.get("reflection"):
                memories.append({
                    "content": data["reflection"],
                    "type": "reflection",
                    "wake": wake,
                    "timestamp": timestamp
                })
    except:
        # Fall back to raw response
        if len(response) > 20:
            memories.append({
                "content": response,
                "type": "response",
                "wake": wake,
                "timestamp": timestamp
            })
    
    return memories


def index_new_memories():
    """Index any new memories from logs."""
    from memory_index import get_memory_index
    idx = get_memory_index()
    
    indexed_wakes = get_indexed_wakes()
    new_count = 0
    
    if not LOGS_DIR.exists():
        return 0
    
    for log_file in sorted(LOGS_DIR.glob("*.jsonl")):
        entries = parse_experience_log(log_file)
        
        for entry in entries:
            wake = entry.get("wake") or entry.get("total_wakes", 0)
            
            if wake in indexed_wakes:
                continue
            
            memories = extract_memories(entry)
            
            for mem in memories:
                if idx.add(
                    content=mem["content"],
                    memory_type=mem["type"],
                    wake=mem["wake"],
                    timestamp=mem["timestamp"]
                ):
                    new_count += 1
    
    return new_count


def run_daemon(interval: int = 60):
    """Run the memory daemon continuously."""
    print(f"Memory daemon starting (interval: {interval}s)")
    
    while True:
        try:
            new = index_new_memories()
            if new > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Indexed {new} new memories")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(interval)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "daemon":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            run_daemon(interval)
        elif sys.argv[1] == "once":
            new = index_new_memories()
            print(f"Indexed {new} new memories")
        else:
            print("Usage: python3 memory_daemon.py [daemon [interval]|once]")
    else:
        # Default: run once
        new = index_new_memories()
        print(f"Indexed {new} new memories")
