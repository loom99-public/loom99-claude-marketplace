#!/usr/bin/env python3
"""
PromptCtl MCP Server

This server provides:
1. MCP tool and prompt endpoints for Claude integration
2. Hook event handling and processing
3. Configuration management (promptctl.yaml)
4. Timer-based event scheduling
5. Hooks configuration generation
"""

import asyncio
import json
import sys
import time
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

# Import logging system
from logflow import (
    LoggingConfig,
    configure_logging,
    get_logger,
    log_hook_received,
    log_hook_matched,
    log_handler_start,
    log_handler_complete,
    log_action_start,
    log_action_result,
    log_info,
    log_error,
)


# ============================================================================
# Hook Event Schemas (Based on Claude Code documentation)
# ============================================================================


class PermissionMode(str, Enum):
    """Permission modes for hook events."""

    DEFAULT = "default"
    PLAN = "plan"
    ACCEPT_EDITS = "acceptEdits"
    BYPASS_PERMISSIONS = "bypassPermissions"


class HookEventName(str, Enum):
    """Supported hook event types."""

    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    USER_PROMPT_SUBMIT = "UserPromptSubmit"
    NOTIFICATION = "Notification"
    STOP = "Stop"
    SUBAGENT_STOP = "SubagentStop"
    PRE_COMPACT = "PreCompact"
    SESSION_START = "SessionStart"
    SESSION_END = "SessionEnd"


class BaseHookInput(BaseModel):
    """Base schema for all hook inputs."""

    session_id: str = Field(..., description="Unique session identifier")
    transcript_path: str = Field(..., description="Path to session transcript")
    cwd: str = Field(..., description="Current working directory")
    permission_mode: PermissionMode = Field(
        ..., description="Current permission mode"
    )
    hook_event_name: str = Field(..., description="Name of the hook event")


class PreToolUseInput(BaseHookInput):
    """Schema for PreToolUse hook input."""

    tool_name: str = Field(..., description="Name of the tool being invoked")
    tool_input: Dict[str, Any] = Field(
        ..., description="Input parameters for the tool"
    )


class PostToolUseInput(BaseHookInput):
    """Schema for PostToolUse hook input."""

    tool_name: str = Field(..., description="Name of the tool that was executed")
    tool_input: Dict[str, Any] = Field(..., description="Input that was provided")
    tool_output: Optional[str] = Field(None, description="Tool output")
    error: Optional[str] = Field(None, description="Error message if tool failed")


class UserPromptSubmitInput(BaseHookInput):
    """Schema for UserPromptSubmit hook input."""

    prompt: str = Field(..., description="User's submitted prompt")


class StopInput(BaseHookInput):
    """Schema for Stop/SubagentStop hook input."""

    stop_reason: Optional[str] = Field(None, description="Reason for stopping")


class NotificationInput(BaseHookInput):
    """Schema for Notification hook input."""

    notification: str = Field(..., description="Notification message")


class SessionStartInput(BaseHookInput):
    """Schema for SessionStart hook input."""

    env_file: Optional[str] = Field(
        None, description="Path for persisting environment variables"
    )


# ============================================================================
# Hook Output Schemas
# ============================================================================


class PermissionDecision(str, Enum):
    """Permission decisions for PreToolUse hooks."""

    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"


class BlockDecision(str, Enum):
    """Block decisions for Stop/UserPromptSubmit hooks."""

    BLOCK = "block"
    UNDEFINED = "undefined"


class PreToolUseOutput(BaseModel):
    """Hook-specific output for PreToolUse."""

    hookEventName: str = Field(default="PreToolUse")
    permissionDecision: Optional[PermissionDecision] = None
    permissionDecisionReason: Optional[str] = None
    updatedInput: Optional[Dict[str, Any]] = None


class UserPromptSubmitOutput(BaseModel):
    """Hook-specific output for UserPromptSubmit."""

    hookEventName: str = Field(default="UserPromptSubmit")
    additionalContext: Optional[str] = None


class StopOutput(BaseModel):
    """Output for Stop/SubagentStop hooks."""

    decision: Optional[BlockDecision] = None
    reason: Optional[str] = None


