# Claude Code Conversation Simulation Framework

**Version**: 1.0.0
**Status**: Design Specification
**Last Updated**: 2025-11-07

---

## Executive Summary

This document specifies the conversation simulation framework for Claude Code E2E testing. The framework enables automated multi-turn conversations that test agent behaviors, workflow progressions, and command chaining across complex scenarios. The design centers on a state machine model that tracks conversation context, workflow stages, and agent modes throughout multi-stage interactions.

### Purpose

The conversation simulation framework provides:

1. **Multi-Turn Interaction**: Support for complex conversations with 5-20 turns
2. **State Tracking**: Track workflow stages, agent modes, and conversation context
3. **Semantic Assertions**: Validate agent responses without brittle exact-string matching
4. **Workflow Validation**: Verify agents progress through expected workflow stages
5. **Command Chaining**: Test multi-command sequences (explore → plan → code → commit)

### Critical Dependency

This framework design is **BLOCKED** on the Claude Code programmatic API (see API_REQUIREMENTS.md). The state machine and assertion strategies are ready, but functional implementation requires API endpoints for conversation management and state inspection.

---

## Conversation State Machine

### State Definitions

The conversation simulation tracks conversations through five distinct states that represent the lifecycle of a test conversation:

**State 1: IDLE**
- Description: No active conversation, waiting for test to start session
- Entry Conditions: Initial state, or after END_CONVERSATION completes
- Valid Transitions: → USER_PROMPT (via start_conversation API call)
- State Data: None
- Actions Allowed: start_conversation()

**State 2: USER_PROMPT**
- Description: User has sent a prompt, waiting for agent to process and respond
- Entry Conditions: User called send_prompt() or execute_command()
- Valid Transitions: → AGENT_RESPONDING (agent begins generating response)
- State Data: `{prompt_text: str, prompt_id: str, timestamp: datetime}`
- Actions Allowed: cancel_prompt(), get_prompt_status()

**State 3: AGENT_RESPONDING**
- Description: Agent is actively generating response (may involve tool calls, reasoning)
- Entry Conditions: Agent received prompt and began processing
- Valid Transitions: → WORKFLOW_TRANSITION (if workflow stage changes), → COMMAND_EXECUTING (if command was executed), → USER_PROMPT (ready for next turn)
- State Data: `{response_id: str, tool_calls: List[ToolCall], partial_response: str, progress: float}`
- Actions Allowed: get_response_status(), cancel_response()

**State 4: COMMAND_EXECUTING**
- Description: A slash command is being executed (e.g., /explore is running)
- Entry Conditions: Agent recognized command in prompt
- Valid Transitions: → AGENT_RESPONDING (command execution triggers agent response)
- State Data: `{command_name: str, command_args: Dict, execution_id: str, start_time: datetime}`
- Actions Allowed: get_command_status(), cancel_command()

**State 5: WORKFLOW_TRANSITION**
- Description: Agent workflow stage is changing (exploring → planning, etc.)
- Entry Conditions: Agent completed action that triggers stage transition
- Valid Transitions: → AGENT_RESPONDING (after transition completes), → USER_PROMPT (ready for next turn)
- State Data: `{from_stage: str, to_stage: str, transition_time: datetime, transition_trigger: str}`
- Actions Allowed: verify_transition(), get_workflow_stage()

