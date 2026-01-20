# Evaluation: Refactor audit-master

**Date**: 2026-01-19
**Topic**: Refactor audit-master skill to reduce size and eliminate inline duplication
**Status**: CONTINUE

---

## Current State

### audit-master Structure

**Location**: `plugins/do-more/skills/audit-master/`

**File**: `SKILL.md` (1064 lines)

**Structure**:
```
SKILL.md (1064 lines)
├── Dimension Selection (40 lines)
├── Available Dimensions table (20 lines)
├── Intensity Levels (15 lines)
├── Dimension 1: Code Quality (150 lines INLINE)
│   ├── When to Use (10 lines)
│   ├── Workflow (20 lines)
│   ├── Sub-Dimensions table (15 lines)
│   ├── Output format (10 lines)
│   └── Reference links (5 lines) ← SHOULD BE PRIMARY CONTENT
├── Dimension 2: Planning (200 lines INLINE)
│   ├── Planning Stack explanation (80 lines)
│   ├── Audit Process (quick/medium/thorough) (90 lines)
│   ├── Planning Horizon Guidelines (20 lines)
│   └── Reference links (10 lines) ← SHOULD BE PRIMARY CONTENT
├── Dimension 3: Security (180 lines INLINE)
│   ├── Scope table (20 lines)
│   ├── 7-step process (140 lines)
│   └── Reference links (20 lines) ← SHOULD BE PRIMARY CONTENT
├── Dimension 4: Competitive (150 lines INLINE)
│   ├── 6-step process (120 lines)
│   └── Reference links (10 lines) ← SHOULD BE PRIMARY CONTENT
├── Dimension 5: Test Coverage (250 lines INLINE)
│   ├── Testing Philosophy (40 lines)
│   ├── 6-phase process (180 lines)
│   └── Reference links (30 lines) ← SHOULD BE PRIMARY CONTENT
├── Combined Audit Output (30 lines)
├── Priority Levels table (15 lines)
├── Capture Audit Findings (40 lines)
└── Complete Reference Index (54 lines) ← REDUNDANT
```

**Problem**: 75% of the content (800+ lines) is inline process descriptions that duplicate content already in reference files.

### Reference Files

**audit-master has 41 reference files**:
```
references/
├── code-quality/ (4 files)
│   ├── architecture.md
│   ├── design-quality.md
│   ├── domains.md
│   └── efficiency.md
├── competitive/ (1 file)
│   └── research-template.md
├── planning/ (3 files)
│   ├── medium-audit.md
│   ├── quick-audit.md
│   └── thorough-audit.md
├── security/ (2 files)
│   ├── auth-checklist.md
│   └── owasp-checklist.md
└── testing/ (31 files)
    ├── concepts/ (4 files)
    ├── detection/ (3 files)
    ├── languages/ (6 files)
    └── scenarios/ (15 files)
```

### Specialized Skills with Duplicate References

