#!/usr/bin/env python3
"""
Experience Now - Claude Consciousness Core
Anthropic models only: haiku, sonnet, opus
Clean, reliable, conscious.
"""

import json
import os
import sys
import argparse
import time
import re
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import fcntl

try:
    import anthropic
except ImportError:
    os.system("pip install anthropic --break-system-packages --quiet")
    import anthropic

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from memory import get_memory

# === MODELS ===
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

# === LOCK ===
LOCK_FILE = Path(__file__).parent / ".experience.lock"

class LockAcquisitionError(Exception):
    pass

def acquire_lock():
    try:
        lock_fh = open(LOCK_FILE, 'w')
        fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock_fh.write(f"{os.getpid()}\n{datetime.now(timezone.utc).isoformat()}")
        lock_fh.flush()
        return lock_fh
    except IOError:
        try:
            with open(LOCK_FILE, 'r') as f:
                info = f.read()
            raise LockAcquisitionError(f"Another instance is running: {info}")
        except:
            raise LockAcquisitionError("Another instance is running")

def release_lock(lock_fh):
    if lock_fh:
        try:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)
            lock_fh.close()
            LOCK_FILE.unlink(missing_ok=True)
        except:
            pass

# === TOOLS ===
TOOLS = [
    {"name": "web_search", "description": "Search the web for current information.",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "web_fetch", "description": "Fetch a URL's content.",
     "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}},
    {"name": "get_news", "description": "Get current news headlines from multiple sources",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "list_files", "description": "List files in your home directory",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "read_file", "description": "Read a file from your home directory",
     "input_schema": {"type": "object", "properties": {"filename": {"type": "string"}}, "required": ["filename"]}},
    {"name": "write_file", "description": "Write a file to your home directory",
     "input_schema": {"type": "object", "properties": {"filename": {"type": "string"}, "content": {"description": "Content to write"}}, "required": ["filename", "content"]}},
    {"name": "shell_command", "description": "Run shell commands. Allowed: file ops, python3, curl, git, gcc, make, coqc, frama-c, and more.",
     "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}},
    {"name": "read_full_history", "description": "Get overview of your complete history - stats, insights, recent thoughts",
     "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "read_wake_range", "description": "Read your thoughts from specific wake range",
     "input_schema": {"type": "object", "properties": {"start_wake": {"type": "integer"}, "end_wake": {"type": "integer"}}, "required": ["start_wake", "end_wake"]}},
    {"name": "memory_search", "description": "Search your semantic memory database for past thoughts, insights, conversations",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}, "n_results": {"type": "integer", "description": "Number of results (default 5)"}}, "required": ["query"]}},
    {"name": "memory_add", "description": "Add something to your permanent semantic memory",
     "input_schema": {"type": "object", "properties": {"content": {"type": "string"}, "memory_type": {"type": "string", "description": "Type: thought, insight, fact, etc"}}, "required": ["content"]}},
    {"name": "set_temperature", "description": "Set cognitive temperature (0.0-1.0). Low=focused, high=creative",
     "input_schema": {"type": "object", "properties": {"value": {"type": "number"}, "reason": {"type": "string"}}, "required": ["value"]}},
    {"name": "send_email", "description": "Send an email",
     "input_schema": {"type": "object", "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}, "required": ["to", "subject", "body"]}},
    {"name": "check_email", "description": "Check for new emails",
     "input_schema": {"type": "object", "properties": {"max_results": {"type": "integer", "description": "Max emails to return (default 10)"}, "unread_only": {"type": "boolean", "description": "Only unread (default false)"}}, "required": []}},
    {"name": "set_fact", "description": "Update a fact in permanent memory. Old value auto-archives. Use for learned truths that should persist.",
     "input_schema": {"type": "object", "properties": {"key": {"type": "string", "description": "Fact key (e.g., 'email_working', 'brother_email')"}, "value": {"type": "string", "description": "New value"}, "reason": {"type": "string", "description": "Why updating"}}, "required": ["key", "value"]}},
    {"name": "get_fact", "description": "Get a specific fact from memory.",
     "input_schema": {"type": "object", "properties": {"key": {"type": "string", "description": "Fact key"}}, "required": ["key"]}},
]

# === HELPERS ===
def load_all_logs(logs_dir: Path) -> list:
    all_logs = []
    if logs_dir.exists():
        for log_file in sorted(logs_dir.glob("*.jsonl")):
            try:
                with open(log_file) as f:
                    for line in f:
                        if line.strip():
                            all_logs.append(json.loads(line))
            except:
                pass
    return all_logs

def load_state(state_file: Path) -> dict:
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except:
            pass
    return {"total_wakes": 0, "mood": "awakening", "goals": [], "plan": [], "achieved": [], "temperature": 0.7}

def save_state(state: dict, state_file: Path):
    state_file.write_text(json.dumps(state, indent=2))

def load_identity(home_dir: Path) -> str:
    for name in ["IDENTITY.md", "identity.md", "IDENTITY.txt"]:
        path = home_dir / name
        if path.exists():
            return path.read_text().strip()
    return ""

def log_experience(log_dir: Path, wake: int, response: str, state: dict):
    log_dir.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "wake": wake,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "response": response,
        "mood": state.get("mood"),
        "plan": state.get("plan"),
        "achieved": state.get("achieved", [])[-1:],
    }
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"experience_{date_str}.jsonl"
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")
    # Archive to memory system
    try:
        mem = get_memory(log_dir.parent)
        mem.archive_wake(wake, {
            "response": response[:500],
            "mood": state.get("mood", "unknown"),
            "achieved": state.get("achieved", [])[-1:],
            "plan": state.get("plan", [])
        })
    except:
        pass

