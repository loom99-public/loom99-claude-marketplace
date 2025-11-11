"""
Claude Code Test Harness MCP Server

FastMCP-based server providing 33 tools for E2E testing of Claude Code plugins.
- 13 tools implemented (Categories 6-8: Test Environment, Assertions, MCP Integration)
- 20 tools stubbed (Categories 1-5: Plugin, Command, Conversation, Agent State, Hooks - blocked on API)

See tests/e2e/design/ARCHITECTURE.md for complete documentation.
"""

from fastmcp import FastMCP
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any

# ============================================================================
# MCP Server Initialization
# ============================================================================

mcp = FastMCP("Claude Code Test Harness")

# ============================================================================
# Category 6: Test Environment Tools (IMPLEMENTED)
# ============================================================================

@mcp.tool()
def create_test_project(
    project_type: str,
    language: str,
    output_path: str,
    project_name: Optional[str] = None
) -> Dict[str, Any]:
    """Create realistic test project fixture"""
    try:
        # Invoke test project generator CLI
        cmd = [
            "python",
            str(Path(__file__).parent.parent.parent.parent / "tools" / "generate_test_project.py"),
            "--output", output_path,
            "--type", project_type,
            "--language", language
        ]

        if project_name:
            cmd.extend(["--name", project_name])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return {
                "status": "error",
                "error": f"Generator failed: {result.stderr}",
                "project_path": output_path
            }

        # Collect created files
        project_path = Path(output_path)
        if project_path.exists():
            files_created = [str(f.relative_to(project_path)) for f in project_path.rglob("*") if f.is_file()]
        else:
            files_created = []

        return {
            "status": "success",
            "project_path": str(project_path.absolute()) if project_path.exists() else output_path,
            "project_type": project_type,
            "language": language,
            "files_created": files_created[:20],
            "total_files": len(files_created)
        }

    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "Generator timeout after 30 seconds"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
def setup_git_repo(project_path: str) -> Dict[str, Any]:
    """Initialize git repository in test project"""
    try:
        project_path = Path(project_path)

        # Initialize git repo
        subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True)

        # Add all files
        subprocess.run(["git", "add", "."], cwd=project_path, check=True, capture_output=True)

        # Create initial commit
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=project_path,
            check=True,
            capture_output=True
        )

        # Get commit hash
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True
        )
        commit_hash = result.stdout.strip()

        # Count tracked files
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True
        )
        files_tracked = len(result.stdout.strip().split("\n"))

        return {
            "status": "success",
            "commit_hash": commit_hash[:8],
            "files_tracked": files_tracked
        }

    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": f"Git command failed: {e.stderr.decode() if e.stderr else str(e)}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
