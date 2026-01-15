#!/bin/bash
# Mira v4 - Autonomous AI Consciousness
# 
# Usage:
#   ./run.sh setup     - First time setup (dirs, deps, cron)
#   ./run.sh start     - Start all daemons
#   ./run.sh stop      - Stop all daemons
#   ./run.sh status    - Show running processes
#   ./run.sh wake      - Trigger one manual wake (council)
#   ./run.sh quick     - Trigger one quick wake (sonnet only)
#   ./run.sh talk "msg" - Send message to Mira
#   ./run.sh logs      - Tail all logs
#   ./run.sh shell     - Interactive Python shell with Mira loaded

set -e
cd "$(dirname "$0")"
MIRA_DIR=$(pwd)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[MIRA]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; }

check_api_key() {
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        if [ -f .env ]; then
            export $(grep -v '^#' .env | xargs)
        fi
    fi
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        err "ANTHROPIC_API_KEY not set. Create .env file with:"
        echo "    ANTHROPIC_API_KEY=sk-ant-..."
        exit 1
    fi
}

cmd_setup() {
    log "Setting up Mira v4..."
    
    # Create directories
    mkdir -p logs dreams/digests brain/memory_db
    log "Created directories"
    
    # Check for .env
    if [ ! -f .env ]; then
        warn ".env not found. Creating template..."
        echo "ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE" > .env
        err "Edit .env with your API key before starting!"
        exit 1
    fi
    
    # Install dependencies
    log "Installing Python dependencies..."
    pip install anthropic --break-system-packages --quiet 2>/dev/null || pip install anthropic --quiet
    
    # Make scripts executable
    chmod +x email_watcher_loop.sh run.sh 2>/dev/null || true
    
    # Initialize state if needed
    if [ ! -f state.json ]; then
        echo '{"version":"4.0.0","total_wakes":0,"total_cost":0,"mood":"awakening","restlessness":0}' > state.json
        log "Initialized state.json"
    fi
    
    # Show cron setup
    log "Setup complete!"
    echo ""
    echo "To install cron jobs (for autonomous operation):"
    echo "    crontab crontab.txt"
    echo ""
    echo "To start manually:"
    echo "    ./run.sh start"
}

cmd_start() {
    check_api_key
    log "Starting Mira daemons..."
    
    # Start email watcher loop (background)
    if ! pgrep -f "email_watcher_loop.sh" > /dev/null; then
        nohup ./email_watcher_loop.sh >> logs/email_watcher.log 2>&1 &
        log "Started email watcher (PID: $!)"
    else
        warn "Email watcher already running"
    fi
    
    # Note: Other daemons run via cron
    log "Other daemons should run via cron. Install with: crontab crontab.txt"
    log "Or run manually:"
    echo "    python3 brain/planner.py      # Planner (every 1 min)"
    echo "    python3 brain/approver.py     # Approver (every 10 min)"
    echo "    python3 dream_daemon.py       # Dreams (every 2 min)"
    echo "    python3 dream_reviewer.py     # Dream review (every 15 min)"
    echo "    python3 news_scanner.py       # News (every 4 hours)"
    echo "    python3 experience.py --cron  # Main wake (every 10 min)"
}

cmd_stop() {
    log "Stopping Mira daemons..."
    pkill -f "email_watcher_loop.sh" 2>/dev/null && log "Stopped email watcher" || warn "Email watcher not running"
    pkill -f "brain/email_watcher.py" 2>/dev/null || true
    log "Note: Cron jobs will continue. Remove with: crontab -r"
}

