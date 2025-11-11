# Functional Tests for Testing Framework

This directory contains functional tests that validate the testing framework components described in `PLAN-testing-framework-2025-11-06-021441.md`.

## Overview

These tests validate the **testing framework itself** - the tools, documentation, and infrastructure needed to test Claude Code plugins. They are organized by the 3-phase approach from the plan:

- **Phase 1**: Manual Testing Framework (P0-1 to P0-5)
- **Phase 2**: Enhanced Structural Validation (P1-1 to P1-7)
- **Phase 3**: E2E Test Harness Design (P2-1 to P2-4)

## Test Files

### test_manual_testing_framework.py

**Validates Phase 1 (P0-1 to P0-5)**: Manual testing documentation and framework

**What it tests:**
- P0-1: Manual testing documentation framework (README, templates, checklists)
- P0-2: Plugin installation test scenarios for all plugins
- P0-3: Command execution test scenarios (all 16 commands)
- P0-4: Complete workflow test scenarios (3-5 per plugin)
- P0-5: Agent behavior observation checklists

**Why this matters:**
Manual testing is the ONLY way to validate plugins actually work. These tests ensure manual testers have comprehensive guidance.

**Key test classes:**
- `TestManualTestingDocumentationFramework` - Core documentation (README, templates)
- `TestPluginInstallationTestScenarios` - Installation checklists
- `TestCommandExecutionTestScenarios` - Command test scenarios
- `TestCompleteWorkflowTestScenarios` - End-to-end workflow scenarios
- `TestAgentBehaviorObservationChecklists` - Agent observation guides
- `TestManualTestingFrameworkCompleteness` - Phase 1 completion summary

