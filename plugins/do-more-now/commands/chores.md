---
argument-hint: [quick | thorough | specific-chore]
description: Chores - maintenance, cleanup, housekeeping tasks.
---

Maintenance and housekeeping. Cleanup of any sort.

<chore-input>
$ARGUMENTS
</chore-input>

## Modes

| Mode | Trigger | Duration | Scope |
|------|---------|----------|-------|
| **Quick** | default, "quick" | 5-10 min | Git hygiene, planning cleanup, quick code scan |
| **Thorough** | "thorough", "deep" | 20-40 min | All quick + dead code, doc sync, tech debt |
| **Specific** | chore name | varies | Single chore type |

**Specific chores**: `git`, `planning`, `dead-code`, `deps`, `debt`, `docs`

## Process

Use do:iterative-implementer to execute chores, actually fixing issues found.

**Quick chores**:
- Git hygiene (clean status, stale branches)
- Planning file cleanup (archive old STATUS/PLAN)
- Quick code scan (TODOs, debug code, secrets)
- Dependency quick check

**Thorough adds**:
- Dead code detection
- Documentation sync
- Technical debt inventory
- Actually fix simple issues found

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
