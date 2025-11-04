#!/usr/bin/env python3
"""
LogFlow - Premium logging system for PromptCtl

A flagship logging implementation with:
- Semantic log levels
- Async non-blocking architecture
- JSONL storage with rotation
- Beautiful console output
- Powerful query capabilities
"""

import asyncio
import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO
from collections import deque

from pydantic import BaseModel, Field


# ============================================================================
# Semantic Log Levels
# ============================================================================


class LogLevel(str, Enum):
    """Semantic log levels for PromptCtl."""

    # Standard levels
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"

    # Hook lifecycle
    HOOK_RECEIVED = "HOOK_RECEIVED"
    HOOK_MATCHED = "HOOK_MATCHED"
    HOOK_EXECUTED = "HOOK_EXECUTED"
    HOOK_SKIPPED = "HOOK_SKIPPED"

    # Handler execution
    HANDLER_START = "HANDLER_START"
    HANDLER_COMPLETE = "HANDLER_COMPLETE"
    HANDLER_ERROR = "HANDLER_ERROR"

    # Action execution
    ACTION_START = "ACTION_START"
    ACTION_RESULT = "ACTION_RESULT"
    ACTION_ERROR = "ACTION_ERROR"

    # Context and state
    CONTEXT_RENDER = "CONTEXT_RENDER"
    STATE_CHANGE = "STATE_CHANGE"

    # Performance
    PERFORMANCE = "PERFORMANCE"
    SLOW_OPERATION = "SLOW_OPERATION"


# Level priorities for filtering
LEVEL_PRIORITY = {
    LogLevel.DEBUG: 10,
    LogLevel.INFO: 20,
    LogLevel.WARN: 30,
    LogLevel.ERROR: 40,
    # Semantic levels
    LogLevel.HOOK_RECEIVED: 15,
    LogLevel.HOOK_MATCHED: 20,
    LogLevel.HOOK_EXECUTED: 20,
    LogLevel.HOOK_SKIPPED: 15,
    LogLevel.HANDLER_START: 20,
    LogLevel.HANDLER_COMPLETE: 20,
    LogLevel.HANDLER_ERROR: 40,
    LogLevel.ACTION_START: 20,
    LogLevel.ACTION_RESULT: 20,
    LogLevel.ACTION_ERROR: 40,
    LogLevel.CONTEXT_RENDER: 10,
    LogLevel.STATE_CHANGE: 15,
    LogLevel.PERFORMANCE: 20,
    LogLevel.SLOW_OPERATION: 30,
}


# ============================================================================
# Log Entry Models
# ============================================================================


class LogEntry(BaseModel):
    """Structured log entry."""

    # Core fields
    timestamp: datetime = Field(default_factory=datetime.now)
    level: LogLevel
    message: str

    # Context
    session_id: Optional[str] = None
    hook_name: Optional[str] = None
    handler_name: Optional[str] = None
    action_type: Optional[str] = None

    # Additional data
    data: Dict[str, Any] = Field(default_factory=dict)

    # Performance metrics
    duration_ms: Optional[float] = None

    # Error tracking
    error: Optional[str] = None
    traceback: Optional[str] = None

    def to_jsonl(self) -> str:
        """Convert to JSONL format (single line JSON)."""
        data = self.model_dump(exclude_none=True)
        # Convert datetime to ISO format
        data["timestamp"] = self.timestamp.isoformat()
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_jsonl(cls, line: str) -> "LogEntry":
        """Parse from JSONL format."""
        data = json.loads(line)
        # Convert ISO timestamp back to datetime
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


# ============================================================================
# Logging Configuration
# ============================================================================


class ConsoleOutputConfig(BaseModel):
    """Console output configuration."""

    enabled: bool = True
    format: str = Field(default="rich", description="Format: rich, simple, json")
    colors: bool = True
    show_data: bool = Field(default=False, description="Show full data dict")


class JsonlOutputConfig(BaseModel):
    """JSONL file output configuration."""

    enabled: bool = True
    path: str = Field(
        default="~/.promptctl/logs/{date}.jsonl",
        description="Path with {date} placeholder",
    )
    rotation: str = Field(default="daily", description="Rotation: daily, size")
    max_size_mb: int = Field(default=100, description="Max size for size rotation")


class LoggingConfig(BaseModel):
    """Root logging configuration."""

    enabled: bool = True
    level: LogLevel = LogLevel.INFO
    buffer_size: int = Field(default=10000, description="Async buffer size")
    rate_limit: int = Field(
        default=1000, description="Max entries per second (0 = unlimited)"
    )

    console: ConsoleOutputConfig = Field(default_factory=ConsoleOutputConfig)
    jsonl: JsonlOutputConfig = Field(default_factory=JsonlOutputConfig)


