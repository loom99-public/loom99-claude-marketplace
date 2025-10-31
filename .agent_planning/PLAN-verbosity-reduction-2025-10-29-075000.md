# Verbosity Reduction Plan: loom99-claude-marketplace

**Generated**: 2025-10-29 07:50:00
**Source Status**: STATUS-2025-10-29-050659.md
**Spec Reference**: CLAUDE.md (v1.0), ARCHITECTURE.md (v1.0)
**Plan Owner**: verbosity-reduction-planner

---

## Executive Summary

### Current State
- **Total Implementation**: 24,459 lines across 3 plugins
- **Bloat Factor**: 2.0-2.4x oversized (STATUS finding)
- **Primary Issue**: Commands catastrophically verbose (75% bloat, 11,803 lines)
- **Secondary Issues**: Framework duplication, three-layer redundancy, excessive examples

### Target State
- **Goal Line Count**: 9,000-12,000 lines (50-62% reduction)
- **Optimal Structure**: Clear layer separation, minimal duplication, focused content
- **Quality Improvement**: 2x better signal-to-noise ratio
- **Effectiveness**: Improved (shorter prompts = better Claude attention)

### Phase Approach
- **Phase 1** (P0-P1): Commands & duplication → -11,500 lines (-47%)
- **Phase 2** (P2): Skills & READMEs → -8,700 lines (cumulative -67%)
- **Phase 3** (P3): Polish & optimization → -1,800 lines (cumulative -69%)
- **Final Target**: 7,500-10,000 lines remaining

### Risk Assessment
- **Risk Level**: LOW (benefits >> risks)
- **Primary Mitigation**: Test suite (60+ tests) validates correctness
- **Validation**: `just validate` + `just test` after each phase
- **Rollback**: Git branches per phase, easy revert

---

## Gap Analysis: Current vs. Optimal

### Commands Gap (CRITICAL - 75% Bloat)

| Plugin | Current | Optimal | Gap | Priority |
|--------|---------|---------|-----|----------|
| visual-iteration | 8,656 lines | 1,640 lines | -7,016 (-81%) | **P0** |
| epti | 2,805 lines | 1,070 lines | -1,735 (-62%) | **P0** |
| agent-loop | 342 lines | 200 lines | -142 (-41%) | **P1** |
| **TOTAL** | **11,803** | **2,910** | **-8,893** | **CRITICAL** |

**Root Cause**: Commands written as tutorials instead of prompts. Contain full workflow explanations, extensive framework examples, and detailed code snippets that should be in skills or removed entirely.

**Evidence**: visual-iteration's `load-mock.md` is 1,324 lines—longer than many complete programs. Contains ~200 lines of guidance buried in 1,124 lines of examples.

### Skills Gap (HIGH - 57% Bloat)

| Plugin | Current | Optimal | Gap | Priority |
|--------|---------|---------|-----|----------|
| visual-iteration | 4,475 lines | 1,700 lines | -2,775 (-62%) | **P2** |
| epti | 3,034 lines | 1,430 lines | -1,604 (-53%) | **P2** |
| agent-loop | 1,763 lines | 900 lines | -863 (-49%) | **P2** |
| **TOTAL** | **9,272** | **4,030** | **-5,242** | **HIGH** |

**Root Cause**: Skills formatted as comprehensive user manuals instead of executable procedures. Framework examples multiply content 5-6x unnecessarily.

### READMEs Gap (HIGH - 75% Bloat)

| Plugin | Current | Optimal | Gap | Priority |
|--------|---------|---------|-----|----------|
| visual-iteration | 2,319 lines | 500 lines | -1,819 (-78%) | **P2** |
| epti | 1,238 lines | 350 lines | -888 (-72%) | **P2** |
| agent-loop | 715 lines | 200 lines | -515 (-72%) | **P2** |
| **TOTAL** | **4,272** | **1,050** | **-3,222** | **HIGH** |

**Root Cause**: READMEs written as human tutorials instead of Claude plugin references. These plugins are FOR Claude, not humans learning concepts.

### Agents Gap (MEDIUM - 33% Bloat)

| Plugin | Current | Optimal | Gap | Priority |
|--------|---------|---------|-----|----------|
| visual-iteration | 946 lines | 600 lines | -346 (-37%) | **P3** |
| epti | 636 lines | 400 lines | -236 (-37%) | **P3** |
| agent-loop | 206 lines | 206 lines | 0 (0%) | **N/A** |
| **TOTAL** | **1,788** | **1,206** | **-582** | **MEDIUM** |

**Root Cause**: Last third of agent files becomes repetitive. Quality guidelines and examples multiply beyond necessity.

### Structural Redundancy (CRITICAL)

**Three-Layer Overlap**:
- Agent describes workflow stage → Command repeats same workflow → Skill repeats procedures
- Estimated 40-60% overlap between agent/commands, 30-50% overlap between commands/skills
- **Impact**: ~2,500 lines of pure redundancy across all layers

**Framework Example Multiplication**:
- 1 Python example: 20 lines
- 6 framework examples: 120 lines (6x multiplier)
- Repeated across 15+ files: ~1,800 lines of redundant examples
- **Impact**: ~2,000 lines of framework duplication

**Git Operations Duplication**:
- Git commands and commit templates repeated across 8+ files
- Each template: 30-50 lines
- **Impact**: ~1,000 lines of git guidance duplication

**Total Structural Bloat**: ~5,500 lines of pure redundancy

---

## Phase 1: Critical Reduction (P0-P1)

**Goal**: Eliminate catastrophic command bloat and structural redundancy
**Target**: -11,500 lines (-47%)
**Effort**: 3-5 days (Medium)
**Risk**: Low (mostly redundant content)

### Initiative 1.1: Command Reduction (P0)

**Target**: Reduce commands from 11,803 → 2,910 lines (-8,893 lines, -75%)

#### visual-iteration Commands (HIGHEST PRIORITY)

| File | Current | Target | Reduction | Effort |
|------|---------|--------|-----------|--------|
| load-mock.md | 1,324 | 250 | -1,074 (-81%) | M |
| iterate.md | 1,120 | 280 | -840 (-75%) | M |
| visual-commit.md | 996 | 280 | -716 (-72%) | M |
| compare.md | 937 | 300 | -637 (-68%) | M |
| implement-design.md | 905 | 280 | -625 (-69%) | M |
| screenshot.md | 809 | 250 | -559 (-69%) | M |
| **TOTAL** | **8,656** | **1,640** | **-7,016** | **2 days** |

