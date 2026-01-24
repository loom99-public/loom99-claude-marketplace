#!/bin/bash
# Python hook runner
# Reads .do-hooks-py (or $DO_HOOKS_PY_PATH) containing python script commands.
# Each command receives hook JSON on stdin via the auto-detected python runner.
#
# File format:
#   - One command per logical line (script name + optional args)
#   - Continuation lines (indented with spaces/tabs) are space-joined
#   - Blank lines and lines starting with # are skipped
#
# Script resolution order:
#   1. $DO_HOOKS_PY_SCRIPTS_PATH (if set)
#   2. Plugin scripts dir (where this file lives)
#   3. ~/.claude/scripts
#
# Exits 0 gracefully in all error scenarios.

LOG_DIR="/tmp/do_plugin"
LOG_FILE="$LOG_DIR/py-shim.log"
INPUT_LOG_FILE="${LOG_DIR}/hooks_input.jsonl"

log_msg() {
    [ -n "$DO_PLUGIN_DEBUG" ] && mkdir -p "$LOG_DIR" && echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_input() {
    mkdir -p "$LOG_DIR" && echo "$1" >> "$INPUT_LOG_FILE"
}

# Read stdin into variable (hooks receive JSON via stdin)
INPUT=$(cat)

log_input "${INPUT}"

# Detect python runner: prefer uv, then python3, then python
# Each candidate is verified to actually work before committing
PYTHON_CMD=""
for candidate in "uv run python" "python3" "python"; do
    if $candidate --version >/dev/null 2>&1; then
        PYTHON_CMD="$candidate"
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    log_msg "WARN: no working python found (tried uv, python3, python)"
    exit 0
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
log_msg "Using $PYTHON_CMD ($PYTHON_VERSION)"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Commands file: env var override or default to .do-hooks-py in script dir
HOOKS_FILE="${DO_HOOKS_PY_PATH:-$SCRIPT_DIR/.do-hooks-py}"

if [ ! -f "$HOOKS_FILE" ]; then
    log_msg "No hooks file found at $HOOKS_FILE"
    exit 0
fi

log_msg "Reading hooks from $HOOKS_FILE"

export DO_PLUGIN_DEBUG

# Resolve a script name to a full path
# Search order: $DO_HOOKS_PY_SCRIPTS_PATH, script dir, ~/.claude/scripts
resolve_script() {
    local name="$1"
    if [ -n "$DO_HOOKS_PY_SCRIPTS_PATH" ] && [ -f "$DO_HOOKS_PY_SCRIPTS_PATH/$name" ]; then
        echo "$DO_HOOKS_PY_SCRIPTS_PATH/$name"
    elif [ -f "$SCRIPT_DIR/$name" ]; then
        echo "$SCRIPT_DIR/$name"
    elif [ -f "$HOME/.claude/scripts/$name" ]; then
        echo "$HOME/.claude/scripts/$name"
    else
        return 1
    fi
}

# Parse the hooks file: join continuation lines (indented) with the previous line
COMMANDS=()
current=""
while IFS= read -r line || [ -n "$line" ]; do
    # Detect continuation: line starts with space or tab
    if [[ "$line" =~ ^[[:space:]] ]] && [ -n "$current" ]; then
        # Strip leading whitespace and append
        trimmed="${line#"${line%%[! ]*}"}"
        current="$current $trimmed"
    else
        # Flush previous command
        if [ -n "$current" ]; then
            COMMANDS+=("$current")
        fi
        # Strip leading whitespace for new line
        current="${line#"${line%%[! ]*}"}"
    fi
done < "$HOOKS_FILE"
# Flush final command
[ -n "$current" ] && COMMANDS+=("$current")

# Execute each command
LAST_OUTPUT=""
for cmd in "${COMMANDS[@]}"; do
    # Skip blank and comment lines
    [ -z "$cmd" ] && continue
    [ "${cmd:0:1}" = "#" ] && continue

    # Parse command into tokens using Python's shlex (safe, no execution)
    PARSED=$($PYTHON_CMD -c "
import shlex, sys
try:
    tokens = shlex.split(sys.argv[1])
    print('\0'.join(tokens))
except ValueError as e:
    print('SHLEX_ERROR: ' + str(e), file=sys.stderr)
    sys.exit(1)
" "$cmd" 2>&1)

    if [ $? -ne 0 ]; then
        log_msg "WARN: failed to parse command: $cmd ($PARSED)"
        continue
    fi

    # Read null-delimited tokens into array
    IFS=$'\0' read -r -a TOKENS <<< "$PARSED"

    if [ ${#TOKENS[@]} -eq 0 ]; then
        log_msg "WARN: empty command after parsing: $cmd"
        continue
    fi

    script_name="${TOKENS[0]}"
    ARGS=("${TOKENS[@]:1}")

    SCRIPT_PATH=$(resolve_script "$script_name")
    if [ -z "$SCRIPT_PATH" ]; then
        log_msg "WARN: script not found: $script_name"
        continue
    fi

    # Set PYTHONPATH to the resolved script's directory so it can import siblings
    export PYTHONPATH="$(dirname "$SCRIPT_PATH"):${PYTHONPATH:-}"

    log_msg "Running: $PYTHON_CMD -B $SCRIPT_PATH ${ARGS[*]}"

    # In dev mode, log file hash to verify which version is running
    if [ -n "$DO_PLUGIN_DEBUG" ]; then
        SCRIPT_HASH=$(md5 -q "$SCRIPT_PATH" 2>/dev/null || md5sum "$SCRIPT_PATH" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
        log_msg "Script hash: $SCRIPT_HASH (mtime: $(stat -f%m "$SCRIPT_PATH" 2>/dev/null || stat -c%Y "$SCRIPT_PATH" 2>/dev/null || echo unknown))"
    fi

    # -B disables .pyc bytecode caching, ensuring fresh code on every run
    OUTPUT=$(echo "$INPUT" | $PYTHON_CMD -B "$SCRIPT_PATH" "${ARGS[@]}")
    EXIT_CODE=$?

    log_msg "Script output: $OUTPUT"
    log_msg "Exit code: $EXIT_CODE"

    if [ $EXIT_CODE -ne 0 ]; then
        log_msg "WARN: $script_name exited with $EXIT_CODE, continuing"
    fi

    [ -n "$OUTPUT" ] && LAST_OUTPUT="$OUTPUT"
done

echo "$LAST_OUTPUT"
exit 0
