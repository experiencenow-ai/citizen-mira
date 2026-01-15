#!/bin/bash
# Email watcher loop - runs every 15 seconds
# Start with: nohup ./email_watcher_loop.sh &
# Or let cron restart it if it dies

cd "$(dirname "$0")"

echo "[$(date)] Email watcher loop starting"

while true; do
    python3 brain/email_watcher.py 2>&1
    sleep 15
done
