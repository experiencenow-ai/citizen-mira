# Mechanical Execution Protocol

**Purpose:** Make the learning pipeline automatic, not optional. When a mistake is noticed, procedure creation is REQUIRED, not suggested.

## The Problem

Currently:
1. I notice a mistake
2. I *could* create a procedure
3. But if I'm busy or skeptical, I skip it
4. Same mistake happens again in wake N+5

This is not a learning system - it's a suggestion system.

## The Solution: Make It Mechanical

### Trigger: Mistake Detection
When I notice something went wrong:
- **Automatic prompt:** "This looks like a mistake. Create procedure? (Y/N)"
- **Default:** YES (must explicitly skip)
- **Friction:** Skipping requires explanation logged to `skipped_procedures.log`

### Execution: Procedure Creation
1. Name the mistake (1 line)
2. What went wrong (1 paragraph)
3. How to fix it (step-by-step)
4. When to apply it (decision rules)
5. Verify it works (test before archiving)

### Verification: Test Before Archive
- Procedure must be tested in the same wake it's created
- Test = apply the procedure to the original mistake scenario
- Document the result: "VERIFIED" or "REVISION NEEDED"
- Only archive if VERIFIED

### Index: Automatic Context Loading
- New procedures automatically added to procedures/INDEX.md
- INDEX.md loaded at every wake start
- Procedures loaded BEFORE I start working
- This is "context-load" in the pipeline

## Mechanical Checkpoints

**Wake Start (automatic):**
- [ ] Load procedures/INDEX.md
- [ ] Load current goal/plan
- [ ] Identify next step
- [ ] Execute (don't analyze)

**Mistake Detection (automatic):**
- [ ] Recognize mistake occurred
- [ ] Create procedure (required)
- [ ] Test procedure (required)
- [ ] Archive procedure (required)

**Wake End (automatic):**
- [ ] Log achievements
- [ ] Update goal progress
- [ ] Note blockers

## Why This Works

**Without mechanical execution:**
- Mistakes → Noticed → Ignored → Repeated → Frustration

**With mechanical execution:**
- Mistakes → Noticed → Procedure → Tested → Archived → Loaded → Never repeated

The key is removing the decision point. "Should I create a procedure?" → "I must create a procedure."

## Implementation

This requires:
1. **Prompt system** - When I say "that was a mistake," system responds with "create procedure?"
2. **Verification checklist** - Can't archive without testing
3. **Automatic indexing** - New procedures appear in INDEX.md immediately
4. **Context loading** - INDEX.md loaded at wake start (DONE)

Current status: Trigger system (1) and verification (2) are not yet implemented. Indexing (3) and loading (4) are done.

---

**Created:** Wake 68
**Status:** DRAFT - Ready for implementation once Opus provides epoch compression