# ============================================================================
# Console Formatter
# ============================================================================


class ConsoleFormatter:
    """Beautiful console output formatter."""

    # ANSI color codes
    COLORS = {
        LogLevel.DEBUG: "\033[36m",  # Cyan
        LogLevel.INFO: "\033[32m",  # Green
        LogLevel.WARN: "\033[33m",  # Yellow
        LogLevel.ERROR: "\033[31m",  # Red
        LogLevel.HOOK_RECEIVED: "\033[34m",  # Blue
        LogLevel.HOOK_MATCHED: "\033[35m",  # Magenta
        LogLevel.HOOK_EXECUTED: "\033[32m",  # Green
        LogLevel.HOOK_SKIPPED: "\033[90m",  # Gray
        LogLevel.HANDLER_START: "\033[36m",  # Cyan
        LogLevel.HANDLER_COMPLETE: "\033[32m",  # Green
        LogLevel.HANDLER_ERROR: "\033[31m",  # Red
        LogLevel.ACTION_START: "\033[36m",  # Cyan
        LogLevel.ACTION_RESULT: "\033[32m",  # Green
        LogLevel.ACTION_ERROR: "\033[31m",  # Red
        LogLevel.CONTEXT_RENDER: "\033[90m",  # Gray
        LogLevel.STATE_CHANGE: "\033[35m",  # Magenta
        LogLevel.PERFORMANCE: "\033[33m",  # Yellow
        LogLevel.SLOW_OPERATION: "\033[33m",  # Yellow
    }

    # Icons for different log levels
    ICONS = {
        LogLevel.DEBUG: "🔍",
        LogLevel.INFO: "ℹ️ ",
        LogLevel.WARN: "⚠️ ",
        LogLevel.ERROR: "❌",
        LogLevel.HOOK_RECEIVED: "📨",
        LogLevel.HOOK_MATCHED: "🎯",
        LogLevel.HOOK_EXECUTED: "✅",
        LogLevel.HOOK_SKIPPED: "⏭️ ",
        LogLevel.HANDLER_START: "🚀",
        LogLevel.HANDLER_COMPLETE: "✨",
        LogLevel.HANDLER_ERROR: "💥",
        LogLevel.ACTION_START: "▶️ ",
        LogLevel.ACTION_RESULT: "✓",
        LogLevel.ACTION_ERROR: "✗",
        LogLevel.CONTEXT_RENDER: "🔄",
        LogLevel.STATE_CHANGE: "📝",
        LogLevel.PERFORMANCE: "⚡",
        LogLevel.SLOW_OPERATION: "🐌",
    }

    RESET = "\033[0m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"

    def __init__(self, colors: bool = True, show_data: bool = False, show_input: bool = False, show_output: bool = False):
        self.colors = colors
        self.show_data = show_data
        self.show_input = show_input
        self.show_output = show_output

    def format(self, entry: LogEntry, format_type: str = "rich") -> str:
        """Format log entry for console output."""
        if format_type == "json":
            return entry.to_jsonl()
        elif format_type == "simple":
            return self._format_simple(entry)
        else:  # rich
            return self._format_rich(entry)

    def _format_rich(self, entry: LogEntry) -> str:
        """Rich formatted output with colors and icons."""
        lines = []

        # Main line: [timestamp] icon LEVEL message
        timestamp = entry.timestamp.strftime("%H:%M:%S.%f")[:-3]
        color = self.COLORS.get(entry.level, "") if self.colors else ""
        icon = self.ICONS.get(entry.level, "")
        reset = self.RESET if self.colors else ""
        gray = self.GRAY if self.colors else ""

        main_line = f"{gray}[{timestamp}]{reset} {color}{icon} {entry.level.value}{reset}"

        # Add handler/action info if present
        if entry.hook_name:
            main_line += f" {entry.hook_name}"
        if entry.handler_name:
            main_line += f" → {entry.handler_name}"

        main_line += f" {entry.message}"

        lines.append(main_line)

        # Add session info on second line if present
        metadata = []
        if entry.session_id:
            metadata.append(f"Session: {entry.session_id[:8]}...")
        if entry.action_type:
            metadata.append(f"Action: {entry.action_type}")
        if entry.duration_ms is not None:
            metadata.append(f"Duration: {entry.duration_ms:.2f}ms")

        if metadata:
            lines.append(f"{gray}               {' | '.join(metadata)}{reset}")

        # Add data if show_data is enabled
        if self.show_data and entry.data:
            for key, value in entry.data.items():
                if key == "hook_input" and not self.show_input:
                    continue
                if key == "hook_output" and not self.show_output:
                    continue
                lines.append(f"{gray}               ├─ {key}: {value}{reset}")

        # Add hook input if requested
        if self.show_input and entry.data.get("hook_input"):
            lines.append(f"{gray}               ├─ Hook Input:{reset}")
            import json
            hook_input = entry.data.get("hook_input")
            for line in json.dumps(hook_input, indent=2).split("\n"):
                lines.append(f"{gray}               │  {line}{reset}")

        # Add hook output if requested
        if self.show_output and entry.data.get("hook_output"):
            lines.append(f"{gray}               ├─ Hook Output:{reset}")
            import json
            hook_output = entry.data.get("hook_output")
            for line in json.dumps(hook_output, indent=2).split("\n"):
                lines.append(f"{gray}               │  {line}{reset}")

        # Add error if present
        if entry.error:
            lines.append(f"{gray}               └─ Error: {entry.error}{reset}")

        return "\n".join(lines)

    def _format_simple(self, entry: LogEntry) -> str:
        """Simple text format."""
        timestamp = entry.timestamp.strftime("%H:%M:%S")
        parts = [timestamp, entry.level.value]

        if entry.handler_name:
            parts.append(entry.handler_name)

        parts.append(entry.message)

        line = " ".join(parts)

        if entry.error:
            line += f" | Error: {entry.error}"

        return line


