---
argument-hint: [version | action]
description: Release - versioning, changelog, release notes (stub).
---

Release management. Versioning, changelog, release notes, tagging.

<release-input>
$ARGUMENTS
</release-input>

## Subcommand Detection (REQUIRED)

**STOP. Check $ARGUMENTS for any `/do:` command references.**

If $ARGUMENTS contains `/do:plan`, `/do:it`, `/do:explore`, `/do:research`, `/do:chores`, or `/do:docs`:
1. **IMMEDIATELY** use the SlashCommand tool to run that command first
2. Wait for it to complete
3. Then continue with this command's main workflow below

**Do NOT skip this step.**

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
