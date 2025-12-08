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

        # Generate execution ID using timestamp format
        execution_id = datetime.now().strftime('%Y%m%d-%H%M%S')

        # Use CLAUDE_PROJECT_DIR if available, otherwise current directory
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
        exec_dir = Path(project_dir) / '.agent_planning' / '.exec'

        # Create .exec directory if it doesn't exist
        exec_dir.mkdir(parents=True, exist_ok=True)

        # Write execution ID to state file
        execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
        execution_id_file.write_text(execution_id)

        # Initialize sequence to 0 (will be incremented to 1 on first agent)
        sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'
        sequence_file.write_text('0')

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('user_prompt_submit', e)
        sys.exit(0)  # Don't block Claude execution


if __name__ == '__main__':
    main()
