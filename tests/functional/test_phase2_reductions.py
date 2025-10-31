"""
Functional tests for Phase 2 Verbosity Reduction (Skills & READMEs).

These tests validate that Phase 2 reduction work maintains quality while achieving
target size reductions. Tests verify real file system state and cannot be gamed
by stubs or mocks.

Reference:
- PLAN-verbosity-reduction-2025-10-29-075000.md (Phase 2)
- TODO-verbosity-phase1.md

Target Reductions:
- Skills: 9,272 → 4,030 lines (-57%)
- READMEs: 4,272 → 1,050 lines (-75%)

These tests are designed to:
1. FAIL before Phase 2 reduction (current state exceeds targets)
2. PASS after Phase 2 reduction (files meet optimal sizes)
3. Resist gaming (verify actual content, not just file size)
"""

import re
from pathlib import Path
from typing import Dict, List, Set

import pytest
import yaml


# Repository root path (absolute)
REPO_ROOT = Path(__file__).parent.parent.parent.resolve()

# All plugins that must be tested
PLUGINS = ["agent-loop", "epti", "visual-iteration"]

# Expected skills per plugin
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

# Phase 2 Target: Optimal skill length range (per PLAN)
SKILL_MIN_LINES = 100  # Prevent too-sparse skills
SKILL_OPTIMAL_MIN_LINES = 250  # Target minimum
SKILL_OPTIMAL_MAX_LINES = 400  # Target maximum
SKILL_ABSOLUTE_MAX_LINES = 450  # Hard limit (with 50 line grace period)

# Phase 2 Target: Total skills size
SKILLS_TOTAL_TARGET = 4030  # Lines (from 9,272)
SKILLS_TOTAL_MAX = 4500  # Allow 10% buffer for content preservation

# Phase 2 Target: README sizes per plugin (per PLAN)
README_TARGETS = {
    "visual-iteration": {"min": 200, "target": 500, "max": 550},
    "epti": {"min": 200, "target": 350, "max": 400},
    "agent-loop": {"min": 100, "target": 200, "max": 250},
}

# Total README target
README_TOTAL_TARGET = 1050  # Lines (from 4,272)
README_TOTAL_MAX = 1200  # Allow buffer


