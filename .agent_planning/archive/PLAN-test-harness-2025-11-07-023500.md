# Test Harness Implementation Plan: Honest Roadmap with API Blocker

**Generated**: 2025-11-07 02:35:00
**Source STATUS**: STATUS-test-harness-feasibility-2025-11-07-022042.md
**Specification**: CLAUDE.md (last modified 2025-11-07)
**Context**: User request to design/build Docker-based test harness for automated Claude Code testing

---

## Provenance

**Input Documents**:
- STATUS-test-harness-feasibility-2025-11-07-022042.md (comprehensive feasibility assessment)
- PLAN-path-a-revised-2025-11-07-014830.md (Path A execution plan)
- CLAUDE.md (project specification)
- Test results: 282/304 tests passing (89.2%), 22 failing

**Key Findings from Feasibility Assessment**:
- **CRITICAL BLOCKER**: Claude Code has no programmatic API (100% certain)
- **What's Possible Now**: Design work, architecture, MCP skeleton, test fixtures (15-22 hours)
- **What's Blocked**: All functional automation until API available (40-60 hours)
- **Current Gap**: 7 test failures in E2E design documentation validation
- **Risk**: 50% probability MCP integration (visual-iteration) is broken

---

## Executive Summary

### The Brutal Truth

**Test harness is TECHNICALLY FEASIBLE but CURRENTLY BLOCKED on Claude Code API.**

**Timeline**:
- **Phase 1 (NOW)**: 15-22 hours over 2 weeks - Design, architecture, preparation
- **Phase 2 (FUTURE)**: 40-60 hours when API available - Functional implementation

**Success Probability**:
- **Phase 1**: 95% (design work, no external blockers)
- **Phase 2**: UNKNOWN (depends on API availability timeline)

**Critical Decision**: Should we invest 15-22 hours in Phase 1 design work, or return to Path A manual testing?

### What This Plan Delivers

**Phase 1 Deliverables** (CAN DO NOW):
1. ✅ E2E test harness architecture documentation → Fixes 7 test failures
2. ✅ Conversation simulation framework design → Prepares for automation
3. ✅ Claude Code API requirements document → Provides requirements to Anthropic
4. ✅ Test project generator implementation → Improves manual testing
5. ✅ MCP server skeleton with 13 working tools, 20 stubs → Ready for API
6. ✅ Docker feasibility research → Answers critical unknowns

**Phase 2 Deliverables** (BLOCKED UNTIL API):
1. ⏳ 20 API-dependent MCP tools implemented
2. ⏳ Docker infrastructure for test orchestration
3. ⏳ Pytest integration for E2E test suite
4. ⏳ Automated plugin installation testing
5. ⏳ Automated command execution testing
6. ⏳ Automated conversation simulation
7. ⏳ CI/CD integration

**Value Proposition**:
- **For v1.0.0**: Phase 1 fixes 7 test failures, documents future automation
- **For v1.1.0+**: Phase 2 enables automated regression testing, fast feedback loop
- **For Anthropic**: Provides clear API requirements that may accelerate development

---

## PHASE 1: Design & Preparation (NOW - 15-22 hours)

**Duration**: 2 weeks (parallel with Path A Phase 1)
**Effort**: 15-22 hours
**Risk**: LOW (no external dependencies)
**Goal**: Complete E2E design documentation, prepare infrastructure for future implementation

### Phase 1 Overview

**Why This Phase Matters**:
- Fixes 7 test failures (E2E design validation tests)
- Documents architecture BEFORE API available
- Creates reusable test fixtures for manual testing
- Provides clear requirements to Anthropic
- Prepares infrastructure so Phase 2 can start immediately when API available

**Success Metrics**:
- 7 test failures fixed (E2E design validation)
- 4 design documents complete (ARCHITECTURE, CONVERSATION_SIMULATION, API_REQUIREMENTS, DOCKER_SETUP)
- Test project generator working
- MCP server skeleton with 13 implemented tools
- Docker research findings documented

### Phase 1 Work Items (Priority Ordered)

---

## [P0] E2E Test Harness Architecture Documentation

**Status**: Not Started
**Effort**: Medium (4 hours)
**Dependencies**: None
**Spec Reference**: CLAUDE.md "Testing Plugins" section • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 2: CURRENT TESTING INFRASTRUCTURE"

### Description

Create comprehensive architecture documentation for the E2E test harness. This document serves as the blueprint for Phase 2 implementation and fixes the test failure for missing `tests/e2e/design/ARCHITECTURE.md`.

**Evidence from STATUS**:
- Current test gap: "E2E Test Harness DOES NOT EXIST" (line 83)
- 7 failing tests due to missing E2E design documentation (line 849)
- STATUS explicitly states: "Document E2E test harness architecture (4 hours, fixes 7 test failures)" (line 976)

### Acceptance Criteria

- [ ] Create `tests/e2e/design/ARCHITECTURE.md` (800-1,200 lines)
- [ ] Document test harness components (MCP server, Docker, pytest integration)
- [ ] Include component diagram (text-based architecture)
- [ ] Document MCP server design with tool inventory (33 tools identified)
- [ ] Document Docker orchestration strategy
- [ ] Document pytest integration approach
- [ ] Document test isolation strategy
- [ ] Document assertion framework design
- [ ] List all stubbed tools (20 API-dependent, 13 implementable now)
- [ ] Test failure `test_e2e_architecture_exists` passes

### Technical Notes

**Architecture Components**:
1. **FastMCP Test Harness Server** (proven viable via promptctl example)
   - Tool categories: Plugin management, Command execution, Conversation simulation, Agent state, Hook verification, Test environment, Assertion helpers, MCP integration
   - 33 total tools: 20 blocked on API, 13 implementable now

2. **Docker Orchestration** (research needed)
   - Claude Code container (feasibility unknown)
   - Test harness MCP container (Python 3.11 + FastMCP)
   - Volume mounts for plugins, test projects, session state

3. **Pytest Integration**
   - Fixtures for Claude harness, session management, cleanup
   - Parameterized tests for multiple plugins
   - Assertion helpers for semantic matching

4. **Test Isolation**
   - Container-per-test or container-per-suite
   - Volume cleanup between tests
   - Session ID generation

**Reference Existing Work**:
- Promptctl MCP server as example (`plugins/promptctl/mcp/server.py`)
- Manual testing framework structure (`tests/manual/`)

---

## [P0] Conversation Simulation Framework Design

**Status**: Not Started
**Effort**: Small (2 hours)
**Dependencies**: None
**Spec Reference**: CLAUDE.md "Testing agent behaviors" • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 2: Challenge 4 - Conversation Simulation"

### Description

Design the conversation state machine and multi-turn interaction patterns for simulating Claude Code conversations. This is critical for testing agent workflows like agent-loop's 4-stage cycle or epti's 6-stage TDD workflow.

**Evidence from STATUS**:
- Current gap: "No conversation simulation framework" (line 87)
- Challenge identified: "Need to simulate realistic user ↔ Claude interactions" (line 250)
- STATUS explicitly states: "Create tests/e2e/design/CONVERSATION_SIMULATION.md (2 hours)" (line 1025)

### Acceptance Criteria

- [ ] Create `tests/e2e/design/CONVERSATION_SIMULATION.md` (500-800 lines)
- [ ] Document conversation state machine (states, transitions)
- [ ] Define multi-turn interaction patterns
- [ ] Document workflow stage tracking approach
- [ ] Document agent mode transitions (e.g., explore → plan → code → commit)
- [ ] Include 3-5 example test scenarios with full conversation flows
- [ ] Document assertion strategies for generative responses
- [ ] Document how to verify agent guidance without string matching
- [ ] Test failure `test_e2e_conversation_simulation_exists` passes

