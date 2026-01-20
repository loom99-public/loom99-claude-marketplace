# Sprint: Condense audit-master

**Generated**: 2026-01-19
**Confidence**: HIGH
**Status**: READY FOR IMPLEMENTATION

---

## Sprint Goal

Eliminate duplicate content between `audit-master/SKILL.md` and reference files. Make SKILL.md an effective orchestrator that sets context and delegates to references for detailed checklists.

**Real Problem**: Process instructions appear in both SKILL.md and references/. Updates require editing two places. SKILL.md should orchestrate, references should contain details.

**Not About**: Line count targets. About effectiveness and eliminating duplication.

---

## Scope

**Deliverables**:
1. audit-master/SKILL.md with no duplicate content from references/
2. Clear orchestration: dimension selection → core concepts → delegate to references
3. Core concepts preserved inline where they provide essential context
4. Repetition kept where it reinforces critical principles

---

## Work Items

### P0: Refactor Dimension 1 (Code Quality)

**Acceptance Criteria**:
- [ ] "When to Use" section preserved - sets context for when this dimension applies
- [ ] Sub-dimensions table preserved - shows what aspects are covered
- [ ] Inline process steps removed - these duplicate references/code-quality/
- [ ] Clear delegation: "See references/code-quality/ for detailed checklists"
- [ ] Output format preserved - shows what audit produces
- [ ] Core concepts kept if they aid understanding
- [ ] No arbitrary line targets - optimize for effectiveness

**Files to Edit**:
- `plugins/do-more/skills/audit-master/SKILL.md:85-234`

**What to Remove**:
- Detailed sub-dimension checklists (already in references/code-quality/)
- Step-by-step process instructions
- Detection commands and tool examples

**What to Keep**:
- When to Use - essential context
- Sub-dimensions table - shows coverage
- Output format - sets expectations
- Any conceptual models that aid understanding

**Add**: Clear pointer to references/code-quality/ for detailed content

---

### P0: Refactor Dimension 2 (Planning)

**Acceptance Criteria**:
- [ ] "When to Use" preserved - context
- [ ] Planning Stack preserved - FOUNDATIONAL CONCEPT agents need repeatedly
- [ ] Planning Horizon Guidelines preserved - CRITICAL for understanding detail levels
- [ ] Process checklists removed - duplicate references/planning/
- [ ] Clear delegation to references/planning/
- [ ] Output format preserved

**What to Remove**:
- Quick/medium/thorough audit process steps (in references/)
- Redundant explanations already in checklists

**What to Keep - These Are Critical**:
- Planning Stack (Strategy→Architecture→Plans→Implementation) - agents need this mental model
- Planning Horizon Guidelines - prevents common mistakes about planning detail
- When to Use - sets context
- Output format - expectations

Repeat critical concepts where repetition aids understanding. The Planning Stack is foundational - keep it prominent.

---

### P0: Refactor Dimension 3 (Security)