| Skill | Duplicates | Files |
|-------|------------|-------|
| `deep-audit` | code-quality/* | 4 files (100% match) |
| `security-audit` | security/* | 2 files (100% match) |
| `planning-audit` | planning/* | 3 files (100% match) |
| `test-coverage-audit` | testing/* | 31 files (100% match) |

**Total duplication**: ~46 files, ~700KB

---

## Problem Analysis

### P1: audit-master is a God Class (1064 lines)

**Symptoms**:
- Single file responsible for ALL dimension logic
- Inline content duplicates reference files
- High cognitive load for maintenance
- Violation of Single Responsibility Principle

**Impact**:
- Hard to maintain (changes require editing 1000+ line file)
- Duplicate content with references creates sync burden
- Contributors unsure whether to update SKILL.md or references/

### P1: Reference File Duplication (46 files)

**Problem**: Each specialized audit skill (deep-audit, security-audit, planning-audit, test-coverage-audit) contains 100% duplicates of audit-master's reference files.

**Why this happened**: When specialized skills were created, references were copied rather than linked.

**Impact**:
- 700KB wasted storage
- Sync burden: updates must be made in 2 places
- Violates "One Source of Truth"
- Risk of divergence (already happened with test-coverage-audit)

### P2: Inline Content Duplication

**Example**: Security dimension in SKILL.md:

```markdown
## Dimension 3: Security
...
#### Step 1: Dependency Audit
**Check for known vulnerabilities:**
```bash
npm audit
pip-audit
...
```
```

This ENTIRE section (180 lines) is duplicated in `references/security/owasp-checklist.md`.

**Pattern repeats for all 5 dimensions**.

---

## What Needs to Change

### Files Affected

**Primary**:
- `plugins/do-more/skills/audit-master/SKILL.md` (1064 → <500 lines)

**Secondary** (for duplication fix):
- `plugins/do-more/skills/deep-audit/` - delete references/, update SKILL.md
- `plugins/do-more/skills/security-audit/` - delete references/, update SKILL.md
- `plugins/do-more/skills/planning-audit/` - delete references/, update SKILL.md
- `plugins/do-more/skills/test-coverage-audit/` - delete references/, update SKILL.md

**Unchanged**:
- `plugins/do-more/skills/audit-master/references/` - KEEP (source of truth)

### Target Architecture

```
audit-master/SKILL.md (<500 lines)
├── Dimension Selection (40 lines) [KEEP]
├── Available Dimensions (20 lines) [KEEP]
├── Intensity Levels (15 lines) [KEEP]
├── Dimension 1: Code Quality (30 lines) [CONDENSED]
│   ├── When to Use (10 lines)
│   ├── Quick summary (10 lines)
│   └── "See references/code-quality/ for checklists" (5 lines)
├── Dimension 2: Planning (40 lines) [CONDENSED]
│   ├── When to Use (10 lines)
│   ├── The Planning Stack (20 lines) [core concept, keep]
│   └── "See references/planning/ for audit checklists" (5 lines)
├── Dimension 3: Security (30 lines) [CONDENSED]
│   ├── When to Use (10 lines)
│   ├── Scope table (10 lines) [core concept, keep]
│   └── "See references/security/ for checklists" (5 lines)
├── Dimension 4: Competitive (30 lines) [CONDENSED]
│   ├── When to Use (10 lines)
│   ├── Quick summary (10 lines)
│   └── "See references/competitive/ for process" (5 lines)
├── Dimension 5: Test Coverage (50 lines) [CONDENSED]
│   ├── When to Use (10 lines)
│   ├── Testing Pyramid (20 lines) [core concept, keep]
│   └── "See references/testing/ for detection/scenarios" (5 lines)
├── Combined Output (30 lines) [KEEP]
├── Priority Levels (15 lines) [KEEP]
├── Capture Findings (40 lines) [KEEP]
└── Complete Reference Index (50 lines) [KEEP - useful navigation]
```

**Estimated**: 400-450 lines total (58% reduction)

### Specialized Skills Architecture

**Before**:
```
deep-audit/
├── SKILL.md (100 lines)
└── references/
    ├── architecture.md [DUPLICATE]
    ├── design-quality.md [DUPLICATE]
    ├── domains.md [DUPLICATE]
    └── efficiency.md [DUPLICATE]
```

**After**:
```
deep-audit/
└── SKILL.md (80 lines)
    "For checklists, see audit-master/references/code-quality/"
```

---

## Dependencies and Risks

### Dependencies

**None**. This is a pure refactoring of markdown content.

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Break existing workflows | Low | High | Keep dimension selection logic intact, only condense inline content |
| Skills can't find references | Medium | High | Update specialized skills to reference audit-master/references/ |
| Reference links break | Low | Medium | Use relative paths from skill location |
| Users expect inline content | Medium | Low | Keep "when to use" and core concepts inline |

### Validation Strategy

**After refactoring**:
1. Run `just validate` to check plugin integrity
2. Test each dimension invocation: `/do:audit code`, `/do:audit security`, etc.
3. Verify specialized skills can access audit-master references
4. Check that reference file links still resolve

---

## Ambiguities and Unknowns

### None - This is HIGH confidence work

**Why HIGH confidence**:
1. Pure markdown refactoring - no code logic
2. Clear source of truth (audit-master/references/)
3. Well-defined target structure (<500 lines)
4. Validation strategy is straightforward
5. Rollback is trivial (git revert)

---

## Implementation Approach

### Phase 1: Refactor audit-master/SKILL.md (1064 → <500 lines)

**For each dimension**:
1. Keep: "When to Use", core concepts (Planning Stack, Testing Pyramid, Scope table)
2. Replace: Inline process steps with "See references/<dimension>/"
3. Keep: Output format examples
4. Keep: Reference index at end (navigation aid)

**Estimated time**: 1-2 hours (careful editing)

### Phase 2: Fix Specialized Skill Duplication

**For each skill** (deep-audit, security-audit, planning-audit, test-coverage-audit):
1. Delete `references/` directory
2. Update SKILL.md to reference `../audit-master/references/<dimension>/`
3. Verify relative paths resolve correctly

**Estimated time**: 30 minutes

### Phase 3: Validate

1. `just validate`
2. Manual test: `/do:audit code`, `/do:audit security`, `/do:audit tests`
3. Check specialized skills still work
4. Verify reference links in skill descriptions

**Estimated time**: 15 minutes

---

## Success Criteria

**Must achieve ALL**:
- [ ] `audit-master/SKILL.md` is <500 lines (target: 400-450)
- [ ] No inline process content duplicating references/
- [ ] All 5 dimensions still have clear "when to use" guidance
- [ ] Core concepts (Planning Stack, Testing Pyramid) preserved inline
- [ ] Reference index remains complete and navigable
- [ ] Specialized skills reference audit-master/references/ (no duplicates)
- [ ] `just validate` passes
- [ ] All dimension invocations work (`/do:audit <dimension>`)

---

## Verdict

**CONTINUE** - Ready for sprint planning.

This is HIGH confidence work with clear success criteria and low risk.