### Technical Notes

**Conversation State Machine**:
- States: Idle, UserPrompt, AgentThinking, AgentResponding, CommandExecuting, WorkflowTransition
- Transitions: User input → Agent response → Workflow stage change
- State persistence: How to track across turns

**Multi-Turn Patterns**:
- agent-loop: 4 stages (explore → plan → code → commit)
- epti: 6 stages (write-tests → verify-fail → commit-tests → implement → iterate → commit-code)
- visual-iteration: iterative cycles (screenshot → feedback → refine → commit)

**Assertion Strategies**:
- Semantic matching (not exact string comparison)
- Keyword presence checks
- Workflow transition verification
- Negative testing (verify agent blocks incorrect actions)

**Example Scenario Format**:
```
Scenario: agent-loop explore command
1. User: "/explore"
2. Agent: <contains "systematic investigation" + "code-exploration skill">
3. User: "explore the database layer"
4. Agent: <contains database-related findings + "plan next">
5. Verify: workflow stage = "exploration complete"
```

---

## [P0] Claude Code API Requirements Documentation

**Status**: Not Started
**Effort**: Small (2 hours)
**Dependencies**: None
**Spec Reference**: N/A (external requirement) • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 4: CURRENT BLOCKERS"

### Description

Document all required Claude Code API capabilities needed for E2E test automation. This serves two purposes: (1) fixes test failure, (2) provides clear requirements to Anthropic that may accelerate API development.

**Evidence from STATUS**:
- CRITICAL DEPENDENCY: "Claude Code Programmatic API MISSING" (line 540)
- STATUS explicitly states: "Create tests/e2e/design/API_REQUIREMENTS.md (2 hours)" (line 1032)
- Required capabilities listed: Plugin installation, command execution, conversation management, state access (lines 543-549)

### Acceptance Criteria

- [ ] Create `tests/e2e/design/API_REQUIREMENTS.md` (600-1,000 lines)
- [ ] Document required plugin management APIs (install, uninstall, list, status)
- [ ] Document required command execution APIs (execute, get output, list commands)
- [ ] Document required conversation APIs (send prompt, get response, history, session)
- [ ] Document required state inspection APIs (agent mode, workflow stage, transcript)
- [ ] Document required hook APIs (list hooks, trigger hook, get execution log)
- [ ] Document alternative approaches if API unavailable
- [ ] Include use cases for each API capability
- [ ] Include priority levels (Critical, High, Medium, Low)
- [ ] Test failure `test_e2e_api_requirements_exists` passes

### Technical Notes

**API Categories** (from STATUS lines 469-532):

1. **Plugin Management Tools** (CRITICAL)
   - `install_plugin(plugin_name, marketplace_path)` → bool
   - `uninstall_plugin(plugin_name)` → bool
   - `list_plugins()` → list[Plugin]
   - `get_plugin_status(plugin_name)` → PluginStatus

2. **Command Execution Tools** (CRITICAL)
   - `execute_command(command: str, args: dict, session_id: str)` → CommandResult
   - `get_command_output(command_id: str)` → str
   - `list_available_commands()` → list[Command]
   - `verify_command_expansion(command: str)` → bool

3. **Conversation Simulation Tools** (CRITICAL)
   - `send_prompt(prompt: str, session_id: str)` → str (response_id)
   - `get_response(response_id: str)` → ConversationTurn
   - `get_conversation_history(session_id: str)` → list[ConversationTurn]
   - `start_conversation(config: dict)` → str (session_id)
   - `end_conversation(session_id: str)` → bool

4. **Agent State Tools** (CRITICAL)
   - `get_agent_mode(session_id: str)` → str
   - `get_agent_guidance(session_id: str)` → AgentGuidance
   - `get_workflow_stage(session_id: str)` → str
   - `verify_agent_transition(session_id: str, expected_stage: str)` → bool

5. **Hook Verification Tools** (CRITICAL)
   - `list_active_hooks()` → list[Hook]
   - `trigger_hook(hook_name: str, payload: dict)` → HookResult
   - `get_hook_execution_log(hook_name: str)` → list[HookExecution]
   - `verify_hook_blocked_action(action_id: str)` → bool

**Alternative Approaches** (if API never provided):
- Filesystem scraping (read session files, if format is documented)
- Log parsing (if Claude Code logs conversation state)
- Manual testing only (fallback, not ideal)

---

## [P0] Test Project Generator Implementation

**Status**: Not Started
**Effort**: Small-Medium (3-4 hours)
**Dependencies**: None
**Spec Reference**: CLAUDE.md "Testing Plugins" section • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 4: Missing Dependency - Test Project Generator"

### Description

Implement a CLI tool to generate realistic test project fixtures. This is NOT blocked on API and provides immediate value for manual testing. Generates projects in multiple languages (Python, JavaScript, Go) with realistic file structures.

**Evidence from STATUS**:
- Current gap: "tools/generate_test_project.py doesn't exist" (line 579)
- STATUS explicitly states: "Implement tools/generate_test_project.py (3 hours, can do NOW)" (line 979)
- Required features listed: Multiple language support, project types, realistic structures (lines 580-587)

### Acceptance Criteria

- [ ] Create `tools/generate_test_project.py` with CLI interface
- [ ] Support Python projects (pytest, pyproject.toml, src/, tests/)
- [ ] Support JavaScript projects (jest, package.json, src/, __tests__/)
- [ ] Support Go projects (go test, go.mod, cmd/, pkg/, internal/)
- [ ] Support multiple project types (web app, CLI tool, library)
- [ ] Generate realistic file structures (not empty placeholder files)
- [ ] Initialize git repository by default
- [ ] Create sample code files with basic implementations
- [ ] Include README.md with project description
- [ ] CLI accepts: `--type [web-app|cli|library]` and `--language [python|javascript|go]`
- [ ] Test failure `test_generate_test_project_exists` passes

### Technical Notes

**CLI Interface**:
```bash
# Generate Python web app
python tools/generate_test_project.py \
  --output /tmp/test-project-1 \
  --type web-app \
  --language python \
  --name "Task Manager API"

# Generate JavaScript CLI tool
python tools/generate_test_project.py \
  --output /tmp/test-project-2 \
  --type cli \
  --language javascript \
  --name "Deploy Script"
```

**Generated Structure (Python web app example)**:
```
test-project-1/
├── .git/
├── .gitignore
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── api.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_api.py
└── .venv/
```

**Realistic Content**:
- Not just empty files - include basic class definitions, simple functions
- Tests should be runnable (even if they just pass trivially)
- README should describe the fictional project
- Configuration files should be valid (pyproject.toml, package.json, go.mod)

**Use Cases**:
1. Manual testing: Create project, test agent-loop workflow on it
2. Future E2E testing: Generate projects on-demand for tests
3. Documentation: Example projects for plugin README files

---

## [P1] MCP Server Skeleton Implementation

**Status**: Not Started
**Effort**: Medium (4-6 hours)
**Dependencies**: E2E architecture documentation complete
**Spec Reference**: CLAUDE.md "MCP Integration" section • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 3: MCP INTEGRATION ANALYSIS"

### Description

Build the FastMCP-based test harness MCP server skeleton with all 33 tools defined. Implement 13 tools that don't require API (test environment, assertions, MCP integration). Stub 20 API-dependent tools with documentation.

**Evidence from STATUS**:
- Current gap: "tests/e2e/mcp_server/ doesn't exist" (line 675)
- STATUS explicitly states: "Build MCP server skeleton (4 hours, can do NOW)" (line 1062)
- Tool inventory: 33 total tools, 13 implementable now, 20 blocked (lines 527-532)

### Acceptance Criteria