**What to Cut**:
- ❌ Full workflow explanations (that's the agent's job)
- ❌ Extensive CSS/HTML code examples (1-2 examples max)
- ❌ Framework duplication (React+Tailwind AND plain CSS)
- ❌ Step-by-step procedures duplicated from skills
- ❌ Repetitive error handling scenarios

**What to Keep**:
- ✅ Mission and critical rules (15-25 lines)
- ✅ Stage activation instructions (10-20 lines)
- ✅ 1-2 representative examples (30-50 lines)
- ✅ Transition logic (10-15 lines)
- ✅ Reference to agent/skills for details

**Implementation Pattern**:
```markdown
# /command-name - Stage Name

Activates Stage N of visual-iteration-agent.md

## Mission
[15-20 lines: Clear, focused mission statement]

## Quick Checklist
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Example (Representative)
[30-40 lines: ONE concrete example showing pattern]

## Guardrails
- DO NOT [critical prohibition 1]
- DO NOT [critical prohibition 2]

## Transition
Ready for next stage? Use `/next-command` when [criteria].

See visual-iteration-agent.md Stage N for full guidance.
```

**Success Criteria**:
- [ ] Each command 200-300 lines (currently 800-1,300)
- [ ] No framework duplication (currently 2-3 variants per example)
- [ ] Clear agent reference (link to full guidance)
- [ ] 1-2 examples max per command (currently 5-10+)
- [ ] All commands still functional after reduction

#### epti Commands

| File | Current | Target | Reduction | Effort |
|------|---------|--------|-----------|--------|
| iterate.md | 548 | 200 | -348 (-64%) | M |
| commit-code.md | 534 | 180 | -354 (-66%) | M |
| implement.md | 469 | 180 | -289 (-62%) | M |
| commit-tests.md | 455 | 180 | -275 (-60%) | M |
| write-tests.md | 429 | 180 | -249 (-58%) | M |
| verify-fail.md | 370 | 150 | -220 (-59%) | M |
| **TOTAL** | **2,805** | **1,070** | **-1,735** | **1.5 days** |

**Reduction Strategy**:
- Cut lines 22-74 of write-tests.md (framework detection examples) to 10 lines
- Eliminate repetitive anti-pattern sections (stated 6+ times)
- Consolidate git operations to single reference
- Remove TDD philosophy (that's tdd-agent.md's job)
- Keep core procedures, trim examples from 6 frameworks → 1-2

#### agent-loop Commands

| File | Current | Target | Reduction | Effort |
|------|---------|--------|-----------|--------|
| commit.md | 124 | 80 | -44 (-35%) | S |
| code.md | 88 | 60 | -28 (-32%) | S |
| plan.md | 73 | 50 | -23 (-32%) | S |
| explore.md | 57 | 40 | -17 (-30%) | S |
| **TOTAL** | **342** | **230** | **-112** | **0.5 days** |

**Reduction Strategy**:
- These are already better-sized, trim redundancy only
- Remove overlap with workflow-agent.md stage descriptions
- Condense from "full explanation" to "activation trigger"

**Validation**:
```bash
# After command reduction
just validate  # Ensure commands still load
just test      # Ensure structure tests pass
# Manual: Test each command in Claude Code
```

### Initiative 1.2: Framework Example Consolidation (P0)

**Target**: -2,000 lines of framework duplication

**Current State**:
- 6 framework examples per concept (Python, JavaScript, Go, Java, Ruby, TypeScript)
- Repeated across agents, commands, skills
- Multiplication factor: 5-6x

**Reduction Strategy**:

1. **Agents**: Framework-agnostic principles only
   - Remove specific framework examples
   - Mention "works with pytest, jest, go test, JUnit, RSpec"
   - No code examples at agent level

2. **Commands**: 1-2 representative examples
   - Python + JavaScript (most common)
   - Note: "Adapt for your framework"
   - Remove Go, Java, Ruby, TypeScript examples

3. **Skills**: Generic procedures with minimal code
   - Pseudocode where possible
   - 1 representative example if needed
   - Framework detection logic condensed to 10 lines

**Files to Modify**:
- epti/agents/tdd-agent.md: Remove lines 94-100 framework list duplication
- epti/commands/write-tests.md: Trim lines 22-74 to 10 lines
- epti/skills/test-generation/SKILL.md: Consolidate 6 examples → 2
- epti/skills/test-execution/SKILL.md: Consolidate 6 examples → 2
- visual-iteration commands: Remove React+Tailwind + Plain CSS duplication → 1 variant

**Success Criteria**:
- [ ] No file contains 5+ framework examples
- [ ] Agent files mention frameworks in list form only
- [ ] Commands contain max 2 framework examples
- [ ] Skills use pseudocode where possible
- [ ] Framework reduction: 6 → 1-2 per file

**Validation**:
```bash
# Check for excessive framework mentions
grep -r "Python.*JavaScript.*Go.*Java.*Ruby" plugins/*/
# Should return minimal results after reduction
```

### Initiative 1.3: Layer Redundancy Elimination (P1)

**Target**: -2,500 lines of agent/command/skill overlap

**Problem**: Three layers repeat same content
```
AGENT (workflow) → 40-60% overlap → COMMAND (activation) → 30-50% overlap → SKILL (execution)
```

**Solution**: Clear separation of concerns

