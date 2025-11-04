"""Command-line interface for promptctl - automated prompt management via Claude Code hooks."""

import sys
from pathlib import Path

import click


@click.group()
@click.version_option(version="0.1.0")
def main():
    """promptctl - Automated prompt management for Claude Code using hooks.

    promptctl integrates with Claude Code's hook system to provide intelligent
    automation workflows triggered by various events (tool use, prompts, etc).

    Installation:
    1. Install hook scripts: promptctl install-hooks
    2. Create config: ~/.promptctl.yaml
    3. Hooks will trigger automatically in Claude Code sessions

    For examples and documentation: promptctl examples
    """
    pass


@main.command()
@click.option(
    "--target",
    "-t",
    type=click.Path(),
    default=".claude/hooks",
    help="Target directory for hook installation",
)
def install_hooks(target):
    """Install Claude Code hook scripts to project directory.

    This copies all hook scripts to .claude/hooks/ (or specified directory)
    and makes them executable.
    """
    import shutil
    from importlib import resources

    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)

    # Get hook scripts from package
    hook_files = [
        "post-tool-use",
        "pre-tool-use",
        "user-prompt-submit",
        "notification",
        "stop",
        "subagent-stop",
        "pre-compact",
        "session-start",
        "session-end",
    ]

    installed = []
    for hook_name in hook_files:
        try:
            # Read from package resources
            hook_source = resources.files('promptctl').joinpath(f'hooks/{hook_name}')
            if hook_source.is_file():
                # Copy to target
                dest = target_path / hook_name
                dest.write_text(hook_source.read_text())
                dest.chmod(0o755)  # Make executable
                installed.append(hook_name)
                click.echo(f"✓ Installed: {hook_name}")
        except Exception as e:
            click.echo(f"✗ Failed to install {hook_name}: {e}", err=True)

    if installed:
        click.echo(f"\n✓ Successfully installed {len(installed)}/{len(hook_files)} hooks to {target_path}")
        click.echo("\nNext steps:")
        click.echo("1. Create ~/.promptctl.yaml configuration")
        click.echo("2. Run 'promptctl examples' to see example configs")
        click.echo("3. Hooks will trigger automatically in Claude Code")
    else:
        click.echo("\n✗ Failed to install hooks", err=True)
        sys.exit(1)


@main.command()
def examples():
    """Show example configuration files for common workflows."""
    from importlib import resources

    click.echo("=== Example Configurations ===\n")

    examples_list = [
        ("auto_test.yaml", "Run tests automatically after Write/Edit"),
        ("smart_commit.yaml", "AI-generated commit messages"),
        ("safety_checks.yaml", "Block dangerous Bash commands"),
        ("code_review.yaml", "Automated code review"),
        ("deploy_pipeline.yaml", "Full CI/CD workflow"),
    ]

    for filename, description in examples_list:
        click.echo(f"{filename}: {description}")

    click.echo("\nTo view an example:")
    click.echo("  promptctl show-example <name>")

    click.echo("\nTo install examples directory:")
    click.echo("  promptctl install-examples --target ./examples")


@main.command()
@click.argument("name")
def show_example(name):
    """Show a specific example configuration."""
    from importlib import resources

    try:
        example_path = resources.files('promptctl.examples').joinpath(f'{name}')
        if example_path.is_file():
            click.echo(f"=== {name} ===\n")
            click.echo(example_path.read_text())
        else:
            click.echo(f"Example '{name}' not found", err=True)
            click.echo("Run 'promptctl examples' to see available examples")
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error loading example: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--target",
    "-t",
    type=click.Path(),
    default="./examples",
    help="Target directory for examples",
)
def install_examples(target):
    """Install example configuration files to directory."""
    import shutil
    from importlib import resources

    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)

    examples = [
        "auto_test.yaml",
        "smart_commit.yaml",
        "safety_checks.yaml",
        "code_review.yaml",
        "deploy_pipeline.yaml",
    ]

    installed = []
    for example_name in examples:
        try:
            example_source = resources.files('promptctl.examples').joinpath(example_name)
            if example_source.is_file():
                dest = target_path / example_name
                dest.write_text(example_source.read_text())
                installed.append(example_name)
                click.echo(f"✓ Installed: {example_name}")
        except Exception as e:
            click.echo(f"✗ Failed to install {example_name}: {e}", err=True)

    if installed:
        click.echo(f"\n✓ Installed {len(installed)} examples to {target_path}")
    else:
        click.echo("\n✗ Failed to install examples", err=True)
        sys.exit(1)


@main.command()
@click.argument("config_path", type=click.Path(exists=True))
def validate(config_path):
    """Validate a promptctl configuration file."""
    import yaml

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Basic validation
        if not isinstance(config, dict):
            click.echo("✗ Config must be a YAML dictionary", err=True)
            sys.exit(1)

        if "handlers" not in config:
            click.echo("⚠ Warning: No handlers defined in config")

        handlers = config.get("handlers", {})
        click.echo(f"✓ Found {len(handlers)} handlers")

        for handler_name, handler_config in handlers.items():
            enabled = handler_config.get("enabled", True)
            status = "enabled" if enabled else "disabled"
            hook = handler_config.get("hook", "unknown")
            actions = len(handler_config.get("actions", []))
            click.echo(f"  - {handler_name}: {hook} hook, {actions} actions ({status})")

        click.echo(f"\n✓ Configuration is valid")

    except yaml.YAMLError as e:
        click.echo(f"✗ YAML parse error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"✗ Validation error: {e}", err=True)
        sys.exit(1)


@main.command()
def docs():
    """Open documentation in browser."""
    import webbrowser

    docs_url = "https://github.com/your-username/promptctl#readme"
    click.echo(f"Opening documentation: {docs_url}")
    webbrowser.open(docs_url)


if __name__ == "__main__":
    main()
