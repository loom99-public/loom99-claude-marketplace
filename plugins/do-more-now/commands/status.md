---
argument-hint: [area of focus]
description: Check the latest status file and tell me what needs to be done
---

Quick project status check. Fast, read-only diagnostic.

<focus-area>
$ARGUMENTS
</focus-area>

## Mode Selection

**If no arguments provided**: Use project-evaluator for full project assessment against planning docs and goals.

**If arguments provided**: Use work-evaluator focused on the specified work area.

---

## No Arguments Mode (Project-Wide Status)

Use the do:project-evaluator agent to evaluate the project.

**Focus on surfacing**:
- Major/fundamental ambiguities
- Missing or incomplete planning documents
- Fundamental unknowns or inconsistencies not yet documented
- Gap analysis against PROJECT_SPEC.md or existing goals

**Output**: STATUS-*.md file with high-level but complete project assessment.

**IMPORTANT**: Do NOT auto-research. Surface issues for user awareness. This is a diagnostic, not a resolution workflow.

**Display summary** with context-dependent next action:

```
═══════════════════════════════════════
Project Status
  STATUS: .agent_planning/STATUS-<ts>.md
  Gaps: [n items] | Ambiguities: [n items]

Next: [context-dependent recommendation]
═══════════════════════════════════════
```

**Next action recommendations**:
- If gaps exist with clear path → "Next: /do:plan to create implementation plan"
- If project appears complete → "Next: Project complete. Review STATUS for polish items."
- If ambiguities found (PAUSE) → "Next: /do:learn to resolve ambiguities in STATUS file"
- If blocked → "Next: Address blockers described in STATUS file"

---

## With Arguments Mode (Focused Work Status)

**Prerequisites**: Check for existing STATUS-*.md or PLAN-*.md files in .agent_planning/

If no planning docs exist:
```
Cannot evaluate specific work - no STATUS or PLAN found.
Run /do:plan first to create evaluation baseline.
Or use /do:status (no args) for full project assessment.
```

If planning docs exist, use the do:work-evaluator agent focused on the specified area.

**Focus on**:
- Runtime validation of the specified work
- Evidence collection (logs, screenshots if applicable, command output)
- Comparison against acceptance criteria from PLAN
- Verdict: COMPLETE, INCOMPLETE, PAUSE, or BLOCKED

**Output**: WORK-EVALUATION-*.md file with focused assessment.

**Display summary** with context-dependent next action:

```
═══════════════════════════════════════
Work Status: [area]
  EVALUATION: .agent_planning/WORK-EVALUATION-<ts>.md
  Verdict: [COMPLETE|INCOMPLETE|PAUSE|BLOCKED]

Next: [context-dependent recommendation]
═══════════════════════════════════════
```

**Next action recommendations**:
- COMPLETE → "Next: Run /do:status (no args) for overall project check"
- INCOMPLETE → "Next: Address issues in evaluation, then /do:status [area]"
- PAUSE → "Next: /do:learn to resolve questions in evaluation"
- BLOCKED → "Next: Resolve blocker described in evaluation"

---

## Philosophy

`/do:status` is the "check engine light" - fast diagnostic that surfaces issues.
`/do:plan` is the "full inspection" - comprehensive planning with auto-research.
`/do:learn` is the "mechanic consultation" - deep research on specific questions.

Keep this command fast and read-only. No file creation beyond STATUS/WORK-EVALUATION outputs.
