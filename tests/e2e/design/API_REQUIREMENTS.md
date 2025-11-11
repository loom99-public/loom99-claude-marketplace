# Claude Code API Requirements for E2E Test Automation

**Version**: 1.0.0
**Status**: Requirements Specification (API Not Yet Available)
**Last Updated**: 2025-11-07
**Target Audience**: Anthropic Engineering Team, Plugin Developers

---

## Executive Summary

This document specifies the Claude Code programmatic API requirements needed to enable automated end-to-end testing of Claude Code plugins. Currently, Claude Code lacks a programmatic API, making functional test automation impossible. This specification defines the minimum API surface area required for test harness implementation, organized into 5 critical categories with 20 API-dependent capabilities.

###

 Critical Dependency

**BLOCKER**: E2E test harness Phase 2 implementation is 100% blocked on this API. Without programmatic access to Claude Code, we cannot:
- Install/uninstall plugins programmatically
- Execute commands and capture responses
- Simulate multi-turn conversations
- Inspect agent state and workflow stages
- Verify hook execution

### API Categories Overview

| Category | Tools | Priority | Description |
|----------|-------|----------|-------------|
| **1. Plugin Management** | 4 | CRITICAL | Install, uninstall, list, and query plugin status |
| **2. Command Execution** | 4 | CRITICAL | Execute slash commands and retrieve responses |
| **3. Conversation Simulation** | 5 | CRITICAL | Start sessions, send prompts, get responses, manage history |
| **4. Agent State Inspection** | 4 | CRITICAL | Query agent mode, workflow stage, and guidance |
| **5. Hook Verification** | 4 | HIGH | List hooks, trigger hooks, query execution log |

**Total API Endpoints Required**: Approximately 20 endpoints across 5 categories

### Success Criteria for API

An adequate Claude Code API must provide:

1. **Plugin Lifecycle Control**: Programmatic install/uninstall with status verification
2. **Command Invocation**: Execute any available command with full response capture
3. **Conversation Management**: Multi-turn conversation simulation with session isolation
4. **State Introspection**: Query agent mode, workflow stage, and contextual information
5. **Event Verification**: Verify hooks executed and blocked actions as expected

**Minimum Viable API**: Categories 1-3 (plugin management, command execution, conversation simulation) are absolutely required. Categories 4-5 enable richer testing but could be worked around with log parsing fallbacks.

---

## Category 1: Plugin Management API

### Overview

The Plugin Management API enables programmatic control of the Claude Code plugin lifecycle. This is foundational for all plugin testing - we must be able to install plugins under test, verify they loaded correctly, and clean up afterwards.

### Required Capabilities

#### 1.1 Install Plugin

**Purpose**: Install a plugin from a marketplace directory into the Claude Code instance.

**API Specification**:
```python
def install_plugin(
    plugin_name: str,
    marketplace_path: str,
    force_reinstall: bool = False
) -> PluginInstallResult:
    """
    Install plugin from marketplace.

    Args:
        plugin_name: Plugin identifier (e.g., "agent-loop")
        marketplace_path: Absolute path to marketplace root (containing .claude-plugin/marketplace.json)
        force_reinstall: If True, reinstall even if already installed

    Returns:
        PluginInstallResult with fields:
        - success: bool
        - plugin_id: str (unique identifier for this installation)
        - status: PluginStatus (loading, loaded, error)
        - error: Optional[str] (error message if success=False)
        - agents_registered: List[str] (agent names registered by plugin)
        - commands_registered: List[str] (command names registered by plugin)
        - hooks_registered: List[str] (hook names registered by plugin)
        - mcp_servers_started: List[str] (MCP server names started by plugin)

    Raises:
        PluginNotFoundError: Plugin not found in marketplace
        PluginInvalidError: Plugin manifest is invalid
        InstallationError: Installation failed for other reasons
    """
    pass
```

**REST API Equivalent**:
```http
POST /api/v1/plugins/install
Content-Type: application/json

{
    "plugin_name": "agent-loop",
    "marketplace_path": "/Users/bmf/marketplace",
    "force_reinstall": false
}

Response 200:
{
    "success": true,
    "plugin_id": "agent-loop-20251107-abc123",
    "status": "loaded",
    "agents_registered": ["workflow-agent"],
    "commands_registered": ["/explore", "/plan", "/code", "/commit"],
    "hooks_registered": ["pre-commit", "post-code", "commit-msg"],
    "mcp_servers_started": []
}

Response 400:
{
    "success": false,
    "error": "Plugin manifest validation failed: missing agents field",
    "status": "error"
}
```