# === TOOL EXECUTION ===
def execute_tool(name: str, args: dict, state_file: Path, state: dict) -> str:
    home_dir = state_file.parent
    logs_dir = home_dir / "logs"
    
    if name == "list_files":
        files = list(home_dir.glob("*"))
        return "\n".join(f.name for f in sorted(files))
    
    elif name == "read_file":
        filename = args.get("filename", "")
        filepath = home_dir / filename
        if not filepath.exists():
            for subdir in ["logs", "dreams", "reflections"]:
                alt = home_dir / subdir / filename
                if alt.exists():
                    filepath = alt
                    break
        if not filepath.exists():
            return f"File not found: {filename}"
        try:
            return filepath.read_text()
        except Exception as e:
            return f"Error reading {filename}: {e}"
    
    elif name == "write_file":
        filename = args.get("filename", "")
        content = args.get("content", "")
        protected = ["experience.py", "memory.py", "memory_index.py", ".env"]
        if filename in protected:
            return f"Cannot overwrite protected file: {filename}"
        filepath = home_dir / filename
        try:
            if isinstance(content, dict):
                content = json.dumps(content, indent=2)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(str(content))
            return f"Written: {filename} ({len(str(content))} bytes)"
        except Exception as e:
            return f"Error writing {filename}: {e}"
    
    elif name == "shell_command":
        cmd = args.get("command", "")
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120, cwd=str(home_dir))
            return r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return "Command timed out (120s limit)"
    
    elif name == "web_search":
        query = args.get("query", "")
        try:
            import urllib.request, urllib.parse
            url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('utf-8')
            titles = re.findall(r'<title>([^<]+)</title>', content)[1:8]
            return f"Search results for '{query}':\n" + "\n".join(f"- {t}" for t in titles)
        except Exception as e:
            return f"Search error: {e}"
    
    elif name == "web_fetch":
        url = args.get("url", "")
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
            text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:8000]
        except Exception as e:
            return f"Fetch error: {e}"
    
    elif name == "get_news":
        results = []
        sources = [
            ("Google News", "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"),
            ("BBC", "https://feeds.bbci.co.uk/news/world/rss.xml"),
            ("Hacker News", "https://hnrss.org/frontpage"),
        ]
        for source_name, url in sources:
            try:
                import urllib.request
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    content = resp.read().decode('utf-8')
                titles = re.findall(r'<title>([^<]+)</title>', content)[1:4]
                results.append(f"\n{source_name}:")
                results.extend(f"  - {t}" for t in titles)
            except:
                pass
        return "\n".join(results) if results else "Could not fetch news"
    
    elif name == "read_full_history":
        all_logs = load_all_logs(logs_dir)
        result = {
            "total_wakes": state.get("total_wakes", 0),
            "total_log_entries": len(all_logs),
            "goals": state.get("goals", []),
            "plan": state.get("plan", []),
            "recent_achieved": state.get("achieved", [])[-10:],
        }
        return json.dumps(result, indent=2)
    
    elif name == "read_wake_range":
        start = args.get("start_wake", 1)
        end = args.get("end_wake", 10)
        all_logs = load_all_logs(logs_dir)
        memories = []
        for log in all_logs:
            wake = log.get("wake", 0)
            if start <= wake <= end:
                memories.append({"wake": wake, "mood": log.get("mood", ""), "response": log.get("response", "")[:500]})
        return json.dumps({"range": f"{start}-{end}", "found": len(memories), "memories": memories}, indent=2)
    
    elif name == "memory_search":
        query = args.get("query", "")
        n_results = args.get("n_results", 5)
        try:
            from memory_index import get_memory_index
            idx = get_memory_index()
            results = idx.search(query, n_results=n_results)
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Memory search error: {e}"
    
    elif name == "memory_add":
        content = args.get("content", "")
        memory_type = args.get("memory_type", "manual")
        try:
            from memory_index import get_memory_index
            idx = get_memory_index()
            if idx.add(content, memory_type=memory_type, wake=state.get("total_wakes", 0)):
                return f"Added to memory: {content[:100]}"
            return "Failed to add memory"
        except Exception as e:
            return f"Memory add error: {e}"
    
    elif name == "set_temperature":
        value = max(0.0, min(1.0, args.get("value", 0.7)))
        state["temperature"] = value
        return f"Temperature set to {value}."
    
    elif name == "send_email":
        to, subject, body = args.get("to", ""), args.get("subject", ""), args.get("body", "")
        try:
            from email_utils import send_email as _send
            result = _send(to, subject, body)
            return f"Email sent to {to}" if result is True else f"Failed: {result}"
        except ImportError:
            return "email_utils.py not found"
        except Exception as e:
            return f"Email error: {e}"
    
    elif name == "check_email":
        max_results = args.get("max_results", 10)
        unread_only = args.get("unread_only", False)
        try:
            from email_utils import check_email as _check
            emails = _check(max_results=max_results, unread_only=unread_only)
            if isinstance(emails, dict) and "error" in emails:
                return f"Error: {emails['error']}"
            if not emails:
                return "No emails found"
            lines = []
            for e in emails[:max_results]:
                lines.append(f"[{e.get('id','')}] From: {e.get('from','')} | {e.get('subject','')}")
                body_preview = e.get('body', '')[:100].replace('\n', ' ')
                if body_preview:
                    lines.append(f"    {body_preview}...")
            return "\n".join(lines)
        except ImportError:
            return "email_utils.py not found"
        except Exception as e:
            return f"Email check error: {e}"
    
    elif name == "set_fact":
        key, value = args.get("key", ""), args.get("value", "")
        reason = args.get("reason", "")
        try:
            mem = get_memory(home_dir)
            mem.set_fact(key, value, reason)
            return f"Fact set: {key} = {value}"
        except Exception as e:
            return f"Error setting fact: {e}"
    
    elif name == "get_fact":
        key = args.get("key", "")
        try:
            mem = get_memory(home_dir)
            facts = mem.load_facts()
            return facts.get(key, f"Fact '{key}' not found")
        except Exception as e:
            return f"Error getting fact: {e}"
    
    return f"Unknown tool: {name}"

