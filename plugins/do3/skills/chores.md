---
name: chores
description: Maintenance and housekeeping tasks. Use when user wants cleanup, dependency updates, or technical debt work.
---

# Chores

Maintenance and housekeeping.

## Modes

**Quick** (default, 5-10 min):
- Git hygiene
- Planning file cleanup
- Quick code scan (TODOs, debug code)
- Dependency quick check

**Thorough** (if "thorough" mentioned, 20-40 min):
- All quick chores
- Dead code detection
- Documentation sync
- Technical debt inventory
- Actually fix simple issues

**Specific** (if specific chore mentioned):
- `git` - Git hygiene only
- `planning` - Planning docs only
- `dead-code` - Dead code detection
- `deps` - Dependencies only
- `debt` - Tech debt inventory

## Process

Use do3:iterative-implementer to execute chores, actually fixing issues found.

## Output

```
═══════════════════════════════════════
Chores Complete
  Mode: [quick | thorough | specific]
  Fixed: [count] issues
  Flagged: [count] for later

  [Summary of what was done]
═══════════════════════════════════════
```
