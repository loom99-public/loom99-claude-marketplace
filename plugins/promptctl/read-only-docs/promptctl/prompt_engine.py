"""Prompt execution engine - handles loading and selecting prompts with minimal complexity."""

import json
import logging
import os
import random
import subprocess
from typing import Dict, List, Optional, Tuple
from importlib import resources


class PromptEngine:
    """Simple prompt execution engine designed for expansion."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.current_series = None
        self.series_index = 0

    def get_current_directory(self, session_path: Optional[str] = None) -> str:
        """Get current working directory with fallback."""
        if session_path:
            return session_path
        return os.getcwd()

    def find_config_file(self, cwd: str) -> Optional[str]:
        """Find .promptctl.yaml in current directory."""
        yaml_path = os.path.join(cwd, ".promptctl.yaml")
        return yaml_path if os.path.exists(yaml_path) else None

    def get_schema_path(self) -> str:
        """Get path to CUE schema file."""
        try:
            schema_files = resources.files('promptctl.schemas')
            schema_path = schema_files / 'prompt_config.schema.cue'
            return str(schema_path)
        except Exception as e:
            raise RuntimeError(f"Cannot locate CUE schema: {e}")

    def validate_and_convert_config(self, yaml_path: str) -> str:
        """Use CUE to validate YAML and generate JSON."""
        # Check if CUE is available
        try:
            subprocess.run(["cue", "version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("CUE is required for config validation but not available")

        # Get paths
        config_dir = os.path.dirname(yaml_path)
        json_path = os.path.join(config_dir, ".promptctl.json")
        schema_path = self.get_schema_path()

        if not os.path.exists(schema_path):
            raise RuntimeError(f"CUE schema not found at {schema_path}")

        # Run CUE validation and export
        cmd = [
            "cue", "export",
            "--outfile", json_path,
            schema_path, yaml_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            self.logger.info(f"Config validated and converted to {json_path}")
            return json_path
        else:
            raise RuntimeError(f"CUE validation failed: {result.stderr}")

    def load_yaml_config(self, yaml_path: str) -> Dict:
        """Load YAML config directly."""
        try:
            import yaml
            with open(yaml_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load YAML config: {e}")

    def load_json_config(self, json_path: str) -> Dict:
        """Load JSON config file."""
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load JSON config: {e}")

    def load_project_config(self, session_path: Optional[str] = None) -> Optional[Dict]:
        """Load project configuration from .promptctl.yaml/.promptctl.json."""
        cwd = self.get_current_directory(session_path)
        self.logger.info(f"Looking for config in: {cwd}")

        # Look for YAML config file
        yaml_path = self.find_config_file(cwd)
        if not yaml_path:
            self.logger.info("No .promptctl.yaml found")
            return None

        # Always validate with CUE first
        try:
            json_path = self.validate_and_convert_config(yaml_path)
            config = self.load_json_config(json_path)
            self.logger.info(f"Loaded validated config from {json_path}")
            return config
        except RuntimeError as e:
            self.logger.error(f"Config validation failed: {e}")
            # If validation fails, load YAML directly but log the issue
            self.logger.warning("Loading unvalidated YAML config as fallback")
            try:
                config = self.load_yaml_config(yaml_path)
                self.logger.info(f"Loaded unvalidated config from {yaml_path}")
                return config
            except RuntimeError as yaml_error:
                self.logger.error(f"Failed to load config: {yaml_error}")
                return None

    def get_default_prompts(self) -> List[str]:
        """Get default prompt list."""
        return [
            "actually run the software end to end and then make a git commit",
            "continue the loop"
        ]

    def get_next_prompt(self, session_path: Optional[str] = None) -> str:
        """Get the next prompt to execute."""
        # Load config fresh each time (no caching/reloading needed)
        config = self.load_project_config(session_path)
        prompts = config.get("prompts") if config else None

        # Use default prompts if no project config
        if not prompts:
            prompts = self.get_default_prompts()

        # Select random prompt
        selected_prompt = random.choice(prompts)
        self.logger.info(f"Selected prompt: {selected_prompt}")
        return selected_prompt

    def reset_series(self):
        """Reset the current prompt series."""
        self.current_series = None
        self.series_index = 0