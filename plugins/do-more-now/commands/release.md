---
argument-hint: [version | action]
description: [bump|changelog|notes|tag|publish] Release - versioning, changelog, release notes (stub).
---

Release management. Versioning, changelog, release notes, tagging.

<user-input>$ARGUMENTS</user-input>
<current-command>release</current-command>

## Subcommand Detection

**Quick check**: Does `$ARGUMENTS` contain `/do:` patterns?

- **If NO** → `main_instructions = $ARGUMENTS`, proceed
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

If subcommands were detected and `post_commands` is non-empty, execute them now.
