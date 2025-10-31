# Phase 1 Verbosity Reduction TODO

**Target**: -11,500 lines (-47%)
**Timeline**: 3-5 days
**Status**: In Progress

## Progress Tracking

### Initiative 1.1: Command Reduction (-8,893 lines)

#### visual-iteration Commands (HIGHEST PRIORITY) [-7,016 lines]

- [ ] load-mock.md: 1,324 → 250 lines (-1,074, -81%)
- [ ] iterate.md: 1,120 → 280 lines (-840, -75%)
- [ ] visual-commit.md: 996 → 280 lines (-716, -72%)
- [ ] compare.md: 937 → 300 lines (-637, -68%)
- [ ] implement-design.md: 905 → 280 lines (-625, -69%)
- [ ] screenshot.md: 892 → 178 lines (-714, -80%)

#### epti Commands [-1,735 lines]

- [ ] feedback.md: 1,324 → 300 lines (-1,024, -77%)
- [ ] iterate.md: 581 → 180 lines (-401, -69%)
- [ ] commit-code.md: 567 → 180 lines (-387, -68%)
- [ ] implement.md: 498 → 180 lines (-318, -64%)
- [ ] verify-fail.md: 393 → 150 lines (-243, -62%)
- [ ] write-tests.md: 456 → 180 lines (-276, -61%)

#### agent-loop Commands [-68 lines]

- [ ] commit.md: 132 → 105 lines (-27, -20%)
- [ ] code.md: 93 → 74 lines (-19, -20%)
- [ ] plan.md: 77 → 62 lines (-15, -20%)
- [ ] explore.md: 60 → 48 lines (-12, -20%)

### Initiative 1.2: Framework Consolidation (-2,000 lines)

- [ ] Consolidate 6 framework examples → 1-2 per file
- [ ] Remove React+Tailwind AND plain CSS duplication
- [ ] Convert to generic patterns

### Initiative 1.3: Layer Redundancy Elimination (-2,500 lines)

- [ ] Remove agent/command overlap (commands reference agent)
- [ ] Remove command/skill overlap (commands reference skills)
- [ ] Establish clear layer separation

## Validation Checklist (after each batch)

- [ ] `just validate` passes
- [ ] `just test` passes (50 tests)
- [ ] Manual review: Core guidance preserved
- [ ] Manual review: Guardrails intact
- [ ] Manual review: Transitions functional

## Final Phase 1 Gate

- [ ] All commands 75-200 lines
- [ ] Framework examples: 1-2 per file (not 6)
- [ ] Layer overlap <20%
- [ ] `just validate && just test` passes
- [ ] Line count: ~13,000 lines (currently 24,459)
- [ ] Manual test: 1 command per plugin

## Notes

**Working Directory**: /Users/bmf/icode/loom99-claude-marketplace

**Reduction Strategy**: Be ruthless. If content appears in agent or skill, cut from command. If 6 framework examples exist, keep only 1-2. Convert detailed procedures to checklists.

**Pattern to Follow**:
```markdown
# /command - Stage Name

## Purpose (2-3 lines)

## When to Use (2-3 lines)

## Workflow (5-10 lines checklist)

## Key Principles (5-10 lines)

## Anti-Patterns (5-10 lines)

## Transition (2-3 lines)

## Example (20-50 lines, ONE framework)
```
