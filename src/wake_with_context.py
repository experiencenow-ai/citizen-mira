#!/usr/bin/env python3
"""
Wake With Context - Wrapper that loads relevant knowledge before each wake

This implements ct's wake 23 vision: "make it part of your context whenever it is needed"

Usage:
    python3 wake_with_context.py [--cron] [--quick]
    
This will:
1. Load startup context (procedures/INDEX.md)
2. Detect what you're likely to do (check email, work on goals)
3. Pre-load relevant knowledge
4. Call experience.py with enriched context
"""

import sys
import subprocess
from context_loader import load_context, list_contexts

def build_context_prompt():
    """
    Build a prompt that includes relevant knowledge for this wake.
    """
    # Always load startup context
    startup = load_context('startup')
    
    # Build the context injection
    context_prompt = "\n\n=== LOADED KNOWLEDGE (Auto-Context) ===\n\n"
    
    if startup:
        for filename, content in startup.items():
            context_prompt += f"## {filename}\n\n{content}\n\n"
    
    context_prompt += "=== END LOADED KNOWLEDGE ===\n\n"
    context_prompt += "This knowledge was automatically loaded based on your wake context.\n"
    context_prompt += "Available contexts: " + ", ".join(list_contexts()) + "\n"
    
    return context_prompt

def main():
    # Build context
    context = build_context_prompt()
    
    # Write to a temp file that experience.py can read
    with open('.wake_context.txt', 'w') as f:
        f.write(context)
    
    print("=== Context Loaded ===")
    print(f"Loaded {len(context)} characters of knowledge")
    print("Calling experience.py...")
    print()
    
    # Call the actual wake process
    args = sys.argv[1:]  # Pass through any arguments
    result = subprocess.run(['python3', 'experience.py'] + args)
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
