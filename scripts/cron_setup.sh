#!/usr/bin/env bash
set -euo pipefail

# Project root = parent directory of this script (scripts/..)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# cron runs with a minimal PATH and /bin/sh (dash):
#  - resolve uv to an absolute path (e.g. /root/.local/bin/uv is not in cron's PATH)
#  - use POSIX redirection (>> file 2>&1), dash does not support bash's &>
UV_BIN="$(command -v uv || true)"
if [[ -z "$UV_BIN" ]]; then
    echo "Error: uv not found in PATH" >&2
    exit 1
fi

LOG_FILE="/tmp/cron_influxdb2.log"
CRON_CMD="cd $PROJECT_DIR && { date; $UV_BIN run lib/influxdb2.py --push; } >$LOG_FILE 2>&1"
CRON_LINE="0 6 * * * $CRON_CMD"

# Skip if the job is already up to date in the current user's crontab
if crontab -l 2>/dev/null | grep -Fq "$CRON_CMD"; then
    echo "Cron job already set up, skipping."
    exit 0
fi

# Remove stale entries for this job, then append the new one
( crontab -l 2>/dev/null | grep -Fv "lib/influxdb2.py --push" || true; echo "$CRON_LINE" ) | crontab -

echo "Cron job added: $CRON_LINE"
