---
argument-hint: [what to document]
description: Docs - README, API docs, architecture documentation.
---

Documentation tasks. Create, update, or improve project documentation.

<doc-input>
$ARGUMENTS
</doc-input>

## Subcommand Detection

If $ARGUMENTS contains any `/do:` command reference (e.g., `/do:plan`, `/do:it`), run that command first with its relevant arguments, then continue with this command's main workflow.

---

## Intent Detection

| Intent signals | Action |
|----------------|--------|
| "readme", "README" | Update/create README.md |
| "api", "API docs" | Generate/update API documentation |
| "architecture", "arch" | Update ARCHITECTURE.md or create diagrams |
| "changelog", "CHANGELOG" | Update CHANGELOG.md |
| "contributing", "CONTRIBUTING" | Update CONTRIBUTING.md |
| *(default)* | Assess docs and suggest improvements |

## Process

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

## Output

```
═══════════════════════════════════════
Docs Complete
  Updated: [list of files]
  Added: [new sections/files]

  [Summary of changes]
═══════════════════════════════════════
```
