### DO NOT MODIFY - FOR REFERENCE PURPOSES ###

---
argument-hint: [area of focus]
description: Evaluate the project and make an implementation plan.  Pass args to focus on something specific, or let Claude decide.  Designed to work with /dev-loop:test-and-implement
---

If specific areas of focus are defined below, focus entirely on those goals and architectural work to enable those goals.  If 'specific-areas-of-focus' is empty, use the PROJECT_SPEC.md file to evaluate the project as a whole.

Specific areas of focus:
<specific-areas-of-focus>
$ARGUMENTS
</specific-areas-of-focus>

## Workflow

**Step 1: Evaluate**
Use the dev-loop:project-evaluator agent to evaluate the current status of the project.

**Step 1b: Display results** - Show project-evaluator's summary to user before proceeding.

**Step 1c: Handle PAUSE (if applicable)**
If project-evaluator returns **PAUSE** with ambiguities that need resolution:
1. For each significant ambiguity identified, use the dev-loop:researcher agent to explore options
2. Use project-evaluator (research evaluation mode) to assess if research is sufficient
3. If sufficient, project-evaluator makes the decision and documents it
4. Continue to planning with resolved ambiguities

This auto-research step removes user from the ambiguity resolution loop. Only surface to user if research cannot resolve after 3 iterations.

**Step 2: Plan**
Use the dev-loop:status-planner agent to plan the remaining work based on:
- The STATUS file from Step 1
- Any research decisions from Step 1c (if applicable)

**Step 2b: Display results** - Show status-planner's summary and final workflow summary:
```
═══════════════════════════════════════
Evaluate & Plan Complete
  STATUS: .agent_planning/STATUS-<ts>.md
  PLAN: .agent_planning/PLAN-<ts>.md
  Research: [n decisions made OR "none needed"]
Next: /dev-loop:test-and-implement or /dev-loop:implement-and-iterate
═══════════════════════════════════════
```
