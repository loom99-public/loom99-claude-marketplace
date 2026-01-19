# Sprint: remove-vestigial-audit-skill

**Generated**: 2026-01-18
**Confidence**: HIGH
**Status**: READY FOR IMPLEMENTATION

## Sprint Goal

Remove the unused `audit` skill, leaving `audit-master` as the single source of truth.

## Scope

**Deliverables:**
1. Delete `plugins/do-more/skills/audit/` directory
2. Update documentation references that incorrectly point to `do:audit` skill

## Work Items

### P0: Delete unused audit skill directory

**Files to delete:**
- `plugins/do-more/skills/audit/SKILL.md`
- `plugins/do-more/skills/audit/` (directory)

**Acceptance Criteria:**
- [ ] Directory `plugins/do-more/skills/audit/` no longer exists
- [ ] Plugin validates successfully (`just validate`)
- [ ] Tests pass (`just test`)

**Technical Notes:**
- Simple `rm -rf` operation
- No code depends on this skill

### P1: Update CLAUDE.md skill reference

**File:** `plugins/do-more/CLAUDE.md:171`

Current: `| 'do:audit' | Deep forensic analysis |`

The CLAUDE.md skills table lists `do:audit` but should reference `do:audit-master` or clarify it's the command.

**Acceptance Criteria:**
- [ ] CLAUDE.md skill table correctly describes audit functionality
- [ ] No confusion between command and skill

**Technical Notes:**
- Line 171 in CLAUDE.md lists `do:audit` in Skills Reference
- This should either:
  - Be `do:audit-master` (the actual skill)
  - Or be removed (since it's really a command, not a skill users invoke directly)

### P2: Update docs/SKILLS.md references

**File:** `plugins/do-more/docs/SKILLS.md:32,287,471`

References to `do:audit` skill should point to `do:audit-master`.

**Acceptance Criteria:**
- [ ] `docs/SKILLS.md` references `audit-master` instead of `audit` for skill invocations

## Dependencies

None - this is a cleanup task.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Claude auto-invokes "do:audit" skill by name | Low | Low | audit-master exists, will be found instead |
| Documentation becomes inconsistent | Low | Low | Addressed in P1/P2 |
