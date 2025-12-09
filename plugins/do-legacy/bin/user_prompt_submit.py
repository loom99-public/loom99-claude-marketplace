#!/usr/bin/env python3
"""
UserPromptSubmit Hook Handler

Detects /do: commands and initializes execution tracking state.
"""

import sys
import json
import re
import os
from datetime import datetime
from pathlib import Path


def log_error(hook_name, error):
    """Log errors to hook_errors.log without blocking execution."""
    try:
        # Use CLAUDE_PROJECT_DIR if available, otherwise current directory
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
        # If we can't even log the error, just exit silently
        pass


def validate_project_dir():
    """
    Validate that project directory exists and is accessible.
    Returns (project_dir_path, error_message) tuple.
    """
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR')

    if not project_dir:
        # Use current directory as fallback
        project_dir = os.getcwd()

    project_path = Path(project_dir)

    # Check if directory exists
    if not project_path.exists():
        return None, f"Project directory does not exist: {project_dir}"

    # Check if it's actually a directory
    if not project_path.is_dir():
        return None, f"Project path is not a directory: {project_dir}"

    # Check if we have write access by attempting to create .agent_planning
    try:
        planning_dir = project_path / '.agent_planning'
        planning_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        return None, f"No write permission for directory: {project_dir}"
    except Exception as e:
        return None, f"Cannot create .agent_planning directory: {e}"

    return project_path, None


def main():
    """Detect /do: commands and initialize execution tracking."""
    try:
        # Read stdin to get user prompt
        stdin_data = sys.stdin.read()

        if not stdin_data:
            # Empty stdin - exit silently
            sys.exit(0)

        # Try to parse as JSON (if Claude provides structured input)
        try:
            data = json.loads(stdin_data)
            user_prompt = data.get('prompt', '') or data.get('text', '') or str(data)
        except (json.JSONDecodeError, ValueError):
            # Not JSON - treat as plain text
            user_prompt = stdin_data

        # Detect /do: command (case-insensitive, allow leading whitespace)
        if not re.match(r'^\s*/do:[a-zA-Z-]+', user_prompt, re.IGNORECASE):
            # Not a /do: command - exit silently
            sys.exit(0)

        # Validate project directory
        project_path, error = validate_project_dir()
        if error:
            log_error('user_prompt_submit', Exception(error))
            sys.exit(0)

        # Generate execution ID using timestamp format
        execution_id = datetime.now().strftime('%Y%m%d-%H%M%S')

        exec_dir = project_path / '.agent_planning' / '.exec'

        # Create .exec directory if it doesn't exist
        try:
            exec_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            log_error('user_prompt_submit', Exception(f"Cannot create .exec directory: {e}"))
            sys.exit(0)

        # Write execution ID to state file
        try:
            execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
            execution_id_file.write_text(execution_id)
        except PermissionError as e:
            log_error('user_prompt_submit', Exception(f"Permission denied writing CURRENT_EXECUTION_ID.txt: {e}"))
            sys.exit(0)
        except Exception as e:
            log_error('user_prompt_submit', Exception(f"Failed to write CURRENT_EXECUTION_ID.txt: {e}"))
            sys.exit(0)

        # Initialize sequence to 0 (will be incremented to 1 on first agent)
        try:
            sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'
            sequence_file.write_text('0')
        except PermissionError as e:
            # Clean up execution_id_file if sequence write fails
            try:
                execution_id_file.unlink()
            except Exception:
                pass
            log_error('user_prompt_submit', Exception(f"Permission denied writing CURRENT_SEQUENCE.txt: {e}"))
            sys.exit(0)
        except Exception as e:
            # Clean up execution_id_file if sequence write fails
            try:
                execution_id_file.unlink()
            except Exception:
                pass
            log_error('user_prompt_submit', Exception(f"Failed to write CURRENT_SEQUENCE.txt: {e}"))
            sys.exit(0)

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('user_prompt_submit', e)
        sys.exit(0)  # Don't block Claude execution


if __name__ == '__main__':
    main()
