# Plugin Workflow Audit Report

**Date**: 2026-01-18
**Scope**: do and do-more plugin workflows - cohesiveness, structure, missing functionality
**Intensity**: Medium

---

## Summary

```
Code Quality Audit:
  Architecture: ⚠️ Attention | Design: ✅ Healthy | Efficiency: ⚠️ Attention
  Findings: P0: 0 | P1: 3 | P2: 5 | P3: 2
```

The plugin architecture is sound with clear command→skill→agent separation. However, there are several orphaned components, incomplete features, and documentation inconsistencies that need attention.

---

## Inventory

| Component | do | do-more | Total |
|-----------|-----|---------|-------|
| Commands | 7 | 12 | 19 |
| Skills | 15 | 31 | 46 |
| Agents | 8 | 4 | 12 |

---

## Findings

### P1: High Priority Issues

#### 1. Orphaned Agents (P1)

**Location**: `plugins/do-more/agents/`

Three agents exist but are not invoked by any skill:

| Agent | File | Status |
|-------|------|--------|
| `execution-summarizer` | `agents/execution-summarizer.md` | Documented in CLAUDE.md but hooks.json is empty |
| `test-auditor` | `agents/test-auditor.md` | Documented in CLAUDE.md but no skill invokes it |
| `gabe` | `agents/gabe.md` | Well-documented rigidity breaker, no invocation path |

**Impact**: Users cannot access these agents through any workflow.

**Recommendation**:
- Connect `execution-summarizer` via hooks (hooks.json is currently `{}`)
- Connect `test-auditor` to `test-coverage-audit` skill
- Create `/do:rigidity` command to invoke `gabe` agent

---

#### 2. Duplicate Agent: gabe (P1)

**Location**:
- `plugins/do-more/agents/gabe.md`
- `plugins/do-extra/agents/gabe.md`

Both files are identical. Violates "One Source of Truth" principle.

**Impact**: Maintenance burden, potential drift.

**Recommendation**: Keep in one plugin (do-more), remove from do-extra.

---

#### 3. Empty Hooks in do-more (P1)

**Location**: `plugins/do-more/hooks/hooks.json`

```json
{
  "hooks": {}
}
```

The CLAUDE.md documentation claims:
- `execution-summarizer` runs on "All commands" for execution logging
- SessionStart/Stop hooks manage execution state

But hooks.json is empty - these documented features don't work.

**Impact**: Documented functionality doesn't exist.

**Recommendation**: Either implement hooks or update documentation to reflect reality.

---

### P2: Medium Priority Issues

#### 4. Stub Command: /do:release (P2)

**Location**: `plugins/do-more/skills/release-skill/SKILL.md`

The skill explicitly states "STUB - This command is a placeholder for future implementation."

**Impact**: Command exists but does nothing useful.

**Recommendation**: Either implement or remove/hide until ready.

---

#### 5. Skill Count Growth (P2)

**Observation**: 46 total skills (15 do + 31 do-more)

The do-more plugin has 31 skills, approaching maintainability limits. Many have overlapping purposes:
- `tdd-skill` vs `tdd-workflow`
- `test-skill` vs `test-coverage-audit` vs `test-recommendations` vs `test-implementation-plan`
- Multiple `*-skill` wrappers that just invoke other skills

**Impact**: Cognitive load, maintenance burden, potential for inconsistency.

**Recommendation**: Consider consolidating related skills or better hierarchical organization.

---

#### 6. Command Namespace Collision (P2)

**Observation**: Both plugins contribute to `/do:` namespace

| Command | Plugin |
|---------|--------|
| `/do:it` | do |
| `/do:plan` | do |
| `/do:stuff` | do-more |
| `/do:audit` | do-more |
| `/do:research` | do (internal) / do-more (external) |

The `/do:research` command exists in BOTH plugins with different purposes:
- do: "Research a problem or question through iterative exploration"
- do-more: "Research external sources - market analysis, competitors, external docs"

**Impact**: User confusion about which research command to use.

**Recommendation**: Rename do-more's research to `/do:market-research` or `/do:external-research`.

---

#### 7. Inconsistent Skill Naming (P2)

**Pattern observed**: Some skills use `-skill` suffix, some don't:

| With `-skill` suffix | Without |
|---------------------|---------|
| `it-skill` | `refactor` |
| `plan-skill` | `debug` |
| `status-skill` | `fix` |
| `release-skill` | `review` |

**Impact**: Inconsistent naming makes discovery harder.

**Recommendation**: Establish naming convention (preferably without `-skill` suffix, as it's redundant).

---

#### 8. Missing Workflow Documentation (P2)

**Location**: `plugins/do-more/CLAUDE.md`

The CLAUDE.md documents agent mapping but doesn't show:
- Which skills invoke which agents
- Complete skill dependency graph
- Workflow decision trees

**Impact**: Understanding plugin internals requires reading many files.

**Recommendation**: Add skill→agent mapping table and workflow diagrams.

---

### P3: Low Priority Issues

#### 9. Dead Documentation Files (P3)

**Location**: `plugins/do-more/`

| File | Status |
|------|--------|
| `DESIGNING-AN-AGENT.md` | Tutorial content, not plugin functionality |
| `FEATURE_PROPOSAL_subagent_execution_logging.md` | Old proposal, should be archived |
| `HANDOFF.md` | Appears to be outdated |

**Impact**: Clutter, potential confusion.

**Recommendation**: Archive or delete.

---

#### 10. Planning Artifact Proliferation (P3)

**Observation**: 8+ file types in `.agent_planning/<topic>/`:
- EVALUATION-*.md
- SPRINT-*-PLAN.md
- SPRINT-*-DOD.md
- SPRINT-*-CONTEXT.md
- USER-RESPONSE-*.md
- TODO-*.md
- RESEARCH-*.md
- WORK-EVALUATION-*.md
- DEFERRED-WORK.md
- eval-cache/

**Impact**: Complex file management, potential for stale artifacts.

**Recommendation**: Consider cleanup command or archival strategy.

---

## Architecture Strengths

1. **Clean Separation**: Command → Skill → Agent flow is well-defined
2. **Confidence-Based Planning**: Plans all work with explicit confidence levels
3. **Deferred Work Capture**: Prevents work from falling through cracks
4. **Agent Specialization**: Each agent has clear, bounded responsibilities
5. **Context Efficiency**: Eval-cache reuses previous work

---

## Missing Functionality

| Gap | Priority | Description |
|-----|----------|-------------|
| Release workflow | P2 | `/do:release` is a stub |
| Rigidity analysis | P2 | `gabe` agent exists but no command invokes it |
| Execution logging | P1 | Documented but hooks not connected |
| Test auditing | P1 | `test-auditor` agent orphaned |

---

## Recommendations Summary

| Priority | Action | Effort |
|----------|--------|--------|
| P1 | Connect execution-summarizer via hooks | Medium |
| P1 | Connect test-auditor to test-coverage-audit skill | Low |
| P1 | Remove duplicate gabe agent from do-extra | Low |
| P2 | Implement or remove release-skill | Medium |
| P2 | Rename do-more /do:research to avoid collision | Low |
| P2 | Add skill→agent mapping to CLAUDE.md | Low |
| P3 | Archive dead documentation files | Low |
| P3 | Create planning artifact cleanup command | Medium |

---

## Next Steps

1. Address P1 issues first (orphaned agents, duplicate gabe, empty hooks)
2. Decide on release-skill: implement or remove
3. Resolve command namespace collision
4. Consider skill consolidation for long-term maintainability
