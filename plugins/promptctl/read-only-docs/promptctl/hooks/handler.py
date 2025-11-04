"""Handler matching and execution engine."""

from typing import Dict, List, Any
from pathlib import Path

from .context import Context
from .actions import (
    Action,
    PromptAction,
    CommandAction,
    GitAction,
    ValidateAction,
    ConditionalAction,
)


class HandlerEngine:
    """Matches handlers and executes action chains."""

    # Map action types to action classes
    ACTION_REGISTRY = {
        "prompt": PromptAction,
        "command": CommandAction,
        "git": GitAction,
        "validate": ValidateAction,
        "conditional": ConditionalAction,
    }

    def __init__(self, config: Dict[str, Any]):
        """Initialize handler engine.

        Args:
            config: Configuration dictionary with handlers
        """
        self.config = config
        self.handlers = config.get("handlers", {})

    def match_handlers(self, hook_name: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find handlers that match this hook event.

        Args:
            hook_name: Name of the hook (e.g., "PostToolUse")
            payload: Hook payload data

        Returns:
            List of matching handler configs sorted by priority
        """
        matched = []

        for handler_name, handler_config in self.handlers.items():
            # Skip disabled handlers
            if not handler_config.get("enabled", True):
                continue

            # Check hook type
            if handler_config.get("hook") != hook_name:
                continue

            # Check match conditions
            match_config = handler_config.get("match", {})
            if not self._matches_conditions(payload, match_config):
                continue

            matched.append({
                "name": handler_name,
                "config": handler_config,
                "priority": handler_config.get("priority", 0)
            })

        # Sort by priority (highest first)
        matched.sort(key=lambda h: h["priority"], reverse=True)

        return matched

    def _matches_conditions(self, payload: Dict[str, Any], match_config: Dict[str, Any]) -> bool:
        """Check if payload matches handler conditions.

        Args:
            payload: Hook payload
            match_config: Handler match configuration

        Returns:
            True if all conditions match
        """
        # No match conditions = match all
        if not match_config:
            return True

        # Tool name matching
        if "tool" in match_config:
            tool_filter = match_config["tool"]
            tool_name = payload.get("tool", {}).get("name")

            if isinstance(tool_filter, list):
                if tool_name not in tool_filter:
                    return False
            elif tool_name != tool_filter:
                return False

        # File pattern matching
        if "file_pattern" in match_config:
            file_path = self._extract_file_path(payload)
            if not file_path:
                return False

            pattern = match_config["file_pattern"]
            if not Path(file_path).match(pattern):
                return False

        return True

    def _extract_file_path(self, payload: Dict[str, Any]) -> str:
        """Extract file path from payload.

        Args:
            payload: Hook payload

        Returns:
            File path or empty string
        """
        tool = payload.get("tool", {})
        tool_input = tool.get("input", {})
        return tool_input.get("file_path", "")

    def execute_handler(
        self,
        handler_name: str,
        hook_name: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a handler's action chain.

        Args:
            handler_name: Name of handler to execute
            hook_name: Hook name
            payload: Hook payload

        Returns:
            Execution result dictionary
        """
        handler_config = self.handlers.get(handler_name, {})
        actions = handler_config.get("actions", [])

        # Create execution context
        context = Context(payload)

        # Execute actions in sequence
        results = []
        for action_config in actions:
            try:
                action = self._create_action(action_config)
                result = action.execute(context)
                results.append({
                    "action": action_config.get("action"),
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "action": action_config.get("action"),
                    "status": "error",
                    "error": str(e)
                })
                # Stop on error by default
                break

        return {
            "handler": handler_name,
            "actions_executed": len(results),
            "results": results
        }

    def _create_action(self, config: Dict[str, Any]) -> Action:
        """Create action instance from configuration.

        Args:
            config: Action configuration

        Returns:
            Action instance

        Raises:
            ValueError: If action type unknown
        """
        action_type = config.get("action")
        action_class = self.ACTION_REGISTRY.get(action_type)

        if not action_class:
            raise ValueError(f"Unknown action type: {action_type}")

        return action_class(config)