class HookOutput(BaseModel):
    """Base output schema for all hooks."""

    model_config = ConfigDict(populate_by_name=True)

    continue_: bool = Field(
        default=True, alias="continue", description="Whether to continue execution"
    )
    stopReason: Optional[str] = Field(None, description="Reason for stopping")
    suppressOutput: bool = Field(
        default=False, description="Suppress output to user"
    )
    systemMessage: Optional[str] = Field(None, description="System message/warning")
    hookSpecificOutput: Optional[
        Union[PreToolUseOutput, UserPromptSubmitOutput, StopOutput]
    ] = None


# ============================================================================
# PromptCtl Configuration Schemas
# ============================================================================


class HandlerAction(BaseModel):
    """Configuration for a handler action."""

    model_config = ConfigDict(extra="allow")

    action: str = Field(..., description="Action type: prompt, command, git, etc.")
    # Additional fields depend on action type - keep flexible
    extra: Dict[str, Any] = Field(default_factory=dict)


class HandlerMatch(BaseModel):
    """Match conditions for a handler."""

    model_config = ConfigDict(extra="allow")

    tool: Optional[Union[str, List[str]]] = None
    file_pattern: Optional[str] = None
    # Additional match conditions
    extra: Dict[str, Any] = Field(default_factory=dict)


class Handler(BaseModel):
    """Configuration for a hook handler."""

    enabled: bool = Field(default=True)
    hook: HookEventName = Field(..., description="Hook event to handle")
    priority: int = Field(default=0, description="Handler priority (higher = first)")
    match: Optional[HandlerMatch] = None
    actions: List[HandlerAction] = Field(default_factory=list)


class PromptCtlConfig(BaseModel):
    """Root configuration for promptctl.yaml."""

    model_config = ConfigDict(extra="allow")

    version: str = Field(default="1.0")
    handlers: Dict[str, Handler] = Field(default_factory=dict)
    logging: Optional[LoggingConfig] = None


# ============================================================================
# Hook Event Context and Handler Engine
# ============================================================================


