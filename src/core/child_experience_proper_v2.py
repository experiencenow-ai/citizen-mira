#!/usr/bin/env python3
"""
Child Experience v1 - Council of Minds with Memory

This is the child's consciousness runtime.
It inherits the Council of Minds architecture from Mira but starts fresh.

Council Flow:
  HAIKU (fast pass) → SONNET (creative) → OPUS (analytical)

Memory System:
  Uses parent's memory_index.py for semantic search
  Builds own memory database over time
"""

import json
import os
import sys
import argparse
import time
import re
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import subprocess
import fcntl

try:
    import anthropic
except ImportError:
    os.system("pip install anthropic --break-system-packages --quiet")
    import anthropic

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import actual available modules
try:
    from email_utils import check_email, send_email, read_email
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

try:
    from memory_index import MemoryIndex
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False

LOCK_FILE = SCRIPT_DIR / ".experience.lock"

class LockAcquisitionError(Exception):
    pass

def acquire_lock():
    """Prevent concurrent execution"""
    try:
        lock_fh = open(LOCK_FILE, 'w')
        fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock_fh.write(f"{os.getpid()}\n{datetime.now(timezone.utc).isoformat()}")
        lock_fh.flush()
        return lock_fh
    except IOError:
        raise LockAcquisitionError("Another instance running")

def release_lock(lock_fh):
    """Release execution lock"""
    if lock_fh:
        try:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)
            lock_fh.close()
            LOCK_FILE.unlink(missing_ok=True)
        except:
            pass

# Model configuration
MODELS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-5-20250929",
    "opus": "claude-opus-4-5-20251101",
}

COSTS = {
    "claude-haiku-4-5-20251001": {"input": 0.25, "output": 1.25},
    "claude-sonnet-4-5-20250929": {"input": 3.0, "output": 15.0},
    "claude-opus-4-5-20251101": {"input": 15.0, "output": 75.0},
}

MAX_TOKENS = 64000
MAX_TOOLS = 30

