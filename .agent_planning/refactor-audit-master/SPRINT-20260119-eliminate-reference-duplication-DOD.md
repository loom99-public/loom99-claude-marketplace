# Definition of Done: Eliminate Reference Duplication

**Sprint**: Eliminate Reference Duplication
**Date**: 2026-01-19

---

## Acceptance Criteria

### Files Deleted

- [ ] `plugins/do-more/skills/deep-audit/references/` deleted (4 files)
- [ ] `plugins/do-more/skills/security-audit/references/` deleted (2 files)
- [ ] `plugins/do-more/skills/planning-audit/references/` deleted (3 files)
- [ ] `plugins/do-more/skills/test-coverage-audit/references/` deleted (31 files)
- [ ] Total: 40 files deleted from specialized skills

### Files Updated

- [ ] `plugins/do-more/skills/deep-audit/SKILL.md` references `../audit-master/references/code-quality/`
- [ ] `plugins/do-more/skills/security-audit/SKILL.md` references `../audit-master/references/security/`
- [ ] `plugins/do-more/skills/planning-audit/SKILL.md` references `../audit-master/references/planning/`
- [ ] `plugins/do-more/skills/test-coverage-audit/SKILL.md` references `../audit-master/references/testing/`

### audit-master Unchanged

- [ ] `plugins/do-more/skills/audit-master/references/` directory intact
- [ ] All 41 reference files present in audit-master
- [ ] No modifications to audit-master/references/ content

### Relative Paths Valid

- [ ] `../audit-master/references/code-quality/` resolves from deep-audit
- [ ] `../audit-master/references/security/` resolves from security-audit
- [ ] `../audit-master/references/planning/` resolves from planning-audit
- [ ] `../audit-master/references/testing/` resolves from test-coverage-audit

### Validation

- [ ] `just validate` passes without errors
- [ ] No broken plugin references
- [ ] All 4 specialized skills load successfully

### Git Diff Quality

- [ ] 40 file deletions (references/ directories)
- [ ] 4 file edits (SKILL.md updates)
- [ ] No unintended changes to other files
- [ ] Clean commit history

### Manual Testing

- [ ] `/do:audit` invoked successfully
- [ ] Specialized skills still selectable if directly invoked
- [ ] No errors about missing reference files
- [ ] Paths resolve correctly at runtime

---

## Quality Checks

### Storage Impact

- [ ] Measured before: `du -sh plugins/do-more/skills/*/references/`
- [ ] Measured after: Only audit-master/references/ remains
- [ ] Confirmed ~700KB savings

### One Source of Truth

- [ ] `find plugins/do-more/skills/ -name "references" -type d` shows ONLY audit-master
- [ ] No duplicate reference files remain in specialized skills
- [ ] audit-master is sole owner of all reference content

### Path Correctness

- [ ] From each skill directory, verify `ls ../audit-master/references/<dimension>/` works
- [ ] Relative paths don't break when plugin directory structure changes (unlikely)

---

## Success Metrics

| Metric | Before | Target | Actual |
|--------|--------|--------|--------|
| Total reference files | 82 | 41 | _____ |
| Duplicate files | 46 | 0 | _____ |
| Skills with references/ | 5 | 1 | _____ |
| Source of truth count | 5 | 1 | _____ |
| Storage savings | 0 | ~700KB | _____ |

---

## Per-Skill Checklist

### deep-audit

- [ ] `references/` deleted (4 files: architecture.md, design-quality.md, domains.md, efficiency.md)
- [ ] SKILL.md updated with `../audit-master/references/code-quality/` path
- [ ] Path verified: `ls ../audit-master/references/code-quality/` from deep-audit directory
- [ ] Skill loads without errors

### security-audit

- [ ] `references/` deleted (2 files: auth-checklist.md, owasp-checklist.md)
- [ ] SKILL.md updated with `../audit-master/references/security/` path
- [ ] Path verified: `ls ../audit-master/references/security/` from security-audit directory
- [ ] Skill loads without errors

### planning-audit

- [ ] `references/` deleted (3 files: quick-audit.md, medium-audit.md, thorough-audit.md)
- [ ] SKILL.md updated with `../audit-master/references/planning/` path
- [ ] Path verified: `ls ../audit-master/references/planning/` from planning-audit directory
- [ ] Skill loads without errors

### test-coverage-audit

- [ ] `references/` deleted (31 files across concepts/, detection/, languages/, scenarios/)
- [ ] SKILL.md updated with `../audit-master/references/testing/` path
- [ ] Path verified: `ls ../audit-master/references/testing/` from test-coverage-audit directory
- [ ] All subdirectories accessible (concepts/, detection/, languages/, scenarios/)
- [ ] Skill loads without errors

---

## Done When

All checkboxes above are ✅ AND:
- Git shows 40 file deletions, 4 edits
- `just validate` passes
- Manual invocation of each specialized skill works
- Only audit-master has a references/ directory
