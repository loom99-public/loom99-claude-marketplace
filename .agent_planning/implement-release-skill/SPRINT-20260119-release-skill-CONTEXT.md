# Implementation Context: release-skill

**Sprint**: release-skill
**Generated**: 2026-01-19

## Critical Files

### Primary Files to Modify

1. **`plugins/do-more/skills/release-skill/SKILL.md`**
   - Current: Stub with planned features
   - Target: Full skill implementation

2. **`justfile`** (may need extension)
   - Current: `bump` and `bump-plugin` commands (patch only)
   - Target: May need `bump-major`, `bump-minor` recipes

3. **`CHANGELOG.md`** (to be created)
   - Location: Repository root
   - Format: Keep a Changelog format

### Reference Files (Patterns to Follow)

- `plugins/do/skills/chores-skill/SKILL.md` - Action routing pattern
- `plugins/do-more/skills/docs-skill/SKILL.md` - Similar structure

### Version Tracking Files

1. `plugins/do/.claude-plugin/plugin.json` - do plugin version
2. `plugins/do-more/.claude-plugin/plugin.json` - do-more plugin version
3. `.claude-plugin/marketplace.json` - marketplace version sync

## Architecture Constraints

### Single Enforcer Principle

Version bumping logic lives in justfile. The skill MUST delegate to justfile, not reimplement.

### One Source of Truth

- Version number: `plugin.json` is authoritative
- Marketplace syncs from plugin.json
- Git tags derived from plugin.json version

## Changelog Format

Recommend [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

## [0.5.22] - 2026-01-19

### Added
- Feature X

### Changed
- Modified Y

### Fixed
- Bug Z
```

## Edge Cases to Handle

1. **No commits since last tag**: Nothing to release
2. **Tag already exists**: Error with clear message
3. **Uncommitted changes**: Warn but allow
4. **First release**: No previous tag, use all commits

## Decision: User Input Required

Before implementation begins, user must confirm:

1. **Which option?** A (full), B (remove), or C (minimal)
2. **If C or A: Major/minor bump needed?** Or patch-only sufficient?
3. **Changelog scope**: All plugins combined, or per-plugin?
4. **Tag format**: `v{version}` or `do-v{version}` for namespacing?
