---
argument-hint: [focus area]
description: [init|audit|status|feature|track] Plan & track - evaluate status, create plans, track backlog items.
---

Planning command. Evaluate where we are, plan where we want to be, track work items.

<user-input>
$ARGUMENTS
</user-input>

## Subcommand Detection (REQUIRED)

**STOP. Check $ARGUMENTS for any `/do:` command references.**

If $ARGUMENTS contains `/do:it`, `/do:explore`, `/do:research`, `/do:chores`, `/do:docs`, or `/do:release`:
1. **IMMEDIATELY** use the SlashCommand tool to run that command first
2. Wait for it to complete
3. Then continue with this command's main workflow below

**Do NOT skip this step. Do NOT proceed to planning until subcommands complete.**

---

## Intent Detection

| Intent signals | Action |
|----------------|--------|
| "init", "new project", "start", "create project" | `do:init-project` skill |
| "audit", "deep dive", "forensic", "comprehensive" | `do:audit` skill |
| "status", "check", "how's it going", "progress" | `do:status-check` skill |
| "feature", "proposal", "new feature", "design" | `do:feature-proposal` skill |
| "track [priority] [type] description" | Quick capture (see below) |
| *(default - any other planning request)* | Evaluate+plan workflow |

**Use the Skill tool** to invoke skills. Otherwise, run workflow below.

---

## Track: Quick Backlog Capture

If input starts with "track", parse and create issue:

- **Priority** (optional): 0-3 (defaults to 2)
- **Type** (optional): bug/feature/task/chore (defaults to task)
- **Description**: everything else

If `mcp__plugin_beads_beads__create` available, create issue. Otherwise:
```
Beads not available. Install beads plugin for tracking.
```

**Output**:
```
Tracked: [description]
  Type: [type] | Priority: P[n]
```

---

## Default: Evaluate + Plan Workflow

**Step 1: Evaluate**
Use do:project-evaluator to assess current state → STATUS-*.md

If evaluator returns PAUSE with ambiguities, use do:researcher to resolve, then re-evaluate.

**Step 1b**: Display evaluator's summary.

**Step 2: Plan**
Use do:status-planner to create implementation plan → PLAN-*.md

**Step 2b**: Display planner's summary.

**Output**:
```
═══════════════════════════════════════
Plan Complete
  STATUS: .agent_planning/STATUS-<ts>.md
  PLAN: .agent_planning/PLAN-<ts>.md
Next: /do:it to implement
═══════════════════════════════════════
```

---

## Beads Sync (Optional)

If beads MCP tools available, sync P0/P1 items after planning.
