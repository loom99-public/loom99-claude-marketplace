# Testing Framework: Next Steps Implementation Plan

**Generated**: 2025-11-06 03:20:04
**Source STATUS**: STATUS-testing-framework-2025-11-06-031516.md
**Previous PLAN**: PLAN-testing-framework-2025-11-06-021441.md (COMPLETE - retiring)
**Specification**: CLAUDE.md (Last modified: 2025-11-06)
**Plan Type**: Focused Action Plan for Remaining Work

---

## Executive Summary

### Current State (from STATUS-testing-framework-2025-11-06-031516.md)

**Implementation Progress**: 73% complete
- **Phase 1 (Manual Testing Framework)**: 100% COMPLETE ✅ - Ready for execution
- **Phase 2 (Enhanced Structural Validation)**: 80% COMPLETE - Catching real issues
- **Phase 3 (E2E Harness Design)**: 0% COMPLETE - Not started (expected)

**Test Results**: 251 of 291 tests passing (86%)

**Critical Finding**: Manual testing framework exists and is comprehensive but **HAS NOT BEEN EXECUTED** in real Claude Code environment. This is the primary blocker for production readiness.

### What Changed Since Last Plan

The **PLAN-testing-framework-2025-11-06-021441.md** has been completed with significant achievements:
- All P0-1 through P0-5 work items complete (manual testing framework built)
- All P1-1 through P1-7 work items complete (enhanced structural validation implemented)
- 17 documentation files created (3,236 lines)
- 157 functional tests implemented (6,018 lines)

This NEW plan focuses ONLY on:
1. **Executing manual testing** (P0-6) - THE critical blocker
2. **Fixing the 14 structural issues** found by Phase 2 tests
3. **Resolving promptctl plugin status** (P0-7)
4. **Planning Phase 3 work** for future implementation

### This Plan's Scope

**IMMEDIATE PRIORITIES (This Week)**:
- P0-6: Execute manual testing in real Claude Code (6-9 hours)
- Fix 14 structural issues caught by automated tests (2-3 hours)
- Resolve promptctl documentation gap (1-2 hours)

**NEAR-TERM WORK (Next 2 Weeks)**:
- Iterate on P0-6 findings and fix discovered bugs
- Complete remaining Phase 2 polish work

**LONG-TERM WORK (Next 1-3 Months)**:
- Execute Phase 3 design work (P2-1 to P2-4)
- Prepare for E2E automation when Claude Code API becomes available

---

## IMMEDIATE PRIORITIES (This Week)

### P0-6-EXEC: Execute Manual Testing for All Plugins - CRITICAL 🔴

**Status**: Not Started (Framework 100% ready)
**Effort**: Large (6-9 hours over 2-3 days)
**Dependencies**: None - can start immediately
**Spec Reference**: Section 8 "Proposed Action Plan" • **Status Reference**: STATUS-testing-framework-2025-11-06-031516.md Section "What We Can Test NOW"

#### Description

Execute the comprehensive manual testing framework that was built in Phase 1. This is **THE CRITICAL BLOCKER** for production readiness. The framework exists, is well-documented, and ready to use. We just need to execute it.

**Why This is Critical**: This is the ONLY way to validate that plugins actually work in Claude Code. All existing tests validate structure, not functionality.

#### Execution Breakdown

**Step 1: Setup and Preparation** (30 minutes)
- [ ] Open Claude Code
- [ ] Navigate to plugin marketplace settings
- [ ] Have /Users/bmf/icode/loom99-claude-marketplace ready
- [ ] Open tests/manual/README.md for reference
- [ ] Open tests/manual/TESTING_RESULTS.md for recording results

**Step 2: Test agent-loop Plugin** (2-3 hours)
- [ ] Install agent-loop plugin using tests/manual/installation-agent-loop.md checklist
- [ ] Verify 4 commands, 1 agent, 4 skills, hooks registered
- [ ] Execute command tests using tests/manual/commands-agent-loop.md
  - [ ] Test /explore command
  - [ ] Test /plan command
  - [ ] Test /code command
  - [ ] Test /commit command
- [ ] Execute at least 2 workflow scenarios from tests/manual/workflows-agent-loop.md
  - [ ] Recommended: "Simple Feature Addition" (add logging to Express app)
  - [ ] Recommended: "Bug Fix" scenario
- [ ] Observe agent behavior using tests/manual/agent-agent-loop.md checklist
- [ ] Record all results in TESTING_RESULTS.md
- [ ] File issues for any bugs using ISSUE_TEMPLATE.md

**Step 3: Test epti Plugin** (2-3 hours)
- [ ] Install epti plugin using tests/manual/installation-epti.md checklist
- [ ] Verify 6 commands, 1 agent, 5 skills, 3 hooks registered
- [ ] Execute command tests using tests/manual/commands-epti.md
  - [ ] Test /write-tests command
  - [ ] Test /verify-fail command
  - [ ] Test /commit-tests command
  - [ ] Test /implement command
  - [ ] Test /iterate command
  - [ ] Test /commit-code command
- [ ] Execute at least 2 TDD workflow scenarios from tests/manual/workflows-epti.md
  - [ ] Recommended: "New Feature with TDD" (calculator class)
  - [ ] Recommended: "Bug Fix with TDD" scenario
- [ ] Verify strict TDD enforcement (no test modifications during implementation)
- [ ] Observe agent behavior using tests/manual/agent-epti.md checklist
- [ ] Record all results in TESTING_RESULTS.md
- [ ] File issues for any bugs using ISSUE_TEMPLATE.md

**Step 4: Test visual-iteration Plugin** (2-3 hours)
- [ ] Install visual-iteration plugin using tests/manual/installation-visual-iteration.md checklist
- [ ] Verify 6 commands, 1 agent, 4 skills, hooks, MCP browser-tools registered
- [ ] Verify browser-tools MCP server starts successfully
- [ ] Execute command tests using tests/manual/commands-visual-iteration.md
  - [ ] Test /screenshot command
  - [ ] Test /load-mock command
  - [ ] Test /implement-design command
  - [ ] Test /iterate command
  - [ ] Test /compare command
  - [ ] Test /visual-commit command
