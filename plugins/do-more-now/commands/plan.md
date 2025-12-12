---
argument-hint: [focus area]
description: [init|audit|status|feature|track] Plan & track - evaluate status, create plans, track backlog items.
---

Planning command. Evaluate where we are, plan where we want to be, track work items.

<user-input>$ARGUMENTS</user-input>
<current-command>plan</current-command>

## Step 0: Load Gate Configuration

Load gate config from: command → session → CLAUDE.md → prompt.
See `/do:it` Step 0 for full gate loading logic.

Write config to `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.yaml`.

---

## Topic Resolution

Determine what to plan:

1. **If `$ARGUMENTS` provided** → Use `$ARGUMENTS` as the topic
2. **If no arguments, check conversation context** → If we were just discussing a subject, that subject is the topic
3. **If no obvious subject in conversation** → Run general project evaluation (no specific focus)

Set `main_instructions` to the resolved topic.

---

## Subcommand Detection

**Quick check**: Does `main_instructions` contain `/do:` patterns (other than the current command)?

- **If NO** → Proceed to Intent Detection
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

**Examples**:
- `track fix login bug` → type: bug, priority: 2, title: "fix login bug"
- `track 0 security vulnerability in auth` → type: task, priority: 0, title: "security vulnerability in auth"
- `track feature 1 add dark mode` → type: feature, priority: 1, title: "add dark mode"

**Parse order**: Check for priority (0-4), then type keyword, then rest is description.

```bash
bd create "<description>" \
  --description="Created via /do:plan track" \
  -t <type> -p <priority> --json
bd sync
```

If bd command fails:
```
Beads not available. Install beads plugin for tracking.
```

**Output**:
```
Tracked: [description]
  Type: [type] | Priority: P[n] | ID: bd-xxx
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

If `route-subcommands` returned `post_commands`, execute each one now:

**For each command in post_commands**:
- Use the `SlashCommand` tool
- Format: `<command> <main_instructions>`
- Example: If post_commands = `["/do:chores"]` and main_instructions = `"plan feature"`, execute:
  ```
  SlashCommand("/do:chores plan feature")
  ```

**Important**: Append main_instructions to preserve context for downstream commands.

---

## Step 3: Checkpoint Gate

After workflow completes, process `checkpoint-gate` per config.
See `/do:it` Step 4 for checkpoint handling logic.

For planning commands, checkpoint presents:
- STATUS file summary - verify assessment accuracy
- PLAN file summary - verify priorities and approach

---

## Beads Integration

**Division of Labor**:
- `.agent_planning/` docs → Strategy, evaluations, research, ARDs, architecture decisions
- Beads (`bd`) → Concrete work items: stories, bugs, tasks, epics, dependencies

### At Command Start

Check existing beads state for context:
```bash
bd ready --json       # What's unblocked?
bd stale --days 14    # What's been forgotten?
bd list --status in_progress --json  # What's active?
```

Include counts in status output.

### After Planning Completes

The status-planner agent handles syncing PLAN items to beads. Verify sync:
```bash
bd list --json | head -20  # Check issues were created
bd blocked --json          # Verify dependency structure
```

### Session End

```bash
bd sync  # Force immediate export/commit/push
```

**Graceful Degradation**: If beads unavailable, planning docs remain authoritative. Workflow continues normally.
