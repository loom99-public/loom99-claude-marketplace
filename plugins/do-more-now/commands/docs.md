---
argument-hint: [what to document]
description: [readme|api|architecture|changelog] Docs - README, API docs, architecture documentation.
---

Documentation tasks. Create, update, or improve project documentation.

<user-input>$ARGUMENTS</user-input>
<current-command>docs</current-command>

## Step 0: Load Gate Configuration

Load gate config from: command → session → CLAUDE.md → prompt.
See `/do:it` Step 0 for full gate loading logic.

---

## Topic Resolution

Determine what to document:

1. **If `$ARGUMENTS` provided** → Use `$ARGUMENTS` as the topic
2. **If no arguments, check conversation context** → If we were just discussing a subject, document that
3. **If no obvious subject in conversation** → Assess all docs and suggest improvements

Set `main_instructions` to the resolved topic.

---

## Subcommand Detection

**Quick check**: Does `main_instructions` contain `/do:` patterns?

- **If NO** → Proceed
- **If YES** → Invoke `do:route-subcommands` skill first

---

## Main Workflow

### Intent Detection

Using `main_instructions`:

| Intent signals | Action |
|----------------|--------|
| "readme", "README" | Update/create README.md |
| "api", "API docs" | Generate/update API documentation |
| "architecture", "arch" | Update ARCHITECTURE.md or create diagrams |
| "changelog", "CHANGELOG" | Update CHANGELOG.md |
| "contributing", "CONTRIBUTING" | Update CONTRIBUTING.md |
| *(default)* | Assess docs and suggest improvements |

### Process

**Step 1: Assess**
- Check what documentation exists
- Identify gaps between code and docs
- Check for stale/outdated sections

**Step 2: Update**
Use do:iterative-implementer to:
- Update documentation to match current code
- Add missing sections
- Improve clarity and examples

**Step 3: Verify**
- Ensure code references are accurate
- Check links work
- Verify examples run

### Output

```
═══════════════════════════════════════
Docs Complete
  Updated: [list of files]
  Added: [new sections/files]

  [Summary of changes]
═══════════════════════════════════════
```

---

## Step 3b: Process Decision and Security Gates

After implementer returns, process any logged gates.
See `/do:it` Step 3b for full logic.

Docs typically don't trigger security-gate (documentation only).

---

## Post-Commands

If `route-subcommands` returned `post_commands`, execute each one now:

**For each command in post_commands**:
- Use the `SlashCommand` tool
- Format: `<command> <main_instructions>`
- Example: If post_commands = `["/do:chores"]` and main_instructions = `"document API"`, execute:
  ```
  SlashCommand("/do:chores document API")
  ```

**Important**: Append main_instructions to preserve context for downstream commands.

---

## Step 4: Checkpoint Gate

After documentation updates complete, process `checkpoint-gate` per config.
See `/do:it` Step 4 for checkpoint handling logic.

For docs commands, checkpoint presents:
- Files updated/created
- Sections added or modified
