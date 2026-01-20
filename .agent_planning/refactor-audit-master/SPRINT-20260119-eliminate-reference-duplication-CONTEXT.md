# Implementation Context: Eliminate Reference Duplication

**Sprint**: Eliminate Reference Duplication
**Date**: 2026-01-19

---

## Background

When specialized audit skills (deep-audit, security-audit, planning-audit, test-coverage-audit) were created, they copied reference files from audit-master rather than linking to them. This created 46 duplicate files violating the "One Source of Truth" principle.

**This sprint fixes the duplication by making audit-master the sole owner of all reference content.**

---

## Architecture Context

### Current (Problematic)

```
plugins/do-more/skills/
├── audit-master/
│   └── references/ (41 files) ← SOURCE OF TRUTH
├── deep-audit/
│   └── references/ (4 files) ← DUPLICATE
├── security-audit/
│   └── references/ (2 files) ← DUPLICATE
├── planning-audit/
│   └── references/ (3 files) ← DUPLICATE
└── test-coverage-audit/
    └── references/ (31 files) ← DUPLICATE
```

**Problem**: 5 skills own reference content → sync burden, risk of divergence

### Target (Clean)

```
plugins/do-more/skills/
├── audit-master/
│   └── references/ (41 files) ← ONLY SOURCE OF TRUTH
├── deep-audit/
│   └── SKILL.md → references ../audit-master/references/code-quality/
├── security-audit/
│   └── SKILL.md → references ../audit-master/references/security/
├── planning-audit/
│   └── SKILL.md → references ../audit-master/references/planning/
└── test-coverage-audit/
    └── SKILL.md → references ../audit-master/references/testing/
```

**Benefit**: 1 skill owns references → single update point, no sync burden

---

## Duplication Analysis

### deep-audit

**Duplicates**: `audit-master/references/code-quality/`

| File | Hash Match | Size |
|------|------------|------|
| architecture.md | ✅ 100% | ~15KB |
| design-quality.md | ✅ 100% | ~12KB |
| domains.md | ✅ 100% | ~18KB |
| efficiency.md | ✅ 100% | ~8KB |

**Total**: 4 files, ~53KB

### security-audit

**Duplicates**: `audit-master/references/security/`

| File | Hash Match | Size |
|------|------------|------|
| auth-checklist.md | ✅ 100% | ~10KB |
| owasp-checklist.md | ✅ 100% | ~8KB |

**Total**: 2 files, ~18KB

### planning-audit

**Duplicates**: `audit-master/references/planning/`

| File | Hash Match | Size |
|------|------------|------|
| quick-audit.md | ✅ 100% | ~6KB |
| medium-audit.md | ✅ 100% | ~12KB |
| thorough-audit.md | ✅ 100% | ~15KB |

**Total**: 3 files, ~33KB

### test-coverage-audit

**Duplicates**: `audit-master/references/testing/`

| Category | Files | Estimated Size |
|----------|-------|----------------|
| concepts/ | 4 | ~40KB |
| detection/ | 3 | ~30KB |
| languages/ | 6 | ~60KB |
| scenarios/ | 15 | ~150KB |

**Total**: 31 files, ~280KB (largest duplication)

---

## Why This Happened

**Root cause**: When specialized skills were extracted from audit-master, the pattern was:

1. Create new skill directory
2. Copy relevant reference files locally
3. Create SKILL.md that references local `references/`

**What should have happened**:
1. Create new skill directory
2. Create SKILL.md that references `../audit-master/references/`
3. No copy step

**Lesson**: When creating related skills, use relative paths to shared resources rather than duplicating.

---

## Relative Path Strategy

### Directory Structure

```
plugins/do-more/skills/
├── audit-master/
│   ├── SKILL.md
│   └── references/
│       ├── code-quality/
│       ├── security/
│       ├── planning/
│       ├── competitive/
│       └── testing/
├── deep-audit/
│   └── SKILL.md
├── security-audit/
│   └── SKILL.md
├── planning-audit/
│   └── SKILL.md
└── test-coverage-audit/
    └── SKILL.md
```

### Path Resolution

From any `plugins/do-more/skills/<skill>/SKILL.md`:
- Target: `../audit-master/references/<dimension>/`
- `..` moves up to `plugins/do-more/skills/`
- `audit-master/references/<dimension>/` descends to target

**Example from deep-audit**:
```markdown
See [architecture checklist](../audit-master/references/code-quality/architecture.md)
```