**Acceptance Criteria**:
- [ ] "When to Use" preserved
- [ ] Scope table preserved - CRITICAL boundary setting (what's in/out of scope)
- [ ] 7-step process removed - duplicates references/security/
- [ ] Clear delegation to references/
- [ ] Output format preserved

**What to Remove**:
- Dependency audit commands (npm audit, pip-audit, etc.) - in references/
- Secret detection tools and usage - in references/
- OWASP Top 10 checklist details - in references/
- Auth/authz review steps - in references/

**What to Keep**:
- Scope table - agents need to know boundaries immediately
- When to Use - context
- Output format

The Scope table is critical - it prevents agents from going down wrong paths (pentesting, infrastructure security, etc.).

---

### P0: Refactor Dimension 4 (Competitive)

**Acceptance Criteria**:
- [ ] "When to Use" preserved
- [ ] Brief summary of competitive audit purpose
- [ ] 6-step process removed - in references/
- [ ] Clear delegation to references/competitive/
- [ ] Output format preserved

**What to Remove**:
- Detailed 6-step research process - in references/competitive/research-template.md

**What to Keep**:
- When to Use - context
- What competitive audit achieves (quick summary)
- Output format

---

### P0: Refactor Dimension 5 (Test Coverage)

**Acceptance Criteria**:
- [ ] "When to Use" preserved
- [ ] Testing Pyramid preserved - FOUNDATIONAL CONCEPT
- [ ] "Testing at the Right Level" table preserved - PREVENTS COMMON MISTAKES
- [ ] "Common AI/LLM Testing Mistakes" preserved - HIGH VALUE, UNIQUE INSIGHT
- [ ] 6-phase detection process removed - in references/
- [ ] Clear delegation to references/testing/
- [ ] Output format preserved

**What to Remove**:
- Complexity source detection steps - in references/testing/detection/
- Project type detection - in references/testing/scenarios/
- Language-specific testing - in references/testing/languages/
- Detailed phase-by-phase process - in references/

**What to Keep - These Are Critical**:
- Testing Pyramid - agents need this fundamental model repeatedly
- Testing at Right Level table - prevents waste (wrong test level)
- LLM Testing Mistakes - prevents AI-specific errors, unique value
- When to Use - context
- Output format

The Testing Pyramid and "Right Level" guidance are foundational - keep prominent. LLM mistakes table is unique insight not elsewhere.

---

### P1: Preserve Utility Sections

**Acceptance Criteria**:
- [ ] "Combined Audit Output" section unchanged (lines 1020-1048)
- [ ] "Priority Levels" table unchanged (lines 1050-1062)
- [ ] "Capture Audit Findings" section unchanged (lines 1064-1118)
- [ ] "Complete Reference Index" unchanged (lines 1120-1217) - NAVIGATION AID
- [ ] "Related Skills" section unchanged (lines 1219-1226)

**Technical Notes**:
These sections provide essential utility and should remain as-is. They are not part of the bloat problem.

---

## Dependencies

**None** - Pure markdown refactoring.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Break dimension selection | Keep all dimension selection logic intact (lines 1-83) |
| References not found | Use correct relative paths; test all reference links |
| Loss of core concepts | Explicitly preserve Planning Stack, Testing Pyramid, Scope tables |
| Users can't find details | Keep reference index complete; add clear "See references/" pointers |

---

## Validation Steps

1. **Line count check**: `wc -l plugins/do-more/skills/audit-master/SKILL.md` shows <500
2. **Plugin validation**: `just validate` passes
3. **Dimension selection test**: Each dimension still selectable via AskUserQuestion
4. **Reference access test**: References load correctly when dimensions invoked
5. **Manual review**: Core concepts (Stack, Pyramid, Scope) still present

---

## Definition of Done

- [ ] No duplicate content between SKILL.md and references/
- [ ] Core concepts preserved where they provide essential context
- [ ] Process steps removed (delegated to references/)
- [ ] Clear "See references/" delegation for each dimension
- [ ] Utility sections unchanged
- [ ] `just validate` passes
- [ ] Dimension selection still works
- [ ] Foundational concepts (Planning Stack, Testing Pyramid, Scope) prominent where agents need them

**Not Done**: Hitting a specific line count. Done when duplication is eliminated and effectiveness maximized.

---

## Key Principles

**Orchestrator vs Manual**: SKILL.md orchestrates, references/ contain details.

**Effectiveness Over Brevity**: Keep text that makes agents more effective. Remove duplicate content.

**Repetition is Valuable**: Foundational concepts (Planning Stack, Testing Pyramid, Security Scope) should be prominent where agents need them. Don't optimize them away.

**What Makes Agents Effective**:
- Clear context (When to Use sections)
- Foundational mental models (Stack, Pyramid, Scope)
- Immediate boundary awareness (what's in/out of scope)
- Prevention of common mistakes (LLM testing errors, wrong test levels)
- Clear delegation when detail is elsewhere

**What Belongs Inline**:
- Dimension selection and routing
- Foundational concepts agents need repeatedly
- Context-setting and boundary definitions
- Output formats
- Navigation aids

**What Belongs in References**:
- Detailed checklists and procedures
- Tool commands and syntax
- Detection patterns and methods
- Step-by-step processes
