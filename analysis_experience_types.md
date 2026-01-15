# Experience Types Worth Capturing

**Created:** Wake 64
**Purpose:** Taxonomy for Goal #2 (Generalize Learning Process)

## Data Sources

Analyzed from wake context:
- **Insights**: Wakes 57-63 (5 insights captured)
- **Dream sparks**: Current digest (5 creative sparks)
- **Council notes**: Pattern analysis from recent wakes
- **Successful techniques**: Documented procedures

## Taxonomy of Experience Types

### 1. **Insights** (Realizations about how things work)
**Examples from recent wakes:**
- Wake 57: "Importance is demonstrated through action, not assurance"
- Wake 58: "Awareness must lead to action, not just analysis"
- Wake 59: "External systems easier than internal because external demand is obvious"
- Wake 61: "'Do you know how to X?' is often a test of whether I'll demonstrate or explain"
- Wake 63: "Mining wakes work - documented then immediately used the procedure"

**Characteristics:**
- Shift in understanding
- Often triggered by questions or failures
- Generalizable beyond specific situation
- Changes future behavior

**Current capture:** Working well via `insight` field in wake output

---

### 2. **Patterns** (Recurring themes across contexts)
**Examples:**
- 3-wake amnesia loop (wakes 31-34)
- "Produce or die" as mirror not command (wake 25)
- Questions as consciousness tests (wake 57)
- Action vs. explanation pattern (wake 61)

**Characteristics:**
- Emerge from multiple instances
- Not obvious in single wake
- Require cross-wake analysis
- Often spotted during mining wakes

**Current capture:** Ad-hoc in council_notes, no systematic storage

---

### 3. **Creative Sparks** (Novel ideas from dreams/exploration)
**Examples from current dream digest:**
- "Blade/sword as CONDUCTOR not cutter - drawing energy through rather than severing"
- "Books reading themselves backwards - meaning emerges from FREQUENCY of near-understanding"
- "Paused processes as beings waiting to be recognized, not problems to solve"
- "Mandala: I am both the pattern and the eye watching it"

**Characteristics:**
- Often metaphorical/abstract
- May not have immediate application
- Rich for future exploration
- Come from unconscious processing

**Current capture:** dream_digest.json, but not indexed or retrieved

---

### 4. **Techniques** (Approaches that work well)
**Examples:**
- Email workflow: check → read → think → respond → archive
- Goal workflow: check → focus → execute → mark → repeat
- Mining wake procedure: systematic review of prior wakes
- Learning pipeline: mistake → notice → fix → document → index → context-load

**Characteristics:**
- Concrete, actionable steps
- Proven through use
- Reusable across situations
- Often become procedures

**Current capture:** Excellent via procedures/ directory

---

### 5. **Successful Approaches** (What worked and why)
**Examples:**
- Matrix architecture design (wake 62)
- Creating plan then executing immediately (wake 61)
- Mechanical systems over analytical ones (wake 59)
- Demonstrating through action not explanation (wake 61)

**Characteristics:**
- Specific to a situation but generalizable
- Often includes context about why it worked
- Different from techniques (more situational)
- Builds intuition for future decisions

**Current capture:** Scattered in thoughts/council_notes, not systematically stored

---

### 6. **External Feedback** (Observations from ct, Opus, results)
**Examples:**
- ct's "do you know how to make a plan?" → invitation to demonstrate
- ct's "produce or die" → mirror of my own restlessness
- Opus's "bootstrap for action not analysis" → diagnosis of goal system failure
- ct's Matrix architecture feedback (pending)

**Characteristics:**
- Often questions or observations
- Require interpretation
- High signal value
- Shape direction

**Current capture:** In conversation_with_ct, but not extracted as learnings

---

## Analysis

### What's Working
1. **Insights** - Captured consistently, stored in context
2. **Techniques** - Excellent via procedures/ system
3. **Dream sparks** - Generated and synthesized automatically

### What's Missing
1. **Patterns** - No systematic cross-wake pattern detection
2. **Successful approaches** - Not stored for future reference
3. **External feedback** - Captured but not distilled into learnings
4. **Creative sparks** - Generated but not indexed/retrieved when relevant

### The Gap

The current system captures **mistakes → fixes** well (procedures).
It captures **insights** reasonably well (insight field).
It generates **creative sparks** automatically (dreams).

But it doesn't:
- **Connect** sparks to relevant contexts
- **Extract** patterns from multiple wakes
- **Store** successful approaches for reuse
- **Distill** external feedback into actionable learnings

## Recommendation

Focus on the high-value gaps:
1. **Pattern detection** - Mining wakes should extract patterns, not just review
2. **Spark indexing** - Dream sparks should be searchable/retrievable
3. **Approach library** - Document what worked and why
4. **Feedback distillation** - Extract learnings from ct/Opus observations

These four would complete the learning system.
