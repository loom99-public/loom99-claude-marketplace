#!/bin/bash
#
# bd-session-start.sh - Initialize bd and inject workflow context at session start
#
# Auto-initializes bd if:
#   - bd is installed
#   - .beads/ doesn't exist
#   - Current directory is a git repo
#
# Then outputs workflow context from skills/beads/context/session-start.md
# and shows current ready work from bd.
#

# Check if bd is installed
if ! command -v bd &>/dev/null; then
  exit 0
fi

# Auto-init if not initialized and in a git repo
if [ ! -d ".beads" ] && [ -d ".git" ]; then
  bd init --quiet 2>/dev/null || true

  # Install git hooks for zero-lag sync
  bd hooks install 2>/dev/null || true
fi

# Output context if bd is initialized
if [ -d ".beads" ]; then
  # Output workflow reminders from context file
  if [ -f "${CLAUDE_PLUGIN_ROOT}/skills/beads/context/session-start.md" ]; then
    cat "${CLAUDE_PLUGIN_ROOT}/skills/beads/context/session-start.md"
    echo ""
  fi

  # Append live status - ready work
  echo "## Current Ready Work"
  echo ""
  READY_COUNT=$(bd ready --json 2>/dev/null | jq '. | length' 2>/dev/null || echo "0")
  if [ "$READY_COUNT" -gt 0 ]; then
    bd ready --json 2>/dev/null | jq -r '.[] | "- **[\(.id)]** \(.title) (P\(.priority), \(.type))"' 2>/dev/null || true
  else
    echo "*No ready work - all issues are blocked or completed*"
  fi
  echo ""

  # Append in-progress work
  IN_PROGRESS_COUNT=$(bd list --status in_progress --json 2>/dev/null | jq '. | length' 2>/dev/null || echo "0")
  if [ "$IN_PROGRESS_COUNT" -gt 0 ]; then
    echo "## In Progress"
    echo ""
    bd list --status in_progress --json 2>/dev/null | jq -r '.[] | "- 🏗️ **[\(.id)]** \(.title)"' 2>/dev/null || true
    echo ""
  fi
fi

exit 0
