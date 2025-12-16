---
argument-hint: [refactor|debug|fix|review|test|chores|tdd|iterate] [focus]
description: Implementation & action. Default auto-selects TDD/iterative. Modes: refactor, debug, fix, review, test, chores.
---

Unified implementation command. Detects mode from first argument.

<user-input>
$ARGUMENTS
</user-input>

## Mode Detection

Parse the first word of arguments to determine mode:

| First word | Mode | Action |
|------------|------|--------|
| `refactor` | Refactoring | Safe code restructuring without behavior change |
| `debug` | Debug | Root cause investigation for bugs/issues |
| `fix` | Fix | Bug fix workflow with verification |
| `review` | Review | Code review / quality assessment |
| `test` | Test | Add tests to existing untested code |
| `chores` | Chores | Maintenance tasks (cleanup, deps, debt) |
| `tdd` | TDD | Explicit TDD workflow |
| `iterate` | Iterative | Explicit iterative workflow |
| *(anything else)* | Default | Auto-select TDD or iterative based on context |

Extract remaining arguments after mode keyword as the focus area.

---

## Mode: Refactor

**Trigger**: `/do2:it refactor [what to refactor]`

Safe code restructuring. No behavior changes, just improved structure.

**Step 1**: Use do2:project-evaluator to understand current structure and identify refactoring targets.

**Step 2**: Use do2:iterative-implementer in **refactor mode**:
- Make incremental structural changes
- Run existing tests after each change to verify no behavior change
- Commit frequently with clear refactoring messages

**Step 3**: Use do2:work-evaluator to verify:
- All existing tests still pass
- No functionality changed
- Code quality improved

**Loop** until work-evaluator confirms COMPLETE.

---

## Mode: Debug

**Trigger**: `/do2:it debug [symptom or bug description]`

Systematic root cause investigation.

**Step 1**: Use do2:researcher in **debug mode**:
- Gather information about the symptom
- Search codebase for relevant code paths
- Identify potential causes
- Form hypotheses

**Step 2**: Use do2:work-evaluator to test hypotheses:
- Add logging/debugging if needed
- Run the code to gather evidence
- Narrow down root cause

**Step 3**: Once root cause identified, display findings:
```
═══════════════════════════════════════
Debug Investigation Complete
  Symptom: [original description]
  Root Cause: [identified cause]
  Location: [file:line]

  Suggested fix: [brief description]
Next: /do2:it fix [description] to implement fix
═══════════════════════════════════════
```

---

## Mode: Fix

**Trigger**: `/do2:it fix [bug description or issue reference]`

Bug fix workflow with verification.

**Step 1**: If not already debugged, use do2:researcher to understand the bug.

**Step 2**: Use do2:iterative-implementer to:
- Write a failing test that reproduces the bug (if testable)
- Implement the fix
- Verify the test passes
- Check for regressions

**Step 3**: Use do2:work-evaluator to confirm fix is complete and no regressions.

---

## Mode: Review

**Trigger**: `/do2:it review [what to review - PR, file, recent changes]`

Code review / quality assessment.

**Step 1**: Use do2:project-evaluator in **review mode**:
- If PR/diff specified: review those changes
- If file specified: review that file
- If no target: review recent uncommitted changes

**Step 2**: Generate review with:
- Code quality assessment
- Potential bugs or issues
- Security concerns
- Suggestions for improvement
- Overall verdict (approve, request changes, concerns)

**Step 3**: Display review summary inline, full details in REVIEW-*.md if extensive.

---

## Mode: Test

**Trigger**: `/do2:it test [what to test]`

Add tests to existing untested code. NOT TDD - this is retroactive testing.

**Step 1**: Use do2:project-evaluator to identify untested code in the target area.

**Step 2**: Use do2:functional-tester to design and write tests:
- Focus on real user workflows
- Verify actual behavior (not implementation details)
- Aim for meaningful coverage, not 100%

**Step 3**: Use do2:work-evaluator to verify tests:
- Tests pass against current code
- Tests would fail if functionality broke
- No tautological or useless tests

---

## Mode: Chores

**Trigger**: `/do2:it chores [quick|thorough] [specific]`

Maintenance and housekeeping.

**Quick mode** (default if no modifier):
- Git hygiene (clean status, untracked files)
- Planning file cleanup
- Quick code scan (TODOs, debug code)
- Dependency quick check

**Thorough mode** (`/do2:it chores thorough`):
- All quick chores plus:
- Dead code detection
- Documentation sync
- Technical debt inventory
- Actually fix simple issues found

**Specific chore** (`/do2:it chores [git|planning|dead-code|deps|debt]`):
- Focus on just that area

---

## Mode: TDD (Explicit)

**Trigger**: `/do2:it tdd [what to implement]`

Test-Driven Development workflow. Tests first, then implement.

**TestLoop** (max 3 iterations):

1. **Design tests**: Use do2:functional-tester to write failing tests
2. **Evaluate tests**: Use do2:project-evaluator to verify tests meet criteria (useful, complete, un-gameable)
3. **Loop** until tests are sufficient

**ImplementLoop** (until complete):

1. **Implement**: Use do2:test-driven-implementer to make tests pass
2. **Evaluate**: Use do2:work-evaluator to assess implementation
3. **Loop** until no outstanding issues

---

## Mode: Iterative (Explicit)

**Trigger**: `/do2:it iterate [what to implement]`

Iterative implementation with runtime validation.

**Loop** (until complete):

1. **Implement**: Use do2:iterative-implementer to build incrementally
2. **Evaluate**: Use do2:work-evaluator to validate with runtime evidence
3. **Loop** until work-evaluator returns COMPLETE

---

## Mode: Default (Auto-Select)

**Trigger**: `/do2:it [what to implement]`

Auto-select TDD or iterative based on context:
- Existing test framework + API/logic work → TDD
- UI/visual work or no test framework → Iterative

Then proceed with the selected workflow.

---

## Final Output

After any mode completes:
```
═══════════════════════════════════════
Implementation Complete
  Mode: [mode name] | Iterations: n
  Files: [count] | Commits: [count]
Next: /do2:plan to update status
═══════════════════════════════════════
```

---

## Beads Sync (Optional)

If `mcp__plugin_beads_beads__*` tools available after implementation:
- Update relevant beads issue status (COMPLETE→close, etc.)
- Skip silently if unavailable