**Expected initial state:** ALL TESTS FAIL (manual testing docs don't exist yet)

**Expected after P0-1 to P0-5:** ALL TESTS PASS (framework complete)

### test_enhanced_structural_validation.py

**Validates Phase 2 (P1-1 to P1-7)**: Enhanced structural validation beyond basic file existence

**What it tests:**
- P1-1: Cross-reference validation (commands→skills, agents→commands, internal links)
- P1-2: Command template validation (required sections, content quality)
- P1-3: Agent workflow validation (stages, completeness, anti-patterns)
- P1-4: Hook script validation (syntax, error handling, exit codes)
- P1-5: MCP configuration validation (JSON schema, server configs)
- P1-6: Plugin manifest schema validation (required fields, paths, semver)
- P1-7: Markdown content quality (code blocks, headings, links)

**Why this matters:**
Catches structural issues that break plugin functionality (broken references, invalid hooks, etc.) before manual testing.

**Key test classes:**
- `TestCrossReferenceValidation` - Validates all component references
- `TestCommandTemplateValidation` - Command structure quality
- `TestAgentWorkflowValidation` - Agent workflow completeness
- `TestHookScriptValidation` - Hook shell script correctness
- `TestMCPConfigurationValidation` - MCP server configs
- `TestPluginManifestSchemaValidation` - plugin.json validation
- `TestMarkdownContentQuality` - Documentation quality

**Expected initial state:** Some tests PASS (basic structure exists), some FAIL (cross-refs broken)

**Expected after P1-1 to P1-7:** ALL TESTS PASS (structural validation complete)

### test_e2e_harness_design.py

**Validates Phase 3 (P2-1 to P2-4)**: E2E test harness design artifacts

**What it tests:**
- P2-1: E2E test harness architecture documentation
- P2-2: Conversation simulation framework design
- P2-3: Test project generator implementation (CAN implement now)
- P2-4: Claude Code API requirements documentation

**Why this matters:**
Prepares for E2E automation when Claude Code provides testing APIs. Documents requirements for Anthropic.

**Key test classes:**
- `TestE2EHarnessArchitectureDocumentation` - Harness design docs
- `TestConversationSimulationFrameworkDesign` - Conversation framework design
- `TestTestProjectGenerators` - Project generator tool (implementable now!)
- `TestClaudeCodeAPIRequirementsDocumentation` - API requirements for Anthropic
- `TestE2EHarnessDesignCompleteness` - Phase 3 completion summary

**Expected initial state:** ALL TESTS FAIL (design docs don't exist yet)

**Expected after P2-1 to P2-4:** ALL TESTS PASS (design complete, ready for API)

**Note:** P3-1 to P3-5 (actual E2E implementation) are BLOCKED on Claude Code API availability.

## Test Criteria Alignment

All tests follow the TestCriteria from the project:

✅ **Useful**: Test actual functionality and quality, not tautologies
✅ **Complete**: Cover all components and edge cases
✅ **Flexible**: Allow refactoring without changing tests (test structure, not implementation)
✅ **Fully automated**: Use pytest, no manual steps required
✅ **No ad-hoc approaches**: Follow existing test patterns in tests/ directory

## Anti-Gaming Design

These tests are designed to resist "gaming" by AI agents:

1. **Parse actual content**: Tests read and parse real files, not just check existence
2. **Validate structure**: Tests verify markdown headings, YAML fields, JSON schemas
3. **Check completeness**: Tests ensure sections have sufficient content (>100 chars, >3 sections)
4. **Verify cross-references**: Tests parse references and validate targets exist
5. **Test shell syntax**: Tests validate hook scripts with `sh -n`
6. **Require meaningful content**: Tests check for specific keywords and patterns

**Cannot be satisfied by:**
- Empty files or minimal stubs
- Generic placeholder text
- Broken cross-references
- Invalid shell syntax
- Missing required sections

## Running Tests

### Run all functional tests
```bash
pytest tests/functional/ -v
```

### Run by phase
```bash
# Phase 1: Manual testing framework
pytest tests/functional/test_manual_testing_framework.py -v

# Phase 2: Enhanced structural validation
pytest tests/functional/test_enhanced_structural_validation.py -v

# Phase 3: E2E harness design
pytest tests/functional/test_e2e_harness_design.py -v
```

### Run by work item
```bash
# Example: Run P0-1 tests (manual testing documentation)
pytest tests/functional/test_manual_testing_framework.py::TestManualTestingDocumentationFramework -v

# Example: Run P1-1 tests (cross-reference validation)
pytest tests/functional/test_enhanced_structural_validation.py::TestCrossReferenceValidation -v
```

### Run summary tests only
```bash
# Get Phase 1 completion status
pytest tests/functional/test_manual_testing_framework.py::TestManualTestingFrameworkCompleteness -v

# Get Phase 2 completion status
pytest tests/functional/test_enhanced_structural_validation.py::TestEnhancedStructuralValidationCompleteness -v

# Get Phase 3 completion status
pytest tests/functional/test_e2e_harness_design.py::TestE2EHarnessDesignCompleteness -v
```

## Test Output Interpretation

### Phase 1 Tests (Manual Testing Framework)

**All passing**: Manual testing framework is complete, ready for P0-6 execution
**Some failing**: Manual testing docs incomplete, work remaining on P0-1 to P0-5
**All failing**: Manual testing framework not started yet

**Critical for**: P0-6 (Execute manual testing for all plugins)

### Phase 2 Tests (Enhanced Structural Validation)

**All passing**: Structural validation complete, plugins have correct structure
**Some failing**: Structural issues exist (broken refs, invalid hooks, etc.)
**All failing**: Enhanced validation not implemented yet

**Critical for**: Catching issues before manual testing, preventing regressions

### Phase 3 Tests (E2E Harness Design)

**All passing**: E2E harness design complete, ready for API implementation
**Some failing**: Design docs incomplete, work remaining on P2-1 to P2-4
**All failing**: E2E harness design not started yet

**Critical for**: Rapid E2E implementation when Claude Code API becomes available

## Test Workflow Integration

These tests integrate with the overall testing workflow:

```
1. Existing Structural Tests (tests/structural/) ← Already passing
   └─> Validate basic structure (files exist, JSON valid, YAML correct)

2. NEW Functional Tests (tests/functional/) ← This directory
   └─> Validate testing framework components

   Phase 1: Manual Testing Framework
   ├─> P0-1 to P0-5: Create manual testing docs
   └─> P0-6: Execute manual testing (not automated)

   Phase 2: Enhanced Structural Validation
   └─> P1-1 to P1-7: Implement enhanced validation

   Phase 3: E2E Harness Design
   ├─> P2-1 to P2-4: Design harness (testable now)
   └─> P3-1 to P3-5: Implement harness (blocked on API)

3. Manual Testing Execution (tests/manual/) ← P0-6
   └─> Validate plugins actually work in Claude Code

4. E2E Automated Tests (tests/e2e/) ← Future
   └─> Automated plugin testing (when API available)
```

## Traceability

Each test class maps to specific work items in the PLAN:

### Phase 1 (Manual Testing)
- `TestManualTestingDocumentationFramework` → P0-1
- `TestPluginInstallationTestScenarios` → P0-2
- `TestCommandExecutionTestScenarios` → P0-3
- `TestCompleteWorkflowTestScenarios` → P0-4
- `TestAgentBehaviorObservationChecklists` → P0-5

### Phase 2 (Enhanced Structural)
- `TestCrossReferenceValidation` → P1-1
- `TestCommandTemplateValidation` → P1-2
- `TestAgentWorkflowValidation` → P1-3
- `TestHookScriptValidation` → P1-4
- `TestMCPConfigurationValidation` → P1-5
- `TestPluginManifestSchemaValidation` → P1-6
- `TestMarkdownContentQuality` → P1-7

### Phase 3 (E2E Harness Design)
- `TestE2EHarnessArchitectureDocumentation` → P2-1
- `TestConversationSimulationFrameworkDesign` → P2-2
- `TestTestProjectGenerators` → P2-3
- `TestClaudeCodeAPIRequirementsDocumentation` → P2-4

## Success Criteria

### Phase 1 Success
- [ ] All manual testing documentation exists
- [ ] All plugins have installation checklists
- [ ] All 16 commands have test scenarios
- [ ] All plugins have workflow scenarios (3-5 each)
- [ ] All plugins have agent observation checklists
- [ ] Manual testing framework ready for P0-6 execution

### Phase 2 Success
- [ ] All cross-references validated automatically
- [ ] All command templates meet quality standards
- [ ] All agent workflows complete and validated
- [ ] All hook scripts have valid syntax
- [ ] All MCP configurations valid
- [ ] All plugin manifests validated
- [ ] Markdown content quality enforced

### Phase 3 Success
- [ ] E2E harness architecture documented
- [ ] Conversation simulation framework designed
- [ ] Test project generator implemented
- [ ] Claude Code API requirements documented
- [ ] Design ready for implementation when API available

## Contributing

When adding new tests:

1. **Follow existing patterns**: Look at current test classes for structure
2. **Add traceability**: Document which PLAN work item the test validates
3. **Write docstrings**: Explain what workflow the test validates
4. **Use anti-gaming patterns**: Verify actual content, not just existence
5. **Add to README**: Document the new test class and its purpose

## Questions?

See the master plan: `PLAN-testing-framework-2025-11-06-021441.md`

For project context: `CLAUDE.md`
