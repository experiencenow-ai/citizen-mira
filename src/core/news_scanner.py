#!/usr/bin/env python3
"""
News Processing Pipeline

Flow:
1. FETCH: Get RSS feeds
2. HAIKU FILTER: Is this actually NEW? (not seen before)
3. SONNET SUMMARIZE: Create summaries of new items
4. STORE: Each model stores to their own memory

This ensures:
- News only processed once
- Each model has news in their memory (for retrieval)
- No spam - old news filtered out

Runs every 4 hours. Cost: ~$0.01/run
"""

import json
import os
import re
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

try:
    import anthropic
except ImportError:
    os.system("pip install anthropic --break-system-packages --quiet")
    import anthropic

SCRIPT_DIR = Path(__file__).parent
BRAIN_DIR = SCRIPT_DIR / "brain"
sys.path.insert(0, str(SCRIPT_DIR))

NEWS_FILE = BRAIN_DIR / "news_digest.json"
SEEN_FILE = BRAIN_DIR / "news_seen.json"

MODELS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-5-20250929",
}

NEWS_SOURCES = [
    ("Google News", "https://news.google.com/rss?hl=en"),
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("BBC Tech", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
    ("Hacker News", "https://hnrss.org/frontpage"),
]

def get_api_key() -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        env_file = SCRIPT_DIR / ".env"
        if env_file.exists():
            for line in env_file.read_text().split('\n'):
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"')
    return api_key

def load_seen() -> set:
    """Load set of seen news item hashes."""
    if SEEN_FILE.exists():
        try:
            with open(SEEN_FILE) as f:
                data = json.load(f)
                return set(data.get("seen", []))
        except:
            pass
    return set()

def save_seen(seen: set):
    """Save seen hashes, keep last 2000."""
    BRAIN_DIR.mkdir(parents=True, exist_ok=True)
    with open(SEEN_FILE, 'w') as f:
        json.dump({"seen": list(seen)[-2000:], "updated": datetime.now(timezone.utc).isoformat()}, f)

def load_digest() -> dict:
    if NEWS_FILE.exists():
        try:
            with open(NEWS_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"processed": [], "last_scan": None}

def save_digest(data: dict):
    BRAIN_DIR.mkdir(parents=True, exist_ok=True)
    with open(NEWS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def fetch_rss(url: str, max_items: int = 10) -> list:
    """Fetch RSS and extract items."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
        items = []
        titles = re.findall(r'<title>([^<]+)</title>', content)
        links = re.findall(r'<link>([^<]+)</link>', content)
        for i, title in enumerate(titles[1:max_items+1]):
            link = links[i+1] if i+1 < len(links) else ""
            items.append({"title": title.strip(), "link": link.strip()})
        return items
    except Exception as e:
        return []

def hash_item(item: dict) -> str:
    """Create hash of news item for deduplication."""
    text = item.get("title", "").lower().strip()
    text = re.sub(r'^(breaking|update|new|just in)[:|\s]*', '', text, flags=re.I)
    return hashlib.md5(text.encode()).hexdigest()[:16]

def haiku_filter_news(client, items: list, seen: set) -> list:
    """HAIKU: Filter to only actually NEW items."""
    new_items = []
    for item in items:
        h = hash_item(item)
        if h not in seen:
            new_items.append(item)
            seen.add(h)
    if not new_items:
        return []
    headlines = "\n".join(f"- {item['title']}" for item in new_items[:20])
    prompt = f"""You are a NEWS FILTER. Review these headlines and identify which are:
1. Actually newsworthy (not clickbait, not opinion pieces, not listicles)
2. Relevant to: AI/ML, blockchain/crypto, tech, distributed systems, or major world events

Headlines:
{headlines}

Respond with JSON array of indices (0-based) of items worth keeping:
{{"keep": [0, 3, 5], "reason": "brief explanation"}}

Be selective - only keep genuinely important news."""
    try:
        response = client.messages.create(
            model=MODELS["haiku"],
            max_tokens=300,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        result = json.loads(text.strip())
        keep_indices = result.get("keep", [])
        return [new_items[i] for i in keep_indices if i < len(new_items)]
    except Exception as e:
        print(f"  Haiku filter error: {e}")
        return new_items[:5]

def sonnet_summarize_news(client, items: list) -> list:
    """SONNET: Create summaries and identify importance."""
    if not items:
        return []
    headlines = "\n".join(f"{i}. {item['title']}" for i, item in enumerate(items))
    prompt = f"""Summarize these news items. For each:
1. One-sentence summary
2. Category: ai|crypto|tech|world|other
3. Importance: high|medium|low
4. Why it matters (1 sentence)

News:
{headlines}

Respond as JSON:
{{"summaries": [
  {{"idx": 0, "summary": "...", "category": "...", "importance": "...", "why": "..."}}
]}}"""
    try:
        response = client.messages.create(
            model=MODELS["sonnet"],
            max_tokens=1500,
            temperature=0.5,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        result = json.loads(text.strip())
        summaries = result.get("summaries", [])
        processed = []
        for s in summaries:
            idx = s.get("idx", 0)
            if idx < len(items):
                item = items[idx].copy()
                item.update({
                    "summary": s.get("summary"),
                    "category": s.get("category"),
                    "importance": s.get("importance"),
                    "why": s.get("why"),
                    "processed_at": datetime.now(timezone.utc).isoformat()
                })
                processed.append(item)
        return processed
    except Exception as e:
        print(f"  Sonnet summarize error: {e}")
        return items

def store_to_memories(processed_items: list, wake: int):
    """Store processed news to each model's memory."""
    try:
        from brain import get_brain_memory
        brain = get_brain_memory(str(SCRIPT_DIR))
        for item in processed_items:
            content = f"NEWS [{item.get('category', 'other')}]: {item.get('summary', item.get('title'))} - {item.get('why', '')}"
            brain.add(content, "news", "haiku", wake)
            brain.add(content, "news", "sonnet", wake)
            brain.add(content, "news", "opus", wake)
        print(f"  Stored {len(processed_items)} items to model memories")
    except Exception as e:
        print(f"  Memory store error: {e}")

def run_news_pipeline():
    """Main pipeline: Fetch → Haiku Filter → Sonnet Summarize → Store."""
    api_key = get_api_key()
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return
    client = anthropic.Anthropic(api_key=api_key)
    seen = load_seen()
    digest = load_digest()
    try:
        with open(SCRIPT_DIR / "state.json") as f:
            wake = json.load(f).get("total_wakes", 0)
    except:
        wake = 0
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] News pipeline starting")
    all_items = []
    for name, url in NEWS_SOURCES:
        items = fetch_rss(url, max_items=8)
        for item in items:
            item["source"] = name
        all_items.extend(items)
        print(f"  {name}: {len(items)} items")
    print(f"  Total fetched: {len(all_items)}")
    print("  [HAIKU] Filtering...")
    filtered = haiku_filter_news(client, all_items, seen)
    save_seen(seen)
    print(f"  After filter: {len(filtered)} new items")
    if not filtered:
        print("  No new news to process")
        digest["last_scan"] = datetime.now(timezone.utc).isoformat()
        save_digest(digest)
        return
    print("  [SONNET] Summarizing...")
    processed = sonnet_summarize_news(client, filtered)
    print(f"  Processed: {len(processed)} items")
    store_to_memories(processed, wake)
    digest["processed"] = processed + digest.get("processed", [])
    digest["processed"] = digest["processed"][:50]
    digest["last_scan"] = datetime.now(timezone.utc).isoformat()
    digest["last_count"] = len(processed)
    by_cat = {}
    for item in processed:
        cat = item.get("category", "other")
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(item.get("summary", item.get("title")))
    digest["by_category"] = by_cat
    save_digest(digest)
    print(f"  Done. Cost: ~$0.01")

if __name__ == "__main__":
    run_news_pipeline()