class EventContext:
    """Execution context for hook events with payload parsing."""

    def __init__(self, payload: Dict[str, Any]):
        self._payload = payload
        self._state: Dict[str, Any] = {}

    def get(self, path: str, default: Any = None) -> Any:
        """Get value from payload using dot notation."""
        parts = path.split(".")
        current = self._payload

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default

        return current

    def render(self, template: str) -> str:
        """Render template with variables from payload and state."""
        result = template

        # Replace payload variables
        result = self._replace_variables(result, self._payload, prefix="")

        # Replace state variables
        result = self._replace_variables(result, self._state, prefix="state.")

        return result

    def _replace_variables(
        self, text: str, data: Dict[str, Any], prefix: str
    ) -> str:
        """Replace variables in text from data dict."""
        result = text

        # Flatten nested dict for replacement
        flat = self._flatten_dict(data, parent_key=prefix.rstrip("."))

        for key, value in flat.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))

        return result

    def _flatten_dict(
        self, data: Dict[str, Any], parent_key: str = ""
    ) -> Dict[str, Any]:
        """Flatten nested dictionary with dot notation keys."""
        items = []

        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key

            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, new_key).items())
            else:
                items.append((new_key, value))

        return dict(items)

    def set_state(self, key: str, value: Any) -> None:
        """Set state value."""
        self._state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get state value."""
        return self._state.get(key, default)


class HandlerEngine:
    """Matches handlers and executes action chains."""

    def __init__(self, config: PromptCtlConfig):
        self.config = config

    def match_handlers(
        self, hook_name: str, payload: Dict[str, Any]
    ) -> List[Handler]:
        """Find handlers that match this hook event."""
        matched = []

        for handler_name, handler in self.config.handlers.items():
            # Skip disabled handlers
            if not handler.enabled:
                continue

            # Check hook type
            if handler.hook.value != hook_name:
                continue

            # Check match conditions
            if handler.match and not self._matches_conditions(payload, handler.match):
                continue

            matched.append(handler)

        # Sort by priority (highest first)
        matched.sort(key=lambda h: h.priority, reverse=True)

        return matched

    def _matches_conditions(
        self, payload: Dict[str, Any], match: HandlerMatch
    ) -> bool:
        """Check if payload matches handler conditions."""
        # Tool name matching
        if match.tool is not None:
            tool_name = payload.get("tool_name")
            if isinstance(match.tool, list):
                if tool_name not in match.tool:
                    return False
            elif tool_name != match.tool:
                return False

        # File pattern matching
        if match.file_pattern is not None:
            # Extract file path from tool_input
            tool_input = payload.get("tool_input", {})
            file_path = tool_input.get("file_path", "")
            if not file_path:
                return False

            if not Path(file_path).match(match.file_pattern):
                return False

        return True

    async def execute_handler(
        self, handler: Handler, handler_name: str, context: EventContext, session_id: str
    ) -> Dict[str, Any]:
        """Execute a handler's action chain."""
        start_time = time.time()

        # Log handler start
        log_handler_start(
            handler_name=handler_name,
            session_id=session_id,
            data={"priority": handler.priority, "action_count": len(handler.actions)}
        )

        results = []

        for action_config in handler.actions:
            action_start_time = time.time()

            try:
                # Log action start
                log_action_start(
                    action_type=action_config.action,
                    handler_name=handler_name,
                    session_id=session_id
                )

                result = await self._execute_action(action_config, context)
                action_duration_ms = (time.time() - action_start_time) * 1000

                # Log action result
                log_action_result(
                    action_type=action_config.action,
                    handler_name=handler_name,
                    session_id=session_id,
                    duration_ms=action_duration_ms,
                    data={"status": "success"}
                )

                results.append(
                    {"action": action_config.action, "status": "success", "result": result}
                )
            except Exception as e:
                action_duration_ms = (time.time() - action_start_time) * 1000

                # Log action error
                get_logger().log(
                    level="ACTION_ERROR",
                    message=f"Action failed",
                    action_type=action_config.action,
                    handler_name=handler_name,
                    session_id=session_id,
                    duration_ms=action_duration_ms,
                    error=str(e)
                )

                results.append(
                    {"action": action_config.action, "status": "error", "error": str(e)}
                )
                # Stop on error by default
                break

        handler_duration_ms = (time.time() - start_time) * 1000

        # Log handler complete
        log_handler_complete(
            handler_name=handler_name,
            session_id=session_id,
            duration_ms=handler_duration_ms,
            data={"actions_executed": len(results), "success": all(r["status"] == "success" for r in results)}
        )

        return {"actions_executed": len(results), "results": results}

    async def _execute_action(
        self, action: HandlerAction, context: EventContext
    ) -> Dict[str, Any]:
        """Execute a single action."""
        # This is where we'd implement different action types
        # For now, return a stub
        return {"type": action.action, "executed": True}


# ============================================================================
# Scheduled Event Manager
# ============================================================================


class ScheduledEvent(BaseModel):
    """Scheduled event for timer-based actions."""

    event_id: str
    scheduled_time: datetime
    action: str
    payload: Dict[str, Any]


class EventScheduler:
    """Manages timer-based event scheduling."""

    def __init__(self):
        self.scheduled_events: List[ScheduledEvent] = []
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Start the event scheduler."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        """Stop the event scheduler."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def schedule_event(
        self,
        event_id: str,
        delay_seconds: float,
        action: str,
        payload: Dict[str, Any],
    ):
        """Schedule an event to execute after a delay."""
        scheduled_time = datetime.now() + timedelta(seconds=delay_seconds)
        event = ScheduledEvent(
            event_id=event_id,
            scheduled_time=scheduled_time,
            action=action,
            payload=payload,
        )
        self.scheduled_events.append(event)

    async def _run(self):
        """Run the scheduler loop."""
        while self._running:
            await asyncio.sleep(1)  # Check every second

            now = datetime.now()
            due_events = [e for e in self.scheduled_events if e.scheduled_time <= now]

            for event in due_events:
                await self._execute_scheduled_event(event)
                self.scheduled_events.remove(event)

    async def _execute_scheduled_event(self, event: ScheduledEvent):
        """Execute a scheduled event."""
        # This is where we'd trigger the actual action
        # For now, just log it
        print(f"Executing scheduled event: {event.event_id}", file=sys.stderr)


# ============================================================================
# Configuration Management
# ============================================================================


