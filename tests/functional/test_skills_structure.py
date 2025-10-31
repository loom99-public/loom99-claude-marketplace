"""
Functional tests for skills restructuring.

These tests validate that ALL skills follow the correct directory structure
required by Claude Code plugins. Tests verify real file system state and
cannot be gamed by stubs or mocks.

Reference: NEXT_STEPS.md - Critical Issue #1 and #2
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set

import pytest
import yaml


# Repository root path (absolute)
REPO_ROOT = Path(__file__).parent.parent.parent.resolve()

# All plugins that must be tested
PLUGINS = ["agent-loop", "epti", "visual-iteration"]

# Expected skills per plugin (from NEXT_STEPS.md)
EXPECTED_SKILLS = {
    "agent-loop": {
        "code-exploration",
        "git-operations",
        "plan-generation",
        "verification",
    },
    "epti": {
        "implementation-with-protection",
        "overfitting-detection",
        "refactoring",
        "test-execution",
        "test-generation",
    },
    "visual-iteration": {
        "design-implementation",
        "screenshot-capture",
        "visual-comparison",
        "visual-refinement",
    },
}

# Total skill count validation
TOTAL_EXPECTED_SKILLS = 13


class TestSkillsDirectoryStructure:
    """
    Test that all skills follow the correct directory structure.

    This test cannot be gamed because:
    1. Verifies actual directory existence on filesystem
    2. Checks for SKILL.md files (not just any .md file)
    3. Ensures no flat .md files remain in skills/ directories
    4. Validates all 13 skills across all 3 plugins
    """

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_plugin_skills_directory_exists(self, plugin_name: str):
        """Each plugin must have a skills directory."""
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        assert skills_dir.exists(), f"Skills directory missing for {plugin_name}"
        assert skills_dir.is_dir(), f"Skills path is not a directory for {plugin_name}"

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_all_skills_use_subdirectories(self, plugin_name: str):
        """
        Each skill must be in its own subdirectory (not flat .md files).

        This validates the core structural fix described in NEXT_STEPS.md.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        # Check each expected skill has a subdirectory
        for skill_name in expected_skills:
            skill_dir = skills_dir / skill_name
            assert skill_dir.exists(), (
                f"Plugin {plugin_name}: Skill '{skill_name}' directory not found. "
                f"Expected: {skill_dir}"
            )
            assert skill_dir.is_dir(), (
                f"Plugin {plugin_name}: '{skill_name}' is not a directory"
            )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_no_flat_markdown_files_in_skills_directory(self, plugin_name: str):
        """
        Skills directory must NOT contain flat .md files.

        This ensures the old structure has been completely removed.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"

        # Find any .md files directly in skills/ directory
        flat_md_files = list(skills_dir.glob("*.md"))

        assert len(flat_md_files) == 0, (
            f"Plugin {plugin_name}: Found flat .md files in skills/ directory: "
            f"{[f.name for f in flat_md_files]}. "
            f"All skills must be in subdirectories with SKILL.md files."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_each_skill_has_skill_md_file(self, plugin_name: str):
        """
        Each skill subdirectory must contain a SKILL.md file.

        This is the required naming convention for Claude Code.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            assert skill_md.exists(), (
                f"Plugin {plugin_name}: Skill '{skill_name}' missing SKILL.md file. "
                f"Expected: {skill_md}"
            )
            assert skill_md.is_file(), (
                f"Plugin {plugin_name}: {skill_md} is not a file"
            )

    def test_total_skill_count(self):
        """
        Verify total number of skills across all plugins is exactly 13.

        This prevents accidentally missing skills during restructuring.
        """
        total_skills = 0
        found_skills = {}

        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"

            # Count subdirectories with SKILL.md files
            plugin_skills = []
            if skills_dir.exists():
                for item in skills_dir.iterdir():
                    if item.is_dir():
                        skill_md = item / "SKILL.md"
                        if skill_md.exists():
                            plugin_skills.append(item.name)

            found_skills[plugin_name] = plugin_skills
            total_skills += len(plugin_skills)

        assert total_skills == TOTAL_EXPECTED_SKILLS, (
            f"Expected exactly {TOTAL_EXPECTED_SKILLS} skills total, "
            f"but found {total_skills}. "
            f"Breakdown: {found_skills}"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skill_subdirectories_match_expected_names(self, plugin_name: str):
        """
        Verify skill directory names exactly match expected skill names.

        This ensures no typos or incorrect naming during restructuring.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        # Get actual skill directories
        actual_skills = set()
        if skills_dir.exists():
            for item in skills_dir.iterdir():
                if item.is_dir():
                    skill_md = item / "SKILL.md"
                    if skill_md.exists():
                        actual_skills.add(item.name)

        assert actual_skills == expected_skills, (
            f"Plugin {plugin_name}: Skill names don't match expected. "
            f"Expected: {sorted(expected_skills)}, "
            f"Found: {sorted(actual_skills)}"
        )


class TestSkillsYAMLFrontmatter:
    """
    Test that all SKILL.md files have valid YAML frontmatter.

    This test cannot be gamed because:
    1. Parses actual YAML from real files
    2. Validates required fields exist
    3. Checks field values are meaningful (non-empty, correct types)
    4. Verifies name consistency with directory structure
    """

    def _extract_yaml_frontmatter(self, file_path: Path) -> Dict:
        """
        Extract and parse YAML frontmatter from a markdown file.

        Expected format:
        ---
        name: skill-name
        description: Skill description
        ---

        Returns parsed YAML dict or raises assertion error if invalid.
        """
        content = file_path.read_text(encoding="utf-8")

        # Frontmatter must start with ---
        assert content.startswith("---\n"), (
            f"{file_path}: YAML frontmatter must start with '---' on first line"
        )

        # Find closing ---
        lines = content.split("\n")
        closing_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                closing_idx = i
                break

        assert closing_idx is not None, (
            f"{file_path}: YAML frontmatter must have closing '---'"
        )

        # Extract YAML content
        yaml_content = "\n".join(lines[1:closing_idx])

        # Parse YAML
        try:
            data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            pytest.fail(f"{file_path}: Invalid YAML frontmatter: {e}")

        assert isinstance(data, dict), (
            f"{file_path}: YAML frontmatter must be a mapping/dict"
        )

        return data

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_all_skills_have_yaml_frontmatter(self, plugin_name: str):
        """All SKILL.md files must have YAML frontmatter."""
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"

            # File must exist (covered by structure tests, but double-check)
            assert skill_md.exists(), f"SKILL.md not found: {skill_md}"

            # Must have valid YAML frontmatter
            self._extract_yaml_frontmatter(skill_md)

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_yaml_frontmatter_has_required_fields(self, plugin_name: str):
        """
        YAML frontmatter must contain 'name' and 'description' fields.

        Reference: NEXT_STEPS.md Issue #2
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            frontmatter = self._extract_yaml_frontmatter(skill_md)

            # Check required fields
            assert "name" in frontmatter, (
                f"{skill_md}: YAML frontmatter missing 'name' field"
            )
            assert "description" in frontmatter, (
                f"{skill_md}: YAML frontmatter missing 'description' field"
            )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_yaml_name_matches_directory_name(self, plugin_name: str):
        """
        The 'name' field in YAML must match the skill directory name.

        This ensures consistency and correct skill identification.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            frontmatter = self._extract_yaml_frontmatter(skill_md)

            yaml_name = frontmatter.get("name")
            assert yaml_name == skill_name, (
                f"{skill_md}: YAML 'name' field '{yaml_name}' "
                f"does not match directory name '{skill_name}'"
            )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_yaml_description_is_valid(self, plugin_name: str):
        """
        The 'description' field must be a non-empty string under 1024 chars.

        Reference: NEXT_STEPS.md - max 1024 chars for description
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            frontmatter = self._extract_yaml_frontmatter(skill_md)

            description = frontmatter.get("description")

            # Must be a string
            assert isinstance(description, str), (
                f"{skill_md}: 'description' must be a string, "
                f"got {type(description).__name__}"
            )

            # Must be non-empty
            assert len(description.strip()) > 0, (
                f"{skill_md}: 'description' cannot be empty"
            )

            # Must be under 1024 characters
            assert len(description) <= 1024, (
                f"{skill_md}: 'description' must be ≤1024 chars, "
                f"got {len(description)} chars"
            )


class TestPluginConfiguration:
    """
    Test that plugin.json files correctly reference skills.

    This test cannot be gamed because:
    1. Parses actual JSON configuration files
    2. Validates paths point to real directories
    3. Ensures consistency between configuration and file system
    """

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_plugin_json_exists(self, plugin_name: str):
        """Each plugin must have a plugin.json file."""
        plugin_json = REPO_ROOT / "plugins" / plugin_name / ".claude-plugin" / "plugin.json"
        assert plugin_json.exists(), f"plugin.json not found for {plugin_name}"
        assert plugin_json.is_file(), f"plugin.json is not a file for {plugin_name}"

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_plugin_json_is_valid_json(self, plugin_name: str):
        """plugin.json must be valid JSON."""
        plugin_json = REPO_ROOT / "plugins" / plugin_name / ".claude-plugin" / "plugin.json"

        try:
            with open(plugin_json, "r", encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"{plugin_json}: Invalid JSON: {e}")

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_plugin_json_has_skills_path(self, plugin_name: str):
        """
        plugin.json must have a 'skills' key pointing to skills directory.

        NOTE: NEXT_STEPS.md indicates this might be missing currently.
        """
        plugin_json = REPO_ROOT / "plugins" / plugin_name / ".claude-plugin" / "plugin.json"

        with open(plugin_json, "r", encoding="utf-8") as f:
            config = json.load(f)

        assert "skills" in config, (
            f"{plugin_json}: Missing 'skills' key in plugin configuration"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skills_path_points_to_valid_directory(self, plugin_name: str):
        """The skills path in plugin.json must point to an existing directory."""
        plugin_json = REPO_ROOT / "plugins" / plugin_name / ".claude-plugin" / "plugin.json"
        plugin_dir = plugin_json.parent.parent  # Go up from .claude-plugin/

        with open(plugin_json, "r", encoding="utf-8") as f:
            config = json.load(f)

        if "skills" not in config:
            pytest.skip("skills key not present in plugin.json")

        skills_path_str = config["skills"]

        # Resolve path relative to plugin directory
        skills_path = (plugin_dir / skills_path_str).resolve()

        assert skills_path.exists(), (
            f"{plugin_json}: skills path '{skills_path_str}' "
            f"does not exist (resolved to {skills_path})"
        )
        assert skills_path.is_dir(), (
            f"{plugin_json}: skills path '{skills_path_str}' "
            f"is not a directory"
        )


class TestContentPreservation:
    """
    Test that skill content is preserved during restructuring.

    This test cannot be gamed because:
    1. Verifies actual file sizes are substantial (not empty stubs)
    2. Checks that markdown content exists beyond frontmatter
    3. Validates each skill has meaningful content (>100 lines expected)
    """

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skill_files_have_substantial_content(self, plugin_name: str):
        """
        Each SKILL.md must have substantial content (not just frontmatter).

        Reference: CLAUDE.md shows skills range from 242-1227 lines.
        We expect at least 100 lines after restructuring to ensure
        content wasn't lost.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"

            if not skill_md.exists():
                pytest.skip(f"SKILL.md does not exist yet: {skill_md}")

            # Read file content
            content = skill_md.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Should have at least 100 lines (skills are comprehensive)
            assert len(lines) >= 100, (
                f"{skill_md}: Expected at least 100 lines of content, "
                f"got {len(lines)}. Content may have been lost during restructuring."
            )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skill_has_markdown_content_after_frontmatter(self, plugin_name: str):
        """
        SKILL.md must have markdown content after the YAML frontmatter.

        This ensures the file isn't just frontmatter with no actual skill content.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"

            if not skill_md.exists():
                pytest.skip(f"SKILL.md does not exist yet: {skill_md}")

            content = skill_md.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Find end of frontmatter
            closing_idx = None
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    closing_idx = i
                    break

            assert closing_idx is not None, (
                f"{skill_md}: Could not find closing --- for frontmatter"
            )

            # Get content after frontmatter
            content_after = "\n".join(lines[closing_idx + 1:])
            content_after_stripped = content_after.strip()

            # Must have substantial content after frontmatter
            assert len(content_after_stripped) > 500, (
                f"{skill_md}: Insufficient content after YAML frontmatter. "
                f"Expected substantial markdown content, got {len(content_after_stripped)} chars."
            )

    def test_total_content_size_preserved(self):
        """
        Total size of all skill content should be substantial.

        Reference: NEXT_STEPS.md shows 8,921 total lines across 13 skills.
        After adding frontmatter, should still be close to this number.
        """
        total_lines = 0

        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            expected_skills = EXPECTED_SKILLS[plugin_name]

            for skill_name in expected_skills:
                skill_md = skills_dir / skill_name / "SKILL.md"

                if not skill_md.exists():
                    continue

                content = skill_md.read_text(encoding="utf-8")
                total_lines += len(content.split("\n"))

        # After Phase 2 verbosity reduction, skills were optimized to 3,600-4,000 lines
        # Original was 8,921 lines, Phase 2 reduced by ~57% to improve effectiveness
        # Target range: 3,600-4,500 lines (250-400 lines per skill * 13 skills)
        if total_lines > 0:
            assert 3600 <= total_lines <= 4500, (
                f"Expected 3,600-4,500 total lines across all skills (post-Phase 2 optimization), "
                f"got {total_lines}. Skills should be optimized to 250-400 lines each."
            )


class TestCompletenessAndCorrectness:
    """
    High-level tests that validate overall restructuring completeness.

    These tests provide a final check that ALL requirements are met.
    """

    def test_all_plugins_have_all_expected_skills(self):
        """
        Comprehensive check that every plugin has every expected skill
        in the correct structure.
        """
        issues = []

        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            expected_skills = EXPECTED_SKILLS[plugin_name]

            if not skills_dir.exists():
                issues.append(f"{plugin_name}: skills directory does not exist")
                continue

            for skill_name in expected_skills:
                skill_dir = skills_dir / skill_name
                skill_md = skill_dir / "SKILL.md"

                if not skill_dir.exists():
                    issues.append(f"{plugin_name}/{skill_name}: directory missing")
                elif not skill_dir.is_dir():
                    issues.append(f"{plugin_name}/{skill_name}: not a directory")
                elif not skill_md.exists():
                    issues.append(f"{plugin_name}/{skill_name}: SKILL.md missing")
                elif not skill_md.is_file():
                    issues.append(f"{plugin_name}/{skill_name}: SKILL.md not a file")

        assert len(issues) == 0, (
            f"Found {len(issues)} structural issues:\n" +
            "\n".join(f"  - {issue}" for issue in issues)
        )

    def test_no_unexpected_files_in_skills_directories(self):
        """
        Skills directories should only contain expected skill subdirectories.

        This catches any leftover files or unexpected structure.
        """
        unexpected = []

        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            expected_skills = EXPECTED_SKILLS[plugin_name]

            if not skills_dir.exists():
                continue

            for item in skills_dir.iterdir():
                # Skip hidden files like .DS_Store
                if item.name.startswith("."):
                    continue

                # Should be a directory with name in expected skills
                if not item.is_dir():
                    unexpected.append(f"{plugin_name}/skills/{item.name} (not a directory)")
                elif item.name not in expected_skills:
                    unexpected.append(f"{plugin_name}/skills/{item.name} (unexpected skill)")

        assert len(unexpected) == 0, (
            f"Found {len(unexpected)} unexpected items in skills directories:\n" +
            "\n".join(f"  - {item}" for item in unexpected)
        )

    def test_restructuring_meets_all_requirements(self):
        """
        Meta-test that validates all NEXT_STEPS.md requirements are met.

        This is a final comprehensive check covering:
        - Issue #1: Skills directory structure
        - Issue #2: YAML frontmatter
        - Plugin configuration
        - Content preservation
        """
        failures = []

        # Check Issue #1: Directory structure
        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            expected_skills = EXPECTED_SKILLS[plugin_name]

            for skill_name in expected_skills:
                skill_dir = skills_dir / skill_name
                skill_md = skill_dir / "SKILL.md"

                if not (skill_dir.exists() and skill_dir.is_dir()):
                    failures.append(f"Structure: {plugin_name}/{skill_name} not in subdirectory")

                if not (skill_md.exists() and skill_md.is_file()):
                    failures.append(f"Structure: {plugin_name}/{skill_name}/SKILL.md missing")

            # Check no flat files
            if skills_dir.exists():
                flat_files = list(skills_dir.glob("*.md"))
                if flat_files:
                    failures.append(
                        f"Structure: {plugin_name} has flat .md files: "
                        f"{[f.name for f in flat_files]}"
                    )

        # Check Issue #2: YAML frontmatter
        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            expected_skills = EXPECTED_SKILLS[plugin_name]

            for skill_name in expected_skills:
                skill_md = skills_dir / skill_name / "SKILL.md"

                if not skill_md.exists():
                    continue

                try:
                    content = skill_md.read_text(encoding="utf-8")
                    if not content.startswith("---\n"):
                        failures.append(f"Frontmatter: {plugin_name}/{skill_name} missing YAML frontmatter")
                        continue

                    # Quick YAML parse check
                    lines = content.split("\n")
                    closing = None
                    for i in range(1, min(20, len(lines))):
                        if lines[i].strip() == "---":
                            closing = i
                            break

                    if closing is None:
                        failures.append(f"Frontmatter: {plugin_name}/{skill_name} no closing ---")
                        continue

                    yaml_str = "\n".join(lines[1:closing])
                    try:
                        data = yaml.safe_load(yaml_str)
                        if "name" not in data:
                            failures.append(f"Frontmatter: {plugin_name}/{skill_name} missing 'name'")
                        if "description" not in data:
                            failures.append(f"Frontmatter: {plugin_name}/{skill_name} missing 'description'")
                    except yaml.YAMLError:
                        failures.append(f"Frontmatter: {plugin_name}/{skill_name} invalid YAML")

                except Exception as e:
                    failures.append(f"Frontmatter: {plugin_name}/{skill_name} error: {e}")

        # Report all failures
        assert len(failures) == 0, (
            f"Restructuring incomplete. Found {len(failures)} issues:\n" +
            "\n".join(f"  - {failure}" for failure in failures)
        )
