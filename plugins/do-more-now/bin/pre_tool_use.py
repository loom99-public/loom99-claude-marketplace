#!/usr/bin/env python3
"""
PreToolUse Hook Handler

Tracks sequence numbers for Task tool invocations (subagent calls).
"""

import sys
import json
import os
import fcntl
from datetime import datetime
from pathlib import Path


def log_error(hook_name, error):
    """Log errors to hook_errors.log without blocking execution."""
    try:
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
        exec_dir = Path(project_dir) / '.agent_planning' / '.exec'
        exec_dir.mkdir(parents=True, exist_ok=True)

        log_path = exec_dir / 'hook_errors.log'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(log_path, 'a') as f:
            f.write(f"[{timestamp}] [{hook_name}] ERROR: {error}\n")
            import traceback
            f.write(traceback.format_exc())
            f.write("\n")
    except Exception:
        pass


def main():
    """Track sequence number for Task tool invocations."""
    try:
        # Read stdin to get tool information
        stdin_data = sys.stdin.read()

        if not stdin_data:
            sys.exit(0)

        # Parse JSON input
        try:
            data = json.loads(stdin_data)
        except (json.JSONDecodeError, ValueError):
            # Can't parse - exit silently
            sys.exit(0)

        # Check if tool is "Task" (case-sensitive match as per spec)
        tool_name = data.get('tool') or data.get('tool_name') or data.get('name')
        if tool_name != 'Task':
            # Not a Task invocation - exit silently
            sys.exit(0)

        # Use CLAUDE_PROJECT_DIR if available
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
        exec_dir = Path(project_dir) / '.agent_planning' / '.exec'

        # Check if execution is in progress
        execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
        if not execution_id_file.exists():
            # No execution in progress - exit silently
            sys.exit(0)

        # Increment sequence number with file locking for atomicity
        sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'

        # Create sequence file if it doesn't exist
        if not sequence_file.exists():
            sequence_file.write_text('0')

        # Atomic read-modify-write with file locking
        with open(sequence_file, 'r+') as f:
            # Lock file for exclusive access
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            except (OSError, AttributeError):
                # fcntl not available (Windows?) - proceed without locking
                pass

            try:
                current_sequence = int(f.read().strip() or '0')
            except ValueError:
                current_sequence = 0

            # Increment sequence
            new_sequence = current_sequence + 1

            # Write back to file
            f.seek(0)
            f.truncate()
            f.write(str(new_sequence))

            # Unlock file
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except (OSError, AttributeError):
                pass

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('pre_tool_use', e)
        sys.exit(0)


if __name__ == '__main__':
    main()
