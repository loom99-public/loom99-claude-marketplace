---
name: iterative-workflow
description: Iterative implementation with runtime validation. Use for UI work, exploratory development, or when TDD is impractical.
---

# Iterative Workflow

Build incrementally, validate with runtime evidence.

## Loop

**Step 1: Implement**
Use do3:iterative-implementer to:
- Read STATUS/PLAN for context
- Build working functionality
- Commit frequently

**Step 2: Evaluate**
Use do3:work-evaluator to validate:
- Run the software
- Capture evidence (screenshots, logs, output)
- Compare against acceptance criteria

**Verdict**:
- COMPLETE → Exit
- INCOMPLETE with clear path → Continue
- PAUSE → Research, then continue
- BLOCKED → Surface to user

**Loop** until COMPLETE or BLOCKED.

## Output

```
═══════════════════════════════════════
Iterative Implementation Complete
  Iterations: [count]
  Files: [count] | Commits: [count]
Next: /do3:plan to update status
═══════════════════════════════════════
```