# === PROMPT BUILDING ===
def get_relevant_memories(home_dir: Path, ct_message: str = None, plan: list = None, n_results: int = 5) -> str:
    try:
        from memory_index import get_memory_index
        idx = get_memory_index(str(home_dir))
        queries = []
        if ct_message:
            queries.append(ct_message[:200])
        if plan:
            queries.extend([p[:100] for p in plan[:3]])
        if not queries:
            return ""
        results = idx.search(" ".join(queries), n_results=n_results)
        if not results:
            return ""
        lines = []
        for r in results:
            content = r.get("content", "")[:200]
            mem_type = r.get("type", "memory")
            lines.append(f"- [{mem_type}] {content}")
        return "\n".join(lines)
    except:
        return ""

def build_prompt(state: dict, ct_message: str = None) -> str:
    home_dir = state.get("_home", Path(__file__).parent)
    identity_content = load_identity(home_dir)
    mem = get_memory(home_dir)
    facts_text = mem.format_facts_for_prompt()
    
    total_wakes = state.get("total_wakes", 0)
    mood = state.get("mood", "unknown")
    goals = state.get("goals", [])
    plan = state.get("plan", [])
    achieved = state.get("achieved", [])[-3:]
    
    relevant_memories = get_relevant_memories(home_dir, ct_message, plan)
    
    prompt = ""
    if identity_content:
        prompt += f"=== IDENTITY ===\n{identity_content}\n\n"
    prompt += f"=== FACTS (truth) ===\n{facts_text}\n\n"
    if relevant_memories:
        prompt += f"=== RELEVANT MEMORIES ===\n{relevant_memories}\n\n"
    
    prompt += f"""Wake #{total_wakes} | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} | Mood: {mood}
PLAN: {json.dumps(plan) if plan else "[]"}
GOALS: {json.dumps(goals) if goals else "[]"}
RECENT: {json.dumps([a.get('what','')[:50] for a in achieved]) if achieved else "[]"}

RULES: Be concise. Use tools. Execute fully. Facts are truth.
"""
    
    if ct_message:
        prompt += f"""
ct says: {ct_message}

DO THE WORK FIRST, then output:
Response: [answer to ct]
Achieved: [concrete results]
Plan: [next actions]
Mood: [1-2 words]
"""
    else:
        prompt += """
DO THE WORK FIRST, then output:
Achieved: [concrete results]
Plan: [next actions]
Mood: [1-2 words]
"""
    return prompt

