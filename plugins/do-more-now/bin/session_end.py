#!/usr/bin/env python3
"""
SessionEnd Hook Handler

Archives PARTIAL files and cleans up execution state.
Note: Does NOT invoke execution-summarizer (not supported from hooks).
Commands should invoke the summarizer manually if needed.
"""

import sys
import os
import shutil
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


def log_info(hook_name, message):
    """Log informational messages to hook_errors.log."""
    try:
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
        exec_dir = Path(project_dir) / '.agent_planning' / '.exec'
        exec_dir.mkdir(parents=True, exist_ok=True)

        log_path = exec_dir / 'hook_errors.log'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(log_path, 'a') as f:
            f.write(f"[{timestamp}] [{hook_name}] INFO: {message}\n")
    except Exception:
        pass


def main():
    """Archive PARTIAL files and clean up execution state."""
    try:
        # Use CLAUDE_PROJECT_DIR if available
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
        exec_dir = Path(project_dir) / '.agent_planning' / '.exec'

        # Check if execution was in progress
        execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
        if not execution_id_file.exists():
            # No execution in progress - exit silently
            sys.exit(0)

        # Read execution ID
        execution_id = execution_id_file.read_text().strip()

        # Find all PARTIAL files for this execution
        partial_files = list(exec_dir.glob(f'PARTIAL-{execution_id}-*.txt'))

        if partial_files:
            # Create archive directory
            archive_dir = exec_dir / 'archive' / execution_id
            archive_dir.mkdir(parents=True, exist_ok=True)

            # Move PARTIAL files to archive
            moved_count = 0
            for partial_file in partial_files:
                try:
                    shutil.move(str(partial_file), str(archive_dir / partial_file.name))
                    moved_count += 1
                except Exception as e:
                    log_error('session_end', f'Failed to move {partial_file.name}: {e}')

            log_info('session_end', f'Archived {moved_count} PARTIAL files for execution {execution_id}')
        else:
            log_info('session_end', f'No PARTIAL files found for execution {execution_id}')

        # Clean up state files
        try:
            execution_id_file.unlink()
        except Exception:
            pass

        sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'
        try:
            if sequence_file.exists():
                sequence_file.unlink()
        except Exception:
            pass

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('session_end', e)
        sys.exit(0)


if __name__ == '__main__':
    main()
