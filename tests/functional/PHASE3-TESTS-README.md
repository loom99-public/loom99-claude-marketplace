# Phase 3 Agent Optimization Tests

Comprehensive functional tests for Phase 3 of the verbosity reduction project, focusing on agent file optimization.

## Overview

Phase 3 targets the 3 agent files across all plugins:
- **workflow-agent.md** (agent-loop): 206 lines → 206 lines (already optimal, no change needed)
- **tdd-agent.md** (epti): 636 lines → 400 lines (-37%, -236 lines)
- **visual-iteration-agent.md** (visual-iteration): 946 lines → 600 lines (-37%, -346 lines)
- **Total**: 1,787 lines → 1,206 lines (-33%, -582 lines)

## Test Structure

### Test File
- **Location**: `tests/functional/test_phase3_agents.py`
- **Total Tests**: 50 tests across 6 test classes
- **Current Status**: 7 failing (expected), 43 passing

### Test Classes

#### 1. TestAgentSizeValidation (8 tests)
Validates agents are within optimal size ranges.

**Tests**:
- `test_agent_file_exists`: Agents exist for all plugins
- `test_agent_within_target_range`: Agent sizes within min/max bounds
- `test_agent_has_substantial_content`: At least 70% non-empty lines (not padding)
- `test_total_agents_size_meets_target`: Total ≤1,300 lines
- `test_agent_reduction_percentage_correct`: Reductions match plan targets

**Anti-Gaming**: Cannot pass by deleting files, adding empty lines, or ignoring targets.

#### 2. TestAgentStructurePreservation (15 tests)
Verifies agents maintain required structure after optimization.

**Tests**:
- `test_agent_has_primary_heading`: H1 title present
- `test_agent_has_hierarchical_structure`: Multiple heading levels (H1, H2, H3)
- `test_agent_contains_required_section_keywords`: Core concepts present
- `test_agent_documents_workflow_stages`: All workflow stages documented
- `test_agent_has_stage_sections`: Stages clearly separated

**Anti-Gaming**: Cannot flatten structure, remove sections, or merge stages.

#### 3. TestAgentContentQuality (18 tests)
Validates essential content quality preserved.

**Tests**:
- `test_agent_has_examples_or_code_blocks`: At least 1 example or code block
- `test_agent_contains_anti_patterns`: Anti-patterns documented
- `test_agent_has_guardrails_or_rules`: Guardrails/rules defined
- `test_agent_has_transition_guidance`: Stage transitions explained
- `test_agent_has_actionable_lists`: At least 5 list items for activities

**Anti-Gaming**: Cannot remove examples, anti-patterns, or guardrails to reduce size.

#### 4. TestAgentConsistency (3 tests)
Ensures consistency across all agents.

**Tests**:
- `test_agents_use_consistent_stage_format`: Similar stage formatting
- `test_agents_balance_is_reasonable`: No agent >3.5x another
- `test_all_agents_have_similar_density`: Content density within 10%

**Anti-Gaming**: Cannot over-optimize one agent while neglecting others.

#### 5. TestPhase3Summary (1 test)
Master validation of Phase 3 completion.

**Tests**:
- `test_phase3_optimization_complete`: All agents on target

**Output Format**:
```
Phase 3 Agent Optimization Status
==================================================

Total agents size: 1790 lines
Target size: 1206 lines
Maximum allowed: 1300 lines
Reduction needed: +584 lines

Per-Agent Status:
  ✅ agent-loop: 206 lines (target: 206, delta: +0)
  ❌ epti: 637 lines (target: 400, delta: +237)
  ❌ visual-iteration: 947 lines (target: 600, delta: +347)

On Target: 1/3
Needs Reduction: 2/3

❌ Phase 3 IN PROGRESS
```

#### 6. TestPhase3Traceability (3 tests)
Validates tests align with planning documents.

**Tests**:
- `test_phase3_targets_match_plan`: Test targets match PLAN document
- `test_phase3_total_reduction_matches_plan`: Total reduction calculation correct
- `test_phase3_scope_documented`: Phase 3 scope clearly documented

**Anti-Gaming**: Tests must be traceable to planning artifacts.

## Running Tests

### Run All Phase 3 Tests
```bash
just test-phase3
```

### Run Quick Phase 3 Check
```bash
just test-phase3-quick
```

### Run Phase 3 for Specific Plugin
```bash
just test-phase3-plugin epti
just test-phase3-plugin visual-iteration
```

### Show Current Metrics
```bash
just phase3-metrics
```

Output:
```
📊 Phase 3 Current Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agents:
  Total: 1787 lines (target: 1,206)
  agent-loop/workflow-agent:      205 lines (target: 206)
  epti/tdd-agent:      636 lines (target: 400)
  visual-iteration/visual-iteration-agent:      946 lines (target: 600)
```

## Expected Test Results

### Current State (Before Optimization)
- **Passing**: 43 tests
- **Failing**: 7 tests (all expected failures)

