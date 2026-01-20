# Sprint: Eliminate Reference Duplication

**Generated**: 2026-01-19
**Confidence**: HIGH
**Status**: READY FOR IMPLEMENTATION
**Depends On**: SPRINT-20260119-condense-audit-master

---

## Sprint Goal

Eliminate ~46 duplicate reference files across specialized audit skills by removing local `references/` directories and updating skills to reference `audit-master/references/` as the single source of truth.

---

## Scope

**Deliverables**:
1. Remove `references/` from 4 specialized audit skills
2. Update each skill's SKILL.md to reference `../audit-master/references/`
3. Verify relative paths resolve correctly
4. Achieve ~700KB storage savings and eliminate sync burden

---

## Work Items

### P0: Fix deep-audit Duplication

**Current State**:
```
plugins/do-more/skills/deep-audit/
├── SKILL.md (100 lines)
└── references/
    ├── architecture.md [DUPLICATE of audit-master/references/code-quality/architecture.md]
    ├── design-quality.md [DUPLICATE]
    ├── domains.md [DUPLICATE]
    └── efficiency.md [DUPLICATE]
```

**Target State**:
```
plugins/do-more/skills/deep-audit/
└── SKILL.md (80 lines)
    "See ../audit-master/references/code-quality/ for checklists"
```

**Acceptance Criteria**:
- [ ] `deep-audit/references/` directory deleted
- [ ] `deep-audit/SKILL.md` updated to reference `../audit-master/references/code-quality/`
- [ ] Relative path works from deep-audit location
- [ ] `just validate` passes

**Files to Change**:
- DELETE: `plugins/do-more/skills/deep-audit/references/`
- EDIT: `plugins/do-more/skills/deep-audit/SKILL.md`

**Technical Notes**:
- Path from deep-audit to audit-master: `../audit-master/references/code-quality/`
- Update all mentions of local references/ to use shared path
- Test path resolution: `ls plugins/do-more/skills/audit-master/references/code-quality/` from deep-audit context

---

### P0: Fix security-audit Duplication

**Current State**:
```
plugins/do-more/skills/security-audit/
├── SKILL.md (120 lines)
└── references/
    ├── auth-checklist.md [DUPLICATE]
    └── owasp-checklist.md [DUPLICATE]
```

**Target State**:
```
plugins/do-more/skills/security-audit/
└── SKILL.md (100 lines)
    "See ../audit-master/references/security/ for checklists"
```

**Acceptance Criteria**:
- [ ] `security-audit/references/` directory deleted
- [ ] `security-audit/SKILL.md` updated to reference `../audit-master/references/security/`
- [ ] Relative path works from security-audit location
- [ ] `just validate` passes

**Files to Change**:
- DELETE: `plugins/do-more/skills/security-audit/references/`
- EDIT: `plugins/do-more/skills/security-audit/SKILL.md`

**Technical Notes**:
- Path from security-audit to audit-master: `../audit-master/references/security/`
- Verify both auth-checklist.md and owasp-checklist.md accessible

---

### P0: Fix planning-audit Duplication

**Current State**:
```
plugins/do-more/skills/planning-audit/
├── SKILL.md (90 lines)
└── references/
    ├── quick-audit.md [DUPLICATE]
    ├── medium-audit.md [DUPLICATE]
    └── thorough-audit.md [DUPLICATE]
```

**Target State**:
```
plugins/do-more/skills/planning-audit/
└── SKILL.md (70 lines)
    "See ../audit-master/references/planning/ for checklists"
```

**Acceptance Criteria**:
- [ ] `planning-audit/references/` directory deleted
- [ ] `planning-audit/SKILL.md` updated to reference `../audit-master/references/planning/`
- [ ] Relative path works from planning-audit location
- [ ] `just validate` passes

**Files to Change**:
- DELETE: `plugins/do-more/skills/planning-audit/references/`
- EDIT: `plugins/do-more/skills/planning-audit/SKILL.md`

**Technical Notes**:
- Path from planning-audit to audit-master: `../audit-master/references/planning/`
- All 3 checklist files (quick/medium/thorough) must be accessible

---

### P0: Fix test-coverage-audit Duplication

