---
argument-hint: [version | action]
description: Release - versioning, changelog, release notes (stub).
---

Release management. Versioning, changelog, release notes, tagging.

<release-input>
$ARGUMENTS
</release-input>

## Subcommand Detection

If $ARGUMENTS contains any `/do:` command reference (e.g., `/do:plan`, `/do:it`), run that command first with its relevant arguments, then continue with this command's main workflow.

---

## Status

**STUB** - This command is a placeholder for future implementation.

## Planned Features

| Action | Description |
|--------|-------------|
| `bump [major|minor|patch]` | Bump version number |
| `changelog` | Generate/update CHANGELOG from commits |
| `notes` | Generate release notes |
| `tag` | Create git tag for release |
| `publish` | Full release workflow |

## Current Behavior

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