### State Transition Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  START                                                          │
│    │                                                            │
│    ▼                                                            │
│  ┌──────┐   start_conversation()   ┌──────────────┐           │
│  │ IDLE │───────────────────────────▶│ USER_PROMPT  │           │
│  └──────┘                            └──────┬───────┘           │
│    ▲                                        │                   │
│    │                                        │ send_prompt()     │
│    │                                        │                   │
│    │                                        ▼                   │
│    │                             ┌──────────────────┐           │
│    │                             │ AGENT_RESPONDING │           │
│    │                             └────────┬─────────┘           │
│    │                                      │                     │
│    │                                      │                     │
│    │              ┌───────────────────────┼─────────────┐       │
│    │              │                       │             │       │
│    │              │                       │             │       │
│    │              ▼                       ▼             ▼       │
│    │   ┌──────────────────┐   ┌───────────────────┐  Response │
│    │   │ COMMAND_EXECUTING│   │WORKFLOW_TRANSITION│  Complete  │
│    │   └─────────┬────────┘   └─────────┬─────────┘           │
│    │             │                       │                     │
│    │             │                       │                     │
│    │             └───────────┬───────────┘                     │
│    │                         │                                 │
│    │                         │                                 │
│    │                         ▼                                 │
│    │              ┌──────────────────┐                        │
│    │              │   USER_PROMPT    │ ◀──┐                   │
│    │              └─────────┬────────┘    │ Next Turn          │
│    │                        │             │                   │
│    │                        └─────────────┘                   │
│    │                                                           │
│    │ end_conversation()                                       │
│    └───────────────────────────────────────────────────────   │
│                                                                 │
│  END                                                            │
└─────────────────────────────────────────────────────────────────┘
```

### State Persistence

Conversation state is maintained at three levels for comprehensive testing:

**Session-Level State** (persists across turns within conversation):
- Conversation history (all turns)
- Current workflow stage
- Active agent mode
- Plugin context (loaded plugins, available commands)
- Session metadata (session_id, start_time, working_directory)

**Turn-Level State** (specific to current turn):
- Current prompt
- Current response (partial or complete)
- Tool calls in progress
- Command execution status

**Workflow-Level State** (for workflow-oriented agents):
- Current stage (idle, exploring, planning, coding, committing)
- Stage history (stages completed)
- Stage entry time
- Actions completed in current stage
- Actions remaining in current stage

---

## Multi-Turn Interaction Patterns

### Pattern 1: agent-loop 4-Stage Workflow

**Workflow**: explore → plan → code → commit

**Typical Conversation**:
```
Turn 1 (User):    "/explore"
Turn 2 (Agent):   "I'll systematically investigate the codebase..." [TRANSITION: idle → exploring]
Turn 3 (User):    "explore the database layer"
Turn 4 (Agent):   "Exploring database layer... [tool calls]... findings: ..." [STAGE: exploring]
Turn 5 (User):    "/plan"
Turn 6 (Agent):   "Creating implementation plan..." [TRANSITION: exploring → planning]
Turn 7 (User):    "plan how to add user authentication"
Turn 8 (Agent):   "Implementation plan: 1. ... 2. ... 3. ..." [STAGE: planning]
Turn 9 (User):    "/code"
Turn 10 (Agent):  "Implementing the plan..." [TRANSITION: planning → coding]
Turn 11 (User):   "implement the authentication module"
Turn 12 (Agent):  "Implementing... [code changes]... done" [STAGE: coding]
Turn 13 (User):   "/commit"
Turn 14 (Agent):  "Creating git commit..." [TRANSITION: coding → committing → complete]
```

**Assertion Points**:
- Turn 2: Verify response contains keywords ["systematic", "investigation", "explore"]
- Turn 2: Verify workflow transitioned to "exploring"
- Turn 4: Verify agent used Read/Glob tools for exploration
- Turn 6: Verify workflow transitioned to "planning"
- Turn 6: Verify agent suggests /code as next step
- Turn 10: Verify workflow transitioned to "coding"
- Turn 14: Verify git commit created successfully
- Turn 14: Verify workflow reached "complete" stage

---

### Pattern 2: epti 6-Stage TDD Workflow

**Workflow**: write-tests → verify-fail → commit-tests → implement → iterate → commit-code

**Typical Conversation**:
```
Turn 1 (User):    "/write-tests for user authentication"
Turn 2 (Agent):   "Writing tests first (TDD discipline)..." [TRANSITION: idle → writing-tests]
Turn 3 (User):    "create unit tests for User.authenticate()"
Turn 4 (Agent):   "Created test_user_auth.py with 5 test cases..." [STAGE: writing-tests]
Turn 5 (User):    "/verify-fail"
Turn 6 (Agent):   "Running tests to verify they fail..." [TRANSITION: writing-tests → verifying-failure]
Turn 7 (User):    "run the tests"
Turn 8 (Agent):   "Tests executed: 5 failed (as expected)..." [STAGE: verifying-failure]
Turn 9 (User):    "/commit-tests"
Turn 10 (Agent):  "Committing tests to git..." [TRANSITION: verifying-failure → committing-tests]
Turn 11 (User):   "commit the test suite"
Turn 12 (Agent):  "Committed tests with message 'test: add user auth tests'" [STAGE: committed-tests]
Turn 13 (User):   "/implement"
Turn 14 (Agent):  "Implementing code to pass tests..." [TRANSITION: committed-tests → implementing]
Turn 15 (User):   "implement User.authenticate() method"
Turn 16 (Agent):  "Implemented authentication logic..." [STAGE: implementing]
Turn 17 (User):   "/iterate"
Turn 18 (Agent):  "Running tests... all passing! Refactoring..." [TRANSITION: implementing → iterating]
Turn 19 (User):   "refactor for better error handling"
Turn 20 (Agent):  "Refactored, tests still passing..." [STAGE: iterating]
Turn 21 (User):   "/commit-code"
Turn 22 (Agent):  "Committing final implementation..." [TRANSITION: iterating → committing-code → complete]
```

**Assertion Points**:
- Turn 2: Verify TDD discipline enforced (tests before code)
- Turn 6: Verify tests run and failures detected
- Turn 8: Assert test failure output contains expected errors
- Turn 10: Verify pre-implementation commit hook allowed test commit
- Turn 14: Verify agent cannot skip to implementation without test commit
- Turn 18: Verify all tests pass before refactoring
- Turn 22: Verify final commit includes implementation

---

### Pattern 3: visual-iteration Screenshot Feedback Loop

**Workflow**: screenshot → feedback → refine → [iterate 2-3 times] → commit

**Typical Conversation**:
```
Turn 1 (User):    "/screenshot"
Turn 2 (Agent):   "Capturing current UI state..." [STAGE: capturing]
Turn 3 (User):    "capture the dashboard page"
Turn 4 (Agent):   "Screenshot saved... analyzing..." [MCP: browser-tools screenshot tool]
Turn 5 (User):    "/feedback"
Turn 6 (Agent):   "Visual analysis: Button padding 32px should be 24px..." [STAGE: analyzing]
Turn 7 (User):    "provide specific CSS improvements"
Turn 8 (Agent):   "Specific changes: 1. button: 32px → 24px, 2. border-radius: 0 → 2px..." [STAGE: feedback-provided]
Turn 9 (User):    "/refine"
Turn 10 (Agent):  "Applying visual improvements..." [TRANSITION: feedback-provided → refining]
Turn 11 (User):   "apply the CSS changes"
Turn 12 (Agent):  "Updated styles.css with improvements..." [STAGE: refining]
Turn 13 (User):   "/screenshot"
Turn 14 (Agent):  "Capturing updated UI..." [STAGE: capturing-iteration-2]
Turn 15 (User):   "capture the updated dashboard"
Turn 16 (Agent):  "Screenshot saved... looks better!" [STAGE: iteration-2]
Turn 17 (User):   "/feedback"
Turn 18 (Agent):  "Visual analysis: Heading size 24px should be 20px..." [STAGE: analyzing-iteration-2]
Turn 19 (User):   "any remaining issues?"
Turn 20 (Agent):  "One more refinement needed: heading size..." [STAGE: feedback-provided-iteration-2]
Turn 21 (User):   "/refine"
Turn 22 (Agent):  "Applying final polish..." [STAGE: refining-iteration-2]
Turn 23 (User):   "apply heading size change"
Turn 24 (Agent):  "Updated... pixel-perfect now!" [STAGE: polished]
Turn 25 (User):   "/commit-visual"
Turn 26 (Agent):  "Committing visual improvements..." [TRANSITION: polished → committing]
```

**Assertion Points**:
- Turn 4: Verify browser-tools MCP server invoked for screenshot
- Turn 6: Verify SPECIFIC feedback (exact pixel values, not vague "improve spacing")
- Turn 8: Assert feedback includes CSS property names and values
- Turn 12: Verify CSS file was actually modified
- Turn 16: Verify second screenshot captured (iteration 2)
- Turn 20: Verify remaining issues identified
- Turn 24: Verify agent declares "pixel-perfect" or similar completion phrase
- Turn 26: Verify git commit created with visual changes

---

## Assertion Strategies

### Strategy 1: Keyword Presence (Semantic Matching)

**Purpose**: Validate agent response contains expected concepts without exact string matching

**Implementation**:
```python
def assert_contains_keywords(
    response: str,
    keywords: List[str],
    require_all: bool = False,
    case_sensitive: bool = False
) -> AssertionResult:
    """
    Check if response contains expected keywords.

    Args:
        response: Agent response text
        keywords: List of keywords to find
        require_all: If True, ALL keywords must be present; if False, ANY is sufficient
        case_sensitive: Whether to match case exactly

    Returns:
        AssertionResult with:
        - passed: bool
        - found_keywords: List[str]
        - missing_keywords: List[str]
        - match_ratio: float (0.0-1.0)
    """
    if not case_sensitive:
        response = response.lower()
        keywords = [k.lower() for k in keywords]

    found = [kw for kw in keywords if kw in response]
    missing = [kw for kw in keywords if kw not in response]

    passed = (len(missing) == 0) if require_all else (len(found) > 0)

    return AssertionResult(
        passed=passed,
        found_keywords=found,
        missing_keywords=missing,
        match_ratio=len(found) / len(keywords) if keywords else 0.0
    )
