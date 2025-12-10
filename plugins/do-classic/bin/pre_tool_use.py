#!/usr/bin/env python3
"""
PreToolUse Hook Handler

Tracks sequence numbers for Task tool invocations (subagent calls).
"""

import sys
import json
import os
import fcntl
import time
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


def validate_project_dir():
    """
    Validate that project directory exists and is accessible.
    Returns (project_dir_path, error_message) tuple.
    """
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR')

    if not project_dir:
        project_dir = os.getcwd()

    project_path = Path(project_dir)

    if not project_path.exists():
        return None, f"Project directory does not exist: {project_dir}"

    if not project_path.is_dir():
        return None, f"Project path is not a directory: {project_dir}"

    return project_path, None


def increment_sequence_with_timeout(sequence_file, timeout_seconds=5):
    """
    Atomically increment sequence number with file locking and timeout.
    Returns (new_sequence, error_message) tuple.
    """
    # Create sequence file if it doesn't exist
    if not sequence_file.exists():
        try:
            sequence_file.write_text('0')
        except Exception as e:
            return None, f"Cannot create sequence file: {e}"

    start_time = time.time()
    lock_acquired = False

    try:
        # Atomic read-modify-write with file locking
        with open(sequence_file, 'r+') as f:
            # Try to acquire lock with timeout
            while time.time() - start_time < timeout_seconds:
                try:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock_acquired = True
                    break
                except (OSError, BlockingIOError):
                    # Lock held by another process, wait and retry
                    time.sleep(0.1)
                except AttributeError:
                    # fcntl not available (Windows) - proceed without locking
                    lock_acquired = True
                    break

            if not lock_acquired:
                return None, f"Timeout acquiring lock on sequence file after {timeout_seconds}s"

            # Read current sequence
            try:
                content = f.read().strip()
                current_sequence = int(content) if content else 0
            except ValueError as e:
                return None, f"Invalid sequence file content: '{content}' - {e}"

            # Increment sequence
            new_sequence = current_sequence + 1

            # Write back to file
            try:
                f.seek(0)
                f.truncate()
                f.write(str(new_sequence))
                f.flush()  # Ensure data is written
                os.fsync(f.fileno())  # Force write to disk
            except Exception as e:
                return None, f"Failed to write new sequence: {e}"

            # Unlock file
            if lock_acquired:
                try:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except (OSError, AttributeError):
                    pass

            return new_sequence, None

    except PermissionError as e:
        return None, f"Permission denied accessing sequence file: {e}"
    except Exception as e:
        return None, f"Unexpected error incrementing sequence: {e}"


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

        # Validate project directory
        project_path, error = validate_project_dir()
        if error:
            log_error('pre_tool_use', Exception(error))
            sys.exit(0)

        exec_dir = project_path / '.agent_planning' / '.exec'

        # Check if execution is in progress
        execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
        if not execution_id_file.exists():
            # No execution in progress - exit silently
            sys.exit(0)

        # Increment sequence number with timeout
        sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'
        new_sequence, error = increment_sequence_with_timeout(sequence_file, timeout_seconds=5)

        if error:
            log_error('pre_tool_use', Exception(error))
            sys.exit(0)

        # Validate that increment succeeded by re-reading file
        try:
            verified_sequence = int(sequence_file.read_text().strip())
            if verified_sequence != new_sequence:
                log_error('pre_tool_use', Exception(
                    f"Sequence verification failed: wrote {new_sequence}, read {verified_sequence}"
                ))
        except Exception as e:
            log_error('pre_tool_use', Exception(f"Sequence verification failed: {e}"))

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('pre_tool_use', e)
        sys.exit(0)


if __name__ == '__main__':
    main()