**Test Use Cases**:
- Install agent-loop before testing 4-stage workflow
- Install epti before testing TDD discipline
- Install visual-iteration before testing screenshot feedback
- Verify all plugin components registered correctly

---

#### 1.2 Uninstall Plugin

**Purpose**: Remove a plugin from Claude Code and clean up registered components.

**API Specification**:
```python
def uninstall_plugin(
    plugin_name: str,
    cleanup_config: bool = True
) -> PluginUninstallResult:
    """
    Uninstall plugin and clean up resources.

    Args:
        plugin_name: Plugin identifier to uninstall
        cleanup_config: If True, remove plugin configuration files

    Returns:
        PluginUninstallResult with fields:
        - success: bool
        - components_removed: Dict[str, int] (counts: agents, commands, hooks, mcp_servers)
        - error: Optional[str]

    Raises:
        PluginNotFoundError: Plugin is not currently installed
    """
    pass
```

**REST API Equivalent**:
```http
DELETE /api/v1/plugins/{plugin_name}?cleanup_config=true

Response 200:
{
    "success": true,
    "components_removed": {
        "agents": 1,
        "commands": 4,
        "hooks": 3,
        "mcp_servers": 0
    }
}
```

**Test Use Cases**:
- Clean up after each test to ensure isolation
- Test plugin uninstall/reinstall cycles
- Verify component deregistration

---

#### 1.3 List Plugins

**Purpose**: Query all currently installed plugins with their status.

**API Specification**:
```python
def list_plugins() -> List[PluginInfo]:
    """
    List all installed plugins.

    Returns:
        List of PluginInfo objects with fields:
        - plugin_name: str
        - plugin_id: str
        - status: PluginStatus (loading, loaded, error, unloading)
        - version: str
        - install_time: datetime
        - component_counts: Dict[str, int]
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/plugins

Response 200:
{
    "plugins": [
        {
            "plugin_name": "agent-loop",
            "plugin_id": "agent-loop-20251107-abc123",
            "status": "loaded",
            "version": "0.1.0",
            "install_time": "2025-11-07T10:30:00Z",
            "component_counts": {"agents": 1, "commands": 4, "hooks": 3}
        }
    ],
    "total": 1
}
```

**Test Use Cases**:
- Verify plugin installation succeeded
- Check plugin still loaded after operations
- Test multiple plugins installed simultaneously

---

#### 1.4 Get Plugin Status

**Purpose**: Get detailed status information about a specific plugin.

**API Specification**:
```python
def get_plugin_status(plugin_name: str) -> PluginStatus:
    """
    Get detailed status for specific plugin.

    Args:
        plugin_name: Plugin identifier

    Returns:
        PluginStatus with fields:
        - status: PluginState (loading, loaded, error, not_installed)
        - error_message: Optional[str]
        - agents: List[AgentInfo] (registered agents with metadata)
        - commands: List[CommandInfo] (registered commands with paths)
        - hooks: List[HookInfo] (registered hooks with configs)
        - mcp_servers: List[MCPServerInfo] (running MCP servers)
        - last_error: Optional[ErrorInfo] (if status=error)

    Raises:
        PluginNotFoundError: Plugin not found
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/plugins/{plugin_name}/status

Response 200:
{
    "status": "loaded",
    "agents": [
        {
            "name": "workflow-agent",
            "file": "agents/workflow-agent.md",
            "active": true
        }
    ],
    "commands": [
        {
            "name": "/explore",
            "file": "commands/explore.md",
            "available": true
        }
    ],
    "hooks": [
        {
            "name": "pre-commit",
            "event": "PreCommit",
            "handler": "hooks/pre-commit.sh",
            "active": true
        }
    ],
    "mcp_servers": [],
    "last_error": null
}
```

**Test Use Cases**:
- Verify all plugin components loaded
- Diagnose plugin loading failures
- Validate hook registration

---

## Category 2: Command Execution API

### Overview

The Command Execution API enables programmatic invocation of slash commands (like `/explore`, `/plan`) and retrieval of command responses. This is essential for testing plugin command functionality and agent guidance quality.

### Required Capabilities

#### 2.1 Execute Command

**Purpose**: Execute a slash command in the context of a conversation session.