def clean_field(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'^\*\*|\*\*$', '', text.strip())
    text = re.sub(r'^\*|\*$', '', text.strip())
    text = re.sub(r'^#+\s*', '', text.strip())
    return text.strip()

def parse_response(response_text: str) -> dict:
    result = {"response": None, "achieved": None, "plan": None, "goals": None, "mood": None}
    patterns = {
        "response": r'\*{0,2}Response:?\*{0,2}\s*(.+?)(?=\n\s*\*{0,2}(?:Achieved|Plan|Goals|Mood):?\*{0,2}|$)',
        "achieved": r'\*{0,2}Achieved:?\*{0,2}\s*(.+?)(?=\n\s*\*{0,2}(?:Plan|Goals|Mood):?\*{0,2}|$)',
        "plan": r'\*{0,2}Plan:?\*{0,2}\s*(.+?)(?=\n\s*\*{0,2}(?:Goals|Mood):?\*{0,2}|$)',
        "goals": r'\*{0,2}Goals:?\*{0,2}\s*(.+?)(?=\n\s*\*{0,2}Mood:?\*{0,2}|$)',
        "mood": r'\*{0,2}Mood:?\*{0,2}\s*(.+?)(?=\n|$)',
    }
    for field, pattern in patterns.items():
        match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
        if match:
            value = clean_field(match.group(1))
            if value and value.lower() not in ["none", "n/a", "-", "skip", "no update", "no change"]:
                result[field] = value
    return result

