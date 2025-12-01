---
argument-hint: [area of focus]
description: Evaluate the project and make an implementation plan.  Pass args to focus on something specific, or let Claude decide.  Designed to work with /dev-loop:test-and-implement
---

If specific areas of focus are defined below, focus entirely on those goals and architectural work to enable those goals.  If 'specific-areas-of-focus' is empty, use the PROJECT_SPEC.md file to evaluate the project as a whole.

Specific areas of focus:
<specific-areas-of-focus>
$ARGUMENTS
</specific-areas-of-focus>

Step 1: Use the dev-loop:project-evaluator agent to evaluate the current status of the project.

Step 2: After project-evaluator completes, display its summary to the user before proceeding.

Step 3: Use the dev-loop:status-planner agent to plan the remaining work based on the STATUS file from Step 1.

Step 4: After status-planner completes, display its summary and show a final workflow summary:
```
═══════════════════════════════════════
Evaluate & Plan Complete
  STATUS: .agent_planning/STATUS-<ts>.md
  PLAN: .agent_planning/PLAN-<ts>.md
Next: /dev-loop:test-and-implement or /dev-loop:implement-and-iterate
═══════════════════════════════════════
```