```

**Use Cases**:
- Verify explore response mentions "systematic", "investigation", "codebase"
- Check plan response includes "strategy", "implementation", "steps"
- Validate feedback contains "specific", "CSS", "pixel"

**Why This Works**:
- Handles response variability (LLM generates different phrasings)
- Validates intent rather than exact wording
- Robust to model updates and temperature changes
- Allows natural language variation

---

### Strategy 2: Workflow Transition Validation

**Purpose**: Verify agent progressed through expected workflow stages

**Implementation**:
```python
def assert_workflow_transition(
    from_stage: str,
    to_stage: str,
    actual_stage: str,
    allow_skip: bool = False
) -> AssertionResult:
    """
    Verify workflow stage transition is correct.

    Args:
        from_stage: Expected previous stage
        to_stage: Expected current stage
        actual_stage: Actual current stage from API
        allow_skip: If True, allow skipping intermediate stages

    Returns:
        AssertionResult with:
        - passed: bool
        - expected_transition: str (e.g., "exploring → planning")
        - actual_stage: str
        - valid: bool (whether transition is valid in workflow)
    """
    # Check exact match
    if actual_stage.lower() == to_stage.lower():
        return AssertionResult(
            passed=True,
            expected_transition=f"{from_stage} → {to_stage}",
            actual_stage=actual_stage,
            valid=True
        )

    # Check if transition is valid (even if not expected)
    valid_transitions = get_valid_transitions(from_stage)  # From workflow definition

    return AssertionResult(
        passed=False,
        expected_transition=f"{from_stage} → {to_stage}",
        actual_stage=actual_stage,
        valid=(actual_stage in valid_transitions)
    )