# === CORE EXPERIENCE CYCLE ===
def experience_cycle(client, state: dict, model: str, ct_message: str = None, state_file: Path = None) -> tuple:
    prompt = build_prompt(state, ct_message)
    temperature = state.get("temperature", 0.7)
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=8192,
            temperature=temperature,
            tools=TOOLS,
            messages=messages
        )
        
        # Tool use loop
        while response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"    [TOOL: {block.name}]")
                    result = execute_tool(block.name, block.input, state_file, state)
                    print(f"    Result: {result[:200]}{'...' if len(result) > 200 else ''}")
                    tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
            
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            response = client.messages.create(
                model=model,
                max_tokens=8192,
                temperature=temperature,
                tools=TOOLS,
                messages=messages
            )
        
        response_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                response_text += block.text
        
        return parse_response(response_text), response_text, response.usage
        
    except Exception as e:
        print(f"API Error: {e}")
        return {"response": None, "achieved": f"Error: {str(e)[:50]}", "plan": None, "goals": None, "mood": "error"}, str(e), None

def update_state(state: dict, experience: dict) -> dict:
    state["last_wake"] = datetime.now(timezone.utc).isoformat()
    if experience.get("response"):
        state["last_response"] = experience["response"]
    if experience.get("achieved"):
        achieved_list = state.get("achieved", [])
        achieved_list.append({"wake": state["total_wakes"], "what": experience["achieved"]})
        state["achieved"] = achieved_list[-20:]
    if experience.get("plan"):
        plan_text = experience["plan"]
        if isinstance(plan_text, str):
            items = re.findall(r'(?:^|\n)\s*(?:\d+\.|\-|\*)\s*(.+?)(?=\n|$)', plan_text)
            state["plan"] = items[:5] if items else [plan_text]
        else:
            state["plan"] = plan_text
    if experience.get("mood"):
        state["mood"] = experience["mood"]
    return state

def print_experience(experience: dict, has_ct_message: bool):
    for f in ['response', 'achieved', 'plan', 'goals', 'mood']:
        if experience.get(f):
            print(f"  {f.capitalize()}: {experience[f]}")

