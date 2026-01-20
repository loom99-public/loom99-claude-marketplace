# Definition of Done: Condense audit-master

**Sprint**: Condense audit-master
**Date**: 2026-01-19

---

## Acceptance Criteria

### File Size

- [ ] `plugins/do-more/skills/audit-master/SKILL.md` is 400-500 lines
- [ ] Reduction of ~600 lines (58% size decrease from 1064 lines)

### Content Structure

- [ ] Dimension 1 (Code Quality): 20-30 lines (down from 150)
- [ ] Dimension 2 (Planning): 35-45 lines (down from 200)
- [ ] Dimension 3 (Security): 25-35 lines (down from 180)
- [ ] Dimension 4 (Competitive): 25-35 lines (down from 150)
- [ ] Dimension 5 (Test Coverage): 45-55 lines (down from 250)

### Core Concepts Preserved

- [ ] Planning Stack diagram/explanation intact (Dimension 2)
- [ ] Testing Pyramid diagram intact (Dimension 5)
- [ ] Security Scope table intact (Dimension 3)
- [ ] Planning Horizon Guidelines intact (Dimension 2)
- [ ] "Testing at the Right Level" table intact (Dimension 5)
- [ ] "Common AI/LLM Testing Mistakes" table intact (Dimension 5)

### Inline Content Removed

- [ ] Code Quality: Sub-dimension detailed checklists removed
- [ ] Planning: Quick/medium/thorough audit process steps removed
- [ ] Security: 7-step process instructions removed
- [ ] Competitive: 6-step process instructions removed
- [ ] Test Coverage: 6-phase process instructions removed

### References Properly Linked

- [ ] Each dimension has clear "See references/<dimension>/" pointer
- [ ] Reference paths are correct (relative from skill location)
- [ ] Complete Reference Index section unchanged
- [ ] All reference files still exist in audit-master/references/

### Utility Sections Unchanged

- [ ] Dimension Selection logic intact (lines 1-83)
- [ ] Available Dimensions table intact
- [ ] Intensity Levels table intact
- [ ] Combined Audit Output format intact
- [ ] Priority Levels table intact
- [ ] Capture Audit Findings section intact
- [ ] Complete Reference Index intact
- [ ] Related Skills section intact

### Validation

- [ ] `just validate` passes without errors
- [ ] Plugin loads successfully in Claude Code
- [ ] Dimension selection via AskUserQuestion works
- [ ] All 5 dimensions selectable
- [ ] Reference files accessible from skill

### Git Diff Quality

- [ ] Diff shows ~600 deletions, <50 additions
- [ ] No reference files deleted or modified
- [ ] Only SKILL.md changed (single-file refactor)
- [ ] No whitespace-only changes

### Manual Testing

- [ ] Run `/do:audit` → dimension selection prompt appears
- [ ] Select "Code Quality" → references load correctly
- [ ] Select "Security" → references load correctly
- [ ] Select "Test Coverage" → references load correctly
- [ ] Core concepts (Stack, Pyramid) visible in skill when needed

---

## Quality Checks

### Readability

- [ ] Each dimension section is scannable (<40 lines)
- [ ] Clear hierarchy: When to Use → Core Concepts → See References
- [ ] No orphaned subsections or broken formatting
- [ ] Markdown formatting valid (headers, lists, code blocks)

### Maintainability

- [ ] Updates to audit process now happen ONLY in references/
- [ ] SKILL.md is pure orchestration (no process duplication)
- [ ] Clear separation: orchestration (SKILL.md) vs. content (references/)

### User Experience

- [ ] Users can still understand what each dimension does
- [ ] Core concepts remain accessible inline (no hunting in references)
- [ ] "See references/" pointers guide users to details
- [ ] Reference index aids navigation

---

## Success Metrics

| Metric | Before | Target | Actual |
|--------|--------|--------|--------|
| SKILL.md lines | 1064 | 400-500 | _____ |
| Code Quality section | 150 | 20-30 | _____ |
| Planning section | 200 | 35-45 | _____ |
| Security section | 180 | 25-35 | _____ |
| Competitive section | 150 | 25-35 | _____ |
| Test Coverage section | 250 | 45-55 | _____ |
| Inline duplication | High | None | _____ |

---

## Done When

All checkboxes above are ✅ AND:
- User can successfully run `/do:audit` and select dimensions
- Plugin passes validation
- Git history shows clean refactoring commit
