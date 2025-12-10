# Progressive Disclosure Implementation Plan

**Date**: 2025-12-10 02:26:05
**Project**: do-more-now plugin
**Source STATUS**: STATUS-gating-impl-20251210-013219.md
**Context**: Refactor 3 verbose skills + fix 3 broken references + integrate 3 orphaned skills

## Executive Summary

**Total Work Items**: 9 items across 3 priorities
**Estimated Effort**: Medium (11 complexity points)
**Dependencies**: None - all items can proceed independently
**Recommended Approach**: Work by priority (P0 → P1 → P2) to maximize immediate impact

**Target Outcomes**:
1. Three verbose skills refactored using progressive disclosure pattern (214 → 80, 162 → 60, 146 → 50 lines)
2. Three broken command references fixed in researcher agent
3. Three orphaned skills properly integrated into command workflows

## Backlog

---

## P0 - Critical: Progressive Disclosure Refactoring

### P0-1: Refactor gating-controller Skill

**Status**: Not Started
**Effort**: Medium (4-5 complexity points)
**Dependencies**: None
**Spec Reference**: evaluation-profiles/SKILL.md (model pattern) • **Status Reference**: Implied by line counts

#### Description

The gating-controller skill is 214 lines and contains extensive examples, templates, and workflow documentation that obscure its core logic. Following the evaluation-profiles pattern, split detailed content into reference files while keeping the essential decision-making process in SKILL.md.

**Current Structure** (214 lines):
- Core process (Steps 1-5): ~50 lines
- Decision templates: ~40 lines
- AskUserQuestion format: ~25 lines
- Example flows (3 scenarios): ~60 lines
- File format reference: ~40 lines

**Target Structure** (80 lines):
- SKILL.md: Core process + brief examples
- references/decision-templates.md: All decision format templates
- references/gate-modes.md: Detailed mode explanations with examples
- references/file-formats.md: GATE_CONFIG and DECISION file specs

#### Acceptance Criteria

- [ ] SKILL.md reduced to ~80 lines focusing on core process (Steps 1-5)
- [ ] references/decision-templates.md created with decision format examples
- [ ] references/gate-modes.md created with BLOCKING/HYBRID/NONBLOCKING examples
- [ ] references/file-formats.md created with GATE_CONFIG and DECISION specs
- [ ] SKILL.md includes "Read references/X.md for details" pointers
- [ ] No loss of information - all original content preserved in references/
- [ ] Grep verification: no broken internal references

#### Technical Notes

**Content to Move**:

1. **To references/decision-templates.md** (~40 lines):
   - AskUserQuestion format template (lines ~88-114)
   - Example decision presentations
   - Approval status formatting

2. **To references/gate-modes.md** (~60 lines):
   - Example flows section (lines ~132-167)
   - BLOCKING mode example
   - HYBRID mode example
   - NONBLOCKING mode example
   - Mode-specific processing logic details

3. **To references/file-formats.md** (~40 lines):
   - GATE_CONFIG.txt format (lines ~171-178)
   - DECISION file format - before approval (lines ~180-205)
   - DECISION file format - after approval (lines ~207-214)

**Keep in SKILL.md** (~80 lines):
- Front matter (name, description)
- Critical context note
- Step 1-5 process (with brief inline examples)
- Error handling summary
- One-sentence reference to each reference/ file

**Pattern** (follow evaluation-profiles):
```markdown
## Step X: [Name]

[Brief explanation]

For detailed templates and examples, read `references/decision-templates.md`.

[Minimal inline example if needed]
```

---

### P0-2: Refactor route-subcommands Skill

**Status**: Not Started
**Effort**: Medium (3-4 complexity points)
**Dependencies**: None
**Spec Reference**: evaluation-profiles/SKILL.md (model pattern) • **Status Reference**: Implied by line counts

#### Description

The route-subcommands skill is 162 lines with extensive examples that make the parsing logic hard to find. The core algorithm is ~40 lines; examples and edge cases consume 120+ lines.

**Current Structure** (162 lines):
- Core process (Steps 1-5): ~40 lines
- Examples section: ~80 lines (4 detailed examples)
- Edge cases: ~20 lines
- Output format: ~20 lines

