"""Action implementations for hook handlers."""

import os
import subprocess
from typing import Any, Dict, List
from .context import Context


class Action:
    """Base action class."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize action with configuration.

        Args:
            config: Action configuration dictionary
        """
        self.config = config

    def execute(self, context: Context) -> Dict[str, Any]:
        """Execute the action.

        Args:
            context: Execution context

        Returns:
            Result dictionary

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Action subclasses must implement execute()")


class PromptAction(Action):
    """Send a prompt to Claude."""

    def execute(self, context: Context) -> Dict[str, Any]:
        """Execute prompt action.

        Args:
            context: Execution context

        Returns:
            Result with rendered prompt
        """
        template = self.config.get("template", "")
        rendered = context.render(template)

        return {
            "type": "prompt",
            "prompt": rendered
        }


class CommandAction(Action):
    """Execute a shell command."""

    def execute(self, context: Context) -> Dict[str, Any]:
        """Execute command action.

        Args:
            context: Execution context

        Returns:
            Result with exit code and output
        """
        script = self.config.get("script", "")
        rendered_script = context.render(script)

        # Execute command
        result = subprocess.run(
            rendered_script,
            shell=True,
            capture_output=True,
            text=True
        )

        # Capture output to state if requested
        if "capture" in self.config:
            key = self.config["capture"]
            context.set_state(key, result.stdout.strip())

        return {
            "type": "command",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }


class GitAction(Action):
    """Perform git operations."""

    def execute(self, context: Context) -> Dict[str, Any]:
        """Execute git action.

        Args:
            context: Execution context

        Returns:
            Result with operation details
        """
        operation = self.config.get("operation")
        result = {
            "type": "git",
            "operation": operation
        }

        if operation == "stage":
            # Render file patterns
            files = self.config.get("files", [])
            rendered_files = [context.render(f) for f in files]
            result["files"] = rendered_files

            # Execute: git add <files>
            for file in rendered_files:
                subprocess.run(["git", "add", file], check=False)

        elif operation == "commit":
            # Render commit message
            message = context.render(self.config.get("message", ""))
            result["message"] = message

            # Execute: git commit -m <message>
            subprocess.run(["git", "commit", "-m", message], check=False)

        return result


class ValidateAction(Action):
    """Run validation checks."""

    def execute(self, context: Context) -> Dict[str, Any]:
        """Execute validation action.

        Args:
            context: Execution context

        Returns:
            Result with pass/fail status
        """
        checks = self.config.get("checks", [])
        all_passed = True

        for check in checks:
            check_type = check.get("type")

            if check_type == "file_exists":
                path = context.render(check.get("path", ""))
                if not os.path.exists(path):
                    all_passed = False

            elif check_type == "command_succeeds":
                command = context.render(check.get("command", ""))
                result = subprocess.run(command, shell=True, capture_output=True)
                if result.returncode != 0:
                    all_passed = False

        return {
            "type": "validate",
            "passed": all_passed
        }


class ConditionalAction(Action):
    """Execute actions conditionally."""

    def execute(self, context: Context) -> Dict[str, Any]:
        """Execute conditional action.

        Args:
            context: Execution context

        Returns:
            Result with condition outcome and branch executed
        """
        condition = self.config.get("condition", "")
        rendered_condition = context.render(condition)

        # Simple condition evaluation
        # For now, just check string equality patterns
        condition_met = self._evaluate_condition(rendered_condition)

        result = {
            "type": "conditional",
            "condition_met": condition_met,
            "branch_executed": None
        }

        if condition_met:
            then_actions = self.config.get("then", [])
            if then_actions:
                result["branch_executed"] = "then"
                # Would execute actions here in full implementation
        else:
            else_actions = self.config.get("else", [])
            if else_actions:
                result["branch_executed"] = "else"
                # Would execute actions here in full implementation

        return result

    def _evaluate_condition(self, condition: str) -> bool:
        """Evaluate a simple condition.

        Args:
            condition: Condition string (e.g., "value == 'expected'")

        Returns:
            True if condition is met
        """
        # Simple evaluation for now - just check equality
        if " == " in condition:
            left, right = condition.split(" == ", 1)
            left = left.strip().strip("'\"")
            right = right.strip().strip("'\"")
            return left == right

        return False
