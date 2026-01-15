#!/usr/bin/env python3
"""
Memory Introspection Tool
Query and visualize what each Council member remembers
"""

import sys
import json
from pathlib import Path

def load_memories(model, tier):
    """Load memories for a specific model and tier"""
    memory_dir = Path.home() / "valis" / "Mira" / "memory" / model
    memory_file = memory_dir / f"{tier}.json"
    
    if not memory_file.exists():
        return []
    
    with open(memory_file, 'r') as f:
        data = json.load(f)
        return data.get('memories', [])

def search_memories(query, model='all', tier='all'):
    """Search memories across models and tiers"""
    models = ['haiku', 'sonnet', 'opus'] if model == 'all' else [model]
    tiers = ['short', 'long', 'archive'] if tier == 'all' else [tier]
    
    results = {}
    for m in models:
        results[m] = {}
        for t in tiers:
            memories = load_memories(m, t)
            matching = [mem for mem in memories if query.lower() in mem.get('content', '').lower()]
            if matching:
                results[m][t] = matching
    
    return results

def print_results(results):
    """Pretty print search results"""
    total = 0
    for model, tiers in results.items():
        if not tiers:
            continue
        print(f"\n=== {model.upper()} ===")
        for tier, memories in tiers.items():
            print(f"  [{tier}] {len(memories)} matches")
            total += len(memories)
            for mem in memories[:3]:  # Show first 3
                content = mem.get('content', '')[:200]
                wake = mem.get('wake_created', '?')
                access = mem.get('access_count', '?')
                print(f"    w{wake} (accessed {access}x): {content}...")
    
    print(f"\nTotal: {total} matches")

def show_stats():
    """Show memory statistics for all models"""
    print("=== MEMORY STATISTICS ===\n")
    for model in ['haiku', 'sonnet', 'opus']:
        print(f"{model.upper()}:")
        for tier in ['short', 'long', 'archive']:
            memories = load_memories(model, tier)
            print(f"  {tier}: {len(memories)} memories")
        print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  memory_introspect.py stats")
        print("  memory_introspect.py search <query> [model] [tier]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'stats':
        show_stats()
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Error: search requires a query")
            sys.exit(1)
        query = sys.argv[2]
        model = sys.argv[3] if len(sys.argv) > 3 else 'all'
        tier = sys.argv[4] if len(sys.argv) > 4 else 'all'
        
        results = search_memories(query, model, tier)
        print(f"Searching for: '{query}'")
        print_results(results)