**Target Structure** (60 lines):
- SKILL.md: Core process with minimal examples
- references/examples.md: All detailed routing examples
- references/edge-cases.md: Self-reference, ambiguous ordering, no main instructions

#### Acceptance Criteria

- [ ] SKILL.md reduced to ~60 lines focusing on parsing logic
- [ ] references/examples.md created with all 4+ detailed examples
- [ ] references/edge-cases.md created with edge case handling
- [ ] Each step in SKILL.md has ONE minimal inline example
- [ ] References/ files include comprehensive examples with input/output pairs
- [ ] No loss of information
- [ ] Grep verification: no broken internal references

#### Technical Notes

**Content to Move**:

1. **To references/examples.md** (~80 lines):
   - Example 1: Pre and post commands (lines ~80-94)
   - Example 2: Only pre-commands (lines ~96-102)
   - Example 3: Only post-commands (lines ~104-111)
   - Example 4: No subcommands (lines ~113-122)
   - Add more edge case examples

2. **To references/edge-cases.md** (~20 lines):
   - Self-reference (lines ~125-127)
   - Ambiguous ordering (lines ~129-136)
   - No clear main instructions (lines ~138-143)

**Keep in SKILL.md** (~60 lines):
- Front matter
- When to use
- Input context
- Steps 1-5 with ONE minimal example per step
- Output format (brief)
- References to examples.md and edge-cases.md

**Pattern**:
```markdown
## Step X: [Name]

[Process description]

**Example**:
```
Input: "/do:it /do:plan. Fix bug"
→ Pre: [/do:plan], Main: "Fix bug", Post: []
```

For more examples, read `references/examples.md`.
```

---

### P0-3: Refactor setup-testing Skill

**Status**: Not Started
**Effort**: Small (2-3 complexity points)
**Dependencies**: None
**Spec Reference**: evaluation-profiles/SKILL.md (model pattern) • **Status Reference**: Implied by line counts

#### Description

The setup-testing skill is 146 lines with framework-specific configuration details embedded throughout. The detection and setup process is ~30 lines; framework configs consume 116 lines.

**Current Structure** (146 lines):
- Core process (Steps 1-5): ~30 lines
- Framework recommendation table: ~10 lines
- Framework-specific configs: ~90 lines (Vitest, pytest, Go, Rust)
- Output format: ~15 lines

**Target Structure** (50 lines):
- SKILL.md: Detection, recommendation, setup process
- references/vitest.md: Full Vitest setup with examples
- references/pytest.md: Full pytest setup with examples
- references/jest.md: Jest setup
- references/go-test.md: Go setup
- references/mocha.md: Mocha setup

#### Acceptance Criteria

- [ ] SKILL.md reduced to ~50 lines focusing on detection and process
- [ ] references/vitest.md created with complete Vitest config
- [ ] references/pytest.md created with complete pytest config
- [ ] references/jest.md, go-test.md, mocha.md created for other frameworks
- [ ] SKILL.md framework table references appropriate reference files
- [ ] AskUserQuestion example uses reference pointers
- [ ] No loss of information
- [ ] Grep verification: no broken internal references

#### Technical Notes

**Content to Move**:

1. **To references/vitest.md** (~25 lines):
   - Lines 95-111: Full Vitest setup
   - Installation commands
   - package.json config
   - vitest.config.ts

2. **To references/pytest.md** (~20 lines):
   - Lines 113-124: Full pytest setup
   - uv add commands
   - pyproject.toml config

3. **To references/go-test.md** (~10 lines):
   - Lines 126-128: Go setup notes

4. **To references/jest.md** (~25 lines):
   - Create comprehensive Jest setup (currently missing)

5. **To references/mocha.md** (~20 lines):
   - Create Mocha + Chai setup (currently missing)

**Keep in SKILL.md** (~50 lines):
- Front matter
- When to use
- Steps 1-5 (detection, recommend, ask, install, verify)
- Framework recommendation table with "See references/X.md" links
- Brief AskUserQuestion template referencing framework details
- Output format

**Pattern** for framework table:
```markdown
| Language | Framework | Details |
|----------|-----------|---------|
| JavaScript | Vitest | See `references/vitest.md` |
| Python | pytest | See `references/pytest.md` |
```

