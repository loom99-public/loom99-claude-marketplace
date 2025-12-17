#!/usr/bin/env python3
"""
Aggregate execution partial logs into a final report.
Called by Stop hook - checks if partials exist and aggregates them.

No external dependencies - uses only Python 3 standard library.

Directory structure:
  .agent_logs/do-more-now/
    CURRENT_EXECUTION_ID.txt   # State file
    CURRENT_SEQUENCE.txt       # State file
    EXEC-<cmd>-<timestamp>.md  # Final reports
    <session-id>-DEBUG.log     # Debug log per session
    partials/                  # Partial logs from agents
      <EXEC_ID>-<SEQ>-PARTIAL-<agent>.txt
"""

import json
import os
import re
import sys
import traceback
from collections import defaultdict
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(".agent_logs/do-more-now")


def get_log_file(session_id: str) -> Path:
    """Get log file path for this session."""
    return BASE_DIR / f"{session_id}-DEBUG.log"


def log(log_file: Path, msg: str):
    """Append timestamped message to log file."""
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a") as f:
            f.write(f"{datetime.now().isoformat()} {msg}\n")
    except Exception:
        pass


def main():
    # Read and parse hook input
    stdin_data = sys.stdin.read()

    try:
        hook_input = json.loads(stdin_data) if stdin_data.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    session_id = hook_input.get("session_id", "unknown")
    log_file = get_log_file(session_id)

    # Log startup
    log(log_file, "-" * 60)
    log(log_file, "aggregate-exec.py: STOP HOOK TRIGGERED")
    log(log_file, f"aggregate-exec.py: session_id={session_id}")
    log(log_file, f"aggregate-exec.py: cwd={os.getcwd()}")
    log(log_file, f"aggregate-exec.py: hook_input keys={list(hook_input.keys())}")

    # Log relevant hook input fields
    for key in ["hook_event_name", "permission_mode", "stop_hook_active"]:
        if key in hook_input:
            log(log_file, f"aggregate-exec.py: {key}={hook_input[key]}")

    try:
        partials_dir = BASE_DIR / "partials"
        output_dir = BASE_DIR

        # Check partials directory
        log(log_file, f"aggregate-exec.py: checking partials_dir={partials_dir}")
        if not partials_dir.exists():
            log(log_file, "aggregate-exec.py: partials dir does not exist, nothing to do")
            sys.exit(0)

        # Find partial files
        log(log_file, "aggregate-exec.py: scanning for partial files...")
        all_partials = list(partials_dir.glob("*-PARTIAL-*.txt"))
        log(log_file, f"aggregate-exec.py: found {len(all_partials)} files matching *-PARTIAL-*.txt")

        if not all_partials:
            log(log_file, "aggregate-exec.py: no partial files, nothing to aggregate")
            sys.exit(0)

        # Log each partial found
        for p in all_partials:
            log(log_file, f"aggregate-exec.py: found partial: {p.name}")

        # Group partials by execution ID
        log(log_file, "aggregate-exec.py: grouping partials by execution ID...")
        partials_by_exec = defaultdict(list)
        for p in all_partials:
            # Format: <EXEC_ID>-<SEQ>-PARTIAL-<agent>.txt
            match = re.match(r"(.+)-(\d+)-PARTIAL-(.*)\.txt", p.name)
            if match:
                exec_id = match.group(1)
                sequence = int(match.group(2))
                agent = match.group(3)
                partials_by_exec[exec_id].append((sequence, agent, p))
                log(log_file, f"aggregate-exec.py: parsed {p.name} -> exec_id={exec_id}, seq={sequence}, agent={agent}")
            else:
                log(log_file, f"aggregate-exec.py: WARNING - could not parse filename: {p.name}")

        if not partials_by_exec:
            log(log_file, "aggregate-exec.py: no valid partials after parsing")
            sys.exit(0)

        log(log_file, f"aggregate-exec.py: found {len(partials_by_exec)} execution groups: {list(partials_by_exec.keys())}")

        # Read current execution ID if available
        current_exec_file = BASE_DIR / "CURRENT_EXECUTION_ID.txt"
        current_exec_id = None
        log(log_file, f"aggregate-exec.py: checking for {current_exec_file}")
        if current_exec_file.exists():
            try:
                current_exec_id = current_exec_file.read_text().strip()
                log(log_file, f"aggregate-exec.py: CURRENT_EXECUTION_ID.txt contains: {current_exec_id}")
            except Exception as e:
                log(log_file, f"aggregate-exec.py: WARNING - could not read CURRENT_EXECUTION_ID.txt: {e}")
        else:
            log(log_file, "aggregate-exec.py: CURRENT_EXECUTION_ID.txt does not exist")

        # Determine which execution to aggregate
        if current_exec_id and current_exec_id in partials_by_exec:
            exec_id = current_exec_id
            log(log_file, f"aggregate-exec.py: using current execution ID: {exec_id}")
        else:
            exec_id = sorted(partials_by_exec.keys(), reverse=True)[0]
            log(log_file, f"aggregate-exec.py: current exec ID not found in partials, using most recent: {exec_id}")

        # Get partials for this execution, sorted by sequence
        partials = sorted(partials_by_exec[exec_id], key=lambda x: x[0])
        log(log_file, f"aggregate-exec.py: aggregating {len(partials)} partials for execution {exec_id}")

        if not partials:
            log(log_file, f"aggregate-exec.py: no partials for execution {exec_id}")
            sys.exit(0)

        # Log the partials we're aggregating
        for seq, agent, path in partials:
            log(log_file, f"aggregate-exec.py: will aggregate: seq={seq}, agent={agent}, file={path.name}")

        # Extract command name from first partial content
        command_name = "do"
        try:
            content = partials[0][2].read_text()
            log(log_file, f"aggregate-exec.py: reading first partial to extract command name...")
            for line in content.split("\n")[:20]:
                if line.startswith("COMMAND:"):
                    cmd = line.split(":", 1)[1].strip()
                    if cmd:
                        command_name = cmd
                        log(log_file, f"aggregate-exec.py: extracted command name: {command_name}")
                    break
        except Exception as e:
            log(log_file, f"aggregate-exec.py: could not extract command name: {e}")

        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = output_dir / f"EXEC-{command_name}-{timestamp}.md"
        log(log_file, f"aggregate-exec.py: output file will be: {output_file}")

        # Build the report
        log(log_file, "aggregate-exec.py: building report...")
        lines = [
            "# Execution Report",
            "",
            f"**Execution ID**: {exec_id}",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Agents**: {len(partials)}",
            "",
            "---",
            "",
        ]

        for sequence, agent_name, partial_path in partials:
            log(log_file, f"aggregate-exec.py: processing partial for agent: {agent_name}")
            lines.append(f"## {agent_name}")
            lines.append("")

            try:
                content = partial_path.read_text()
                content_lines = len(content.split("\n"))
                log(log_file, f"aggregate-exec.py: read {content_lines} lines from {partial_path.name}")

                # Skip metadata header (everything before first blank line)
                parts = content.split("\n\n", 1)
                if len(parts) > 1:
                    lines.append(parts[1])
                else:
                    lines.append(content)
            except Exception as e:
                lines.append(f"*Error reading partial: {e}*")
                log(log_file, f"aggregate-exec.py: ERROR reading {partial_path}: {e}")

            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append(f"**Report saved to**: `{output_file}`")

        # Write the report
        report_content = "\n".join(lines)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file.write_text(report_content)
        report_lines = len(report_content.split("\n"))
        log(log_file, f"aggregate-exec.py: wrote report ({report_lines} lines) to {output_file}")

        # Clean up partial files for THIS execution only
        log(log_file, "aggregate-exec.py: cleaning up partial files...")
        for _, agent, partial_path in partials:
            try:
                partial_path.unlink()
                log(log_file, f"aggregate-exec.py: deleted {partial_path.name}")
            except Exception as e:
                log(log_file, f"aggregate-exec.py: WARNING - could not delete {partial_path}: {e}")

        # Clean up state files
        log(log_file, "aggregate-exec.py: cleaning up state files...")
        for state_file in ["CURRENT_EXECUTION_ID.txt", "CURRENT_SEQUENCE.txt"]:
            try:
                state_path = BASE_DIR / state_file
                if state_path.exists():
                    state_path.unlink()
                    log(log_file, f"aggregate-exec.py: deleted {state_file}")
            except Exception as e:
                log(log_file, f"aggregate-exec.py: WARNING - could not delete {state_file}: {e}")

        log(log_file, "aggregate-exec.py: aggregation complete, outputting systemMessage")

        # Output JSON with systemMessage for Claude Code to display
        output = {"systemMessage": report_content}
        print(json.dumps(output))

    except Exception as e:
        log(log_file, f"aggregate-exec.py: FATAL ERROR - {type(e).__name__}: {e}")
        log(log_file, f"aggregate-exec.py: traceback:\n{traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()