# ============================================================================
# JSONL Storage
# ============================================================================


class JsonlStorage:
    """JSONL file storage with rotation."""

    def __init__(self, config: JsonlOutputConfig):
        self.config = config
        self.current_file: Optional[Path] = None
        self.current_handle: Optional[TextIO] = None
        self.current_date: Optional[str] = None

    def _get_log_path(self) -> Path:
        """Get current log file path with date substitution."""
        path_template = self.config.path
        date_str = datetime.now().strftime("%Y-%m-%d")

        # Expand home directory
        path_str = path_template.replace("~", str(Path.home()))

        # Replace {date} placeholder
        path_str = path_str.replace("{date}", date_str)

        return Path(path_str)

    def _should_rotate(self) -> bool:
        """Check if log file should be rotated."""
        if self.config.rotation == "daily":
            current_date = datetime.now().strftime("%Y-%m-%d")
            if self.current_date != current_date:
                return True

        elif self.config.rotation == "size":
            if self.current_file and self.current_file.exists():
                size_mb = self.current_file.stat().st_size / (1024 * 1024)
                if size_mb >= self.config.max_size_mb:
                    return True

        return False

    def _rotate(self):
        """Rotate log file."""
        if self.current_handle:
            self.current_handle.close()
            self.current_handle = None

        self.current_file = None
        self.current_date = None

    def write(self, entry: LogEntry):
        """Write log entry to JSONL file."""
        if not self.config.enabled:
            return

        # Check for rotation
        if self._should_rotate():
            self._rotate()

        # Open new file if needed
        if self.current_file is None:
            self.current_file = self._get_log_path()
            self.current_date = datetime.now().strftime("%Y-%m-%d")

            # Create directory if needed
            self.current_file.parent.mkdir(parents=True, exist_ok=True)

            # Open file in append mode
            self.current_handle = open(self.current_file, "a", encoding="utf-8")

        # Write JSONL entry
        if self.current_handle:
            self.current_handle.write(entry.to_jsonl() + "\n")
            self.current_handle.flush()

    def close(self):
        """Close current file handle."""
        if self.current_handle:
            self.current_handle.close()
            self.current_handle = None


# ============================================================================
# Async LogFlow Engine
# ============================================================================