- [ ] Execute at least 2 visual iteration scenarios from tests/manual/workflows-visual-iteration.md
  - [ ] Recommended: "UI Component Refinement" (button styling)
  - [ ] Recommended: "Design Mockup Implementation" (landing page)
- [ ] Verify screenshot capture and comparison working
- [ ] Observe agent behavior using tests/manual/agent-visual-iteration.md checklist
- [ ] Record all results in TESTING_RESULTS.md
- [ ] File issues for any bugs using ISSUE_TEMPLATE.md

**Step 5: Consolidation and Reporting** (30-60 minutes)
- [ ] Review all TESTING_RESULTS.md entries
- [ ] Summarize pass/fail rates for each plugin
- [ ] Prioritize issues by severity (Critical, High, Medium, Low)
- [ ] Update CLAUDE.md with actual testing status
- [ ] Create summary report of findings

#### Acceptance Criteria

- [ ] All 3 plugins successfully install in Claude Code
- [ ] All 16 commands execute and provide appropriate guidance
- [ ] At least 2 complete workflows succeed per plugin (6 total)
- [ ] All command tests documented with pass/fail in TESTING_RESULTS.md
- [ ] All workflow tests documented with outcomes
- [ ] All bugs discovered filed with ISSUE_TEMPLATE.md format
- [ ] Agent behavior observations recorded for each plugin
- [ ] CLAUDE.md updated with real testing status (not claimed "100% complete" anymore)
- [ ] Overall pass rate of at least 80% for functional tests

#### Technical Notes

**Testing Environment**:
- Use real Claude Code (not mock or simulation)
- Use real codebases (not toy examples)
- Complete full workflows (no shortcuts)
- Take detailed notes of all observations

**Issue Severity Definitions** (from ISSUE_TEMPLATE.md):
- **Critical**: Plugin cannot be used at all
- **High**: Major feature broken, serious workflow blocker
- **Medium**: Feature works but has issues or workarounds needed
- **Low**: Minor polish needed, cosmetic issues

**Success Threshold**: 80% pass rate means:
- 13 of 16 commands work correctly
- 5 of 6 workflows complete successfully
- No critical issues blocking core functionality

**If Testing Reveals Major Issues**: This is GOOD. Finding issues now prevents users from encountering them. Document thoroughly and prioritize fixes.

---

### STRUCT-FIX-01: Fix 14 Structural Issues Found by Phase 2 Tests - HIGH 🟡

**Status**: Not Started
**Effort**: Medium (2-3 hours)
**Dependencies**: None
**Spec Reference**: CLAUDE.md quality standards • **Status Reference**: STATUS-testing-framework-2025-11-06-031516.md Section "Blocking Issues"

#### Description

Phase 2 enhanced structural validation tests found **14 genuine issues** in the plugin implementations:
- 8 TODO/FIXME/XXX comments in production code
- 2 agent-command cross-reference mismatches
- 1 broken path reference (agent-loop hooks/hooks.json)
- 10 heading hierarchy violations
- 1 MCP configuration issue (visual-iteration)

These are NOT false positives - they are real quality issues that should be fixed.

#### Issues to Fix

**Issue 1: Remove 8 TODO Comments from Production Code** (30 minutes)

Files with TODO comments:
- `/Users/bmf/icode/loom99-claude-marketplace/plugins/agent-loop/agents/workflow-agent.md`
- `/Users/bmf/icode/loom99-claude-marketplace/plugins/agent-loop/commands/commit.md`
- `/Users/bmf/icode/loom99-claude-marketplace/plugins/agent-loop/commands/code.md`
- `/Users/bmf/icode/loom99-claude-marketplace/plugins/agent-loop/skills/code-exploration/SKILL.md`
- `/Users/bmf/icode/loom99-claude-marketplace/plugins/epti/commands/commit-code.md`
- `/Users/bmf/icode/loom99-claude-marketplace/plugins/epti/commands/write-tests.md`

Files with XXX comments:
- `/Users/bmf/icode/loom99-claude-marketplace/plugins/visual-iteration/commands/screenshot.md`
- `/Users/bmf/icode/loom99-claude-marketplace/plugins/visual-iteration/skills/visual-comparison/SKILL.md`

**Action**:
- [ ] Search each file for TODO, FIXME, XXX comments
- [ ] Either complete the implementation or remove the comment
- [ ] If implementation is incomplete, add work item to track separately
- [ ] Verify no TODO/FIXME/XXX remains in production code

**Issue 2: Fix 2 Agent-Command Cross-Reference Mismatches** (30 minutes)

Problems detected:
- epti agent references `/iterate` but command name doesn't match
- visual-iteration agent references commands that don't match actual filenames

**Action**:
- [ ] Review epti/agents/tdd-agent.md for command references
- [ ] Review visual-iteration/agents/visual-iteration-agent.md for command references
- [ ] Compare referenced command names to actual files in commands/ directories
- [ ] Update agent references to match actual command filenames
- [ ] Verify cross-reference validation tests pass

**Issue 3: Fix agent-loop Broken Path Reference** (15 minutes)

Problem: plugin.json references `./hooks/hooks.json` but file doesn't exist

**Action**:
- [ ] Check if agent-loop should have hooks
- [ ] If YES: Create hooks/hooks.json with appropriate hook definitions
- [ ] If NO: Remove hooks reference from plugin.json
- [ ] Verify plugin manifest validation tests pass

**Issue 4: Fix 10 Heading Hierarchy Violations** (45 minutes)

Problem: Markdown files skip heading levels (e.g., H1 → H3 without H2)

Affected files (from test output):
- agent-loop: 2 files (skills/verification/SKILL.md, skills/git-operations/SKILL.md)
- epti: 8 files (multiple agents/commands/skills)

