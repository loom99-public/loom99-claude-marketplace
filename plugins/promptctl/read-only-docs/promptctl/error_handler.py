"""Error handling and recovery with minimal complexity."""

import asyncio
import logging
import re
import time
from typing import Dict, List, Optional


class ErrorHandler:
    """Simple error detection and recovery handler."""

    def __init__(self, logger: logging.Logger, config: Dict):
        self.logger = logger
        self.config = config
        self.interrupt_start_time = None
        self.interrupt_timeout_minutes = config.get("interrupt_timeout_minutes", 5)

    def detect_fatal_errors(self, screen_content: str) -> bool:
        """Detect fatal errors using simple patterns."""
        content_lower = screen_content.lower()

        fatal_patterns = [
            'unable to connect',
            'connection failed',
            'failed to connect',
            'authentication failed',
            'fatal error',
            'crashed',
            'segmentation fault',
            'out of memory'
        ]

        for pattern in fatal_patterns:
            if pattern in content_lower:
                self.logger.warning(f"Fatal error detected: {pattern}")
                return True

        return False

    def detect_user_interrupt(self, screen_content: str) -> bool:
        """Detect user interruption."""
        return 'interrupted by user' in screen_content.lower()

    def start_interrupt_timer(self):
        """Start tracking interrupt timeout."""
        self.interrupt_start_time = time.time()

        if self.interrupt_timeout_minutes == -1:
            self.logger.info("User interrupt detected - will wait indefinitely")
        elif self.interrupt_timeout_minutes == 0:
            self.logger.info("User interrupt detected - continuing immediately")
        else:
            self.logger.info(f"User interrupt detected - will auto-continue after {self.interrupt_timeout_minutes} minutes")

    def should_force_continue(self) -> bool:
        """Check if we should force continue after interrupt."""
        if self.interrupt_timeout_minutes == -1:
            return False

        if self.interrupt_timeout_minutes == 0:
            return True

        if not self.interrupt_start_time:
            return False

        elapsed_minutes = (time.time() - self.interrupt_start_time) / 60
        return elapsed_minutes >= self.interrupt_timeout_minutes

    def reset_interrupt_timer(self):
        """Reset interrupt timer when resuming."""
        if self.interrupt_start_time:
            elapsed_minutes = (time.time() - self.interrupt_start_time) / 60
            self.logger.info(f"Resumed from interrupt after {elapsed_minutes:.1f} minutes")
            self.interrupt_start_time = None

    async def handle_fatal_error(self, session) -> None:
        """Handle fatal errors by interrupting and restarting."""
        self.logger.warning("Handling fatal error - sending Ctrl+C and restarting")
        await session.async_send_text("\x03")  # Ctrl+C
        await asyncio.sleep(1)
        await session.async_send_text("claude --continue\r")

    async def handle_interrupt_timeout(self, session) -> bool:
        """Handle interrupt timeout - returns True if action was taken."""
        if self.should_force_continue():
            elapsed_minutes = (time.time() - self.interrupt_start_time) / 60
            self.logger.warning(f"Forcing continuation after {elapsed_minutes:.1f} minutes of interrupt")

            self.reset_interrupt_timer()
            await session.async_send_text("\r")
            return True

        return False
