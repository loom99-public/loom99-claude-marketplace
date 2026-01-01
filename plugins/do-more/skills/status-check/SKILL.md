---
name: status-check
description: Quick diagnostic of project or work status. Use when user asks "what's the status", "how's it going", "where are we".
---

# Status Check

Fast, read-only diagnostic.

## Process

Determine scope from context:
- **Project-wide**: Use do:project-evaluator for high-level assessment
- **Focused area**: Use do:work-evaluator for specific assessment

## Beads Integration (if available)

Include beads summary in status check:
```bash
bd ready --json       # Unblocked work
bd blocked --json     # Blocked work
bd stale --days 14    # Forgotten items
bd list --status in_progress --json  # Active work
```

## Output

STATUS-*.md or WORK-EVALUATION-*.md with:
- Current state assessment
- Completion metrics
- Blockers/issues identified
- Beads issue summary (if available)
- Verdict: COMPLETE | INCOMPLETE | BLOCKED | PAUSE

```
═══════════════════════════════════════
Status: [verdict]
  [Key findings - 2-3 bullets]
  Beads: n ready, m blocked, k in_progress
Next: [recommended action]
═══════════════════════════════════════
```
