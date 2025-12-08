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


def extract_execution_trace_from_transcript(transcript_path):
    """
    Extract execution tracking section from transcript.

    Returns the content if found, None otherwise.
    """
    try:
        if not transcript_path or not Path(transcript_path).exists():
            return None

        with open(transcript_path, 'r') as f:
            content = f.read()

        # Look for execution tracking section
        # Agents write sections like "## Execution Tracking" or "## Partial Execution Trace"
        import re
        pattern = r'##\s*(Execution Tracking|Partial Execution Trace)\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            return match.group(2).strip()

        return None

    except Exception:
        return None


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
        agent_name = data.get('agent') or data.get('task') or data.get('agent_name') or 'unknown'
        status = data.get('status', 'unknown')
        transcript_path = data.get('transcript_path')

        # Use CLAUDE_PROJECT_DIR if available
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
        exec_dir = Path(project_dir) / '.agent_planning' / '.exec'

        # Check if execution is in progress
        execution_id_file = exec_dir / 'CURRENT_EXECUTION_ID.txt'
        if not execution_id_file.exists():
            # No execution in progress - exit silently
            sys.exit(0)

        # Read execution ID and sequence
        execution_id = execution_id_file.read_text().strip()

        sequence_file = exec_dir / 'CURRENT_SEQUENCE.txt'
        if not sequence_file.exists():
            sequence = 0
        else:
            try:
                sequence = int(sequence_file.read_text().strip())
            except ValueError:
                sequence = 0

        # Expected PARTIAL file path (what agent should have written)
        partial_file = exec_dir / f'PARTIAL-{execution_id}-{sequence:03d}-{agent_name}.txt'

        # Check if agent already wrote PARTIAL file
        if partial_file.exists():
            # Agent wrote the file - verify it's not empty and exit
            if partial_file.stat().st_size > 0:
                # File exists and has content - nothing to do
                sys.exit(0)

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

        # Write PARTIAL file
        partial_file.write_text(partial_content)

        # Exit cleanly
        sys.exit(0)

    except Exception as e:
        log_error('subagent_stop', e)
        sys.exit(0)


if __name__ == '__main__':
    main()
