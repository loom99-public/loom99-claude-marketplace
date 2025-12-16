### DO NOT MODIFY - FOR REFERENCE PURPOSES ###

---
argument-hint: [area of focus]
description: Implement functionality iteratively through implementation and evaluation cycles. Focuses on working software without requiring tests upfront.
---

IMPORTANT: if "$1" is set to "plan-first" you MUST run this slash command first:
/dev-loop:evaluate-and-plan $ARGUMENTS

If specific areas of focus are defined below, focus entirely on those goals. If 'specific-areas-of-focus' is empty, use the latest STATUS and PLAN files.

Specific areas of focus:
<specific-areas-of-focus>
$ARGUMENTS
</specific-areas-of-focus>

This command integrates with `/dev-loop:evaluate-and-plan`. If no STATUS and PLAN files exist in .agent_planning for the current goal, run `/dev-loop:evaluate-and-plan $ARGUMENTS` first.

## Implementation Loop

This command runs an implementation-evaluation cycle until goals are achieved.

### Loop Structure

Repeat until complete:

**Step 1: Implement**
Use the dev-loop:iterative-implementer agent to build functionality incrementally. The agent will:
- Read STATUS/PLAN for context
- Implement real, working functionality
- Commit progress frequently
- Update planning documents

**Step 1b: Display results** - Show iterative-implementer's summary (completed items, files, commits) to user.

**Step 2: Evaluate**
Use the dev-loop:work-evaluator agent to assess if goals are achieved. The agent will:
- Run the software
- Collect evidence (screenshots, logs, output)
- Compare against acceptance criteria
- Determine: COMPLETE, INCOMPLETE, PAUSE, or BLOCKED

**Step 2b: Display results** - Show work-evaluator's summary and loop decision to user.

### Loop Conditions

**Exit Condition (COMPLETE)**:
When work-evaluator confirms all goals achieved (status: COMPLETE), exit the loop and proceed to final step.

**Continue Condition (INCOMPLETE)**:
If work-evaluator reports INCOMPLETE and the path forward is clear (concrete next steps identified), continue the loop.

**Research Condition (PAUSE)**:
If work-evaluator reports PAUSE with ambiguities that need resolution:
1. Use the dev-loop:researcher agent to explore the specific question(s)
2. Use work-evaluator (research evaluation mode) to assess if research is sufficient
3. If sufficient, work-evaluator makes the decision
4. Continue the implementation loop with resolved ambiguity

This auto-research step removes user from the ambiguity resolution loop. Only surface to user if research cannot resolve after 3 iterations.

**Blocked Condition (BLOCKED)**:
If work-evaluator reports BLOCKED with no clear path forward (external dependency, fundamental issue), pause and request user guidance.

### Final Step

After loop completion, run `/dev-loop:evaluate-and-plan $ARGUMENTS` to update STATUS and PLAN with current implementation state.

Then display a final summary:
```
═══════════════════════════════════════
Implement & Iterate Complete
  Iterations: n | Status: [COMPLETE/INCOMPLETE/BLOCKED]
  Files: [count] | Commits: [count] | Goals: n/m achieved
  Research: [n decisions made OR "none needed"]
Next: Review STATUS/PLAN or continue development
═══════════════════════════════════════
```

## Important Notes

- This workflow does not require tests to be written first
- Validation happens through manual testing and runtime evaluation
- Work-evaluator uses actual software execution to verify functionality
- Quality standards are maintained through iterative-implementer's engineering practices
- **PAUSE triggers automatic research** - user only involved if research gets stuck
- User may test and provide feedback during any iteration
