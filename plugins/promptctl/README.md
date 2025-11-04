# PromptCtl

Hook-based automation for Claude Code workflows.

## Overview

PromptCtl is a Claude Code plugin that provides powerful hook-based automation capabilities. It allows you to:

- **Automate workflows** based on Claude Code events (tool usage, prompts, stops, etc.)
- **Execute custom actions** in response to hooks (commands, prompts, git operations)
- **Schedule delayed actions** with timer-based event management
- **Configure handlers** using simple YAML configuration

## Architecture

PromptCtl consists of four main components:

### 1. MCP Server (`mcp/server.py`)

The persistent server component that:
- Provides MCP tools and prompts to Claude
- Manages configuration from `promptctl.yaml`
- Handles hook event processing
- Schedules and executes timer-based actions
- Manages LogFlow logging system

### 2. Dispatch Script (`bin/dispatch.py`)

A lightweight script that:
- Receives hook events from Claude Code
- Forwards events to the server handler
- Returns structured responses

### 3. LogFlow Logging System (`mcp/logflow.py`)

Premium logging system with:
- **Semantic log levels** (HOOK_MATCHED, ACTION_START, etc.)
- **Async non-blocking architecture** (< 1% performance overhead)
- **JSONL storage** with automatic daily rotation
- **Beautiful console output** with colors and icons
- **Powerful CLI** for querying and filtering logs
- **MCP tool integration** for log access from Claude

### 4. Configuration (`promptctl.yaml`)

User-defined handlers and logging configuration:
- Which hooks to respond to
- Matching conditions (tool names, file patterns, etc.)
- Actions to execute (prompts, commands, git operations)
- Logging preferences (levels, outputs, formats)

## Installation

1. Install dependencies using uv:
```bash
cd plugins/promptctl
uv sync
```

2. The plugin will be automatically loaded by Claude Code when the marketplace is active.

## Quick Start (Using Justfile)