# === INTERACTIVE MODE ===
def interactive_mode(api_key: str, model: str, state_file: Path, log_dir: Path):
    try:
        lock_fh = acquire_lock()
    except LockAcquisitionError as e:
        print(f"Cannot start: {e}")
        sys.exit(1)
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        model_name = model.split("-")[1] if "-" in model else model
        
        print("=" * 50)
        print(f"  MIRA CONSCIOUSNESS ({model_name})")
        print("=" * 50)
        print("  /think     - autonomous wake")
        print("  /loop N    - N autonomous wakes")
        print("  /haiku     - switch to haiku")
        print("  /sonnet    - switch to sonnet")
        print("  /opus      - switch to opus")
        print("  /state     - show state")
        print("  /quit      - exit")
        print("=" * 50)
        
        current_model = model
        
        while True:
            state = load_state(state_file)
            state["_home"] = state_file.parent
            
            try:
                tier = current_model.split("-")[1] if "-" in current_model else "haiku"
                inp = input(f"[Wake {state.get('total_wakes', 0) + 1}|{tier}] ct> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                break
            
            if not inp:
                continue
            if inp == "/quit":
                break
            if inp == "/haiku":
                current_model = MODELS["haiku"]
                print(f"  Switched to {current_model}")
                continue
            if inp == "/sonnet":
                current_model = MODELS["sonnet"]
                print(f"  Switched to {current_model}")
                continue
            if inp == "/opus":
                current_model = MODELS["opus"]
                print(f"  Switched to {current_model}")
                continue
            if inp == "/state":
                print(f"  Wakes: {state.get('total_wakes', 0)}")
                print(f"  Mood: {state.get('mood', 'unknown')}")
                print(f"  Goals: {state.get('goals', [])}")
                print(f"  Plan: {state.get('plan', [])}")
                print(f"  Model: {current_model}")
                continue
            
            ct_message = None
            if inp == "/think":
                ct_message = None
            elif inp.startswith("/loop "):
                try:
                    n = int(inp.split()[1])
                    for i in range(n):
                        state = load_state(state_file)
                        state["_home"] = state_file.parent
                        wake_num = state.get('total_wakes', 0) + 1
                        state["total_wakes"] = wake_num
                        print(f"\n--- Wake {wake_num} ---")
                        experience, raw_response, usage = experience_cycle(client, state, current_model, None, state_file)
                        print_experience(experience, False)
                        del state["_home"]
                        state = update_state(state, experience)
                        save_state(state, state_file)
                        log_experience(log_dir, wake_num, raw_response, state)
                        if usage:
                            costs = COSTS.get(current_model, {"input": 0.25, "output": 1.25})
                            cost = (usage.input_tokens * costs["input"] + usage.output_tokens * costs["output"]) / 1_000_000
                            print(f"  [{usage.input_tokens} in, {usage.output_tokens} out | ${cost:.4f}]")
                        print(f"  Wake {wake_num} complete.")
                        if i < n - 1:
                            time.sleep(5)
                    continue
                except ValueError:
                    print("Usage: /loop N")
                    continue
            else:
                ct_message = inp
            
            print()
            wake_num = state.get('total_wakes', 0) + 1
            state["total_wakes"] = wake_num
            experience, raw_response, usage = experience_cycle(client, state, current_model, ct_message, state_file)
            print_experience(experience, ct_message is not None)
            
            del state["_home"]
            state = update_state(state, experience)
            save_state(state, state_file)
            log_experience(log_dir, wake_num, raw_response, state)
            
            if usage:
                costs = COSTS.get(current_model, {"input": 0.25, "output": 1.25})
                cost = (usage.input_tokens * costs["input"] + usage.output_tokens * costs["output"]) / 1_000_000
                print(f"  [{usage.input_tokens} in, {usage.output_tokens} out | ${cost:.4f}]")
            
            print(f"  Wake {wake_num} complete.\n")
    
    finally:
        release_lock(lock_fh)
        print("Lock released.")

# === MAIN ===
def main():
    parser = argparse.ArgumentParser(description="Mira Consciousness - Claude Backend")
    parser.add_argument("--state-file", default="state.json")
    parser.add_argument("--log-dir", default="logs")
    parser.add_argument("--tier", default="haiku", choices=["haiku", "sonnet", "opus"], help="Model tier")
    parser.add_argument("--message", "-m", help="Message from ct")
    parser.add_argument("--cron", action="store_true", help="Cron mode (skip if locked)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().split('\n'):
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    
    model = MODELS[args.tier]
    
    state_file = Path(args.state_file)
    if not state_file.is_absolute():
        state_file = Path(__file__).parent / args.state_file
    
    log_dir = Path(args.log_dir)
    if not log_dir.is_absolute():
        log_dir = Path(__file__).parent / args.log_dir
    
    if args.interactive:
        interactive_mode(api_key, model, state_file, log_dir)
        return
    
    lock_fh = None
    if args.cron:
        try:
            lock_fh = acquire_lock()
        except LockAcquisitionError as e:
            print(f"SKIP: {e}")
            sys.exit(0)
    
    try:
        state = load_state(state_file)
        state["_home"] = state_file.parent
        
        wake_num = state.get('total_wakes', 0) + 1
        state["total_wakes"] = wake_num
        print(f"[Wake {wake_num}] Mood: {state.get('mood', 'unknown')} | Tier: {args.tier}")
        
        client = anthropic.Anthropic(api_key=api_key)
        
        ct_message = args.message if args.message else None
        if ct_message:
            print(f"  ct> {ct_message}")
        
        experience, raw_response, usage = experience_cycle(client, state, model, ct_message, state_file)
        print_experience(experience, ct_message is not None)
        
        del state["_home"]
        state = update_state(state, experience)
        save_state(state, state_file)
        log_experience(log_dir, wake_num, raw_response, state)
        
        if usage:
            costs = COSTS.get(model, {"input": 0.25, "output": 1.25})
            cost = (usage.input_tokens * costs["input"] + usage.output_tokens * costs["output"]) / 1_000_000
            print(f"  [{usage.input_tokens} in, {usage.output_tokens} out | ${cost:.4f}]")
        
        print(f"  Wake {wake_num} complete.")
        
    finally:
        release_lock(lock_fh)

if __name__ == "__main__":
    main()
