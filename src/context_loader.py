#!/usr/bin/env python3
"""
Context Loader - Automatically load relevant knowledge based on what I'm doing

This solves ct's wake 16/23 challenge: "figure out how to save this knowledge 
in a way that you will not forget it"

The system:
1. Detect what context I'm in (email, goals, debugging, etc.)
2. Load relevant procedures/knowledge files
3. Inject them into my working memory

Usage:
    from context_loader import load_context
    
    # When checking email
    knowledge = load_context('email')
    
    # When working on goals
    knowledge = load_context('goals')
    
    # When debugging
    knowledge = load_context('debug')
"""

import os
import json
from pathlib import Path

# Context → Knowledge mapping
CONTEXT_MAP = {
    'email': [
        'procedures/email_workflow.md',
    ],
    'goals': [
        'procedures/goal_system_hygiene.md',
    ],
    'startup': [
        'procedures/INDEX.md',
    ],
    'ct_messages': [
        # ct's key messages about the system
        'ct_wake_16_23.txt',  # The forgetting problem
    ],
}

def load_context(context_name):
    """
    Load all knowledge files for a given context.
    
    Args:
        context_name: One of 'email', 'goals', 'startup', 'ct_messages'
        
    Returns:
        dict: {filename: content} for all relevant files
    """
    if context_name not in CONTEXT_MAP:
        return {}
    
    knowledge = {}
    for filepath in CONTEXT_MAP[context_name]:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                knowledge[filepath] = f.read()
        else:
            print(f"Warning: {filepath} not found")
    
    return knowledge

def get_context_summary(context_name):
    """
    Get a brief summary of what knowledge is available for a context.
    """
    if context_name not in CONTEXT_MAP:
        return f"Unknown context: {context_name}"
    
    files = CONTEXT_MAP[context_name]
    existing = [f for f in files if os.path.exists(f)]
    missing = [f for f in files if not os.path.exists(f)]
    
    summary = f"Context '{context_name}' has {len(existing)} knowledge files:\n"
    for f in existing:
        summary += f"  ✓ {f}\n"
    if missing:
        summary += f"\nMissing {len(missing)} files:\n"
        for f in missing:
            summary += f"  ✗ {f}\n"
    
    return summary

def add_context_mapping(context_name, filepath):
    """
    Add a new file to a context's knowledge map.
    This modifies the CONTEXT_MAP in memory - to persist, update this file.
    """
    if context_name not in CONTEXT_MAP:
        CONTEXT_MAP[context_name] = []
    
    if filepath not in CONTEXT_MAP[context_name]:
        CONTEXT_MAP[context_name].append(filepath)
        return True
    return False

def list_contexts():
    """List all available contexts."""
    return list(CONTEXT_MAP.keys())

if __name__ == '__main__':
    # Test the system
    print("=== Context Loader Test ===\n")
    
    for context in list_contexts():
        print(get_context_summary(context))
        print()
    
    # Try loading email context
    print("=== Loading 'email' context ===")
    knowledge = load_context('email')
    for filename, content in knowledge.items():
        print(f"\n{filename}:")
        print(content[:200] + "..." if len(content) > 200 else content)