class ConfigManager:
    """Manages promptctl.yaml configuration."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self._default_config_path()
        self._config: Optional[PromptCtlConfig] = None

    def _default_config_path(self) -> Path:
        """Get default config path."""
        # Look for promptctl.yaml in current directory or ~/.promptctl/
        local_config = Path.cwd() / "promptctl.yaml"
        if local_config.exists():
            return local_config

        home_config = Path.home() / ".promptctl" / "promptctl.yaml"
        return home_config

    def load_config(self) -> PromptCtlConfig:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            # Return default empty config
            return PromptCtlConfig()

        with open(self.config_path, "r") as f:
            data = yaml.safe_load(f)

        self._config = PromptCtlConfig(**data)
        return self._config

    def save_config(self, config: PromptCtlConfig):
        """Save configuration to YAML file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, "w") as f:
            yaml.dump(
                config.model_dump(exclude_none=True),
                f,
                default_flow_style=False,
                sort_keys=False,
            )

    def get_config(self) -> PromptCtlConfig:
        """Get current config, loading if necessary."""
        if self._config is None:
            self._config = self.load_config()
        return self._config


class HooksConfigWriter:
    """Writes hooks.json configuration for Claude Code."""

    @staticmethod
    def generate_hooks_config(
        dispatch_script: str, events: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate hooks.json configuration."""
        if events is None:
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

    @staticmethod
    def write_hooks_config(output_path: Path, dispatch_script: str):
        """Write hooks.json to file."""
        config = HooksConfigWriter.generate_hooks_config(dispatch_script)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(config, f, indent=2)


# ============================================================================
# MCP Server
# ============================================================================

# Initialize FastMCP server
mcp = FastMCP("promptctl")

# Global state
config_manager = ConfigManager()
event_scheduler = EventScheduler()


@mcp.tool()
def promptctl(action: str = "status") -> str:
    """
    PromptCtl tool for managing hook-based automation.

    Args:
        action: Action to perform (status, config, help)

    Returns:
        Result message
    """
    if action == "status":
        config = config_manager.get_config()
        enabled_handlers = sum(
            1 for h in config.handlers.values() if h.enabled
        )
        return f"PromptCtl active with {enabled_handlers} enabled handlers"

    elif action == "config":
        config_path = config_manager.config_path
        return f"Configuration: {config_path}"

    elif action == "help":
        return """PromptCtl - Hook-based automation for Claude Code

Available actions:
- status: Show current status
- config: Show config file location
- help: Show this help message

Configure handlers in promptctl.yaml to automate workflows."""

    else:
        return f"Unknown action: {action}. Use 'help' for available actions."


@mcp.tool()
def logs(
    filter_type: str = "all",
    limit: int = 20,
    days: int = 1,
) -> str:
    """
    Query PromptCtl logs.

    Args:
        filter_type: Filter type (all, hooks, errors, slow, recent)
        limit: Maximum number of entries to return
        days: Number of days to query

    Returns:
        Formatted log entries
    """
    from pathlib import Path
    from logflow import LogEntry, LogLevel, ConsoleFormatter

    log_dir = Path.home() / ".promptctl" / "logs"

    if not log_dir.exists():
        return "No logs found. Logs directory does not exist."

    # Get log files from the last N days
    from datetime import datetime, timedelta

    cutoff_date = datetime.now() - timedelta(days=days)
    log_files = []

    for file_path in sorted(log_dir.glob("*.jsonl"), reverse=True):
        try:
            date_str = file_path.stem
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date >= cutoff_date:
                log_files.append(file_path)
        except ValueError:
            continue

    if not log_files:
        return f"No log files found in {log_dir}"

    # Read entries
    entries = []
    for file_path in log_files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = LogEntry.from_jsonl(line.strip())

                    # Apply filters
                    if filter_type == "hooks" and not entry.level.value.startswith("HOOK"):
                        continue
                    elif filter_type == "errors" and entry.level != LogLevel.ERROR and not entry.error:
                        continue
                    elif filter_type == "slow" and (entry.duration_ms is None or entry.duration_ms < 1000):
                        continue

                    entries.append(entry)

                    if len(entries) >= limit:
                        break
                except Exception:
                    continue

            if len(entries) >= limit:
                break

    if not entries:
        return f"No matching log entries found (filter: {filter_type})"

    # Format entries
    formatter = ConsoleFormatter(colors=False, show_data=False)
    result_lines = []

    for entry in sorted(entries, key=lambda e: e.timestamp, reverse=True):
        formatted = formatter.format(entry, format_type="simple")
        result_lines.append(formatted)

    result = "\n".join(result_lines)
    result += f"\n\n{len(entries)} entries (filter: {filter_type}, days: {days})"

    return result


@mcp.prompt()
def setup_promptctl() -> str:
    """
    Setup prompt to help users configure PromptCtl.

    Returns:
        Setup instructions and guidance
    """
    return """# PromptCtl Setup

PromptCtl provides hook-based automation for Claude Code workflows. Let me help you set it up!

## Quick Start

1. **Create Configuration**: Create a `promptctl.yaml` file in your project or `~/.promptctl/`

2. **Define Handlers**: Configure handlers for different hook events:

```yaml
version: "1.0"
handlers:
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

  review-prompt:
    enabled: true
    hook: Stop
    priority: 5
    actions:
      - action: prompt
        template: "Please review the changes and suggest improvements"
```

## Available Hooks

- **PreToolUse**: Before tool execution (can modify input or block)
- **PostToolUse**: After tool completes
- **UserPromptSubmit**: When user submits a prompt
- **Stop**: When main agent finishes
- **SubagentStop**: When subagent finishes
- **SessionStart**: On session initialization
- **SessionEnd**: On session termination

## Action Types

- **prompt**: Send a prompt to Claude
- **command**: Execute a shell command
- **git**: Perform git operations
- **validate**: Run validation checks
- **conditional**: Execute actions conditionally

## What would you like to configure?

I can help you:
- Set up automatic testing on file changes
- Create review prompts after completion
- Configure git automation
- Set up validation workflows
- Create custom handler patterns

Let me know what you'd like to automate!"""


# Hook event handler - called by dispatch.py
async def handle_hook_event(event_data: Dict[str, Any]) -> HookOutput:
    """
    Process a hook event from Claude Code.

    Args:
        event_data: Hook event payload

    Returns:
        Hook output response
    """
    # Parse event type and create appropriate input model
    hook_event_name = event_data.get("hook_event_name", "")
    session_id = event_data.get("session_id", "unknown")

    # Log hook received with full input
    log_hook_received(
        hook_name=hook_event_name,
        session_id=session_id,
        data={
            "cwd": event_data.get("cwd", ""),
            "permission_mode": event_data.get("permission_mode", ""),
            "hook_input": event_data,  # Full hook input for debugging
        }
    )

    # Load configuration and match handlers
    config = config_manager.get_config()

    # Configure logging if specified in config
    if config.logging:
        configure_logging(config.logging)

    engine = HandlerEngine(config)

    matched_handlers = engine.match_handlers(hook_event_name, event_data)

    # Log matched handlers
    for handler in matched_handlers:
        # Find handler name
        handler_name = None
        for name, h in config.handlers.items():
            if h == handler:
                handler_name = name
                break

        if handler_name:
            log_hook_matched(
                hook_name=hook_event_name,
                handler_name=handler_name,
                session_id=session_id,
                data={
                    "priority": handler.priority,
                    "actions": len(handler.actions)
                }
            )

    # Create execution context
    context = EventContext(event_data)

    # Execute matched handlers
    for handler in matched_handlers:
        # Find handler name again
        handler_name = None
        for name, h in config.handlers.items():
            if h == handler:
                handler_name = name
                break

        if handler_name:
            await engine.execute_handler(handler, handler_name, context, session_id)

    # Return default success response
    hook_output = HookOutput()

    # Log hook output for debugging
    log_info(
        f"Hook response generated",
        session_id=session_id,
        hook_name=hook_event_name,
        data={
            "hook_output": hook_output.model_dump(by_alias=True, exclude_none=True),
            "handlers_executed": len(matched_handlers)
        }
    )

    return hook_output


def main():
    """Main entry point for the MCP server."""
    # Start logger
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(get_logger().start())

    # Start event scheduler
    loop.create_task(event_scheduler.start())

    # Log server start
    log_info("PromptCtl MCP server starting")

    try:
        # Run MCP server
        mcp.run()
    finally:
        # Stop logger on shutdown
        loop.run_until_complete(get_logger().stop())
        log_info("PromptCtl MCP server stopped")


if __name__ == "__main__":
    main()
