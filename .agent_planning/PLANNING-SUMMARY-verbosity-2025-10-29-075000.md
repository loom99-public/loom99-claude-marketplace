# Planning Summary: Verbosity Reduction Initiative

**Generated**: 2025-10-29 07:50:00
**Source STATUS**: STATUS-2025-10-29-050659.md
**Detailed Plan**: PLAN-verbosity-reduction-2025-10-29-075000.md
**Initiative Owner**: verbosity-reduction-planner

---

## One-Page Overview

### The Problem

The loom99-claude-marketplace plugins are **2x more verbose than necessary** (24,459 lines → optimal 9,000-12,000 lines).

**Key Finding**: Commands are catastrophically oversized (75% bloat), with excessive framework duplication, three-layer redundancy, and cognitive overload.

### The Solution

**3-Phase Reduction Plan** targeting 62% reduction (-15,263 lines):

1. **Phase 1 (P0-P1)**: Commands & structural redundancy → -11,500 lines (-47%)
2. **Phase 2 (P2)**: Skills & READMEs → -8,700 lines (cumulative -67%)
3. **Phase 3 (P3)**: Agents & polish → -1,800 lines (cumulative -69%)

**Timeline**: 8-11 days (2-3 weeks with buffer)

### The Impact

**Before**:
- Commands: 11,803 lines (avg 723 lines/command) ❌
- Skills: 9,272 lines (avg 692 lines/skill) ❌
- Cognitive load: HIGH (files exceed 1,000 lines)
- Signal-to-noise: 40% signal, 60% noise

**After**:
- Commands: 2,910 lines (avg 182 lines/command) ✅
- Skills: 4,030 lines (avg 310 lines/skill) ✅
- Cognitive load: OPTIMAL (files 75-400 lines)
- Signal-to-noise: 75% signal, 25% noise

**Result**: 2x better effectiveness through focused, scannable content

---

## Phase Breakdown

### Phase 1: Commands & Structure (3-5 days)

**Target**: -11,500 lines through command reduction, framework consolidation, layer separation

**Highest Impact**:
- visual-iteration commands: 8,656 → 1,640 lines (-81% bloat)
- epti commands: 2,805 → 1,070 lines (-62% bloat)
- Framework examples: 5-6 variants → 1-2 variants
- Three-layer redundancy: 40-60% overlap → <20% overlap

**Deliverable**: Commands are prompts (not tutorials), framework duplication eliminated

---

### Phase 2: Skills & READMEs (3-4 days)

**Target**: -8,700 lines through skill streamlining, README condensation, git consolidation

**Highest Impact**:
- visual-iteration skills: 4,475 → 1,700 lines (-62%)
- epti skills: 3,034 → 1,430 lines (-53%)
- All READMEs: 4,272 → 1,050 lines (-75%)
- Git operations: Consolidated to single source

**Deliverable**: Skills are procedures (not manuals), READMEs are references (not tutorials)

---

### Phase 3: Agents & Polish (1-2 days)

**Target**: -1,800 lines through agent optimization, pseudocode conversion, consistency

**Highest Impact**:
- visual-iteration agent: 946 → 600 lines (-37%)
- epti agent: 636 → 400 lines (-37%)
- Code examples → pseudocode patterns
- Final consistency pass

**Deliverable**: Agents optimized, pseudocode patterns, consistent across plugins

---

## Risk & Mitigation

**Overall Risk**: LOW (benefits >> risks)

| Risk | Mitigation |
|------|------------|
| **Loss of clarity** | Keep core procedures intact |
| **Test failures** | Run `just test` after every change |
| **Skill non-invocation** | Preserve YAML descriptions |
| **Command malfunction** | Validate after each reduction |
| **Framework confusion** | Keep 1-2 representative examples |

**Rollback**: Git branches per phase, easy revert at any level (phase/file/plugin)

---

## Success Criteria

### Quantitative
- [ ] Total lines: 24,459 → 7,500-9,000 (62-69% reduction)
- [ ] Commands: 723 avg → 182 avg (75% reduction)
- [ ] Skills: 692 avg → 310 avg (57% reduction)
- [ ] READMEs: 1,424 avg → 350 avg (75% reduction)
- [ ] Framework examples: 5-6 → 1-2 per concept

### Qualitative
- [ ] Signal-to-noise: 40% → 75% signal
- [ ] Layer overlap: 40-60% → <20%
- [ ] Cognitive load: Files within optimal ranges (75-400 lines)
- [ ] Effectiveness: Equal or better Claude adherence

### Validation
- [ ] `just validate` passing (all phases)
- [ ] `just test` passing (60+ tests, all phases)
- [ ] Manual testing: Commands, skills, full workflows
- [ ] Effectiveness comparison: Before/after testing

---

## File-Level Targets (Top Priority)

### Commands (Phase 1 - CRITICAL)