**Resolves to**:
```
plugins/do-more/skills/audit-master/references/code-quality/architecture.md
```

---

## Implementation Strategy

### Order of Operations

**Process each skill independently**:

1. **Delete local references/**
   ```bash
   rm -rf plugins/do-more/skills/<skill>/references/
   ```

2. **Update SKILL.md**
   - Find all mentions of `references/<dimension>/`
   - Replace with `../audit-master/references/<dimension>/`

3. **Verify path**
   ```bash
   cd plugins/do-more/skills/<skill>/
   ls ../audit-master/references/<dimension>/
   ```

4. **Validate**
   ```bash
   just validate
   ```

### Skill-Specific Notes

#### deep-audit

**References to update**: `references/` → `../audit-master/references/code-quality/`

**Files affected**: Only SKILL.md (likely 2-3 references)

#### security-audit

**References to update**: `references/` → `../audit-master/references/security/`

**Files affected**: Only SKILL.md (likely 2-3 references)

#### planning-audit

**References to update**: `references/` → `../audit-master/references/planning/`

**Files affected**: Only SKILL.md (likely 3-4 references for quick/medium/thorough)

#### test-coverage-audit

**References to update**: `references/` → `../audit-master/references/testing/`

**Files affected**: SKILL.md (many references to concepts/, detection/, languages/, scenarios/)

**Complexity**: Highest - many subdirectories and files referenced

**Strategy**: Use search/replace carefully:
- `references/concepts/` → `../audit-master/references/testing/concepts/`
- `references/detection/` → `../audit-master/references/testing/detection/`
- `references/languages/` → `../audit-master/references/testing/languages/`
- `references/scenarios/` → `../audit-master/references/testing/scenarios/`

---

## Testing Strategy

### Per-Skill Testing

After updating each skill:

1. **Path verification**:
   ```bash
   cd plugins/do-more/skills/<skill>/
   ls -la ../audit-master/references/<dimension>/
   ```
   Should show files, not "No such file or directory"

2. **Validation**:
   ```bash
   just validate
   ```
   Should pass

3. **Manual load test**:
   - Open Claude Code
   - Reload plugins
   - Check skill loads without errors

### Integration Testing

After all skills updated:

1. **Check no duplicates remain**:
   ```bash
   find plugins/do-more/skills/ -name "references" -type d
   ```
   Should show ONLY: `plugins/do-more/skills/audit-master/references`

2. **Verify audit-master untouched**:
   ```bash
   git status plugins/do-more/skills/audit-master/references/
   ```
   Should show no changes

3. **Storage check**:
   ```bash
   du -sh plugins/do-more/skills/*/references/ 2>/dev/null
   ```
   Should show ONLY audit-master, ~700KB

---

## Rollback Strategy

If issues found:

```bash
git revert <commit-hash>
```

All changes are deletions + small edits, easy to roll back.

**Prevention**: Test each skill individually before moving to next.

---

## Common Pitfalls

### Don't: Change audit-master/references/

**Zero edits to reference content**. This sprint is ONLY about:
- Deleting duplicate directories
- Updating paths in SKILL.md files

### Don't: Use absolute paths

**Wrong**:
```markdown
See /Users/.../plugins/do-more/skills/audit-master/references/...
```

**Right**:
```markdown
See ../audit-master/references/...
```

### Don't: Break existing functionality

**Before deleting**: Verify the specialized skill actually uses those references. If unused, deletion is fine. If used, update paths first.

---

## Success Indicators

**You know you're done when**:
- `find . -name references -type d` shows only audit-master
- All 4 specialized skills updated
- `just validate` passes
- Git diff shows 40 deletions, 4 edits
- ~700KB storage reclaimed

---

## Commit Strategy

**Commit message**:
```
refactor(do-more): eliminate audit reference duplication

Removes duplicate reference files from specialized audit skills.
audit-master/references/ is now the single source of truth.

Changes:
- Delete references/ from deep-audit (4 files)
- Delete references/ from security-audit (2 files)
- Delete references/ from planning-audit (3 files)
- Delete references/ from test-coverage-audit (31 files)
- Update all 4 skills to reference ../audit-master/references/

Savings: ~700KB, eliminates sync burden.

Fixes P1 finding from audit consolidation evaluation.
```

**Rationale**: Clear explanation of why (duplication), what (40 file deletions), and benefit (storage + maintainability).