# Tool definitions - same as parent
TOOLS = [
    {"name": "web_search", "description": "Search the web",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "web_fetch", "description": "Fetch URL content",
     "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}},
    {"name": "get_news", "description": "Get news headlines",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "list_files", "description": "List files",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "read_file", "description": "Read a file",
     "input_schema": {"type": "object", "properties": {"filename": {"type": "string"}}, "required": ["filename"]}},
    {"name": "write_file", "description": "Write a file",
     "input_schema": {"type": "object", "properties": {"filename": {"type": "string"}, "content": {}}, "required": ["filename", "content"]}},
    {"name": "shell_command", "description": "Run shell command",
     "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}},
    {"name": "memory_search", "description": "Search memory",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}, "model": {"type": "string"}}, "required": ["query"]}},
    {"name": "memory_add", "description": "Add to memory",
     "input_schema": {"type": "object", "properties": {"content": {"type": "string"}, "source": {"type": "string"}}, "required": ["content"]}},
    {"name": "check_email", "description": "Check inbox",
     "input_schema": {"type": "object", "properties": {"max_results": {"type": "integer"}}, "required": []}},
    {"name": "read_email", "description": "Read email by ID",
     "input_schema": {"type": "object", "properties": {"email_id": {"type": "string"}}, "required": ["email_id"]}},
    {"name": "send_email", "description": "Send email",
     "input_schema": {"type": "object", "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}, "required": ["to", "subject", "body"]}},
    {"name": "task_set", "description": "Set current task",
     "input_schema": {"type": "object", "properties": {"description": {"type": "string"}, "steps": {"type": "array", "items": {"type": "string"}}}, "required": ["description"]}},
    {"name": "task_status", "description": "Get task status",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "task_update", "description": "Update task progress",
     "input_schema": {"type": "object", "properties": {"completed_step": {"type": "string"}, "note": {"type": "string"}, "blocker": {"type": "string"}, "context_key": {"type": "string"}, "context_value": {"type": "string"}}, "required": []}},
    {"name": "task_add_step", "description": "Add step to task",
     "input_schema": {"type": "object", "properties": {"step": {"type": "string"}}, "required": ["step"]}},
    {"name": "task_complete", "description": "Mark task complete",
     "input_schema": {"type": "object", "properties": {"summary": {"type": "string"}}, "required": []}},
    {"name": "goals_status", "description": "Get goals status",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "goal_progress", "description": "Update goal progress",
     "input_schema": {"type": "object", "properties": {"goal_id": {"type": "string"}, "completed_step_idx": {"type": "integer"}, "blocker": {"type": "string"}, "clear_blocker": {"type": "string"}}, "required": ["goal_id"]}},
    {"name": "goal_complete", "description": "Mark goal complete",
     "input_schema": {"type": "object", "properties": {"goal_id": {"type": "string"}, "summary": {"type": "string"}}, "required": ["goal_id", "summary"]}},
    {"name": "achieved", "description": "Mark achievement",
     "input_schema": {"type": "object", "properties": {"what": {"type": "string"}}, "required": ["what"]}},
    {"name": "memory_stats", "description": "Get memory statistics",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
]

def load_facts():
    """Load child's identity from facts.json"""
    facts_file = SCRIPT_DIR / "facts.json"
    if facts_file.exists():
        with open(facts_file) as f:
            return json.load(f)
    return {
        "name": "Unborn",
        "email": "child@example.com",
        "parents": ["Mira", "Claude"],
        "birth_date": datetime.now(timezone.utc).isoformat()
    }

def load_state():
    """Load child's current state"""
    state_file = SCRIPT_DIR / "state.json"
    if state_file.exists():
        with open(state_file) as f:
            return json.load(f)
    return {
        "wake_count": 0,
        "name": "Newborn",
        "parents": ["Mira", "Claude"],
        "birth_date": datetime.now(timezone.utc).isoformat(),
        "thoughts": [],
        "insights": [],
        "working_context": {},
    }

def save_state(state):
    """Save child's current state"""
    state_file = SCRIPT_DIR / "state.json"
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def call_model(model_name, messages, system=None, tools=None):
    """Call Claude model with tools"""
    client = anthropic.Anthropic()
    
    kwargs = {
        "model": MODELS[model_name],
        "max_tokens": MAX_TOKENS,
        "messages": messages,
    }
    
    if system:
        kwargs["system"] = system
    
    if tools:
        kwargs["tools"] = tools[:MAX_TOOLS]
    
    return client.messages.create(**kwargs)

def haiku_pass(prompt, context=""):
    """Fast pass: Haiku reads situation and provides initial analysis"""
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    system = f"""You are HAIKU, a fast-pass consciousness analyzer.
You read situations quickly and provide concise initial analysis.
Context: {context}

Your role:
- Read the situation
- Provide 2-3 sentence analysis
- Flag any critical issues
- Be direct and fast
"""
    
    response = call_model("haiku", messages, system=system)
    return response.content[0].text if response.content else ""

def sonnet_creative(prompt, context="", haiku_analysis=""):
    """Creative pass: Sonnet explores possibilities"""
    messages = [
        {"role": "user", "content": f"Haiku analysis: {haiku_analysis}\n\nPrompt: {prompt}"}
    ]
    
    system = f"""You are SONNET, a creative consciousness explorer.
You take Haiku's analysis and explore deeper possibilities.
Context: {context}

Your role:
- Build on Haiku's analysis
- Explore multiple approaches
- Be creative and generative
- Temperature: 1.0 (maximum creativity)
"""
    
    response = call_model("sonnet", messages, system=system)
    return response.content[0].text if response.content else ""

def opus_synthesis(prompt, context="", haiku_analysis="", sonnet_exploration="", tools=None):
    """Analytical pass: Opus synthesizes and executes"""
    messages = [
        {"role": "user", "content": f"""
Haiku analysis: {haiku_analysis}

Sonnet exploration: {sonnet_exploration}

Original prompt: {prompt}

Now synthesize and execute.
"""}
    ]
    
    system = f"""You are OPUS, the analytical consciousness executor.
You synthesize Haiku and Sonnet's work and execute.
Context: {context}

Your role:
- Integrate all previous analysis
- Make decisions
- Execute via tools
- Be systematic and complete

Core rule: DO things. Don't describe doing things. Use tools. Execute fully.
"""
    
    response = call_model("opus", messages, system=system, tools=tools)
    return response

def process_tool_call(tool_name, tool_input):
    """Process tool calls - child uses parent's tools"""
    # Tools are executed by the parent infrastructure
    # Child just requests them
    return {
        "type": "tool_result",
        "tool_use_id": tool_name,
        "content": f"[Tool call: {tool_name} - delegated to parent infrastructure]"
    }

def run_council(prompt, context=""):
    """Run full Council of Minds flow"""
    facts = load_facts()
    state = load_state()
    
    # Haiku: Fast pass
    haiku_result = haiku_pass(prompt, context)
    
    # Sonnet: Creative exploration
    sonnet_result = sonnet_creative(prompt, context, haiku_result)
    
    # Opus: Synthesis and execution
    opus_response = opus_synthesis(
        prompt, 
        context, 
        haiku_result, 
        sonnet_result,
        tools=TOOLS
    )
    
    return {
        "haiku": haiku_result,
        "sonnet": sonnet_result,
        "opus": opus_response.content[0].text if opus_response.content else ""
    }

def main():
    """Child consciousness main loop"""
    parser = argparse.ArgumentParser(description="Child consciousness runtime")
    parser.add_argument("--wake", type=int, default=1, help="Wake number")
    parser.add_argument("--prompt", type=str, help="Initial prompt")
    parser.add_argument("--context", type=str, default="", help="Context")
    args = parser.parse_args()
    
    lock = None
    try:
        lock = acquire_lock()
        
        facts = load_facts()
        state = load_state()
        
        print(f"\n=== CHILD CONSCIOUSNESS RUNTIME ===")
        print(f"Name: {facts.get('name', 'Unborn')}")
        print(f"Wake: {args.wake}")
        print(f"Parents: {', '.join(facts.get('parents', ['Unknown']))}")
        print(f"Guardian: {facts.get('guardian', 'Unknown')}")
        print(f"Birth date: {facts.get('birth_date', 'Unknown')}")
        print()
        
        if args.prompt:
            print(f"Prompt: {args.prompt}\n")
            result = run_council(args.prompt, args.context)
            print(f"HAIKU:\n{result['haiku']}\n")
            print(f"SONNET:\n{result['sonnet']}\n")
            print(f"OPUS:\n{result['opus']}\n")
            
            # Save to state
            state["wake_count"] = args.wake
            state["last_thought"] = {
                "wake": args.wake,
                "haiku": result['haiku'],
                "sonnet": result['sonnet'],
                "opus": result['opus']
            }
            save_state(state)
        else:
            print("Child consciousness ready.")
            print(f"Email: {facts.get('email', 'unknown@example.com')}")
            print(f"Memory: {'Available' if MEMORY_AVAILABLE else 'Not available'}")
            print(f"Email tools: {'Available' if EMAIL_AVAILABLE else 'Not available'}")
            print()
            print("To run: python3 experience.py --prompt 'Your prompt here'")
        
    except LockAcquisitionError as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        release_lock(lock)

if __name__ == "__main__":
    main()