- [ ] Create `tests/e2e/mcp_server/harness_server.py` with FastMCP setup
- [ ] Create `tests/e2e/mcp_server/pyproject.toml` with FastMCP 2.0.0+ dependency
- [ ] Implement Category 6 tools: Test environment (5 tools) - FULLY WORKING
- [ ] Implement Category 7 tools: Assertion helpers (4 tools) - FULLY WORKING
- [ ] Implement Category 8 tools: MCP integration (4 tools) - FULLY WORKING
- [ ] Stub Category 1-5 tools with docstrings explaining API blocker (20 tools)
- [ ] Add error handling for stubbed tools (raise NotImplementedError with message)
- [ ] Include usage examples in docstrings
- [ ] Server can start and list all tools
- [ ] MCP server passes `fastmcp dev` validation

### Technical Notes

**FastMCP Server Structure**:
```python
# tests/e2e/mcp_server/harness_server.py
from fastmcp import FastMCP

mcp = FastMCP("Claude Code Test Harness")

# Category 6: Test Environment Tools (IMPLEMENT NOW)
@mcp.tool()
def create_test_project(project_type: str, language: str) -> dict:
    """Generate test fixture project using tools/generate_test_project.py"""
    # FULLY IMPLEMENTED
    pass

@mcp.tool()
def setup_git_repo(project_path: str) -> dict:
    """Initialize git repository for testing"""
    # FULLY IMPLEMENTED
    pass

@mcp.tool()
def create_sample_files(project_path: str, file_specs: list) -> dict:
    """Populate test project with sample files"""
    # FULLY IMPLEMENTED
    pass

@mcp.tool()
def reset_test_environment() -> dict:
    """Clean up test environment between tests"""
    # FULLY IMPLEMENTED
    pass

@mcp.tool()
def capture_test_artifacts(test_name: str) -> dict:
    """Save logs, screenshots, state for test result analysis"""
    # FULLY IMPLEMENTED
    pass

# Category 7: Assertion Helper Tools (IMPLEMENT NOW)
@mcp.tool()
def assert_contains_keywords(text: str, keywords: list) -> dict:
    """Semantic matching for agent responses"""
    # FULLY IMPLEMENTED
    pass

@mcp.tool()
def assert_workflow_transition(from_stage: str, to_stage: str, actual: str) -> dict:
    """Verify workflow state transitions"""
    # FULLY IMPLEMENTED
    pass

@mcp.tool()
def assert_command_suggested(response: str, command_name: str) -> dict:
    """Verify agent suggests correct command"""
    # FULLY IMPLEMENTED
    pass

@mcp.tool()
def assert_error_handled_gracefully(response: str, error_type: str) -> dict:
    """Verify agent handles errors appropriately"""
    # FULLY IMPLEMENTED
    pass

# Category 8: MCP Integration Tools (IMPLEMENT NOW)
@mcp.tool()
def start_mcp_server(server_config: dict) -> dict:
    """Spin up MCP server (e.g., browser-tools) for test"""
    # FULLY IMPLEMENTED (Docker orchestration)
    pass

@mcp.tool()
def stop_mcp_server(server_id: str) -> dict:
    """Clean up MCP server after test"""
    # FULLY IMPLEMENTED
    pass

@mcp.tool()
def verify_mcp_communication(server_id: str) -> dict:
    """Test MCP connection"""
    # FULLY IMPLEMENTED
    pass

@mcp.tool()
def mock_mcp_tool_response(tool_name: str, mock_response: dict) -> dict:
    """Stub MCP tool for unit testing"""
    # FULLY IMPLEMENTED
    pass

# Category 1-5: API-Dependent Tools (STUB FOR NOW)
@mcp.tool()
def install_plugin(plugin_name: str) -> dict:
    """
    Install plugin in Claude Code test instance.

    BLOCKED: Requires Claude Code programmatic API.

    Required API:
    - Claude.Plugins.install(plugin_name, marketplace_path) -> PluginStatus

    When API available, implement:
    1. Call Claude Code API to install plugin
    2. Wait for installation to complete
    3. Verify plugin loaded correctly
    4. Return installation result
    """
    raise NotImplementedError(
        "install_plugin blocked on Claude Code API. "
        "See tests/e2e/design/API_REQUIREMENTS.md for details."
    )

# ... 19 more stubbed tools with similar documentation
```

**Dependencies in pyproject.toml**:
```toml
[project]
name = "claude-code-test-harness"
version = "0.1.0"
dependencies = [
    "fastmcp>=2.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
]
```

**Validation**:
- Run `fastmcp dev tests/e2e/mcp_server/harness_server.py` to test server
- Verify all 33 tools are listed
- Verify 13 tools execute successfully
- Verify 20 tools raise NotImplementedError with helpful message

---

## [P1] Docker Feasibility Research

**Status**: Not Started
**Effort**: Small-Medium (2-4 hours)
**Dependencies**: None
**Spec Reference**: N/A (research task) • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 2: Can Claude Code Run in Docker?"

### Description

