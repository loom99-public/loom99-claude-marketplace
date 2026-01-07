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

