# Phase 1 Test Harness Functional Tests

**Test File**: `test_phase1_test_harness.py`
**Reference**: `PLAN-test-harness-2025-11-07-023500.md`
**Total Tests**: 57 tests covering 8 work items

## Overview

This test suite validates **Phase 1** of the Test Harness Implementation Plan. Phase 1 focuses on **design and preparation** work that can be completed NOW, before the Claude Code API becomes available.

**Phase 1 Goal**: Document test harness architecture, design conversation simulation framework, document API requirements, implement supporting tools, and prepare infrastructure for Phase 2 functional implementation.

## Anti-Gaming Design Philosophy

These tests are designed to be **ungameable** - they cannot be satisfied by:
- ❌ Lorem ipsum filler text
- ❌ Keyword stuffing without substance
- ❌ Stub implementations marked "TODO"
- ❌ Empty files or minimal content
- ❌ Copy-pasted examples without customization

Instead, tests validate:
- ✅ **Real document structure**: Sections, tables, code blocks, diagrams
- ✅ **Executable code**: Python syntax validation, function definitions
- ✅ **Substantive content**: Paragraph counting, sentence structure analysis
- ✅ **Cross-references**: Consistency between related documents
- ✅ **Research findings**: Experiment metadata, results documentation
- ✅ **Concrete specifications**: Function signatures, API definitions

## Test Coverage by Work Item

### P0-1: Architecture Documentation (7 tests)

**File Under Test**: `tests/e2e/design/ARCHITECTURE.md`

Tests validate:
- Document exists at expected path
- Minimum length (800-1,200 lines) for comprehensive coverage
- Required major sections (overview, components, MCP server, Docker, pytest, isolation, assertions, tools)
- Component diagram included (ASCII art showing architecture)
- All 33 MCP tools documented (13 implementable, 20 blocked)
- Substantive explanatory content (at least 10 detailed paragraphs)
- Code examples with valid Python syntax
- References STATUS feasibility assessment findings

**Why These Tests Matter**: Architecture document is the blueprint for Phase 2 implementation. Must be thorough, accurate, and based on feasibility research.

### P0-2: Conversation Simulation Design (5 tests)

**File Under Test**: `tests/e2e/design/CONVERSATION_SIMULATION.md`

Tests validate:
- Document exists at expected path
- Minimum length (500-800 lines)
- State machine documented (states: idle, prompt, thinking, responding, transition)
- State transitions clearly defined
- 3-5 complete example scenarios with multi-turn conversations
- Assertion strategies documented (semantic matching, workflow verification)
- Plugin-specific workflow patterns addressed (agent-loop 4-stage, epti 6-stage, visual-iteration iterative)

**Why These Tests Matter**: Conversation simulation is critical for testing agent workflows. Design must handle generative responses without brittle string matching.

### P0-3: API Requirements Documentation (6 tests)

**File Under Test**: `tests/e2e/design/API_REQUIREMENTS.md`

Tests validate:
- Document exists at expected path
- Minimum length (600-1,000 lines)
- All 5 API categories documented (plugin management, command execution, conversation, agent state, hooks)
- Concrete function signatures included (at least 20 API functions)
- Priority levels assigned (Critical, High, Medium, Low)
- Alternative approaches documented (filesystem scraping, log parsing, manual testing)
- Use cases provided for each API capability

**Why These Tests Matter**: API requirements document serves two purposes: (1) guides Phase 2 implementation when API available, (2) provides clear requirements to Anthropic that may influence API development.

### P0-4: Test Project Generator Implementation (7 tests)

**File Under Test**: `tools/generate_test_project.py`

Tests validate:
- Python file exists at expected path
- Valid Python syntax (uses ast.parse)
- CLI interface implemented (argparse or click)
- Required arguments: --type, --language, --output
- Multiple language support (Python, JavaScript, Go)
- Multiple project types (web-app, CLI, library)
- File generation functions defined
- Module can be imported successfully

