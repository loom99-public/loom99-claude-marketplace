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


def validate_execution_id(execution_id):
    """
    Validate execution ID format to prevent path traversal.
    Returns True if valid, False otherwise.
    """
    if not execution_id or not isinstance(execution_id, str):
        return False

    # Expected format: YYYYMMDD-HHMMSS (15 characters)
    if len(execution_id) != 15:
        return False

    # Check format: 8 digits, dash, 6 digits
    import re
    if not re.match(r'^\d{8}-\d{6}$', execution_id):
        return False

    # No path separators
    if '/' in execution_id or '\\' in execution_id or '..' in execution_id:
        return False

    return True


def safe_move_leftover_files(exec_dir, planning_dir, execution_id, partial_files):
    """
    Safely move leftover PARTIAL files with race condition protection.
    Returns (moved_count, failed_moves) tuple.
    """
    # Create leftover directory with timestamp to avoid conflicts
    leftover_timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    leftover_dir = planning_dir / '_subagent_logs_leftover' / f'{execution_id}-{leftover_timestamp}'

    try:
        leftover_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        log_error('session_start', Exception(f"Permission denied creating leftover directory: {e}"))
        return 0, [(f.name, "Cannot create leftover directory") for f in partial_files]
    except Exception as e:
        log_error('session_start', Exception(f"Failed to create leftover directory: {e}"))
        return 0, [(f.name, "Cannot create leftover directory") for f in partial_files]

    moved_count = 0
    failed_moves = []

    # Move each PARTIAL file
    for partial_file in partial_files:
        try:
            # Re-check that file still exists (race condition protection)
            if not partial_file.exists():
                continue

            dest_path = leftover_dir / partial_file.name
            shutil.move(str(partial_file), str(dest_path))
            moved_count += 1
        except FileNotFoundError:
            # File was deleted by concurrent process - not an error
            continue
        except PermissionError as e:
            failed_moves.append((partial_file.name, f"Permission denied: {e}"))
            log_error('session_start', Exception(f"Permission denied moving {partial_file.name}: {e}"))
        except Exception as e:
            failed_moves.append((partial_file.name, f"Failed: {e}"))
            log_error('session_start', Exception(f"Failed to move {partial_file.name}: {e}"))

    return moved_count, failed_moves


def safe_delete_old_leftovers(leftover_base):
    """
    Safely delete old leftover directories with error handling.
    """
    if not leftover_base.exists() or not leftover_base.is_dir():
        return

    # Remove all subdirectories in _subagent_logs_leftover
    deleted_count = 0
    for item in leftover_base.iterdir():
        if item.is_dir():
            try:
                shutil.rmtree(item)
                deleted_count += 1
                log_info('session_start', f'Deleted old leftover directory: {item.name}')
            except PermissionError as e:
                log_error('session_start', Exception(f"Permission denied deleting {item.name}: {e}"))
            except Exception as e:
                log_error('session_start', Exception(f"Failed to delete {item.name}: {e}"))

    if deleted_count > 0:
        log_info('session_start', f'Cleaned up {deleted_count} old leftover directories')


def main():
    """Clean up leftover state files from interrupted sessions."""
    try:
        # Validate project directory
        project_path, error = validate_project_dir()
        if error:
            log_error('session_start', Exception(error))
            sys.exit(0)

        exec_dir = project_path / '.agent_planning' / '.exec'
        planning_dir = project_path / '.agent_planning'

        # Create .exec directory if it doesn't exist
        try:
            exec_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            log_error('session_start', Exception(f"Permission denied creating .exec directory: {e}"))
            sys.exit(0)
        except Exception as e:
            log_error('session_start', Exception(f"Failed to create .exec directory: {e}"))
            sys.exit(0)

        # Check for leftover state files
        execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
        sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'

        leftover_found = False
        execution_id = None

        if execution_id_file.exists():
            try:
                execution_id = execution_id_file.read_text().strip()

                # Validate execution ID before using it
                if not validate_execution_id(execution_id):
                    log_error('session_start', Exception(f"Invalid leftover execution ID format: {execution_id}"))
                    # Clean up invalid state files
                    try:
                        execution_id_file.unlink()
                    except Exception:
                        pass
                    execution_id = None
                else:
                    leftover_found = True
                    log_info('session_start', f'Found leftover execution ID: {execution_id}')

            except Exception as e:
                log_error('session_start', Exception(f"Failed to read leftover execution ID: {e}"))

        # If leftovers exist, move PARTIAL files to leftover directory
        if leftover_found and execution_id:
            # Find PARTIAL files for this execution with error handling
            try:
                partial_files = list(exec_dir.glob(f'PARTIAL-{execution_id}-*.txt'))
            except Exception as e:
                log_error('session_start', Exception(f"Failed to list leftover PARTIAL files: {e}"))
                partial_files = []

            if partial_files:
                # Move PARTIAL files with race condition protection
                moved_count, failed_moves = safe_move_leftover_files(
                    exec_dir, planning_dir, execution_id, partial_files
                )

                if moved_count > 0:
                    log_info('session_start', f'Moved {moved_count} leftover PARTIAL files')

                if failed_moves:
                    for filename, error_msg in failed_moves:
                        log_info('session_start', f'Failed to move leftover {filename}: {error_msg}')

            # Clean up state files (best effort)
            try:
                if execution_id_file.exists():
                    execution_id_file.unlink()
            except PermissionError as e:
                log_error('session_start', Exception(f"Permission denied deleting CURRENT_EXECUTION_ID.txt: {e}"))
            except Exception as e:
                log_error('session_start', Exception(f"Failed to delete CURRENT_EXECUTION_ID.txt: {e}"))

            try:
                if sequence_file.exists():
                    sequence_file.unlink()
            except PermissionError as e:
                log_error('session_start', Exception(f"Permission denied deleting CURRENT_SEQUENCE.txt: {e}"))
            except Exception as e:
                log_error('session_start', Exception(f"Failed to delete CURRENT_SEQUENCE.txt: {e}"))

        # Delete old leftover directories
        leftover_base = planning_dir / '_subagent_logs_leftover'
        safe_delete_old_leftovers(leftover_base)

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('session_start', e)
        sys.exit(0)


if __name__ == '__main__':
    main()