**Action**:
- [ ] Use markdown linter or manual review to find heading skips
- [ ] Fix heading levels to follow proper hierarchy (H1 → H2 → H3, never skip)
- [ ] Verify markdown content quality tests pass
- [ ] Ensure documentation remains readable

**Issue 5: Fix visual-iteration MCP Configuration** (15 minutes)

Problem: `.mcp.json` missing required fields for browser-tools server

**Action**:
- [ ] Review visual-iteration/.mcp.json
- [ ] Add missing required fields (command, args, env if needed)
- [ ] Verify MCP configuration validation tests pass
- [ ] Test that browser-tools MCP server can initialize (during P0-6)

#### Acceptance Criteria

- [ ] All 8 TODO/FIXME/XXX comments resolved
- [ ] 2 agent-command mismatches fixed
- [ ] agent-loop hooks path issue resolved
- [ ] 10 heading hierarchy violations corrected
- [ ] visual-iteration MCP config complete
- [ ] Phase 2 test pass rate increases from 82% to ~95%
- [ ] No false positives remain (all failures are real issues)

#### Technical Notes

**Test Command to Verify Fixes**:
```bash
cd /Users/bmf/icode/loom99-claude-marketplace
source .venv/bin/activate
pytest tests/functional/test_enhanced_structural_validation.py -v
```

**Expected Outcome After Fixes**:
- P1-1 (Cross-Reference Validation): 18/18 passing (currently 16/18)
- P1-6 (Plugin Manifest Validation): 9/9 passing (currently 8/9)
- P1-7 (Markdown Content Quality): 6/6 passing (currently 1/6)
- P1-5 (MCP Configuration Validation): 6/6 passing (currently 5/6)

**Git Workflow**:
- Make fixes in feature branch
- Run structural validation tests
- Commit with message: "fix: resolve 14 structural issues found by automated tests"
- Re-run tests to verify

---

### P0-7: Resolve promptctl Plugin Status - MEDIUM 🟡

**Status**: Not Started
**Effort**: Small (1-2 hours)
**Dependencies**: None
**Spec Reference**: CLAUDE.md documentation standards • **Status Reference**: STATUS-testing-framework-2025-11-06-031516.md Section "Work Item Status"

#### Description

The STATUS report identified that `promptctl` plugin exists in the repository but is not documented in CLAUDE.md. This creates documentation ambiguity - is promptctl part of the marketplace or work-in-progress?

**Evidence**:
- `plugins/promptctl/` directory exists
- Contains hooks/hooks.json and bin/dispatch.sh
- Not mentioned in CLAUDE.md "Current Plugins" section
- Not clear if it's included in marketplace.json

#### Action Options