**API Specification**:
```python
def execute_command(
    command: str,
    session_id: str,
    args: Optional[Dict[str, Any]] = None,
    wait_for_completion: bool = True,
    timeout_ms: int = 30000
) -> CommandExecutionResult:
    """
    Execute command in session context.

    Args:
        command: Command string (e.g., "/explore", "/plan add new feature")
        session_id: Active conversation session ID
        args: Optional command arguments (if command supports structured args)
        wait_for_completion: If True, block until command finishes; if False, return immediately
        timeout_ms: Maximum wait time in milliseconds

    Returns:
        CommandExecutionResult with fields:
        - execution_id: str (unique ID for this execution)
        - command: str (command that was executed)
        - status: CommandStatus (pending, running, completed, failed, timeout)
        - response: Optional[str] (command response/output if completed)
        - workflow_stage: Optional[str] (workflow stage after command, if applicable)
        - agent_mode: Optional[str] (agent mode after command)
        - tool_calls: List[ToolCall] (tools invoked during execution)
        - duration_ms: int (execution time)
        - error: Optional[str] (if status=failed)

    Raises:
        CommandNotFoundError: Command doesn't exist
        SessionNotFoundError: Session ID invalid
        CommandTimeoutError: Execution exceeded timeout
    """
    pass
```

**REST API Equivalent**:
```http
POST /api/v1/sessions/{session_id}/commands/execute
Content-Type: application/json

{
    "command": "/explore",
    "wait_for_completion": true,
    "timeout_ms": 30000
}

Response 200:
{
    "execution_id": "exec-abc123",
    "command": "/explore",
    "status": "completed",
    "response": "I'll systematically investigate the codebase using code-exploration skills...",
    "workflow_stage": "exploring",
    "agent_mode": "agent-loop-workflow",
    "tool_calls": [
        {"tool": "Read", "file": "src/main.py"},
        {"tool": "Glob", "pattern": "**/*.py"}
    ],
    "duration_ms": 5432
}
```

**Test Use Cases**:
- Test each plugin command (16 commands across 3 plugins)
- Verify command expansion works correctly
- Validate agent responses contain expected guidance
- Test workflow stage transitions

---

#### 2.2 Get Command Output

**Purpose**: Retrieve output from a previously executed command (for async command execution).

**API Specification**:
```python
def get_command_output(execution_id: str) -> CommandOutput:
    """
    Get output from command execution.

    Args:
        execution_id: Execution ID from execute_command()

    Returns:
        CommandOutput with fields:
        - execution_id: str
        - status: CommandStatus
        - response: str
        - complete: bool
        - progress: Optional[float] (0.0-1.0 for long-running commands)

    Raises:
        ExecutionNotFoundError: Execution ID not found
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/commands/executions/{execution_id}

Response 200:
{
    "execution_id": "exec-abc123",
    "status": "completed",
    "response": "Planning complete. I've created a detailed implementation strategy...",
    "complete": true
}
```

**Test Use Cases**:
- Test async command execution pattern
- Verify long-running commands (visual-iteration /iterate-loop)
- Test command cancellation scenarios

---

#### 2.3 List Available Commands

**Purpose**: Query all commands available in the current Claude Code instance.

**API Specification**:
```python
def list_available_commands(
    session_id: Optional[str] = None,
    filter_by_plugin: Optional[str] = None
) -> List[CommandInfo]:
    """
    List available commands.

    Args:
        session_id: If provided, list commands available in this session context
        filter_by_plugin: If provided, only list commands from this plugin

    Returns:
        List of CommandInfo with fields:
        - name: str (command name, e.g., "/explore")
        - plugin: str (plugin providing the command)
        - description: str (command description from markdown)
        - file_path: str (path to command markdown file)
        - available: bool (whether command is currently available)
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/commands?plugin=agent-loop

Response 200:
{
    "commands": [
        {
            "name": "/explore",
            "plugin": "agent-loop",
            "description": "Systematically investigate codebase",
            "file_path": "plugins/agent-loop/commands/explore.md",
            "available": true
        },
        {
            "name": "/plan",
            "plugin": "agent-loop",
            "description": "Create structured implementation plan",
            "file_path": "plugins/agent-loop/commands/plan.md",
            "available": true
        }
    ],
    "total": 4
}
```

**Test Use Cases**:
- Verify plugin commands registered correctly
- Test command availability after plugin installation
- Validate command discovery

---

#### 2.4 Verify Command Expansion

**Purpose**: Test if a command string is valid and can be expanded.

**API Specification**:
```python
def verify_command_expansion(
    command: str,
    session_id: Optional[str] = None
) -> CommandVerificationResult:
    """
    Verify command is valid and can be executed.

    Args:
        command: Command string to verify
        session_id: Optional session for context-sensitive verification

    Returns:
        CommandVerificationResult with fields:
        - valid: bool
        - command_name: str (parsed command name)
        - plugin: Optional[str] (plugin providing command)
        - available: bool (whether command can be executed now)
        - reason: Optional[str] (if not available, why not)
    """
    pass
```

