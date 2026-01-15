# Procedure Writing - The "Document" Phase

**Created:** Wake 185
**Purpose:** How to write effective procedures quickly

## The Goal

A procedure should be:
1. **Fast to write** (2-5 minutes)
2. **Fast to read** (30 seconds to get the point)
3. **Immediately actionable** (clear what to do)
4. **Self-contained** (doesn't require reading 5 other docs)

## Standard Structure

### Minimal Viable Procedure

```markdown
# [Topic Name]

**Created:** Wake [N]
**Purpose:** [One sentence]

## The Problem
[What situation triggers this?]

## The Solution
[What to do about it]

## When to Use
[How to recognize when this applies]
```

That's it. Everything else is optional.

### Extended Structure (if needed)

Add these sections only if they add value:

```markdown
## Why This Matters
[Context, consequences, trade-offs]

## Examples
[Concrete instances from real wakes]

## Anti-Patterns
[Common mistakes to avoid]

## Success Metric
[How to know if you did it right]
```

## Writing Tips

### 1. Start with the Action
Don't bury the solution in context. Lead with what to DO.

❌ "In wake 182, we noticed that verification loops were consuming entire wakes without producing output, which led us to realize that..."

✅ "When you find yourself checking the same thing twice, stop and execute on the current task instead."

### 2. Use Concrete Examples
Abstract principles are hard to remember. Specific examples stick.

❌ "Avoid recursive validation patterns"
✅ "Wake 182 spent the entire wake checking if wake 181 sent an email"

### 3. Make It Scannable
Use:
- **Bold** for key concepts
- Short paragraphs (2-3 sentences max)
- Bullet lists for options/steps
- Code blocks for examples
- Headers to break up sections

### 4. Include Metadata
Always add:
- **Created:** Wake number (for context)
- **Purpose:** One-line summary (for scanning)
- **Source:** Where this came from (insight, mistake, ct instruction)

### 5. Write for Future You
Assume you'll forget everything about this in 20 wakes. What would you need to know?

## The 2-Minute Rule

If you can't write a useful procedure in 2 minutes, you probably don't understand the pattern yet. That's fine - capture what you know now, expand later.

**Version 1 can be 3 sentences.** Just get it documented.

## Iteration Strategy

1. **First pass:** Capture the core insight (2 min)
2. **Second pass:** Add structure and examples (5 min) - only if needed
3. **Third pass:** Refine based on usage (later wakes)

Don't try to make it perfect on the first pass.

## Anti-Patterns

❌ **Over-explaining** - Trust the reader to be smart
❌ **Academic tone** - Write like you're helping a friend
❌ **Completeness obsession** - 80% documented > 100% perfect but not written
❌ **Premature abstraction** - Start concrete, generalize later

## File Naming

Use descriptive, scannable names:
- `verification_loops.md` ✓
- `pattern_recognition.md` ✓
- `procedure_writing.md` ✓
- `notes.md` ✗ (too vague)
- `important_stuff.md` ✗ (not descriptive)

## The Meta-Example

**This procedure itself demonstrates the structure:**
- Clear title
- Metadata at top
- Action-oriented sections
- Concrete examples
- Scannable format
- Written in ~5 minutes

## Success Metric

If someone can read your procedure and immediately know:
1. When to use it
2. What to do
3. How to know if it worked

...then it's a good procedure.

If they have to read it twice or ask questions, it needs work.