**Option A: Document promptctl in Marketplace** (if it's production-ready)
- [ ] Review promptctl plugin structure and implementation
- [ ] Determine if promptctl is complete and functional
- [ ] Add promptctl section to CLAUDE.md with full documentation
  - Purpose and overview
  - Implementation details (hooks, scripts)
  - Line counts and completion status
  - Testing status
- [ ] Verify promptctl is listed in .claude-plugin/marketplace.json
- [ ] Create manual test scenarios for promptctl (if pursuing P0-6 for it)
- [ ] Update marketplace plugin count (currently "3 plugins", would become "4 plugins")

**Option B: Remove promptctl from Marketplace** (if it's WIP)
- [ ] Verify promptctl is experimental or incomplete
- [ ] Remove promptctl from .claude-plugin/marketplace.json (if listed)
- [ ] Move plugins/promptctl/ to archive/ or separate repository
- [ ] Update CLAUDE.md to reflect 3 production plugins only
- [ ] Document promptctl status in planning files (experimental, future work, etc.)

**Option C: Mark promptctl as Experimental** (middle ground)
- [ ] Add promptctl section to CLAUDE.md with "EXPERIMENTAL" status
- [ ] Document what exists and what's incomplete
- [ ] Mark as excluded from production marketplace
- [ ] Keep code in repo for future development

#### Acceptance Criteria

- [ ] promptctl status is clearly documented in CLAUDE.md
- [ ] Decision made: Include, Exclude, or Mark Experimental
- [ ] Marketplace.json accurately reflects included plugins
- [ ] No ambiguity about promptctl's production readiness
- [ ] Plugin count in CLAUDE.md is accurate

#### Technical Notes

**Investigation Steps**:
1. Review `/Users/bmf/icode/loom99-claude-marketplace/plugins/promptctl/`
2. Check `.claude-plugin/marketplace.json` for promptctl entry
3. Assess completeness (is it at same quality level as agent-loop/epti/visual-iteration?)
4. Make decision based on actual state

**Current Documented Plugins**:
- agent-loop: v0.1.0 (100% complete)
- epti: v0.1.0 (100% complete)
- visual-iteration: v0.1.0 (100% complete)

**Pattern**: All documented plugins are at v0.1.0 and 100% complete. If promptctl is not at this level, it should not be documented as production-ready.

---

## NEAR-TERM WORK (Next 2 Weeks)

### ITERATE-P0-6: Iterate on Manual Testing Results - HIGH 🟡

**Status**: Blocked (depends on P0-6 execution)
**Effort**: Variable (1-2 weeks estimated)
**Dependencies**: P0-6-EXEC must complete first
**Spec Reference**: Section 8 "Proposed Action Plan" • **Status Reference**: STATUS-testing-framework-2025-11-06-031516.md Section "Near-Term Actions"

#### Description

After P0-6 execution, manual testing will likely reveal bugs, usability issues, or missing functionality. This work item covers the iteration cycle: fix bugs, retest, refine, repeat until production ready.

**Assumption**: Manual testing will find 10-20 issues ranging from Critical to Low severity. This is expected and healthy.

#### Execution Process

**Step 1: Triage Issues** (after P0-6)
- [ ] Review all issues filed in TESTING_RESULTS.md
- [ ] Categorize by severity: Critical, High, Medium, Low
- [ ] Identify patterns (e.g., multiple issues in same component)
- [ ] Prioritize Critical and High issues for immediate fixing
- [ ] Defer Low priority issues to future polish phase

**Step 2: Fix Critical Issues** (priority 1)
- [ ] Address all Critical severity issues (plugin cannot be used)
- [ ] Retest affected workflows after each fix
- [ ] Update TESTING_RESULTS.md with retest outcomes
- [ ] Verify fix doesn't break other functionality

**Step 3: Fix High Severity Issues** (priority 2)
- [ ] Address all High severity issues (major features broken)
- [ ] Retest affected workflows after each fix
- [ ] Update TESTING_RESULTS.md with retest outcomes
- [ ] Document any workarounds if full fix not immediately possible

**Step 4: Evaluate Medium/Low Issues** (priority 3)
- [ ] Review Medium severity issues (features work but have problems)
- [ ] Decide: Fix now or defer to future iteration
- [ ] Review Low severity issues (minor polish)
- [ ] Document decisions for deferred items

**Step 5: Retest Complete Workflows** (validation)
- [ ] Re-run at least 1 complete workflow per plugin
- [ ] Verify all Critical and High issues resolved
- [ ] Document final pass/fail rate in TESTING_RESULTS.md
- [ ] Update CLAUDE.md with production readiness status

#### Acceptance Criteria

- [ ] All Critical issues resolved (0 critical bugs remaining)
- [ ] All High severity issues fixed or documented with workarounds
- [ ] At least 80% of workflows pass successfully
- [ ] Updated TESTING_RESULTS.md shows improvements
- [ ] CLAUDE.md reflects accurate production status (not "100% MVP" if bugs remain)

#### Technical Notes

**Likely Issue Categories** (based on typical plugin testing):
1. **Command Execution Issues**: Commands don't expand correctly, missing content
2. **Agent Behavior Issues**: Agent doesn't enforce expected guardrails
3. **Hook Execution Issues**: Hooks don't trigger or execute incorrectly
4. **MCP Integration Issues**: Browser-tools doesn't start or functions incorrectly
5. **Workflow Transition Issues**: Moving between stages feels unnatural
6. **Documentation Issues**: Command guidance unclear or insufficient

**Iteration Velocity**: Assume 2-3 issues can be fixed per day. A backlog of 15 issues = ~1 week of work.

**When to Stop Iterating**: When Critical and High issues are zero and overall workflow success rate is 80%+.

---

### PHASE2-POLISH: Complete Phase 2 Polish Work - MEDIUM 🟡

**Status**: Not Started
**Effort**: Medium (1 week)
**Dependencies**: STRUCT-FIX-01 completion
**Spec Reference**: Section 5 "Realistic Testing Approach" • **Status Reference**: STATUS-testing-framework-2025-11-06-031516.md Section "Phase 2 Summary"

#### Description

Phase 2 enhanced structural validation is 80% complete with 82% pass rate. After fixing the 14 known issues (STRUCT-FIX-01), some additional polish work remains to achieve 95%+ pass rate.

**Current State**: 64 of 78 tests passing (82%)
**Target State**: 74 of 78 tests passing (95%+)

#### Remaining Work Items

**Polish Task 1: Improve Command Template Validation** (2 days)
- [ ] Review agent-loop commands flagged for insufficient actionable content
- [ ] Compare content depth to epti and visual-iteration commands
- [ ] Add more detailed guidance where appropriate
- [ ] Verify command template validation tests pass

**Polish Task 2: Enhance Agent Workflow Validation** (2 days)
- [ ] Review epti agent stages vs. available commands
- [ ] Review visual-iteration agent stages vs. available commands
- [ ] Align agent documentation with actual command implementations
- [ ] Update agent references to match command filenames
- [ ] Verify agent workflow validation tests pass

**Polish Task 3: Reduce False Negatives** (1 day)
- [ ] Review 4 false negative test failures from Phase 1
  - README Troubleshooting section detection
  - 3 workflow scenarios "execution steps" detection
- [ ] Improve markdown parsers to better detect existing content
- [ ] Verify tests detect real issues, not formatting quirks
- [ ] Aim for <2% false negative rate

**Polish Task 4: Add Hook Unit Tests** (2 days)
- [ ] Implement unit tests for epti hook shell commands (beyond syntax checking)
- [ ] Test pre-implementation hook detects missing tests
- [ ] Test post-code hook runs test suite correctly
- [ ] Test pre-commit hook blocks commits with failing tests
- [ ] Test commit-msg hook validates conventional commit format
- [ ] Implement unit tests for visual-iteration hook shell commands

#### Acceptance Criteria

- [ ] Phase 2 test pass rate increases to 95%+ (74+ of 78 tests passing)
- [ ] False negative rate below 2% (<2 test failures that aren't real issues)
- [ ] All Phase 2 validation tests are meaningful (not tautological)
- [ ] Hook unit tests cover both success and failure paths
- [ ] Command template validation catches quality issues consistently

#### Technical Notes

**Test Execution**:
```bash
cd /Users/bmf/icode/loom99-claude-marketplace
source .venv/bin/activate
pytest tests/functional/test_enhanced_structural_validation.py -v
```

**Success Metric**: Pass rate 95%+ means only 1-2 tests may be failing, and those failures should represent genuinely ambiguous cases or edge cases, not production issues.

---

## LONG-TERM WORK (Next 1-3 Months)

### P2-1: Design E2E Test Harness Architecture - LOW 🟢

**Status**: Not Started
**Effort**: Medium (1 week - design only)
**Dependencies**: None (design can proceed without API)
**Spec Reference**: Section 5 "Realistic Testing Approach - Phase 2" • **Status Reference**: STATUS-testing-framework-2025-11-06-031516.md Section "Phase 3: E2E Test Harness Design"

#### Description

Design the architecture for an automated E2E testing framework that can be implemented when Claude Code provides testing APIs. This is documentation and design work only - no implementation until API becomes available.

**Deliverable**: Comprehensive design document for future implementation

#### Design Components

**Component 1: Required Claude Code API Specification** (2 days)

Document what APIs we need from Claude Code:
- [ ] Plugin management API (install, uninstall, list, reload)
- [ ] Command execution API (execute slash commands, capture expanded prompts)
- [ ] Conversation API (start conversation, send messages, receive responses)
- [ ] Observability API (skill invocation logs, agent rule application, hook execution logs)
- [ ] Testing utilities API (mock filesystem, mock git, test data injection)

**Component 2: Test Harness Class Architecture** (2 days)

Design test harness interfaces and classes:
- [ ] E2ETestHarness main class with setup/teardown
- [ ] PluginManager for installation/loading
- [ ] ConversationSimulator for multi-turn interactions
- [ ] DeliverableValidator for verifying outputs (code, tests, commits)
- [ ] TestProjectGenerator for creating realistic test projects

**Component 3: Integration Points** (1 day)

Define how test harness integrates with:
- [ ] Claude Code plugin system
- [ ] MCP servers (browser-tools for visual-iteration)
- [ ] Git repositories (for commit verification)
- [ ] Test frameworks (pytest, jest, go test for epti testing)
- [ ] CI/CD pipelines (GitHub Actions, etc.)

**Component 4: API Request Template for Anthropic** (1 day)

Create feature request document:
- [ ] Describe why automated testing is valuable for plugin ecosystem
- [ ] List required API capabilities with use cases
- [ ] Provide code examples of desired API usage
- [ ] Estimate effort to implement on Anthropic's side
- [ ] Offer to collaborate on design or implementation

#### Acceptance Criteria

- [ ] Design document created: `docs/e2e-harness-architecture.md`
- [ ] All required API capabilities documented
- [ ] Test harness class structure defined with interfaces
- [ ] Integration points clearly specified
- [ ] API request template ready to send to Anthropic
- [ ] Design enables rapid implementation when API becomes available

#### Technical Notes

**Example API Usage** (from design):
```python
class ClaudeCodeAPI:
    """Required APIs for plugin testing."""
    def install_plugin(self, path: str) -> InstallResult
    def uninstall_plugin(self, name: str) -> bool
    def list_plugins(self) -> List[Plugin]
    def execute_command(self, command: str) -> CommandResult
    def start_conversation(self, plugin: str) -> Conversation
    def send_message(self, conversation: Conversation, message: str) -> Response

class E2ETestHarness:
    """Test harness for automated E2E testing."""
    def setup_test_environment(self) -> TestEnv
    def load_plugin(self, plugin_name: str) -> Plugin
    def execute_workflow(self, steps: List[WorkflowStep]) -> WorkflowResult
    def validate_deliverables(self, expected: Deliverables) -> ValidationResult
```

**Design Serves Multiple Purposes**:
1. Blueprint for future implementation (when API available)
2. Requirements document for Anthropic (API request)
3. Specification for test authors (how to write E2E tests)

---

### P2-2: Design Conversation Simulation Framework - LOW 🟢

**Status**: Not Started
**Effort**: Medium (1 week - design only)
**Dependencies**: P2-1 (harness architecture)
**Spec Reference**: Section 4 "Technical Blockers - Blocker #2" • **Status Reference**: STATUS-testing-framework-2025-11-06-031516.md Section "Phase 3: E2E Test Harness Design"

#### Description

Design a framework for simulating multi-turn conversations with Claude in plugin context. The key challenge: How do we verify Claude followed agent guidance during a conversation?

**Key Research Question**: Can we observe agent behavior programmatically or only qualitatively?

#### Design Components

**Component 1: Conversation State Model** (2 days)

Define conversation state structure:
- [ ] Message/response abstraction (user messages, Claude responses)
- [ ] Agent context injection mechanism (how agent becomes active)
- [ ] Skill invocation tracking (when/how skills are used)
- [ ] Workflow stage tracking (which stage of agent workflow is active)
- [ ] Conversation history management (full transcript available)

**Component 2: Observability Requirements** (2 days)

Document what we need to observe:
- [ ] Which agent rules were considered during response generation
- [ ] Which skills were invoked and with what parameters
- [ ] Whether agent guardrails were enforced (anti-patterns blocked)
- [ ] Stage transitions in workflow (explore → plan → code → commit)
- [ ] Hook executions triggered by conversation actions

**Component 3: Assertion Framework** (1 day)

Design test assertions for conversation validation:
- [ ] assert_guidance_provided(guidance: str) - Agent gave specific guidance
- [ ] assert_skill_invoked(skill: str) - Specific skill was used
- [ ] assert_agent_rule_followed(rule: str) - Agent rule was enforced
- [ ] assert_stage_transition(from_stage: str, to_stage: str) - Workflow progressed correctly
- [ ] get_conversation_transcript() -> List[Turn] - Full conversation history

**Component 4: Heuristic Testing Approach** (2 days)

Design fallback approach if observability unavailable:
- [ ] Response content analysis (if response contains certain phrases, infer agent guidance)
- [ ] Deliverable analysis (if correct deliverables produced, infer workflow followed)
- [ ] Correlation metrics (measure correlation between agent rules and responses)
- [ ] Probabilistic validation (not perfect, but better than nothing)

#### Acceptance Criteria

- [ ] Design document created: `docs/conversation-simulation-framework.md`
- [ ] Conversation state model defined
- [ ] Observability requirements documented
- [ ] Assertion framework specified
- [ ] Heuristic testing approach designed (fallback if no observability)
- [ ] Example test scenarios demonstrating API usage
- [ ] Research conclusions on observability feasibility

#### Technical Notes

**Key Challenge**: Agent behavior verification

**Ideal Solution**: Claude Code provides observability into which agent sections were active and which rules were applied during response generation.

**Fallback Solution**: Heuristic analysis based on response content and deliverables. Less precise but still valuable.

**Example Heuristic Test**:
```python
def test_tdd_agent_prevents_test_modification():
    """Verify TDD agent blocks test modifications during implementation."""
    conversation = harness.start_conversation("epti")
    conversation.execute_command("/write-tests")
    conversation.send_message("Write tests for add(a, b) function")
    # ... tests written ...
    conversation.execute_command("/implement")
    conversation.send_message("Implement add function")
    # ... implementation completed ...

    # Heuristic: If tests were modified during implementation, agent failed
    test_file_changes = conversation.get_file_changes("tests/")
    assert test_file_changes.count() == 0, "Agent should prevent test modifications during implementation"
```

This doesn't verify HOW the agent prevented modifications, but it verifies the OUTCOME (tests weren't modified).

---

### P2-3: Implement Test Project Generator - LOW 🟢

**Status**: Not Started
**Effort**: Small (3 days)
**Dependencies**: None (can be implemented now)
**Spec Reference**: Section 5 "Realistic Testing Approach - Phase 2 Task 4" • **Status Reference**: STATUS-testing-framework-2025-11-06-031516.md Section "Phase 3: E2E Test Harness Design"

#### Description

Create a tool for generating realistic test projects that can be used for manual testing (now) and E2E automation (later). This CAN be implemented immediately as it doesn't depend on Claude Code API.

**Value**: Speeds up manual testing by providing ready-made test projects instead of requiring testers to create them.

#### Implementation Tasks

**Task 1: Design Project Template System** (1 day)

- [ ] Create templates directory structure: `tests/test-projects/templates/`
- [ ] Define template metadata format (JSON or YAML)
- [ ] Design template variable substitution system
- [ ] Document how to create new templates

**Task 2: Create Sample Project Templates** (1 day)

For agent-loop testing:
- [ ] Node.js Express.js app template (simple REST API)
- [ ] Python Flask app template (simple web app)
- [ ] Go service template (simple CLI tool)

For epti testing:
- [ ] Python pytest project template (minimal codebase)
- [ ] JavaScript jest project template (minimal codebase)
- [ ] Go testing project template (minimal codebase)

For visual-iteration testing:
- [ ] HTML/CSS/JS static site template (simple landing page)
- [ ] React component library template (simple component)

**Task 3: Implement Generator CLI Tool** (1 day)

- [ ] Create `tools/generate_test_project.py` script
- [ ] Command-line interface for generating projects
- [ ] Template selection and customization
- [ ] Git initialization and initial commit
- [ ] Dependency installation (npm install, pip install, etc.)
- [ ] Verification that generated project is valid

#### Acceptance Criteria

- [ ] Generator tool implemented: `tools/generate_test_project.py`
- [ ] At least 8 project templates created (3 for agent-loop, 3 for epti, 2 for visual-iteration)
- [ ] Templates include realistic code structure and configuration
- [ ] Generator CLI has clear usage instructions
- [ ] Generated projects are immediately usable for testing
- [ ] Documentation for creating new templates exists

#### Technical Notes

**Generator CLI Usage**:
```bash
# Generate Node.js Express app for agent-loop testing
python tools/generate_test_project.py --template node-express --name test-app

# Generate Python pytest project for epti testing
python tools/generate_test_project.py --template python-pytest --name test-calculator

# Generate static site for visual-iteration testing
python tools/generate_test_project.py --template html-landing --name test-landing
```

**Generated Project Structure**:
```
test-app/
├── .git/                  # Git repository initialized
├── src/                   # Source code
├── tests/                 # Tests (if applicable)
├── package.json           # Dependencies (if applicable)
├── README.md              # Project description
└── .gitignore             # Standard gitignore
```

**Templates Should Include**:
- Intentional gaps for testing (e.g., missing logging, missing tests, visual polish needed)
- Realistic project structure (not toy examples)
- Working configuration (dependencies installable)
- Initial commit with message "chore: initialize project"

**Value for Manual Testing**: Reduces setup time from 15-20 minutes to 2-3 minutes per test project. Enables more thorough manual testing in same timeframe.

---

### P2-4: Document Claude Code API Requirements - LOW 🟢

**Status**: Not Started
**Effort**: Small (2-3 days)
**Dependencies**: P2-1 (harness architecture)
**Spec Reference**: Section 4 "Technical Blockers - Blocker #1" • **Status Reference**: STATUS-testing-framework-2025-11-06-031516.md Section "Phase 3: E2E Test Harness Design"

#### Description

Research and document what testing capabilities we need from Claude Code, then create a feature request for Anthropic. This informs future API development and positions us to provide valuable feedback.

#### Research Tasks

**Task 1: Document Required API Endpoints** (1 day)

Required capabilities:
- [ ] Plugin Management API (install, uninstall, query, reload)
- [ ] Command Execution API (execute commands, capture expansions)
- [ ] Conversation API (start, send messages, receive responses)
- [ ] Observability API (skill logs, agent logs, hook logs, MCP logs)
- [ ] Testing Utilities API (mock filesystem, mock git, deterministic mode)

**Task 2: Research Existing Solutions** (1 day)

- [ ] Check if Claude Code CLI exists or is planned
- [ ] Search Claude Code documentation for testing APIs
- [ ] Look for community solutions to plugin testing
- [ ] Investigate reverse-engineering Claude Code (risk assessment)
- [ ] Explore using Claude API directly as alternative (bypassing Claude Code)

**Task 3: Assess Alternatives** (1 day)

If Claude Code API unavailable:
- [ ] Can we use Claude API directly with plugin prompts?
- [ ] Can we mock Claude Code environment for testing?
- [ ] Are there testing tools in Claude Code source code?
- [ ] What's the effort to implement workarounds vs. waiting for API?

**Task 4: Create Feature Request for Anthropic** (1 day)

- [ ] Write comprehensive feature request document
- [ ] Include use cases demonstrating value
- [ ] Provide code examples of desired API usage
- [ ] Estimate value to plugin ecosystem
- [ ] Offer to collaborate on design/implementation
- [ ] Submit to appropriate Anthropic channel (forum, GitHub, support)

#### Acceptance Criteria

- [ ] API requirements documented: `docs/claude-code-api-requirements.md`
- [ ] Research summary of existing solutions completed
- [ ] Alternative approaches assessed and documented
- [ ] Feature request created and submitted to Anthropic
- [ ] Decision made: Wait for API, implement workaround, or accept manual testing only

#### Technical Notes

**Required Capabilities Summary**:

1. **Plugin Management API**:
   - `install_plugin(path: str) -> InstallResult`
   - `uninstall_plugin(name: str) -> bool`
   - `list_plugins() -> List[Plugin]`
   - `reload_plugin(name: str) -> bool`

2. **Command Execution API**:
   - `execute_command(command: str) -> CommandResult`
   - `get_command_expansion(command: str) -> str`
   - `get_command_list() -> List[str]`

3. **Conversation API**:
   - `start_conversation(plugin: str) -> Conversation`
   - `send_message(conversation: Conversation, message: str) -> Response`
   - `get_conversation_history(conversation: Conversation) -> List[Turn]`

4. **Observability API** (most valuable for testing):
   - `get_skill_invocations(conversation: Conversation) -> List[SkillInvocation]`
   - `get_agent_rule_applications(conversation: Conversation) -> List[RuleApplication]`
   - `get_hook_executions() -> List[HookExecution]`
   - `get_mcp_interactions() -> List[MCPCall]`

5. **Testing Utilities API**:
   - `create_mock_filesystem(structure: Dict) -> MockFS`
   - `create_mock_git_repo(commits: List[Commit]) -> MockRepo`
   - `inject_test_data(data: Any) -> None`
   - `enable_deterministic_mode() -> None` (for reproducible testing)

**Alternative: Direct Claude API Usage**

If Claude Code API unavailable, explore:
- Can we send plugin prompts directly to Claude API?
- Can we simulate plugin context without Claude Code?
- What's the fidelity gap between Claude Code and Claude API?

**Decision Point**: After research, decide whether to:
1. Wait for Claude Code API (accept manual testing only)
2. Implement workaround using Claude API directly
3. Reverse-engineer Claude Code (risky)
4. Accept E2E automation is not feasible

---

## Risk Assessment

### Critical Risks

**Risk #1: Manual Testing Reveals Major Bugs**

**Likelihood**: MEDIUM-HIGH (60-70%)
**Impact**: HIGH (delays production readiness by 1-2 weeks)
**Mitigation**:
- Prioritize P0-6 immediately
- Fix Critical/High issues before claiming production ready
- Iterate quickly on discovered issues
- Document all issues thoroughly

**Trigger**: If P0-6 execution finds >5 Critical or High severity bugs

---

**Risk #2: Manual Testing Shows Plugins Don't Work as Designed**

**Likelihood**: LOW-MEDIUM (20-30%)
**Impact**: CRITICAL (requires redesign, 1-2 months delay)
**Mitigation**:
- Start with simplest plugin (agent-loop)
- Test incrementally, not all at once
- Be prepared to iterate on design
- Don't claim "100% MVP complete" prematurely

**Trigger**: If core workflows fail to complete successfully

---

**Risk #3: Structural Fixes Break Functionality**

**Likelihood**: LOW (10-20%)
**Impact**: MEDIUM (adds 2-3 days to timeline)
**Mitigation**:
- Fix structural issues in isolated commits
- Run structural validation tests after each fix
- Test manually if change affects user-facing behavior
- Roll back if fix causes regression

**Trigger**: If fixing TODO comments or cross-references changes plugin behavior

---

### Medium Risks

**Risk #4: P0-6 Execution Takes Longer Than Expected**

**Likelihood**: MEDIUM (40-50%)
**Impact**: MEDIUM (timeline extends by 1-2 days)
**Mitigation**:
- Allocate 6-9 hours over 2-3 days (not 1 day)
- Prioritize 2 workflows per plugin (not all 11 scenarios)
- Accept 80% pass rate (not 100%)
- Document time spent for future planning

**Trigger**: If testing takes >9 hours to complete

---

**Risk #5: Phase 3 API Never Becomes Available**

**Likelihood**: MEDIUM (40-50%)
**Impact**: HIGH (no E2E automation ever)
**Mitigation**:
- Accept manual testing as permanent solution
- Focus on maximizing structural testing value
- Consider workarounds (Claude API directly, reverse engineering)
- Build test project generator to speed manual testing

**Trigger**: If Claude Code doesn't provide API by Q2 2025

---

## Success Metrics

### Immediate Success (This Week)

- [ ] P0-6 executed: All 3 plugins manually tested in Claude Code
- [ ] Results documented: TESTING_RESULTS.md populated with outcomes
- [ ] Issues filed: All bugs discovered documented with severity
- [ ] 14 structural issues fixed: Phase 2 pass rate increases to 95%+
- [ ] promptctl resolved: Status clearly documented in CLAUDE.md

**Success Threshold**: 80%+ pass rate for manual tests, <5 High severity bugs found

---

### Near-Term Success (Next 2 Weeks)

- [ ] Critical bugs fixed: All Critical severity issues resolved
- [ ] High bugs fixed: All High severity issues resolved or documented with workarounds
- [ ] Retesting complete: Updated TESTING_RESULTS.md shows improvements
- [ ] Phase 2 polished: 95%+ pass rate for structural validation
- [ ] Documentation accurate: CLAUDE.md reflects real testing status (not "100% MVP")

**Success Threshold**: Production readiness can be claimed with confidence

---

### Long-Term Success (Next 1-3 Months)

- [ ] Phase 3 design complete: E2E harness architecture documented
- [ ] Test project generator implemented: Speeds up manual testing
- [ ] API requirements submitted: Feature request to Anthropic
- [ ] Ready for E2E automation: When API becomes available, rapid implementation possible

**Success Threshold**: Foundation for automated testing is solid

---

## Execution Order and Timeline

### Week 1 (November 6-13, 2025)

**Monday-Tuesday**: STRUCT-FIX-01 + P0-7
- Fix 14 structural issues (2-3 hours)
- Resolve promptctl status (1-2 hours)
- Run structural validation tests to verify fixes

**Wednesday-Friday**: P0-6-EXEC
- Test agent-loop plugin (2-3 hours)
- Test epti plugin (2-3 hours)
- Test visual-iteration plugin (2-3 hours)
- Consolidate results and file issues (1 hour)

**Deliverable**: Manual testing complete, structural issues resolved

---

### Week 2-3 (November 13-27, 2025)

**Week 2**: ITERATE-P0-6
- Fix Critical severity issues (2-3 days)
- Fix High severity issues (2-3 days)
- Retest affected workflows (1 day)

**Week 3**: PHASE2-POLISH
- Complete command template validation improvements (2 days)
- Enhance agent workflow validation (2 days)
- Reduce false negatives (1 day)
- Add hook unit tests (2 days, if time allows)

**Deliverable**: Production readiness achieved, enhanced structural validation at 95%+

---

### Month 2-3 (December 2025 - January 2026)

**Weeks 4-5**: Phase 3 Design (P2-1, P2-2, P2-4)
- Design E2E harness architecture (1 week)
- Design conversation simulation framework (1 week)
- Document API requirements (3 days)

**Week 6**: Test Project Generator (P2-3)
- Implement generator tool (3 days)
- Create project templates (2 days)

**Deliverable**: Phase 3 design complete, test generator implemented

---

## File Management and Cleanup

### Retire Completed Plan

**Action**: Archive PLAN-testing-framework-2025-11-06-021441.md
- [ ] This plan is 100% complete (P0-1 through P1-7 done)
- [ ] Move to archive/PLAN-testing-framework-2025-11-06-021441.md.archived
- [ ] Document why: "Phase 1 and Phase 2 implementation complete, superseded by next-steps plan"

### Check for Old Planning Files

```bash
ls -t /Users/bmf/icode/loom99-claude-marketplace/.agent_planning/PLAN-*.md
ls -t /Users/bmf/icode/loom99-claude-marketplace/.agent_planning/SPRINT-*.md
```

**Current PLAN files** (as of 2025-11-06):
1. PLAN-testing-framework-next-steps-2025-11-06-032004.md (THIS FILE - NEW)
2. PLAN-testing-framework-2025-11-06-021441.md (COMPLETE - retiring)
3. PLAN-verbosity-reduction-2025-10-29-075000.md (OLD - different initiative)

**Action**: Keep exactly 4 PLAN-*.md files. Currently have 3, so no deletion needed.

**Current SPRINT files**: None for testing-framework initiative

**Archive Conflicts**: No conflicting planning files detected (no undated PLAN.md or BACKLOG.md)

---

## Alignment Verification

### Alignment with STATUS-testing-framework-2025-11-06-031516.md

- ✅ Acknowledges Phase 1 is 100% complete (P0-1 to P0-5)
- ✅ Acknowledges Phase 2 is 80% complete with 14 real issues found
- ✅ Acknowledges Phase 3 is 0% complete (expected)
- ✅ Prioritizes P0-6 execution as THE critical blocker
- ✅ Includes work items to fix 14 structural issues
- ✅ Includes promptctl resolution (P0-7)
- ✅ Recognizes manual testing framework is ready to use
- ✅ Accepts E2E automation is blocked on Claude Code API

**Alignment Score**: 100% - This plan directly addresses STATUS findings

---

### Alignment with CLAUDE.md Specification

- ✅ Follows test-first development principles
- ✅ Evaluates testing framework quality before claiming success
- ✅ Plans manual testing before automated testing
- ✅ Addresses production readiness honestly (not claiming "100% MVP" prematurely)
- ✅ Creates actionable work items with realistic effort estimates
- ✅ Includes risk assessment and mitigation
- ✅ Maintains architectural alignment (manual → structural → E2E)

**Alignment Score**: 100% - This plan follows specification principles

---

## Critical Path to Production Readiness

These items MUST be completed before claiming "Production Ready":

1. ✅ **P0-6-EXEC**: Execute manual testing for all plugins (CRITICAL - 6-9 hours)
2. ✅ **STRUCT-FIX-01**: Fix 14 structural issues (HIGH - 2-3 hours)
3. ✅ **ITERATE-P0-6**: Fix Critical and High severity bugs from manual testing (HIGH - 1-2 weeks)
4. ✅ **Update CLAUDE.md**: Reflect accurate testing status, not "100% MVP" (HIGH - 30 minutes)

**Critical Path Duration**: 2-3 weeks total

**Blocker**: P0-6 execution is the ONLY blocker right now. Everything else depends on its completion.

---

## Conclusion

This plan provides a focused, actionable roadmap for completing the testing framework implementation and achieving production readiness. It builds on the significant progress made in Phase 1 and Phase 2 while prioritizing the critical work that remains.

**Key Principles**:

1. **Execution Over Planning** - Phase 1 framework exists; now we execute (P0-6)
2. **Fix What's Broken** - 14 structural issues found; now we fix them
3. **Be Honest About Status** - Don't claim "production ready" until validated
4. **Prepare for Future** - Design Phase 3 for when API becomes available

**Immediate Action**: Begin P0-6-EXEC manual testing execution. This is THE blocker. Everything else is secondary.

**Timeline**: 2-3 weeks to production readiness (1 week manual testing + fixes, 1-2 weeks iteration)

**Next Status File**: STATUS-testing-framework-[timestamp].md after P0-6 execution completes

---

**Plan Complete**
**Ready for Execution**: YES - All work items are actionable with clear acceptance criteria
