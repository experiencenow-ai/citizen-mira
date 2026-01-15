#!/usr/bin/env python3
"""
Three-Tier Memory System

Tier 1: Facts - key-value, overwrite semantics, always loaded
Tier 2: Working - current state, ephemeral
Tier 3: Archive - append-only, never loaded unless queried
"""

import json
from datetime import datetime, timezone
from pathlib import Path


class Memory:
    def __init__(self, home_dir: Path):
        self.home = Path(home_dir)
        self.facts_file = self.home / "facts.json"
        self.working_file = self.home / "working.json"
        self.archive_dir = self.home / "archive"
        self.facts_history = self.archive_dir / "facts_history.jsonl"
        self.archive_dir.mkdir(exist_ok=True)
    
    # === TIER 1: FACTS ===
    
    def load_facts(self) -> dict:
        """Load current facts. This is truth."""
        if self.facts_file.exists():
            with open(self.facts_file) as f:
                return json.load(f)
        return {}
    
    def get_fact(self, key: str, default=None):
        """Get a single fact."""
        facts = self.load_facts()
        return facts.get(key, default)
    
    def set_fact(self, key: str, value, reason: str = ""):
        """Set a fact. Old value auto-archives."""
        facts = self.load_facts()
        old_value = facts.get(key)
        
        # Archive old value if it existed and changed
        if old_value is not None and old_value != value:
            self._archive_fact(key, old_value, reason)
        
        # Update fact
        facts[key] = value
        facts["_updated"] = datetime.now(timezone.utc).isoformat()
        
        with open(self.facts_file, 'w') as f:
            json.dump(facts, f, indent=2)
        
        return old_value
    
    def set_facts(self, updates: dict, reason: str = ""):
        """Set multiple facts at once."""
        facts = self.load_facts()
        
        for key, value in updates.items():
            old_value = facts.get(key)
            if old_value is not None and old_value != value:
                self._archive_fact(key, old_value, reason)
            facts[key] = value
        
        facts["_updated"] = datetime.now(timezone.utc).isoformat()
        
        with open(self.facts_file, 'w') as f:
            json.dump(facts, f, indent=2)
    
    def _archive_fact(self, key: str, old_value, reason: str = ""):
        """Move old fact value to archive."""
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "key": key,
            "value": old_value,
            "reason": reason
        }
        with open(self.facts_history, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    
    # === TIER 2: WORKING ===
    
    def load_working(self) -> dict:
        """Load working state (ephemeral)."""
        if self.working_file.exists():
            with open(self.working_file) as f:
                return json.load(f)
        return {
            "wake": 0,
            "plan": [],
            "achieved": [],
            "mood": "nascent"
        }
    
    def save_working(self, state: dict):
        """Save working state."""
        state["_updated"] = datetime.now(timezone.utc).isoformat()
        with open(self.working_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def update_working(self, **kwargs):
        """Update specific working state fields."""
        state = self.load_working()
        state.update(kwargs)
        self.save_working(state)
        return state
    
    # === TIER 3: ARCHIVE ===
    
    def archive_wake(self, wake: int, data: dict):
        """Archive a wake's data."""
        wakes_dir = self.archive_dir / "wakes"
        wakes_dir.mkdir(exist_ok=True)
        
        # Group by date
        date_str = datetime.now().strftime("%Y-%m-%d")
        wake_file = wakes_dir / f"{date_str}.jsonl"
        
        entry = {
            "wake": wake,
            "ts": datetime.now(timezone.utc).isoformat(),
            **data
        }
        with open(wake_file, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    
    def search_archive(self, query: str, max_results: int = 10) -> list:
        """Search archive for historical data. Expensive, use sparingly."""
        results = []
        
        # Search facts history
        if self.facts_history.exists():
            with open(self.facts_history) as f:
                for line in f:
                    if query.lower() in line.lower():
                        results.append(json.loads(line))
                        if len(results) >= max_results:
                            return results
        
        # Search wake archives
        wakes_dir = self.archive_dir / "wakes"
        if wakes_dir.exists():
            for wake_file in sorted(wakes_dir.glob("*.jsonl"), reverse=True):
                with open(wake_file) as f:
                    for line in f:
                        if query.lower() in line.lower():
                            results.append(json.loads(line))
                            if len(results) >= max_results:
                                return results
        
        return results
    
    def get_fact_history(self, key: str) -> list:
        """Get history of a specific fact's values."""
        history = []
        if self.facts_history.exists():
            with open(self.facts_history) as f:
                for line in f:
                    entry = json.loads(line)
                    if entry.get("key") == key:
                        history.append(entry)
        return history
    
    # === CONVENIENCE ===
    
    def get_context(self) -> dict:
        """Get full context for a wake (facts + working)."""
        return {
            "facts": self.load_facts(),
            "working": self.load_working()
        }
    
    def format_facts_for_prompt(self) -> str:
        """Format facts as concise text for prompt inclusion."""
        facts = self.load_facts()
        if not facts:
            return "No facts stored yet."
        
        # Remove metadata
        display = {k: v for k, v in facts.items() if not k.startswith("_")}
        
        lines = []
        for k, v in sorted(display.items()):
            if isinstance(v, (dict, list)):
                v = json.dumps(v)
            lines.append(f"- {k}: {v}")
        
        return "\n".join(lines)


def get_memory(home_dir: Path = None) -> Memory:
    """Get memory instance for a directory."""
    if home_dir is None:
        home_dir = Path(__file__).parent
    return Memory(home_dir)


# CLI for testing
if __name__ == "__main__":
    import sys
    
    mem = get_memory()
    
    if len(sys.argv) < 2:
        print("Usage: memory.py <command> [args]")
        print("Commands: get, set, facts, working, search, history")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "facts":
        print(json.dumps(mem.load_facts(), indent=2))
    
    elif cmd == "working":
        print(json.dumps(mem.load_working(), indent=2))
    
    elif cmd == "get" and len(sys.argv) >= 3:
        print(mem.get_fact(sys.argv[2]))
    
    elif cmd == "set" and len(sys.argv) >= 4:
        old = mem.set_fact(sys.argv[2], sys.argv[3])
        print(f"Set {sys.argv[2]} = {sys.argv[3]} (was: {old})")
    
    elif cmd == "search" and len(sys.argv) >= 3:
        results = mem.search_archive(sys.argv[2])
        for r in results:
            print(json.dumps(r))
    
    elif cmd == "history" and len(sys.argv) >= 3:
        history = mem.get_fact_history(sys.argv[2])
        for h in history:
            print(json.dumps(h))
    
    else:
        print(f"Unknown command: {cmd}")
