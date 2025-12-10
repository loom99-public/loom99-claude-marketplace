---
argument-hint: [version | action]
description: [bump|changelog|notes|tag|publish] Release - versioning, changelog, release notes (stub).
---

Release management. Versioning, changelog, release notes, tagging.

<user-input>$ARGUMENTS</user-input>
<current-command>release</current-command>

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

## Step 3: Execute Post-Commands

If `post_commands` from Step 1 is non-empty, execute each one now using `SlashCommand` tool.
