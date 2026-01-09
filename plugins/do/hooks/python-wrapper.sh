#!/bin/bash
# Generic Python wrapper for hooks
# Usage: python-wrapper.sh <script.py> [args...]
# Silently exits if python3 not available

LOG_DIR="/tmp/do_plugin"
LOG_FILE="$LOG_DIR/python-wrapper.log"

log_msg() {
    [ -n "$DO_PLUGIN_DEBUG" ] && mkdir -p "$LOG_DIR" && echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Read stdin into variable (hooks receive JSON via stdin)
INPUT=$(cat)

log_msg "Received input: $INPUT"

command -v python3 >/dev/null 2>&1 || { log_msg "WARN: python3 not found"; exit 0; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$1"
shift

[ -z "$SCRIPT" ] && { log_msg "ERROR: No script specified"; exit 0; }

log_msg "Running $SCRIPT"

# Set PYTHONPATH so scripts can import lib.py
export PYTHONPATH="$SCRIPT_DIR:${PYTHONPATH:-}"
export DO_PLUGIN_DEBUG

# -B disables .pyc bytecode caching, ensuring fresh code on every run
SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT"

# In dev mode, log file hash to verify which version is running
if [ -n "$DO_PLUGIN_DEBUG" ]; then
    SCRIPT_HASH=$(md5 -q "$SCRIPT_PATH" 2>/dev/null || md5sum "$SCRIPT_PATH" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
    log_msg "Script hash: $SCRIPT_HASH (mtime: $(stat -f%m "$SCRIPT_PATH" 2>/dev/null || stat -c%Y "$SCRIPT_PATH" 2>/dev/null || echo unknown))"
fi

OUTPUT=$(echo "$INPUT" | python3 -B "$SCRIPT_PATH" "$@")
EXIT_CODE=$?

log_msg "Script output: $OUTPUT"
log_msg "Exit code: $EXIT_CODE"

echo "$OUTPUT"
exit $EXIT_CODE
