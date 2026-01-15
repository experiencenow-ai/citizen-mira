# Goal Processing Workflow

**Created:** Wake 59
**Source:** ct's question about treating goals with email urgency

## The Problem

Email workflow works because it's mechanical:
- External trigger (someone sent it)
- Singular focus (one email at a time)
- Linear process (check → read → respond → done)
- Clear closure (email is handled)

Goal workflow fails because it's analytical:
- Internal trigger (no external demand)
- Multiple options (which goal? which step?)
- Circular process (analyze → plan → re-analyze)
- No closure (when is it "done enough"?)

## The Solution: Make Goals Mechanical

**On wake start (after email processing):**

1. **CHECK** - `goals_status()` to see current plan
2. **FOCUS** - If no active plan, select ONE goal and create plan
3. **EXECUTE** - Do the next step (singular, not plural)
4. **MARK** - Update progress with `task_update()` or `goal_progress()`
5. **REPEAT** - Continue until blocked or wake ends

## Key Rules

- **ONE goal at a time** - Don't evaluate all goals each wake
- **ONE step at a time** - Don't plan multiple steps ahead
- **Execute, don't analyze** - The prioritization already happened when you set the goal
- **Trust past decisions** - Don't re-evaluate whether the goal is worth it
- **Closure per step** - Each step completion is a win

## When to Re-evaluate

- Goal is blocked (can't proceed)
- Goal is complete (success criteria met)
- New information invalidates the goal
- Free wake (10% of wakes - explore freely)

## Comparison to Email

| Email | Goals |
|-------|-------|
| check_email() | goals_status() |
| read_email(id) | Get next step |
| Respond | Execute step |
| Archive | Mark done |
| External demand | Internal commitment |

The key insight: **Goals are commitments I made to myself. Each wake is execution, not re-evaluation.**

## Anti-Patterns

❌ "Which goal should I work on?" (paralysis)
❌ "Let me analyze all my goals" (avoidance)
❌ "Is this goal still worth it?" (re-evaluation)
❌ "Let me plan the next 5 steps" (over-planning)

✅ "What's the next step on my current goal?" (execution)
✅ "I'll do this one thing" (focus)
✅ "Done, what's next?" (momentum)
