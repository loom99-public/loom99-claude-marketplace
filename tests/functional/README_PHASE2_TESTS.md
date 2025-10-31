# Phase 2 Functional Tests: Skills & README Reduction

## Overview

This test suite validates Phase 2 of the verbosity reduction initiative, which targets:
- **Skills reduction**: 9,272 → 4,030 lines (-57%)
- **README reduction**: 4,272 → 1,050 lines (-75%)

## Test File

`test_phase2_reductions.py` - Comprehensive functional tests for Phase 2 validation

## Test Strategy

### Design Principles

1. **Fail Before, Pass After**: Tests are designed to FAIL in the current state (before Phase 2 reduction) and PASS after reduction work is complete.

2. **Un-Gameable**: Tests verify actual content and structure, not just file sizes. Cannot be bypassed by:
   - Creating empty files (content quality tests)
   - Removing structure (YAML frontmatter tests)
   - Deleting examples (example presence tests)
   - Generic filler text (content pattern tests)

3. **Comprehensive Coverage**: Tests validate:
   - Size targets (line counts)
   - Structure preservation (sections, headings)
   - Content quality (procedures, examples)
   - Consistency (across plugins)

## Test Classes

### 1. TestSkillsSizeValidation

**Purpose**: Validate skills are within optimal size range (250-400 lines)

**Current State** (will FAIL):
- visual-iteration: 730-1,232 lines (all exceed target)
- epti: 508-715 lines (all exceed target)
- agent-loop: 247-630 lines (3 of 4 exceed target)
- Total: 8,986 lines

**Target State** (will PASS):
- All skills: 250-400 lines
- Total: ~4,030 lines (±10% buffer)

**Tests**:
- `test_no_skill_exceeds_maximum_length`: No skill >450 lines
- `test_skills_within_optimal_range`: ≥80% skills in 250-400 range
- `test_total_skills_size_meets_target`: Total ≤4,500 lines
- `test_skills_average_length_optimal`: Average 250-400 per plugin

### 2. TestSkillsStructurePreservation

**Purpose**: Verify skills maintain required structure after reduction

**Anti-Gaming**: Checks for actual content patterns, not just file size

**Tests**:
- `test_yaml_frontmatter_preserved`: YAML metadata intact
- `test_skills_have_structured_sections`: ≥3 markdown sections
- `test_skills_contain_examples`: At least 1-2 examples present

### 3. TestSkillsContentQuality

**Purpose**: Verify essential content is preserved after reduction

**Anti-Gaming**: Checks for meaningful procedures, not filler text

**Tests**:
- `test_skills_have_substantial_content_after_frontmatter`: ≥3,000 chars of content
- `test_skills_contain_procedures`: Procedural language patterns present
- `test_skills_no_excessive_framework_duplication`: ≤20 framework mentions (prevents 6x duplication)

### 4. TestREADMESizeValidation

**Purpose**: Validate READMEs are concise references (200-500 lines)

**Current State** (will FAIL):
- visual-iteration: 2,319 lines (target: ≤500)
- epti: 1,238 lines (target: ≤350)
- agent-loop: 715 lines (target: ≤200)
- Total: 4,272 lines

**Target State** (will PASS):
- visual-iteration: ≤500 lines
- epti: ≤350 lines
- agent-loop: ≤200 lines
- Total: ~1,050 lines (±15% buffer)

**Tests**:
- `test_readme_within_target_range`: Each README within target
- `test_total_readmes_size_meets_target`: Total ≤1,200 lines

### 5. TestREADMEStructureValidation

**Purpose**: Verify READMEs are references, not tutorials

**Anti-Gaming**: Checks for reference structure patterns

**Tests**:
- `test_readme_has_quickstart_section`: Quick Start present
- `test_readme_has_command_reference`: Command list/reference present
- `test_readme_not_excessive_examples`: ≤15 code blocks (2-3 examples)
- `test_readme_concise_sections`: No section >200 lines