**Current State**:
```
plugins/do-more/skills/test-coverage-audit/
├── SKILL.md (150 lines)
└── references/
    ├── concepts/ (4 files) [ALL DUPLICATE]
    ├── detection/ (3 files) [ALL DUPLICATE]
    ├── languages/ (6 files) [ALL DUPLICATE]
    └── scenarios/ (15 files) [ALL DUPLICATE]
    Total: 31 files, all duplicates
```

**Target State**:
```
plugins/do-more/skills/test-coverage-audit/
└── SKILL.md (130 lines)
    "See ../audit-master/references/testing/ for comprehensive guides"
```

**Acceptance Criteria**:
- [ ] `test-coverage-audit/references/` directory deleted (31 files)
- [ ] `test-coverage-audit/SKILL.md` updated to reference `../audit-master/references/testing/`
- [ ] Relative path works from test-coverage-audit location
- [ ] All subdirectories accessible (concepts/, detection/, languages/, scenarios/)
- [ ] `just validate` passes

**Files to Change**:
- DELETE: `plugins/do-more/skills/test-coverage-audit/references/` (entire directory, 31 files)
- EDIT: `plugins/do-more/skills/test-coverage-audit/SKILL.md`

**Technical Notes**:
- Path from test-coverage-audit to audit-master: `../audit-master/references/testing/`
- This removes the most duplication (31 files vs 4+2+3 for others)
- Verify subdirectory access: concepts/, detection/, languages/, scenarios/

---

## Dependencies

**Must complete FIRST**: SPRINT-20260119-condense-audit-master

**Why**: audit-master refactoring may change how references are structured/documented. Complete that first to avoid rework.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Relative paths break | Low | High | Test each path after editing |
| Skills can't find references | Low | High | Verify `../audit-master/references/` exists from each location |
| `just validate` fails | Low | Medium | Run validation after each skill update |
| Break existing invocations | Low | Medium | Test each skill invocation after change |

---

## Validation Steps

**Per skill**:
1. Delete `references/` directory: `rm -rf plugins/do-more/skills/<skill>/references/`
2. Edit SKILL.md to use `../audit-master/references/<dimension>/`
3. Verify path: `ls ../audit-master/references/<dimension>/` from skill directory
4. Run `just validate`

**Final**:
1. Check all 4 skills updated
2. Verify `audit-master/references/` unchanged
3. Run full test: `/do:audit` → select each dimension → verify works
4. Check storage savings: `du -sh plugins/do-more/skills/*/references/ 2>/dev/null` → should show ONLY audit-master

---

## Definition of Done

- [ ] `deep-audit/references/` deleted (4 files)
- [ ] `security-audit/references/` deleted (2 files)
- [ ] `planning-audit/references/` deleted (3 files)
- [ ] `test-coverage-audit/references/` deleted (31 files)
- [ ] All 4 skills updated to reference `../audit-master/references/<dimension>/`
- [ ] `just validate` passes
- [ ] Manual test: All 4 specialized skills work when invoked
- [ ] Git diff shows 46 file deletions, 4 SKILL.md edits
- [ ] Storage savings: ~700KB

---

## Implementation Order

1. **deep-audit** (simplest, 4 files)
2. **security-audit** (simple, 2 files)
3. **planning-audit** (simple, 3 files)
4. **test-coverage-audit** (most complex, 31 files)

**Rationale**: Build confidence with simple cases before tackling the 31-file test-coverage-audit.

---

## Success Metrics

| Metric | Before | After |
|--------|--------|-------|
| Total reference files | 82 | 41 |
| Duplicate files | 46 | 0 |
| Storage (references/) | ~1.4MB | ~700KB |
| Skills with local references/ | 5 | 1 (audit-master only) |
| Source of truth locations | 5 | 1 |

---

## Notes

**Key Principle**: One Source of Truth for all audit reference content.

**Why this matters**:
- **Maintainability**: Updates happen once, not 2-5 times
- **Consistency**: No risk of divergence between copies
- **Simplicity**: Clear ownership (audit-master owns references)

**Why it's safe**:
- Relative paths are stable (plugins/do-more/skills/<name>/)
- No code logic depends on local references/
- Skills are just markdown that references other markdown
- Easy rollback if issues found
