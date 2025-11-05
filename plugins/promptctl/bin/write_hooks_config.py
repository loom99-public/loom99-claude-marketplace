#!/usr/bin/env python3
"""
Write hooks configuration for PromptCtl.

This script generates the hooks.json file that configures Claude Code
to call the dispatch.py script for all hook events.
"""

import json
from pathlib import Path


def generate_hooks_config(dispatch_script: str):
    """Generate hooks.json configuration."""
    events = [
        "PreToolUse",
        "PostToolUse",
        "Notification",
        "UserPromptSubmit",
        "SessionStart",
        "SessionEnd",
        "Stop",
        "SubagentStop",
        "PreCompact"
    ]

    hooks = {}
    for event_name in events:
        hooks[event_name] = [
            {
                "matcher": "*",
                "hooks": [{"type": "command", "command": dispatch_script}],
            }
        ]

    return {"hooks": hooks}


def main():
    """Generate and write hooks.json configuration."""
    script_dir = Path(__file__).parent
    hooks_config_file = script_dir.parent / "hooks" / "hooks.json"

    # Generate dispatch command - uses python3 to run dispatch.sh
    dispatch_command = "\"${CLAUDE_PLUGIN_ROOT}\"/bin/dispatch.sh"

    # Write hooks configuration
    config = generate_hooks_config(dispatch_command)

    hooks_config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(hooks_config_file, "w") as f:
        json.dump(config, f, indent=2)

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