class TestSkillsSizeValidation:
    """
    Validate skills are within optimal size range (250-400 lines).

    These tests FAIL before Phase 2 (current: 247-1,232 lines)
    and PASS after Phase 2 reduction (target: 250-400 lines).

    Anti-Gaming: Cannot bypass by empty files (content tests) or
    removing structure (YAML frontmatter tests).
    """

    def _get_skill_line_count(self, skill_path: Path) -> int:
        """Get line count for a skill file."""
        if not skill_path.exists():
            return 0
        content = skill_path.read_text(encoding="utf-8")
        return len(content.split("\n"))

    def _get_non_empty_line_count(self, skill_path: Path) -> int:
        """Get non-empty line count (excluding blank lines)."""
        if not skill_path.exists():
            return 0
        content = skill_path.read_text(encoding="utf-8")
        lines = [line for line in content.split("\n") if line.strip()]
        return len(lines)

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_no_skill_exceeds_maximum_length(self, plugin_name: str):
        """
        No skill should exceed 450 lines (400 target + 50 grace period).

        Current state (will FAIL):
        - visual-iteration: 730-1,232 lines (4 skills exceed)
        - epti: 508-715 lines (all 5 exceed)
        - agent-loop: 247-630 lines (3 exceed)

        Target state (will PASS): All skills ≤450 lines
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        violations = []
        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if not skill_md.exists():
                pytest.skip(f"Skill not yet created: {skill_md}")

            line_count = self._get_skill_line_count(skill_md)

            if line_count > SKILL_ABSOLUTE_MAX_LINES:
                violations.append(
                    f"{skill_name}: {line_count} lines "
                    f"(exceeds max {SKILL_ABSOLUTE_MAX_LINES})"
                )

        assert len(violations) == 0, (
            f"Plugin {plugin_name}: {len(violations)} skill(s) exceed maximum length:\n"
            + "\n".join(f"  - {v}" for v in violations)
            + f"\n\nPhase 2 target: All skills ≤{SKILL_ABSOLUTE_MAX_LINES} lines"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skills_within_optimal_range(self, plugin_name: str):
        """
        All skills should be within optimal range (250-400 lines).

        Current state (will FAIL): Most skills outside range
        Target state (will PASS): All skills 250-400 lines
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        too_short = []
        too_long = []
        optimal = []

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if not skill_md.exists():
                pytest.skip(f"Skill not yet created: {skill_md}")

            line_count = self._get_skill_line_count(skill_md)

            if line_count < SKILL_OPTIMAL_MIN_LINES:
                too_short.append(f"{skill_name}: {line_count} lines")
            elif line_count > SKILL_OPTIMAL_MAX_LINES:
                too_long.append(f"{skill_name}: {line_count} lines")
            else:
                optimal.append(f"{skill_name}: {line_count} lines")

        # Calculate percentage in optimal range
        total_skills = len(expected_skills)
        optimal_count = len(optimal)
        optimal_percentage = (optimal_count / total_skills * 100) if total_skills > 0 else 0

        # Require at least 80% in optimal range (allows some flexibility)
        assert optimal_percentage >= 80, (
            f"Plugin {plugin_name}: Only {optimal_percentage:.0f}% of skills "
            f"in optimal range (250-400 lines).\n\n"
            f"Optimal ({optimal_count}/{total_skills}):\n"
            + "\n".join(f"  ✓ {s}" for s in optimal)
            + (f"\n\nToo short ({len(too_short)}):\n" + "\n".join(f"  ✗ {s}" for s in too_short) if too_short else "")
            + (f"\n\nToo long ({len(too_long)}):\n" + "\n".join(f"  ✗ {s}" for s in too_long) if too_long else "")
            + f"\n\nPhase 2 target: ≥80% skills in 250-400 line range"
        )

    def test_total_skills_size_meets_target(self):
        """
        Total skills size should be ~4,030 lines (±10% buffer).

        Current state (will FAIL): 8,986 lines total
        Target state (will PASS): ~4,030 lines total
        """
        total_lines = 0
        skill_breakdown = {}

        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            expected_skills = EXPECTED_SKILLS[plugin_name]

            plugin_lines = 0
            for skill_name in expected_skills:
                skill_md = skills_dir / skill_name / "SKILL.md"
                if skill_md.exists():
                    lines = self._get_skill_line_count(skill_md)
                    plugin_lines += lines
                    total_lines += lines

            skill_breakdown[plugin_name] = plugin_lines

        # Must be under maximum (with 10% buffer)
        assert total_lines <= SKILLS_TOTAL_MAX, (
            f"Total skills size {total_lines} lines exceeds maximum {SKILLS_TOTAL_MAX}.\n\n"
            f"Breakdown:\n"
            + "\n".join(f"  - {plugin}: {lines} lines" for plugin, lines in skill_breakdown.items())
            + f"\n\nPhase 2 target: ~{SKILLS_TOTAL_TARGET} lines total"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skills_average_length_optimal(self, plugin_name: str):
        """
        Average skill length should be 250-400 lines per plugin.

        Current state (will FAIL):
        - agent-loop: 523 avg (4 skills, 2,083 lines)
        - epti: 607 avg (5 skills, 3,034 lines)
        - visual-iteration: 1,042 avg (4 skills, 4,169 lines)

        Target state (will PASS): All averages 250-400 lines
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        total_lines = 0
        skill_count = 0

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if skill_md.exists():
                total_lines += self._get_skill_line_count(skill_md)
                skill_count += 1

        if skill_count == 0:
            pytest.skip(f"No skills found for {plugin_name}")

        avg_lines = total_lines / skill_count

        assert SKILL_OPTIMAL_MIN_LINES <= avg_lines <= SKILL_OPTIMAL_MAX_LINES, (
            f"Plugin {plugin_name}: Average skill length {avg_lines:.0f} lines "
            f"outside optimal range.\n"
            f"Expected: {SKILL_OPTIMAL_MIN_LINES}-{SKILL_OPTIMAL_MAX_LINES} lines\n"
            f"Total: {total_lines} lines across {skill_count} skills\n\n"
            f"Phase 2 target: Average 250-400 lines per skill"
        )


class TestSkillsStructurePreservation:
    """
    Verify skills maintain required structure after reduction.

    Anti-Gaming: Checks for actual content patterns, not just file size.
    """

    def _extract_yaml_frontmatter(self, file_path: Path) -> Dict:
        """Extract and parse YAML frontmatter."""
        content = file_path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), f"{file_path}: Missing YAML frontmatter"

        lines = content.split("\n")
        closing_idx = None
        for i in range(1, min(50, len(lines))):
            if lines[i].strip() == "---":
                closing_idx = i
                break

        assert closing_idx is not None, f"{file_path}: No closing --- for frontmatter"

        yaml_content = "\n".join(lines[1:closing_idx])
        return yaml.safe_load(yaml_content)

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_yaml_frontmatter_preserved(self, plugin_name: str):
        """
        YAML frontmatter must be preserved after reduction.

        Anti-Gaming: Cannot reduce by removing metadata.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if not skill_md.exists():
                pytest.skip(f"Skill not yet created: {skill_md}")

            frontmatter = self._extract_yaml_frontmatter(skill_md)

            # Required fields
            assert "name" in frontmatter, f"{skill_md}: Missing 'name' field"
            assert "description" in frontmatter, f"{skill_md}: Missing 'description' field"

            # Name matches directory
            assert frontmatter["name"] == skill_name, (
                f"{skill_md}: Name mismatch (expected {skill_name}, got {frontmatter['name']})"
            )

            # Description is meaningful
            description = frontmatter["description"]
            assert isinstance(description, str), f"{skill_md}: Description must be string"
            assert len(description.strip()) >= 20, (
                f"{skill_md}: Description too short ({len(description)} chars, min 20)"
            )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skills_have_structured_sections(self, plugin_name: str):
        """
        Skills must maintain structured sections (not just wall of text).

        Anti-Gaming: Verifies presence of markdown headings.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if not skill_md.exists():
                pytest.skip(f"Skill not yet created: {skill_md}")

            content = skill_md.read_text(encoding="utf-8")

            # Count markdown headings (## or ###)
            heading_pattern = re.compile(r'^#{2,3}\s+.+$', re.MULTILINE)
            headings = heading_pattern.findall(content)

            # Should have at least 3 sections (Purpose, Procedure, Examples, etc.)
            assert len(headings) >= 3, (
                f"{skill_md}: Only {len(headings)} sections found. "
                f"Expected at least 3 structured sections.\n"
                f"Skills should not be reduced to unstructured text."
            )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skills_contain_examples(self, plugin_name: str):
        """
        Skills must contain at least 1-2 examples (not removed entirely).

        Anti-Gaming: Checks for example markers or code blocks.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if not skill_md.exists():
                pytest.skip(f"Skill not yet created: {skill_md}")

            content = skill_md.read_text(encoding="utf-8")

            # Look for example indicators
            has_example_heading = bool(re.search(r'#{2,3}\s+Example', content, re.IGNORECASE))
            has_code_blocks = bool(re.search(r'```', content))
            has_example_word = content.lower().count('example') >= 2

            # Should have at least one indicator of examples
            assert has_example_heading or has_code_blocks or has_example_word, (
                f"{skill_md}: No examples found. "
                f"Skills must retain 1-2 examples for clarity.\n"
                f"Phase 2 reduction should not eliminate all examples."
            )


class TestSkillsContentQuality:
    """
    Verify essential content is preserved after reduction.

    Anti-Gaming: Checks for specific content patterns that indicate
    meaningful procedures, not just filler text.
    """

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skills_have_substantial_content_after_frontmatter(self, plugin_name: str):
        """
        Skills must have substantial content after YAML frontmatter.

        Anti-Gaming: Cannot pass by having only frontmatter and minimal content.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if not skill_md.exists():
                pytest.skip(f"Skill not yet created: {skill_md}")

            content = skill_md.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Find end of frontmatter
            closing_idx = None
            for i in range(1, min(50, len(lines))):
                if lines[i].strip() == "---":
                    closing_idx = i
                    break

            assert closing_idx is not None, f"{skill_md}: No closing ---"

            # Get content after frontmatter
            content_after = "\n".join(lines[closing_idx + 1:])
            content_after_stripped = content_after.strip()

            # Must have substantial content (at least 3,000 chars for 150+ lines of real content)
            min_chars = 3000
            assert len(content_after_stripped) >= min_chars, (
                f"{skill_md}: Only {len(content_after_stripped)} chars after frontmatter.\n"
                f"Expected at least {min_chars} chars for meaningful skill content.\n"
                f"Phase 2 reduction should not gut the content."
            )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skills_contain_procedures(self, plugin_name: str):
        """
        Skills must contain procedural guidance (not just descriptions).

        Anti-Gaming: Looks for procedural language patterns.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        # Procedural indicators
        procedural_patterns = [
            r'\b(step|procedure|process|workflow|approach|method)\b',
            r'\b(when|how|should|must|ensure)\b',
            r'\d+\.\s+',  # Numbered lists
            r'^[-*]\s+',  # Bullet points
        ]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if not skill_md.exists():
                pytest.skip(f"Skill not yet created: {skill_md}")

            content = skill_md.read_text(encoding="utf-8")

            # Count procedural indicators
            indicators_found = 0
            for pattern in procedural_patterns:
                if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                    indicators_found += 1

            # Should have at least 3 types of procedural indicators
            assert indicators_found >= 3, (
                f"{skill_md}: Only {indicators_found}/4 procedural patterns found.\n"
                f"Skills must contain executable procedures, not just descriptions."
            )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_skills_no_excessive_framework_duplication(self, plugin_name: str):
        """
        Skills should not contain excessive framework duplication (max 2 examples).

        Anti-Gaming: Prevents bloat from 6+ framework examples.
        """
        skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
        expected_skills = EXPECTED_SKILLS[plugin_name]

        # Common framework names
        frameworks = ["Python", "JavaScript", "Go", "Java", "Ruby", "TypeScript", "pytest", "jest", "JUnit", "RSpec"]

        for skill_name in expected_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            if not skill_md.exists():
                pytest.skip(f"Skill not yet created: {skill_md}")

            content = skill_md.read_text(encoding="utf-8")

            # Count framework mentions
            framework_mentions = sum(content.count(fw) for fw in frameworks)

            # Should not have excessive mentions (threshold: 20 mentions = ~3-4 frameworks heavily duplicated)
            max_mentions = 20
            assert framework_mentions <= max_mentions, (
                f"{skill_md}: {framework_mentions} framework mentions found.\n"
                f"Expected ≤{max_mentions} mentions (1-2 example frameworks).\n"
                f"Phase 2 reduction should eliminate framework duplication."
            )


class TestREADMESizeValidation:
    """
    Validate READMEs are concise references (200-500 lines).

    These tests FAIL before Phase 2 (current: 715-2,319 lines)
    and PASS after Phase 2 reduction (target: 200-500 lines).

    Anti-Gaming: Cannot bypass by empty files (content tests).
    """

    def _get_readme_line_count(self, readme_path: Path) -> int:
        """Get line count for README."""
        if not readme_path.exists():
            return 0
        content = readme_path.read_text(encoding="utf-8")
        return len(content.split("\n"))

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_readme_within_target_range(self, plugin_name: str):
        """
        README should be within target range for plugin.

        Current state (will FAIL):
        - visual-iteration: 2,319 lines (target: ≤500)
        - epti: 1,238 lines (target: ≤350)
        - agent-loop: 715 lines (target: ≤200)

        Target state (will PASS): All READMEs within target
        """
        readme_path = REPO_ROOT / "plugins" / plugin_name / "README.md"

        if not readme_path.exists():
            pytest.skip(f"README not found: {readme_path}")

        line_count = self._get_readme_line_count(readme_path)
        targets = README_TARGETS[plugin_name]

        assert line_count >= targets["min"], (
            f"Plugin {plugin_name}: README too short ({line_count} lines).\n"
            f"Expected at least {targets['min']} lines for meaningful reference."
        )

        assert line_count <= targets["max"], (
            f"Plugin {plugin_name}: README too long ({line_count} lines).\n"
            f"Target: {targets['target']} lines (max {targets['max']}).\n"
            f"Phase 2 reduction: Convert from tutorial to concise reference."
        )

    def test_total_readmes_size_meets_target(self):
        """
        Total READMEs size should be ~1,050 lines (±15% buffer).

        Current state (will FAIL): 4,272 lines total
        Target state (will PASS): ~1,050 lines total
        """
        total_lines = 0
        readme_breakdown = {}

        for plugin_name in PLUGINS:
            readme_path = REPO_ROOT / "plugins" / plugin_name / "README.md"
            if readme_path.exists():
                lines = self._get_readme_line_count(readme_path)
                readme_breakdown[plugin_name] = lines
                total_lines += lines

        # Must be under maximum (with 15% buffer)
        assert total_lines <= README_TOTAL_MAX, (
            f"Total READMEs size {total_lines} lines exceeds maximum {README_TOTAL_MAX}.\n\n"
            f"Breakdown:\n"
            + "\n".join(f"  - {plugin}: {lines} lines" for plugin, lines in readme_breakdown.items())
            + f"\n\nPhase 2 target: ~{README_TOTAL_TARGET} lines total"
        )


class TestREADMEStructureValidation:
    """
    Verify READMEs are references, not tutorials.

    Anti-Gaming: Checks for reference structure patterns.
    """

    def _get_readme_content(self, plugin_name: str) -> str:
        """Get README content."""
        readme_path = REPO_ROOT / "plugins" / plugin_name / "README.md"
        if not readme_path.exists():
            pytest.skip(f"README not found: {readme_path}")
        return readme_path.read_text(encoding="utf-8")

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_readme_has_quickstart_section(self, plugin_name: str):
        """
        README must have a Quick Start or Getting Started section.

        Anti-Gaming: Verifies reference structure.
        """
        content = self._get_readme_content(plugin_name)

        has_quickstart = bool(re.search(
            r'#{1,2}\s+(Quick\s*Start|Getting\s*Started|Installation)',
            content,
            re.IGNORECASE
        ))

        assert has_quickstart, (
            f"Plugin {plugin_name}: README missing Quick Start section.\n"
            f"READMEs should be references with clear quickstart guidance."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_readme_has_command_reference(self, plugin_name: str):
        """
        README must have a command reference/list section.

        Anti-Gaming: Verifies reference format (not tutorial).
        """
        content = self._get_readme_content(plugin_name)

        has_command_section = bool(re.search(
            r'#{1,2}\s+(Commands?|Command\s+Reference|Available\s+Commands)',
            content,
            re.IGNORECASE
        ))

        assert has_command_section, (
            f"Plugin {plugin_name}: README missing Command Reference section.\n"
            f"READMEs should list commands concisely, not teach concepts."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_readme_not_excessive_examples(self, plugin_name: str):
        """
        README should not have excessive examples (max 3-4 major examples).

        Anti-Gaming: Prevents tutorial-style bloat.
        """
        content = self._get_readme_content(plugin_name)

        # Count code blocks (examples)
        code_blocks = len(re.findall(r'```', content)) // 2  # Divide by 2 for open/close

        # Should have examples, but not excessive
        max_code_blocks = 15  # Reasonable for 2-3 examples with variants
        assert code_blocks <= max_code_blocks, (
            f"Plugin {plugin_name}: README has {code_blocks} code blocks.\n"
            f"Expected ≤{max_code_blocks} blocks (2-3 examples).\n"
            f"Phase 2 reduction: Remove excessive examples, keep 1-2 representative ones."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_readme_concise_sections(self, plugin_name: str):
        """
        README sections should be concise (not multi-page explanations).

        Anti-Gaming: Checks that no single section is excessively long.
        """
        content = self._get_readme_content(plugin_name)

        # Split by ## headings
        sections = re.split(r'\n#{1,2}\s+', content)

        # Find longest section
        max_section_length = max(len(section.split("\n")) for section in sections)

        # No section should be > 200 lines (that's a chapter, not a reference section)
        max_allowed = 200
        assert max_section_length <= max_allowed, (
            f"Plugin {plugin_name}: README has a section with {max_section_length} lines.\n"
            f"Expected ≤{max_allowed} lines per section.\n"
            f"Phase 2 reduction: Break up or condense long sections."
        )


class TestREADMEContentQuality:
    """
    Verify essential README content is preserved.

    Anti-Gaming: Checks for meaningful content, not filler.
    """

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_readme_has_plugin_description(self, plugin_name: str):
        """
        README must describe what the plugin does.

        Anti-Gaming: Cannot pass with generic filler text.
        """
        readme_path = REPO_ROOT / "plugins" / plugin_name / "README.md"
        if not readme_path.exists():
            pytest.skip(f"README not found: {readme_path}")

        content = readme_path.read_text(encoding="utf-8")

        # Should mention plugin name or key concepts
        plugin_keywords = {
            "visual-iteration": ["visual", "screenshot", "iteration", "UI"],
            "epti": ["TDD", "test", "implement", "evaluate"],
            "agent-loop": ["workflow", "loop", "explore", "plan"],
        }

        keywords = plugin_keywords[plugin_name]
        mentions = sum(1 for kw in keywords if kw.lower() in content.lower())

        assert mentions >= 2, (
            f"Plugin {plugin_name}: README doesn't mention key concepts.\n"
            f"Expected at least 2 of: {keywords}\n"
            f"READMEs must clearly describe plugin purpose."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_readme_lists_all_commands(self, plugin_name: str):
        """
        README should list all available commands.

        Anti-Gaming: Verifies completeness of reference.
        """
        readme_path = REPO_ROOT / "plugins" / plugin_name / "README.md"
        commands_dir = REPO_ROOT / "plugins" / plugin_name / "commands"

        if not readme_path.exists():
            pytest.skip(f"README not found: {readme_path}")
        if not commands_dir.exists():
            pytest.skip(f"Commands directory not found: {commands_dir}")

        content = readme_path.read_text(encoding="utf-8")

        # Get all command names
        command_files = list(commands_dir.glob("*.md"))
        command_names = [f.stem for f in command_files]

        # Check each command is mentioned (either as /command or command.md)
        missing_commands = []
        for cmd_name in command_names:
            if not (f"/{cmd_name}" in content or cmd_name in content):
                missing_commands.append(cmd_name)

        assert len(missing_commands) == 0, (
            f"Plugin {plugin_name}: README doesn't mention these commands: {missing_commands}\n"
            f"READMEs must list all available commands."
        )


class TestConsistencyAcrossPlugins:
    """
    Verify consistent patterns across all plugins.

    Anti-Gaming: Ensures Phase 2 reduction is applied consistently.
    """

    def test_skills_consistent_size_distribution(self):
        """
        Skills size distribution should be similar across plugins.

        Anti-Gaming: Prevents reducing only some plugins.
        """
        plugin_averages = {}

        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            expected_skills = EXPECTED_SKILLS[plugin_name]

            total_lines = 0
            skill_count = 0

            for skill_name in expected_skills:
                skill_md = skills_dir / skill_name / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text(encoding="utf-8")
                    total_lines += len(content.split("\n"))
                    skill_count += 1

            if skill_count > 0:
                plugin_averages[plugin_name] = total_lines / skill_count

        if len(plugin_averages) < 2:
            pytest.skip("Not enough plugins to compare")

        # Check that averages are reasonably consistent (within 50% of each other)
        avg_values = list(plugin_averages.values())
        min_avg = min(avg_values)
        max_avg = max(avg_values)
        ratio = max_avg / min_avg if min_avg > 0 else 0

        assert ratio <= 2.0, (
            f"Skills size inconsistent across plugins:\n"
            + "\n".join(f"  - {plugin}: {avg:.0f} lines avg" for plugin, avg in plugin_averages.items())
            + f"\n\nRatio: {ratio:.2f}x (expected ≤2.0x)\n"
            f"Phase 2 reduction should be applied consistently."
        )

    def test_all_skills_follow_same_structure_pattern(self):
        """
        All skills should follow similar structural patterns.

        Anti-Gaming: Ensures consistent quality across all skills.
        """
        structure_scores = []

        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            expected_skills = EXPECTED_SKILLS[plugin_name]

            for skill_name in expected_skills:
                skill_md = skills_dir / skill_name / "SKILL.md"
                if not skill_md.exists():
                    continue

                content = skill_md.read_text(encoding="utf-8")

                # Score based on structural elements
                score = 0

                # Has YAML frontmatter
                if content.startswith("---\n"):
                    score += 1

                # Has multiple sections (## headings)
                section_count = len(re.findall(r'^#{2,3}\s+', content, re.MULTILINE))
                if section_count >= 3:
                    score += 1

                # Has examples
                if re.search(r'#{2,3}\s+Example', content, re.IGNORECASE):
                    score += 1

                # Has procedural language
                if re.search(r'\b(step|procedure|when|should)\b', content, re.IGNORECASE):
                    score += 1

                # Has code blocks
                if '```' in content:
                    score += 1

                structure_scores.append((f"{plugin_name}/{skill_name}", score))

        if len(structure_scores) < 2:
            pytest.skip("Not enough skills to compare")

        # All skills should score at least 4/5 (consistent structure)
        low_scores = [(name, score) for name, score in structure_scores if score < 4]

        assert len(low_scores) == 0, (
            f"Skills with inconsistent structure:\n"
            + "\n".join(f"  - {name}: {score}/5" for name, score in low_scores)
            + f"\n\nAll skills should follow consistent structure pattern."
        )


class TestPhase2ValidationSummary:
    """
    High-level summary test validating Phase 2 completion.

    This test provides a clear pass/fail signal for Phase 2 work.
    """

    def test_phase2_reduction_targets_met(self):
        """
        Comprehensive check that all Phase 2 targets are met.

        This test summarizes the overall Phase 2 completion status.
        """
        issues = []

        # 1. Check skills total size
        total_skills_lines = 0
        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            for skill_name in EXPECTED_SKILLS[plugin_name]:
                skill_md = skills_dir / skill_name / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text(encoding="utf-8")
                    total_skills_lines += len(content.split("\n"))

        if total_skills_lines > SKILLS_TOTAL_MAX:
            issues.append(
                f"Skills total: {total_skills_lines} lines "
                f"(target: {SKILLS_TOTAL_TARGET}, max: {SKILLS_TOTAL_MAX})"
            )

        # 2. Check READMEs total size
        total_readme_lines = 0
        for plugin_name in PLUGINS:
            readme_path = REPO_ROOT / "plugins" / plugin_name / "README.md"
            if readme_path.exists():
                content = readme_path.read_text(encoding="utf-8")
                total_readme_lines += len(content.split("\n"))

        if total_readme_lines > README_TOTAL_MAX:
            issues.append(
                f"READMEs total: {total_readme_lines} lines "
                f"(target: {README_TOTAL_TARGET}, max: {README_TOTAL_MAX})"
            )

        # 3. Check individual README targets
        for plugin_name in PLUGINS:
            readme_path = REPO_ROOT / "plugins" / plugin_name / "README.md"
            if readme_path.exists():
                content = readme_path.read_text(encoding="utf-8")
                lines = len(content.split("\n"))
                targets = README_TARGETS[plugin_name]

                if lines > targets["max"]:
                    issues.append(
                        f"{plugin_name} README: {lines} lines "
                        f"(target: {targets['target']}, max: {targets['max']})"
                    )

        # 4. Check skills optimal range compliance
        for plugin_name in PLUGINS:
            skills_dir = REPO_ROOT / "plugins" / plugin_name / "skills"
            out_of_range = []

            for skill_name in EXPECTED_SKILLS[plugin_name]:
                skill_md = skills_dir / skill_name / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text(encoding="utf-8")
                    lines = len(content.split("\n"))

                    if lines < SKILL_OPTIMAL_MIN_LINES or lines > SKILL_ABSOLUTE_MAX_LINES:
                        out_of_range.append(f"{skill_name}: {lines} lines")

            if out_of_range:
                issues.append(
                    f"{plugin_name} skills out of range (250-450):\n    "
                    + "\n    ".join(out_of_range)
                )

        # Summary
        assert len(issues) == 0, (
            f"Phase 2 reduction targets NOT MET. {len(issues)} issues found:\n\n"
            + "\n".join(f"  ✗ {issue}" for issue in issues)
            + f"\n\nPhase 2 Targets:\n"
            f"  - Skills: {SKILLS_TOTAL_TARGET} lines total, 250-400 per skill\n"
            f"  - READMEs: {README_TOTAL_TARGET} lines total\n"
            f"    - visual-iteration: ≤500 lines\n"
            f"    - epti: ≤350 lines\n"
            f"    - agent-loop: ≤200 lines"
        )