class LogFlow:
    """
    Async logging engine with three-layer pipeline:
    Capture → Process → Store
    """

    def __init__(self, config: LoggingConfig):
        self.config = config
        self.buffer: deque = deque(maxlen=config.buffer_size)
        self.console_formatter = ConsoleFormatter(
            colors=config.console.colors, show_data=config.console.show_data
        )
        self.jsonl_storage = JsonlStorage(config.jsonl)

        # Async processing
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._last_log_time = datetime.now()
        self._log_count_this_second = 0

    async def start(self):
        """Start async log processing."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._process_loop())

    async def stop(self):
        """Stop async log processing and flush."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        # Flush remaining entries
        await self._flush()

        # Close storage
        self.jsonl_storage.close()

    def log(
        self,
        level: LogLevel,
        message: str,
        session_id: Optional[str] = None,
        hook_name: Optional[str] = None,
        handler_name: Optional[str] = None,
        action_type: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[float] = None,
        error: Optional[str] = None,
        traceback: Optional[str] = None,
    ):
        """Log an entry (non-blocking)."""
        if not self.config.enabled:
            return

        # Check level priority
        if LEVEL_PRIORITY.get(level, 0) < LEVEL_PRIORITY.get(self.config.level, 0):
            return

        # Rate limiting
        if self.config.rate_limit > 0:
            now = datetime.now()
            if (now - self._last_log_time).total_seconds() >= 1.0:
                self._last_log_time = now
                self._log_count_this_second = 0

            if self._log_count_this_second >= self.config.rate_limit:
                return

            self._log_count_this_second += 1

        # Create log entry
        entry = LogEntry(
            level=level,
            message=message,
            session_id=session_id,
            hook_name=hook_name,
            handler_name=handler_name,
            action_type=action_type,
            data=data or {},
            duration_ms=duration_ms,
            error=error,
            traceback=traceback,
        )

        # Add to buffer
        self.buffer.append(entry)

    async def _process_loop(self):
        """Async processing loop."""
        while self._running:
            await asyncio.sleep(0.1)  # Process every 100ms
            await self._flush()

    async def _flush(self):
        """Flush buffer to outputs."""
        while self.buffer:
            entry = self.buffer.popleft()

            # Console output
            if self.config.console.enabled:
                formatted = self.console_formatter.format(
                    entry, format_type=self.config.console.format
                )
                print(formatted, file=sys.stderr, flush=True)

            # JSONL storage
            self.jsonl_storage.write(entry)


# ============================================================================
# Global Logger Instance
# ============================================================================

# Default configuration
_default_config = LoggingConfig()
_logger: Optional[LogFlow] = None


def get_logger() -> LogFlow:
    """Get global logger instance."""
    global _logger
    if _logger is None:
        _logger = LogFlow(_default_config)
    return _logger


def configure_logging(config: LoggingConfig):
    """Configure global logger."""
    global _logger, _default_config
    _default_config = config

    if _logger is not None:
        # Stop old logger
        asyncio.create_task(_logger.stop())

    # Create new logger
    _logger = LogFlow(config)
    asyncio.create_task(_logger.start())


# ============================================================================
# Convenience Functions
# ============================================================================


def log_debug(message: str, **kwargs):
    """Log debug message."""
    get_logger().log(LogLevel.DEBUG, message, **kwargs)


def log_info(message: str, **kwargs):
    """Log info message."""
    get_logger().log(LogLevel.INFO, message, **kwargs)


def log_warn(message: str, **kwargs):
    """Log warning message."""
    get_logger().log(LogLevel.WARN, message, **kwargs)


def log_error(message: str, **kwargs):
    """Log error message."""
    get_logger().log(LogLevel.ERROR, message, **kwargs)


def log_hook_received(hook_name: str, session_id: str, **kwargs):
    """Log hook received event."""
    get_logger().log(
        LogLevel.HOOK_RECEIVED,
        f"Hook received",
        hook_name=hook_name,
        session_id=session_id,
        **kwargs,
    )


def log_hook_matched(hook_name: str, handler_name: str, session_id: str, **kwargs):
    """Log hook matched event."""
    get_logger().log(
        LogLevel.HOOK_MATCHED,
        f"Handler matched",
        hook_name=hook_name,
        handler_name=handler_name,
        session_id=session_id,
        **kwargs,
    )


def log_handler_start(handler_name: str, session_id: str, **kwargs):
    """Log handler start event."""
    get_logger().log(
        LogLevel.HANDLER_START,
        f"Handler started",
        handler_name=handler_name,
        session_id=session_id,
        **kwargs,
    )


def log_handler_complete(
    handler_name: str, session_id: str, duration_ms: float, **kwargs
):
    """Log handler complete event."""
    get_logger().log(
        LogLevel.HANDLER_COMPLETE,
        f"Handler completed",
        handler_name=handler_name,
        session_id=session_id,
        duration_ms=duration_ms,
        **kwargs,
    )


def log_action_start(action_type: str, handler_name: str, session_id: str, **kwargs):
    """Log action start event."""
    get_logger().log(
        LogLevel.ACTION_START,
        f"Action started",
        action_type=action_type,
        handler_name=handler_name,
        session_id=session_id,
        **kwargs,
    )


def log_action_result(
    action_type: str, handler_name: str, session_id: str, duration_ms: float, **kwargs
):
    """Log action result event."""
    get_logger().log(
        LogLevel.ACTION_RESULT,
        f"Action completed",
        action_type=action_type,
        handler_name=handler_name,
        session_id=session_id,
        duration_ms=duration_ms,
        **kwargs,
    )