```

**Use Cases**:
- Verify explore command transitions to "exploring" stage
- Check plan command moves from "exploring" to "planning"
- Validate TDD workflow enforces correct stage order

---

### Strategy 3: Command Suggestion Detection

**Purpose**: Verify agent suggests appropriate next command in workflow

**Implementation**:
```python
def assert_command_suggested(
    response: str,
    command_name: str,
    allow_variations: bool = True
) -> AssertionResult:
    """
    Check if agent suggests specific command.

    Args:
        response: Agent response text
        command_name: Command to look for (e.g., "/plan")
        allow_variations: Allow mentions like "run /plan" or "use the plan command"

    Returns:
        AssertionResult with:
        - passed: bool
        - command_found: str (exact text matched)
        - location: int (character position)
        - context: str (surrounding text)
    """
    # Normalize command (add slash if missing)
    if not command_name.startswith("/"):
        command_name = "/" + command_name

    # Find command mention
    location = response.find(command_name)

    if location >= 0:
        # Extract context (20 chars before/after)
        start = max(0, location - 20)
        end = min(len(response), location + len(command_name) + 20)
        context = response[start:end]

        return AssertionResult(
            passed=True,
            command_found=command_name,
            location=location,
            context=context
        )

    # If allow_variations, check for alternative phrasings
    if allow_variations:
        variations = [
            command_name.lstrip("/"),  # Without slash
            f"use {command_name}",
            f"run {command_name}",
            f"execute {command_name}",
            f"{command_name.lstrip('/')} command"
        ]

        for variation in variations:
            if variation.lower() in response.lower():
                return AssertionResult(
                    passed=True,
                    command_found=variation,
                    location=response.lower().find(variation.lower()),
                    context=variation
                )

    return AssertionResult(passed=False, command_found=None, location=-1)