---

## P1 - High: Fix Broken References

### P1-1: Fix Broken Command References in researcher.md

**Status**: Not Started
**Effort**: Small (1 complexity point)
**Dependencies**: None
**Spec Reference**: agents/researcher.md lines 185, 206, 207 • **Status Reference**: Implied by evaluation notes

#### Description

The researcher agent references three commands that don't exist or have been renamed:
1. Line 185: `/do:peek` - command doesn't exist
2. Line 206: `/do:learn` - should be `/do:research`
3. Line 207: `/do:status` - should be `/do:plan status`

#### Acceptance Criteria

- [ ] Line 185: Remove `/do:peek` reference entirely or document as future work
- [ ] Line 206: Change `/do:learn` to `/do:research`
- [ ] Line 207: Change `/do:status` to `/do:plan status`
- [ ] No other broken command references in researcher.md
- [ ] Researcher agent tested with corrected references

#### Technical Notes

**File**: `plugins/do-more-now/agents/researcher.md`

**Changes**:

1. **Line 185** - "Peek Mode" section header:
   - **Option A**: Remove entire "Peek Mode" section (lines 183-209) if `/do:peek` is not planned
   - **Option B**: Keep section but change reference to "When invoked by `/do:explore` in quick mode"
   - **Recommendation**: Option B - reframe as an optimization hint for explore command

2. **Line 206**: Redirect to correct command:
   ```markdown
   - Question needs external research (redirect to `/do:research`)
   ```

3. **Line 207**: Redirect to correct command:
   ```markdown
   - Question is about correctness (redirect to `/do:plan status`)
   ```

**Verification**:
```bash
grep -n "do:peek\|do:learn\|do:status" plugins/do-more-now/agents/researcher.md
# Should return ZERO matches after fix
```

---

## P2 - Medium: Integrate Orphaned Skills

### P2-1: Integrate market-research Skill into research Command

**Status**: Not Started
**Effort**: Small (1 complexity point)
**Dependencies**: None
**Spec Reference**: commands/research.md, skills/market-research/SKILL.md • **Status Reference**: Noted as orphaned skill

#### Description

The `market-research` skill exists but is not referenced by any command. It should be integrated into the `/do:research` command workflow for competitive analysis scenarios.

**Current State**:
- `skills/market-research/SKILL.md` exists (41 lines)
- `commands/research.md` invokes `do:researcher` directly
- No pathway to invoke `market-research` skill

**Target State**:
- `/do:research` command detects "market" intent
- Routes to `do:market-research` skill
- `do:researcher` continues to handle other research types

#### Acceptance Criteria

- [ ] commands/research.md references market-research skill
- [ ] Intent detection table includes market research routing
- [ ] When user input contains "market", "competitors", "alternatives", "demand" → invoke market-research
- [ ] Other research intents continue using do:researcher
- [ ] Plugin manifest includes market-research in skills list
- [ ] Integration tested with sample inputs

#### Technical Notes

**File**: `plugins/do-more-now/commands/research.md`

**Add to Intent Detection table** (around line 36):

```markdown
| Intent signals | Workflow |
|----------------|----------|
| "market", "competitors", "alternatives", "demand", "landscape" | Invoke `do:market-research` skill |
| "docs", "documentation", "how to use X" | Use `do:researcher` for external docs |
| "best practices", "patterns", "how others do" | Use `do:researcher` for industry research |
| *(default)* | Use `do:researcher` for general external research |
```

**Update Step 2 Process** (around line 44):

```markdown
### Process

**If market/competitive research detected**:
Invoke `do:market-research` skill - handles competitive landscape, demand signals, alternatives

**Otherwise, use do:researcher in external mode**:
1. **Search**: Web search for relevant sources
2. **Gather**: Collect information from multiple sources
...
```

**Verification**:
Test commands:
- `/do:research competitors for auth tools` → should invoke market-research
- `/do:research jwt best practices` → should use researcher
- `/do:research react hooks documentation` → should use researcher

---

### P2-2: Document gating-controller Integration Points

**Status**: Not Started
**Effort**: Small (1 complexity point)
**Dependencies**: P0-1 (gating-controller refactor should complete first)
**Spec Reference**: skills/gating-controller/SKILL.md • **Status Reference**: STATUS notes gating-controller exists but is unintegrated