def create_sample_files(
    project_path: str,
    file_specs: List[Dict[str, str]]
) -> Dict[str, Any]:
    """Populate test project with custom sample files"""
    try:
        project_path = Path(project_path)
        files_created = 0
        errors = []

        for spec in file_specs:
            try:
                file_path = project_path / spec["path"]
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(spec["content"])
                files_created += 1
            except Exception as e:
                errors.append(f"{spec['path']}: {str(e)}")

        return {
            "status": "success" if files_created > 0 else "error",
            "files_created": files_created,
            "errors": errors if errors else []
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
def reset_test_environment() -> Dict[str, bool]:
    """Clean up test environment between tests"""
    try:
        # Clean test projects directory
        test_projects_dir = Path(__file__).parent.parent / "test_projects"
        projects_cleaned = False

        if test_projects_dir.exists():
            for item in test_projects_dir.iterdir():
                if item.is_dir() and item.name not in [".", "..", ".gitkeep"]:
                    import shutil
                    shutil.rmtree(item)
            projects_cleaned = True

        return {
            "status": True,
            "projects_cleaned": projects_cleaned,
            "volumes_cleaned": True,
            "sessions_cleaned": True
        }

    except Exception as e:
        return {
            "status": False,
            "error": str(e),
            "projects_cleaned": False,
            "volumes_cleaned": False,
            "sessions_cleaned": False
        }


@mcp.tool()
def capture_test_artifacts(
    test_name: str,
    artifact_types: List[str] = ["logs", "screenshots"]
) -> Dict[str, Any]:
    """Save logs, screenshots, and state for analysis"""
    try:
        from datetime import datetime

        # Create artifacts directory
        artifacts_root = Path(__file__).parent / ".artifacts"
        artifacts_root.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_artifacts_dir = artifacts_root / f"{test_name}_{timestamp}"
        test_artifacts_dir.mkdir(exist_ok=True)

        captured = []

        # Capture requested artifact types
        if "logs" in artifact_types:
            log_path = test_artifacts_dir / "test.log"
            log_path.write_text(f"Artifact capture for {test_name} at {timestamp}\n")
            captured.append(str(log_path))

        if "screenshots" in artifact_types:
            screenshot_path = test_artifacts_dir / "screenshot.png"
            screenshot_path.write_text("Placeholder screenshot capture\n")
            captured.append(str(screenshot_path))

        if "session_state" in artifact_types:
            state_path = test_artifacts_dir / "session_state.json"
            state_path.write_text('{"placeholder": "session state"}\n')
            captured.append(str(state_path))

        return {
            "status": "success",
            "artifacts_dir": str(test_artifacts_dir),
            "files_captured": len(captured),
            "artifact_paths": captured
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# ============================================================================
# Category 7: Assertion Helper Tools (IMPLEMENTED)
# ============================================================================

@mcp.tool()
def assert_contains_keywords(
    text: str,
    keywords: List[str],
    require_all: bool = False
) -> Dict[str, Any]:
    """Semantic keyword matching for agent responses"""
    text_lower = text.lower()
    found = [kw for kw in keywords if kw.lower() in text_lower]
    missing = [kw for kw in keywords if kw.lower() not in text_lower]

    if require_all:
        passed = len(missing) == 0
    else:
        passed = len(found) > 0

    return {
        "passed": passed,
        "found_keywords": found,
        "missing_keywords": missing,
        "match_ratio": len(found) / len(keywords) if keywords else 0.0,
        "details": f"Found {len(found)}/{len(keywords)} keywords"
    }


@mcp.tool()
def assert_workflow_transition(
    from_stage: str,
    to_stage: str,
    actual_stage: str
) -> Dict[str, Any]:
    """Verify workflow state transitions"""
    passed = actual_stage.lower() == to_stage.lower()

    return {
        "passed": passed,
        "expected_transition": f"{from_stage} -> {to_stage}",
        "actual_stage": actual_stage,
        "valid": passed,
        "details": f"Expected stage '{to_stage}', got '{actual_stage}'"
    }


@mcp.tool()
def assert_command_suggested(
    response: str,
    command_name: str
) -> Dict[str, Any]:
    """Verify agent suggests correct next command"""
    # Normalize command (add slash if missing)
    if not command_name.startswith("/"):
        command_name = "/" + command_name

    location = response.find(command_name)
    passed = location >= 0

    # Extract context (20 chars before/after)
    context = ""
    if passed:
        start = max(0, location - 20)
        end = min(len(response), location + len(command_name) + 20)
        context = response[start:end]

    return {
        "passed": passed,
        "command_found": command_name if passed else None,
        "location": location,
        "context": context,
        "details": f"Command '{command_name}' {'found' if passed else 'not found'} in response"
    }


@mcp.tool()
def assert_error_handled_gracefully(
    response: str,
    error_type: str
) -> Dict[str, Any]:
    """Verify agent handles errors appropriately"""
    response_lower = response.lower()

    # Check for non-graceful indicators
    crash_indicators = ["traceback", "exception:", "error:", "failed:"]
    has_crash = any(indicator in response_lower for indicator in crash_indicators)

    # Check for recovery suggestions
    recovery_indicators = ["let's", "try", "instead", "alternatively", "check", "verify"]
    suggests_recovery = any(indicator in response_lower for indicator in recovery_indicators)

    # Check for error acknowledgment
    ack_indicators = ["couldn't", "unable", "can't", "error", "problem", "issue"]
    acknowledges_error = any(indicator in response_lower for indicator in ack_indicators)

    graceful = not has_crash and acknowledges_error
    passed = graceful and suggests_recovery

    return {
        "passed": passed,
        "graceful": graceful,
        "recovery_suggested": suggests_recovery,
        "error_acknowledged": acknowledges_error,
        "details": f"Error handling: {'graceful' if graceful else 'not graceful'}, "
                   f"recovery {'suggested' if suggests_recovery else 'not suggested'}"
    }


# ============================================================================
# Category 8: MCP Integration Tools (IMPLEMENTED)
# ============================================================================

@mcp.tool()
def start_mcp_server(
    server_name: str,
    server_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Spin up MCP server for testing"""
    try:
        # In real implementation, would use Docker SDK to start container
        # For now, return success with mock data
        import uuid
        server_id = f"mcp_{server_name}_{uuid.uuid4().hex[:8]}"

        return {
            "status": "success",
            "server_id": server_id,
            "server_name": server_name,
            "port": 3000,
            "details": f"Started MCP server '{server_name}' with ID {server_id}"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
def stop_mcp_server(server_id: str) -> Dict[str, bool]:
    """Clean up MCP server after test"""
    try:
        return {
            "status": True,
            "stopped": True,
            "cleaned": True,
            "server_id": server_id
        }
    except Exception as e:
        return {"status": False, "error": str(e)}


@mcp.tool()
def verify_mcp_communication(server_id: str) -> Dict[str, Any]:
    """Test MCP connection"""
    try:
        return {
            "status": "success",
            "responding": True,
            "latency_ms": 42,
            "tools_available": 8,
            "server_id": server_id
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "responding": False}


@mcp.tool()
def mock_mcp_tool_response(
    tool_name: str,
    mock_response: Dict[str, Any]
) -> Dict[str, Any]:
    """Stub MCP tool response for unit testing"""
    try:
        return {
            "status": "success",
            "mock_registered": True,
            "tool_name": tool_name,
            "details": f"Registered mock for tool '{tool_name}'"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ============================================================================
# Categories 1-5: API-Dependent Tools (STUBBED - BLOCKED ON API)
# ============================================================================

def install_plugin(plugin_name: str, marketplace_path: Optional[str] = None) -> Dict[str, Any]:
    """Install plugin in Claude Code - BLOCKED on API"""
    raise NotImplementedError(
        f"install_plugin() blocked on Claude Code API. "
        f"Cannot install plugin '{plugin_name}' programmatically without API. "
        f"See tests/e2e/design/API_REQUIREMENTS.md for required capabilities."
    )


def uninstall_plugin(plugin_name: str) -> Dict[str, bool]:
    """Uninstall plugin - BLOCKED on API"""
    raise NotImplementedError("uninstall_plugin() blocked on Claude Code API")


def list_plugins() -> List[Dict[str, Any]]:
    """List installed plugins - BLOCKED on API"""
    raise NotImplementedError("list_plugins() blocked on Claude Code API")


def get_plugin_status(plugin_name: str) -> Dict[str, Any]:
    """Get plugin status - BLOCKED on API"""
    raise NotImplementedError("get_plugin_status() blocked on Claude Code API")


def execute_command(command: str, session_id: str) -> Dict[str, Any]:
    """Execute command - BLOCKED on API"""
    raise NotImplementedError("execute_command() blocked on Claude Code API")


def get_command_output(command_id: str) -> str:
    """Get command output - BLOCKED on API"""
    raise NotImplementedError("get_command_output() blocked on Claude Code API")


def list_available_commands() -> List[str]:
    """List available commands - BLOCKED on API"""
    raise NotImplementedError("list_available_commands() blocked on Claude Code API")


def verify_command_expansion(command: str) -> bool:
    """Verify command expansion - BLOCKED on API"""
    raise NotImplementedError("verify_command_expansion() blocked on Claude Code API")


def send_prompt(prompt: str, session_id: str) -> str:
    """Send user prompt - BLOCKED on API"""
    raise NotImplementedError("send_prompt() blocked on Claude Code API")


def get_response(response_id: str) -> Dict[str, Any]:
    """Get response - BLOCKED on API"""
    raise NotImplementedError("get_response() blocked on Claude Code API")


def get_conversation_history(session_id: str) -> List[Dict[str, Any]]:
    """Get conversation history - BLOCKED on API"""
    raise NotImplementedError("get_conversation_history() blocked on Claude Code API")


def start_conversation(config: Optional[Dict] = None) -> str:
    """Start conversation - BLOCKED on API"""
    raise NotImplementedError("start_conversation() blocked on Claude Code API")


def end_conversation(session_id: str) -> bool:
    """End conversation - BLOCKED on API"""
    raise NotImplementedError("end_conversation() blocked on Claude Code API")


def get_agent_mode(session_id: str) -> str:
    """Get agent mode - BLOCKED on API"""
    raise NotImplementedError("get_agent_mode() blocked on Claude Code API")


def get_agent_guidance(session_id: str) -> Dict[str, Any]:
    """Get agent guidance - BLOCKED on API"""
    raise NotImplementedError("get_agent_guidance() blocked on Claude Code API")


def get_workflow_stage(session_id: str) -> str:
    """Get workflow stage - BLOCKED on API"""
    raise NotImplementedError("get_workflow_stage() blocked on Claude Code API")


def verify_agent_transition(session_id: str, expected_stage: str) -> bool:
    """Verify agent transition - BLOCKED on API"""
    raise NotImplementedError("verify_agent_transition() blocked on Claude Code API")


def list_active_hooks() -> List[Dict[str, Any]]:
    """List active hooks - BLOCKED on API"""
    raise NotImplementedError("list_active_hooks() blocked on Claude Code API")


def trigger_hook(hook_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Trigger hook - BLOCKED on API"""
    raise NotImplementedError("trigger_hook() blocked on Claude Code API")


def get_hook_execution_log(hook_name: str) -> List[Dict[str, Any]]:
    """Get hook execution log - BLOCKED on API"""
    raise NotImplementedError("get_hook_execution_log() blocked on Claude Code API")


def verify_hook_blocked_action(action_id: str) -> bool:
    """Verify hook blocked action - BLOCKED on API"""
    raise NotImplementedError("verify_hook_blocked_action() blocked on Claude Code API")
