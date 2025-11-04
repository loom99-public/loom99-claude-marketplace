#!/usr/bin/env python3
"""
PromptCtl Logs CLI

View and query PromptCtl logs with powerful filtering and formatting options.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

# Add parent directory to path to import logflow module
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp"))

from logflow import LogEntry, LogLevel, ConsoleFormatter


class LogQuery:
    """Query and filter log entries."""

    def __init__(self, log_dir: Path):
        self.log_dir = log_dir

    def get_log_files(self, days: int = 7) -> List[Path]:
        """Get log files from the last N days."""
        files = []
        cutoff_date = datetime.now() - timedelta(days=days)

        if not self.log_dir.exists():
            return files

        for file_path in sorted(self.log_dir.glob("*.jsonl"), reverse=True):
            try:
                # Parse date from filename (format: YYYY-MM-DD.jsonl)
                date_str = file_path.stem
                file_date = datetime.strptime(date_str, "%Y-%m-%d")

                if file_date >= cutoff_date:
                    files.append(file_path)
            except ValueError:
                # Skip files that don't match the date format
                continue

        return files

    def read_entries(
        self,
        files: List[Path],
        level: Optional[LogLevel] = None,
        hooks: bool = False,
        errors: bool = False,
        slow: bool = False,
        session_id: Optional[str] = None,
        handler: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[LogEntry]:
        """Read and filter log entries."""
        entries = []

        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = LogEntry.from_jsonl(line.strip())

                        # Apply filters
                        if level and entry.level != level:
                            continue

                        if hooks and not entry.level.value.startswith("HOOK"):
                            continue

                        if errors and entry.level != LogLevel.ERROR and not entry.error:
                            continue

                        if slow and (
                            entry.duration_ms is None or entry.duration_ms < 1000
                        ):
                            continue

                        if session_id and entry.session_id != session_id:
                            continue

                        if handler and entry.handler_name != handler:
                            continue

                        if event_type and entry.hook_name != event_type:
                            continue

                        entries.append(entry)

                        # Check limit
                        if limit and len(entries) >= limit:
                            return entries

                    except Exception as e:
                        # Skip malformed entries
                        print(
                            f"Warning: Failed to parse entry: {e}",
                            file=sys.stderr,
                        )
                        continue

        return entries


def main():
    """Main entry point for logs CLI."""
    parser = argparse.ArgumentParser(
        description="View and query PromptCtl logs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View all logs from today
  promptctl logs

  # View only hook events
  promptctl logs --hooks

  # View errors only
  promptctl logs --errors

  # View slow operations (>1s)
  promptctl logs --slow

  # View logs for specific session
  promptctl logs --session abc123

  # View logs for specific handler
  promptctl logs --handler auto-test

  # Limit output
  promptctl logs --limit 50

  # View logs from last N days
  promptctl logs --days 7

  # Output as JSON
  promptctl logs --format json

  # Specific log level
  promptctl logs --level HOOK_MATCHED
""",
    )

    parser.add_argument(
        "--log-dir",
        type=Path,
        default=Path.home() / ".promptctl" / "logs",
        help="Log directory (default: ~/.promptctl/logs)",
    )

    parser.add_argument(
        "--days",
        type=int,
        default=1,
        help="Number of days to query (default: 1)",
    )

    parser.add_argument(
        "--level",
        type=str,
        choices=[level.value for level in LogLevel],
        help="Filter by log level",
    )

    parser.add_argument(
        "--hooks",
        action="store_true",
        help="Show only hook-related events",
    )

    parser.add_argument(
        "--errors",
        action="store_true",
        help="Show only errors",
    )

    parser.add_argument(
        "--slow",
        action="store_true",
        help="Show only slow operations (>1s)",
    )

    parser.add_argument(
        "--session",
        type=str,
        help="Filter by session ID",
    )

    parser.add_argument(
        "--handler",
        type=str,
        help="Filter by handler name",
    )

    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of entries",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["rich", "simple", "json"],
        default="rich",
        help="Output format (default: rich)",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    parser.add_argument(
        "--tail",
        action="store_true",
        help="Show most recent entries first",
    )

    parser.add_argument(
        "-f",
        "--follow",
        action="store_true",
        help="Follow log file in real-time (like tail -f)",
    )

    parser.add_argument(
        "--event-type",
        type=str,
        help="Filter by specific hook event (e.g., PreToolUse, PostToolUse, Stop)",
    )

    parser.add_argument(
        "--show-input",
        action="store_true",
        help="Show full hook input data",
    )

    parser.add_argument(
        "--show-output",
        action="store_true",
        help="Show full hook output data",
    )

    args = parser.parse_args()

    # Create log query
    query = LogQuery(args.log_dir)

    # Get log files
    log_files = query.get_log_files(days=args.days)

    if not log_files:
        print(f"No log files found in {args.log_dir}", file=sys.stderr)
        return 1

    # Handle follow mode (tail -f)
    if args.follow:
        return follow_logs(
            log_dir=args.log_dir,
            level=LogLevel(args.level) if args.level else None,
            hooks=args.hooks,
            errors=args.errors,
            slow=args.slow,
            session_id=args.session,
            handler=args.handler,
            event_type=args.event_type,
            format_type=args.format,
            no_color=args.no_color,
            show_input=args.show_input,
            show_output=args.show_output,
        )

    # Read and filter entries
    level = LogLevel(args.level) if args.level else None
    entries = query.read_entries(
        log_files,
        level=level,
        hooks=args.hooks,
        errors=args.errors,
        slow=args.slow,
        session_id=args.session,
        handler=args.handler,
        event_type=args.event_type,
        limit=args.limit,
    )

    # Sort entries
    if args.tail:
        entries = sorted(entries, key=lambda e: e.timestamp, reverse=True)
    else:
        entries = sorted(entries, key=lambda e: e.timestamp)

    # Format and output
    if args.format == "json":
        for entry in entries:
            print(entry.to_jsonl())
    else:
        formatter = ConsoleFormatter(
            colors=not args.no_color,
            show_data=False,
            show_input=args.show_input,
            show_output=args.show_output,
        )

        for entry in entries:
            formatted = formatter.format(entry, format_type=args.format)
            print(formatted)

    # Print summary
    print(
        f"\n{len(entries)} entries found",
        file=sys.stderr,
    )

    return 0


