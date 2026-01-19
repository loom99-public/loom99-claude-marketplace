# Definition of Done: release-skill

**Sprint**: release-skill
**Generated**: 2026-01-19
**User Decision**: Option A - Full Implementation

## Acceptance Criteria

### Core Functionality

- [ ] `/do:release` command executes without error
- [ ] `/do:release status` shows current version, last tag, commits since tag
- [ ] `/do:release bump` increments patch version correctly
- [ ] `/do:release bump minor` increments minor version correctly
- [ ] `/do:release bump major` increments major version correctly
- [ ] `/do:release changelog` generates/updates CHANGELOG.md
- [ ] `/do:release notes` displays release notes for current version
- [ ] `/do:release tag` creates git tag for current version
- [ ] `/do:release publish` orchestrates full release workflow

### Quality Gates

- [ ] No "STUB" text remains in SKILL.md
- [ ] Skill follows established patterns (reference: chores-skill, docs-skill)
- [ ] Error handling for edge cases:
  - [ ] No commits since last tag
  - [ ] Tag already exists
  - [ ] Uncommitted changes
  - [ ] Validation failure
- [ ] Output format matches other skills (boxed summary)

### Integration

- [ ] `just validate` passes after changes
- [ ] Existing `just bump` functionality preserved
- [ ] Version updates sync plugin.json and marketplace.json
- [ ] Justfile extended if needed for major/minor bumps

### Documentation

- [ ] SKILL.md has complete workflow documentation
- [ ] Each action documented with examples
- [ ] Error messages are clear and actionable

### Verification

Manual tests:
- [ ] `/do:release status` shows correct version info
- [ ] `/do:release bump patch` increments 0.5.21 → 0.5.22
- [ ] `/do:release changelog` creates valid CHANGELOG.md
- [ ] `/do:release tag` creates `v0.5.22` tag
- [ ] `/do:release publish` completes full workflow

## Files Created/Modified

| File | Change |
|------|--------|
| `plugins/do-more/skills/release-skill/SKILL.md` | Full implementation |
| `justfile` | Add bump-level recipe if needed |
| `CHANGELOG.md` | Created by changelog action |

## Not In Scope

- Automatic publishing to npm/pypi/etc
- GitHub release creation (just git tags)
- Multi-plugin version coordination (each plugin independent)