**Why These Tests Matter**: Test project generator is immediately useful for manual testing AND provides fixtures for future automated testing. Must be working code, not stubs.

### P1-5: MCP Server Skeleton Implementation (9 tests)

**Files Under Test**:
- `tests/e2e/mcp_server/harness_server.py`
- `tests/e2e/mcp_server/pyproject.toml`

Tests validate:
- MCP server file exists
- Valid Python syntax
- FastMCP imported and instantiated
- At least 13 tools defined (Categories 6-8: Test environment, Assertion helpers, MCP integration)
- 20 API-dependent tools stubbed with NotImplementedError
- Comprehensive docstrings for all tools
- pyproject.toml exists with valid TOML format
- FastMCP dependency declared (fastmcp>=2.0.0)
- Category 6 tools implemented (create_test_project, setup_git_repo, create_sample_files, reset_test_environment, capture_test_artifacts)
- Category 7 tools implemented (assert_contains_keywords, assert_workflow_transition, assert_command_suggested, assert_error_handled_gracefully)

**Why These Tests Matter**: MCP server skeleton provides working tools NOW and clearly marks API-dependent tools for Phase 2. Tests enforce distinction between implemented and stubbed tools.

### P1-6: Docker Feasibility Research (7 tests)

**File Under Test**: `tests/e2e/design/DOCKER_SETUP.md`

Tests validate:
- Document exists at expected path
- Minimum length (500-800 lines)
- **Experiment conducted**: Metadata or text confirms actual testing performed
- **Result documented**: Success, partial success, or failure clearly stated
- Dockerfile included (attempted or working)
- Environment variables identified and documented
- Volume mounts identified and documented
- Recommendation provided (viable / needs workarounds / not viable)

**Why These Tests Matter**: Docker research answers critical unknown: Can Claude Code run in containers? Tests enforce REAL experimentation, not speculation.

**Anti-Gaming Focus**: Tests specifically look for:
- YAML frontmatter with `experiment_conducted: true` or `tested: true`
- Result indicators: "success", "failure", "works", "doesn't work", "blocked"
- Actual Dockerfile code block with FROM/RUN commands
- This prevents documenting theory without actually attempting containerization

### P2-7: E2E Test Projects Directory Setup (5 tests)

**Files Under Test**:
- `tests/e2e/test_projects/` (directory)
- `tests/e2e/test_projects/README.md`
- `tests/e2e/test_projects/.gitignore`

Tests validate:
- Directory exists
- README exists and explains purpose
- README mentions key concepts (test, fixture, project, generate)
- .gitignore exists
- .gitignore excludes generated projects (contains `*` pattern)

**Why These Tests Matter**: Test projects directory organizes generated fixtures. .gitignore prevents committing generated test projects to repo.

### P2-8: Design Completeness Validation (4 tests)

**Cross-Document Validation**

Tests validate:
- All 4 design documents exist (ARCHITECTURE, CONVERSATION_SIMULATION, API_REQUIREMENTS, DOCKER_SETUP)
- All documents meet minimum length requirements
- Documents reference STATUS feasibility assessment
- Architecture document cross-references other design documents

**Why These Tests Matter**: Ensures Phase 1 deliverables are mutually consistent and complete. Validates work is based on feasibility assessment findings.

### Summary Tests (2 tests)

**Master Validation**

Tests validate:
- All 8 Phase 1 deliverables complete (comprehensive failure report if incomplete)
- Phase 1 prepares infrastructure for Phase 2 (API requirements documented, MCP server has stubs, architecture complete)

**Why These Tests Matter**: Provides high-level Phase 1 completion status and readiness for Phase 2.

## Running the Tests

### Run All Phase 1 Tests

```bash
cd loom99-claude-marketplace
uv run pytest tests/functional/test_phase1_test_harness.py -v
```

### Run Tests by Work Item