#### Description

The `gating-controller` skill exists and is well-defined, but it's not yet integrated into any workflow skills or commands. This item creates a documentation artifact that maps WHERE gating-controller should be invoked once the gating system is implemented (per the existing gating implementation plan).

**Note**: This is NOT implementing the gating system (that's a separate effort tracked in STATUS-gating-impl). This is simply documenting the integration points so they're discoverable.

#### Acceptance Criteria

- [ ] Create `.agent_planning/INTEGRATION-gating-controller.md`
- [ ] Document which commands should initialize gate mode (7 commands)
- [ ] Document which workflow skills should call gating checkpoints (tdd-workflow, iterative-workflow, etc.)
- [ ] Document which agents should log decisions (9 agents)
- [ ] Reference the gating design document for full implementation details
- [ ] Add "See INTEGRATION-gating-controller.md" note to gating-controller/SKILL.md

#### Technical Notes

**Create**: `.agent_planning/INTEGRATION-gating-controller.md`

**Content outline**:

```markdown
# Gating Controller Integration Points

**Status**: Not yet implemented
**Design**: EXPLORE-gating-system-design-20251210.md
**Implementation Plan**: STATUS-gating-impl-20251210-013219.md

This document maps WHERE gating-controller should be invoked once the gating system is implemented.

## Commands That Initialize Gate Mode (7)

- it.md
- plan.md
- explore.md
- research.md
- chores.md
- docs.md
- release.md

Each needs gate detection logic at Step 0.

## Workflow Skills That Need Checkpoints (5)

- tdd-workflow.md
- iterative-workflow.md
- refactor.md
- debug.md
- fix.md

Each needs checkpoint after agent invocations.

## Agents That Should Log Decisions (9)

- test-driven-implementer
- iterative-implementer
- functional-tester
- project-architect
- researcher
- project-evaluator
- work-evaluator
- status-planner
- product-visionary

Each needs decision logging section.

## Next Steps

See STATUS-gating-impl-20251210-013219.md for implementation phases.
```

**Update gating-controller/SKILL.md**:
Add after front matter:
```markdown
**Integration Status**: Not yet integrated. See `.agent_planning/INTEGRATION-gating-controller.md` for planned integration points.
```

---

### P2-3: Verify evaluation-profiles Integration

**Status**: Not Started
**Effort**: Small (0.5 complexity points)
**Dependencies**: None
**Spec Reference**: skills/evaluation-profiles/SKILL.md • **Status Reference**: Noted as internal skill (OK as-is)

#### Description

The `evaluation-profiles` skill is noted as "internal (OK as-is)" but we should verify it's properly integrated into the evaluator agents that should use it (project-evaluator, work-evaluator).

This is a verification-only task - if integration is confirmed, no changes needed. If gaps found, document them.

#### Acceptance Criteria

- [ ] Grep for "evaluation-profiles" in project-evaluator.md
- [ ] Grep for "evaluation-profiles" in work-evaluator.md
- [ ] If found: Verify usage is correct (profile selection happens before validation)
- [ ] If not found: Document in `.agent_planning/FINDINGS-evaluation-profiles.md` that integration is missing
- [ ] If integration is correct: Document "✓ Verified" in final summary

#### Technical Notes

**Commands**:
```bash
grep -n "evaluation-profiles" plugins/do-more-now/agents/project-evaluator.md
grep -n "evaluation-profiles" plugins/do-more-now/agents/work-evaluator.md
```

**Expected**: Both agents should reference the skill in their validation sections.

**If missing**: Create `.agent_planning/FINDINGS-evaluation-profiles.md`:
```markdown
# Evaluation Profiles Integration Findings

**Status**: evaluation-profiles skill exists but is not referenced by evaluator agents

## Agents That Should Use It
- project-evaluator.md - should select profile before validation
- work-evaluator.md - should select profile before validation

## Recommendation
Add profile selection step to both agents:

1. Determine project type
2. Invoke `do:evaluation-profiles` skill
3. Read appropriate references/X.md
4. Apply profile-specific validation criteria
```

**If present**: No action needed, note in summary.

---

## Dependency Graph

```
P0-1: gating-controller refactor
  ↓ (soft dependency)
P2-2: Document gating-controller integration

P0-2: route-subcommands refactor (independent)

P0-3: setup-testing refactor (independent)

P1-1: Fix researcher.md references (independent)

P2-1: Integrate market-research (independent)

P2-3: Verify evaluation-profiles (independent)
```

**No hard blockers** - all items can proceed in parallel except P2-2 should wait for P0-1.

---

## Recommended Sprint Planning

### Sprint 1: Progressive Disclosure Core (P0)

**Goal**: Refactor verbose skills to match evaluation-profiles pattern

**Items**:
1. P0-1: gating-controller (4-5 effort)
2. P0-2: route-subcommands (3-4 effort)
3. P0-3: setup-testing (2-3 effort)

**Total Effort**: 9-12 complexity points
**Estimated Duration**: Medium complexity work session

**Success Criteria**:
- All three skills reduced to target line counts
- All reference files created with full content
- No information loss
- No broken internal references

### Sprint 2: References and Integration (P1-P2)

**Goal**: Fix broken links and integrate orphaned skills

**Items**:
1. P1-1: Fix researcher.md references (1 effort)
2. P2-1: Integrate market-research (1 effort)
3. P2-2: Document gating-controller integration (1 effort)
4. P2-3: Verify evaluation-profiles (0.5 effort)

**Total Effort**: 3.5 complexity points
**Estimated Duration**: Short work session

**Success Criteria**:
- All broken references fixed
- market-research reachable via /do:research
- gating-controller integration documented
- evaluation-profiles integration verified or findings documented

---

## Risk Assessment

### Low Risk
- **P0-2 (route-subcommands)**: Pure refactoring, well-understood pattern
- **P0-3 (setup-testing)**: Framework configs are isolated, easy to extract
- **P1-1 (researcher references)**: Simple find-replace operations
- **P2-3 (evaluation-profiles)**: Verification only, no changes expected

### Medium Risk
- **P0-1 (gating-controller)**: Largest refactor (214 → 80 lines), most complex content
  - **Mitigation**: Follow evaluation-profiles pattern exactly, verify no content loss
- **P2-1 (market-research)**: Changing command routing logic
  - **Mitigation**: Test with multiple input patterns to ensure correct routing
- **P2-2 (gating-controller docs)**: Documenting unimplemented system
  - **Mitigation**: Link to existing design/status docs, mark as "planned not implemented"

### High Risk
- **None identified**

---

## Validation Strategy

### Per-Item Validation

**After P0 refactors**:
```bash
# Verify line counts
wc -l plugins/do-more-now/skills/*/SKILL.md

# Verify no broken references
grep -r "references/" plugins/do-more-now/skills/gating-controller/
grep -r "references/" plugins/do-more-now/skills/route-subcommands/
grep -r "references/" plugins/do-more-now/skills/setup-testing/

# Verify reference files exist
ls plugins/do-more-now/skills/*/references/*.md
```

**After P1-1 (researcher fix)**:
```bash
# Should return ZERO matches
grep "do:peek\|do:learn" plugins/do-more-now/agents/researcher.md

# Should return corrected references
grep "do:research\|do:plan status" plugins/do-more-now/agents/researcher.md
```

**After P2-1 (market-research)**:
```bash
# Should find reference
grep "market-research" plugins/do-more-now/commands/research.md
```

### End-to-End Validation

**Test Cases**:
1. Load plugin in Claude Code
2. Invoke `/do:research competitors for X` → should hit market-research skill
3. Invoke `/do:research best practices for X` → should hit researcher agent
4. Check researcher agent documentation reads correctly
5. Verify all skill SKILL.md files are under target line counts
6. Verify all references/ directories contain expected files

---

## Open Questions

### Low Priority (Can Answer During Implementation)

1. **P0-1 (gating-controller)**: Should gate-modes.md include decision approval workflow diagram?
   - **Recommendation**: Yes if easily created; otherwise skip for now

2. **P0-3 (setup-testing)**: Should we create reference files for ALL supported frameworks or just top 3?
   - **Recommendation**: Create vitest, pytest, jest first; add others if time allows

3. **P1-1 (researcher)**: Should we preserve "Peek Mode" concept even though /do:peek doesn't exist?
   - **Recommendation**: Yes, reframe as "quick mode" for /do:explore

### None (Critical)

---

## File Creation Checklist

### New Files to Create (13 files)

**gating-controller** (3 reference files):
- [ ] `plugins/do-more-now/skills/gating-controller/references/decision-templates.md`
- [ ] `plugins/do-more-now/skills/gating-controller/references/gate-modes.md`
- [ ] `plugins/do-more-now/skills/gating-controller/references/file-formats.md`

**route-subcommands** (2 reference files):
- [ ] `plugins/do-more-now/skills/route-subcommands/references/examples.md`
- [ ] `plugins/do-more-now/skills/route-subcommands/references/edge-cases.md`

**setup-testing** (5+ reference files):
- [ ] `plugins/do-more-now/skills/setup-testing/references/vitest.md`
- [ ] `plugins/do-more-now/skills/setup-testing/references/pytest.md`
- [ ] `plugins/do-more-now/skills/setup-testing/references/jest.md`
- [ ] `plugins/do-more-now/skills/setup-testing/references/go-test.md`
- [ ] `plugins/do-more-now/skills/setup-testing/references/mocha.md`

**Integration docs** (1 file):
- [ ] `.agent_planning/INTEGRATION-gating-controller.md`

**Optional findings** (0-1 file):
- [ ] `.agent_planning/FINDINGS-evaluation-profiles.md` (only if gaps found)

### Files to Modify (4 files)

- [ ] `plugins/do-more-now/skills/gating-controller/SKILL.md`
- [ ] `plugins/do-more-now/skills/route-subcommands/SKILL.md`
- [ ] `plugins/do-more-now/skills/setup-testing/SKILL.md`
- [ ] `plugins/do-more-now/agents/researcher.md`
- [ ] `plugins/do-more-now/commands/research.md`

---

## Success Metrics

**Quantitative**:
- gating-controller: 214 → 80 lines (62% reduction)
- route-subcommands: 162 → 60 lines (63% reduction)
- setup-testing: 146 → 50 lines (66% reduction)
- **Total reduction**: 522 → 190 lines in SKILL.md (63% less cognitive load)
- **Total references**: 13 new reference files created
- **Broken references fixed**: 3 fixes in researcher.md
- **Orphaned skills integrated**: 1 (market-research)
- **Orphaned skills documented**: 1 (gating-controller)
- **Integrations verified**: 1 (evaluation-profiles)

**Qualitative**:
- SKILL.md files are scannable and show core logic immediately
- Detailed examples are discoverable but non-intrusive
- Pattern consistency across all skills matches evaluation-profiles
- No information loss - all original content preserved
- Commands properly route to all available skills

---

## Implementation Order

**Recommended sequence** (maximize early wins):

1. **P0-3** (setup-testing) - Smallest refactor, build confidence
2. **P0-2** (route-subcommands) - Medium refactor, establish rhythm
3. **P0-1** (gating-controller) - Largest refactor, apply learned patterns
4. **P1-1** (researcher references) - Quick win, fix broken links
5. **P2-1** (market-research integration) - Enable hidden functionality
6. **P2-2** (gating-controller docs) - Document future work
7. **P2-3** (evaluation-profiles verify) - Confirm final integration

**Rationale**: Start small (P0-3), build momentum, tackle hardest refactor (P0-1) when pattern is clear, then quickly finish integration items.

---

## What Could Not Be Determined

| Question | Why Unknown | How to Resolve |
|----------|-------------|----------------|
| Is /do:peek command planned? | Not in command list, but referenced | Ask user: implement or remove reference? |
| Should gating-controller integration happen now? | Separate implementation effort tracked in STATUS-gating-impl | Proceed with documentation only for now |
| Are all framework configs needed for setup-testing? | User preference dependent | Start with top 3 (vitest, pytest, jest), add others if time |

---

## Next Steps

After plan approval, begin with:

```bash
/do:it refactor setup-testing skill per P0-3
```

Or for full sprint:

```bash
/do:it tdd progressive disclosure sprint 1
```

This will execute all P0 items using test-driven approach (if applicable) or iterative validation.
