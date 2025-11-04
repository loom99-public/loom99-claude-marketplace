#!/usr/bin/env python3
"""
Write hooks configuration for PromptCtl.

This script generates the hooks.json file that configures Claude Code
to call the dispatch.py script for all hook events.
"""

import sys
from pathlib import Path

# Add parent directory to path to import server module
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp"))

from server import HooksConfigWriter


def main():
    """Generate and write hooks.json configuration."""
    script_dir = Path(__file__).parent
    hooks_config_file = script_dir.parent / "hooks" / "hooks.json"

    # Generate dispatch command - uses python3 to run dispatch.py
    dispatch_command = "python3 ${CLAUDE_PLUGIN_ROOT}/bin/dispatch.py"

    # Write hooks configuration
    HooksConfigWriter.write_hooks_config(hooks_config_file, dispatch_command)

    print(f"Wrote hooks config to: {hooks_config_file}")
    print("\nThe following hook events are configured:")
    print("- PreToolUse")
    print("- PostToolUse")
    print("- Notification")
    print("- UserPromptSubmit")
    print("- Stop")
    print("- SubagentStop")
    print("- PreCompact")
    print("- SessionStart")
    print("- SessionEnd")


if __name__ == "__main__":
    main()