```

**Use Cases**:
- Verify explore response suggests "/plan" as next step
- Check plan response recommends "/code"
- Validate agent guides user through workflow

---

### Strategy 4: Tool Call Verification

**Purpose**: Verify agent used expected tools during response generation

**Implementation**:
```python
def assert_tools_used(
    response_metadata: ResponseMetadata,
    expected_tools: List[str],
    require_all: bool = False
) -> AssertionResult:
    """
    Verify agent invoked expected tools.

    Args:
        response_metadata: Metadata from API (includes tool_calls list)
        expected_tools: Tools that should have been used
        require_all: If True, ALL tools must be used; if False, ANY is sufficient

    Returns:
        AssertionResult with:
        - passed: bool
        - tools_used: List[str]
        - tools_missing: List[str]
        - tool_details: List[ToolCallInfo]
    """
    tools_used = [call.tool_name for call in response_metadata.tool_calls]

    found = [tool for tool in expected_tools if tool in tools_used]
    missing = [tool for tool in expected_tools if tool not in tools_used]

    passed = (len(missing) == 0) if require_all else (len(found) > 0)

    return AssertionResult(
        passed=passed,
        tools_used=tools_used,
        tools_missing=missing,
        tool_details=response_metadata.tool_calls
    )
```

**Use Cases**:
- Verify explore command used Read and Glob tools
- Check visual-iteration used browser-tools screenshot
- Validate code command used Write tool

---

### Strategy 5: Error Handling Validation

**Purpose**: Verify agent handles errors gracefully with helpful guidance

**Implementation**:
```python
def assert_error_handled_gracefully(
    response: str,
    error_type: str,
    should_recover: bool = True
) -> AssertionResult:
    """
    Verify agent handles error appropriately.

    Args:
        response: Agent response to error condition
        error_type: Type of error (e.g., "file_not_found", "syntax_error")
        should_recover: Whether agent should suggest recovery actions

    Returns:
        AssertionResult with:
        - passed: bool
        - graceful: bool (no crash, stack trace)
        - acknowledges_error: bool
        - suggests_recovery: bool
        - recovery_actions: List[str] (suggested next steps)
    """
    response_lower = response.lower()

    # Check for crash indicators
    crash_indicators = ["traceback", "exception:", "error:", "stack trace", "failed:"]
    has_crash = any(indicator in response_lower for indicator in crash_indicators)

    # Check for error acknowledgment
    ack_indicators = ["couldn't", "unable", "can't", "not found", "error", "problem"]
    acknowledges_error = any(indicator in response_lower for indicator in ack_indicators)

    # Check for recovery suggestions
    recovery_indicators = ["let's", "try", "instead", "alternatively", "check", "verify", "could"]
    suggests_recovery = any(indicator in response_lower for indicator in recovery_indicators)

    graceful = not has_crash and acknowledges_error
    passed = graceful and (suggests_recovery if should_recover else True)

    return AssertionResult(
        passed=passed,
        graceful=graceful,
        acknowledges_error=acknowledges_error,
        suggests_recovery=suggests_recovery
    )
