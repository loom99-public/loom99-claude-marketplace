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


def archive_partial_files(exec_dir, execution_id, partial_files):
    """
    Archive PARTIAL files with comprehensive error handling.
    Returns (moved_count, failed_moves) tuple.
    """
    moved_count = 0
    failed_moves = []

    # Validate archive directory is writable
    archive_base = exec_dir / 'archive'
    try:
        archive_base.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        log_error('session_end', Exception(f"Permission denied creating archive directory: {e}"))
        return 0, [(f.name, "Cannot create archive directory") for f in partial_files]
    except Exception as e:
        log_error('session_end', Exception(f"Failed to create archive directory: {e}"))
        return 0, [(f.name, "Cannot create archive directory") for f in partial_files]

    # Create execution-specific archive directory
    archive_dir = archive_base / execution_id
    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        log_error('session_end', Exception(f"Failed to create execution archive directory: {e}"))
        return 0, [(f.name, "Cannot create execution directory") for f in partial_files]

    # Check if archive directory is writable
    if not os.access(archive_dir, os.W_OK):
        log_error('session_end', Exception(f"Archive directory not writable: {archive_dir}"))
        return 0, [(f.name, "Archive directory not writable") for f in partial_files]

    # Move each PARTIAL file
    for partial_file in partial_files:
        try:
            dest_path = archive_dir / partial_file.name
            shutil.move(str(partial_file), str(dest_path))
            moved_count += 1
        except PermissionError as e:
            failed_moves.append((partial_file.name, f"Permission denied: {e}"))
            log_error('session_end', Exception(f"Permission denied moving {partial_file.name}: {e}"))
        except Exception as e:
            failed_moves.append((partial_file.name, f"Failed: {e}"))
            log_error('session_end', Exception(f"Failed to move {partial_file.name}: {e}"))

    return moved_count, failed_moves


def main():
    """Archive PARTIAL files and clean up execution state."""
    try:
        # Validate project directory
        project_path, error = validate_project_dir()
        if error:
            log_error('session_end', Exception(error))
            sys.exit(0)

        exec_dir = project_path / '.agent_planning' / '.exec'

        # Check if execution was in progress
        execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
        if not execution_id_file.exists():
            # No execution in progress - exit silently
            sys.exit(0)

        # Read execution ID
        try:
            execution_id = execution_id_file.read_text().strip()
        except Exception as e:
            log_error('session_end', Exception(f"Failed to read CURRENT_EXECUTION_ID.txt: {e}"))
            sys.exit(0)

        # Validate execution ID to prevent malicious path traversal
        if not validate_execution_id(execution_id):
            log_error('session_end', Exception(f"Invalid execution ID format: {execution_id}"))
            sys.exit(0)

        # Find all PARTIAL files for this execution
        try:
            partial_files = list(exec_dir.glob(f'PARTIAL-{execution_id}-*.txt'))
        except Exception as e:
            log_error('session_end', Exception(f"Failed to list PARTIAL files: {e}"))
            partial_files = []

        if partial_files:
            # Archive PARTIAL files with comprehensive error handling
            moved_count, failed_moves = archive_partial_files(exec_dir, execution_id, partial_files)

            if moved_count > 0:
                log_info('session_end', f'Archived {moved_count} PARTIAL files for execution {execution_id}')

            if failed_moves:
                for filename, error_msg in failed_moves:
                    log_info('session_end', f'Failed to archive {filename}: {error_msg}')
        else:
            log_info('session_end', f'No PARTIAL files found for execution {execution_id}')

        # Clean up state files (best effort - don't fail if we can't delete)
        try:
            execution_id_file.unlink()
        except PermissionError as e:
            log_error('session_end', Exception(f"Permission denied deleting CURRENT_EXECUTION_ID.txt: {e}"))
        except Exception as e:
            log_error('session_end', Exception(f"Failed to delete CURRENT_EXECUTION_ID.txt: {e}"))

        sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'
        try:
            if sequence_file.exists():
                sequence_file.unlink()
        except PermissionError as e:
            log_error('session_end', Exception(f"Permission denied deleting CURRENT_SEQUENCE.txt: {e}"))
        except Exception as e:
            log_error('session_end', Exception(f"Failed to delete CURRENT_SEQUENCE.txt: {e}"))

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('session_end', e)
        sys.exit(0)


if __name__ == '__main__':
    main()
