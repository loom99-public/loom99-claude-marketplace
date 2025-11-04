"""Context for hook execution with payload parsing and template rendering."""

from typing import Any, Dict, Optional


class Context:
    """Execution context for hook handlers."""

    def __init__(self, payload: Dict[str, Any]):
        """Initialize context with hook payload.

        Args:
            payload: JSON payload from Claude Code hook
        """
        self._payload = payload
        self._state: Dict[str, Any] = {}

    def get(self, path: str, default: Any = None) -> Any:
        """Get value from payload using dot notation.

        Args:
            path: Dot-separated path (e.g., "tool.input.file_path")
            default: Default value if path not found

        Returns:
            Value at path or default
        """
        parts = path.split('.')
        current = self._payload

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default

        return current

    def render(self, template: str) -> str:
        """Render template with variables from payload and state.

        Supports:
        - Simple: {variable}
        - Nested: {tool.name}
        - State: {state.key}

        Args:
            template: Template string with {variable} placeholders

        Returns:
            Rendered string
        """
        result = template

        # Replace payload variables
        result = self._replace_variables(result, self._payload, prefix="")

        # Replace state variables
        result = self._replace_variables(result, self._state, prefix="state.")

        return result

    def _replace_variables(self, text: str, data: Dict[str, Any], prefix: str) -> str:
        """Replace variables in text from data dict.

        Args:
            text: Text with {variable} placeholders
            data: Data dictionary
            prefix: Prefix for variable names (e.g., "state.")

        Returns:
            Text with variables replaced
        """
        result = text

        # Flatten nested dict for replacement
        flat = self._flatten_dict(data, parent_key=prefix.rstrip('.'))

        for key, value in flat.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))

        return result

    def _flatten_dict(self, data: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        """Flatten nested dictionary with dot notation keys.

        Args:
            data: Nested dictionary
            parent_key: Parent key prefix

        Returns:
            Flattened dictionary
        """
        items = []

        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key

            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, new_key).items())
            else:
                items.append((new_key, value))

        return dict(items)

    def set_state(self, key: str, value: Any) -> None:
        """Set state value.

        Args:
            key: State key
            value: Value to store
        """
        self._state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get state value.

        Args:
            key: State key
            default: Default if key not found

        Returns:
            State value or default
        """
        return self._state.get(key, default)
