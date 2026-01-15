# Mira v4 System Audit

## Connection Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW DIAGRAM                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                           ┌──────────────────┐
                           │   EMAIL INBOX    │
                           │   (IMAP server)  │
                           └────────┬─────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  EMAIL WATCHER (Haiku, every 15 sec)                                         │
│  brain/email_watcher.py                                                      │
│                                                                              │
│  READS:  IMAP inbox via email_utils.py                                       │
│  WRITES: brain/email_inbox.json (triaged emails)                            │
│          brain/email_processed.json (seen IDs)                              │
│          haiku_short memory (email summaries)                               │
│                                                                              │
│  OUTPUT: {"emails": [...], "last_check": "..."}                             │
│          Each email has: id, from, subject, body, triage                    │
│          Triage: {classification, summary, urgency, suggested_response}     │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
┌────────────────────────────┐    ┌────────────────────────────────────────────┐
│  PLANNER                   │    │  APPROVER                                  │
│  (Sonnet, every 1 min)     │    │  (Opus, every 10 min)                      │
│  brain/planner.py          │    │  brain/approver.py                         │
│                            │    │                                            │
│  READS:                    │    │  READS:                                    │
│    brain/goals.json        │    │    brain/goals.json                        │
│    brain/plans.json        │    │    brain/proposed_goals.json               │
│    brain/email_inbox.json  │    │    brain/email_inbox.json                  │
│    state.json              │    │    state.json                              │
│                            │    │    IDENTITY.md                             │
│  WRITES:                   │    │                                            │
│    brain/plans.json        │    │  WRITES:                                   │
│    brain/proposed_goals.json│   │    brain/goals.json                        │
│    brain/email_inbox.json  │    │    brain/proposed_goals.json               │
│    sonnet_short memory     │    │    brain/email_inbox.json                  │
│                            │    │    opus_short memory                       │
│  ACTIONS:                  │    │                                            │
│    - Updates plans         │    │  ACTIONS:                                  │
│    - Proposes goals        │    │    - Approves/rejects proposals            │
│    - Answers trivial emails│    │    - Creates goals directly                │
│                            │    │    - Answers complex emails                │
└────────────────────────────┘    └────────────────────────────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        brain/goals.json                                      │
│  {                                                                           │
│    "goals": [{id, description, why, success_criteria, priority, status}],   │
│    "archived": [...]                                                        │
│  }                                                                           │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  MAIN CONSCIOUSNESS (Council, every 10 min)                                  │
│  experience.py                                                               │
│                                                                              │
│  READS:                                                                      │
│    IDENTITY.md                                                              │
│    facts.json                                                               │
│    state.json                                                               │
│    dream_digest.json                                                        │
│    brain/news_digest.json                                                   │
│    brain/goals.json, plans.json, schedule.json                              │
│    task_db.json                                                             │
│    {haiku,sonnet,opus}_{short,long} memories                                │
│                                                                              │
│  WRITES:                                                                     │
│    state.json                                                               │
│    logs/experience_YYYY-MM-DD.jsonl                                         │
│    task_db.json                                                             │
│    {haiku,sonnet,opus}_short memories                                       │
│                                                                              │
│  COUNCIL FLOW:                                                               │
│    1. HAIKU (temp 0.7) + haiku_short/long memories                          │
│       → Response feeds to Sonnet                                             │
│    2. SONNET (temp 1.0) + sonnet_short/long memories + Haiku response       │
│       → Creative response feeds to Opus                                      │
│    3. OPUS (temp 0.4) + opus_short/long memories + Sonnet response          │
│       → FINAL DECISION (Haiku filtered out)                                  │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│  DREAM DAEMON (Haiku, every 2 min)                                           │
│  dream_daemon.py                                                             │
│                                                                              │
│  READS:  state.json, dreams/recent.json                                     │
│  WRITES: dreams/{timestamp}.json, dreams/recent.json                        │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  DREAM REVIEWER (Sonnet, every 15 min)                                       │
│  dream_reviewer.py                                                           │
│                                                                              │
│  READS:  dreams/*.json (last 20 min)                                        │
│  WRITES: dream_digest.json, dreams/digests/{timestamp}.json                 │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│  NEWS SCANNER (Haiku+Sonnet, every 4 hours)                                  │
│  news_scanner.py                                                             │
│                                                                              │
│  FLOW:                                                                       │
│    1. Fetch RSS feeds                                                        │
│    2. HAIKU filters: Is this actually NEW?                                  │
│    3. SONNET summarizes new items                                           │
│    4. Store to ALL model memories                                           │
│                                                                              │
│  READS:  brain/news_seen.json (dedup hashes)                                │
│  WRITES: brain/news_digest.json                                             │
│          brain/news_seen.json                                               │
│          {haiku,sonnet,opus}_short memories (news items)                    │
└──────────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────────────┐
│  MEMORY LIFECYCLE (hourly)                                                   │
│  brain/lifecycle.py                                                          │
│                                                                              │
│  For each model (haiku, sonnet, opus):                                      │
│    SHORT-TERM (max 5000 per model):                                         │
│      - Purge if not accessed in 50 wakes OR capacity full (oldest first)   │
│      - Promote to long-term if 60+ wakes AND 3+ accesses                    │
│    LONG-TERM (max 100000 per model):                                        │
│      - Archive if not accessed in 500 wakes OR capacity full (oldest first)│
│    ARCHIVE: Append-only, grep to search                                     │
│                                                                              │
│  WRITES: brain/memory_db/lifecycle.log, brain/memory_db/archive.jsonl      │
└──────────────────────────────────────────────────────────────────────────────┘
```

## File Layout

```
/root/mira/
├── experience.py           # Main consciousness
├── dream_daemon.py         # Dream generation
├── dream_reviewer.py       # Dream synthesis
├── news_scanner.py         # News pipeline
├── email_watcher_loop.sh   # Email loop script
├── crontab.txt            # Cron configuration
├── .env                   # API key
├── state.json             # Wake state
├── dream_digest.json      # Synthesized dreams
├── IDENTITY.md            # Core identity
├── facts.json             # Structured facts
├── logs/                  # All log files
├── dreams/                # Raw dream files
│   ├── *.json
│   └── digests/
└── brain/
    ├── __init__.py
    ├── memory.py          # 6-DB memory system
    ├── lifecycle.py       # Memory GC
    ├── task.py            # Working memory
    ├── goals.py           # Goals/plans
    ├── planner.py         # Planning daemon
    ├── approver.py        # Approval daemon
    ├── email_watcher.py   # Email triage
    ├── creative_index.py  # Sonnet combinations
    ├── goals.json         # Active goals
    ├── proposed_goals.json
    ├── plans.json
    ├── schedule.json
    ├── email_inbox.json
    ├── email_processed.json
    ├── news_digest.json
    ├── news_seen.json
    ├── task_db.json       # Working memory
    └── memory_db/
        ├── haiku_short/
        ├── haiku_long/
        ├── sonnet_short/
        ├── sonnet_long/
        ├── opus_short/
        ├── opus_long/
        └── archive/
```

## File Checklist

| File | Purpose | Reads | Writes |
|------|---------|-------|--------|
| experience.py | Main consciousness | *, memories | state.json, memories, logs |
| brain/email_watcher.py | Inbox triage | IMAP | email_inbox.json, haiku_short |
| brain/planner.py | Plan management | goals, plans, inbox | plans, proposals, sonnet_short |
| brain/approver.py | Goal approval | proposals, inbox | goals, opus_short |
| brain/goals.py | Goal/plan CRUD | goals.json, plans.json | goals.json, plans.json |
| brain/task.py | Working memory | task_db.json | task_db.json |
| brain/memory.py | 6 semantic DBs | memory_db/* | memory_db/* |
| brain/lifecycle.py | Memory GC | memory_db/* | memory_db/*, archive |
| news_scanner.py | News pipeline | RSS, news_seen | news_digest, all memories |
| dream_daemon.py | Dream generation | state, recent dreams | dreams/*.json |
| dream_reviewer.py | Dream synthesis | dreams/*.json | dream_digest.json |

## Expected Behavior

### On Each Wake (every 10 min):

1. **Load Context:**
   - IDENTITY.md → Who am I?
   - goals.json + plans.json → What am I working on?
   - task_db.json → Immediate working memory
   - dream_digest.json → Creative fuel
   - news_digest.json → World awareness
   - state.json → Recent thoughts, mood

2. **Query Model Memories:**
   - Extract query hint from ct_message or current task
   - Search haiku_short + haiku_long → inject into Haiku prompt
   - Search sonnet_short + sonnet_long → inject into Sonnet prompt
   - Search opus_short + opus_long → inject into Opus prompt

3. **Council Processing:**
   ```
   HAIKU (temp 0.7):
     Context: Base + haiku memories
     Output: Quick take on query
     Stored to: haiku_short
   
   SONNET (temp 1.0):
     Context: Base + Haiku output + sonnet memories
     Output: Creative proposals
     Stored to: sonnet_short (with combinations)
   
   OPUS (temp 0.4):
     Context: Base + Sonnet output + opus memories
     NOTE: Haiku FILTERED (reduces noise)
     Output: Final decision
     Stored to: opus_short
   ```

4. **Execute:**
   - If active plan → execute next step
   - If recurring tasks due → do them
   - Update task_db, goals progress
   - Log to experience log

### Background Daemons:

| Daemon | Frequency | Purpose |
|--------|-----------|---------|
| email_watcher | 15 sec | Triage inbox → haiku memory |
| planner | 1 min | Refine plans → sonnet memory |
| approver | 10 min | Approve goals → opus memory |
| dream_daemon | 2 min | Generate dreams |
| dream_reviewer | 15 min | Synthesize dreams |
| news_scanner | 4 hours | News → all memories |
| lifecycle | 1 hour | Purge/promote/archive |

### Key Invariants:

1. **Each model has its own memory view** - different DBs, different retrieval
2. **News only processed once** - hash dedup, then stored to all memories
3. **Goals flow: Sonnet proposes → Opus approves**
4. **Plans constantly refined** by planner daemon
5. **Wake prompt shows exactly what to do** - no "what should I do?"
6. **Haiku filtered from Opus** - only Sonnet's creative output matters

## Cost Breakdown (Daily)

| Component | Model | Frequency | Per Run | Daily |
|-----------|-------|-----------|---------|-------|
| Email watcher | Haiku | 4/min | $0.001 | $5.76 |
| Planner | Sonnet | 1/min | $0.02 | $28.80 |
| Approver | Opus | 6/hour (when needed) | $0.50 | $10-72 |
| Dream daemon | Haiku | 0.5/min | $0.001 | $0.72 |
| Dream reviewer | Sonnet | 4/hour | $0.02 | $1.92 |
| News scanner | Haiku+Sonnet | 6/day | $0.01 | $0.06 |
| Main wake | Council | 6/hour | $0.52 | $74.88 |
| **TOTAL** | | | | **$55-185** |

Conservative (approver only when needed, mixed wakes): ~$55/day
Maximum (all council, constant approval): ~$185/day

## Verification Commands

```bash
# Check all files exist
ls -la experience.py dream_daemon.py dream_reviewer.py news_scanner.py
ls -la brain/*.py

# Check crontab installed
crontab -l

# Check daemons running
pgrep -f email_watcher_loop
pgrep -f planner.py

# Check logs
tail -f logs/*.log

# Check memory DBs
ls -la brain/memory_db/

# Check goals/plans
cat brain/goals.json
cat brain/plans.json

# Check news digest
cat brain/news_digest.json
```
