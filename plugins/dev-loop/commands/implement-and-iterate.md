---
argument-hint: [area of focus]
description: Implement functionality iteratively through implementation and evaluation cycles. Focuses on working software without requiring tests upfront.
---

IMPORTANT: if "$1" is set to "plan-first" you MUST run this slash command first:
/evaluate-and-plan $ARGUMENTS

If specific areas of focus are defined below, focus entirely on those goals. If 'specific-areas-of-focus' is empty, use the latest STATUS and PLAN files.

Specific areas of focus:
<specific-areas-of-focus>
$ARGUMENTS
</specific-areas-of-focus>

This command integrates with `/evaluate-and-plan`. If no STATUS and PLAN files exist in .agent_planning for the current goal, run `/evaluate-and-plan $ARGUMENTS` first.

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

**Step 2: Evaluate**
Use the dev-loop:work-evaluator agent to assess if goals are achieved. The agent will:
- Run the software
- Collect evidence (screenshots, logs, output)
- Compare against acceptance criteria
- Determine: COMPLETE or INCOMPLETE

**Exit Condition**:
When work-evaluator confirms all goals achieved (status: COMPLETE), exit the loop and proceed to final step.

**Continue Condition**:
If work-evaluator reports INCOMPLETE and the path forward is clear (concrete next steps identified), continue the loop.

**Blocked Condition**:
If work-evaluator reports blockers with no clear path forward, pause and request user guidance.

### Final Step

After loop completion, run `/evaluate-and-plan $ARGUMENTS` to update STATUS and PLAN with current implementation state.

## Important Notes

- This workflow does not require tests to be written first
- Validation happens through manual testing and runtime evaluation
- Work-evaluator uses actual software execution to verify functionality
- Quality standards are maintained through iterative-implementer's engineering practices
- User may test and provide feedback during any iteration