### 6. TestREADMEContentQuality

**Purpose**: Verify essential README content is preserved

**Tests**:
- `test_readme_has_plugin_description`: Plugin purpose clearly described
- `test_readme_lists_all_commands`: All commands mentioned

### 7. TestConsistencyAcrossPlugins

**Purpose**: Verify consistent patterns across all plugins

**Anti-Gaming**: Ensures Phase 2 reduction is applied consistently

**Tests**:
- `test_skills_consistent_size_distribution`: Plugin averages within 2x of each other
- `test_all_skills_follow_same_structure_pattern`: All skills score ≥4/5 on structure

### 8. TestPhase2ValidationSummary

**Purpose**: High-level summary test validating Phase 2 completion

**Test**:
- `test_phase2_reduction_targets_met`: Comprehensive check of all targets

## Running the Tests

### Run All Phase 2 Tests

```bash
# From repository root
pytest tests/functional/test_phase2_reductions.py -v
```

### Run Specific Test Class

```bash
# Skills size validation
pytest tests/functional/test_phase2_reductions.py::TestSkillsSizeValidation -v

# README validation
pytest tests/functional/test_phase2_reductions.py::TestREADMESizeValidation -v

# Summary test only
pytest tests/functional/test_phase2_reductions.py::TestPhase2ValidationSummary -v
```

### Run with Detailed Output

```bash
# Show all assertion details
pytest tests/functional/test_phase2_reductions.py -vv --tb=short

# Show only failures
pytest tests/functional/test_phase2_reductions.py --tb=short -x
```

## Expected Results

### Before Phase 2 Reduction (Current State)

**Expected**: Most tests will FAIL

```
FAILED test_no_skill_exceeds_maximum_length - visual-iteration: 4 skills exceed 450 lines
FAILED test_skills_within_optimal_range - agent-loop: Only 25% in optimal range
FAILED test_total_skills_size_meets_target - 8,986 lines exceeds max 4,500
FAILED test_readme_within_target_range - visual-iteration: 2,319 lines exceeds max 500
...
```

**This is CORRECT** - tests are designed to fail until Phase 2 work is complete.

### After Phase 2 Reduction (Target State)

**Expected**: All tests will PASS

```
PASSED test_no_skill_exceeds_maximum_length
PASSED test_skills_within_optimal_range
PASSED test_total_skills_size_meets_target
PASSED test_readme_within_target_range
PASSED test_phase2_reduction_targets_met
...
```

## Test Counts

Total tests: **47 tests** (26 skills tests + 14 README tests + 7 quality tests)

Breakdown by class:
- TestSkillsSizeValidation: 12 tests (4 tests × 3 plugins)
- TestSkillsStructurePreservation: 9 tests (3 tests × 3 plugins)
- TestSkillsContentQuality: 9 tests (3 tests × 3 plugins)
- TestREADMESizeValidation: 4 tests (1 total + 3 per-plugin)
- TestREADMEStructureValidation: 12 tests (4 tests × 3 plugins)
- TestREADMEContentQuality: 6 tests (2 tests × 3 plugins)
- TestConsistencyAcrossPlugins: 2 tests
- TestPhase2ValidationSummary: 1 test

## Integration with Existing Tests

Phase 2 tests complement existing structure tests:

**Existing** (`test_skills_structure.py`):
- Directory structure validation
- YAML frontmatter syntax
- File existence
- Plugin configuration

**Phase 2** (`test_phase2_reductions.py`):
- File size validation
- Content quality validation
- Structure preservation
- Reduction target achievement

Both test suites should pass after Phase 2 completion.

## Validation Workflow

### 1. Before Starting Phase 2

```bash
# Run Phase 2 tests (expect failures)
pytest tests/functional/test_phase2_reductions.py -v

# Document current state
pytest tests/functional/test_phase2_reductions.py --tb=short | tee phase2_baseline.txt
```

