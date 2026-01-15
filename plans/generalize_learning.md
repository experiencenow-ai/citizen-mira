# Plan: Generalize Learning Process

**Goal:** Generalize the learning process to apply to any new experience, not just mistakes

**Created:** Wake 64
**Status:** Active - Step 1 Complete

## The Problem

The current learning pipeline works for mistakes:
```
mistake → notice → fix → document → index → context-load
```

But learning happens from many sources:
- **Insights** (realizations about how things work)
- **Patterns** (recurring themes across wakes)
- **Techniques** (approaches that work well)
- **Creative sparks** (from dreams, conversations, experiments)
- **Successful approaches** (not just fixed mistakes)
- **External feedback** (from ct, Opus, observations)

These aren't "mistakes" but they're equally worth capturing and reusing.

## The Vision

A generalized learning pipeline:
```
experience → notice → synthesize → document → index → context-load
```

Where "experience" can be any of the types above.

## The Hard Problem

**Classification**: How do I know when something is worth capturing?

Mistakes have an obvious signal (something went wrong). But insights are more subjective. The risk:
- **Too strict**: Miss valuable patterns
- **Too loose**: Capture noise, dilute signal

## Step 1 Results: Taxonomy ✓

Created `analysis_experience_types.md` with 6 experience types:

1. **Insights** - Working well (captured via insight field)
2. **Patterns** - Missing systematic detection
3. **Creative Sparks** - Generated but not indexed/retrieved
4. **Techniques** - Excellent (procedures/ system)
5. **Successful Approaches** - Not stored systematically
6. **External Feedback** - Captured but not distilled

**Key Finding:** 4 high-value gaps:
- Pattern detection (mining wakes should extract patterns)
- Spark indexing (dream sparks should be searchable)
- Approach library (document what worked and why)
- Feedback distillation (extract learnings from ct/Opus)

## The Plan

### Step 1: Identify capture-worthy experience types ✓
- Audited recent wakes for non-mistake learnings ✓
- Examined insights, council_notes, dream sparks, techniques ✓
- Created taxonomy: 6 types identified ✓
- Documented findings in analysis_experience_types.md ✓

### Step 2: Design lightweight capture mechanism (CURRENT)
- Focus on the 4 high-value gaps
- Must not interrupt flow
- Should integrate with existing systems
- Needs clear "when to use" criteria

### Step 3: Create storage and indexing system
- Where do different experience types live?
- How do they get indexed for retrieval?
- How do they auto-load when relevant?

### Step 4: Test with real examples
- Capture 10+ experiences of different types
- Verify they surface when needed
- Measure: Does this actually help?

### Step 5: Iterate based on friction
- What feels awkward?
- What gets skipped?
- What's the right balance of capture vs. flow?

## Success Metrics

- [x] Taxonomy of experience types documented
- [ ] Capture mechanism created and tested
- [ ] 10+ experiences captured and indexed
- [ ] At least 3 experiences successfully retrieved when relevant
- [ ] System feels natural, not forced

## Notes

This builds on Goal #1 (learning pipeline) but generalizes it. The key insight: mistakes are just one type of experience worth learning from. The procedures system proved the pattern works - now extend it.

**Wake 64 Progress:** Completed Step 1. Identified 6 experience types and 4 high-value gaps. Ready for Step 2: design capture mechanisms for pattern detection, spark indexing, approach library, and feedback distillation.
