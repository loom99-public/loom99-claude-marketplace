### DO NOT MODIFY - FOR REFERENCE PURPOSES ###

---
argument-hint: [area of focus]
description: Write tests and then implement. Pass args to focus on something specific, or Claude will automatically use the most recent planning docs. Designed to work with /dev-loop:evaluate-and-plan. Pass 'plan-first' to tell Claude to run an initial /dev-loop:valuate-and-plan cycle.
---

IMPORTANT: if "$1" is set to "plan-first" you MUST run this slash command first:
/dev-loop:evaluate-and-plan $ARGUMENTS

If specific areas of focus are defined below, focus entirely on those goals and architectural work to enable those goals.  If 'specific-areas-of-focus' is empty OR only contains 'plan-first', use the latest STATUS and PLAN files

Specific areas of focus:
<specific-areas-of-focus>
$ARGUMENTS
</specific-areas-of-focus>

This command integrates with the `/dev-loop:evaluate-and-plan` slash command. If there are no existing STATUS and PLAN files in the .agent_planning dir for our current goal, run the slash command `/dev-loop:evaluate-and-plan $ARGUMENTS` first.

This command runs two core loops: TestLoop and ImplementLoop. Each loop is repeated until the condition is satisfied. CRITICAL: ALL LOOPS END WITH AN 'EVALUATE' STEP.

Tests MUST be (TestCriteria):
<TestCriteria>
- useful (no useless tests)
- complete (test all edge cases)
- flexible (they should allow refactoring of implementation details without changing tests, where possible)
- Fully automated
- All tests MUST be AUTOMATED
  - using either the existing testing framework defined in the project OR
  - using a STANDARD framework for the framework/language/tools under test.
  - DO NOT implement ad-hoc tests in a non-standard way.
- If more information is required, ask!
</TestCriteria>

<TestLoop>
**Step 1: Design and write tests**
Use the dev-loop:functional-tester agent to design and write high-level functional tests that validate real user workflows and follow all TestCriteria. Upon subsequent loops, iterate on tests to meet TestCriteria.

**Step 1b: Display results** - Show functional-tester's summary to user before proceeding.

**Step 2: Evaluate tests**
Use the dev-loop:project-evaluator agent to evaluate ONLY THE RESULT OF STEP 1 (the tests just written). Evaluate in context of the plan to ensure they follow TestCriteria.

**Step 2b: Display results** - Show project-evaluator's summary and loop decision to user.

**Step 2c: Handle PAUSE (if applicable)**
If project-evaluator returns PAUSE with ambiguities about test design:
1. Use dev-loop:researcher to explore the testing question (e.g., what to test, how to structure, what's appropriate scope)
2. Use project-evaluator (research evaluation mode) to assess if research is sufficient
3. If sufficient, project-evaluator makes the decision
4. Continue TestLoop with resolved ambiguity

<LoopExitCondition>
When TestCriteria are met with NO EXCEPTIONS, exit the loop and proceed
</LoopExitCondition>

<LoopContinueCondition>
If tests don't meet TestCriteria, restart the loop with specific feedback.
</LoopContinueCondition>
</TestLoop>

ONLY proceed after the first loop has been completed and the 'evaluate' step confirms that we have properly implemented the tests according to the TestCriteria.  If this is not the case, restart TestLoop.

<ImplementLoop>
**Step 1: Implement**
Use the dev-loop:test-driven-implementer agent to implement the functionality that makes these tests pass.

**Step 1b: Display results** - Show test-driven-implementer's summary (tests passing/failing, files, commits) to user.

**Step 2: Evaluate implementation**
Use the dev-loop:work-evaluator agent to evaluate ONLY THE RESULT OF STEP 1 (the current implementation).

**Step 2b: Display results** - Show work-evaluator's summary and loop decision to user.

**Step 2c: Handle PAUSE (if applicable)**
If work-evaluator returns PAUSE with ambiguities about implementation:
1. Use dev-loop:researcher to explore the specific technical question
2. Use work-evaluator (research evaluation mode) to assess if research is sufficient
3. If sufficient, work-evaluator makes the decision
4. Continue ImplementLoop with resolved ambiguity

<LoopExitCondition>
There are no outstanding issues for which the solution is well defined / little to no ambiguity.
</LoopExitCondition>

<LoopContinueCondition>
If there are known outstanding issues and the solution is well defined, restart the ImplementLoop.
</LoopContinueCondition>
</ImplementLoop>

**FINAL STEP**: AFTER we have run BOTH TestLoop and ImplementLoop to completion, run the command `/dev-loop:evaluate-and-plan $ARGUMENTS` to ensure we have up to date planning and status documents.

Then display a final summary:
```
═══════════════════════════════════════
Test & Implement Complete
  TestLoop: n iterations | ImplementLoop: m iterations
  Tests: all passing | Files: [count] | Commits: [count]
  Research: [n decisions made OR "none needed"]
Next: Review STATUS/PLAN or continue development
═══════════════════════════════════════
```

## Important Notes

- **PAUSE triggers automatic research** - evaluators can trigger research to resolve ambiguities
- User only involved if research cannot resolve after 3 iterations
- Both loops must complete before final evaluation
