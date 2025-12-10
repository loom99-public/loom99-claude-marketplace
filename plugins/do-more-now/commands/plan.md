---
argument-hint: [focus area]
description: [init|audit|status|feature|track] Plan & track - evaluate status, create plans, track backlog items.
---

Planning command. Evaluate where we are, plan where we want to be, track work items.

<user-input>$ARGUMENTS</user-input>
<current-command>plan</current-command>

## Subcommand Detection

**Quick check**: Does `$ARGUMENTS` contain `/do:` patterns (other than the current command)?

- **If NO** → `main_instructions = $ARGUMENTS`, proceed to Intent Detection
- **If YES** → Invoke `do:route-subcommands` skill, then proceed with returned `main_instructions`

---

## Intent Detection

Analyze `main_instructions`:

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

## Post-Commands

If subcommands were detected earlier and `post_commands` is non-empty, execute them now.

---

## Beads Sync (Optional)

If beads MCP tools available, sync P0/P1 items after planning.