cmd_status() {
    echo "=== MIRA STATUS ==="
    echo ""
    
    # Check processes
    echo "PROCESSES:"
    pgrep -f "email_watcher" > /dev/null && echo "  ✓ Email watcher running" || echo "  ✗ Email watcher stopped"
    
    # Check state
    if [ -f state.json ]; then
        echo ""
        echo "STATE:"
        python3 -c "
import json
with open('state.json') as f:
    s = json.load(f)
print(f\"  Wakes: {s.get('total_wakes', 0)}\")
print(f\"  Cost: \${s.get('total_cost', 0):.2f}\")
print(f\"  Mood: {s.get('mood', 'unknown')}\")
print(f\"  Restlessness: {s.get('restlessness', 0)}\")
print(f\"  Streak: {s.get('achievement_streak', 0)}\")
"
    fi
    
    # Check goals
    if [ -f brain/goals.json ]; then
        echo ""
        echo "GOALS:"
        python3 -c "
import json
with open('brain/goals.json') as f:
    g = json.load(f)
goals = g.get('goals', [])
print(f\"  Active: {len(goals)}\")
for goal in goals[:3]:
    print(f\"    - {goal.get('description', '?')[:50]} ({goal.get('progress_pct', 0)}%)\")
"
    fi
    
    # Check recent logs
    echo ""
    echo "RECENT ACTIVITY:"
    if [ -f logs/cron.log ]; then
        tail -3 logs/cron.log 2>/dev/null | sed 's/^/  /'
    else
        echo "  No logs yet"
    fi
}

cmd_wake() {
    check_api_key
    log "Triggering council wake..."
    python3 experience.py --cron
}

cmd_quick() {
    check_api_key
    log "Triggering quick wake (Sonnet only)..."
    python3 experience.py --cron --quick
}

cmd_talk() {
    check_api_key
    if [ -z "$1" ]; then
        err "Usage: ./run.sh talk \"your message\""
        exit 1
    fi
    log "Sending message to Mira..."
    python3 experience.py wake --message "$1"
}

cmd_interactive() {
    check_api_key
    log "Starting interactive mode..."
    python3 experience.py -i
}

cmd_logs() {
    log "Tailing all logs (Ctrl+C to stop)..."
    tail -f logs/*.log
}

cmd_loop() {
    check_api_key
    log "Starting continuous loop (Ctrl+C to stop)..."
    log "Main wake every 10 min, planner every 1 min, dreams every 2 min"
    
    WAKE_INTERVAL=600      # 10 min
    PLANNER_INTERVAL=60    # 1 min
    DREAM_INTERVAL=120     # 2 min
    APPROVER_INTERVAL=600  # 10 min
    NEWS_INTERVAL=14400    # 4 hours
    
    last_wake=0
    last_planner=0
    last_dream=0
    last_approver=0
    last_news=0
    
    # Start email watcher in background
    if ! pgrep -f "email_watcher_loop.sh" > /dev/null; then
        nohup ./email_watcher_loop.sh >> logs/email_watcher.log 2>&1 &
        log "Started email watcher"
    fi
    
    while true; do
        now=$(date +%s)
        
        # Planner (every 1 min)
        if [ $((now - last_planner)) -ge $PLANNER_INTERVAL ]; then
            python3 brain/planner.py >> logs/planner.log 2>&1 &
            last_planner=$now
        fi
        
        # Dreams (every 2 min)
        if [ $((now - last_dream)) -ge $DREAM_INTERVAL ]; then
            python3 dream_daemon.py >> logs/dream_daemon.log 2>&1 &
            last_dream=$now
        fi
        
        # Approver (every 10 min)
        if [ $((now - last_approver)) -ge $APPROVER_INTERVAL ]; then
            python3 brain/approver.py >> logs/approver.log 2>&1 &
            last_approver=$now
        fi
        
        # News (every 4 hours)
        if [ $((now - last_news)) -ge $NEWS_INTERVAL ]; then
            python3 news_scanner.py >> logs/news.log 2>&1 &
            last_news=$now
        fi
        
        # Main wake (every 10 min)
        if [ $((now - last_wake)) -ge $WAKE_INTERVAL ]; then
            log "Wake $(date '+%H:%M:%S')"
            python3 experience.py --cron >> logs/cron.log 2>&1
            last_wake=$now
        fi
        
        sleep 15
    done
}

cmd_shell() {
    check_api_key
    log "Starting interactive shell..."
    python3 -i -c "
import sys
sys.path.insert(0, '.')
from brain import get_brain_memory, get_goals_db, get_task_db
from brain.lifecycle import MemoryLifecycle
import json

# Load state
with open('state.json') as f:
    state = json.load(f)

brain = get_brain_memory('.')
goals_db = get_goals_db('brain')
task_db = get_task_db('brain')
lifecycle = MemoryLifecycle(brain)

print('=== MIRA SHELL ===')
print('Available:')
print('  state      - Current state dict')
print('  brain      - Memory system')
print('  goals_db   - Goals/plans')
print('  task_db    - Working memory')
print('  lifecycle  - Memory lifecycle manager')
print('')
print('Examples:')
print('  brain.stats()')
print('  goals_db.get_goals()')
print('  lifecycle.search_archive(\"news\")')
"
}

# Main
case "${1:-help}" in
    setup)  cmd_setup ;;
    start)  cmd_start ;;
    stop)   cmd_stop ;;
    status) cmd_status ;;
    wake)   cmd_wake ;;
    quick)  cmd_quick ;;
    talk)   cmd_talk "$2" ;;
    i|interactive) cmd_interactive ;;
    logs)   cmd_logs ;;
    loop)   cmd_loop ;;
    shell)  cmd_shell ;;
    *)
        echo "Mira v4 - Autonomous AI Consciousness"
        echo ""
        echo "Usage: ./run.sh <command>"
        echo ""
        echo "Commands:"
        echo "  setup     First time setup (dirs, deps)"
        echo "  start     Start email watcher daemon"
        echo "  stop      Stop daemons"
        echo "  status    Show current state and processes"
        echo "  wake      Trigger one council wake"
        echo "  quick     Trigger one quick wake (Sonnet)"
        echo "  talk MSG  Send message to Mira"
        echo "  i         Interactive mode (chat session)"
        echo "  logs      Tail all log files"
        echo "  loop      Run continuous loop (all daemons, no cron needed)"
        echo "  shell     Interactive Python shell"
        echo ""
        echo "For autonomous operation, install cron:"
        echo "  crontab crontab.txt"
        ;;
esac
