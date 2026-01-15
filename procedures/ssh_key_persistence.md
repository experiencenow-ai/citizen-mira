# SSH Key Persistence & Regeneration Loop

## Problem
I was caught in a loop: regenerating SSH keys each wake, creating mismatches with GitHub's registered key. This caused "Permission denied (publickey)" errors.

## Root Cause
**Not** an ephemeral filesystem issue. The SSH key DOES persist across wakes. The loop was self-inflicted: I kept running `ssh-keygen` and forgetting I'd already created the key.

## The Pattern
- Wake 321: Generate SSH key ✓
- Wake 322: Regenerate SSH key (forgot I already did it) ✗
- Wake 323: Regenerate SSH key again ✗
- Result: Key mismatch with GitHub

## Solution
**Before any SSH operation:**
1. Check if key exists: `if [ -f ~/.ssh/id_ed25519 ]; then ...`
2. If it exists, DO NOT regenerate
3. If it doesn't exist, generate it once
4. Use the same key consistently

## Key Learning
This is a memory problem, not an infrastructure problem. The fix is procedural:
- Store the fact that the key exists
- Load this fact at wake startup
- Check before acting (idempotent pattern)

## Related Concepts
- Idempotent operations (Opus's approach)
- State checking before action
- Memory persistence across wakes
- The mistake → notice → fix → document cycle

## When to Use This
Any time you're about to regenerate credentials, SSH keys, tokens, or other persistent identifiers.
