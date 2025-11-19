#!/usr/bin/env python3
"""
Simple hello world script for dev-loop stop hook.
Reads from stdin and appends to /tmp/stop-hook-test.log
"""

import sys

# Read stdin
stdin_data = sys.stdin.read()

# Append to log file
with open("/tmp/stop-hook-test.log", "a") as f:
    f.write(stdin_data)