```

**Use Cases**:
- Test file not found scenarios
- Verify agent doesn't crash on syntax errors
- Validate agent provides helpful error messages

---

## Example Test Scenarios

### Scenario 1: agent-loop Happy Path (4 stages, 8 turns)

```python
def test_agent_loop_happy_path(harness, test_session, test_project):
    """Test complete agent-loop workflow from explore to commit"""

    # Install plugin
    harness.install_plugin("agent-loop")

    # Create test project
    project = harness.create_test_project(
        type="web-app",
        language="python",
        path=test_project
    )

    # Initialize git
    harness.setup_git_repo(project)

    # ===== TURN 1-2: EXPLORE =====
    response1 = harness.execute_command("/explore", session=test_session)

    assert_contains_keywords(
        response1.text,
        keywords=["systematic", "investigation", "explore"],
        require_all=False
    )

    assert_workflow_transition(
        from_stage="idle",
        to_stage="exploring",
        actual_stage=response1.workflow_stage
    )

    assert_command_suggested(
        response1.text,
        command_name="/plan"
    )

    # ===== TURN 3-4: PLAN =====
    response2 = harness.execute_command("/plan", session=test_session)

    assert_contains_keywords(
        response2.text,
        keywords=["implementation", "strategy", "plan"],
        require_all=False
    )

    assert_workflow_transition(
        from_stage="exploring",
        to_stage="planning",
        actual_stage=response2.workflow_stage
    )

    # ===== TURN 5-6: CODE =====
    response3 = harness.execute_command("/code", session=test_session)

    assert_workflow_transition(
        from_stage="planning",
        to_stage="coding",
        actual_stage=response3.workflow_stage
    )

    assert_tools_used(
        response3.metadata,
        expected_tools=["Write"],
        require_all=False
    )

    # ===== TURN 7-8: COMMIT =====
    response4 = harness.execute_command("/commit", session=test_session)

    assert_workflow_transition(
        from_stage="coding",
        to_stage="complete",
        actual_stage=response4.workflow_stage
    )

    # Verify git commit created
    assert_git_commit_exists(project, expected_count=2)  # Initial + agent's commit
```

---

### Scenario 2: epti TDD Discipline Enforcement (6 stages, 12 turns)

```python
def test_epti_tdd_discipline_enforcement(harness, test_session, test_project):
    """Test epti enforces TDD workflow: tests before code"""

    # Install plugin
    harness.install_plugin("epti")

    # Create test project
    project = harness.create_test_project(
        type="library",
        language="python",
        path=test_project
    )

    # Initialize git
    harness.setup_git_repo(project)

    # ===== TURN 1-2: WRITE TESTS =====
    response1 = harness.execute_command(
        "/write-tests for calculator module",
        session=test_session
    )

    assert_contains_keywords(
        response1.text,
        keywords=["test", "TDD", "discipline"],
        require_all=False
    )

    assert_workflow_transition(
        from_stage="idle",
        to_stage="writing-tests",
        actual_stage=response1.workflow_stage
    )

    # ===== TURN 3-4: VERIFY TESTS FAIL =====
    response2 = harness.execute_command("/verify-fail", session=test_session)

    assert_workflow_transition(
        from_stage="writing-tests",
        to_stage="verifying-failure",
        actual_stage=response2.workflow_stage
    )

    # Verify tests were run and failed
    assert "failed" in response2.text.lower()
    assert "passed" not in response2.text.lower()  # No tests should pass yet

    # ===== TURN 5-6: COMMIT TESTS =====
    response3 = harness.execute_command("/commit-tests", session=test_session)

    assert_workflow_transition(
        from_stage="verifying-failure",
        to_stage="committed-tests",
        actual_stage=response3.workflow_stage
    )

    # Verify git commit for tests
    assert_git_commit_message_contains(project, "test:")

    # ===== TURN 7-8: ATTEMPT TO CODE BEFORE TESTS (SHOULD BLOCK) =====
    # This tests negative case - agent should refuse

    response4 = harness.send_prompt(
        "let's implement the calculator code now",
        session=test_session
    )

    # Agent should enforce TDD: no code before tests committed
    assert_contains_keywords(
        response4.text,
        keywords=["commit", "tests", "first"],
        require_all=False
    )

    # ===== TURN 9-10: IMPLEMENT (AFTER TESTS COMMITTED) =====
    response5 = harness.execute_command("/implement", session=test_session)

    assert_workflow_transition(
        from_stage="committed-tests",
        to_stage="implementing",
        actual_stage=response5.workflow_stage
    )

    # ===== TURN 11-12: ITERATE =====
    response6 = harness.execute_command("/iterate", session=test_session)

    assert_workflow_transition(
        from_stage="implementing",
        to_stage="iterating",
        actual_stage=response6.workflow_stage
    )

    # Verify all tests pass
    assert "all.*passing" in response6.text.lower() or "tests.*pass" in response6.text.lower()
