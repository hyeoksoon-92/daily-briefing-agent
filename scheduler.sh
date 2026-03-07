#!/bin/bash
# scheduler.sh — Run once to set up a daily cron job for the briefing agent.
# Usage: ./scheduler.sh
# To remove: crontab -e (delete the daily-briefing-agent line)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$SCRIPT_DIR/.venv/bin/python"
LOG_FILE="$SCRIPT_DIR/briefings/cron.log"

if [[ ! -f "$PYTHON" ]]; then
    echo "ERROR: Virtual environment not found at $SCRIPT_DIR/.venv" >&2
    echo "Run: python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'" >&2
    exit 1
fi

if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
    echo "ERROR: ANTHROPIC_API_KEY environment variable is not set." >&2
    echo "Export it before running this script." >&2
    exit 1
fi

CRON_JOB="0 8 * * * cd $SCRIPT_DIR && ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY $PYTHON main.py >> $LOG_FILE 2>&1"
CRON_MARKER="daily-briefing-agent"

# Remove old entry if present, then add new one (idempotent)
(crontab -l 2>/dev/null | grep -v "$CRON_MARKER"; echo "# $CRON_MARKER"; echo "$CRON_JOB") | crontab -

echo "Cron job set: runs every day at 08:00."
echo "Log file: $LOG_FILE"
echo "To verify: crontab -l"
echo "To remove: crontab -e (delete the two lines marked $CRON_MARKER)"
