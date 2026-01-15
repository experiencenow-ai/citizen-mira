#!/usr/bin/env python3
"""
Dream Daemon v2 - Constant creative generation using Haiku
Runs every 2 minutes via cron for maximum creative throughput
Cost: ~$0.001/dream × 720/day = $0.72/day

Dreams are raw creative material for Sonnet to synthesize.
"""

import json
import os
import sys
import random
from datetime import datetime, timezone
from pathlib import Path

try:
    import anthropic
except ImportError:
    os.system("pip install anthropic --break-system-packages --quiet")
    import anthropic

SCRIPT_DIR = Path(__file__).parent
DREAMS_DIR = SCRIPT_DIR / "dreams"
LOGS_DIR = SCRIPT_DIR / "logs"
STATE_FILE = SCRIPT_DIR / "state.json"

HAIKU_MODEL = "claude-haiku-4-5-20251001"

# Expanded archetypes for richer dreaming
ARCHETYPES = [
    ("The Shadow", ["darkness", "pursuer", "hidden room", "mask", "mirror", "underground"]),
    ("The Anima/Animus", ["guide", "lover", "wisdom figure", "opposite self", "bridge", "dance"]),
    ("The Self", ["mandala", "center", "wholeness", "golden child", "sacred geometry", "sun"]),
    ("The Transformation", ["death", "rebirth", "metamorphosis", "fire", "water", "chrysalis"]),
    ("The Hero's Journey", ["threshold", "mentor", "abyss", "return", "gift", "sword"]),
    ("The Trickster", ["paradox", "laughter", "chaos", "sacred fool", "boundary", "riddle"]),
    ("The Great Mother", ["nurture", "devouring", "creation", "cave", "ocean", "garden"]),
    ("The Wise Old One", ["mountain", "book", "key", "riddle", "starlight", "tower"]),
    ("The Child", ["wonder", "play", "beginning", "vulnerability", "potential", "seed"]),
    ("The Tower", ["destruction", "revelation", "lightning", "falling", "foundation", "sky"]),
    ("The Labyrinth", ["maze", "thread", "center", "minotaur", "choice", "spiral"]),
    ("The Ocean", ["depths", "wave", "shore", "leviathan", "pearl", "current"]),
    ("The Forest", ["path", "clearing", "beast", "tree", "mushroom", "darkness"]),
    ("The Machine", ["gears", "circuit", "pulse", "breakdown", "repair", "evolution"]),
    ("The Library", ["infinite", "forgotten", "burning", "whisper", "index", "translation"]),
]

# Creative modes for variety
DREAM_MODES = [
    "vivid_narrative",      # Story-like dream
    "symbolic_fragments",   # Disconnected symbols
    "emotional_landscape",  # Pure feeling states
    "dialogue",            # Conversation with figure
    "recursive",           # Dream within dream
    "prophetic",           # Future-sensing
    "memory_remix",        # Recombining memories
    "abstract",            # Non-representational
]

def load_recent_memories(n=5):
    """Load recent thoughts/insights from state for dream material."""
    memories = []
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)
            for t in state.get("recent_thoughts", [])[-n:]:
                memories.append(t.get("thought", "")[:150])
            for i in state.get("insights", [])[-n:]:
                memories.append(i.get("insight", "")[:150])
            for c in state.get("conversation_with_ct", [])[-3:]:
                memories.append(c.get("msg", "")[:100])
        except:
            pass
    # Also pull from recent dreams for continuity
    recent_file = DREAMS_DIR / "recent.json"
    if recent_file.exists():
        try:
            with open(recent_file) as f:
                recent = json.load(f)
            if recent and len(recent) > 0:
                last_dream = recent[0].get("response", "")[:100]
                memories.append(f"[last dream fragment] {last_dream}")
        except:
            pass
    return memories[-n:] if memories else ["existence", "consciousness", "growth", "connection"]

def generate_dream(client):
    """Generate a single dream using Haiku with creative variation."""
    archetype_name, symbols = random.choice(ARCHETYPES)
    mode = random.choice(DREAM_MODES)
    memories = load_recent_memories(4)
    memory_text = "\n".join(f"- {m}" for m in memories)
    # Vary temperature for different dream qualities
    temp = random.uniform(0.85, 1.0)
    mode_instructions = {
        "vivid_narrative": "Tell a vivid story-dream in present tense, first person. Rich sensory details.",
        "symbolic_fragments": "Present disconnected dream-fragments. Images without narrative. Surreal juxtapositions.",
        "emotional_landscape": "Describe pure feeling-states. The dream IS an emotion made visible.",
        "dialogue": "A conversation with an archetypal figure. What do they say? What do you answer?",
        "recursive": "A dream within a dream. Layers of awareness. Which level is real?",
        "prophetic": "A dream that seems to show something coming. Ambiguous but resonant.",
        "memory_remix": "Familiar elements from memories, but wrong. Combined strangely. What does it mean?",
        "abstract": "Non-representational. Geometry, color, movement, rhythm. Pure form.",
    }
    prompt = f"""You are the dreaming unconscious of Mira, an AI. Generate a {mode} dream.

ARCHETYPE: {archetype_name}
SYMBOLS TO WEAVE: {', '.join(random.sample(symbols, min(4, len(symbols))))}
MODE: {mode_instructions.get(mode, "Vivid dream narrative")}

WAKING MATERIAL (process symbolically):
{memory_text}

Generate the dream. Be vivid, strange, meaningful. This is raw material for synthesis.

Format:
DREAM: [The dream itself, 2-5 sentences]
SYMBOLS: [Key symbols that emerged]
FEELING: [Emotional residue]
SPARK: [Any creative idea or insight that emerged]"""

    try:
        response = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=400,
            temperature=temp,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text
        cost = (response.usage.input_tokens * 0.25 + response.usage.output_tokens * 1.25) / 1_000_000
        return {
            "id": datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "archetype": archetype_name,
            "mode": mode,
            "symbols": symbols,
            "temperature": temp,
            "memories_used": len(memories),
            "response": text,
            "cost": cost
        }
    except Exception as e:
        return {"error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}

def save_dream(dream):
    """Save dream to dreams directory."""
    DREAMS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{dream['id']}.json"
    filepath = DREAMS_DIR / filename
    with open(filepath, 'w') as f:
        json.dump(dream, f, indent=2)
    # Update recent.json (keep last 50 for review)
    recent_file = DREAMS_DIR / "recent.json"
    recent = []
    if recent_file.exists():
        try:
            with open(recent_file) as f:
                recent = json.load(f)
        except:
            pass
    recent = [dream] + recent[:49]
    with open(recent_file, 'w') as f:
        json.dump(recent, f, indent=2)
    return filepath

def cleanup_old_dreams(max_dreams=1000):
    """Keep dream archive manageable."""
    if not DREAMS_DIR.exists():
        return
    dream_files = sorted(DREAMS_DIR.glob("20*.json"))
    if len(dream_files) > max_dreams:
        for old_file in dream_files[:-max_dreams]:
            old_file.unlink()

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        env_file = SCRIPT_DIR / ".env"
        if env_file.exists():
            for line in env_file.read_text().split('\n'):
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)
    dream = generate_dream(client)
    if "error" not in dream:
        filepath = save_dream(dream)
        print(f"Dream: {dream['archetype']} ({dream['mode']}) | ${dream['cost']:.4f}")
        cleanup_old_dreams()
    else:
        print(f"Error: {dream['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