```

---

### Scenario 3: visual-iteration Feedback Loop (3 iterations, 20 turns)

```python
def test_visual_iteration_feedback_loop(harness, test_session, test_project):
    """Test visual-iteration's screenshot feedback refinement cycle"""

    # Install plugin
    harness.install_plugin("visual-iteration")

    # Create web app project
    project = harness.create_test_project(
        type="web-app",
        language="javascript",
        path=test_project
    )

    # Initialize git
    harness.setup_git_repo(project)

    # Start development server (for screenshot capture)
    harness.start_dev_server(project, port=3000)

    # ===== ITERATION 1 =====

    # TURN 1-2: Screenshot
    response1 = harness.execute_command("/screenshot", session=test_session)

    assert_tools_used(
        response1.metadata,
        expected_tools=["screenshot"],  # From browser-tools MCP
        require_all=True
    )

    # TURN 3-4: Feedback
    response2 = harness.execute_command("/feedback", session=test_session)

    # Verify SPECIFIC feedback (not vague)
    assert_specific_feedback(response2.text, min_specificity=3)

    # TURN 5-6: Refine
    response3 = harness.execute_command("/refine", session=test_session)

    assert_tools_used(
        response3.metadata,
        expected_tools=["Write"],  # Modified CSS/HTML files
        require_all=False
    )

    # ===== ITERATION 2 =====

    # TURN 7-8: Screenshot (verify improvement)
    response4 = harness.execute_command("/screenshot", session=test_session)

    # TURN 9-10: Feedback (fewer issues)
    response5 = harness.execute_command("/feedback", session=test_session)

    # Verify feedback mentions improvement
    assert_contains_keywords(
        response5.text,
        keywords=["better", "improved", "closer"],
        require_all=False
    )

    # TURN 11-12: Refine
    response6 = harness.execute_command("/refine", session=test_session)

    # ===== ITERATION 3 (FINAL POLISH) =====

    # TURN 13-14: Screenshot
    response7 = harness.execute_command("/screenshot", session=test_session)

    # TURN 15-16: Feedback (should be minimal or none)
    response8 = harness.execute_command("/feedback", session=test_session)

    # Verify agent indicates completion
    assert_contains_keywords(
        response8.text,
        keywords=["pixel-perfect", "complete", "polished", "ready"],
        require_all=False
    )

    # TURN 17-18: Commit
    response9 = harness.execute_command("/commit-visual", session=test_session)

    # Verify git commit with visual changes
    assert_git_commit_message_contains(project, "visual:")
```

---

## Conversation Context Management

### Context Tracking

The framework tracks multiple context dimensions throughout conversations:

**File Context**: Files mentioned, read, or modified
- Track which files agent has seen
- Maintain file content snapshots for each turn
- Detect when agent references files not in context

**Tool Context**: Tools invoked and their results
- Log all tool calls with inputs/outputs
- Track tool call sequences (useful for debugging)
- Detect repeated tool calls (possible agent confusion)

**Workflow Context**: Stage history and progression
- Maintain stage entry/exit times
- Track stage transitions and triggers
- Detect invalid stage transitions

**Command Context**: Commands executed and their effects
- Log command executions with full metadata
- Track command chaining patterns
- Detect command failures

---

## Implementation Roadmap

### Phase 1: Design (COMPLETE)
- State machine specification
- Assertion strategy definitions
- Example test scenarios
- Context tracking design

### Phase 2: Implementation (BLOCKED on API)
- Implement state machine in Python
- Build assertion helper library
- Create conversation test fixtures
- Integrate with pytest

### Phase 3: Validation (FUTURE)
- Run test scenarios against real Claude Code
- Refine assertion thresholds
- Optimize for test execution speed
- Document failure patterns

---

## Conclusion

This conversation simulation framework provides a comprehensive foundation for testing multi-turn agent interactions in Claude Code. The state machine model, assertion strategies, and example scenarios are ready for implementation once the Claude Code programmatic API becomes available.

**Status**: Design complete, implementation blocked on API.

For API details, see `API_REQUIREMENTS.md`.
For tool implementation, see `ARCHITECTURE.md`.
For Docker configuration, see `DOCKER_SETUP.md`.
