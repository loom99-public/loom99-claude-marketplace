# Evaluation: implement-release-skill

**Generated**: 2026-01-19
**Topic**: Decide whether to implement or remove the stub release skill

## Context

From AUDIT-plugin-workflows-20260118.md (P2 finding):
- `/do:release` command exists but is marked as STUB
- Location: `plugins/do-more/skills/release-skill/SKILL.md`
- The skill explicitly states "STUB - This command is a placeholder for future implementation."

## Current State Analysis

### Existing Infrastructure

| Component | Location | Current Capability |
|-----------|----------|-------------------|
| Version tracking | `plugins/*/.claude-plugin/plugin.json` | Manual version string |
| Marketplace sync | `.claude-plugin/marketplace.json` | Manual sync with plugin versions |
| Bump automation | `justfile` (bump, bump-plugin) | Patch-only increment, updates both files |
| Git tags | None | No tagging workflow |
| Changelog | None | No CHANGELOG.md exists |

### Stub Skill Analysis

The stub defines planned features:

| Action | Description | Overlap with justfile |
|--------|-------------|----------------------|
| `bump [major\|minor\|patch]` | Semantic version bump | Partial (justfile: patch only) |
| `changelog` | Generate CHANGELOG from commits | None |
| `notes` | Generate release notes | None |
| `tag` | Create git tag | None |
| `publish` | Full release workflow | Partial (justfile: bump + reload) |

## Options

### Option A: Full Implementation
- All planned features (bump, changelog, notes, tag, publish)
- Medium effort

### Option B: Remove Stub
- Delete command and skill, users use `just bump`
- Low effort

### Option C: Minimal Wrapper (Recommended)
- Wrap justfile + add changelog/tag only
- Low-Medium effort
- Preserves existing infrastructure (single enforcer)

## Recommendation

**Option C: Minimal Implementation** - Wrap justfile, add changelog and tagging.

**Rationale:**
- Preserves working justfile infrastructure (single enforcer)
- Adds changelog for project history documentation
- Addresses P2 finding without over-engineering
- Can extend if needs grow

## Decision Required

User must choose: A (full), B (remove), or C (minimal wrapper).

## Verdict

**PAUSE** - Requires user decision before implementation.