**Expected Failures**:
1. `test_agent_within_target_range[epti]` - epti agent too large
2. `test_agent_within_target_range[visual-iteration]` - visual-iteration agent too large
3. `test_total_agents_size_meets_target` - total size exceeds maximum
4. `test_agent_reduction_percentage_correct[epti]` - epti needs reduction
5. `test_agent_reduction_percentage_correct[visual-iteration]` - visual-iteration needs reduction
6. `test_agents_balance_is_reasonable` - size ratio too high
7. `test_phase3_optimization_complete` - optimization incomplete

### After Phase 3 Optimization
- **Passing**: 50 tests (100%)
- **Failing**: 0 tests

All tests should pass once agents are optimized to targets.

## Optimization Targets

### workflow-agent.md (agent-loop)
- **Current**: 206 lines
- **Target**: 206 lines (no change)
- **Status**: ✅ Already optimal

This agent is already at the optimal size and should not be modified significantly.

### tdd-agent.md (epti)
- **Current**: 636 lines
- **Target**: 400 lines
- **Reduction**: -236 lines (-37%)
- **Status**: ❌ Needs optimization

**Focus areas for reduction**:
- Consolidate redundant framework examples (Python, JS, Go, etc.)
- Streamline git command examples
- Reduce verbose failure message examples
- Keep core TDD principles and workflow intact

**Must preserve**:
- 6-stage TDD workflow
- Test-first discipline guidance
- Anti-patterns section
- Hook integration points
- Core principles

### visual-iteration-agent.md (visual-iteration)
- **Current**: 946 lines
- **Target**: 600 lines
- **Reduction**: -346 lines (-37%)
- **Status**: ❌ Needs optimization

**Focus areas for reduction**:
- Consolidate MCP integration examples
- Streamline subagent prompt examples
- Reduce verbose example output
- Simplify error handling sections

**Must preserve**:
- 6-stage visual iteration workflow
- Screenshot capture guidance (automated + manual)
- Visual comparison specificity requirements
- MCP integration patterns
- Core principles

## Anti-Gaming Measures

These tests are designed to be **un-gameable** - they validate real functionality and content:

### 1. Size Validation
- Verifies actual file line counts
- Checks non-empty line ratio (prevents padding)
- Validates total across all agents

### 2. Structure Verification
- Counts actual markdown headings
- Verifies hierarchical organization
- Checks for required section keywords

### 3. Content Quality
- Looks for specific content patterns (examples, code blocks)
- Verifies anti-patterns present
- Checks for actionable lists
- Validates transition guidance

### 4. Consistency Checks
- Compares agent sizes (balance)
- Validates content density
- Ensures similar formatting

### 5. Traceability
- Tests match planning document targets
- Scope clearly documented
- Reduction calculations verified

## Integration with Planning

These tests integrate with the planning workflow:

1. **Consume Planning Artifacts**:
   - Read PLAN-verbosity-reduction document for targets
   - Extract Phase 3 requirements
   - Map targets to test assertions

2. **Validate Against Plan**:
   - Test targets match plan targets
   - Reduction percentages match plan
   - Scope documented in tests

3. **Report Progress**:
   - Summary test shows current status
   - Per-agent breakdown with deltas
   - Clear pass/fail criteria

## Success Criteria

Phase 3 is complete when:

1. ✅ Total agents size ≤1,300 lines (target: 1,206)
2. ✅ workflow-agent: 180-220 lines (already at 206 ✓)
3. ✅ tdd-agent: 350-450 lines (currently 637, needs -237)
4. ✅ visual-iteration-agent: 550-650 lines (currently 947, needs -347)
5. ✅ All structure tests passing
6. ✅ All content quality tests passing
7. ✅ All consistency tests passing
8. ✅ Phase 3 summary test passing

## Files

### Test Implementation
- `/tests/functional/test_phase3_agents.py` (947 lines)

### Documentation
- `/tests/functional/PHASE3-TESTS-README.md` (this file)

### Justfile Commands
```
test-phase3         # Run all Phase 3 tests
test-phase3-quick   # Quick test run (quiet mode)
test-phase3-plugin  # Test specific plugin
phase3-metrics      # Show current metrics
```

## Next Steps

After Phase 3 tests are implemented:

1. **Run Baseline Tests**: Verify current state shows expected failures
2. **Begin Optimization**: Start with tdd-agent (epti)
3. **Iterative Testing**: Run tests after each optimization pass
4. **Verify Quality**: Ensure structure and content preserved
5. **Optimize visual-iteration-agent**: Apply similar techniques
6. **Final Validation**: Run full test suite, verify all 50 tests pass

## Notes

- Tests use absolute file paths (via REPO_ROOT)
- Tests are independent (no execution order dependency)
- Tests verify real file content (not mocks or stubs)
- Thresholds calibrated to current content patterns
- Tests resist gaming through multi-dimensional validation

---

**Last Updated**: 2025-10-29
**Phase**: Phase 3 (Agent Optimization)
**Test Count**: 50 tests (7 failing, 43 passing)
**Target Reduction**: -582 lines (-33%)
