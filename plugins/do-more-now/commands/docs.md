---
argument-hint: [what to document]
description: [readme|api|architecture|changelog] Docs - README, API docs, architecture documentation.
---

Documentation tasks. Create, update, or improve project documentation.

<user-input>$ARGUMENTS</user-input>
<current-command>docs</current-command>

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

## Step 3: Execute Post-Commands

If `post_commands` from Step 1 is non-empty, execute each one now using `SlashCommand` tool.
