---
argument-hint: [area of focus] [tdd|iterate]
description: Implement functionality. Auto-selects TDD or iterative mode. Pass 'tdd' or 'iterate' to override.
---

IMPORTANT: if "$1" is set to "plan-first" run `/do:plan $ARGUMENTS` first.

If 'specific-areas-of-focus' is empty, use the latest STATUS and PLAN files.

Specific areas of focus:
<specific-areas-of-focus>
$ARGUMENTS
</specific-areas-of-focus>

Integrates with `/do:plan`. If no STATUS and PLAN files exist in .agent_planning, run `/do:plan $ARGUMENTS` first.

## Mode Selection

Check $ARGUMENTS for mode hint:
- Contains 'tdd' → TDD workflow
- Contains 'iterate' → Iterative workflow
- Otherwise → Auto-select: existing test framework or API/logic = TDD, UI/visual = iterative

---

## TDD Workflow

Runs two loops: TestLoop and ImplementLoop. ALL LOOPS END WITH AN 'EVALUATE' STEP.

Tests MUST be (TestCriteria):
- useful, complete, flexible
- Fully automated using standard framework
- No ad-hoc tests

<TestLoop>
**Step 1: Design and write tests**
Use do:functional-tester to design and write high-level functional tests.

**Step 1b: Display results** to user.

**Step 2: Evaluate tests**
Use do:project-evaluator to evaluate tests meet TestCriteria.

**Step 2b: Display results** and loop decision.

**Step 2c: Handle PAUSE** - Use do:researcher if ambiguities, then project-evaluator to assess.  After do:researcher and exiting the loop, ALWAYS continue to implementation phase!

<LoopExitCondition>TestCriteria met with NO EXCEPTIONS</LoopExitCondition>
<LoopContinueCondition>Tests don't meet criteria → restart with feedback</LoopContinueCondition>
</TestLoop>

ONLY proceed after TestLoop completes and evaluate confirms proper tests.

<ImplementLoop>
**Step 1: Implement**
Use do:test-driven-implementer to make tests pass.

**Step 1b: Display results** (tests passing/failing, files, commits).

**Step 2: Evaluate implementation**
Use do:work-evaluator to evaluate implementation.

**Step 2b: Display results** and loop decision.

**Step 2c: Handle PAUSE** - Use do:researcher if ambiguities.  ALWAYS continue to another implementation phase if we do research.

<LoopExitCondition>No outstanding issues with well-defined solutions</LoopExitCondition>
<LoopContinueCondition>Known issues with defined solution → restart</LoopContinueCondition>
</ImplementLoop>

---

## Iterative Workflow

Runs implementation-evaluation cycle until goals achieved.

**Step 1: Implement**
Use do:iterative-implementer to build incrementally:
- Read STATUS/PLAN for context
- Implement working functionality
- Commit frequently

**Step 1b: Display results** (completed items, files, commits).

**Step 2: Evaluate**
Use do:work-evaluator to assess goals:
- Run software, collect evidence
- Compare against acceptance criteria
- Determine: COMPLETE, INCOMPLETE, PAUSE, or BLOCKED

**Step 2b: Display results** and loop decision.

**Loop Conditions**:
- COMPLETE → Exit, proceed to final step
- INCOMPLETE with clear path → Continue
- PAUSE → Use do:researcher, then work-evaluator to assess
- BLOCKED → Pause, request user guidance

---

## Final Step

After loops complete, run `/do:plan $ARGUMENTS` to update status.

Display summary:
```
═══════════════════════════════════════
Implementation Complete
  Mode: [TDD|Iterative] | Iterations: n
  Files: [count] | Commits: [count]
  Research: [n decisions OR "none needed"]
Next: Review STATUS/PLAN or continue
═══════════════════════════════════════
```

## Execution Summary (Final Step)

After all agents complete:
1. Read `.agent_planning/.exec/CURRENT_EXECUTION_ID.txt` to get execution ID
2. If exists, invoke do:execution-summarizer agent to aggregate PARTIAL files into an EXEC report
3. Display the executive summary from the generated EXEC report
4. Show file path to full report

**Display format**:
```
═══════════════════════════════════════
Execution Summary: <EXECUTION_ID>
  Agents: [count] | Duration: [approx]

[Executive summary from EXEC report - 2-3 sentences]

Full report: .agent_planning/EXEC-it-<timestamp>.md
═══════════════════════════════════════
```

If state files don't exist, skip this step (non-tracked execution).

## Notes

- PAUSE triggers automatic research - user only involved after 3 failed iterations
- Both TDD loops must complete before final evaluation
- Validation through tests (TDD) or runtime evidence (iterative)
