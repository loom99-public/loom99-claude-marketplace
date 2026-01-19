# Sprint: remove-gabe-dup

**Generated**: 2026-01-19
**Confidence**: HIGH
**Status**: READY FOR IMPLEMENTATION

## Sprint Goal

Remove duplicate gabe agent from do-extra plugin, establishing do-more as single source of truth.

## Scope

**Deliverables:**
1. Delete `plugins/do-extra/agents/gabe.md`
2. Update `plugins/do-extra/README.md` to remove gabe references

## Work Items

### P0: Delete duplicate agent file

**File to delete:**
- `plugins/do-extra/agents/gabe.md`

**Acceptance Criteria:**
- [ ] File `plugins/do-extra/agents/gabe.md` no longer exists
- [ ] `plugins/do-more/agents/gabe.md` still exists
- [ ] `just validate` passes

**Technical Notes:**
- Simple `rm` operation
- Verify do-more version exists first

### P0: Update do-extra README.md

**File:** `plugins/do-extra/README.md`

**Changes:**
1. Remove gabe from Agents section
2. Remove gabe from "When to Use" section

**Acceptance Criteria:**
- [ ] README.md no longer mentions gabe
- [ ] README.md remains valid markdown
- [ ] Other content preserved

## Dependencies

None - standalone cleanup task.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Someone invokes gabe from do-extra | Very Low | Low | do-more version found instead |
