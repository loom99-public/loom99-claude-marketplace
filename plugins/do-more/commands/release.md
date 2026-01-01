---
argument-hint: [version | action]
description: [bump|changelog|notes|tag|publish] Release - versioning, changelog, release notes (stub).
---

Release management. Versioning, changelog, release notes, tagging.

<user-input>$ARGUMENTS</user-input>
<current-command>release</current-command>

## Topic Resolution

Determine release scope:

1. **If `$ARGUMENTS` provided** → Use `$ARGUMENTS` as the release action/version
2. **If no arguments, check conversation context** → If we were just discussing a release, use that context
3. **If no obvious subject in conversation** → Show release status and prompt for action

Set `main_instructions` to the resolved scope.

---

## Subcommand Detection

**Quick check**: Does `main_instructions` contain `/do:` patterns?

- **If NO** → Proceed
- **If YES** → Invoke `do:route-subcommands` skill first

---

## Main Workflow

### Status

**STUB** - This command is a placeholder for future implementation.

### Planned Features

| Action | Description |
|--------|-------------|
| `bump [major|minor|patch]` | Bump version number |
| `changelog` | Generate/update CHANGELOG from commits |
| `notes` | Generate release notes |
| `tag` | Create git tag for release |
| `publish` | Full release workflow |

### Current Behavior

```
═══════════════════════════════════════
Release (Stub)
  Status: Not yet implemented

  This command will handle:
  - Version bumping
  - Changelog generation
  - Release notes
  - Git tagging

  For now, use manual release workflow.
═══════════════════════════════════════
```

---

## Post-Commands

If `route-subcommands` returned `post_commands`, execute each one now:

**For each command in post_commands**:
- Use the `SlashCommand` tool
- Format: `<command> <main_instructions>`
- Example: If post_commands = `["/do:chores"]` and main_instructions = `"release v1.0"`, execute:
  ```
  SlashCommand("/do:chores release v1.0")
  ```

**Important**: Append main_instructions to preserve context for downstream commands.
