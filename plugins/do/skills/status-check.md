---
name: status-check
description: Quick diagnostic of project or work status. Use when user asks "what's the status", "how's it going", "where are we".
---

# Status Check

Fast, read-only diagnostic.

## Process

Determine scope from context:
- **Project-wide**: Use do3:project-evaluator for high-level assessment
- **Focused area**: Use do3:work-evaluator for specific assessment

## Output

STATUS-*.md or WORK-EVALUATION-*.md with:
- Current state assessment
- Completion metrics
- Blockers/issues identified
- Verdict: COMPLETE | INCOMPLETE | BLOCKED | PAUSE

```
═══════════════════════════════════════
Status: [verdict]
  [Key findings - 2-3 bullets]
Next: [recommended action]
═══════════════════════════════════════
```