**REST API Equivalent**:
```http
POST /api/v1/commands/verify
Content-Type: application/json

{
    "command": "/explore the database layer"
}

Response 200:
{
    "valid": true,
    "command_name": "/explore",
    "plugin": "agent-loop",
    "available": true
}
```

**Test Use Cases**:
- Test command validation before execution
- Verify invalid commands rejected
- Test command availability logic

---

## Category 3: Conversation Simulation API

### Overview

The Conversation Simulation API enables programmatic management of multi-turn conversations with Claude Code. This is the foundation for testing agent behaviors, workflow progressions, and complex multi-stage interactions.

### Required Capabilities

#### 3.1 Start Conversation

**Purpose**: Initialize a new conversation session for testing.

**API Specification**:
```python
def start_conversation(
    config: Optional[ConversationConfig] = None
) -> ConversationSession:
    """
    Start new conversation session.

    Args:
        config: Optional configuration with fields:
            - agent_mode: Optional[str] (specific agent to use)
            - working_directory: Optional[str] (cwd for session)
            - plugins: Optional[List[str]] (restrict to specific plugins)
            - context_files: Optional[List[str]] (files to include in context)

    Returns:
        ConversationSession with fields:
        - session_id: str (unique session identifier)
        - created_at: datetime
        - agent_mode: str (active agent)
        - working_directory: str
        - plugins_active: List[str]
    """
    pass
```

**REST API Equivalent**:
```http
POST /api/v1/sessions/start
Content-Type: application/json

{
    "config": {
        "working_directory": "/tmp/test-project",
        "plugins": ["agent-loop"]
    }
}

Response 200:
{
    "session_id": "session-abc123",
    "created_at": "2025-11-07T10:30:00Z",
    "agent_mode": "workflow-agent",
    "working_directory": "/tmp/test-project",
    "plugins_active": ["agent-loop"]
}
```

**Test Use Cases**:
- Create isolated session for each test
- Test session configuration options
- Verify plugin context loaded correctly

---

#### 3.2 Send Prompt

**Purpose**: Send a user prompt to Claude Code and receive response asynchronously.

**API Specification**:
```python
def send_prompt(
    prompt: str,
    session_id: str,
    wait_for_response: bool = True,
    timeout_ms: int = 60000
) -> PromptResponse:
    """
    Send user prompt to Claude Code.

    Args:
        prompt: User message text
        session_id: Active session ID
        wait_for_response: If True, block until response ready
        timeout_ms: Maximum wait time

    Returns:
        PromptResponse with fields:
        - response_id: str (unique ID for this response)
        - prompt: str (user prompt sent)
        - status: ResponseStatus (pending, streaming, complete, error)
        - response_text: Optional[str] (if complete)
        - tool_calls: List[ToolCall] (tools used)
        - agent_mode: str (agent that responded)
        - workflow_stage: Optional[str]

    Raises:
        SessionNotFoundError: Invalid session ID
        PromptTimeoutError: Response not ready within timeout
    """
    pass
```

**REST API Equivalent**:
```http
POST /api/v1/sessions/{session_id}/prompts
Content-Type: application/json

{
    "prompt": "explore the database layer",
    "wait_for_response": true,
    "timeout_ms": 60000
}

Response 200:
{
    "response_id": "resp-abc123",
    "prompt": "explore the database layer",
    "status": "complete",
    "response_text": "I'll systematically explore the database layer...",
    "tool_calls": [
        {"tool": "Glob", "pattern": "**/models/*.py"},
        {"tool": "Read", "file": "src/models/user.py"}
    ],
    "agent_mode": "workflow-agent",
    "workflow_stage": "exploring"
}
```

**Test Use Cases**:
- Test natural language prompt handling
- Verify agent interprets prompts correctly
- Test multi-turn conversation flows

---

#### 3.3 Get Response

**Purpose**: Retrieve a previously sent prompt's response (for async pattern).

**API Specification**:
```python
def get_response(response_id: str) -> PromptResponse:
    """
    Get response by ID.

    Args:
        response_id: Response ID from send_prompt()

    Returns:
        PromptResponse (same structure as send_prompt return value)

    Raises:
        ResponseNotFoundError: Invalid response ID
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/responses/{response_id}

Response 200:
{
    "response_id": "resp-abc123",
    "status": "complete",
    "response_text": "Exploration complete...",
    "tool_calls": [...],
    "agent_mode": "workflow-agent"
}
```