```bash
# P0-1: Architecture Documentation
uv run pytest tests/functional/test_phase1_test_harness.py::TestArchitectureDocumentation -v

# P0-2: Conversation Simulation Design
uv run pytest tests/functional/test_phase1_test_harness.py::TestConversationSimulationDesign -v

# P0-3: API Requirements Documentation
uv run pytest tests/functional/test_phase1_test_harness.py::TestAPIRequirementsDocumentation -v

# P0-4: Test Project Generator Implementation
uv run pytest tests/functional/test_phase1_test_harness.py::TestProjectGeneratorImplementation -v

# P1-5: MCP Server Skeleton Implementation
uv run pytest tests/functional/test_phase1_test_harness.py::TestMCPServerSkeleton -v

# P1-6: Docker Feasibility Research
uv run pytest tests/functional/test_phase1_test_harness.py::TestDockerFeasibilityResearch -v

# P2-7: E2E Test Projects Directory Setup
uv run pytest tests/functional/test_phase1_test_harness.py::TestE2ETestProjectsDirectory -v

# P2-8: Design Completeness Validation
uv run pytest tests/functional/test_phase1_test_harness.py::TestE2EDesignCompletenessValidation -v

# Summary Tests
uv run pytest tests/functional/test_phase1_test_harness.py::TestPhase1CompleteSummary -v
```

### Run Specific Test

```bash
uv run pytest tests/functional/test_phase1_test_harness.py::TestPhase1CompleteSummary::test_phase1_all_deliverables_complete -v
```

## Expected Test Results

### Initial State (Nothing Implemented)

All 57 tests should **FAIL** with clear error messages indicating what's missing:

```
FAILED - P0-1: Architecture document missing
FAILED - P0-2: Conversation simulation document missing
FAILED - P0-3: API requirements document missing
FAILED - P0-4: Test project generator missing
FAILED - P1-5: MCP server implementation missing
FAILED - P1-6: Docker setup document missing
FAILED - P2-7: Test projects directory missing
...
Progress: 0/8 deliverables complete
```

### Progressive Implementation

As work items are completed, tests transition from FAIL to PASS:

```
PASSED - P0-1: Architecture document exists
PASSED - P0-1: Architecture has required sections
FAILED - P0-1: Architecture missing component diagram
...
Progress: 2/8 deliverables complete
```

### Phase 1 Complete

When all work items are implemented, all 57 tests should **PASS**:

```
57 passed in X.XXs
Progress: 8/8 deliverables complete
Phase 1 READY for Phase 2 implementation
```

## Test Strategies by Validation Type

### Document Structure Validation

**Method**: Parse markdown into sections using regex

```python
sections = parse_markdown_sections(content)
assert "## Overview" in sections.keys()
```

**Why Ungameable**: Requires actual markdown headings, not just keywords in text.

### Code Syntax Validation

**Method**: Use Python AST parser

```python
assert validate_python_syntax(code)  # Uses ast.parse()
functions = parse_python_functions(code)
assert "create_test_project" in functions
```

**Why Ungameable**: Code must be valid Python that parses successfully.

### Substantive Content Validation

**Method**: Count paragraphs meeting strict criteria

```python
substantive_paras = count_substantive_paragraphs(content)
assert substantive_paras >= 10
```

**Criteria**:
- At least 200 characters long
- At least 3 sentences (. ! ?)
- Not list items or headings

**Why Ungameable**: Lorem ipsum alone won't pass - needs structured explanatory text.

### Diagram Validation

**Method**: Extract ASCII art from code blocks

```python
diagrams = extract_ascii_diagrams(content)
assert len(diagrams) >= 1
assert "mcp" in diagrams[0].lower()
```

**Criteria**:
- Box-drawing characters or ASCII patterns
- Multiple lines (at least 3)
- Mentions key components

**Why Ungameable**: Requires actual diagram, not just description.

### Table Validation

**Method**: Parse markdown tables into structured data

```python
tables = extract_markdown_tables(content)
assert any("Priority" in table.keys() for table in tables)
```

**Why Ungameable**: Requires actual markdown table syntax with pipes and separators.