PromptCtl includes a `justfile` with common tasks. Install [just](https://github.com/casey/just) and run:

```bash
# See all available commands
just --list

# Tail logs in real-time
just tail

# View recent logs
just logs

# Run tests
just test

# Check syntax
just check
```

See the [Justfile section](#justfile-commands) for all available commands.

## Configuration

Create a `promptctl.yaml` file in your project root or `~/.promptctl/`:

```yaml
version: "1.0"

# Logging configuration
logging:
  enabled: true
  level: INFO  # DEBUG, INFO, WARN, ERROR, or semantic levels
  buffer_size: 10000
  rate_limit: 1000  # Max entries per second

  # Console output
  console:
    enabled: true
    format: rich  # rich, simple, json
    colors: true
    show_data: false

  # JSONL file output
  jsonl:
    enabled: true
    path: "~/.promptctl/logs/{date}.jsonl"
    rotation: daily  # daily or size
    max_size_mb: 100  # For size-based rotation

# Handler configuration
handlers:
  # Auto-run tests after editing Python files
  auto-test:
    enabled: true
    hook: PostToolUse
    priority: 10
    match:
      tool: ["Edit", "Write"]
      file_pattern: "*.py"
    actions:
      - action: command
        script: "pytest {tool_input.file_path}"

  # Prompt for review when agent stops
  review-prompt:
    enabled: true
    hook: Stop
    priority: 5
    actions:
      - action: prompt
        template: "Please review the changes and suggest improvements"

  # Validate before commits
  pre-commit-validation:
    enabled: true
    hook: PreToolUse
    match:
      tool: ["Bash"]
    actions:
      - action: validate
        checks:
          - type: command_succeeds
            command: "pytest"
```

## Available Hooks

PromptCtl supports all Claude Code hook events:

- **PreToolUse**: Before tool execution (can modify input or block)
- **PostToolUse**: After tool completes
- **UserPromptSubmit**: When user submits a prompt
- **Notification**: When Claude sends notifications
- **Stop**: When main agent finishes
- **SubagentStop**: When subagent finishes
- **PreCompact**: Before compacting context
- **SessionStart**: On session initialization
- **SessionEnd**: On session termination

## Action Types

### Prompt Action
Send a prompt to Claude:
```yaml
- action: prompt
  template: "Please review {tool_name} execution"
```

### Command Action
Execute shell commands:
```yaml
- action: command
  script: "pytest {tool_input.file_path}"
  capture: test_output  # Optional: capture output to state
```

### Git Action
Perform git operations:
```yaml
- action: git
  operation: stage
  files: ["*.py"]
```

### Validate Action
Run validation checks:
```yaml
- action: validate
  checks:
    - type: file_exists
      path: "tests/"
    - type: command_succeeds
      command: "pytest"
```

### Conditional Action
Execute actions conditionally:
```yaml
- action: conditional
  condition: "{tool_name} == 'Bash'"
  then:
    - action: prompt
      template: "Bash command executed"
  else:
    - action: prompt
      template: "Non-bash tool used"
```

## Template Variables

Actions support template variables from hook payloads:

- `{session_id}` - Current session ID
- `{cwd}` - Current working directory
- `{tool_name}` - Tool being used
- `{tool_input.file_path}` - File path from tool input
- `{prompt}` - User's prompt (UserPromptSubmit only)
- `{state.key}` - Access captured state values

## MCP Tool

The plugin provides a `promptctl` tool accessible from Claude:

```
promptctl(action="status")  # Show current status
promptctl(action="config")  # Show config location
promptctl(action="help")    # Show help
```

## MCP Prompt

Use the `setup_promptctl` prompt to get interactive setup guidance:

```
/setup_promptctl
```

Claude will help you configure handlers for your specific workflow needs.

## Handler Matching

Handlers use optional `match` conditions to filter events:

```yaml
match:
  # Match specific tools
  tool: "Edit"              # Single tool
  tool: ["Edit", "Write"]   # Multiple tools

  # Match file patterns
  file_pattern: "*.py"
  file_pattern: "src/**/*.ts"
```

Handlers without `match` conditions trigger on all events of that hook type.

## Handler Priority

When multiple handlers match, they execute in priority order (highest first):

```yaml
handlers:
  critical-validation:
    priority: 100
    # ...

  logging:
    priority: 1
    # ...
```

## Development

### Project Structure

```
promptctl/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── .mcp.json                # MCP server configuration
├── bin/
│   ├── dispatch.py          # Hook event dispatcher
│   ├── logs.py              # Log query CLI
│   └── write_hooks_config.py # Hooks config generator
├── hooks/
│   └── hooks.json           # Generated hooks configuration
├── mcp/
│   ├── server.py            # MCP server & event handler
│   └── logflow.py           # LogFlow logging system
├── tests/
│   └── test_logging.py      # Logging system tests
├── read-only-docs/          # Reference documentation
├── pyproject.toml           # Python dependencies
└── README.md                # This file
```

### Schema Validation

All hook inputs and outputs use Pydantic models for validation:
- `BaseHookInput` - Base schema for all hooks
- `PreToolUseInput`, `PostToolUseInput`, etc. - Event-specific schemas
- `HookOutput` - Standard output format
- `PreToolUseOutput`, `StopOutput`, etc. - Hook-specific outputs

### Testing

Run tests with pytest:
```bash
uv run pytest
```

## Examples

### Example 1: Auto-format on save

```yaml
handlers:
  auto-format:
    enabled: true
    hook: PostToolUse
    match:
      tool: ["Edit", "Write"]
      file_pattern: "*.py"
    actions:
      - action: command
        script: "black {tool_input.file_path}"
```

### Example 2: Delayed review prompt

```yaml
handlers:
  delayed-review:
    enabled: true
    hook: Stop
    actions:
      - action: schedule
        delay: 300  # 5 minutes
        action: prompt
        template: "Ready for a review of the recent changes?"
```

### Example 3: Pre-commit validation

```yaml
handlers:
  pre-commit-check:
    enabled: true
    hook: PreToolUse
    match:
      tool: "Bash"
    actions:
      - action: validate
        checks:
          - type: command_succeeds
            command: "pytest"
      - action: conditional
        condition: "{validated} == false"
        then:
          - action: prompt
            template: "Tests are failing. Please fix before committing."
```

## LogFlow Logging System

PromptCtl includes a flagship logging system called LogFlow that provides premium logging capabilities with beautiful output and powerful querying.

### Features

- **Semantic Log Levels**: Beyond ERROR/WARN/INFO
  - `HOOK_RECEIVED`, `HOOK_MATCHED`, `HOOK_EXECUTED`, `HOOK_SKIPPED`
  - `HANDLER_START`, `HANDLER_COMPLETE`, `HANDLER_ERROR`
  - `ACTION_START`, `ACTION_RESULT`, `ACTION_ERROR`
  - `PERFORMANCE`, `SLOW_OPERATION`

- **Beautiful Console Output**: Color-coded with icons
  ```
  [22:14:40.343] ℹ️  INFO Testing INFO level log
  [22:14:40.544] 📨 HOOK_RECEIVED PostToolUse Hook received
                 Session: test-ses...
  [22:14:40.645] 🎯 HOOK_MATCHED PostToolUse → auto-test Handler matched
                 Session: test-ses... | Priority: 10
  [22:14:40.898] ▶️  ACTION_START → auto-test Action started
                 Session: test-ses... | Action: command
  [22:14:40.999] ✓ ACTION_RESULT → auto-test Action completed
                 Session: test-ses... | Action: command | Duration: 50.67ms
  ```

- **JSONL Storage**: Structured logs with automatic rotation
  ```json
  {
    "timestamp": "2025-11-03T22:14:40.544187",
    "level": "HOOK_RECEIVED",
    "message": "Hook received",
    "session_id": "test-session-123",
    "hook_name": "PostToolUse",
    "data": {
      "cwd": "/test/path",
      "tool": "Edit"
    }
  }
  ```

- **Async Non-Blocking**: < 1% performance overhead
- **Daily Rotation**: Automatic log file management

### Viewing Logs

**CLI Tool**:
```bash
# View all logs
python3 bin/logs.py

# Tail logs in real-time (like tail -f)
python3 bin/logs.py --follow
python3 bin/logs.py -f

# Tail with filters
python3 bin/logs.py -f --hooks
python3 bin/logs.py -f --event-type PostToolUse
python3 bin/logs.py -f --errors

# Filter by event type (specific Claude Code hook events)
python3 bin/logs.py --event-type PreToolUse
python3 bin/logs.py --event-type PostToolUse
python3 bin/logs.py --event-type Stop
python3 bin/logs.py --event-type UserPromptSubmit

# Show full hook input and output payloads
python3 bin/logs.py --show-input --show-output --limit 10
python3 bin/logs.py --show-input --event-type PreToolUse
python3 bin/logs.py --show-output --event-type Stop

# View only hook events
python3 bin/logs.py --hooks

# View errors only
python3 bin/logs.py --errors

# View slow operations (>1s)
python3 bin/logs.py --slow

# Filter by session
python3 bin/logs.py --session abc123

# Filter by handler
python3 bin/logs.py --handler auto-test

# Limit output
python3 bin/logs.py --limit 50

# Different formats
python3 bin/logs.py --format simple
python3 bin/logs.py --format json

# Show recent logs first
python3 bin/logs.py --tail

# Combine filters
python3 bin/logs.py --event-type PostToolUse --show-input --limit 5
python3 bin/logs.py -f --hooks --show-input --show-output
```

**Using Justfile** (recommended):
```bash
# Tail logs in real-time
just tail

# Tail only hook events
just tail-hooks

# Tail specific event type
just tail-event PreToolUse

# View recent logs
just logs

# View logs with debug info (input/output)
just logs-debug

# View logs for specific event
just logs-event PostToolUse

# View only hook events
just logs-hooks

# View errors
just logs-errors

# See all available commands
just --list
```

**MCP Tool** (from Claude):
```python
# View recent logs
logs(filter_type="all", limit=20, days=1)

# View hook events
logs(filter_type="hooks", limit=10)

# View errors
logs(filter_type="errors", limit=5)

# View slow operations
logs(filter_type="slow", limit=10)
```

### Log Levels

Standard levels: `DEBUG`, `INFO`, `WARN`, `ERROR`

Semantic levels for hooks and handlers:
- **Hook lifecycle**: `HOOK_RECEIVED`, `HOOK_MATCHED`, `HOOK_EXECUTED`, `HOOK_SKIPPED`
- **Handler execution**: `HANDLER_START`, `HANDLER_COMPLETE`, `HANDLER_ERROR`
- **Action execution**: `ACTION_START`, `ACTION_RESULT`, `ACTION_ERROR`
- **Context**: `CONTEXT_RENDER`, `STATE_CHANGE`
- **Performance**: `PERFORMANCE`, `SLOW_OPERATION`

### Configuration

```yaml
logging:
  enabled: true
  level: INFO  # Minimum level to log
  buffer_size: 10000  # Async buffer capacity
  rate_limit: 1000  # Max entries/second (0 = unlimited)

  console:
    enabled: true
    format: rich  # rich, simple, json
    colors: true
    show_data: false  # Show full data dict in output

  jsonl:
    enabled: true
    path: "~/.promptctl/logs/{date}.jsonl"
    rotation: daily  # daily or size
    max_size_mb: 100  # For size-based rotation
```

### Log File Location

Default: `~/.promptctl/logs/`

Files are named by date: `2025-11-03.jsonl`

### Performance

- **< 1% overhead**: Async architecture with write-behind buffering
- **199 logs/second** in benchmark tests
- **Automatic batching**: Logs flushed every 100ms
- **Rate limiting**: Prevents log flooding

### Testing

Run logging tests:
```bash
python3 tests/test_logging.py
```

Tests validate:
- Basic logging functionality
- Hook lifecycle events
- Performance (100 logs in <0.5s)
- Log rotation and file creation

## Debugging with Hook Input/Output

PromptCtl captures the full [Claude Code hook input and output](https://docs.claude.com/en/docs/claude-code/hooks) for every hook event, allowing you to inspect the exact data sent and received.

### Viewing Hook Input

The `--show-input` flag displays the complete hook input payload as defined in the Claude Code hooks documentation:

```bash
# View hook inputs for all events
python3 bin/logs.py --show-input --limit 10

# View input for specific event type
python3 bin/logs.py --show-input --event-type PreToolUse

# Tail and show inputs in real-time
python3 bin/logs.py -f --show-input
```

**Example Output**:
```
[22:14:40.544] 📨 HOOK_RECEIVED PostToolUse Hook received
               Session: test-ses...
               ├─ Hook Input:
               │  {
               │    "session_id": "abc123",
               │    "transcript_path": "/path/to/transcript",
               │    "cwd": "/project/path",
               │    "permission_mode": "default",
               │    "hook_event_name": "PostToolUse",
               │    "tool_name": "Edit",
               │    "tool_input": {
               │      "file_path": "server.py",
               │      "old_string": "...",
               │      "new_string": "..."
               │    },
               │    "tool_output": "success"
               │  }
```

### Viewing Hook Output

The `--show-output` flag displays the hook response sent back to Claude Code:

```bash
# View hook outputs
python3 bin/logs.py --show-output --limit 10

# View output for Stop events
python3 bin/logs.py --show-output --event-type Stop

# View both input and output
python3 bin/logs.py --show-input --show-output --event-type PreToolUse
```

**Example Output**:
```
[22:14:41.234] ℹ️  INFO Hook response generated
               Session: test-ses... | Hook: PostToolUse
               ├─ Hook Output:
               │  {
               │    "continue": true,
               │    "suppressOutput": false
               │  }
```

### Common Debugging Workflows

**Debug a specific event type**:
```bash
# Watch PreToolUse events with full context
just tail-event PreToolUse --show-input --show-output
```

**Investigate handler execution**:
```bash
# See what handlers matched and their inputs
python3 bin/logs.py --hooks --show-input --limit 20
```

**Debug errors**:
```bash
# View errors with full context
python3 bin/logs.py --errors --show-input --show-output
```

### Hook Input Schema Reference

Different hook events provide different input fields. See the [Claude Code Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks#hook-input) for the complete schema for each event type:

- **PreToolUse**: Includes `tool_name`, `tool_input`
- **PostToolUse**: Includes `tool_name`, `tool_input`, `tool_output`, `error`
- **UserPromptSubmit**: Includes `prompt`
- **Stop/SubagentStop**: Includes `stop_reason`
- **SessionStart**: Includes `env_file`
- And more...

## Justfile Commands

PromptCtl includes a comprehensive `justfile` for common development and operations tasks.

### Installation

Install [just](https://github.com/casey/just):
```bash
# macOS
brew install just

# Linux
cargo install just

# Or see: https://github.com/casey/just#installation
```

### Available Commands

**Log Viewing**:
```bash
just logs               # View recent logs (rich format)
just logs-days 7        # View logs from last 7 days
just logs-hooks         # View only hook events
just logs-errors        # View only errors
just logs-slow          # View slow operations
just logs-debug         # View with hook input/output
just logs-event PostToolUse  # View specific event type
just logs-json          # View in JSON format
```

**Log Tailing**:
```bash
just tail               # Tail all logs in real-time
just tail-hooks         # Tail only hook events
just tail-event Stop    # Tail specific event type
```

**Development**:
```bash
just install            # Install dependencies
just test               # Run tests
just check              # Validate Python syntax
just dev                # Install + test + check
just format             # Format code with black
just lint               # Lint code with ruff
```

**Utilities**:
```bash
just log-info           # Show log file info and sizes
just log-count          # Count log entries
just log-search "pattern"  # Search logs for pattern
just clean-logs         # Delete all log files
just status             # Show plugin status
just example-config     # Generate example config
just gen-hooks          # Generate hooks.json
```

**Help**:
```bash
just --list             # List all commands
just logs-help          # Show logs CLI help
```

### Justfile Examples

**Monitor all hook events in real-time**:
```bash
just tail-hooks
```

**Debug a failing handler**:
```bash
# View logs for specific handler with full context
python3 bin/logs.py --handler auto-test --show-input --show-output
```

**Track down a bug**:
```bash
# Search for error pattern
just log-search "error_message"

# View errors with full context
just logs-errors
```

**Clean up old logs**:
```bash
# See current log size
just log-info

# Delete old logs
just clean-logs
```

## Contributing

This plugin is part of the loom99 Claude marketplace. Contributions welcome!

## License

MIT License - see LICENSE file for details.