**Test Use Cases**:
- Test async conversation pattern
- Handle long-running agent operations
- Test response streaming

---

#### 3.4 Get Conversation History

**Purpose**: Retrieve the full conversation history for a session.

**API Specification**:
```python
def get_conversation_history(
    session_id: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> ConversationHistory:
    """
    Get conversation history.

    Args:
        session_id: Session ID
        limit: Maximum number of turns to return
        offset: Skip first N turns (for pagination)

    Returns:
        ConversationHistory with fields:
        - session_id: str
        - turns: List[ConversationTurn]
            - turn_number: int
            - role: str ("user" | "assistant")
            - content: str
            - tool_calls: List[ToolCall]
            - timestamp: datetime
            - workflow_stage: Optional[str]
        - total_turns: int

    Raises:
        SessionNotFoundError: Invalid session ID
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/sessions/{session_id}/history?limit=10

Response 200:
{
    "session_id": "session-abc123",
    "turns": [
        {
            "turn_number": 1,
            "role": "user",
            "content": "/explore",
            "timestamp": "2025-11-07T10:30:00Z"
        },
        {
            "turn_number": 2,
            "role": "assistant",
            "content": "I'll systematically investigate...",
            "tool_calls": [...],
            "timestamp": "2025-11-07T10:30:05Z",
            "workflow_stage": "exploring"
        }
    ],
    "total_turns": 2
}
```

**Test Use Cases**:
- Verify conversation state persists
- Test conversation replay
- Debug test failures by reviewing history

---

#### 3.5 End Conversation

**Purpose**: Terminate a conversation session and clean up resources.

**API Specification**:
```python
def end_conversation(
    session_id: str,
    save_history: bool = True
) -> ConversationEndResult:
    """
    End conversation session.

    Args:
        session_id: Session to terminate
        save_history: If True, preserve history for later retrieval

    Returns:
        ConversationEndResult with fields:
        - session_id: str
        - ended_at: datetime
        - total_turns: int
        - history_saved: bool
        - history_path: Optional[str] (if save_history=True)

    Raises:
        SessionNotFoundError: Invalid session ID
    """
    pass
```

**REST API Equivalent**:
```http
DELETE /api/v1/sessions/{session_id}?save_history=true

Response 200:
{
    "session_id": "session-abc123",
    "ended_at": "2025-11-07T10:35:00Z",
    "total_turns": 8,
    "history_saved": true,
    "history_path": "/tmp/claude-sessions/session-abc123.json"
}
```

**Test Use Cases**:
- Clean up after each test
- Test session isolation
- Verify history persistence

---

## Category 4: Agent State Inspection API

### Overview

The Agent State Inspection API provides visibility into Claude Code's internal state during conversations. This enables testing of workflow transitions, agent mode changes, and contextual behavior - critical for validating agent-loop's 4-stage cycle and epti's TDD workflow enforcement.

### Required Capabilities

#### 4.1 Get Agent Mode

**Purpose**: Query the currently active agent in a session.

**API Specification**:
```python
def get_agent_mode(session_id: str) -> AgentModeInfo:
    """
    Get active agent information.

    Args:
        session_id: Session ID

    Returns:
        AgentModeInfo with fields:
        - agent_name: str (e.g., "workflow-agent")
        - plugin: str (plugin providing agent)
        - mode_description: str
        - active_since: datetime
        - mode_context: Dict[str, Any] (agent-specific context)

    Raises:
        SessionNotFoundError: Invalid session ID
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/sessions/{session_id}/agent/mode

Response 200:
{
    "agent_name": "workflow-agent",
    "plugin": "agent-loop",
    "mode_description": "4-stage software engineering workflow",
    "active_since": "2025-11-07T10:30:00Z",
    "mode_context": {
        "current_stage": "exploring",
        "stages_completed": ["idle"]
    }
}
```

**Test Use Cases**:
- Verify correct agent activated after plugin installation
- Test agent mode transitions
- Validate plugin-specific agent context

---

#### 4.2 Get Agent Guidance

**Purpose**: Retrieve the current agent's guidance/instructions that are active in the session.

