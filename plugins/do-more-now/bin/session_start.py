#!/usr/bin/env python3
"""
SessionStart Hook Handler

Cleans up leftover state files from interrupted sessions.
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
    """Clean up leftover state files from interrupted sessions."""
    try:
        # Use CLAUDE_PROJECT_DIR if available
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
        exec_dir = Path(project_dir) / '.agent_planning' / '.exec'
        planning_dir = Path(project_dir) / '.agent_planning'

        # Create .exec directory if it doesn't exist
        exec_dir.mkdir(parents=True, exist_ok=True)

        # Check for leftover state files
        execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
        sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'

        leftover_found = False
        execution_id = None

        if execution_id_file.exists():
            leftover_found = True
            execution_id = execution_id_file.read_text().strip()
            log_info('session_start', f'Found leftover execution ID: {execution_id}')

        # If leftovers exist, move PARTIAL files to leftover directory
        if leftover_found and execution_id:
            # Find PARTIAL files for this execution
            partial_files = list(exec_dir.glob(f'PARTIAL-{execution_id}-*.txt'))

            if partial_files:
                # Create leftover directory with timestamp
                leftover_timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                leftover_dir = planning_dir / '_subagent_logs_leftover' / f'{execution_id}-{leftover_timestamp}'
                leftover_dir.mkdir(parents=True, exist_ok=True)

                # Move PARTIAL files to leftover directory
                moved_count = 0
                for partial_file in partial_files:
                    try:
                        shutil.move(str(partial_file), str(leftover_dir / partial_file.name))
                        moved_count += 1
                    except Exception as e:
                        log_error('session_start', f'Failed to move {partial_file.name}: {e}')

                log_info('session_start', f'Moved {moved_count} leftover PARTIAL files to {leftover_dir}')

            # Clean up state files
            try:
                execution_id_file.unlink()
            except Exception:
                pass

            try:
                if sequence_file.exists():
                    sequence_file.unlink()
            except Exception:
                pass

        # Delete old leftover directories (keep directory structure, remove contents older than this session)
        leftover_base = planning_dir / '_subagent_logs_leftover'
        if leftover_base.exists() and leftover_base.is_dir():
            # Remove all subdirectories in _subagent_logs_leftover
            for item in leftover_base.iterdir():
                if item.is_dir():
                    try:
                        shutil.rmtree(item)
                        log_info('session_start', f'Deleted old leftover directory: {item.name}')
                    except Exception as e:
                        log_error('session_start', f'Failed to delete {item.name}: {e}')

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('session_start', e)
        sys.exit(0)


if __name__ == '__main__':
    main()
