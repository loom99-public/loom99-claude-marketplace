#!/usr/bin/env python3
"""
Dispatch script for promptctl hooks.

This lightweight script receives hook events from Claude Code and forwards
them to the promptctl server component for processing.

The dispatch script:
1. Reads JSON event data from stdin
2. Forwards to the server's event handler
3. Outputs the response (exit code 0 for success)
"""

import sys
import json
import asyncio
from pathlib import Path

# Add parent directory to path to import server module
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp"))

from server import handle_hook_event


def read_event_data():
    """Read and parse JSON event data from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON from stdin: {e}", file=sys.stderr)
        sys.exit(1)


async def dispatch_event():
    """Dispatch hook event to server handler."""
    # Read event data from stdin
    event_data = read_event_data()

    try:
        # Forward to server handler
        hook_output = await handle_hook_event(event_data)

        # Convert output to JSON and print to stdout
        output_json = hook_output.model_dump(by_alias=True, exclude_none=True)

        # Only output JSON if there's meaningful content
        # Otherwise, hooks work fine with exit code 0 and no output
        if hook_output.hookSpecificOutput or hook_output.systemMessage or not hook_output.continue_:
            print(json.dumps(output_json))

        # Exit with success
        sys.exit(0)

    except Exception as e:
        # Log error and exit with error code
        print(f"Error processing hook event: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the dispatch script."""
    asyncio.run(dispatch_event())


if __name__ == "__main__":
    main()