def follow_logs(
    log_dir: Path,
    level: Optional[LogLevel] = None,
    hooks: bool = False,
    errors: bool = False,
    slow: bool = False,
    session_id: Optional[str] = None,
    handler: Optional[str] = None,
    event_type: Optional[str] = None,
    format_type: str = "rich",
    no_color: bool = False,
    show_input: bool = False,
    show_output: bool = False,
) -> int:
    """Follow log files in real-time."""
    import time

    formatter = ConsoleFormatter(
        colors=not no_color,
        show_data=False,
        show_input=show_input,
        show_output=show_output,
    )

    # Get current log file (today's date)
    from datetime import datetime

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{date_str}.jsonl"

    # Wait for file to exist
    while not log_file.exists():
        time.sleep(0.5)

    print(f"Following {log_file}... (Ctrl+C to stop)\n", file=sys.stderr)

    # Open file and seek to end
    with open(log_file, "r", encoding="utf-8") as f:
        # Seek to end
        f.seek(0, 2)

        try:
            while True:
                line = f.readline()
                if line:
                    try:
                        entry = LogEntry.from_jsonl(line.strip())

                        # Apply filters
                        if level and entry.level != level:
                            continue
                        if hooks and not entry.level.value.startswith("HOOK"):
                            continue
                        if errors and entry.level != LogLevel.ERROR and not entry.error:
                            continue
                        if slow and (entry.duration_ms is None or entry.duration_ms < 1000):
                            continue
                        if session_id and entry.session_id != session_id:
                            continue
                        if handler and entry.handler_name != handler:
                            continue
                        if event_type and entry.hook_name != event_type:
                            continue

                        # Format and print
                        if format_type == "json":
                            print(entry.to_jsonl())
                        else:
                            formatted = formatter.format(entry, format_type=format_type)
                            print(formatted)
                            sys.stdout.flush()
                    except Exception as e:
                        # Skip malformed entries
                        print(f"Warning: Failed to parse entry: {e}", file=sys.stderr)
                else:
                    # No new data, wait a bit
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopped following logs", file=sys.stderr)
            return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
