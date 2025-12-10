---
argument-hint: [quick|thorough|git|planning|dead-code|deps|debt]
description: [quick|thorough|git|planning|dead-code|deps|debt] Chores - maintenance, cleanup, housekeeping.
---

Maintenance and housekeeping. Cleanup of any sort.

<user-input>$ARGUMENTS</user-input>
<current-command>chores</current-command>

## Step 1: Route Subcommands (REQUIRED)

**Invoke `do:route-subcommands` skill FIRST.**

This skill will:
1. Analyze `$ARGUMENTS` for any `/do:*` commands
2. Execute pre-commands (commands that should run before main workflow)
3. Return `main_instructions` and `post_commands`

If no subcommands found, it returns immediately with `main_instructions = $ARGUMENTS`.

**Store the returned `post_commands` for later.**

---

## Step 2: Main Workflow

### Modes

Using `main_instructions`:

| Mode | Trigger | Duration | Scope |
|------|---------|----------|-------|
| **Quick** | default, "quick" | 5-10 min | Git hygiene, planning cleanup, quick code scan |
| **Thorough** | "thorough", "deep" | 20-40 min | All quick + dead code, doc sync, tech debt |
| **Specific** | chore name | varies | Single chore type |

**Specific chores**: `git`, `planning`, `dead-code`, `deps`, `debt`, `docs`

### Process

Use do:iterative-implementer to execute chores.
- If there are minor issues or standard tasks to tidy up, do them immediately.
- If there are larger concerns or a large amount of ambiguity, use /do:plan track to add an item to the backlog (print in summary)

**Quick chores**:
- Git hygiene (clean status, stale branches)
- Planning file cleanup (archive old STATUS/PLAN)
- Quick code scan (TODOs, debug code, secrets)
- Dependency quick check

**Thorough chores**:
- All quick chores AND
- Dead code detection
- Documentation sync
- Technical debt inventory
- Actually fix simple issues found

### Output

Use subagent do:execution-summarizer to generate summary of work completed.

```
═══════════════════════════════════════
Chores Complete ([quick | thorough | specific])
  Cleaned up:
   - [list items cleaned up]
  Fixed:
   - [list issues]
  Addl work tracked:
    - [list items]
  Flagged:
    - [list items]

  [Summary of what was done]
═══════════════════════════════════════
```

---

## Step 3: Execute Post-Commands

If `post_commands` from Step 1 is non-empty, execute each one now using `SlashCommand` tool.
