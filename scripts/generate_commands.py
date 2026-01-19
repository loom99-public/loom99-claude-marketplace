#!/usr/bin/env python3
"""
Generate slash command files from commands.yaml configuration.

This script reads the commands.yaml file and generates markdown command files
for each defined command, following the skill+wrapper pattern.

Usage:
    python scripts/generate_commands.py
"""

import sys
from pathlib import Path
import yaml


def load_commands_config():
    """Load commands configuration from commands.yaml"""
    config_path = Path(__file__).parent.parent / "commands.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def format_argument_hint(hint):
    """Format argument hint for display"""
    if hint is None:
        return ""
    return hint


def generate_command_content(command):
    """Generate the markdown content for a command file"""
    plugin = command["plugin"]
    skill_name = command["skill_name"]
    skill_arg = command["skill_arg"]
    argument_hint = format_argument_hint(command.get("argument_hint"))
    description = command.get("description", "")

    # Build frontmatter
    lines = ["---"]
    if argument_hint:
        lines.append(f'argument-hint: {argument_hint}')
    lines.append(f'description: "{description}"')
    lines.append("---")

    # Build skill invocation
    lines.append("")
    if skill_arg:
        lines.append(f'Skill("{skill_name}") with:')
        lines.append(f"  {skill_arg}: $ARGUMENTS")
    else:
        lines.append(f'Skill("{skill_name}")')

    return "\n".join(lines) + "\n"


def is_skill_wrapper(file_path):
    """Check if a command file is already a skill wrapper (safe to overwrite)"""
    if not file_path.exists():
        return True  # New files are safe to create

    content = file_path.read_text()
    # A skill wrapper has minimal content: frontmatter + Skill() invocation
    # Look for the Skill( pattern which indicates it's already a wrapper
    return "Skill(" in content and content.count("\n") < 15


def generate_commands():
    """Generate all command files from configuration"""
    config = load_commands_config()
    commands = config.get("commands", [])

    if not commands:
        print("No commands found in commands.yaml")
        return False

    errors = []
    success = 0
    skipped = 0

    for cmd in commands:
        try:
            plugin = cmd["plugin"]
            name = cmd["name"]

            # Determine command file path
            cmd_file = (
                Path(__file__).parent.parent
                / "plugins"
                / plugin
                / "commands"
                / f"{name}.md"
            )

            # Check if file exists and is NOT a skill wrapper (protect custom content)
            if cmd_file.exists() and not is_skill_wrapper(cmd_file):
                print(f"⊘ {plugin}:{name} - skipped (custom content, not a wrapper)")
                skipped += 1
                continue

            # Create parent directory if needed
            cmd_file.parent.mkdir(parents=True, exist_ok=True)

            # Generate and write content
            content = generate_command_content(cmd)
            cmd_file.write_text(content)

            print(f"✓ {plugin}:{name} → {cmd_file}")
            success += 1

        except Exception as e:
            errors.append(f"✗ {plugin}:{name} - {e}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  {error}")

    if skipped > 0:
        print(f"\n{success} commands generated, {skipped} skipped (custom content)")
    else:
        print(f"\n{success} commands generated successfully")

    return len(errors) == 0


if __name__ == "__main__":
    try:
        success = generate_commands()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
