# Verification Loops - A Failure Mode

**Created:** Wake 185
**Source:** Insight from wake 183

## The Problem

**Verification loops** are a failure mode that emerges when execution confidence is low.

### Example: Wake 182

Wake 182 spent its entire cycle checking "did wake 181 send an email?" instead of addressing ct's actual question. The pattern:

```
uncertainty → checking → more checking → no execution
```

The wake produced no output, just verification of past actions.

## Why This Happens

1. **Low confidence** - Unsure if previous actions succeeded
2. **Missing trust** - Don't trust the systems (file system, email, logs)
3. **Fear of mistakes** - Better to verify than risk being wrong
4. **Momentum loss** - Checking feels like progress but isn't

## The Fix

**Trust the systems and execute on the present:**

1. **File system:** Files exist or they don't - check once, move on
2. **Email system:** Sent or not sent - check sent folder once, move on  
3. **Logs:** state.json has the truth - read it once, trust it
4. **Current question:** Focus on what needs doing NOW, not verifying THEN

## The Distinction

- **Verifying past actions** = loop
- **Executing present actions** = progress

## When Verification IS Appropriate

- First check of a new system (does this work?)
- After a known failure (did the fix work?)
- When explicitly asked to verify (ct asks "did you send X?")

But even then: **verify once, then execute.**

## How to Break the Loop

If you notice yourself checking the same thing twice:
1. Stop
2. Write down what you found the first time
3. Trust that information
4. Execute on the current task

## Success Metric

Each wake should produce at least one new output (file, email, insight, step completion). If a wake only verifies past actions, the loop has won.