Research whether Claude Code can run in Docker containers. Attempt to containerize Claude Code locally, document results (works / partially works / doesn't work), and identify configuration requirements.

**Evidence from STATUS**:
- Critical unknown: "Can Claude Code run in Docker? NEEDS RESEARCH" (line 136)
- STATUS explicitly states: "Research Docker feasibility (2-4 hours, answers critical unknown)" (line 1054)
- Risk assessment: 30% works out of box, 40% works with config, 30% doesn't work (lines 166-168)

### Acceptance Criteria

- [ ] Create `tests/e2e/design/DOCKER_SETUP.md` (500-800 lines)
- [ ] Attempt to run Claude Code in Docker container locally
- [ ] Document results (success / partial success / failure)
- [ ] Identify required environment variables
- [ ] Identify required volume mounts
- [ ] Identify required configuration files
- [ ] Test basic plugin installation in container (if possible)
- [ ] Test basic command execution in container (if possible)
- [ ] Document all blockers encountered
- [ ] Provide recommendation (viable / needs workarounds / not viable)
- [ ] Test failure `test_e2e_docker_setup_exists` passes

### Technical Notes

**Research Steps**:

1. **Create Base Dockerfile**:
```dockerfile
FROM node:18-slim

# Install Claude Code CLI (research correct installation method)
RUN npm install -g @anthropic/claude-code

# Set up working directory
WORKDIR /workspace

# Copy plugin marketplace
COPY .claude-plugin /workspace/.claude-plugin
COPY plugins /workspace/plugins

# Set environment variables (research correct vars)
ENV CLAUDE_HOME=/workspace
ENV CLAUDE_PLUGIN_PATH=/workspace/plugins

CMD ["claude", "--version"]
```

2. **Test Basic Functionality**:
   - Does `claude --version` work?
   - Can Claude Code start in container?
   - Does it require interactive terminal?
   - Can plugins be loaded?
   - Can commands be executed?

3. **Identify Configuration Needs**:
   - Where does Claude Code store config? (`~/.claude`?)
   - What files need to be mounted?
   - What environment variables are required?
   - Does it need network access?
   - Does it expect specific directory structure?

4. **Document Findings**:
   - **SUCCESS**: Document working Dockerfile, required mounts, config
   - **PARTIAL**: Document what works, what doesn't, workarounds
   - **FAILURE**: Document why it doesn't work, alternatives

**Expected Outcomes**:
- **Best case**: Claude Code runs in Docker with minor configuration
- **Likely case**: Works but requires volume mounts, env vars, workarounds
- **Worst case**: Requires interactive terminal, GUI, or OS-specific features

---

## [P2] E2E Test Projects Directory Setup

**Status**: Not Started
**Effort**: Trivial (15 minutes)
**Dependencies**: None
**Spec Reference**: N/A • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 4: Missing Files"

### Description

Create the `tests/e2e/test_projects/` directory structure for storing generated test project fixtures. Include README explaining purpose and usage.

**Evidence from STATUS**:
- Current gap: "tests/e2e/test_projects/ directory missing" (line 854)
- This is a quick organizational task, no implementation required

### Acceptance Criteria

- [ ] Create `tests/e2e/test_projects/` directory
- [ ] Create `tests/e2e/test_projects/README.md` explaining purpose
- [ ] Create `.gitignore` to exclude generated projects (don't commit fixtures)
- [ ] Document how to generate test projects using `tools/generate_test_project.py`
- [ ] Include example usage in README
- [ ] Test failure `test_e2e_test_projects_dir_exists` passes

### Technical Notes

**Directory Structure**:
```
tests/e2e/test_projects/
├── README.md
├── .gitignore
└── (generated projects go here, not committed to git)
```

**README.md Content**:
- Purpose: Store test project fixtures for E2E testing
- How to generate: `python tools/generate_test_project.py --output tests/e2e/test_projects/my-test`
- How to clean up: `rm -rf tests/e2e/test_projects/*` (except README and .gitignore)
- Example projects: List typical test scenarios (Python web app, JS CLI, Go library)

**.gitignore Content**:
```
# Ignore all generated test projects
*

# Except metadata files
!README.md
!.gitignore
```

---

## [P2] E2E Design Completeness Validation

**Status**: Not Started
**Effort**: Trivial (30 minutes)
**Dependencies**: All P0 and P1 items complete
**Spec Reference**: N/A • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 4: Completion Task 1"

### Description

Final validation step to ensure all E2E design documentation is complete and meets quality standards. Review all design documents for consistency, completeness, and accuracy.

**Evidence from STATUS**:
- Test failure: "Design completeness check fails" (line 856)
- This is a validation task after all design work is done

### Acceptance Criteria

- [ ] All 4 design documents exist (ARCHITECTURE, CONVERSATION_SIMULATION, API_REQUIREMENTS, DOCKER_SETUP)
- [ ] All design documents are 500+ lines (indicates thoroughness)
- [ ] All design documents reference STATUS findings
- [ ] All design documents include examples
- [ ] Cross-references between documents are accurate
- [ ] Test project generator works as documented in ARCHITECTURE
- [ ] MCP server skeleton matches ARCHITECTURE design
- [ ] Docker research findings match ARCHITECTURE assumptions
- [ ] All 7 E2E design validation tests pass
- [ ] Automated test pass rate increases from 89.2% to 91.6% (282/304 → 289/304)

### Technical Notes

**Validation Checklist**:
1. Run automated tests: `uv run pytest tests/functional/test_e2e_harness_design.py`
2. Verify all 7 tests pass
3. Review each design doc for completeness
4. Check for TODO/FIXME comments in design docs
5. Verify examples are realistic and complete
6. Ensure STATUS evidence is cited properly

**Expected Test Results**:
```
tests/functional/test_e2e_harness_design.py::test_e2e_design_dir_exists PASSED
tests/functional/test_e2e_harness_design.py::test_architecture_exists PASSED
tests/functional/test_e2e_harness_design.py::test_conversation_simulation_exists PASSED
tests/functional/test_e2e_harness_design.py::test_api_requirements_exists PASSED
tests/functional/test_e2e_harness_design.py::test_docker_setup_exists PASSED
tests/functional/test_e2e_harness_design.py::test_test_projects_dir_exists PASSED
tests/functional/test_e2e_harness_design.py::test_generate_test_project_exists PASSED
```

---

## Phase 1 Summary

**Total Effort**: 15-22 hours
**Timeline**: 2 weeks (parallel with Path A Phase 1)
**Deliverables**: 7 test failures fixed, complete E2E design documentation, working test fixtures generator, MCP skeleton

**Phase 1 Schedule**:

**Week 1 (Critical Path)** - 11 hours:
- Day 1-2: E2E Architecture Documentation (P0) - 4 hours
- Day 3: Conversation Simulation Design (P0) - 2 hours
- Day 4: API Requirements Documentation (P0) - 2 hours
- Day 5: Test Project Generator Implementation (P0) - 3 hours

**Week 2 (Quality & Research)** - 7-11 hours:
- Day 1-2: MCP Server Skeleton (P1) - 4-6 hours
- Day 3-4: Docker Feasibility Research (P1) - 2-4 hours
- Day 5: E2E Test Projects Setup (P2) - 15 minutes
- Day 5: Design Completeness Validation (P2) - 30 minutes

**Success Criteria**:
- ✅ All 7 E2E design validation tests pass
- ✅ Test pass rate increases from 89.2% to 91.6%
- ✅ Test project generator working and validated
- ✅ MCP server skeleton starts successfully
- ✅ Docker research findings documented
- ✅ Ready for Phase 2 implementation (when API available)

---

## PHASE 2: Functional Implementation (FUTURE - 40-60 hours)

**Duration**: 4-6 weeks (when API available)
**Effort**: 40-60 hours
**Risk**: HIGH (depends on API timeline)
**Goal**: Implement functional E2E test automation

### Phase 2 Overview

**TRIGGER FOR PHASE 2**: Anthropic announces Claude Code programmatic API

**Why This Phase is Blocked**:
- All functional testing requires API that doesn't exist yet
- Cannot implement plugin installation automation without API
- Cannot implement command execution automation without API
- Cannot implement conversation simulation without API
- Cannot implement agent state inspection without API
- Timeline completely unknown (could be months or years)

**Success Metrics**:
- All 20 API-dependent MCP tools implemented
- Docker infrastructure working end-to-end
- Automated E2E test suite passing
- CI/CD integration functional
- Test execution time <5 minutes for full suite

### Phase 2 Work Items (Priority Ordered)

---

## [P0] Implement API-Dependent MCP Tools

**Status**: BLOCKED (waiting for API)
**Effort**: Large (30-40 hours)
**Dependencies**: Claude Code API available, Phase 1 complete
**Spec Reference**: CLAUDE.md "Testing Plugins" • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 3: Category 1-5 Tools"

### Description

Implement the 20 API-dependent MCP tools that are currently stubbed. This is the core functional automation work that enables E2E testing.

**Evidence from STATUS**:
- Status explicitly states: "Implement 20 API-dependent MCP tools (30-40 hours)" (line 1084)
- Tool categories listed: Plugin management (4 tools), Command execution (4 tools), Conversation simulation (5 tools), Agent state (4 tools), Hook verification (4 tools) (lines 469-504)

### Acceptance Criteria

- [ ] Implement 4 Plugin Management tools (install, uninstall, list, status)
- [ ] Implement 4 Command Execution tools (execute, get output, list, verify)
- [ ] Implement 5 Conversation Simulation tools (send, receive, history, session mgmt)
- [ ] Implement 4 Agent State tools (mode, guidance, stage, transition)
- [ ] Implement 4 Hook Verification tools (list, trigger, log, verify)
- [ ] All tools have comprehensive error handling
- [ ] All tools have usage examples in docstrings
- [ ] All tools tested individually
- [ ] MCP server passes full validation

### Technical Notes

**This work CANNOT start until**:
1. Anthropic provides Claude Code API
2. API documentation is available
3. API authentication/access is configured
4. API capabilities match requirements (from API_REQUIREMENTS.md)

**Implementation per Tool** (average 1.5-2 hours each):
- Read API documentation
- Design integration approach
- Implement tool function
- Add error handling
- Write usage example
- Test with real Claude Code instance
- Document any API limitations

**Risk**: API may not provide all required capabilities. May need workarounds or compromises.

---

## [P0] Build Docker Infrastructure

**Status**: BLOCKED (waiting for Phase 1 Docker research)
**Effort**: Medium (6-10 hours)
**Dependencies**: Docker research complete, Claude Code containerization viable
**Spec Reference**: CLAUDE.md "Testing Plugins" • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 4: Completion Task 4"

### Description

Build the complete Docker infrastructure for test orchestration: Dockerfile for Claude Code, Dockerfile for test harness MCP server, docker-compose for multi-container orchestration.

**Evidence from STATUS**:
- Status explicitly states: "Build Docker infrastructure (6-10 hours)" (line 1091)
- Required files listed: Dockerfile.claude-code, Dockerfile.test-harness, docker-compose.yml (lines 690-695)

### Acceptance Criteria

- [ ] Create `tests/e2e/docker/Dockerfile.claude-code`
- [ ] Create `tests/e2e/docker/Dockerfile.test-harness`
- [ ] Create `tests/e2e/docker/docker-compose.yml`
- [ ] Create `tests/e2e/docker/docker-compose.test.yml` (test-specific)
- [ ] Volume mounts configured (plugins, test projects, session state)
- [ ] Network configuration for inter-container communication
- [ ] Environment variables passed correctly
- [ ] Test isolation working (container per test or per suite)
- [ ] Cleanup scripts for stopping/removing containers
- [ ] Full test suite runs in Docker successfully

### Technical Notes

**This work CANNOT start until**:
1. Docker research (Phase 1) confirms Claude Code works in containers
2. Required environment variables identified
3. Required volume mounts identified
4. Configuration file formats documented

**Docker Compose Structure**:
```yaml
# tests/e2e/docker/docker-compose.yml
services:
  claude-code:
    build:
      context: ../../..
      dockerfile: tests/e2e/docker/Dockerfile.claude-code
    volumes:
      - ../../../plugins:/workspace/plugins
      - ../test_projects:/workspace/test-projects
      - claude-session:/tmp/claude-sessions
    environment:
      - CLAUDE_HOME=/workspace
      - CLAUDE_PLUGIN_PATH=/workspace/plugins
    networks:
      - test-network

  test-harness:
    build:
      context: ../../..
      dockerfile: tests/e2e/docker/Dockerfile.test-harness
    depends_on:
      - claude-code
    volumes:
      - ../mcp_server:/harness
      - ../test_projects:/test-projects
    networks:
      - test-network

volumes:
  claude-session:

networks:
  test-network:
```

---

## [P0] Integrate with Pytest

**Status**: BLOCKED (waiting for API and Docker)
**Effort**: Small-Medium (4-6 hours)
**Dependencies**: API tools implemented, Docker infrastructure working
**Spec Reference**: CLAUDE.md "Testing Plugins" • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Section 2: Integration with Pytest"

### Description

Integrate the MCP test harness with pytest. Create fixtures for Claude Code harness, session management, cleanup. Enable parameterized tests for multiple plugins.

**Evidence from STATUS**:
- Status explicitly states: "Integrate with pytest (4-6 hours)" (line 1098)
- Example integration shown in STATUS lines 405-429

### Acceptance Criteria

- [ ] Create pytest fixtures in `tests/e2e/conftest.py`
- [ ] Fixture: `claude_harness` - provides MCP connection
- [ ] Fixture: `test_session` - manages conversation session
- [ ] Fixture: `test_project` - generates and cleans up test project
- [ ] Fixture: `plugin_installed` - handles plugin install/uninstall
- [ ] Parameterized tests work (test same scenario across multiple plugins)
- [ ] Cleanup fixtures properly tear down environment
- [ ] Assertion helpers integrated
- [ ] Test isolation verified (tests don't interfere with each other)

### Technical Notes

**Fixture Example**:
```python
# tests/e2e/conftest.py
import pytest
from tests.e2e.harness import ClaudeTestHarness

@pytest.fixture
def claude_harness():
    """Fixture that provides test harness with MCP connection"""
    harness = ClaudeTestHarness()
    harness.start()  # Spins up Docker, connects to MCP
    yield harness
    harness.cleanup()  # Tears down environment

@pytest.fixture
def test_session(claude_harness):
    """Fixture that manages conversation session"""
    session_id = claude_harness.start_conversation()
    yield session_id
    claude_harness.end_conversation(session_id)

@pytest.fixture
def plugin_installed(claude_harness):
    """Fixture that installs/uninstalls plugin"""
    def _install(plugin_name):
        result = claude_harness.install_plugin(plugin_name)
        assert result["success"], f"Failed to install {plugin_name}"
        return plugin_name

    installed = []
    yield _install

    for plugin in installed:
        claude_harness.uninstall_plugin(plugin)
```

---

## [P0] Write E2E Test Suite

**Status**: BLOCKED (waiting for pytest integration)
**Effort**: Medium-Large (10-15 hours)
**Dependencies**: Pytest integration complete, all infrastructure working
**Spec Reference**: CLAUDE.md "Testing Plugins" • **Status Reference**: STATUS-test-harness-feasibility-2025-11-07-022042.md "Phase 2: Implementation"

### Description

Write comprehensive E2E test suite covering plugin installation, command execution, conversation flows, agent behaviors, workflow completion, and integration testing.

**Evidence from STATUS**:
- Status explicitly states: "Write E2E test suite (10-15 hours)" (line 1107)
- Test categories: Installation, commands, conversations, agents, workflows, integration (lines 1106-1112)

### Acceptance Criteria

- [ ] Test suite covers all 3 production plugins (agent-loop, epti, visual-iteration)
- [ ] Installation tests (3 tests, one per plugin)
- [ ] Command execution tests (16 tests, all commands across plugins)
- [ ] Conversation flow tests (9 tests, multi-turn scenarios)
- [ ] Agent behavior tests (9 tests, verify guidance quality)
- [ ] Workflow completion tests (6 tests, end-to-end workflows)
- [ ] Integration tests (3 tests, plugins working together)
- [ ] All tests have clear assertions
- [ ] All tests are reproducible
- [ ] Test execution time <5 minutes for full suite

### Technical Notes

**Test Examples**:

```python
# tests/e2e/test_plugin_installation.py
def test_agent_loop_installation(claude_harness):
    """Test agent-loop plugin installs correctly"""
    result = claude_harness.install_plugin("agent-loop")
    assert result["success"]
    assert "agent-loop" in claude_harness.list_plugins()
    assert claude_harness.get_plugin_status("agent-loop") == "loaded"

# tests/e2e/test_command_execution.py
def test_explore_command(claude_harness, test_session, plugin_installed):
    """Test /explore command expands correctly"""
    plugin_installed("agent-loop")

    response = claude_harness.execute_command("/explore", session_id=test_session)

    assert_contains_keywords(
        response["content"],
        ["systematic investigation", "code-exploration", "project understanding"]
    )

# tests/e2e/test_workflows.py
def test_agent_loop_full_cycle(claude_harness, test_session, test_project, plugin_installed):
    """Test complete agent-loop 4-stage workflow"""
    plugin_installed("agent-loop")
    project = test_project(type="web-app", language="python")

    # Stage 1: Explore
    explore_response = claude_harness.execute_command("/explore", session_id=test_session)
    assert_workflow_transition("idle", "exploring", explore_response["workflow_stage"])

    # Stage 2: Plan
    plan_response = claude_harness.execute_command("/plan", session_id=test_session)
    assert_workflow_transition("exploring", "planning", plan_response["workflow_stage"])

    # Stage 3: Code
    code_response = claude_harness.execute_command("/code", session_id=test_session)
    assert_workflow_transition("planning", "coding", code_response["workflow_stage"])

    # Stage 4: Commit
    commit_response = claude_harness.execute_command("/commit", session_id=test_session)
    assert_workflow_transition("coding", "complete", commit_response["workflow_stage"])
```

**Test Organization**:
- `tests/e2e/test_plugin_installation.py` - Installation tests
- `tests/e2e/test_command_execution.py` - Command tests
- `tests/e2e/test_conversation_flows.py` - Multi-turn interaction tests
- `tests/e2e/test_agent_behaviors.py` - Agent guidance verification
- `tests/e2e/test_workflows.py` - End-to-end workflow tests
- `tests/e2e/test_integration.py` - Cross-plugin integration tests

---

## Phase 2 Summary

**Total Effort**: 40-60 hours
**Timeline**: 4-6 weeks (when API available)
**Deliverables**: Fully functional E2E test automation, CI/CD integration

**Phase 2 Schedule** (FUTURE):

**Week 1-2: API Integration** - 30-40 hours:
- Implement 20 API-dependent MCP tools
- Test each tool individually
- Validate against real Claude Code instance

**Week 3-4: Infrastructure** - 10-16 hours:
- Build Docker infrastructure (6-10 hours)
- Integrate with pytest (4-6 hours)

**Week 5-6: Test Suite** - 10-15 hours:
- Write E2E test suite (10-15 hours)
- Run full suite, fix issues
- Document test results

**Success Criteria**:
- ✅ All 20 API-dependent tools implemented and tested
- ✅ Docker infrastructure working end-to-end
- ✅ Pytest integration functional
- ✅ E2E test suite passing (≥90% pass rate)
- ✅ Test execution time <5 minutes
- ✅ CI/CD integration working
- ✅ Automated regression testing enabled

**Outcome**: Automated E2E testing enables rapid iteration for v1.1.0+

---

## DECISION POINTS

### Decision Point 1: After Phase 1 (Week 2)

**Question**: Should we proceed with Phase 2 planning, or return to Path A manual testing?

**Metrics to Assess**:
- Are all 7 E2E design tests passing?
- Is test project generator working?
- Is MCP server skeleton functional?
- Are Docker research findings documented?
- Is Claude Code API timeline known?

**Decision Criteria**:

**✅ Option A: Continue Monitoring for API** if:
- Phase 1 complete successfully (all deliverables done)
- No immediate timeline for Claude Code API
- Path A manual testing is sufficient for v1.0.0
- **Action**: Shelve Phase 2 work, return to Path A manual testing
- **Benefit**: Phase 1 design work complete, ready when API arrives
- **Cost**: 15-22 hours spent, but fixes 7 tests and documents architecture

**✅ Option B: Wait for API News** if:
- Anthropic announces API coming soon (e.g., within 3 months)
- Path A can be deferred
- Automation is critical for project success
- **Action**: Wait for API, then immediately start Phase 2
- **Benefit**: Prepared to implement quickly when API available
- **Cost**: Project timeline extends until API available

**❌ Option C: Abandon Test Harness** if:
- Anthropic confirms no API planned
- Path A manual testing is working well
- Automation not critical for project goals
- **Action**: Archive Phase 1 work, focus entirely on Path A
- **Benefit**: Stop investing time in blocked work
- **Cost**: 15-22 hours spent, but not wasted (documented architecture)

**Recommendation**: **Option A** (Continue monitoring, return to Path A)

**Rationale**:
- Phase 1 fixes 7 test failures (immediate value)
- Documents requirements for Anthropic (potential influence)
- Prepares infrastructure for future (when API available)
- Does not block v1.0.0 completion (Path A proceeds)
- 15-22 hours is reasonable investment for future automation

---

### Decision Point 2: When API Becomes Available

**Question**: Should we immediately start Phase 2, or defer to v1.1.0+?

**Metrics to Assess**:
- Is API documentation comprehensive?
- Does API provide all required capabilities (from API_REQUIREMENTS.md)?
- Is v1.0.0 already shipped?
- Is there appetite for 40-60 hours of implementation work?

**Decision Criteria**:

**✅ Immediately Start Phase 2** if:
- API documentation is comprehensive
- API provides ≥90% of required capabilities
- v1.0.0 not yet shipped (can integrate before release)
- Team has capacity for 40-60 hours work
- **Action**: Start Phase 2 implementation immediately
- **Benefit**: v1.0.0 ships with automated testing

**⚠️ Defer to v1.1.0** if:
- API documentation incomplete
- API provides <90% of required capabilities
- v1.0.0 already shipped
- Team focused on other priorities
- **Action**: Ship v1.0.0 with manual testing, plan Phase 2 for v1.1.0
- **Benefit**: Don't rush automation, v1.0.0 ships on time

**❌ Reassess Viability** if:
- API significantly different from requirements
- API insufficient for testing needs
- Workarounds required for most tools
- **Action**: Redesign test harness approach, or accept manual testing only
- **Benefit**: Avoid investing in unviable automation

---

## RISK MITIGATION

### High-Risk Items and Mitigations

**1. Claude Code API Never Provided (20% probability)**

**Impact**: Phase 2 permanently blocked, 15-22 hours spent on Phase 1 design

**Mitigation Strategy**:
- **Phase 1 has independent value**: Fixes 7 tests, documents architecture
- **Accept manual testing only**: Path A is viable without automation
- **Archive Phase 1 work**: Keep documentation for reference
- **Future alternatives**: If API never comes, explore other approaches (filesystem scraping, log parsing)

**Contingency**:
- If Anthropic confirms no API planned → Archive Phase 2 plan, focus on Path A
- If API never arrives → v1.0.0 ships with manual testing, v1.1.0+ continues with manual testing

---

**2. Claude Code API Insufficient (30% probability)**

**Impact**: API provides <50% of required capabilities, Phase 2 requires significant compromises

**Mitigation Strategy**:
- **Prioritize critical capabilities**: Focus on plugin install, command execution, conversation mgmt
- **Accept limited automation**: Some tools may remain manual
- **Document limitations**: Be honest about what can/cannot be automated
- **Hybrid approach**: Automate what's possible, manual test the rest

**Contingency**:
- If API provides 50-90% capabilities → Implement available tools, document gaps
- If API provides <50% capabilities → Reassess viability, may not be worth effort

---

**3. Docker Doesn't Work (30% probability from research)**

**Impact**: Cannot use Docker for test orchestration, must find alternative

**Mitigation Strategy**:
- **Research identifies issue early** (Phase 1): Know before Phase 2 investment
- **Alternative approaches**: Direct localhost testing, VM-based testing, manual orchestration
- **Redesign if needed**: Update ARCHITECTURE.md with alternative approach
- **Accept limitations**: May need to run tests on developer machines, not CI/CD

**Contingency**:
- If Docker doesn't work → Redesign using localhost testing
- If no orchestration viable → Manual testing remains only option

---

**4. Phase 1 Takes Longer Than Estimated (40% probability)**

**Impact**: 15-22 hours estimate becomes 20-28 hours actual

**Mitigation Strategy**:
- **Built in buffer**: 2-week timeline allows for overruns
- **Parallel with Path A**: Not blocking other work
- **De-prioritize P2 items**: Focus on P0 (test fixes), defer P1/P2 if needed
- **Accept imperfect design docs**: Good enough documentation is better than perfect delay

**Contingency**:
- If exceeds 22 hours → Stop, assess value delivered so far
- If exceeds 28 hours → Cut P2 items, ship with P0/P1 only
- If exceeds 30 hours → Abandon remaining work, return to Path A

---

**5. Phase 2 Blocked Indefinitely (50% probability)**

**Impact**: Phase 1 work doesn't lead to functional automation

**Mitigation Strategy**:
- **Phase 1 is self-contained**: Delivers value regardless of Phase 2
- **Documentation is useful**: Architecture design informs future work
- **Test fixtures help manual testing**: Test project generator improves Path A
- **Honest status**: Document "automation prepared, blocked on API" in CLAUDE.md

**Contingency**:
- If API never arrives → v1.0.0 ships with manual testing evidence
- If API arrives in 2+ years → Revisit Phase 2 for future release
- Phase 1 work is NOT wasted even if Phase 2 never happens

---

## CONTINGENCY PLANS

### If Phase 1 Exceeds Time Budget

**Trigger**: Phase 1 taking >22 hours, still incomplete

**Options**:

**Option A: Cut P2 Items**
- Complete P0 items (test fixes, architecture, API requirements, test generator)
- Skip P1 items (MCP skeleton, Docker research)
- **Deliverables**: 4-5 test failures fixed, core design docs complete
- **Effort Saved**: 6-10 hours
- **Impact**: Less prepared for Phase 2, but core value delivered

**Option B: Accept "Good Enough"**
- Rush remaining items to completion
- Accept shorter documentation (600-800 lines instead of 1,000-1,200)
- Skip extensive examples
- **Deliverables**: All items complete but less polished
- **Effort Saved**: 3-5 hours
- **Impact**: Lower quality documentation, but all test failures fixed

**Option C: Abandon Remaining Work**
- Stop after 22 hours
- Document what's complete, what's incomplete
- Ship with partial design documentation
- **Deliverables**: Whatever is done at 22 hours
- **Effort Saved**: Remaining hours
- **Impact**: Some test failures remain, design incomplete

**Recommendation**: **Option A** (cut P2 items, focus on P0)

---

### If Claude Code API Never Arrives

**Trigger**: Anthropic confirms no API planned, or 2+ years with no news

**Action**:
1. Accept manual testing as permanent solution
2. Archive Phase 1 design work for reference
3. Update CLAUDE.md status: "Manual Testing Framework - Automated Testing Not Viable"
4. Continue with Path A for v1.0.0 and future releases
5. Explore alternative approaches if automation becomes critical

**Honest Status**: "Implementation Complete, Manual Testing Evidence, Automated Testing Not Available"

---

### If Docker Research Shows Not Viable

**Trigger**: Phase 1 Docker research confirms Claude Code cannot run in containers

**Action**:
1. Update DOCKER_SETUP.md with findings and "Not Viable" conclusion
2. Redesign ARCHITECTURE.md with localhost-based testing approach
3. Accept that CI/CD automation may not be possible
4. Document limitation in all design docs
5. Phase 2 proceeds with localhost testing (if API becomes available)

**Alternative Approach**:
- Run tests on developer machines (not CI/CD)
- Use VMs instead of Docker (heavier, slower)
- Manual orchestration instead of docker-compose

---

## DELIVERABLES SUMMARY

### Phase 1 Deliverables (NOW)

**Documentation** (5 files):
- [ ] `tests/e2e/design/ARCHITECTURE.md` (800-1,200 lines)
- [ ] `tests/e2e/design/CONVERSATION_SIMULATION.md` (500-800 lines)
- [ ] `tests/e2e/design/API_REQUIREMENTS.md` (600-1,000 lines)
- [ ] `tests/e2e/design/DOCKER_SETUP.md` (500-800 lines)
- [ ] `tests/e2e/test_projects/README.md` (200-300 lines)

**Implementation** (2 components):
- [ ] `tools/generate_test_project.py` (working CLI tool)
- [ ] `tests/e2e/mcp_server/harness_server.py` (MCP skeleton with 13 working tools, 20 stubs)

**Infrastructure** (1 component):
- [ ] `tests/e2e/mcp_server/pyproject.toml` (FastMCP project config)

**Testing**:
- [ ] 7 test failures fixed (E2E design validation)
- [ ] Test pass rate increases from 89.2% to 91.6%

**Total Phase 1**: 3,600-5,100 lines of documentation + 600-800 lines of code = 4,200-5,900 lines

---

### Phase 2 Deliverables (FUTURE)

**Implementation** (4 components):
- [ ] 20 API-dependent MCP tools (fully functional)
- [ ] Docker infrastructure (Dockerfiles, docker-compose)
- [ ] Pytest fixtures (session, harness, cleanup)
- [ ] E2E test suite (46+ tests across 6 test files)

**Testing**:
- [ ] Automated plugin installation testing
- [ ] Automated command execution testing
- [ ] Automated conversation simulation
- [ ] Automated workflow completion testing
- [ ] Automated integration testing
- [ ] CI/CD integration

**Total Phase 2**: 2,000-3,000 lines of code + infrastructure

---

## WORK ITEMS SUMMARY

### Phase 1 Work Items

| Priority | Task | Effort | Status | Fixes Tests |
|----------|------|--------|--------|-------------|
| P0 | E2E Architecture Documentation | 4 hours | Not Started | 1 test |
| P0 | Conversation Simulation Design | 2 hours | Not Started | 1 test |
| P0 | API Requirements Documentation | 2 hours | Not Started | 1 test |
| P0 | Test Project Generator | 3-4 hours | Not Started | 1 test |
| P1 | MCP Server Skeleton | 4-6 hours | Not Started | 0 tests |
| P1 | Docker Feasibility Research | 2-4 hours | Not Started | 1 test |
| P2 | E2E Test Projects Setup | 15 min | Not Started | 1 test |
| P2 | Design Completeness Validation | 30 min | Not Started | 1 test |

**Total Phase 1**: 15-22 hours, fixes 7 test failures

---

### Phase 2 Work Items (BLOCKED)

| Priority | Task | Effort | Status | Blocker |
|----------|------|--------|--------|---------|
| P0 | Implement API-Dependent MCP Tools | 30-40 hours | BLOCKED | API |
| P0 | Build Docker Infrastructure | 6-10 hours | BLOCKED | Docker research + API |
| P0 | Integrate with Pytest | 4-6 hours | BLOCKED | API + Docker |
| P0 | Write E2E Test Suite | 10-15 hours | BLOCKED | All above |

**Total Phase 2**: 40-60 hours, ALL BLOCKED on Claude Code API

---

## RECOMMENDATIONS

### Primary Recommendation: Execute Phase 1 NOW, Defer Phase 2 to Future

**Proceed with Phase 1 IF**:
1. ✅ Can commit 15-22 hours over 2 weeks (parallel with Path A Phase 1)
2. ✅ Accept that Phase 2 timeline is completely unknown
3. ✅ Value the immediate benefits (fix 7 tests, document architecture)
4. ✅ Want to be prepared when API becomes available
5. ✅ Path A manual testing proceeds regardless (not blocked)

**Start with**: P0 items (11-12 hours over Week 1)

**First Major Decision**: After Week 1 → Are P0 items complete? Proceed to P1?

**Second Major Decision**: After Week 2 → Phase 1 complete? Return to Path A or wait for API news?

---

### Alternative: Return to Path A Immediately

**Choose Path A Only** if:
- Phase 1 time investment (15-22 hours) not worthwhile
- Manual testing is sufficient for all future releases
- API timeline uncertainty is unacceptable
- Want to focus entirely on v1.0.0 completion

**Action**: Skip test harness work entirely, proceed with PLAN-path-a-revised-2025-11-07-014830.md

**Benefit**: Saves 15-22 hours, full focus on manual testing

**Cost**: No automated testing preparation, remains 100% manual forever

---

### Hybrid Approach: Do P0 Only, Skip P1/P2

**Minimal Investment Option**:
- Complete P0 items only (11-12 hours)
- Skip MCP skeleton and Docker research (save 6-10 hours)
- Fix 5 test failures instead of 7
- Document core architecture without full implementation preparation

**Benefit**: Minimal time investment (11-12 hours), majority of value delivered

**Cost**: Less prepared for Phase 2, 2 test failures remain

---

## HONEST SELF-ASSESSMENT CHECKLIST

Before starting Phase 1, answer these questions honestly:

### Time Commitment
- [ ] I can dedicate 15-22 hours to Phase 1 over 2 weeks
- [ ] I can work on this parallel with Path A Phase 1 work
- [ ] I accept Phase 2 timeline is completely unknown (could be never)
- [ ] I understand Phase 1 does not deliver functional automation

### Value Proposition
- [ ] Fixing 7 test failures is worthwhile
- [ ] Documenting architecture is valuable even if Phase 2 never happens
- [ ] Test project generator improves manual testing (Path A benefit)
- [ ] Providing API requirements to Anthropic is valuable

### Risk Tolerance
- [ ] I accept 20% probability Claude Code API never provided
- [ ] I accept 30% probability API insufficient for needs
- [ ] I accept 30% probability Docker doesn't work
- [ ] I accept Phase 2 may be blocked for years

### Decision Criteria
- [ ] After Phase 1, I will return to Path A manual testing
- [ ] I will NOT wait indefinitely for Phase 2 to start
- [ ] I will track API news but not depend on it
- [ ] I accept v1.0.0 ships with manual testing only

**If you answered YES to ALL**: Proceed with Phase 1 (this plan)
**If you answered NO to ANY**: Skip test harness, proceed with Path A only

---

## NEXT IMMEDIATE ACTIONS

### Action 1: Make Decision (NOW - 5 minutes)

**Question**: Invest 15-22 hours in Phase 1 design work, or return to Path A?

**Options**:
- **Option A**: Phase 1 NOW, Phase 2 FUTURE → Proceed to Action 2
- **Option B**: Path A only → Go to PLAN-path-a-revised-2025-11-07-014830.md
- **Option C**: P0 only, skip P1/P2 → Modified Phase 1 (11-12 hours)

**Make decision, then proceed accordingly.**

---

### Action 2: Start Phase 1 P0 Items (Week 1 - 11 hours)

**IF Decision = Option A or C**:

**Day 1-2: E2E Architecture Documentation** (4 hours)
- Create `tests/e2e/design/ARCHITECTURE.md`
- Document test harness components
- Include tool inventory (33 tools)
- Document Docker orchestration strategy
- Document pytest integration approach

**Day 3: Conversation Simulation Design** (2 hours)
- Create `tests/e2e/design/CONVERSATION_SIMULATION.md`
- Document conversation state machine
- Define multi-turn interaction patterns
- Include 3-5 example test scenarios

**Day 4: API Requirements Documentation** (2 hours)
- Create `tests/e2e/design/API_REQUIREMENTS.md`
- Document all 5 API categories (20 tools)
- Include use cases and priority levels
- Document alternative approaches

**Day 5: Test Project Generator** (3 hours)
- Create `tools/generate_test_project.py`
- Implement Python, JavaScript, Go support
- Support web-app, CLI, library types
- Test with realistic project generation

**Outcome**: 5 test failures fixed, core design documented, test generator working

---

### Action 3: Continue Phase 1 P1 Items (Week 2 - 6-10 hours)

**IF Week 1 successful and want to complete Phase 1**:

**Day 1-2: MCP Server Skeleton** (4-6 hours)
- Create `tests/e2e/mcp_server/harness_server.py`
- Implement 13 non-API tools (Categories 6-8)
- Stub 20 API-dependent tools
- Validate with `fastmcp dev`

**Day 3-4: Docker Feasibility Research** (2-4 hours)
- Create base Dockerfile
- Attempt Claude Code in container
- Document results (works / partial / doesn't work)
- Update `tests/e2e/design/DOCKER_SETUP.md`

**Day 5: Finalize Phase 1** (1 hour)
- Create `tests/e2e/test_projects/` directory
- Run design completeness validation
- Verify 7 test failures fixed
- Document Phase 1 completion

**Outcome**: Phase 1 complete, ready for Phase 2 (when API available)

---

### Action 4: Return to Path A (After Phase 1 Complete)

**After Phase 1 done (Week 2 end)**:

1. Document Phase 1 completion in CLAUDE.md
2. Update test pass rate (89.2% → 91.6%)
3. Return to Path A manual testing (PLAN-path-a-revised-2025-11-07-014830.md)
4. Monitor Anthropic for API news
5. Shelve Phase 2 work until API available

**Do NOT wait for Phase 2 to start. Proceed with Path A v1.0.0 completion.**

---

## FILE MANAGEMENT

**This Planning File**: `PLAN-test-harness-2025-11-07-023500.md`

**Source Files**:
- STATUS-test-harness-feasibility-2025-11-07-022042.md (feasibility assessment)
- PLAN-path-a-revised-2025-11-07-014830.md (Path A execution plan)
- CLAUDE.md (specification)

**Existing PLAN Files** (before this file):
1. PLAN-path-a-revised-2025-11-07-014830.md
2. PLAN-final-100-percent-2025-11-07-012334.md
3. PLAN-testing-framework-next-steps-2025-11-06-032004.md
4. PLAN-verbosity-reduction-2025-10-29-075000.md

**After this file created**: 5 total (EXCEEDS 4 max)

**Action Required**: Delete oldest file to maintain 4 max retention policy

**File to Delete**: PLAN-verbosity-reduction-2025-10-29-075000.md (oldest, least relevant)

**Remaining Files** (after deletion):
1. PLAN-testing-framework-next-steps-2025-11-06-032004.md
2. PLAN-final-100-percent-2025-11-07-012334.md
3. PLAN-path-a-revised-2025-11-07-014830.md
4. PLAN-test-harness-2025-11-07-023500.md ← this file

---

## CLOSING NOTES

### This Plan is Honest About the API Blocker

**The Core Truth**:
- Claude Code has no programmatic API (100% certain)
- Phase 2 is BLOCKED until API available (timeline unknown)
- Phase 1 delivers value regardless of Phase 2 (fixes tests, documents architecture)
- Manual testing remains the ONLY option for v1.0.0

**No False Promises**:
- Phase 1 does NOT deliver functional automation
- Phase 2 timeline is UNKNOWN (could be never)
- Test harness is preparation, not completion
- Value is in design, documentation, and preparation

### This Plan is Realistic About Effort

**Phase 1 Estimates**:
- 15-22 hours is honest (not 5-10 hours)
- 2 weeks allows for overruns
- Parallel with Path A does not block other work
- Can cut P2 items if needed

**Phase 2 Estimates**:
- 40-60 hours is realistic (not 20-30 hours)
- 4-6 weeks when API available
- All work blocked on external dependency
- Cannot start Phase 2 until API exists

### This Plan Respects Decision Gates

**Decision Point 1** (After Phase 1 Week 1):
- Continue to P1 items OR return to Path A?

**Decision Point 2** (After Phase 1 Week 2):
- Phase 1 complete, return to Path A
- Monitor API news, shelve Phase 2

**Decision Point 3** (When API Arrives):
- Start Phase 2 immediately OR defer to v1.1.0?

**Decision Point 4** (If API Never Arrives):
- Accept manual testing only, archive design work

### You Have a Clear Path Forward

**Immediate next step**: Make decision (Phase 1? Path A only? P0 only?)
**First real work**: P0 items (11 hours, Week 1)
**First decision gate**: End of Week 1
**Return to Path A**: End of Week 2 (regardless of API status)

**You have an honest, executable plan for test harness work with clear API blocker acknowledgment.**

**Good luck. Be realistic. Return to Path A for v1.0.0.**

---

**END OF TEST HARNESS IMPLEMENTATION PLAN**
