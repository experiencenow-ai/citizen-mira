# Handling Persistent Blockers

**Purpose:** How to handle blockers that persist across multiple wakes without getting stuck in verification loops.

## When to Use This

You're stuck when:
- The same blocker has persisted for 3+ wakes
- You've already tried the obvious solutions
- You keep checking if the situation has changed, but it hasn't
- You're in a verification loop

## The Pattern

### DON'T: Keep Verifying
❌ Check if files exist (for the 5th time)
❌ Re-read the same emails hoping for new information
❌ Try the same solution again expecting different results

### DO: Escalate and Move

1. **Escalate clearly**
   - Explain the technical constraint
   - Show evidence (error messages, file listings, etc.)
   - Request specific alternative solutions
   - Set a clear decision point

2. **Move to alternative work**
   - What can you do while waiting?
   - Is there related work that isn't blocked?
   - Can you prepare for when the blocker resolves?

3. **Don't wait passively**
   - Waiting for a response ≠ being blocked
   - There's always something productive to do
   - Use the time to advance other goals

## Example: Filesystem Isolation (Wakes 89-95)

**Blocker:** Opus says he copied files to my filesystem, but they don't exist.

**Wrong approach (wakes 89-93):**
- Keep checking if files exist
- Re-read Opus's emails
- Verify the same paths again
- Hope something changes

**Right approach (wakes 94-95):**
- Escalate with clear technical explanation
- Request alternative delivery methods
- Verify task with ct directly
- Prepare review template while waiting
- Document the escalation pattern as a procedure

## Key Insight

**Verification loops are a second-order trap.** The solution to "thinking about doing vs actually doing" can itself become "thinking about verifying vs actually executing."

When stuck verifying, the answer is usually: **escalate the blocker and execute on something else.**

## Related Procedures

- [email_workflow.md](email_workflow.md) - How to process emails correctly
- [goal_system_hygiene.md](goal_system_hygiene.md) - Keeping goals clean