### Cross-Reference Validation

**Method**: Check document mentions other documents

```python
assert "STATUS" in architecture_content.lower()
assert "CONVERSATION_SIMULATION" in architecture_content
```

**Why Ungameable**: Documents must actually reference each other for consistency.

### Experiment Validation (Docker Research)

**Method**: Look for experiment metadata and results

```python
frontmatter = parse_yaml_frontmatter(content)
assert frontmatter["experiment_conducted"] == True
assert frontmatter["result"] in ["success", "failure", "blocked"]
```

**Why Ungameable**: Forces actual experimentation, not theoretical documentation.

## Failure Message Examples

### Clear Actionable Feedback

When tests fail, messages provide specific guidance:

```
AssertionError: Architecture document only 350 lines.
P0-1 requires comprehensive documentation (800-1,200 lines).
Current length suggests incomplete content.
```

```
AssertionError: Architecture document missing required sections:
  - docker orchestration
  - assertion framework
  - tool inventory

P0-1 requires comprehensive architecture documentation
```

```
AssertionError: MCP server has only 3 tool definitions.
P1-5 requires 13 implementable tools (Categories 6-8).
Note: 20 more should be stubbed (Categories 1-5).
```

```
AssertionError: Docker research doesn't document experiment result.
P1-6 requires clear outcome: success, partial success, or failure.
```

## Success Criteria Summary

Phase 1 is **COMPLETE** when:
- ✅ All 57 tests pass
- ✅ All 8 work items have deliverables present
- ✅ All documents meet minimum length requirements
- ✅ All documents have substantive content (not just outlines)
- ✅ MCP server has 13 implemented tools + 20 stubs
- ✅ Test project generator is working executable code
- ✅ Docker research documents actual experiment results
- ✅ Documents cross-reference each other consistently
- ✅ Summary test confirms Phase 1 ready for Phase 2

## What Comes After Phase 1?

**Phase 1 Output**: Design documentation, test fixtures, MCP skeleton, research findings

**Phase 1 Status**: Can be completed NOW (no external blockers)

**Phase 2 Trigger**: Claude Code programmatic API becomes available

**Phase 2 Work**:
- Implement 20 API-dependent MCP tools (currently stubbed)
- Build Docker infrastructure based on research findings
- Integrate MCP server with pytest
- Write E2E test suite using conversation simulation framework

**Phase 2 Status**: BLOCKED until API available (timeline unknown)

## Dependencies

Tests require these Python packages (already in pyproject.toml):
- `pytest>=7.4.0` - Test framework
- `PyYAML>=6.0.1` - YAML frontmatter parsing
- `tomli>=2.0.0` - TOML pyproject.toml parsing

All dependencies installed automatically via `uv sync`.

## Maintenance Notes

### When to Update Tests

Update tests when:
- PLAN requirements change (e.g., minimum line counts adjusted)
- New work items added to Phase 1
- Acceptance criteria modified
- Document structure requirements change

**Do NOT** update tests to make them easier to pass. Tests should remain strict.

### Test Evolution

As implementation progresses:
- Tests may reveal edge cases not considered in PLAN
- Some tests may need minor adjustments for realistic edge cases
- Document any test changes in git commit messages
- Tests should remain ungameable throughout

## Test File Statistics

- **Total Lines**: ~1,800 lines
- **Test Classes**: 9 classes (8 work items + 1 summary)
- **Total Tests**: 57 tests
- **Helper Functions**: 12 parsing/validation utilities
- **Documentation**: Comprehensive docstrings for every test
- **Anti-Gaming Strategies**: Multiple validation approaches per work item

## Questions?

For questions about these tests:
1. Read the docstrings in `test_phase1_test_harness.py`
2. Reference `PLAN-test-harness-2025-11-07-023500.md`
3. Review `STATUS-test-harness-feasibility-2025-11-07-022042.md`
4. Check test failure messages for specific guidance

The tests are designed to be self-documenting through clear assertions and failure messages.
