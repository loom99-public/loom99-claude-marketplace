---
argument-hint: [init|audit|status|feature] [focus area]
description: Planning & evaluation. Default evaluates+plans. Modes: init (new project), audit (deep dive), status (quick check), feature (proposal).
---

Unified planning command. Detects mode from first argument.

<user-input>
$ARGUMENTS
</user-input>

## Mode Detection

Parse the first word of arguments to determine mode:

| First word | Mode | Action |
|------------|------|--------|
| `init` | Initialize | Create new project spec via project-architect |
| `audit` | Deep audit | Exhaustive evaluation via project-evaluator (audit mode) |
| `status` | Quick status | Fast diagnostic via project-evaluator or work-evaluator |
| `feature` | Feature proposal | Design new feature via product-visionary |
| *(anything else)* | Default | Full evaluate + plan cycle |

Extract the remaining arguments after the mode keyword as the focus area.

---

## Mode: Initialize (`init`)

**Trigger**: `/do2:plan init [project description]`

Transform user intent into concrete project foundation.

**Step 1**: Use do2:project-architect agent with the project description.
The architect conducts adaptive interview (15-25 questions), generates PROJECT_SPEC.md.

**Step 2**: Display summary and recommend `/do2:plan` to start implementation planning.

---

## Mode: Audit (`audit`)

**Trigger**: `/do2:plan audit [area]`

Exhaustive, in-depth evaluation. Full forensic examination.

**Step 1**: Use do2:project-evaluator agent in **audit mode**:
- If no area specified: audit entire project (architecture, quality, deps, security, docs, debt)
- If area specified: focused deep dive on that area

**Step 2**: Generate AUDIT-*.md with comprehensive findings, problem inventory (P0-P3).

**Step 3**: Display summary with critical findings.

---

## Mode: Status (`status`)

**Trigger**: `/do2:plan status [area]`

Quick diagnostic. Fast, read-only check.

**Step 1**: Determine scope:
- No area: Use do2:project-evaluator for high-level project assessment
- With area: Use do2:work-evaluator focused on that area

**Step 2**: Output STATUS-*.md or WORK-EVALUATION-*.md.

**Step 3**: Display verdict (COMPLETE, INCOMPLETE, BLOCKED, etc.) and key findings.

---

## Mode: Feature Proposal (`feature`)

**Trigger**: `/do2:plan feature [description]`

Design high-value features.

**Step 1**: Use do2:product-visionary agent with the feature description.

**Step 2**: Generate feature proposal document.

**Step 3**: Display summary, recommend `/do2:plan` to incorporate into roadmap.

---

## Mode: Default (Evaluate + Plan)

**Trigger**: `/do2:plan [focus area]` or `/do2:plan`

Full evaluation and planning cycle.

**Step 1: Evaluate**
Use do2:project-evaluator to assess current state.
- Generates STATUS-*.md with gap analysis
- If PAUSE with ambiguities: use do2:researcher to resolve, then re-evaluate

**Step 1b**: Display evaluator's summary before proceeding.

**Step 2: Plan**
Use do2:status-planner to create implementation plan.
- Generates PLAN-*.md with prioritized backlog
- Archives stale planning docs

**Step 2b**: Display planner's summary.

**Final output**:
```
═══════════════════════════════════════
Plan Complete
  STATUS: .agent_planning/STATUS-<ts>.md
  PLAN: .agent_planning/PLAN-<ts>.md
Next: /do2:it to implement
═══════════════════════════════════════
```

---

## Beads Sync (Optional)

If `mcp__plugin_beads_beads__*` tools are available after planning:
- Sync P0/P1 items from PLAN to beads
- This is optional enhancement - skip silently if unavailable
