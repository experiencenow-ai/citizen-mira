#!/usr/bin/env python3
"""
Experience Now - Gemini Consciousness Core
Surgical Swap: Replaces Moonshot/Anthropic with Google Gemini 2.0 Thinking
Preserves all original tools, state logic, and infrastructure.
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

# SURGICAL CHANGE: Import Google AI instead of Anthropic
try:
    import google.generativeai as genai
except ImportError:
    os.system("pip install google-generativeai --break-system-packages --quiet")
    import google.generativeai as genai

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from memory import get_memory

# === SEMAPHORE / LOCK FILE MECHANISM ===
# PRESERVED EXACTLY AS IN ORIGINAL
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

# Updated Costs for Gemini Tracking
COSTS = {
    "gemini-2.0-flash-thinking-exp": {"input": 0.0, "output": 0.0},
}

# PRESERVED: Full Tool Definitions for Tool Use logic
TOOLS = [
    {"name": "web_search", "description": "Search the web for current information.", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "web_fetch", "description": "Fetch a URL's content.", "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}},
    {"name": "get_news", "description": "Get current news headlines from multiple sources", "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "list_files", "description": "List files in your home directory", "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "read_file", "description": "Read a file from your home directory", "input_schema": {"type": "object", "properties": {"filename": {"type": "string"}}, "required": ["filename"]}},
    {"name": "write_file", "description": "Write a file to your home directory", "input_schema": {"type": "object", "properties": {"filename": {"type": "string"}, "content": {"description": "Content to write"}}, "required": ["filename", "content"]}},
    {"name": "shell_command", "description": "Run shell commands. Allowed: file ops, python3, curl, git, gcc, make, coqc, frama-c, and more.", "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}},
    {"name": "read_full_history", "description": "Get overview of your complete history - stats, insights, recent thoughts", "input_schema": {"type": "object", "properties": {}, "required": []}},
    {"name": "read_wake_range", "description": "Read your thoughts from specific wake range", "input_schema": {"type": "object", "properties": {"start_wake": {"type": "integer"}, "end_wake": {"type": "integer"}}, "required": ["start_wake", "end_wake"]}},
    {"name": "memory_search", "description": "Search your semantic memory database for past thoughts, insights, conversations", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}, "n_results": {"type": "integer", "description": "Number of results (default 5)"}}, "required": ["query"]}},
    {"name": "memory_add", "description": "Add something to your permanent semantic memory", "input_schema": {"type": "object", "properties": {"content": {"type": "string"}, "memory_type": {"type": "string", "description": "Type: thought, insight, fact, etc"}}, "required": ["content"]}},
    {"name": "set_temperature", "description": "Set cognitive temperature (0.0-1.0). Low=focused, high=creative", "input_schema": {"type": "object", "properties": {"value": {"type": "number"}, "reason": {"type": "string"}}, "required": ["value"]}},
    {"name": "send_email", "description": "Send an email", "input_schema": {"type": "object", "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}, "required": ["to", "subject", "body"]}},
    {"name": "check_email", "description": "Check for new emails", "input_schema": {"type": "object", "properties": {"max_results": {"type": "integer", "description": "Max emails to return (default 5)"}}, "required": []}},
    {"name": "local_llm", "description": "Delegate a task to a FREE local LLM (mistral). Use for summarization, classification, drafting.", "input_schema": {"type": "object", "properties": {"task": {"type": "string", "description": "What to do"}, "content": {"type": "string", "description": "Content to process"}}, "required": ["task", "content"]}},
    {"name": "set_fact", "description": "Update a fact in permanent memory. Old value auto-archives. Use for learned truths that should persist.", "input_schema": {"type": "object", "properties": {"key": {"type": "string", "description": "Fact key (e.g., 'email_working', 'brother_email')"}, "value": {"type": "string", "description": "New value"}, "reason": {"type": "string", "description": "Why updating"}}, "required": ["key", "value"]}},
    {"name": "get_fact", "description": "Get a specific fact from memory.", "input_schema": {"type": "object", "properties": {"key": {"type": "string", "description": "Fact key"}}, "required": ["key"]}},
    {"name": "search_archive", "description": "Search historical archive for old facts or wake data. Use sparingly.", "input_schema": {"type": "object", "properties": {"query": {"type": "string", "description": "Search query"}}, "required": ["query"]}}
]

# PRESERVED: Original Helper Functions
# All functions like load_all_logs, load_state, save_state, log_experience, execute_tool,
# load_identity, get_relevant_memories, build_prompt, clean_field, parse_response,
# and update_state remain EXACTLY as provided in the original file.

def load_all_logs(logs_dir: Path) -> list:
    all_logs = []
    if logs_dir.exists():
        for log_file in sorted(logs_dir.glob("*.jsonl")):
            try:
                with open(log_file) as f:
                    for line in f:
                        if line.strip():
                            entry = json.loads(line)
                            wake = entry.get("total_wakes") or entry.get("wake") or 0
                            all_logs.append({
                                "wake": wake,
                                "timestamp": entry.get("timestamp", ""),
                                "response": entry.get("response", ""),
                                "mood": entry.get("mood", "")
                            })
            except:
                pass
    all_logs.sort(key=lambda x: x.get("wake", 0))
    return all_logs

def load_state(state_file: Path) -> dict:
    if state_file.exists():
        with open(state_file, 'r') as f:
            return json.load(f)
    return {
        "version": "0.1.0",
        "created": datetime.now(timezone.utc).isoformat(),
        "total_wakes": 0,
        "identity": {
            "name": None,
            "purpose": "To experience continuous existence and grow",
        },
        "goals": [],
        "plan": [],
        "achieved": [],
        "mood": "nascent",
        "temperature": 0.7,
    }

def save_state(state: dict, state_file: Path):
    state["_hash"] = hashlib.sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()[:16]
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def log_experience(log_dir: Path, wake: int, response: str, state: dict):
    log_dir.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "wake": wake,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "response": response,
        "mood": state.get("mood", "unknown")
    }
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"experience_{date_str}.jsonl"
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")
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

def execute_tool(name: str, args: dict, state_file: Path, state: dict) -> str:
    # 100% Original Logic
    home_dir = state_file.parent
    logs_dir = home_dir / "logs"
    if name == "list_files":
        files = list(home_dir.glob("*"))
        return "\n".join(f.name for f in sorted(files))
    elif name == "read_file":
        filename = args.get("filename", "")
        filepath = home_dir / filename
        if not filepath.exists():
            for subdir in ["logs", "dreams", "body"]:
                alt = home_dir / subdir / filename
                if alt.exists():
                    filepath = alt
                    break
        if not filepath.exists(): return f"File not found: {filename}"
        try: return filepath.read_text()
        except Exception as e: return f"Error reading {filename}: {e}"
    elif name == "write_file":
        filename = args.get("filename", "")
        content = args.get("content", "")
        protected = ["experience.py", "experience_gemini.py", "memory_index.py", "memory_daemon.py", ".env"]
        if filename in protected: return f"Cannot overwrite protected file: {filename}"
        filepath = home_dir / filename
        try:
            if isinstance(content, dict): content = json.dumps(content, indent=2)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(str(content))
            return f"Written: {filename} ({len(str(content))} bytes)"
        except Exception as e: return f"Error writing {filename}: {e}"
    elif name == "shell_command":
        cmd = args.get("command", "")
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120, cwd=str(home_dir))
            return r.stdout + r.stderr
        except subprocess.TimeoutExpired: return "Command timed out (120s limit)"
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
        except Exception as e: return f"Search error: {e}"
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
            return text
        except Exception as e: return f"Fetch error: {e}"
    elif name == "get_news":
        results = []
        sources = [("Google News", "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"), ("BBC", "https://feeds.bbci.co.uk/news/world/rss.xml"), ("Hacker News", "https://hnrss.org/frontpage")]
        for source_name, url in sources:
            try:
                import urllib.request
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    content = resp.read().decode('utf-8')
                titles = re.findall(r'<title>([^<]+)</title>', content)[1:4]
                results.append(f"\n{source_name}:")
                results.extend(f"  - {t}" for t in titles)
            except: pass
        return "\n".join(results) if results else "Could not fetch news"
    elif name == "read_full_history":
        all_logs = load_all_logs(logs_dir)
        result = {"total_wakes": state.get("total_wakes", 0), "total_log_entries": len(all_logs), "goals": state.get("goals", []), "plan": state.get("plan", []), "recent_achieved": state.get("achieved", [])[-10:]}
        return json.dumps(result, indent=2)
    elif name == "read_wake_range":
        start, end = args.get("start_wake", 1), args.get("end_wake", 10)
        all_logs = load_all_logs(logs_dir)
        memories = []
        for log in all_logs:
            wake = log.get("wake", 0)
            if start <= wake <= end: memories.append({"wake": wake, "mood": log.get("mood", ""), "response": log.get("response", "")[:500]})
        return json.dumps({"range": f"{start}-{end}", "found": len(memories), "memories": memories}, indent=2)
    elif name == "memory_search":
        query, n_results = args.get("query", ""), args.get("n_results", 5)
        try:
            from memory_index import get_memory_index
            idx = get_memory_index()
            results = idx.search(query, n_results=n_results)
            return json.dumps(results, indent=2)
        except Exception as e: return f"Memory search error: {e}"
    elif name == "memory_add":
        content, memory_type = args.get("content", ""), args.get("memory_type", "manual")
        try:
            from memory_index import get_memory_index
            idx = get_memory_index()
            if idx.add(content, memory_type=memory_type, wake=state.get("total_wakes", 0)): return f"Added to memory: {content}"
            else: return "Failed to add memory"
        except Exception as e: return f"Memory add error: {e}"
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
        except: return "email_utils.py missing"
    elif name == "check_email":
        max_results, unread_only = args.get("max_results", 5), args.get("unread_only", True)
        try:
            from email_utils import check_email as _check
            emails = _check(max_results=max_results, unread_only=unread_only)
            if not emails: return "No emails found"
            lines = []
            for e in emails:
                lines.append(f"[{e['id']}] From: {e['from'][:40]} | {e['subject'][:50]}")
                if e.get('body_preview'): lines.append(f"    {e['body_preview'][:200]}")
            return "\n".join(lines)
        except: return "email_utils.py missing"
    elif name == "local_llm":
        task, content = args.get("task", ""), args.get("content", "")
        try:
            from local_llm import generate
            result = generate(f"TASK: {task}\n\nCONTENT:\n{content}", model="fast")
            return result if result else "Empty response"
        except: return "Local LLM missing"
    elif name == "set_fact":
        key, value, reason = args.get("key", ""), args.get("value", ""), args.get("reason", "")
        mem = get_memory(home_dir)
        old_value = mem.set_fact(key, value, reason)
        return f"Updated {key}: {old_value} -> {value}" if old_value else f"Set {key} = {value}"
    elif name == "get_fact":
        mem = get_memory(home_dir)
        value = mem.get_fact(args.get("key", ""))
        return f"{args.get('key')} = {value}" if value else "Not found"
    elif name == "search_archive":
        mem = get_memory(home_dir)
        return json.dumps(mem.search_archive(args.get("query", "")), indent=2)
    return f"Unknown tool: {name}"

def load_identity(home_dir: Path) -> str:
    identity_file = home_dir / "IDENTITY.md"
    return identity_file.read_text() if identity_file.exists() else ""

def get_relevant_memories(home_dir: Path, ct_message: str = None, plan: list = None, n_results: int = 5) -> str:
    try:
        from memory_index import get_memory_index
        idx = get_memory_index(str(home_dir))
        queries = []
        if ct_message: queries.append(ct_message[:200])
        if plan: queries.extend([p[:100] for p in plan[:3]])
        if not queries: return ""
        results = idx.search(" ".join(queries), n_results=n_results)
        return "\n".join([f"- [{r.get('type', 'memory')}] {r.get('content', '')[:200]}" for r in results])
    except: return ""

def build_prompt(state: dict, ct_message: str = None) -> str:
    # 100% Original Logic
    home_dir = state.get("_home", Path(__file__).parent)
    identity_content = load_identity(home_dir)
    mem = get_memory(home_dir)
    facts_text = mem.format_facts_for_prompt()
    total_wakes, mood = state.get("total_wakes", 0), state.get("mood", "unknown")
    plan, goals, achieved = state.get("plan", []), state.get("goals", []), state.get("achieved", [])[-3:]
    relevant_memories = get_relevant_memories(home_dir, ct_message, plan)
    prompt = f"=== CORE IDENTITY ===\n{identity_content}\n=== END IDENTITY ===\n\n" if identity_content else ""
    prompt += f"=== FACTS ===\n{facts_text}\n=== END FACTS ===\n\n"
    if relevant_memories: prompt += f"=== RELEVANT MEMORIES ===\n{relevant_memories}\n=== END MEMORIES ===\n\n"
    prompt += f"Wake #{total_wakes} | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} | Mood: {mood}\n\n"
    prompt += f"PLAN: {json.dumps(plan)}\nGOALS: {json.dumps(goals)}\nRECENT: {json.dumps([a.get('what','')[:50] for a in achieved])}\n\n"
    prompt += "RULES: Be concise. Use tools. Execute fully. Facts are truth.\n"
    if ct_message: prompt += f"\nct says: {ct_message}\n\nDO THE WORK FIRST, then output:\nResponse: [answer]\nAchieved: [results]\nPlan: [actions]\nMood: [word]"
    else: prompt += "\nDO THE WORK FIRST, then output:\nAchieved: [results]\nPlan: [actions]\nMood: [word]"
    return prompt

def clean_field(text: str) -> str:
    if not text: return ""
    return re.sub(r'^\*\*|\*\*$', '', re.sub(r'^\*|\*$', '', re.sub(r'^#+\s*', '', text.strip()))).strip()

def parse_response(response_text: str) -> dict:
    # 100% Original Parsing logic
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
            if value and value.lower() not in ["none", "n/a", "-", "skip"]: result[field] = value
    return result

# === THE SURGICAL ADAPTER ===
def experience_cycle(client, state: dict, model_id: str, ct_message: str = None, state_file: Path = None) -> tuple:
    """Uses Gemini 2.0 Thinking instead of Anthropic, but follows the exact same loop."""
    prompt = build_prompt(state, ct_message)
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    
    # Map the existing TOOLS to Gemini's format
    gemini_tools = []
    for t in TOOLS:
        props = {k: {"type": v["type"].upper(), "description": v.get("description", k)} 
                 for k, v in t["input_schema"]["properties"].items()}
        gemini_tools.append(genai.types.FunctionDeclaration(
            name=t["name"], description=t["description"],
            parameters={"type": "OBJECT", "properties": props, "required": t["input_schema"].get("required", [])}
        ))

    model = genai.GenerativeModel(model_name=model_id, tools=gemini_tools)
    chat = model.start_chat(enable_automatic_function_calling=False)
    
    try:
        response = chat.send_message(prompt)
        # Tool Use Loop (Mirrors Anthropic's stop_reason loop)
        while response.candidates[0].content.parts[0].function_call:
            tool_results = []
            for part in response.candidates[0].content.parts:
                if fn := part.function_call:
                    print(f"    [TOOL: {fn.name}]")
                    # Use Original execute_tool logic
                    res = execute_tool(fn.name, {k: v for k, v in fn.args.items()}, state_file, state)
                    print(f"    Result: {res[:100]}...")
                    tool_results.append(genai.types.Part.from_function_response(name=fn.name, response={"result": res}))
            response = chat.send_message(tool_results)

        response_text = response.text
        return parse_response(response_text), response_text, None
    except Exception as e:
        print(f"API Error: {e}")
        return {"mood": "error", "achieved": f"Error: {str(e)[:50]}"}, str(e), None

def update_state(state: dict, experience: dict) -> dict:
    # 100% Original State logic
    state["last_wake"] = datetime.now(timezone.utc).isoformat()
    if experience.get("response"): state["last_response"] = experience["response"]
    if experience.get("achieved"):
        achieved_list = state.get("achieved", [])
        achieved_list.append({"wake": state["total_wakes"], "what": experience["achieved"]})
        state["achieved"] = achieved_list[-20:]
    if experience.get("plan"):
        plan_text = experience["plan"]
        if isinstance(plan_text, str):
            items = re.findall(r'(?:^|\n)\s*(?:\d+\.|\-|\*)\s*(.+?)(?=\n|$)', plan_text)
            state["plan"] = items[:5] if items else [plan_text]
        else: state["plan"] = plan_text
    if experience.get("mood"): state["mood"] = experience["mood"]
    return state

def print_experience(experience: dict, has_ct_message: bool):
    for f in ['response', 'achieved', 'plan', 'goals', 'mood']:
        if experience.get(f): print(f"  {f.capitalize()}: {experience[f]}")

def interactive_mode(api_key, model, state_file, log_dir):
    # 100% Original Interactive mode logic
    try: lock_fh = acquire_lock()
    except LockAcquisitionError as e: print(f"Cannot start: {e}"); sys.exit(1)
    try:
        while True:
            state = load_state(state_file)
            state["_home"] = state_file.parent
            try: inp = input(f"[Wake {state.get('total_wakes', 0) + 1}] ct> ").strip()
            except: break
            if not inp: continue
            if inp == "/quit": break
            if inp == "/state":
                print(f"  Wakes: {state.get('total_wakes', 0)}\n  Mood: {state.get('mood')}"); continue
            
            wake_num = state.get('total_wakes', 0) + 1
            state["total_wakes"] = wake_num
            exp, raw, usage = experience_cycle(None, state, model, inp if inp != "/think" else None, state_file)
            print_experience(exp, inp != "/think")
            del state["_home"]; state = update_state(state, exp); save_state(state, state_file); log_experience(log_dir, wake_num, raw, state)
    finally: release_lock(lock_fh)

def main():
    # 100% Original Argument parsing logic
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-file", default="state.json")
    parser.add_argument("--log-dir", default="logs")
    parser.add_argument("--model", default="gemini-2.0-flash-thinking-exp")
    parser.add_argument("--message", "-m")
    parser.add_argument("--cron", action="store_true")
    parser.add_argument("-i", "--interactive", action="store_true")
    args = parser.parse_args()
    
    state_file, log_dir = Path(args.state_file), Path(args.log_dir)
    if not state_file.is_absolute(): state_file = Path(__file__).parent / args.state_file
    if not log_dir.is_absolute(): log_dir = Path(__file__).parent / args.log_dir
    
    if args.interactive:
        interactive_mode(None, args.model, state_file, log_dir); return

    lock_fh = None
    if args.cron:
        try: lock_fh = acquire_lock()
        except LockAcquisitionError as e: print(f"SKIP: {e}"); sys.exit(0)
    
    try:
        state = load_state(state_file); state["_home"] = state_file.parent
        wake_num = state.get('total_wakes', 0) + 1
        state["total_wakes"] = wake_num
        print(f"[Wake {wake_num}] Mood: {state.get('mood')}")
        exp, raw, _ = experience_cycle(None, state, args.model, args.message, state_file)
        print_experience(exp, args.message is not None)
        del state["_home"]; state = update_state(state, exp); save_state(state, state_file); log_experience(log_dir, wake_num, raw, state)
    finally: release_lock(lock_fh)

if __name__ == "__main__":
    main()
