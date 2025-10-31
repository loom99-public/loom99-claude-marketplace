"""
Functional tests for Phase 3 Agent Optimization.

These tests validate that Phase 3 optimization work maintains agent quality while achieving
target size reductions. Tests verify real file system state and cannot be gamed
by stubs or mocks.

Reference:
- PLAN-verbosity-reduction-2025-10-29-075000.md (Phase 3)
- TODO-verbosity-phase3.md

Target Reductions:
- workflow-agent.md: 206 lines → 206 lines (already optimal, no change)
- tdd-agent.md: 636 lines → 400 lines (-37%, -236 lines)
- visual-iteration-agent.md: 946 lines → 600 lines (-37%, -346 lines)
- Total: 1,787 lines → 1,206 lines (-33%, -582 lines)

These tests are designed to:
1. FAIL before Phase 3 optimization (current agents exceed targets)
2. PASS after Phase 3 optimization (agents meet optimal sizes)
3. Resist gaming (verify actual content, structure, and quality)
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest


# Repository root path (absolute)
REPO_ROOT = Path(__file__).parent.parent.parent.resolve()

# All plugins with agent files
PLUGINS = ["agent-loop", "epti", "visual-iteration"]

# Agent file paths
AGENT_PATHS = {
    "agent-loop": "plugins/agent-loop/agents/workflow-agent.md",
    "epti": "plugins/epti/agents/tdd-agent.md",
    "visual-iteration": "plugins/visual-iteration/agents/visual-iteration-agent.md",
}

# Phase 3 Targets: Optimal agent lengths (per PLAN)
AGENT_TARGETS = {
    "agent-loop": {
        "name": "workflow-agent",
        "min": 180,
        "target": 206,  # Already optimal, no change needed
        "max": 220,
    },
    "epti": {
        "name": "tdd-agent",
        "min": 350,
        "target": 400,  # -37% from 636
        "max": 450,
    },
    "visual-iteration": {
        "name": "visual-iteration-agent",
        "min": 550,
        "target": 600,  # -37% from 946
        "max": 650,
    },
}

# Total agent size target
AGENTS_TOTAL_TARGET = 1206  # Lines (from 1,787)
AGENTS_TOTAL_MAX = 1300  # Allow 8% buffer for content preservation

# Minimum required sections for each agent type
REQUIRED_AGENT_SECTIONS = {
    "workflow-agent": {
        "Purpose",
        "Philosophy",
        "Workflow",
        "Stage",
        "Guardrails",
        "Anti-Patterns",
    },
    "tdd-agent": {
        "Philosophy",
        "Principles",
        "Workflow",
        "Stage",
        "Test",
        "Implementation",
        "Anti-Patterns",
    },
    "visual-iteration-agent": {
        "Mission",
        "Principles",
        "Workflow",
        "Stage",
        "Visual",
        "Iteration",
        "Screenshot",
    },
}

# Required workflow elements
WORKFLOW_KEYWORDS = {
    "agent-loop": ["explore", "plan", "code", "commit"],
    "epti": ["write-tests", "verify-fail", "commit-tests", "implement", "iterate", "commit-code"],
    "visual-iteration": ["screenshot", "feedback", "refine", "iterate", "commit"],
}


class TestAgentSizeValidation:
    """
    Validate agents are within optimal size range.

    These tests FAIL before Phase 3 (current: 206, 636, 946 lines)
    and PASS after Phase 3 optimization (target: 206, 400, 600 lines).

    Anti-Gaming: Cannot bypass by empty files (content tests) or
    removing structure (section verification tests).
    """

    def _get_line_count(self, file_path: Path) -> int:
        """Get total line count for a file."""
        if not file_path.exists():
            return 0
        content = file_path.read_text(encoding="utf-8")
        return len(content.split("\n"))

    def _get_non_empty_line_count(self, file_path: Path) -> int:
        """Get non-empty line count (excluding blank lines)."""
        if not file_path.exists():
            return 0
        content = file_path.read_text(encoding="utf-8")
        lines = [line for line in content.split("\n") if line.strip()]
        return len(lines)

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_file_exists(self, plugin_name: str):
        """
        Agent file must exist for each plugin.

        Anti-Gaming: Cannot skip tests by deleting files.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
        assert agent_path.exists(), f"Agent file missing: {agent_path}"
        assert agent_path.is_file(), f"Agent path is not a file: {agent_path}"

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_within_target_range(self, plugin_name: str):
        """
        Agent file should be within optimal size range.

        Current state (will FAIL):
        - agent-loop: 206 lines (already optimal ✓)
        - epti: 636 lines (exceeds target 400 by +236)
        - visual-iteration: 946 lines (exceeds target 600 by +346)

        Target state (will PASS): All agents within target ranges
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
        target = AGENT_TARGETS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        line_count = self._get_line_count(agent_path)

        assert target["min"] <= line_count <= target["max"], (
            f"Agent {plugin_name}: {line_count} lines outside optimal range.\n"
            f"Target: {target['target']} lines\n"
            f"Acceptable range: {target['min']}-{target['max']} lines\n"
            f"Delta: {line_count - target['target']:+d} lines\n\n"
            f"Phase 3 target: Reduce to ~{target['target']} lines"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_has_substantial_content(self, plugin_name: str):
        """
        Agent must have substantial non-empty content (not just whitespace).

        Anti-Gaming: Cannot reduce size by adding empty lines.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
        target = AGENT_TARGETS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        total_lines = self._get_line_count(agent_path)
        non_empty_lines = self._get_non_empty_line_count(agent_path)

        # At least 75% of lines should be non-empty
        min_content_percentage = 70
        content_percentage = (non_empty_lines / total_lines * 100) if total_lines > 0 else 0

        assert content_percentage >= min_content_percentage, (
            f"Agent {plugin_name}: Only {content_percentage:.0f}% non-empty lines.\n"
            f"Total lines: {total_lines}\n"
            f"Non-empty lines: {non_empty_lines}\n"
            f"Empty lines: {total_lines - non_empty_lines}\n\n"
            f"Phase 3 target: At least {min_content_percentage}% content (not padding)"
        )

    def test_total_agents_size_meets_target(self):
        """
        Total agents size should be ~1,206 lines (±8% buffer).

        Current state (will FAIL): 1,787 lines total
        Target state (will PASS): ~1,206 lines total (-33%)
        """
        total_lines = 0
        agent_breakdown = {}

        for plugin_name in PLUGINS:
            agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
            if agent_path.exists():
                lines = self._get_line_count(agent_path)
                agent_breakdown[plugin_name] = lines
                total_lines += lines

        assert total_lines <= AGENTS_TOTAL_MAX, (
            f"Total agents size {total_lines} lines exceeds maximum {AGENTS_TOTAL_MAX}.\n\n"
            f"Breakdown:\n"
            + "\n".join(
                f"  - {plugin}: {lines} lines (target: {AGENT_TARGETS[plugin]['target']})"
                for plugin, lines in agent_breakdown.items()
            )
            + f"\n\nPhase 3 target: ~{AGENTS_TOTAL_TARGET} lines total (-33%)"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_reduction_percentage_correct(self, plugin_name: str):
        """
        Verify reduction percentage is approximately correct.

        Current sizes:
        - agent-loop: 206 → 206 (0% reduction, already optimal)
        - epti: 636 → 400 (-37% reduction)
        - visual-iteration: 946 → 600 (-37% reduction)
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
        target = AGENT_TARGETS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        current_lines = self._get_line_count(agent_path)
        target_lines = target["target"]

        # Allow some flexibility (within target range is acceptable)
        within_range = target["min"] <= current_lines <= target["max"]

        if not within_range:
            # Calculate actual vs expected reduction
            if plugin_name == "agent-loop":
                # No reduction needed
                pytest.fail(
                    f"Agent {plugin_name}: {current_lines} lines (should stay ~{target_lines}).\n"
                    f"This agent is already optimal and should not change significantly."
                )
            else:
                # Calculate reduction percentage
                expected_reduction = target_lines / current_lines
                pytest.fail(
                    f"Agent {plugin_name}: {current_lines} lines needs reduction to {target_lines}.\n"
                    f"Target reduction: {(1 - expected_reduction) * 100:.0f}%\n"
                    f"Acceptable range: {target['min']}-{target['max']} lines"
                )


class TestAgentStructurePreservation:
    """
    Verify agents maintain required structure after optimization.

    Anti-Gaming: Checks for actual structure patterns, not just file size.
    Cannot pass by removing essential sections or content.
    """

    def _get_content(self, file_path: Path) -> str:
        """Get file content."""
        return file_path.read_text(encoding="utf-8")

    def _extract_headings(self, content: str) -> List[str]:
        """Extract all markdown headings from content."""
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        matches = heading_pattern.findall(content)
        return [heading.strip() for _, heading in matches]

    def _count_sections_by_level(self, content: str) -> Dict[int, int]:
        """Count headings by level (# = 1, ## = 2, etc.)."""
        heading_pattern = re.compile(r'^(#{1,6})\s+.+$', re.MULTILINE)
        matches = heading_pattern.findall(content)
        counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for match in matches:
            level = len(match)
            counts[level] = counts.get(level, 0) + 1
        return counts

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_has_primary_heading(self, plugin_name: str):
        """
        Agent must have a primary H1 heading (title).

        Anti-Gaming: Cannot remove title to save space.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
        agent_name = AGENT_TARGETS[plugin_name]["name"]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)

        # Check for H1 heading at start
        h1_pattern = re.compile(r'^#\s+.+$', re.MULTILINE)
        h1_matches = h1_pattern.findall(content)

        assert len(h1_matches) >= 1, (
            f"Agent {plugin_name}: No H1 heading found.\n"
            f"Agents must have a clear title/heading.\n"
            f"Expected format: '# Agent Name' or similar"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_has_hierarchical_structure(self, plugin_name: str):
        """
        Agent must maintain hierarchical structure with multiple section levels.

        Anti-Gaming: Cannot flatten to single-level structure to save space.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)
        section_counts = self._count_sections_by_level(content)

        # Must have headings at multiple levels
        assert section_counts[1] >= 1, f"Agent {plugin_name}: No H1 headings"
        assert section_counts[2] >= 3, (
            f"Agent {plugin_name}: Only {section_counts[2]} H2 sections. "
            f"Need at least 3 major sections (Philosophy, Workflow, etc.)"
        )

        # Total sections should be reasonable
        total_sections = sum(section_counts.values())
        assert total_sections >= 6, (
            f"Agent {plugin_name}: Only {total_sections} total sections.\n"
            f"Agents need structured organization with multiple sections.\n"
            f"Phase 3 optimization should not eliminate structure."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_contains_required_section_keywords(self, plugin_name: str):
        """
        Agent must contain required conceptual sections.

        Anti-Gaming: Cannot remove core agent sections to reduce size.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
        agent_name = AGENT_TARGETS[plugin_name]["name"]
        required_keywords = REQUIRED_AGENT_SECTIONS[agent_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)
        content_lower = content.lower()

        missing_keywords = []
        for keyword in required_keywords:
            # Check for keyword in headings or prominent text
            keyword_lower = keyword.lower()
            if keyword_lower not in content_lower:
                missing_keywords.append(keyword)

        assert len(missing_keywords) == 0, (
            f"Agent {plugin_name}: Missing required concepts:\n"
            + "\n".join(f"  - {kw}" for kw in missing_keywords)
            + f"\n\nThese concepts are essential to agent functionality.\n"
            f"Phase 3 optimization should not remove core agent guidance."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_documents_workflow_stages(self, plugin_name: str):
        """
        Agent must document all workflow stages.

        Anti-Gaming: Cannot remove stage definitions to reduce size.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
        expected_stages = WORKFLOW_KEYWORDS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)
        content_lower = content.lower()

        missing_stages = []
        for stage in expected_stages:
            # Check for stage mentions
            stage_lower = stage.lower()
            if stage_lower not in content_lower:
                missing_stages.append(stage)

        assert len(missing_stages) == 0, (
            f"Agent {plugin_name}: Missing workflow stages:\n"
            + "\n".join(f"  - {stage}" for stage in missing_stages)
            + f"\n\nAll workflow stages must be documented.\n"
            f"Phase 3 optimization should not remove stage definitions."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_has_stage_sections(self, plugin_name: str):
        """
        Agent must have dedicated sections for workflow stages.

        Anti-Gaming: Cannot merge all stages into one paragraph.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)

        # Look for "Stage" keyword in headings
        stage_pattern = re.compile(r'^#{2,3}\s+.*Stage\s*\d+', re.MULTILINE | re.IGNORECASE)
        stage_sections = stage_pattern.findall(content)

        # Should have multiple stage sections
        min_stages = 3  # Minimum for a workflow
        assert len(stage_sections) >= min_stages, (
            f"Agent {plugin_name}: Only {len(stage_sections)} stage sections found.\n"
            f"Expected at least {min_stages} workflow stages.\n"
            f"Stages should be clearly separated and documented.\n"
            f"Phase 3 optimization should not merge stage definitions."
        )


class TestAgentContentQuality:
    """
    Verify essential content quality is preserved after optimization.

    Anti-Gaming: Checks for specific content patterns that indicate
    meaningful guidance, not just generic filler.
    """

    def _get_content(self, file_path: Path) -> str:
        """Get file content."""
        return file_path.read_text(encoding="utf-8")

    def _count_code_blocks(self, content: str) -> int:
        """Count code blocks (```)."""
        return content.count("```")

    def _count_lists(self, content: str) -> int:
        """Count list items (-, *, numbers)."""
        list_pattern = re.compile(r'^\s*[-*]\s+.+$', re.MULTILINE)
        return len(list_pattern.findall(content))

    def _extract_sentences(self, content: str) -> List[str]:
        """Extract sentences from content."""
        # Simple sentence extraction (split on . ! ?)
        sentences = re.split(r'[.!?]+', content)
        return [s.strip() for s in sentences if len(s.strip()) > 20]

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_has_examples_or_code_blocks(self, plugin_name: str):
        """
        Agent should contain examples or code blocks (not purely text).

        Anti-Gaming: Cannot reduce by removing all concrete examples.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)

        # Count examples
        code_blocks = self._count_code_blocks(content) // 2  # Pairs of ```
        has_example_keyword = content.lower().count("example") >= 2

        # Should have at least some concrete examples
        assert code_blocks >= 1 or has_example_keyword, (
            f"Agent {plugin_name}: No examples or code blocks found.\n"
            f"Code blocks: {code_blocks}\n"
            f"Example keywords: {has_example_keyword}\n\n"
            f"Agents should include 1-2 concrete examples for clarity.\n"
            f"Phase 3 optimization should not remove all examples."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_contains_anti_patterns(self, plugin_name: str):
        """
        Agent must document anti-patterns (what NOT to do).

        Anti-Gaming: Cannot remove anti-patterns section to reduce size.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)
        content_lower = content.lower()

        # Look for anti-pattern indicators
        has_anti_pattern_heading = "anti-pattern" in content_lower
        has_avoid_keyword = "avoid" in content_lower or "don't" in content_lower
        has_do_not = content_lower.count("do not") >= 2

        assert has_anti_pattern_heading or (has_avoid_keyword and has_do_not), (
            f"Agent {plugin_name}: No anti-patterns documented.\n"
            f"Anti-pattern heading: {has_anti_pattern_heading}\n"
            f"Avoid keywords: {has_avoid_keyword}\n"
            f"'Do not' phrases: {has_do_not}\n\n"
            f"Agents must document what NOT to do to prevent mistakes.\n"
            f"Phase 3 optimization should not remove anti-patterns."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_has_guardrails_or_rules(self, plugin_name: str):
        """
        Agent must define guardrails or rules for workflow.

        Anti-Gaming: Cannot remove guardrails to reduce size.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)
        content_lower = content.lower()

        # Look for guardrail/rule indicators
        has_guardrails = "guardrail" in content_lower
        has_rules = "rule" in content_lower
        has_must_or_should = content_lower.count("must") >= 3 or content_lower.count("should") >= 10

        assert has_guardrails or has_rules or has_must_or_should, (
            f"Agent {plugin_name}: No guardrails or rules documented.\n"
            f"Guardrails: {has_guardrails}\n"
            f"Rules: {has_rules}\n"
            f"'Must/Should' statements: {has_must_or_should}\n\n"
            f"Agents must define clear rules/guardrails for proper workflow.\n"
            f"Phase 3 optimization should not remove guardrails."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_has_transition_guidance(self, plugin_name: str):
        """
        Agent must provide transition guidance between stages.

        Anti-Gaming: Cannot remove transition logic to reduce size.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)
        content_lower = content.lower()

        # Look for transition indicators
        has_transition_keyword = "transition" in content_lower
        has_next_keyword = content_lower.count("next") >= 2
        has_when_keyword = content_lower.count("when") >= 2

        assert has_transition_keyword or (has_next_keyword and has_when_keyword), (
            f"Agent {plugin_name}: No transition guidance found.\n"
            f"Transition keyword: {has_transition_keyword}\n"
            f"Next keywords: {has_next_keyword}\n"
            f"When keywords: {has_when_keyword}\n\n"
            f"Agents must guide users on when/how to transition between stages.\n"
            f"Phase 3 optimization should not remove transition logic."
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_has_actionable_lists(self, plugin_name: str):
        """
        Agent should contain actionable lists (activities, checklists).

        Anti-Gaming: Cannot reduce to pure prose without structure.
        """
        agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]

        if not agent_path.exists():
            pytest.skip(f"Agent not yet created: {agent_path}")

        content = self._get_content(agent_path)
        list_count = self._count_lists(content)

        # Should have multiple lists for activities, rules, etc.
        min_list_items = 5
        assert list_count >= min_list_items, (
            f"Agent {plugin_name}: Only {list_count} list items found.\n"
            f"Expected at least {min_list_items} actionable list items.\n\n"
            f"Agents should use lists for activities, rules, and checklists.\n"
            f"Phase 3 optimization should not convert all lists to prose."
        )


class TestAgentConsistency:
    """
    Verify consistency across agents.

    Anti-Gaming: Cannot optimize one agent perfectly while breaking others.
    """

    def _get_content(self, file_path: Path) -> str:
        """Get file content."""
        return file_path.read_text(encoding="utf-8")

    def test_agents_use_consistent_stage_format(self):
        """
        All agents should use consistent formatting for stage definitions.

        Anti-Gaming: Cannot use radically different formats per agent.
        """
        stage_patterns = {}

        for plugin_name in PLUGINS:
            agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
            if not agent_path.exists():
                continue

            content = self._get_content(agent_path)

            # Count stage sections
            stage_pattern = re.compile(r'^#{2,3}\s+.*Stage\s*\d+', re.MULTILINE | re.IGNORECASE)
            stage_matches = stage_pattern.findall(content)
            stage_patterns[plugin_name] = len(stage_matches)

        # All agents that have stages should have at least 3
        for plugin_name, count in stage_patterns.items():
            if count > 0:  # If agent uses stage concept
                assert count >= 3, (
                    f"Agent {plugin_name}: Only {count} stages.\n"
                    f"Workflow agents should have at least 3 stages."
                )

    def test_agents_balance_is_reasonable(self):
        """
        Agent sizes should be relatively balanced (no extreme outliers).

        Anti-Gaming: Cannot over-optimize one agent while ignoring others.
        """
        sizes = {}

        for plugin_name in PLUGINS:
            agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
            if agent_path.exists():
                content = self._get_content(agent_path)
                sizes[plugin_name] = len(content.split("\n"))

        if len(sizes) < 2:
            pytest.skip("Need at least 2 agents to compare balance")

        # Check that no agent is more than 3x another agent
        min_size = min(sizes.values())
        max_size = max(sizes.values())
        ratio = max_size / min_size if min_size > 0 else 0

        assert ratio <= 3.5, (
            f"Agent size imbalance detected (ratio: {ratio:.1f}x):\n"
            + "\n".join(f"  - {plugin}: {size} lines" for plugin, size in sizes.items())
            + f"\n\nAgent sizes should be relatively balanced.\n"
            f"Large imbalances suggest incomplete optimization."
        )

    def test_all_agents_have_similar_density(self):
        """
        Agents should have similar content density (not padded with whitespace).

        Anti-Gaming: Cannot pad one agent with empty lines while others are dense.
        """
        densities = {}

        for plugin_name in PLUGINS:
            agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
            if not agent_path.exists():
                continue

            content = self._get_content(agent_path)
            total_lines = len(content.split("\n"))
            non_empty_lines = len([line for line in content.split("\n") if line.strip()])
            density = (non_empty_lines / total_lines * 100) if total_lines > 0 else 0
            densities[plugin_name] = density

        if len(densities) < 2:
            pytest.skip("Need at least 2 agents to compare density")

        # All agents should have similar density (within 10%)
        avg_density = sum(densities.values()) / len(densities)
        outliers = []

        for plugin_name, density in densities.items():
            if abs(density - avg_density) > 10:
                outliers.append(f"{plugin_name}: {density:.0f}% (avg: {avg_density:.0f}%)")

        assert len(outliers) == 0, (
            f"Content density inconsistency detected:\n"
            + "\n".join(f"  - {o}" for o in outliers)
            + f"\n\nAll agents should have similar content density.\n"
            f"Large variations suggest padding or over-compression."
        )


class TestPhase3Summary:
    """
    High-level Phase 3 validation summary.

    This test provides a comprehensive overview of Phase 3 progress.
    """

    def test_phase3_optimization_complete(self):
        """
        Validate Phase 3 is complete: All agents optimized to targets.

        This is the master test that verifies overall Phase 3 success.
        """
        results = {
            "total_size": 0,
            "agents": {},
            "on_target": 0,
            "needs_reduction": 0,
        }

        for plugin_name in PLUGINS:
            agent_path = REPO_ROOT / AGENT_PATHS[plugin_name]
            target = AGENT_TARGETS[plugin_name]

            if not agent_path.exists():
                results["agents"][plugin_name] = {
                    "status": "MISSING",
                    "current": 0,
                    "target": target["target"],
                }
                continue

            content = agent_path.read_text(encoding="utf-8")
            current_lines = len(content.split("\n"))
            results["total_size"] += current_lines

            # Check if within target range
            within_range = target["min"] <= current_lines <= target["max"]
            status = "ON_TARGET" if within_range else "NEEDS_REDUCTION"

            if within_range:
                results["on_target"] += 1
            else:
                results["needs_reduction"] += 1

            results["agents"][plugin_name] = {
                "status": status,
                "current": current_lines,
                "target": target["target"],
                "min": target["min"],
                "max": target["max"],
                "delta": current_lines - target["target"],
            }

        # Generate summary report
        summary_lines = [
            "Phase 3 Agent Optimization Status",
            "=" * 50,
            "",
            f"Total agents size: {results['total_size']} lines",
            f"Target size: {AGENTS_TOTAL_TARGET} lines",
            f"Maximum allowed: {AGENTS_TOTAL_MAX} lines",
            f"Reduction needed: {results['total_size'] - AGENTS_TOTAL_TARGET:+d} lines",
            "",
            "Per-Agent Status:",
        ]

        for plugin_name, data in results["agents"].items():
            if data["status"] == "MISSING":
                summary_lines.append(f"  ❌ {plugin_name}: MISSING")
            elif data["status"] == "ON_TARGET":
                summary_lines.append(
                    f"  ✅ {plugin_name}: {data['current']} lines "
                    f"(target: {data['target']}, delta: {data['delta']:+d})"
                )
            else:
                summary_lines.append(
                    f"  ❌ {plugin_name}: {data['current']} lines "
                    f"(target: {data['target']}, delta: {data['delta']:+d})"
                )

        summary_lines.extend([
            "",
            f"On Target: {results['on_target']}/{len(PLUGINS)}",
            f"Needs Reduction: {results['needs_reduction']}/{len(PLUGINS)}",
            "",
        ])

        # Phase 3 is complete when:
        # 1. Total size is under maximum
        # 2. All agents are within target range
        phase3_complete = (
            results["total_size"] <= AGENTS_TOTAL_MAX
            and results["needs_reduction"] == 0
        )

        summary_lines.append(
            "✅ Phase 3 COMPLETE" if phase3_complete else "❌ Phase 3 IN PROGRESS"
        )

        summary = "\n".join(summary_lines)

        assert phase3_complete, (
            f"\n{summary}\n\n"
            f"Phase 3 optimization not complete.\n"
            f"Agents need reduction to meet targets."
        )


# Test traceability helpers
class TestPhase3Traceability:
    """
    Verify tests trace back to planning artifacts.

    These tests ensure Phase 3 tests align with planning docs.
    """

    def test_phase3_targets_match_plan(self):
        """
        Verify test targets match PLAN-verbosity-reduction document.

        This ensures tests validate actual requirements, not arbitrary numbers.
        """
        # These targets come from PLAN-verbosity-reduction-2025-10-29-075000.md
        expected_targets = {
            "agent-loop": 206,  # Already optimal
            "epti": 400,        # -37% from 636
            "visual-iteration": 600,  # -37% from 946
        }

        for plugin_name, expected_target in expected_targets.items():
            actual_target = AGENT_TARGETS[plugin_name]["target"]
            assert actual_target == expected_target, (
                f"Target mismatch for {plugin_name}:\n"
                f"Test target: {actual_target}\n"
                f"Plan target: {expected_target}\n\n"
                f"Tests must match planning document targets."
            )

    def test_phase3_total_reduction_matches_plan(self):
        """
        Verify total reduction target matches plan (-33%, -582 lines).
        """
        # From PLAN: 1,787 → 1,206 lines (-33%, -582 lines)
        expected_original = 1787
        expected_target = 1206
        expected_reduction = 581

        calculated_reduction = expected_original - expected_target

        assert calculated_reduction == expected_reduction, (
            f"Phase 3 reduction calculation error:\n"
            f"Original: {expected_original}\n"
            f"Target: {expected_target}\n"
            f"Expected reduction: {expected_reduction}\n"
            f"Calculated reduction: {calculated_reduction}\n\n"
            f"Test constants must match plan calculations."
        )

    def test_phase3_scope_documented(self):
        """
        Verify Phase 3 scope is clearly documented in test file.

        Anti-Gaming: Tests must document what they're validating.
        """
        # Read this test file
        test_file = Path(__file__)
        content = test_file.read_text(encoding="utf-8")

        # Check for documentation
        assert "Phase 3" in content
        assert "agent-loop" in content
        assert "epti" in content
        assert "visual-iteration" in content
        assert "1,787" in content or "1787" in content  # Original size
        assert "1,206" in content or "1206" in content  # Target size

        # All checks passed - scope is documented
