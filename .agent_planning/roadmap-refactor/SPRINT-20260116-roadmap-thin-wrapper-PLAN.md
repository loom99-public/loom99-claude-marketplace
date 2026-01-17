# Sprint: roadmap-thin-wrapper - Refactor Roadmap Command to Thin Wrapper

Generated: 2026-01-16
Confidence: HIGH
Status: READY FOR IMPLEMENTATION

## Sprint Goal

Convert `/do:roadmap` command from 448-line implementation to thin wrapper that invokes `do-roadmap-skill`.

## Scope

**Deliverables:**
1. Rename skill directory from `roadmap` to `do-roadmap-skill`
2. Update skill SKILL.md with entry point procedure
3. Reduce command to thin wrapper (~30 lines)
4. Update all documentation references

## Work Items

### P0: Rename skill directory and update metadata

**Acceptance Criteria:**
- [ ] Directory renamed: `skills/roadmap/` → `skills/do-roadmap-skill/`
- [ ] SKILL.md frontmatter updated: `name: do-roadmap-skill`
- [ ] Skill description updated to reflect it's the core implementation
- [ ] SCHEMA.md moved to new directory (unchanged otherwise)

**Technical Notes:**
- Use `git mv` to preserve history
- Update any internal references within the skill files

### P1: Add entry point procedure to skill

**Acceptance Criteria:**
- [ ] New "Procedure 0: Execute Roadmap Command" added to SKILL.md
- [ ] Procedure handles both modes (view/add) based on input
- [ ] Accepts `mode` and `topic` parameters
- [ ] Returns formatted output for display

**Technical Notes:**
- Entry point orchestrates existing procedures
- Should be at top of Core Procedures section

### P2: Convert command to thin wrapper

**Acceptance Criteria:**
- [ ] Command reduced to ~30 lines
- [ ] Command invokes `Skill("do:do-roadmap-skill")` with mode/topic
- [ ] Same user-facing behavior (view mode, add mode)
- [ ] Preserves frontmatter (argument-hint, description)

**Technical Notes:**
- Remove all step-by-step implementation from command
- Command becomes pure invocation + argument parsing

### P3: Update documentation references

**Acceptance Criteria:**
- [ ] README.md still shows `/do:roadmap` (unchanged - command still exists)
- [ ] SKILL.md "See Also" references updated
- [ ] SCHEMA.md references updated
- [ ] Any stale `do:roadmap` skill references updated to `do:do-roadmap-skill`

**Technical Notes:**
- Cross-references in SKILL.md line 737
- SCHEMA.md line 259, 289

## Dependencies

- None (self-contained refactor)

## Risks

| Risk | Mitigation |
|------|------------|
| Breaking existing `/do:roadmap` invocations | Test both modes after refactor |
| Documentation inconsistency | Update all refs in same commit |

## Verification

After implementation:
1. Run `/do:roadmap` (no args) - should display tree or "no roadmap" message
2. Run `/do:roadmap test-topic` (with args) - should trigger add flow
3. Verify `just validate` passes
4. Verify `just test` passes
