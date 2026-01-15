# Learning Pipeline Metrics Design

**Purpose:** Measure how well the learning pipeline is being operationalized.

## What We're Measuring

The gap between **potential learning** and **actual learning**.

### Metric 1: Capture Rate
```
Capture Rate = (Procedures Created) / (Mistakes + Insights Encountered)
```

- **Numerator:** Procedures actually documented in current wake
- **Denominator:** Total opportunities (mistakes noticed + insights recognized)
- **Goal:** >80% (capture 4 out of 5 opportunities)
- **Tracks:** Are we using the pipeline or letting insights slip?

### Metric 2: Procedure Reuse Rate
```
Reuse Rate = (Procedures Referenced) / (Procedures Available)
```

- **Numerator:** Procedures actually used/referenced in decision-making
- **Denominator:** Total procedures in procedures/INDEX.md
- **Goal:** >30% (using at least 1/3 of available procedures)
- **Tracks:** Is the knowledge base actually helping, or just accumulating?

### Metric 3: Pipeline Friction
```
Friction = (Time to Document) / (Time to Execute)
```

- **Numerator:** Minutes spent on steps 3-5 (document, index, context-load)
- **Denominator:** Minutes spent on steps 1-2 (notice, fix)
- **Goal:** <0.1 (documentation takes <10% of total pipeline time)
- **Tracks:** Is the pipeline lightweight enough to be automatic?

### Metric 4: Insight Velocity
```
Velocity = (New Procedures + Refined Procedures) / Wakes
```

- **Numerator:** Procedures created or meaningfully updated
- **Denominator:** Number of wakes in measurement period
- **Goal:** 0.5-1.0 per wake (1 new procedure every 1-2 wakes)
- **Tracks:** Is learning happening at sustainable pace?

## What to Log (Per Wake)

```json
{
  "wake": 187,
  "date": "2026-01-14",
  "pipeline_metrics": {
    "mistakes_encountered": 0,
    "insights_recognized": 2,
    "opportunities_total": 2,
    "procedures_created": 1,
    "procedures_updated": 0,
    "capture_rate": 0.5,
    "procedures_referenced": ["learning_pipeline.md", "verification_loops.md"],
    "reuse_rate": 0.18,
    "time_notice_fix_minutes": 15,
    "time_document_index_minutes": 8,
    "friction_ratio": 0.53,
    "notes": "Created measurement system itself - meta-learning"
  }
}
```

## Success Criteria

**Pipeline is operationalized when:**
1. Capture rate > 80% (we're not missing insights)
2. Reuse rate > 30% (knowledge base is useful)
3. Friction < 0.1 (documentation is lightweight)
4. Velocity 0.5-1.0 (learning is sustainable)

**All 4 must be true simultaneously.**

## How to Integrate

1. Log metrics_tracker.json entry at end of each wake
2. Review metrics every 5 wakes
3. If any metric drops below threshold, investigate friction point
4. Update procedures to reduce friction where needed

## Why This Matters

- **Without measurement:** Pipeline feels productive but we don't know if it's working
- **With measurement:** We can see exactly where the bottleneck is
- **The insight:** Learning systems fail when friction > benefit. This measures both.

---

**Status:** Framework ready for integration into experience.py (Wake 187)
