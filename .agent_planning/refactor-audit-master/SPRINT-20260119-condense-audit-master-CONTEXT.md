# Implementation Context: Condense audit-master

**Sprint**: Condense audit-master
**Date**: 2026-01-19

---

## Background

The `audit-master` skill serves as the entry point for `/do:audit`, routing to 5 audit dimensions (code quality, planning, security, competitive, test coverage). Over time, it grew to 1064 lines by including inline process instructions that duplicate content in `references/` files.

**Root cause**: When dimensions were added, process steps were written inline first, then extracted to references later, but inline content was never removed.

---

## Architecture Context

### Current Architecture

```
audit-master/
├── SKILL.md (1064 lines) - ORCHESTRATOR + MANUAL (PROBLEM)
└── references/
    ├── code-quality/ (4 files)
    ├── competitive/ (1 file)
    ├── planning/ (3 files)
    ├── security/ (2 files)
    └── testing/ (31 files)
```

**Problem**: SKILL.md acts as both:
1. Orchestrator (dimension selection, routing) ← CORRECT ROLE
2. Manual (detailed checklists, process steps) ← SHOULD DELEGATE

### Target Architecture

```
audit-master/
├── SKILL.md (400-500 lines) - PURE ORCHESTRATOR
│   ├── Dimension selection logic
│   ├── Core concepts (inline)
│   └── "See references/" pointers (delegation)
└── references/ (unchanged)
    └── ... (detailed checklists)
```

**Principle**: SKILL.md orchestrates, references/ provide content.

---

## What to Preserve

### 1. Dimension Selection Logic (Lines 1-83)

**CRITICAL - DO NOT CHANGE**

This section handles:
- User prompt for dimension selection (multiSelect question)
- Trigger word detection ("code", "security", "tests", etc.)
- "Audit everything" handling

**Why preserve**: Core routing logic for the skill.

### 2. Core Conceptual Models

**These are HIGH VALUE inline content - KEEP**:

| Concept | Location | Why Keep Inline |
|---------|----------|-----------------|
| Planning Stack | Dimension 2 | Essential mental model for understanding planning audits |
| Planning Horizon Guidelines | Dimension 2 | Critical for setting expectations about planning detail |
| Testing Pyramid | Dimension 5 | Fundamental testing concept, needed for context |
| Testing at Right Level | Dimension 5 | Prevents common mistakes, high value |
| LLM Testing Mistakes | Dimension 5 | Prevents AI-specific errors, unique insight |
| Security Scope Table | Dimension 3 | Sets boundaries (what's in/out of scope) |

**Rationale**: These are conceptual frameworks, not process steps. They belong in the orchestrator for context-setting.

### 3. Utility Sections

**UNCHANGED**:
- Combined Audit Output format
- Priority Levels table
- Capture Audit Findings section
- Complete Reference Index (navigation aid)
- Related Skills section

**Rationale**: These provide essential utility and are not part of the bloat.

---

## What to Remove

### Inline Process Steps

**REMOVE from all 5 dimensions**:
- Step-by-step instructions (already in references/)
- Detection commands (`grep`, `find`, tool installation)
- Detailed checklists
- Example code snippets
- Tool usage examples

**Replace with**: "See references/<dimension>/ for detailed checklists"

### Example: Security Dimension

**BEFORE** (180 lines):
```markdown
## Dimension 3: Security
### Security Audit Process
#### Step 1: Dependency Audit
**Check for known vulnerabilities:**
```bash
npm audit
pip-audit
govulncheck ./...
```
**Document findings:**
| Dependency | CVE | Severity | Fix Available? |
...
(140 more lines of detailed steps)
```

**AFTER** (30 lines):
```markdown
## Dimension 3: Security
### When to Use Security
- Before deployment to production
- After adding auth/payment/sensitive data handling
- Periodic security review

### Scope
| In Scope | Out of Scope |
|----------|--------------|
| Dependency CVEs | Penetration testing |
| Code-level vulnerabilities | Infrastructure security |
| Auth/authz patterns | Network security |
| OWASP Top 10 | Compliance audits |

### Security Audit Process
See [references/security/owasp-checklist.md](references/security/owasp-checklist.md) and [references/security/auth-checklist.md](references/security/auth-checklist.md) for comprehensive checklists covering:
- Dependency audit (npm audit, pip-audit, etc.)
- Secret detection (gitleaks, trufflehog)
- Authentication review
- Authorization review
- Data exposure review
- OWASP Top 10 review
- Input validation review

### Security Output
(output format preserved)
```

**Result**: 180 lines → 30 lines, delegating to references.

---

## Line Budget per Dimension

| Dimension | Current | Target | What Stays Inline |
|-----------|---------|--------|-------------------|
| Code Quality | 150 | 20-30 | When to Use, Sub-dimensions table, output |
| Planning | 200 | 35-45 | When to Use, Planning Stack, Horizon Guidelines, output |
| Security | 180 | 25-35 | When to Use, Scope table, output |
| Competitive | 150 | 25-35 | When to Use, quick summary, output |
| Test Coverage | 250 | 45-55 | When to Use, Testing Pyramid, Right Level table, LLM Mistakes, output |

**Total target**: 400-450 lines (down from 1064)

---

## Implementation Strategy

### Phase 1: Dimension-by-Dimension Refactoring

**For each dimension**:
1. Read current section fully
2. Identify core concepts (see "What to Preserve" above)
3. Identify process steps (see "What to Remove" above)
4. Edit section:
   - Keep: "When to Use", core concepts, output format
   - Remove: Process steps
   - Add: "See references/<dimension>/" pointer
5. Verify: Section is 20-55 lines (depending on dimension)

**Order**: Code Quality → Planning → Security → Competitive → Test Coverage

### Phase 2: Validation

1. `wc -l` check: Confirm <500 lines
2. `just validate`: Plugin validation passes
3. Read through: Check for broken formatting, orphaned sections
4. Manual test: `/do:audit` → select dimensions → verify references load

### Phase 3: Commit

**Commit message format**:
```
refactor(do-more): condense audit-master from 1064 to ~450 lines

Removes inline process content duplicating reference files.
audit-master/SKILL.md now acts as pure orchestrator.

- Preserves: dimension selection, core concepts, reference index
- Removes: inline checklists, process steps (now in references/)
- Delegates: detailed content to audit-master/references/

Fixes P1 finding from audit consolidation evaluation.
```

---

## Reference Paths

**From SKILL.md location**:
```
plugins/do-more/skills/audit-master/SKILL.md
plugins/do-more/skills/audit-master/references/code-quality/
plugins/do-more/skills/audit-master/references/planning/
plugins/do-more/skills/audit-master/references/security/
plugins/do-more/skills/audit-master/references/competitive/
plugins/do-more/skills/audit-master/references/testing/
```

**Relative path from SKILL.md**: `references/<dimension>/`

---

## Common Pitfalls

### Don't: Remove core concepts

**Example**: Removing the Testing Pyramid from Dimension 5 would be a mistake. It's a foundational concept that sets context for the entire dimension.

**Rule**: If it's a mental model / conceptual framework, keep it inline. If it's a process step / checklist, delegate to references.

### Don't: Break dimension selection

**Lines 1-83 are untouchable**. The AskUserQuestion logic, dimension table, and intensity levels must remain exactly as-is.

### Don't: Change reference files

**Zero edits to references/ directory**. This refactoring is ONLY about condensing SKILL.md.

### Don't: Remove the Reference Index

**Lines 1120-1217 (Complete Reference Index) stay unchanged**. This is a navigation aid, not bloat.

---

## Testing Strategy

### Unit Test (per dimension)

After editing each dimension:
1. Check line count: `sed -n '/^## Dimension N:/,/^## Dimension N+1:/p' SKILL.md | wc -l`
2. Verify structure: "When to Use" → Core Concepts → "See references/"
3. Check formatting: No broken headers, lists, or code blocks

### Integration Test (full file)

After all dimensions edited:
1. `wc -l plugins/do-more/skills/audit-master/SKILL.md` → 400-500
2. `just validate` → PASS
3. Read through: Spot-check for coherence, no orphaned text

### Manual Test (runtime)

1. Run `/do:audit`
2. Dimension selection prompt appears
3. Select "Code Quality" → verify workflow makes sense
4. Select "Test Coverage" → verify Testing Pyramid visible
5. Check that references are accessible (even if not automatically loaded)

---

## Success Indicators

**You know you're done when**:
- File is <500 lines
- Each dimension is <55 lines
- No inline process steps remain
- Core concepts still present
- `just validate` passes
- Git diff shows clean refactoring (~600 deletions, ~40 additions)
