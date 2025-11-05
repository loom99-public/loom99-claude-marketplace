#!/usr/bin/env python3
"""
Dispatch script for promptctl hooks.

This standalone script receives hook events from Claude Code and processes
them independently. It does NOT import from the server module.

The dispatch script:
1. Reads JSON event data from stdin
2. Processes the hook event locally
3. Outputs the response (exit code 0 for success)
4. Logs everything to ~/.promptctl/logs/dispatch.log
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def get_log_file():
    """Get the log file path."""
    log_dir = Path.home() / ".promptctl" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "dispatch.log"


def log(message):
    """Write a log message to the log file."""
    timestamp = datetime.now().isoformat()
    log_file = get_log_file()
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def read_event_data():
    """Read and parse JSON event data from stdin."""
    try:
        data = json.load(sys.stdin)
        log(f"Received event data: {json.dumps(data, indent=2)}")
        return data
    except json.JSONDecodeError as e:
        log(f"ERROR: Invalid JSON from stdin: {e}")
        sys.exit(1)


def process_hook_event(event_data):
    """
    Process hook event and return response.

    This is a minimal implementation that:
    - Accepts all hook events (returns success)
    - Can be extended to read promptctl.yaml and execute handlers

    For now, this just logs the event and returns success.
    """
    # Extract basic event info
    hook_event_name = event_data.get("hook_event_name", "unknown")
    session_id = event_data.get("session_id", "unknown")
    cwd = event_data.get("cwd", "unknown")

    log(f"Hook triggered: {hook_event_name}")
    log(f"Session ID: {session_id}")
    log(f"Working directory: {cwd}")

    # Log tool-specific info if available
    if "tool_name" in event_data:
        log(f"Tool: {event_data['tool_name']}")
    if "tool_input" in event_data:
        log(f"Tool input: {json.dumps(event_data['tool_input'], indent=2)}")

    # Return minimal successful response
    # Most hooks just need exit code 0 with no output
    return {
        "continue": True
    }


def main():
    """Main entry point for the dispatch script."""
    log("=" * 80)
    log("Dispatch script started")

    # Read event data from stdin
    event_data = read_event_data()

    try:
        # Process the hook event
        response = process_hook_event(event_data)

        log(f"Processing complete - response: {json.dumps(response)}")

        # Only output JSON if there's meaningful content
        # Empty response with exit 0 is valid and means "allow/continue"
        if response and any(v is not True for v in response.values()):
            log(f"Writing JSON response to stdout: {json.dumps(response)}")
            print(json.dumps(response))
        else:
            log("No JSON response needed - returning exit code 0")

        # Exit with success
        log("Exiting with code 0 (success)")
        sys.exit(0)

    except Exception as e:
        # Log error and exit with error code
        log(f"ERROR: Exception during processing: {e}")
        import traceback
        log(f"Traceback:\n{traceback.format_exc()}")
        log("Exiting with code 1 (error)")
        sys.exit(1)


if __name__ == "__main__":
    main()