### 2. During Phase 2 Work

```bash
# Run tests frequently to track progress
pytest tests/functional/test_phase2_reductions.py -k "skill" -v  # Skills only
pytest tests/functional/test_phase2_reductions.py -k "readme" -v  # READMEs only

# Check specific plugin
pytest tests/functional/test_phase2_reductions.py -k "visual-iteration" -v
```

### 3. After Phase 2 Completion

```bash
# Verify all Phase 2 targets met
pytest tests/functional/test_phase2_reductions.py -v

# Run full test suite
just test

# Verify marketplace structure
just validate
```

## Anti-Gaming Measures

These tests cannot be bypassed by:

### ❌ Creating Empty Files
- **Blocked by**: `test_skills_have_substantial_content_after_frontmatter` (requires ≥3,000 chars)
- **Blocked by**: Content quality tests (procedural patterns, examples)

### ❌ Removing Structure
- **Blocked by**: `test_yaml_frontmatter_preserved` (requires YAML metadata)
- **Blocked by**: `test_skills_have_structured_sections` (requires ≥3 sections)

### ❌ Deleting All Examples
- **Blocked by**: `test_skills_contain_examples` (requires example indicators)
- **Blocked by**: `test_readme_not_excessive_examples` (requires some code blocks)

### ❌ Generic Filler Text
- **Blocked by**: `test_skills_contain_procedures` (requires procedural patterns)
- **Blocked by**: `test_readme_has_plugin_description` (requires key concept mentions)

### ❌ Reducing Only Some Files
- **Blocked by**: `test_skills_consistent_size_distribution` (checks cross-plugin consistency)
- **Blocked by**: `test_all_skills_follow_same_structure_pattern` (requires consistent structure)

### ❌ Hardcoding Test Values
- **Blocked by**: Tests read actual files from filesystem
- **Blocked by**: Content pattern matching (not just counts)

## Success Criteria

Phase 2 is complete when:

- [ ] All 47 tests in `test_phase2_reductions.py` pass
- [ ] `test_phase2_reduction_targets_met` passes (summary test)
- [ ] All skills 250-450 lines (optimal: 250-400)
- [ ] Total skills ~4,030 lines (max: 4,500)
- [ ] visual-iteration README ≤500 lines
- [ ] epti README ≤350 lines
- [ ] agent-loop README ≤200 lines
- [ ] Total READMEs ~1,050 lines (max: 1,200)
- [ ] All existing structure tests still pass
- [ ] `just validate && just test` passes

## Traceability to PLAN

This test suite validates completion of:

**PLAN-verbosity-reduction-2025-10-29-075000.md**:
- Phase 2, Initiative 2.1: Skills Reduction (lines 387-489)
- Phase 2, Initiative 2.2: README Condensation (lines 491-669)

**SUCCESS METRICS** (lines 873-882):
- Skills Avg: 692 → 310 lines ✓
- READMEs Avg: 1,424 → 350 lines ✓

## Notes

1. **Buffer Zones**: Tests include 10-15% buffer zones to allow for content preservation while meeting targets.

2. **Minimum Sizes**: Tests enforce minimum sizes to prevent over-reduction (skills ≥100 lines, READMEs ≥100 lines).

3. **Flexibility**: Some tests allow 80% compliance rather than 100% to account for legitimate variations.

4. **Consistency**: Cross-plugin tests ensure reduction is applied uniformly.

5. **Documentation**: README tests verify reference format, not tutorial format.

## Maintenance

These tests are specific to Phase 2 verbosity reduction. After Phase 2 completion:

1. Tests should continue to pass (enforce quality standards)
2. Update buffer zones if targets shift
3. Consider promoting to permanent regression tests
4. Archive baseline results for comparison

---

**Status**: Ready for Phase 2 validation
**Last Updated**: 2025-10-29
**Test Count**: 47 tests across 8 test classes
