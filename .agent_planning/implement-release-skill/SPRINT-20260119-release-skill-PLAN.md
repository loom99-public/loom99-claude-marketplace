# Sprint: release-skill

**Generated**: 2026-01-19
**Confidence**: HIGH
**Status**: READY FOR IMPLEMENTATION

## Sprint Goal

Fully implement the release-skill with all planned features: bump, changelog, notes, tag, publish.

## Scope

**Deliverables:**
1. Implement `status` action - show current version and release info
2. Implement `bump` action - semantic version bumping (major/minor/patch)
3. Implement `changelog` action - generate CHANGELOG.md from git commits
4. Implement `notes` action - generate release notes for current version
5. Implement `tag` action - create git tag for current version
6. Implement `publish` action - full orchestrated release workflow

## Work Items

### P0: Implement core structure

**File:** `plugins/do-more/skills/release-skill/SKILL.md`

**Changes:**
- Remove "STUB" status
- Add action routing based on arguments
- Define workflow sections for each action

**Acceptance Criteria:**
- [ ] SKILL.md no longer marked as stub
- [ ] Action routing works (status, bump, changelog, notes, tag, publish)
- [ ] Default action is `status` when no arguments

### P1: Implement status action

**Purpose:** Show current release state

**Output:**
- Current version from plugin.json files
- Last git tag (if any)
- Commits since last tag
- Uncommitted changes warning

**Acceptance Criteria:**
- [ ] `/do:release status` shows version info
- [ ] Shows commit count since last tag
- [ ] Warns about uncommitted changes

### P2: Implement bump action

**Purpose:** Semantic version bumping

**Behavior:**
- `bump patch` (default) - increment patch version
- `bump minor` - increment minor, reset patch
- `bump major` - increment major, reset minor and patch
- Delegate to `just bump-plugin` for actual file updates
- May need to extend justfile for major/minor support

**Acceptance Criteria:**
- [ ] `/do:release bump` increments patch version
- [ ] `/do:release bump minor` increments minor version
- [ ] `/do:release bump major` increments major version
- [ ] Updates both plugin.json and marketplace.json

### P3: Implement changelog action

**Purpose:** Generate/update CHANGELOG.md

**Behavior:**
- Parse git commits since last tag (or all commits if no tags)
- Group by type if conventional commits used
- Append new section to CHANGELOG.md (or create if missing)
- Use Keep a Changelog format

**Format:**
```markdown
## [0.5.22] - 2026-01-19

### Added
- Feature descriptions

### Changed
- Modification descriptions

### Fixed
- Bug fix descriptions
```

**Acceptance Criteria:**
- [ ] `/do:release changelog` creates/updates CHANGELOG.md
- [ ] Groups commits by type when possible
- [ ] Preserves existing changelog content
- [ ] Uses current version from plugin.json

### P4: Implement notes action

**Purpose:** Generate release notes for current version

**Behavior:**
- Extract section for current version from CHANGELOG.md
- Format for human consumption
- Optionally output to file or display

**Acceptance Criteria:**
- [ ] `/do:release notes` displays release notes for current version
- [ ] Works even if CHANGELOG.md doesn't exist (generates from commits)

### P5: Implement tag action

**Purpose:** Create git tag for current version

**Behavior:**
- Read version from plugin.json
- Create annotated tag: `v{version}`
- Include release notes in tag message
- Check if tag already exists (error if so)

**Acceptance Criteria:**
- [ ] `/do:release tag` creates git tag
- [ ] Tag format is `v{version}` (e.g., `v0.5.22`)
- [ ] Errors if tag already exists
- [ ] Creates annotated tag with message

### P6: Implement publish action

**Purpose:** Full release workflow orchestration

**Behavior:**
1. Run `just validate` - abort if fails
2. Check for uncommitted changes - warn or abort
3. Run bump action (with specified level or patch default)
4. Run changelog action
5. Commit version bump and changelog
6. Run tag action
7. Display summary with next steps (push commands)

**Acceptance Criteria:**
- [ ] `/do:release publish` runs full workflow
- [ ] `/do:release publish minor` bumps minor then releases
- [ ] Validates before proceeding
- [ ] Creates single commit for version + changelog
- [ ] Displays push commands at end

## Dependencies

- `just bump-plugin` command (exists, may need extension)
- Git repository with commit history
- plugin.json files for version tracking

## Technical Notes

### Justfile Extension

May need to add to justfile:
```just
# Bump with specific level
bump-level plugin level:
    # Implementation for major/minor/patch
```

### Version Source of Truth

- `plugins/*/.claude-plugin/plugin.json` - authoritative version
- `.claude-plugin/marketplace.json` - synced from plugin.json
- Git tags - derived from plugin.json version

### Error Handling

- No commits since last tag → "Nothing to release"
- Tag already exists → Error with clear message
- Uncommitted changes → Warning (allow with confirmation)
- Validation fails → Abort with error details

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Changelog format inconsistency | Medium | Define clear format, parse commits carefully |
| Version drift between files | Low | Reuse justfile logic |
| Git tag conflicts | Low | Check before creating |
| Partial release failure | Low | Clear rollback instructions |