**API Specification**:
```python
def get_agent_guidance(session_id: str) -> AgentGuidance:
    """
    Get active agent guidance.

    Args:
        session_id: Session ID

    Returns:
        AgentGuidance with fields:
        - agent_name: str
        - guidance_text: str (current agent instructions)
        - guidance_source: str (file path to agent markdown)
        - skills_available: List[str] (skills agent can invoke)
        - commands_available: List[str] (commands agent suggests)
        - workflow_stage: Optional[str]

    Raises:
        SessionNotFoundError: Invalid session ID
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/sessions/{session_id}/agent/guidance

Response 200:
{
    "agent_name": "workflow-agent",
    "guidance_text": "You are in the EXPLORE stage...",
    "guidance_source": "plugins/agent-loop/agents/workflow-agent.md",
    "skills_available": ["code-exploration", "verification"],
    "commands_available": ["/plan", "/code"],
    "workflow_stage": "exploring"
}
```

**Test Use Cases**:
- Verify agent provides appropriate guidance for stage
- Test skill availability
- Validate command suggestions

---

#### 4.3 Get Workflow Stage

**Purpose**: Query the current workflow stage for workflow-oriented agents (agent-loop, epti).

**API Specification**:
```python
def get_workflow_stage(session_id: str) -> WorkflowStageInfo:
    """
    Get current workflow stage.

    Args:
        session_id: Session ID

    Returns:
        WorkflowStageInfo with fields:
        - stage: str (e.g., "exploring", "planning", "coding")
        - stage_description: str
        - allowed_transitions: List[str] (valid next stages)
        - stage_entry_time: datetime
        - stage_actions_completed: List[str]
        - stage_actions_remaining: List[str]

    Raises:
        SessionNotFoundError: Invalid session ID
        NoWorkflowError: Agent doesn't use workflow stages
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/sessions/{session_id}/workflow/stage

Response 200:
{
    "stage": "exploring",
    "stage_description": "Systematic codebase investigation",
    "allowed_transitions": ["planning"],
    "stage_entry_time": "2025-11-07T10:30:05Z",
    "stage_actions_completed": ["directory_scanned", "files_listed"],
    "stage_actions_remaining": ["read_key_files", "summarize_findings"]
}
```

**Test Use Cases**:
- Test workflow stage transitions (critical for agent-loop)
- Verify stage progression logic
- Validate TDD workflow enforcement (epti)

---

#### 4.4 Verify Agent Transition

**Purpose**: Check if agent correctly transitioned to expected workflow stage.

**API Specification**:
```python
def verify_agent_transition(
    session_id: str,
    expected_stage: str,
    from_stage: Optional[str] = None
) -> TransitionVerification:
    """
    Verify workflow stage transition.

    Args:
        session_id: Session ID
        expected_stage: Expected current stage
        from_stage: Optional expected previous stage

    Returns:
        TransitionVerification with fields:
        - valid: bool
        - actual_stage: str
        - expected_stage: str
        - transition_time: Optional[datetime]
        - transition_trigger: Optional[str] (what caused transition)

    Raises:
        SessionNotFoundError: Invalid session ID
    """
    pass
```

**REST API Equivalent**:
```http
POST /api/v1/sessions/{session_id}/workflow/verify-transition
Content-Type: application/json

{
    "expected_stage": "planning",
    "from_stage": "exploring"
}

Response 200:
{
    "valid": true,
    "actual_stage": "planning",
    "expected_stage": "planning",
    "transition_time": "2025-11-07T10:32:15Z",
    "transition_trigger": "user executed /plan command"
}
```

**Test Use Cases**:
- Validate workflow transition logic
- Test incorrect transition blocking
- Verify stage enforcement (epti TDD stages)

---

## Category 5: Hook Verification API

### Overview

The Hook Verification API enables testing of plugin-defined hooks that execute in response to Claude Code events. This is important for testing hook-based plugins like promptctl and validating hook execution in agent-loop and epti.

### Required Capabilities

#### 5.1 List Active Hooks

**Purpose**: Query all hooks currently registered in Claude Code.

**API Specification**:
```python
def list_active_hooks() -> List[HookInfo]:
    """
    List all registered hooks.

    Returns:
        List of HookInfo with fields:
        - hook_name: str
        - event: str (event type: PreToolUse, PostToolUse, Stop, etc.)
        - plugin: str (plugin that registered hook)
        - handler: str (handler script path)
        - enabled: bool
        - execution_count: int (times hook has executed)
        - last_execution: Optional[datetime]
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/hooks

Response 200:
{
    "hooks": [
        {
            "hook_name": "pre-commit",
            "event": "PreToolUse",
            "plugin": "agent-loop",
            "handler": "hooks/pre-commit.sh",
            "enabled": true,
            "execution_count": 5,
            "last_execution": "2025-11-07T10:35:00Z"
        }
    ],
    "total": 3
}
```

