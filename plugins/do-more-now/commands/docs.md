---
argument-hint: [what to document]
description: [readme|api|architecture|changelog] Docs - README, API docs, architecture documentation.
---

Documentation tasks. Create, update, or improve project documentation.

<user-input>$ARGUMENTS</user-input>
<current-command>docs</current-command>

## Subcommand Detection

**Quick check**: Does `$ARGUMENTS` contain `/do:` patterns?

- **If NO** → `main_instructions = $ARGUMENTS`, proceed
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

## Post-Commands

If subcommands were detected and `post_commands` is non-empty, execute them now.