| File | Current | Target | Reduction |
|------|---------|--------|-----------|
| visual-iteration/load-mock.md | 1,324 | 250 | **-1,074 (-81%)** |
| visual-iteration/iterate.md | 1,120 | 280 | **-840 (-75%)** |
| visual-iteration/visual-commit.md | 996 | 280 | **-716 (-72%)** |
| visual-iteration/compare.md | 937 | 300 | **-637 (-68%)** |
| visual-iteration/implement-design.md | 905 | 280 | **-625 (-69%)** |
| visual-iteration/screenshot.md | 809 | 250 | **-559 (-69%)** |

### Skills (Phase 2 - HIGH)

| File | Current | Target | Reduction |
|------|---------|--------|-----------|
| visual-iteration/design-implementation | 1,232 | 480 | **-752 (-61%)** |
| visual-iteration/visual-refinement | 1,137 | 450 | **-687 (-60%)** |
| visual-iteration/visual-comparison | 1,070 | 420 | **-650 (-61%)** |
| epti/refactoring | 715 | 320 | **-395 (-55%)** |
| epti/test-execution | 652 | 300 | **-352 (-54%)** |

### READMEs (Phase 2 - HIGH)

| File | Current | Target | Reduction |
|------|---------|--------|-----------|
| visual-iteration/README.md | 2,319 | 500 | **-1,819 (-78%)** |
| epti/README.md | 1,238 | 350 | **-888 (-72%)** |
| agent-loop/README.md | 715 | 200 | **-515 (-72%)** |

---

## Timeline & Dependencies

```
Week 1: Phase 1 (Commands & Structure)
├── Day 1-2: visual-iteration commands (-7,016 lines)
├── Day 3: epti commands (-1,735 lines)
├── Day 4: agent-loop commands + framework consolidation (-142 + -2,000 lines)
└── Day 5: Layer redundancy elimination (-2,500 lines)
    └── Gate 1: Validation (13,000 lines remaining)

Week 2: Phase 2 (Skills & READMEs)
├── Day 6-7: visual-iteration + epti skills (-4,379 lines)
├── Day 8: agent-loop skills + git consolidation (-1,863 lines)
└── Day 9: READMEs (-3,222 lines)
    └── Gate 2: Validation (8,000 lines remaining)

Week 2-3: Phase 3 (Polish)
├── Day 10: Agents + pseudocode (-2,082 lines)
└── Day 11: Final pass + documentation (-300 lines)
    └── Gate 3: Final validation (7,500 lines remaining)

Buffer: +3 days for issues, testing, documentation
```

**Estimated Completion**: Mid-November 2025

---

## Key Decisions

1. **Work across plugins in parallel** (not one at a time) for consistency
2. **Commands first** (Phase 1) due to worst bloat (75%)
3. **Clear layer separation**: agent=workflow, command=trigger, skill=procedure
4. **Minimum viable content**: Commands 75-200, Skills 250-400, Agents 300-600 lines
5. **Validation strategy**: Structural (automated) + Functional (manual) + Effectiveness (comparison)
6. **Rollback plan**: Git branches per phase, per-file granularity

---

## Next Steps

### Immediate (Before Starting)
1. Read full plan: PLAN-verbosity-reduction-2025-10-29-075000.md
2. Review questions/decisions log in plan
3. Verify current state: `just validate && just test`
4. Create baseline metrics: `./scripts/count-lines.sh`
5. Back up repository (local + cloud)

### Phase 1 Kickoff
1. Create branch: `git checkout -b phase-1-command-reduction`
2. Start with visual-iteration commands (highest impact)
3. Apply reduction pattern: mission + checklist + 1 example + reference
4. Validate continuously: `just validate && just test`
5. Complete Gate 1 validation

### Questions?
- See "Questions & Decisions Log" section in detailed plan
- All major decisions documented with rationale
- Rollback strategy defined for each risk scenario

---

## Success Looks Like

**3 weeks from now:**
- ✅ 7,500-9,000 lines of focused, effective plugin content
- ✅ Commands are scannable prompts (75-200 lines)
- ✅ Skills are procedural checklists (250-400 lines)
- ✅ READMEs are quick references (200-500 lines)
- ✅ 2x better signal-to-noise ratio
- ✅ Improved Claude effectiveness (faster, better adherence)
- ✅ All 60+ tests passing
- ✅ All validation passing
- ✅ Documentation updated
- ✅ Ready for v0.1.1 release

**The Bottom Line**: Less is more. Shorter prompts = better Claude attention = better results.

---

**Status**: READY TO EXECUTE
**Confidence**: HIGH (low risk, high reward, clear plan)
**Owner**: Awaiting execution assignment

---

**References**:
- Detailed Plan: PLAN-verbosity-reduction-2025-10-29-075000.md
- Source Analysis: STATUS-2025-10-29-050659.md
- Architecture: ARCHITECTURE.md (v1.0)
- Spec: CLAUDE.md (v1.0)