**Test Use Cases**:
- Verify hooks registered correctly after plugin install
- Test hook enable/disable
- Validate hook execution counts

---

#### 5.2 Trigger Hook

**Purpose**: Manually trigger a hook for testing purposes.

**API Specification**:
```python
def trigger_hook(
    hook_name: str,
    payload: Dict[str, Any],
    wait_for_completion: bool = True
) -> HookExecutionResult:
    """
    Manually trigger hook.

    Args:
        hook_name: Hook to trigger
        payload: Event payload matching hook's event type
        wait_for_completion: Block until hook finishes

    Returns:
        HookExecutionResult with fields:
        - execution_id: str
        - hook_name: str
        - status: HookStatus (running, success, failed, blocked)
        - output: Optional[str] (handler stdout)
        - error: Optional[str] (handler stderr if failed)
        - duration_ms: int
        - action_blocked: bool (if hook blocked the action)

    Raises:
        HookNotFoundError: Hook doesn't exist
    """
    pass
```

**REST API Equivalent**:
```http
POST /api/v1/hooks/{hook_name}/trigger
Content-Type: application/json

{
    "payload": {
        "tool": "Bash",
        "command": "git commit -m 'test'"
    },
    "wait_for_completion": true
}

Response 200:
{
    "execution_id": "hook-exec-abc123",
    "hook_name": "pre-commit",
    "status": "blocked",
    "output": "Error: No plan file found. Run /plan first.",
    "duration_ms": 125,
    "action_blocked": true
}
```

**Test Use Cases**:
- Test hook blocking logic (agent-loop pre-commit blocks without plan)
- Verify hook execution order
- Test hook payload handling

---

#### 5.3 Get Hook Execution Log

**Purpose**: Retrieve execution history for a specific hook.

**API Specification**:
```python
def get_hook_execution_log(
    hook_name: str,
    limit: int = 50
) -> List[HookExecution]:
    """
    Get hook execution history.

    Args:
        hook_name: Hook to query
        limit: Maximum number of executions to return

    Returns:
        List of HookExecution with fields:
        - execution_id: str
        - timestamp: datetime
        - event_payload: Dict[str, Any]
        - status: HookStatus
        - output: str
        - duration_ms: int
        - action_blocked: bool

    Raises:
        HookNotFoundError: Hook doesn't exist
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/hooks/{hook_name}/executions?limit=50

Response 200:
{
    "hook_name": "pre-commit",
    "executions": [
        {
            "execution_id": "hook-exec-abc123",
            "timestamp": "2025-11-07T10:35:00Z",
            "event_payload": {"tool": "Bash", "command": "git commit..."},
            "status": "blocked",
            "output": "Error: No plan file found",
            "duration_ms": 125,
            "action_blocked": true
        }
    ],
    "total": 1
}
```

**Test Use Cases**:
- Verify hook executed at expected times
- Debug hook failures
- Test hook execution order

---

#### 5.4 Verify Hook Blocked Action

**Purpose**: Confirm a hook successfully blocked an action.

**API Specification**:
```python
def verify_hook_blocked_action(
    action_id: str,
    hook_name: str
) -> HookBlockVerification:
    """
    Verify hook blocked specific action.

    Args:
        action_id: Action identifier to verify
        hook_name: Hook that should have blocked it

    Returns:
        HookBlockVerification with fields:
        - blocked: bool
        - hook_name: str
        - action_id: str
        - block_reason: str
        - block_time: datetime

    Raises:
        ActionNotFoundError: Action ID not found
    """
    pass
```

**REST API Equivalent**:
```http
GET /api/v1/hooks/{hook_name}/verifications/{action_id}

Response 200:
{
    "blocked": true,
    "hook_name": "pre-commit",
    "action_id": "action-abc123",
    "block_reason": "No plan file found",
    "block_time": "2025-11-07T10:35:00Z"
}
```

**Test Use Cases**:
- Test negative scenarios (hook blocks incorrect action)
- Verify hook enforcement logic
- Test hook blocking messages

---

## Alternative Approaches (If API Not Available)

### Fallback Strategy 1: Filesystem Scraping

If Claude Code API is never provided, partial testing may be possible by scraping Claude Code's filesystem artifacts:

**What Could Work**:
- **Session State**: If Claude Code persists session state to JSON/YAML files, tests could read these files to inspect conversation history and agent state
- **Plugin Registry**: If plugin installation updates a registry file, tests could verify plugin presence
- **Hook Execution Logs**: If hooks write execution logs, tests could parse these for verification