#### Agent Layer (KEEP)
**Purpose**: High-level workflow orchestration
**Content**:
- ✅ Stage definitions and transitions
- ✅ Overall philosophy and principles
- ✅ Anti-patterns and guardrails
- ✅ When to invoke commands
- ❌ Detailed procedures (that's skills)
- ❌ Specific examples (that's commands/skills)
- ❌ Git commands (that's skills)

#### Command Layer (SIMPLIFY)
**Purpose**: Stage activation trigger
**Content**:
- ✅ Mission statement (1 sentence)
- ✅ Quick checklist (5-10 items)
- ✅ Critical guardrails (3-5 items)
- ✅ Transition criteria
- ✅ Reference to agent for full guidance
- ❌ Full workflow explanations (redundant with agent)
- ❌ Detailed procedures (redundant with skills)
- ❌ Multiple examples (1-2 max)

#### Skill Layer (STREAMLINE)
**Purpose**: Executable procedures
**Content**:
- ✅ Step-by-step procedures
- ✅ Tool invocation patterns
- ✅ Minimal examples (1-2)
- ✅ Error handling (critical cases only)
- ❌ Philosophy and principles (redundant with agent)
- ❌ Workflow explanations (redundant with agent)
- ❌ Anti-patterns (redundant with agent)

**Reduction Pattern by File**:

1. **agent-loop/commands/explore.md** (80% overlap with agent Stage 1)
   - Current: 57 lines duplicating agent guidance
   - Target: 40 lines referencing agent guidance
   - Remove: Lines restating Stage 1 description verbatim

2. **agent-loop/commands/plan.md** (similar pattern)
   - Current: 73 lines
   - Target: 50 lines
   - Remove: Redundant workflow explanation

3. Apply pattern across all 16 commands

**Success Criteria**:
- [ ] Agent files contain workflow, not procedures
- [ ] Command files reference agent, not duplicate
- [ ] Skill files contain procedures, not philosophy
- [ ] No more than 20% content overlap between layers
- [ ] Each layer serves distinct purpose

**Validation**:
```bash
# Check for redundant phrases across layers
# Example: "Tests must fail first" should appear in agent, not in 5+ files
grep -r "Tests must fail first" plugins/epti/ | wc -l
# Should be 1-2 occurrences, not 6+
```

### Phase 1 Summary

**Total Reduction**: -11,500 lines (-47%)
- Commands: -8,893 lines
- Framework duplication: -2,000 lines
- Layer redundancy: -2,500 lines
- Some overlap in counting (commands reduction includes some framework/layer work)

**Effort**: 3-5 days (Medium)
**Risk**: Low (redundant content, tests validate)

**Deliverables**:
- [ ] All commands 75-300 lines (from 57-1,324)
- [ ] Framework examples: 1-2 per file (from 5-6)
- [ ] Layer separation: agent→command→skill with <20% overlap
- [ ] All 60+ tests passing
- [ ] `just validate` passing
- [ ] Git branch: `phase-1-command-reduction`

**Validation Checklist**:
```bash
# Structure validation
just validate

# Test suite
just test

# Line count verification
./scripts/count-lines.sh  # Should show ~13,000 lines

# Manual testing
# - Test each command in Claude Code
# - Verify commands still trigger correct behaviors
# - Confirm agent guidance still accessible
```

---

## Phase 2: High-Impact Reduction (P2)

**Goal**: Reduce skills and READMEs to optimal lengths
**Target**: -8,700 lines (cumulative -67% from start)
**Effort**: 3-4 days (Medium)
**Risk**: Low-Medium (some valuable examples will be trimmed)

### Initiative 2.1: Skills Reduction

**Target**: Reduce skills from 9,272 → 4,030 lines (-5,242 lines, -57%)

**Optimal Skill Length**: 250-400 lines (current avg: 692 lines)

#### visual-iteration Skills

| File | Current | Target | Reduction | Effort |
|------|---------|--------|-----------|--------|
| design-implementation/SKILL.md | 1,232 | 480 | -752 (-61%) | M |
| visual-refinement/SKILL.md | 1,137 | 450 | -687 (-60%) | M |
| visual-comparison/SKILL.md | 1,070 | 420 | -650 (-61%) | M |
| screenshot-capture/SKILL.md | 730 | 350 | -380 (-52%) | M |
| **TOTAL** | **4,475** | **1,700** | **-2,775** | **2 days** |

**Reduction Strategy**:
- Remove CSS/HTML code examples (keep 1-2, remove 8-10)
- Eliminate framework duplication (React vs. plain)
- Condense procedures from verbose to checklist
- Remove obvious error scenarios (keep critical only)

**Pattern for visual-comparison/SKILL.md** (1,070 → 420 lines):
```markdown
---
name: visual-comparison
description: Compare before/after screenshots and generate specific visual feedback with measurements
---

# Visual Comparison Skill

## Purpose
[20 lines: What this skill does, when Claude invokes it]

## Core Procedure
[100 lines: Step-by-step comparison methodology]

## Feedback Format
[50 lines: Structure of output, specificity requirements]

## Example (One Representative)
[150 lines: ONE complete before/after comparison example]

## Critical Edge Cases
[50 lines: Only non-obvious error scenarios]

## Tool Integration
[50 lines: How to use browser-tools MCP if available]
```

#### epti Skills

| File | Current | Target | Reduction | Effort |
|------|---------|--------|-----------|--------|
| refactoring/SKILL.md | 715 | 320 | -395 (-55%) | M |
| test-execution/SKILL.md | 652 | 300 | -352 (-54%) | M |
| test-generation/SKILL.md | 585 | 280 | -305 (-52%) | M |
| implementation-with-protection/SKILL.md | 574 | 280 | -294 (-51%) | M |
| overfitting-detection/SKILL.md | 508 | 250 | -258 (-51%) | M |
| **TOTAL** | **3,034** | **1,430** | **-1,604** | **1.5 days** |

**Reduction Strategy**:
- Consolidate 6 framework examples → 1-2
- Remove TDD philosophy (redundant with tdd-agent.md)
- Trim test running examples from 40+ lines to 10 lines
- Convert code snippets to pseudocode where possible

#### agent-loop Skills

| File | Current | Target | Reduction | Effort |
|------|---------|--------|-----------|--------|
| git-operations/SKILL.md | 625 | 300 | -325 (-52%) | M |
| verification/SKILL.md | 466 | 250 | -216 (-46%) | M |
| plan-generation/SKILL.md | 430 | 200 | -230 (-53%) | M |
| code-exploration/SKILL.md | 242 | 150 | -92 (-38%) | S |
| **TOTAL** | **1,763** | **900** | **-863** | **1 day** |

**Reduction Strategy**:
- git-operations: 625→300 (remove repetitive git command examples, consolidate commit templates)
- verification: 466→250 (trim test framework examples)
- plan-generation: 430→200 (remove extensive dependency examples)
- code-exploration: 242→150 (already reasonable, light trim)

**Success Criteria**:
- [ ] All skills 250-400 lines (currently 242-1,232)
- [ ] YAML frontmatter preserved (critical for discovery)
- [ ] Core procedures intact
- [ ] Examples reduced to 1-2 per skill
- [ ] No framework duplication
- [ ] All skills still invokable by Claude

**Validation**:
```bash
# Check YAML frontmatter intact
python tests/functional/test_skills_structure.py -k frontmatter

# Verify line counts
find plugins/*/skills -name "SKILL.md" -exec wc -l {} \; | awk '{print $1}' | sort -n
# Should all be 250-400 range

# Full test suite
just test
```

### Initiative 2.2: README Condensation

**Target**: Reduce READMEs from 4,272 → 1,050 lines (-3,222 lines, -75%)

**Current Problem**: READMEs are comprehensive tutorials for humans, but plugins are FOR Claude

**Solution**: Convert from tutorial to reference documentation

#### visual-iteration/README.md (2,319 → 500 lines)

**Current Structure** (problems):
- 2,319 lines of detailed workflow explanations
- Extensive examples for every command
- Multi-page user guide format
- Teaches visual iteration concepts in depth

**Target Structure** (solutions):
```markdown
# visual-iteration Plugin

## Quick Start
[50 lines: Installation, basic usage, first screenshot]

## Command Reference
[200 lines: Brief description of each command, when to use]

## Workflow Overview
[100 lines: High-level flow, typical cycles]

## MCP Integration
[50 lines: browser-tools setup]

## Examples
[100 lines: 2-3 complete examples, not 10+]
```

**What to Cut**:
- ❌ Detailed command explanations (that's the command files)
- ❌ Extensive CSS/HTML tutorials (not relevant to plugin)
- ❌ Multiple framework variants
- ❌ Deep-dive educational content
- ❌ Philosophy of visual iteration (that's the agent)

**What to Keep**:
- ✅ Installation instructions
- ✅ Quick start guide
- ✅ Command list with 1-line descriptions
- ✅ 2-3 representative examples
- ✅ MCP setup guide

#### epti/README.md (1,238 → 350 lines)

**Reduction Pattern**:
```markdown
# epti Plugin

## Overview
[30 lines: What is TDD plugin, why use it]

## Quick Start
[50 lines: Installation, first test cycle]

## TDD Workflow
[100 lines: 6-stage overview, minimal detail]

## Command Reference
[100 lines: 6 commands, brief descriptions]

## Examples
[70 lines: 1-2 complete TDD cycles]
```

**Cut**: Detailed TDD education, extensive examples, framework tutorials (1,238 → 350)

#### agent-loop/README.md (715 → 200 lines)

**Reduction Pattern**:
```markdown
# agent-loop Plugin

## Overview
[30 lines: Agentic workflow plugin purpose]

## Quick Start
[40 lines: Installation, first workflow]

## Workflow Stages
[60 lines: 4-stage overview]

## Command Reference
[40 lines: 4 commands]

## Examples
[30 lines: 1 complete cycle]
```

**Cut**: Extensive workflow explanations, multiple examples (715 → 200)

**Success Criteria**:
- [ ] visual-iteration README ≤ 500 lines (from 2,319)
- [ ] epti README ≤ 350 lines (from 1,238)
- [ ] agent-loop README ≤ 200 lines (from 715)
- [ ] All READMEs focus on reference, not tutorial
- [ ] Quick start section < 50 lines each
- [ ] Examples reduced to 1-2 per README

### Initiative 2.3: Git Operations Consolidation

**Target**: -1,000 lines of git duplication

**Current Problem**: Git commands and commit templates repeated across 8+ files

**Files Containing Git Guidance**:
- agent-loop/skills/git-operations/SKILL.md (625 lines)
- agent-loop/commands/commit.md (124 lines)
- epti/commands/commit-tests.md (455 lines)
- epti/commands/commit-code.md (534 lines)
- visual-iteration/commands/visual-commit.md (996 lines)
- Others (various agent/skill references)

**Reduction Strategy**:

1. **Consolidate to Single Source**: agent-loop/skills/git-operations/SKILL.md
   - Reduce from 625 → 300 lines
   - Contains: Core git procedures, commit message format, common operations
   - Remove: Repetitive examples, obvious git commands

2. **Commands Reference Skill**: All commit commands just reference git-operations
   - commit.md: 124 → 80 lines (remove duplicated git guidance)
   - commit-tests.md: 455 → 180 lines (remove git operations, keep TDD-specific)
   - commit-code.md: 534 → 180 lines (remove git operations, keep TDD-specific)
   - visual-commit.md: 996 → 280 lines (remove git operations, keep visual-specific)

3. **Commit Message Templates**: One canonical template
   - Currently: 30-50 line templates repeated 4-6 times
   - Target: Template in git-operations, others reference it

**Success Criteria**:
- [ ] git-operations/SKILL.md is single source of truth (300 lines)
- [ ] Commit commands reference skill, not duplicate (80-180 lines each)
- [ ] Commit message template appears once (not 4-6x)
- [ ] Git command examples consolidated (not scattered)

### Phase 2 Summary

**Total Reduction**: -8,700 lines (cumulative -67% from start)
- Skills: -5,242 lines
- READMEs: -3,222 lines
- Git consolidation: -1,000 lines (overlap with above)

**Effort**: 3-4 days (Medium)
**Risk**: Low-Medium (some examples trimmed, but core intact)

**Deliverables**:
- [ ] All skills 250-400 lines (from 242-1,232)
- [ ] All READMEs 200-500 lines (from 715-2,319)
- [ ] Git operations consolidated to single source
- [ ] All 60+ tests passing
- [ ] `just validate` passing
- [ ] Git branch: `phase-2-skills-readme-reduction`

**Validation Checklist**:
```bash
# Test suite (skills structure validation)
pytest tests/functional/test_skills_structure.py -v

# README validation (manual)
wc -l plugins/*/README.md
# visual-iteration: ~500 lines
# epti: ~350 lines
# agent-loop: ~200 lines

# Skill validation (manual)
find plugins/*/skills -name "SKILL.md" -exec wc -l {} \;
# All should be 250-400 range

# Full validation
just validate && just test
```

---

## Phase 3: Polish & Optimization (P3)

**Goal**: Final optimizations for consistency and effectiveness
**Target**: -1,800 lines (cumulative -69% from start, ~7,500 lines remaining)
**Effort**: 1-2 days (Low-Medium)
**Risk**: Medium (agents are core guidance, be careful)

### Initiative 3.1: Agent Optimization

**Target**: Trim agents from 1,788 → 1,206 lines (-582 lines, -33%)

#### visual-iteration/agents/visual-iteration-agent.md (946 → 600 lines)

**Current Assessment** (from STATUS):
- Lines 1-466: Core workflow (KEEP - excellent)
- Lines 467-636: Supporting patterns (KEEP - valuable)
- Lines 637-946: Fluff and repetition (TRIM 50%)

**Reduction Strategy**:
- Lines 641-657: Good/bad feedback examples (8+ examples → 3-4 examples)
- Lines 810-946: Error handling and communication (consolidate repetition)
- Keep all 6 workflow stages intact (critical)
- Keep MCP integration patterns (valuable)
- Keep subagent coordination (unique value)

**Target**: 600 lines (-346 lines, -37%)

#### epti/agents/tdd-agent.md (636 → 400 lines)

**Current Assessment** (from STATUS):
- Lines 1-62: Philosophy (valuable but verbose)
- Lines 63-407: 6-stage workflow (KEEP - core value)
- Lines 408-496: Anti-patterns (KEEP - valuable)
- Lines 497-563: Framework integration (condense)
- Lines 564-637: Quality checklist (condense)

**Reduction Strategy**:
- Lines 94-100: Framework detection (condense to list)
- Lines 183-196: Git commands (reference git-operations skill)
- Lines 500-541: Test running examples (40+ lines → 10 lines)
- Keep TDD principles (foundation)
- Keep 6-stage workflow (core)
- Keep anti-patterns (valuable)

**Target**: 400 lines (-236 lines, -37%)

#### agent-loop/agents/workflow-agent.md (206 → 206 lines)

**Status**: Already optimal length ✅

**Evidence from STATUS**: "This is actually well-sized... No reduction needed."

**Action**: KEEP AS IS (206 lines, 0% reduction)

**Success Criteria**:
- [ ] visual-iteration agent ≤ 600 lines (from 946)
- [ ] epti agent ≤ 400 lines (from 636)
- [ ] agent-loop agent unchanged (206 lines)
- [ ] All workflow stages preserved
- [ ] Core principles intact
- [ ] Examples reduced, not eliminated

### Initiative 3.2: Pseudocode Conversion

**Target**: -1,500 lines by converting code snippets to pseudocode

**Problem**: Full CSS/HTML/Python/JavaScript examples bloat files

**Solution**: Generic pseudocode for patterns, real code only when necessary

**Files to Convert** (highest impact):
1. visual-iteration commands (CSS/HTML examples)
2. visual-iteration skills (CSS patterns)
3. epti skills (test framework code)
4. agent-loop skills (minimal, already reasonable)

**Conversion Pattern**:

**Before** (CSS example, ~25 lines):
```markdown
[React + Tailwind]
Change:
- Heading: `text-2xl` → `text-3xl` (24px → 32px)
- Input labels: `text-xs` → `text-sm` (12px → 14px)

[Plain CSS]
Change in styles.css:
.heading {
  font-size: 24px; /* REMOVE */
  font-size: 32px; /* ADD */
}

.login-heading {
  margin-bottom: 24px; /* REMOVE */
  margin-bottom: 32px; /* ADD */
}
```

**After** (pseudocode, ~8 lines):
```markdown
[Generic Pattern]
Increase heading size: 24px → 32px
Increase label size: 12px → 14px
Increase spacing: 24px → 32px

(Adapt to your CSS framework: Tailwind classes, plain CSS, CSS-in-JS)
```

**Files to Modify**:
- visual-iteration/commands/*.md (convert CSS examples)
- visual-iteration/skills/*.md (convert CSS patterns)
- epti/skills/test-generation/SKILL.md (convert test code → pseudocode)
- epti/skills/implementation-with-protection/SKILL.md (convert implementation code)

**Scope Limits** (keep real code when):
- ✅ MCP integration examples (technical, necessary)
- ✅ Git command examples (literal, not patterns)
- ✅ Test framework detection (needs real file patterns)
- ✅ One representative example per concept

**Success Criteria**:
- [ ] CSS examples reduced from ~50 to ~15 across visual-iteration
- [ ] Test framework code examples reduced from 6 → 1-2
- [ ] Implementation examples converted to pseudocode patterns
- [ ] No more than 1 real code example per concept
- [ ] Patterns described generically

### Initiative 3.3: Final Consistency Pass

**Target**: -300 lines through consistency improvements

**Focus Areas**:

1. **Remove Repetitive Anti-Patterns**
   - Check for phrases appearing 4+ times across files
   - Consolidate to agent, remove from commands/skills
   - Example: "DO NOT write implementation during test phase" (appears 6+ times in epti)

2. **Consolidate Quality Guidelines**
   - visual-iteration agent lines 637-809 contain repetitive quality guidance
   - Trim redundant examples
   - Keep unique guidelines

3. **Remove Obvious Error Scenarios**
   - Skills contain 50-100 lines of error handling
   - Remove obvious cases ("file not found", "command not available")
   - Keep non-obvious cases

4. **Trim Extended Philosophy Sections**
   - Introduction sections: 50-75 lines → 10-15 lines
   - Keep core principles, remove extended explanations

**Success Criteria**:
- [ ] No phrase appears 4+ times verbatim across files
- [ ] Obvious error scenarios removed
- [ ] Philosophy sections concise (10-20 lines max)
- [ ] Consistency across all three plugins

### Phase 3 Summary

**Total Reduction**: -1,800 lines (cumulative -69% from start)
- Agents: -582 lines
- Pseudocode conversion: -1,500 lines
- Consistency pass: -300 lines (some overlap with above)

**Effort**: 1-2 days (Low-Medium)
**Risk**: Medium (agents are core, be careful)

**Deliverables**:
- [ ] Agents at optimal length (206-600 lines)
- [ ] Code examples converted to pseudocode where appropriate
- [ ] Consistency across all plugins
- [ ] All 60+ tests passing
- [ ] `just validate` passing
- [ ] Git branch: `phase-3-polish-optimization`

**Validation Checklist**:
```bash
# Agent line counts
wc -l plugins/*/agents/*.md
# visual-iteration: ~600 lines
# epti: ~400 lines
# agent-loop: ~206 lines

# Pseudocode conversion check (manual)
grep -r "React + Tailwind" plugins/visual-iteration/
# Should be minimal occurrences

# Full validation
just validate && just test

# Final line count
./scripts/count-lines.sh
# Should show ~7,500-8,000 lines total
```

---

## Success Metrics & Validation

### Quantitative Metrics

| Metric | Start | Phase 1 | Phase 2 | Phase 3 | Target |
|--------|-------|---------|---------|---------|--------|
| **Total Lines** | 24,459 | ~13,000 | ~8,000 | ~7,500 | 9,000-12,000 ✅ |
| **Commands Avg** | 723 lines | ~182 lines | ~182 lines | ~182 lines | 75-200 ✅ |
| **Skills Avg** | 692 lines | ~692 lines | ~310 lines | ~310 lines | 250-400 ✅ |
| **Agents Avg** | 596 lines | ~596 lines | ~596 lines | ~402 lines | 300-500 ✅ |
| **READMEs Avg** | 1,424 lines | ~1,424 lines | ~350 lines | ~350 lines | 200-500 ✅ |

### Qualitative Metrics

**Signal-to-Noise Ratio**:
- Start: 40% signal, 60% noise
- Target: 75% signal, 25% noise
- Measurement: Manual review of reduced files for value density

**Layer Separation**:
- Start: 40-60% overlap between layers
- Target: <20% overlap between layers
- Measurement: Grep for duplicate phrases across agent/command/skill

**Framework Duplication**:
- Start: 5-6 examples per concept
- Target: 1-2 examples per concept
- Measurement: Count framework mentions per file

**File Length Distribution**:
- Start: 24/32 files outside optimal range (75%)
- Target: <25% files outside optimal range
- Measurement: Count files exceeding targets

### Test Validation

**Critical Test Suite**: `pytest tests/functional/test_skills_structure.py`

Tests validate:
- ✅ Directory structure (13 skills in correct locations)
- ✅ YAML frontmatter (name + description fields)
- ✅ File existence (SKILL.md files present)
- ✅ Content size (no empty stubs)
- ✅ Configuration validity (plugin.json, marketplace.json)

**Validation Commands**:
```bash
# Structure validation
just validate

# Test suite (60+ tests)
just test

# JSON validation
jq empty .claude-plugin/marketplace.json
find plugins -name "*.json" -exec jq empty {} \;

# Line count verification
./scripts/count-lines.sh

# Manual testing checklist
# [ ] Load marketplace in Claude Code
# [ ] Test each command in each plugin
# [ ] Verify agent behaviors
# [ ] Confirm skill invocation
# [ ] Check hook execution
```

### Effectiveness Validation

**Before/After Comparison** (manual testing):

1. **Command Effectiveness**:
   - Test: Invoke `/compare` with 1,324-line version vs. 250-line version
   - Measure: Does Claude follow guidance correctly in both?
   - Hypothesis: Shorter version performs equally or better

2. **Skill Invocation**:
   - Test: Trigger visual-comparison skill (1,070 lines vs. 420 lines)
   - Measure: Does Claude invoke skill appropriately in both?
   - Hypothesis: Shorter version triggers more reliably (better description focus)

3. **Agent Adherence**:
   - Test: Run full visual-iteration workflow (946-line agent vs. 600-line agent)
   - Measure: Does Claude follow 6-stage workflow correctly in both?
   - Hypothesis: Shorter version maintains adherence (less distraction)

**Success Threshold**: Reduced versions perform ≥ 95% as effective as original versions

---

## Risk Mitigation & Rollback

### Risk Register

| Risk | Probability | Impact | Mitigation | Rollback |
|------|------------|--------|------------|----------|
| **Loss of Clarity** | Low | Medium | Keep core procedures intact, preserve examples | Git revert branch |
| **Skill Non-Invocation** | Low | High | Preserve YAML descriptions, test extensively | Restore SKILL.md from backup |
| **Command Malfunction** | Low | High | Validate after each reduction, manual testing | Git revert specific commands |
| **Test Failures** | Low | High | Run `just test` after every change | Git revert branch |
| **Framework Confusion** | Low-Med | Medium | Keep 1-2 representative examples | Add back examples if needed |
| **Git Operations Break** | Very Low | High | Consolidate carefully, test commits | Restore git-operations skill |

### Rollback Strategy

**Per-Phase Rollback**:
```bash
# If Phase 1 causes issues
git checkout main
git branch -D phase-1-command-reduction

# If Phase 2 causes issues
git checkout phase-1-command-reduction
git branch -D phase-2-skills-readme-reduction

# If Phase 3 causes issues
git checkout phase-2-skills-readme-reduction
git branch -D phase-3-polish-optimization
```

**Per-File Rollback**:
```bash
# Restore specific file from previous phase
git checkout phase-1-command-reduction -- plugins/visual-iteration/commands/compare.md
```

**Per-Plugin Rollback**:
```bash
# Restore entire plugin
git checkout main -- plugins/visual-iteration/
```

### Validation Gates (Must Pass to Proceed)

**Gate 1: After Phase 1**
- [ ] `just validate` passes
- [ ] `just test` passes (60+ tests)
- [ ] All commands still loadable in Claude Code
- [ ] Manual test: Run 1 command from each plugin
- [ ] Line count: ~13,000 lines

**Gate 2: After Phase 2**
- [ ] All Phase 1 gates still passing
- [ ] Skills still invokable (test descriptions)
- [ ] READMEs still render correctly
- [ ] Manual test: Run 1 skill from each plugin
- [ ] Line count: ~8,000 lines

**Gate 3: After Phase 3**
- [ ] All Phase 1 & 2 gates still passing
- [ ] Agents still guide workflow correctly
- [ ] Pseudocode examples understandable
- [ ] Manual test: Run full workflow in 1 plugin
- [ ] Line count: ~7,500 lines

**Final Release Gate**
- [ ] All gates passing
- [ ] Effectiveness validation complete (before/after comparison)
- [ ] Documentation updated (CLAUDE.md, ARCHITECTURE.md)
- [ ] Manual testing: Full workflow in all 3 plugins
- [ ] Performance: No degradation in Claude response quality

---

## Implementation Timeline

### Phase 1: Critical Reduction (3-5 days)

**Day 1-2: Commands (visual-iteration)**
- Monday: load-mock.md (1,324→250), iterate.md (1,120→280), visual-commit.md (996→280)
- Tuesday: compare.md (937→300), implement-design.md (905→280), screenshot.md (809→250)
- Validation: `just validate && just test`

**Day 3: Commands (epti)**
- Wednesday: All 6 epti commands (2,805→1,070)
- Validation: `just validate && just test`

**Day 4: Commands (agent-loop) + Framework Consolidation**
- Thursday AM: All 4 agent-loop commands (342→230)
- Thursday PM: Framework example consolidation across all plugins
- Validation: `just validate && just test`

**Day 5: Layer Redundancy Elimination**
- Friday: Remove agent/command/skill overlap across all plugins
- Validation: `just validate && just test`
- Gate 1 validation

**Deliverable**: Git branch `phase-1-command-reduction`, ~13,000 lines

---

### Phase 2: Skills & READMEs (3-4 days)

**Day 6-7: Skills (visual-iteration & epti)**
- Monday: visual-iteration skills (4,475→1,700)
- Tuesday: epti skills (3,034→1,430)
- Validation: `pytest tests/functional/test_skills_structure.py -v`

**Day 8: Skills (agent-loop) + Git Consolidation**
- Wednesday AM: agent-loop skills (1,763→900)
- Wednesday PM: Git operations consolidation
- Validation: `just test`

**Day 9: READMEs**
- Thursday: All 3 plugin READMEs (4,272→1,050)
- Validation: `just validate && just test`
- Gate 2 validation

**Deliverable**: Git branch `phase-2-skills-readme-reduction`, ~8,000 lines

---

### Phase 3: Polish & Optimization (1-2 days)

**Day 10: Agents + Pseudocode**
- Friday AM: Agent optimization (visual-iteration, epti)
- Friday PM: Pseudocode conversion (commands & skills)
- Validation: `just validate && just test`

**Day 11: Final Pass**
- Monday: Consistency pass, final cleanup
- Final validation: All gates, effectiveness testing
- Documentation updates (CLAUDE.md, ARCHITECTURE.md)

**Deliverable**: Git branch `phase-3-polish-optimization`, ~7,500 lines

---

### Total Timeline: 8-11 days (2-3 weeks)

**Buffer**: 3 days for unexpected issues, additional testing, documentation

**Estimated Completion**: Mid-November 2025

---

## Dependencies & Prerequisites

### Required Before Starting

- [ ] Current implementation 100% functional (VERIFIED ✅)
- [ ] All 60+ tests passing (VERIFIED ✅)
- [ ] `just validate` passing (VERIFIED ✅)
- [ ] Git repository clean (no uncommitted changes)
- [ ] Baseline metrics documented (24,459 lines, current file sizes)
- [ ] Backup of full repository (local + cloud)

### Tools Required

- [ ] Claude Code CLI (`claude` command available)
- [ ] pytest (`pytest tests/` works)
- [ ] jq (JSON validation)
- [ ] just (task automation)
- [ ] Git (version control)
- [ ] Line counting script (`./scripts/count-lines.sh` or equivalent)

### Knowledge Required

- Understanding of Claude Code plugin system
- Familiarity with all 3 plugins (agent-loop, epti, visual-iteration)
- Awareness of test suite structure
- Git branching and merging workflow

---

## Post-Reduction Work

### Documentation Updates

After Phase 3 completion, update:

1. **CLAUDE.md**:
   - Update line count statistics (24,459 → ~7,500)
   - Update component counts (commands 723 avg → 182 avg)
   - Update "Current State" section
   - Mark verbosity issue as RESOLVED

2. **ARCHITECTURE.md**:
   - Update Repository Statistics section (line counts)
   - Update component characteristics (optimal lengths)
   - Add note on verbosity reduction (v1.0 → v1.1)

3. **README.md**:
   - Update plugin descriptions if needed
   - Ensure line counts accurate

4. **Plugin READMEs**:
   - Already updated during Phase 2 (part of reduction)

### Performance Validation

**Measure effectiveness improvement**:

1. **Before Reduction** (baseline):
   - Time to process 1,324-line command: [measure]
   - Claude adherence rate: [measure through testing]
   - User cognitive load: [subjective assessment]

2. **After Reduction**:
   - Time to process 250-line command: [measure]
   - Claude adherence rate: [measure through testing]
   - User cognitive load: [subjective assessment]

3. **Expected Improvements**:
   - Faster command processing
   - Better adherence (less distraction)
   - Lower cognitive load (easier to understand)

### Future Optimization

**Potential future work** (not in this plan):

1. **Shared Skills Library**:
   - Extract common skills (git-operations) to shared library
   - Reduce duplication across plugins
   - Version management for skills

2. **Dynamic Content Generation**:
   - Generate framework examples on-demand
   - Reduce static content further
   - Personalize to user's tech stack

3. **Continuous Monitoring**:
   - Track file growth over time
   - Alert if files exceed optimal ranges
   - Automated verbosity detection

---

## Appendix: File-by-File Reduction Targets

### Complete Reduction Matrix

#### agent-loop Plugin (3,021 → 1,506 lines, -50%)

| File | Current | Target | Reduction | Phase | Effort |
|------|---------|--------|-----------|-------|--------|
| agents/workflow-agent.md | 206 | 206 | 0 (0%) | - | - |
| commands/explore.md | 57 | 40 | -17 (-30%) | 1 | S |
| commands/plan.md | 73 | 50 | -23 (-32%) | 1 | S |
| commands/code.md | 88 | 60 | -28 (-32%) | 1 | S |
| commands/commit.md | 124 | 80 | -44 (-35%) | 1 | S |
| skills/code-exploration/SKILL.md | 242 | 150 | -92 (-38%) | 2 | S |
| skills/plan-generation/SKILL.md | 430 | 200 | -230 (-53%) | 2 | M |
| skills/verification/SKILL.md | 466 | 250 | -216 (-46%) | 2 | M |
| skills/git-operations/SKILL.md | 625 | 300 | -325 (-52%) | 2 | M |
| README.md | 715 | 200 | -515 (-72%) | 2 | M |
| **TOTAL** | **3,021** | **1,536** | **-1,485** | | **2 days** |

#### epti Plugin (7,688 → 3,250 lines, -58%)

| File | Current | Target | Reduction | Phase | Effort |
|------|---------|--------|-----------|-------|--------|
| agents/tdd-agent.md | 636 | 400 | -236 (-37%) | 3 | M |
| commands/write-tests.md | 429 | 180 | -249 (-58%) | 1 | M |
| commands/verify-fail.md | 370 | 150 | -220 (-59%) | 1 | M |
| commands/commit-tests.md | 455 | 180 | -275 (-60%) | 1 | M |
| commands/implement.md | 469 | 180 | -289 (-62%) | 1 | M |
| commands/iterate.md | 548 | 200 | -348 (-64%) | 1 | M |
| commands/commit-code.md | 534 | 180 | -354 (-66%) | 1 | M |
| skills/test-generation/SKILL.md | 585 | 280 | -305 (-52%) | 2 | M |
| skills/test-execution/SKILL.md | 652 | 300 | -352 (-54%) | 2 | M |
| skills/implementation-with-protection/SKILL.md | 574 | 280 | -294 (-51%) | 2 | M |
| skills/overfitting-detection/SKILL.md | 508 | 250 | -258 (-51%) | 2 | M |
| skills/refactoring/SKILL.md | 715 | 320 | -395 (-55%) | 2 | M |
| README.md | 1,238 | 350 | -888 (-72%) | 2 | M |
| **TOTAL** | **7,688** | **3,250** | **-4,438** | | **4 days** |

#### visual-iteration Plugin (12,750 → 4,440 lines, -65%)

| File | Current | Target | Reduction | Phase | Effort |
|------|---------|--------|-----------|-------|--------|
| agents/visual-iteration-agent.md | 946 | 600 | -346 (-37%) | 3 | M |
| commands/load-mock.md | 1,324 | 250 | -1,074 (-81%) | 1 | M |
| commands/implement-design.md | 905 | 280 | -625 (-69%) | 1 | M |
| commands/screenshot.md | 809 | 250 | -559 (-69%) | 1 | M |
| commands/compare.md | 937 | 300 | -637 (-68%) | 1 | M |
| commands/iterate.md | 1,120 | 280 | -840 (-75%) | 1 | M |
| commands/visual-commit.md | 996 | 280 | -716 (-72%) | 1 | M |
| skills/design-implementation/SKILL.md | 1,232 | 480 | -752 (-61%) | 2 | M |
| skills/visual-refinement/SKILL.md | 1,137 | 450 | -687 (-60%) | 2 | M |
| skills/visual-comparison/SKILL.md | 1,070 | 420 | -650 (-61%) | 2 | M |
| skills/screenshot-capture/SKILL.md | 730 | 350 | -380 (-52%) | 2 | M |
| README.md | 2,319 | 500 | -1,819 (-78%) | 2 | M |
| **TOTAL** | **12,750** | **4,440** | **-8,310** | | **5 days** |

---

## Questions & Decisions Log

### Q1: Should we tackle one plugin at a time or all in parallel?

**Decision**: Work across all plugins in same phase (e.g., all commands in Phase 1)

**Rationale**:
- Consistency: Apply same patterns across all plugins
- Learning: Patterns learned in one plugin apply to others
- Testing: Can compare effectiveness across plugins
- Efficiency: Batch similar work together

**Alternative Rejected**: One plugin at a time (slower, inconsistent patterns)

---

### Q2: Should commands be reduced before skills or vice versa?

**Decision**: Commands first (Phase 1), then skills (Phase 2)

**Rationale**:
- Commands have worse bloat (75% vs. 57%)
- Commands reference skills, easier to update references
- Commands are explicit invocations, higher user visibility
- Skills can be optimized knowing command structure

**Alternative Rejected**: Skills first (would complicate command references)

---

### Q3: How to handle the three-layer redundancy systematically?

**Decision**: Clear separation pattern (agent = workflow, command = trigger, skill = procedure)

**Rationale**:
- Each layer serves distinct purpose
- Minimize overlap by defining boundaries
- Commands reference agent for full guidance
- Skills contain only procedures, no philosophy

**Implementation**:
- Phase 1: Establish pattern in commands (reference agent)
- Phase 2: Reinforce pattern in skills (remove philosophy)
- Phase 3: Final consistency in agents (trim duplication)

---

### Q4: What's the minimum viable content for each component type?

**Decision**:
- **Agents**: 300-600 lines (workflow, principles, transitions)
- **Commands**: 75-200 lines (mission, checklist, transition, reference)
- **Skills**: 250-400 lines (procedures, 1-2 examples, tool integration)
- **READMEs**: 200-500 lines (quick start, reference, 1-2 examples)

**Rationale**:
- Based on STATUS analysis of optimal lengths
- Balances completeness with conciseness
- Proven effective in agent-loop (commands avg 85 lines, already work well)
- Allows for complexity while preventing bloat

---

### Q5: How to test effectiveness after reduction?

**Decision**: Three-level validation

1. **Structural**: `just validate && just test` (automated)
2. **Functional**: Manual testing of each command/skill (manual)
3. **Effectiveness**: Before/after comparison testing (manual)

**Rationale**:
- Structural: Catches breaking changes immediately
- Functional: Verifies real-world usage still works
- Effectiveness: Confirms hypothesis (shorter = better)

**Metrics**:
- Pass/fail: All tests must pass
- Adherence: Claude follows guidance correctly
- Speed: Faster processing expected
- Quality: Output quality maintained or improved

---

### Q6: What's the rollback plan if reduction breaks things?

**Decision**: Git branches per phase + per-file granularity

**Strategy**:
1. Create branch per phase (easy phase-level rollback)
2. Commit per file or small batch (easy file-level rollback)
3. Tag before each phase (easy version restore)
4. Keep main untouched until all phases complete

**Rollback Options**:
- Entire phase: `git checkout phase-N-branch`
- Specific file: `git checkout <commit> -- <file>`
- Entire plugin: `git checkout main -- plugins/<plugin>/`

**Alternative Rejected**: Single large commit (hard to rollback granularly)

---

## Final Checklist

### Before Starting
- [ ] Read STATUS-2025-10-29-050659.md completely
- [ ] Understand current architecture from ARCHITECTURE.md
- [ ] Verify all tests passing (`just test`)
- [ ] Verify marketplace validation passing (`just validate`)
- [ ] Create baseline metrics (line counts per file)
- [ ] Back up repository (local + cloud)
- [ ] Create Phase 1 branch: `git checkout -b phase-1-command-reduction`

### After Phase 1
- [ ] All commands 75-300 lines
- [ ] Framework examples reduced to 1-2 per file
- [ ] Layer separation established
- [ ] `just validate` passing
- [ ] `just test` passing (60+ tests)
- [ ] Manual testing: 1 command per plugin
- [ ] Line count: ~13,000 lines
- [ ] Gate 1 validation complete
- [ ] Merge to main or create Phase 2 branch

### After Phase 2
- [ ] All skills 250-400 lines
- [ ] All READMEs 200-500 lines
- [ ] Git operations consolidated
- [ ] `just validate` passing
- [ ] `just test` passing
- [ ] Manual testing: 1 skill per plugin
- [ ] Line count: ~8,000 lines
- [ ] Gate 2 validation complete
- [ ] Merge to main or create Phase 3 branch

### After Phase 3
- [ ] All agents at optimal length
- [ ] Pseudocode conversion complete
- [ ] Consistency pass complete
- [ ] `just validate` passing
- [ ] `just test` passing
- [ ] Manual testing: Full workflow per plugin
- [ ] Line count: ~7,500 lines
- [ ] Gate 3 validation complete
- [ ] Effectiveness validation complete
- [ ] Documentation updated
- [ ] Ready for merge to main

### Post-Completion
- [ ] All phases merged to main
- [ ] CLAUDE.md updated
- [ ] ARCHITECTURE.md updated
- [ ] Create STATUS report documenting completion
- [ ] Tag release: `v0.1.1-optimized`
- [ ] Celebrate 62% reduction achieved! 🎉

---

**END OF PLAN**

**Next Action**: Review this plan, ask questions if needed, then proceed to Phase 1 execution.
