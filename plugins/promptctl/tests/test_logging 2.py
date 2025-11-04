#!/usr/bin/env python3
"""
Test script for LogFlow logging system.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp"))

from logging import (
    LoggingConfig,
    ConsoleOutputConfig,
    JsonlOutputConfig,
    configure_logging,
    get_logger,
    log_info,
    log_error,
    log_hook_received,
    log_hook_matched,
    log_handler_start,
    log_handler_complete,
    log_action_start,
    log_action_result,
    LogLevel,
)


async def test_basic_logging():
    """Test basic logging functionality."""
    print("=== Test 1: Basic Logging ===\n")

    # Configure logging
    config = LoggingConfig(
        enabled=True,
        level=LogLevel.DEBUG,
        console=ConsoleOutputConfig(
            enabled=True,
            format="rich",
            colors=True,
        ),
        jsonl=JsonlOutputConfig(
            enabled=True,
            path="~/.promptctl/logs/test-{date}.jsonl",
        ),
    )

    configure_logging(config)
    await get_logger().start()

    # Test basic log levels
    log_info("Testing INFO level log")
    log_error("Testing ERROR level log", error="Sample error message")

    await asyncio.sleep(0.2)  # Let logs flush

    print("\n✓ Basic logging test complete\n")


async def test_hook_lifecycle():
    """Test hook lifecycle logging."""
    print("=== Test 2: Hook Lifecycle ===\n")

    session_id = "test-session-123"
    hook_name = "PostToolUse"
    handler_name = "auto-test"

    # Log hook lifecycle
    log_hook_received(
        hook_name=hook_name,
        session_id=session_id,
        data={"cwd": "/test/path", "tool": "Edit"}
    )

    await asyncio.sleep(0.1)

    log_hook_matched(
        hook_name=hook_name,
        handler_name=handler_name,
        session_id=session_id,
        data={"priority": 10, "actions": 2}
    )

    await asyncio.sleep(0.1)

    log_handler_start(
        handler_name=handler_name,
        session_id=session_id,
        data={"action_count": 2}
    )

    await asyncio.sleep(0.1)

    # Simulate action execution
    action_start_time = time.time()
    await asyncio.sleep(0.05)
    action_duration = (time.time() - action_start_time) * 1000

    log_action_start(
        action_type="command",
        handler_name=handler_name,
        session_id=session_id
    )

    await asyncio.sleep(0.1)

    log_action_result(
        action_type="command",
        handler_name=handler_name,
        session_id=session_id,
        duration_ms=action_duration,
        data={"exit_code": 0}
    )

    await asyncio.sleep(0.1)

    # Complete handler
    handler_duration = 150.5

    log_handler_complete(
        handler_name=handler_name,
        session_id=session_id,
        duration_ms=handler_duration,
        data={"actions_executed": 2, "success": True}
    )

    await asyncio.sleep(0.2)  # Let logs flush

    print("\n✓ Hook lifecycle test complete\n")


async def test_performance():
    """Test logging performance."""
    print("=== Test 3: Performance ===\n")

    session_id = "perf-test-session"

    start_time = time.time()
    num_logs = 100

    for i in range(num_logs):
        log_info(
            f"Performance test log {i}",
            session_id=session_id,
            data={"index": i}
        )

    # Wait for logs to flush
    await asyncio.sleep(0.5)

    elapsed = time.time() - start_time
    logs_per_second = num_logs / elapsed

    print(f"Logged {num_logs} entries in {elapsed:.3f}s")
    print(f"Performance: {logs_per_second:.0f} logs/second")

    print("\n✓ Performance test complete\n")


async def test_log_rotation():
    """Test log file rotation."""
    print("=== Test 4: Log Rotation ===\n")

    log_dir = Path.home() / ".promptctl" / "logs"
    log_pattern = "test-*.jsonl"

    # Log some entries to create a file
    for i in range(10):
        log_info(f"Rotation test log {i}", data={"test": "rotation"})

    await asyncio.sleep(0.2)

    # Check if log file was created
    log_files = list(log_dir.glob(log_pattern))

    if log_files:
        print(f"Log files created: {len(log_files)}")
        for log_file in log_files:
            size = log_file.stat().st_size
            print(f"  - {log_file.name}: {size} bytes")
    else:
        print("No log files found")

    print("\n✓ Log rotation test complete\n")


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("LogFlow Logging System Test Suite")
    print("="*60 + "\n")

    try:
        await test_basic_logging()
        await test_hook_lifecycle()
        await test_performance()
        await test_log_rotation()

        # Stop logger
        await get_logger().stop()

        print("="*60)
        print("All tests completed successfully!")
        print("="*60 + "\n")

        print("Check logs at: ~/.promptctl/logs/")
        print("\nView logs with:")
        print("  python3 bin/logs.py --format rich")
        print("  python3 bin/logs.py --hooks")
        print("  python3 bin/logs.py --format json\n")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