**Limitations**:
- Cannot install/uninstall plugins programmatically
- Cannot execute commands programmatically
- Cannot send prompts programmatically
- File formats must be stable and documented

**Viability**: 20% - requires extensive reverse engineering, fragile, breaks with Claude Code updates

---

### Fallback Strategy 2: Log Parsing

Parse Claude Code's debug logs to infer state:

**What Could Work**:
- Command execution detection via log lines
- Hook execution verification via log entries
- Plugin loading confirmation via logs
- Agent mode changes via logs

**Limitations**:
- No control over Claude Code behavior
- No programmatic command execution
- Log format must remain stable
- Very fragile

**Viability**: 10% - extremely fragile, infeas ible for comprehensive testing

---

### Fallback Strategy 3: Manual Testing Only

If no programmatic API and fallbacks are infeasible:

**Approach**:
- Maintain manual test plan (PLAN-path-a-revised-2025-11-07-014830.md)
- Document manual test procedures
- Run manual tests before each release
- Accept lack of automation

**Limitations**:
- No automation
- Slow feedback loop
- High manual effort
- No CI/CD integration

**Viability**: 100% - always viable, but defeats purpose of E2E test harness

---

## Priority Levels

### Critical (Must-Have for Viable Testing)

**Without these, automation is impossible:**
- Category 1: Plugin Management (all 4 tools) - Install/uninstall plugins
- Category 2: Command Execution (tools 2.1, 2.3) - Execute commands, list commands
- Category 3: Conversation Simulation (tools 3.1, 3.2, 3.5) - Start session, send prompt, end session

**Minimum Viable API**: Categories 1-3 with 11 endpoints

### Important (Enable Rich Testing)

**These significantly improve test quality:**
- Category 2: Command Execution (tools 2.2, 2.4) - Async patterns, command verification
- Category 3: Conversation Simulation (tools 3.3, 3.4) - Response retrieval, history access
- Category 4: Agent State Inspection (all 4 tools) - Workflow validation, agent mode checking

**Enhanced Testing API**: Critical + Important = 19 endpoints

### Nice-to-Have (Specialized Testing)

**These enable advanced test scenarios:**
- Category 5: Hook Verification (all 4 tools) - Hook testing, execution verification

**Complete Testing API**: All 5 categories = 20 endpoints

---

## Implementation Recommendations for Anthropic

### Design Principles

If Anthropic chooses to implement this API, we recommend:

1. **RESTful Design**: HTTP REST API is most accessible for test tooling
2. **Async-First**: Long-running operations (command execution, prompt responses) should support async patterns
3. **Rich Responses**: Include metadata (workflow stage, tool calls, timing) in responses
4. **Clear Errors**: Structured error responses with actionable messages
5. **Versioned API**: `/api/v1/` prefix to allow evolution
6. **Authentication**: API key or token-based auth for security
7. **Rate Limiting**: Reasonable rate limits for test scenarios
8. **Documentation**: OpenAPI/Swagger spec for API reference

### Phased Rollout

Suggested implementation phases:

**Phase 1: MVP** (11 endpoints, ~2-4 weeks effort)
- Category 1: Plugin Management (4 endpoints)
- Category 2: Command Execution (2 endpoints: execute, list)
- Category 3: Conversation Simulation (3 endpoints: start, send, end)
- Category 4: Agent State (2 endpoints: get mode, get stage)

**Phase 2: Enhanced** (8 more endpoints, ~2-3 weeks effort)
- Category 2: Complete (2 more endpoints)
- Category 3: Complete (2 more endpoints)
- Category 4: Complete (2 more endpoints)
- Category 5: Partial (2 endpoints: list hooks, trigger hook)

**Phase 3: Complete** (2 more endpoints, ~1 week effort)
- Category 5: Complete (2 more endpoints)

**Total Estimated Effort**: 5-8 weeks for full API implementation

---

## Conclusion

This specification defines the minimum Claude Code API required for automated E2E testing of plugins. The API spans 5 categories with 20 tools, enabling comprehensive testing of plugin functionality, agent behaviors, and workflow progressions.

**Current Status**: API does not exist, blocking Phase 2 test harness implementation.

**Next Steps**:
1. Share this specification with Anthropic engineering team
2. Advocate for programmatic API development
3. Monitor for API availability announcements
4. Begin Phase 2 implementation when API is released

**Fallback**: If API never materializes, accept manual testing only (Path A) as permanent solution.

For architecture details, see `ARCHITECTURE.md`.
For conversation patterns, see `CONVERSATION_SIMULATION.md`.
For Docker configuration, see `DOCKER_SETUP.md`.
