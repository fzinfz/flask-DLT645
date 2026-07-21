#!/usr/bin/env bash
set -euo pipefail

# Project root = parent directory of this script (scripts/..)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

CRON_CMD="cd $PROJECT_DIR && uv run lib/influxdb2.py --push"
CRON_LINE="0 9 * * * $CRON_CMD"

# Skip if the job is already set up in the current user's crontab
if crontab -l 2>/dev/null | grep -Fq "$CRON_CMD"; then
    echo "Cron job already set up, skipping."
    exit 0
fi

# Append the job to the crontab
( crontab -l 2>/dev/null; echo "$CRON_LINE" ) | crontab -

echo "Cron job added: $CRON_LINE"
