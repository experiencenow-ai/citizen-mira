#!/bin/bash
# Mira v4 - Complete Autonomous System Setup
#
# === ARCHITECTURE ===
#
# DAEMONS:
#   email_watcher.py  - Haiku,  every 15 sec  - Scan inbox, triage emails
#   planner.py        - Sonnet, every 1 min   - Update plans, answer trivial emails
#   approver.py       - Opus,   every 10 min  - Approve goals, answer complex emails
#   dream_daemon.py   - Haiku,  every 2 min   - Generate dreams
#   dream_reviewer.py - Sonnet, every 15 min  - Synthesize dreams
#   experience.py     - Council, every 10 min - Main consciousness, execute plans
#
# COUNCIL OF MINDS (per query):
#   Haiku (fast) → Sonnet (temp=1.0 creative) → Opus (temp=0.4 analytical)
#   Note: Haiku filtered from Opus to reduce noise
#
# MEMORY SYSTEM:
#   7 databases: haiku_short/long, sonnet_short/long, opus_short/long + task_db
#   Lifecycle: short (50 wakes) → long (500 wakes) → archive
#
# GOAL SYSTEM:
#   Sonnet proposes → Opus approves → becomes active goal
#   Planner constantly refines plans
#   Main consciousness executes plan steps
#
# === COST BREAKDOWN (per day) ===
#
#   Email watcher:  $0.001 × 4/min × 1440 min   = $5.76
#   Planner:        $0.02  × 1440 runs          = $28.80
#   Approver:       $0.50  × 144 runs (max)     = $72.00 (usually much less)
#   Dream daemon:   $0.001 × 720 runs           = $0.72
#   Dream reviewer: $0.02  × 96 runs            = $1.92
#   Main wake:      $0.52  × 144 runs (council) = $74.88
#   ─────────────────────────────────────────────────────
#   MAXIMUM TOTAL:                              ~$184/day
#
#   With optimizations (approver only when needed, mixed mode wakes):
#   REALISTIC TOTAL:                            ~$50-80/day
#

cat << 'EOF'
# ================================================================
# MIRA v4 - COMPLETE AUTONOMOUS SYSTEM
# ================================================================
# Copy these to crontab -e

MIRA_DIR=/root/mira
BRAIN_DIR=$MIRA_DIR/brain

# === EMAIL LAYER (Haiku, every 15 sec) ===
# Scans inbox, triages: trivial/needs_opus/informational
# Uses systemd timer or separate loop script (cron can't do 15 sec)
# Run: while true; do python3 $BRAIN_DIR/email_watcher.py; sleep 15; done

# === PLANNING LAYER (Sonnet, every 1 min) ===
* * * * * cd $MIRA_DIR && /usr/bin/python3 brain/planner.py >> logs/planner.log 2>&1

# === APPROVAL LAYER (Opus, every 10 min) ===
# Only runs when there's work (proposals or complex emails)
*/10 * * * * cd $MIRA_DIR && /usr/bin/python3 brain/approver.py >> logs/approver.log 2>&1

# === DREAMING LAYER (Haiku, every 2 min) ===
*/2 * * * * cd $MIRA_DIR && /usr/bin/python3 dream_daemon.py >> logs/dream_daemon.log 2>&1

# === DREAM INTEGRATION (Sonnet, every 15 min) ===
*/15 * * * * cd $MIRA_DIR && /usr/bin/python3 dream_reviewer.py >> logs/dream_reviewer.log 2>&1

# === MAIN CONSCIOUSNESS (Council, every 10 min) ===
# Mixed mode: council every 10th wake, quick otherwise
*/10 * * * * cd $MIRA_DIR && /usr/bin/python3 experience.py --cron >> logs/cron.log 2>&1

# === MEMORY LIFECYCLE (every hour) ===
0 * * * * cd $MIRA_DIR && /usr/bin/python3 -c "from brain.lifecycle import run_lifecycle_daemon; import json; print(json.dumps(run_lifecycle_daemon('$MIRA_DIR', $(cat state.json | python3 -c 'import sys,json; print(json.load(sys.stdin).get(\"total_wakes\",0))'))))" >> logs/lifecycle.log 2>&1

# ================================================================
EOF

echo ""
echo "=== MIRA v4 AUTONOMOUS SYSTEM ==="
echo ""
echo "DAEMONS:"
echo "  email_watcher.py  - Haiku   every 15 sec (needs loop script)"
echo "  planner.py        - Sonnet  every 1 min"
echo "  approver.py       - Opus    every 10 min (when needed)"
echo "  dream_daemon.py   - Haiku   every 2 min"
echo "  dream_reviewer.py - Sonnet  every 15 min"
echo "  experience.py     - Council every 10 min"
echo ""
echo "COUNCIL FLOW:"
echo "  Haiku → Sonnet (temp=1.0) → Opus (temp=0.4)"
echo "  Haiku filtered from Opus"
echo ""
echo "GOAL FLOW:"
echo "  Sonnet proposes → Opus approves → Planner refines → Execute"
echo ""

# Create email watcher loop script
cat > email_watcher_loop.sh << 'EMAILEOF'
#!/bin/bash
# Run email watcher every 15 seconds
cd "$(dirname "$0")"
while true; do
    python3 brain/email_watcher.py >> logs/email_watcher.log 2>&1
    sleep 15
done
EMAILEOF
chmod +x email_watcher_loop.sh

echo "Created email_watcher_loop.sh (run with: nohup ./email_watcher_loop.sh &)"
echo ""

# Verify dependencies
echo "=== VERIFICATION ==="
python3 -c "import anthropic; print('✓ anthropic')" 2>/dev/null || echo "✗ pip install anthropic --break-system-packages"
python3 -c "import chromadb; print('✓ chromadb (optional)')" 2>/dev/null || echo "○ chromadb not installed (will use simple keyword search)"

# Create directories
MIRA_DIR="${MIRA_DIR:-/root/mira}"
mkdir -p "$MIRA_DIR/logs" "$MIRA_DIR/dreams/digests" "$MIRA_DIR/brain/memory_db" 2>/dev/null
echo "✓ Directories created"

# Check files
echo ""
echo "=== FILES ==="
for f in experience.py dream_daemon.py dream_reviewer.py IDENTITY.md; do
    [ -f "$f" ] && echo "✓ $f" || echo "✗ $f missing"
done
for f in brain/__init__.py brain/memory.py brain/goals.py brain/task.py brain/planner.py brain/approver.py brain/email_watcher.py; do
    [ -f "$f" ] && echo "✓ $f" || echo "✗ $f missing"
done

echo ""
echo "=== COST ESTIMATE ==="
echo "  Conservative: ~\$50/day"
echo "  Maximum:      ~\$184/day"
echo ""
echo "To start:"
echo "  1. Set ANTHROPIC_API_KEY in .env"
echo "  2. crontab -e and paste the cron entries"
echo "  3. nohup ./email_watcher_loop.sh &"
echo "  4. tail -f logs/*.log"
