#!/usr/bin/env python3
"""
SubagentStop Hook Handler

Verifies or creates PARTIAL execution trace files for completed subagents.
"""

import sys
import json
import os
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


def extract_execution_trace_from_transcript(transcript_path):
    """
    Extract execution tracking section from transcript.

    Returns the content if found, None otherwise.
    """
    try:
        if not transcript_path or not Path(transcript_path).exists():
            return None

        # Read transcript file with error handling for binary/encoding issues
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try with latin-1 encoding as fallback
            try:
                with open(transcript_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception:
                return None
        except Exception:
            return None

        # Look for execution tracking section
        # Agents write sections like "## Execution Tracking" or "## Partial Execution Trace"
        import re
        pattern = r'##\s*(Execution Tracking|Partial Execution Trace)\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            return match.group(2).strip()

        return None

    except Exception as e:
        log_error('subagent_stop', Exception(f"Failed to extract from transcript: {e}"))
        return None


def validate_agent_name(agent_name):
    """
    Validate and sanitize agent name to prevent path traversal.
    Returns sanitized agent name or 'unknown'.
    """
    if not agent_name or not isinstance(agent_name, str):
        return 'unknown'

    # Remove any path separators to prevent directory traversal
    agent_name = agent_name.replace('/', '-').replace('\\', '-').replace('..', '')

    # Remove any non-alphanumeric characters except dash and underscore
    import re
    agent_name = re.sub(r'[^a-zA-Z0-9_-]', '', agent_name)

    # Limit length
    agent_name = agent_name[:50]

    return agent_name if agent_name else 'unknown'


def main():
    """Verify or create PARTIAL execution trace file."""
    try:
        # Read stdin to get subagent completion event
        stdin_data = sys.stdin.read()

        if not stdin_data:
            sys.exit(0)

        # Parse JSON input
        try:
            data = json.loads(stdin_data)
        except (json.JSONDecodeError, ValueError):
            # Can't parse - exit silently
            sys.exit(0)

        # Extract information from stdin
        raw_agent_name = data.get('agent') or data.get('task') or data.get('agent_name') or 'unknown'
        agent_name = validate_agent_name(raw_agent_name)
        status = data.get('status', 'unknown')
        transcript_path = data.get('transcript_path')

        # Validate project directory
        project_path, error = validate_project_dir()
        if error:
            log_error('subagent_stop', Exception(error))
            sys.exit(0)

        exec_dir = project_path / '.agent_planning' / '.exec'

        # Check if execution is in progress
        execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
        if not execution_id_file.exists():
            # No execution in progress - exit silently
            sys.exit(0)

        # Read execution ID and sequence
        try:
            execution_id = execution_id_file.read_text().strip()
        except Exception as e:
            log_error('subagent_stop', Exception(f"Failed to read CURRENT_EXECUTION_ID.txt: {e}"))
            sys.exit(0)

        sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'
        if not sequence_file.exists():
            sequence = 0
        else:
            try:
                sequence = int(sequence_file.read_text().strip())
            except ValueError:
                sequence = 0
            except Exception as e:
                log_error('subagent_stop', Exception(f"Failed to read CURRENT_SEQUENCE.txt: {e}"))
                sequence = 0

        # Expected PARTIAL file path (what agent should have written)
        partial_file = exec_dir / f'PARTIAL-{execution_id}-{sequence:03d}-{agent_name}.txt'

        # Check if agent already wrote PARTIAL file
        if partial_file.exists():
            # Agent wrote the file - verify it's not empty and exit
            try:
                if partial_file.stat().st_size > 0:
                    # File exists and has content - nothing to do
                    sys.exit(0)
            except Exception as e:
                log_error('subagent_stop', Exception(f"Failed to check PARTIAL file size: {e}"))

        # Agent didn't write PARTIAL or file is empty - create minimal metadata file
        completed_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Try to extract execution trace from transcript
        extracted_content = None
        if transcript_path:
            extracted_content = extract_execution_trace_from_transcript(transcript_path)

        # Build fallback PARTIAL content
        partial_content = f"""EXECUTION: {execution_id}
SEQUENCE: {sequence:03d}
AGENT: {agent_name}
STARTED: unknown
COMPLETED: {completed_time}
STATUS: {status}

## Work Performed
"""

        if extracted_content:
            # Use extracted content from transcript
            partial_content += extracted_content + "\n"
        else:
            # No transcript content available
            partial_content += "- Details not available (agent did not write execution trace)\n"

        partial_content += """
## Issues Encountered
"""

        if status != 'success' and status != 'unknown':
            partial_content += f"- Status: {status}\n"
        else:
            partial_content += "- None recorded\n"

        # Write PARTIAL file with error handling
        try:
            partial_file.write_text(partial_content)
        except PermissionError as e:
            log_error('subagent_stop', Exception(f"Permission denied writing PARTIAL file: {e}"))
            sys.exit(0)
        except Exception as e:
            log_error('subagent_stop', Exception(f"Failed to write PARTIAL file: {e}"))
            sys.exit(0)

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('subagent_stop', e)
        sys.exit(0)


if __name__ == '__main__':
    main()
