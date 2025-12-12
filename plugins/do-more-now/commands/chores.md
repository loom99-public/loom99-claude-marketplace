---
argument-hint: [quick|thorough|git|planning|dead-code|deps|debt]
description: [quick|thorough|git|planning|dead-code|deps|debt] Chores - maintenance, cleanup, housekeeping.
---

Maintenance and housekeeping. Cleanup of any sort.

<user-input>$ARGUMENTS</user-input>
<current-command>chores</current-command>

## Step 0: Load Gate Configuration

Load gate config from: command → session → CLAUDE.md → prompt.
See `/do:it` Step 0 for full gate loading logic.

---

## Topic Resolution

Determine scope of chores:

1. **If `$ARGUMENTS` provided** → Use `$ARGUMENTS` to determine chore type/scope
2. **If no arguments, check conversation context** → If we were just discussing a subject, scope chores to that area
3. **If no obvious subject in conversation** → Run quick chores (default)

Set `main_instructions` to the resolved scope.

---

## Subcommand Detection

**Quick check**: Does `main_instructions` contain `/do:` patterns?

- **If NO** → Proceed
- **If YES** → Invoke `do:route-subcommands` skill first

---

## Main Workflow

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

## Step 3b: Process Decision and Security Gates

After implementer returns, process any logged gates.
See `/do:it` Step 3b for full logic.

Chores may trigger security-gate when:
- Updating dependencies
- Removing secrets/credentials from code
- Modifying config files

---

## Post-Commands

If `route-subcommands` returned `post_commands`, execute each one now:

**For each command in post_commands**:
- Use the `SlashCommand` tool
- Format: `<command> <main_instructions>`
- Example: If post_commands = `["/do:docs"]` and main_instructions = `"cleanup"`, execute:
  ```
  SlashCommand("/do:docs cleanup")
  ```

**Important**: Append main_instructions to preserve context for downstream commands.

---

## Step 4: Checkpoint Gate

After chores complete, process `checkpoint-gate` per config.
See `/do:it` Step 4 for checkpoint handling logic.

For chores commands, checkpoint presents:
- Items cleaned up
- Issues fixed
- Items added to backlog
