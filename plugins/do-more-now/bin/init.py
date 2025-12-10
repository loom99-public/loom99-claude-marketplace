#!/usr/bin/env python3
"""
Initialize do-more-now plugin environment.
Called by SessionStart hook.

No external dependencies - uses only Python 3 standard library.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(".agent_planning/do-command-logs")


def get_log_file(session_id: str) -> Path:
    """Get log file path for this session."""
    return BASE_DIR / f"{session_id}-DEBUG.log"


def log(log_file: Path, msg: str):
    """Append timestamped message to log file."""
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a") as f:
            f.write(f"{datetime.now().isoformat()} {msg}\n")
    except Exception:
        pass


def main():
    # Read and parse hook input
    stdin_data = sys.stdin.read()

    try:
        hook_input = json.loads(stdin_data) if stdin_data.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    session_id = hook_input.get("session_id", "unknown")
    log_file = get_log_file(session_id)

    # Log startup
    log(log_file, "=" * 60)
    log(log_file, "init.py: SESSION START")
    log(log_file, f"init.py: session_id={session_id}")
    log(log_file, f"init.py: cwd={os.getcwd()}")
    log(log_file, f"init.py: hook_input keys={list(hook_input.keys())}")

    # Log relevant hook input fields
    for key in ["hook_event_name", "permission_mode", "transcript_path"]:
        if key in hook_input:
            log(log_file, f"init.py: {key}={hook_input[key]}")

    try:
        # Create required directories
        dirs = [
            BASE_DIR,
            BASE_DIR / "partials",
        ]

        for d in dirs:
            existed = d.exists()
            d.mkdir(parents=True, exist_ok=True)
            if existed:
                log(log_file, f"init.py: directory exists: {d}")
            else:
                log(log_file, f"init.py: created directory: {d}")

        log(log_file, "init.py: initialization complete")

    except Exception as e:
        log(log_file, f"init.py: ERROR - {type(e).__name__}: {e}")
        import traceback
        log(log_file, f"init.py: traceback:\n{traceback.format_exc()}")


if __name__ == "__main__":
    main()
