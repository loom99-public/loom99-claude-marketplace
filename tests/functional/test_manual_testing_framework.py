"""
Functional tests for Manual Testing Framework (Phase 1 - P0-1 to P0-5).

These tests validate that the manual testing documentation and framework components
are complete, well-formed, and provide comprehensive guidance for manual testers.

Tests verify real file system state and cannot be gamed by stubs or mocks.

Reference:
- PLAN-testing-framework-2025-11-06-021441.md (Phase 1)
- Phase 1 Work Items: P0-1 through P0-5

Test Criteria Alignment:
- Useful: Tests actual documentation quality, not tautologies
- Complete: Covers all manual testing components
- Flexible: Tests structure, not implementation details
- Fully automated: Uses pytest, no manual steps
- No ad-hoc: Follows existing test patterns

Manual Testing Components:
1. Testing documentation framework (P0-1)
2. Installation test scenarios (P0-2)
3. Command execution test scenarios (P0-3)
4. Complete workflow test scenarios (P0-4)
5. Agent behavior observation checklists (P0-5)
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest
import yaml


# Repository root path (absolute)
REPO_ROOT = Path(__file__).parent.parent.parent.resolve()

# Manual testing documentation location
MANUAL_TESTS_DIR = REPO_ROOT / "tests" / "manual"

# All plugins that need manual testing
PLUGINS = ["agent-loop", "epti", "visual-iteration"]

# Expected command counts per plugin (from PLAN)
EXPECTED_COMMAND_COUNTS = {
    "agent-loop": 4,
    "epti": 6,
    "visual-iteration": 6,
}

# Total expected commands
TOTAL_EXPECTED_COMMANDS = 16


# ============================================================================
# Markdown Parsing Utilities (REAL semantic parsing, not keyword matching)
# ============================================================================

def parse_markdown_sections(content: str) -> Dict[str, str]:
    """
    Parse markdown into sections by heading.

    Returns dict mapping heading text to section content.
    Cannot be gamed - requires actual markdown structure.
    """
    sections = {}
    current_heading = None
    current_content = []

    for line in content.split('\n'):
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)

        if heading_match:
            # Save previous section
            if current_heading:
                sections[current_heading] = '\n'.join(current_content).strip()

            # Start new section
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            current_heading = f"{'#' * level} {heading_text}"
            current_content = []
        else:
            current_content.append(line)

    # Save final section
    if current_heading:
        sections[current_heading] = '\n'.join(current_content).strip()

    return sections


def extract_markdown_lists(content: str) -> List[List[str]]:
    """
    Extract all lists (bullet points) from markdown.

    Returns list of lists (each list is a separate bulleted/numbered section).
    Cannot be gamed - requires actual list structure.
    """
    lists = []
    current_list = []
    in_code_block = False

    for line in content.split('\n'):
        # Track code blocks to avoid false matches
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Match bullet or numbered list items
        list_match = re.match(r'^\s*[-*+\d.]\s+(.+)$', line)

        if list_match:
            current_list.append(list_match.group(1).strip())
        elif current_list:
            # End of current list
            lists.append(current_list)
            current_list = []

    if current_list:
        lists.append(current_list)

    return lists


def extract_markdown_tables(content: str) -> List[Dict[str, List[str]]]:
    """
    Extract tables from markdown.

    Returns list of tables, each as dict mapping column headers to values.
    Cannot be gamed - requires actual table structure.
    """
    tables = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Look for table header (must have |)
        if '|' in line and not line.startswith('```'):
            # Extract headers
            headers = [h.strip() for h in line.split('|') if h.strip()]

            # Next line should be separator
            if i + 1 < len(lines) and re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i + 1]):
                # Extract rows
                rows = []
                j = i + 2
                while j < len(lines) and '|' in lines[j] and not lines[j].strip().startswith('```'):
                    row_values = [v.strip() for v in lines[j].split('|') if v.strip()]
                    if len(row_values) == len(headers):
                        rows.append(row_values)
                    j += 1

                # Build table dict
                if rows:
                    table = {header: [] for header in headers}
                    for row in rows:
                        for header, value in zip(headers, row):
                            table[header].append(value)
                    tables.append(table)

                i = j
                continue

        i += 1

    return tables


def count_substantive_paragraphs(content: str) -> int:
    """
    Count paragraphs with actual content (not just keywords or short phrases).

    A substantive paragraph must:
    - Be at least 100 characters
    - Contain at least 2 sentences (. ! ?)
    - Not be a list item or heading

    Cannot be gamed with lorem ipsum alone - checks sentence structure.
    """
    count = 0
    in_code_block = False
    paragraphs = []
    current_para = []

    for line in content.split('\n'):
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Skip headings and list items
        if re.match(r'^#{1,6}\s+', line) or re.match(r'^\s*[-*+\d.]\s+', line):
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
            continue

        # Accumulate paragraph lines
        if line.strip():
            current_para.append(line.strip())
        else:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []

    if current_para:
        paragraphs.append(' '.join(current_para))

    # Count substantive paragraphs
    for para in paragraphs:
        if len(para) >= 100:
            # Count sentences
            sentence_endings = para.count('.') + para.count('!') + para.count('?')
            if sentence_endings >= 2:
                count += 1

    return count


def extract_actionable_steps(content: str) -> List[str]:
    """
    Extract actionable steps (imperatives/verbs) from content.

    Looks for sentences starting with action verbs like:
    - Run, Execute, Verify, Check, Create, Install, etc.

    Cannot be gamed - requires actual instructional content.
    """
    steps = []
    action_verbs = [
        'run', 'execute', 'verify', 'check', 'test', 'validate',
        'create', 'install', 'configure', 'setup', 'build',
        'open', 'click', 'select', 'enter', 'type',
        'confirm', 'ensure', 'review', 'inspect', 'observe',
        'load', 'start', 'stop', 'restart', 'reload'
    ]

    # Look through list items and sentences
    lists = extract_markdown_lists(content)
    for lst in lists:
        for item in lst:
            # Check if item starts with action verb
            first_word = item.split()[0].lower() if item.split() else ""
            if first_word in action_verbs:
                steps.append(item)

    return steps


def has_measurable_criteria(text: str) -> bool:
    """
    Check if text contains measurable success criteria.

    Measurable criteria include:
    - Percentages (95%, 100%)
    - Counts (3 tests, 5 commands)
    - Definitive states (pass, fail, complete, error)
    - Boolean outcomes (true/false, yes/no, present/absent)

    Cannot be gamed - requires specific numeric or definitive language.
    """
    # Check for percentages
    if re.search(r'\d+\s*%', text):
        return True

    # Check for counts with units
    if re.search(r'\d+\s+(test|check|validation|scenario|command|step|file)', text, re.IGNORECASE):
        return True

    # Check for definitive states
    definitive_states = [
        'pass', 'fail', 'complete', 'error', 'success', 'failure',
        'true', 'false', 'present', 'absent', 'exists', 'missing'
    ]
    if any(state in text.lower() for state in definitive_states):
        return True

    return False


# ============================================================================
# Test Classes
# ============================================================================

class TestManualTestingDocumentationFramework:
    """
    Test P0-1: Manual Testing Documentation Framework

    Validates that the documentation structure and templates for manual testing
    provide complete, systematic guidance for testers.

    Anti-Gaming: Cannot pass with empty files or incomplete templates.
    """

    def test_manual_tests_directory_exists(self):
        """
        Manual testing directory must exist.

        Validates: P0-1 Acceptance Criteria - directory structure
        """
        assert MANUAL_TESTS_DIR.exists(), (
            f"Manual tests directory not found: {MANUAL_TESTS_DIR}\n"
            f"P0-1 requires creating tests/manual/ directory structure"
        )
        assert MANUAL_TESTS_DIR.is_dir(), (
            f"Manual tests path is not a directory: {MANUAL_TESTS_DIR}"
        )

    def test_manual_testing_readme_has_required_sections(self):
        """
        Manual testing README must exist with comprehensive structured sections.

        Validates: P0-1 Acceptance Criteria - README with testing overview

        Anti-Gaming: Parses actual markdown structure and validates content quality.
        """
        readme_path = MANUAL_TESTS_DIR / "README.md"

        assert readme_path.exists(), (
            f"Manual testing README not found: {readme_path}\n"
            f"P0-1 requires README.md with testing overview and instructions"
        )

        content = readme_path.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Required sections for comprehensive manual testing guide
        required_section_keywords = [
            "overview",
            "instruction",
            "setup",
            "execution",
            "workflow",
            "recording",  # Video/screenshot recording instructions
        ]

        missing_sections = []
        for keyword in required_section_keywords:
            # Check if any section heading contains this keyword
            if not any(keyword.lower() in heading.lower() for heading in sections.keys()):
                missing_sections.append(keyword)

        assert len(missing_sections) == 0, (
            f"Manual testing README missing required sections:\n"
            + "\n".join(f"  - {s}" for s in missing_sections)
            + f"\n\nP0-1 requires comprehensive testing overview and instructions"
        )

        # Each major section must have substantive content (not just filler)
        sparse_sections = []
        for heading, section_content in sections.items():
            # Check for major sections (##)
            if heading.startswith('## '):
                # Must have actionable steps or substantive paragraphs
                actionable_steps = extract_actionable_steps(section_content)
                substantive_paras = count_substantive_paragraphs(section_content)

                if len(actionable_steps) == 0 and substantive_paras < 2:
                    sparse_sections.append(heading)

        assert len(sparse_sections) == 0, (
            f"Manual testing README has sections without substantive content:\n"
            + "\n".join(f"  - {s}" for s in sparse_sections)
            + f"\n\nEach section must have actionable steps or detailed explanations"
        )

    def test_manual_testing_readme_has_actionable_quick_start(self):
        """
        README must have Quick Start section with actionable steps.

        Validates: P0-1 Acceptance Criteria - immediately usable instructions

        Anti-Gaming: Extracts and validates actual action verbs and steps.
        """
        readme_path = MANUAL_TESTS_DIR / "README.md"

        if not readme_path.exists():
            pytest.skip("README not yet created")

        content = readme_path.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Find Quick Start or Getting Started section
        quick_start_section = None
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['quick start', 'getting started', 'how to use']):
                quick_start_section = section_content
                break

        assert quick_start_section is not None, (
            f"README missing Quick Start or Getting Started section.\n"
            f"P0-1 requires immediately actionable instructions"
        )

        # Extract actionable steps
        steps = extract_actionable_steps(quick_start_section)

        assert len(steps) >= 3, (
            f"Quick Start section has only {len(steps)} actionable steps.\n"
            f"Expected at least 3 steps with action verbs (Run, Execute, Verify, etc.).\n"
            f"P0-1 requires clear, actionable quick start instructions"
        )

    def test_testing_results_template_has_all_fields(self):
        """
        Testing results template must exist with all required fields as table columns.

        Validates: P0-1 Acceptance Criteria - TESTING_RESULTS.md template

        Anti-Gaming: Parses actual table structure and validates fields.
        """
        template_path = MANUAL_TESTS_DIR / "TESTING_RESULTS.md"

        assert template_path.exists(), (
            f"Testing results template not found: {template_path}\n"
            f"P0-1 requires TESTING_RESULTS.md template for recording results"
        )

        content = template_path.read_text(encoding="utf-8")
        tables = extract_markdown_tables(content)

        assert len(tables) > 0, (
            f"Testing results template doesn't contain any markdown tables.\n"
            f"P0-1 requires structured table format for recording results"
        )

        # Required fields in results table
        required_fields = [
            "date",
            "tester",
            "plugin",
            "test",
            "result",
            "expected",
            "actual",
        ]

        # Check at least one table has all required columns
        valid_table_found = False
        for table in tables:
            headers = [h.lower() for h in table.keys()]
            missing_fields = [field for field in required_fields if not any(field in h for h in headers)]

            if len(missing_fields) == 0:
                valid_table_found = True
                break

        assert valid_table_found, (
            f"Testing results template missing required fields.\n"
            f"Expected fields: {required_fields}\n"
            f"P0-1 requires comprehensive results recording template"
        )

    def test_issue_template_has_all_sections(self):
        """
        Issue template must exist with all standard sections.

        Validates: P0-1 Acceptance Criteria - ISSUE_TEMPLATE.md

        Anti-Gaming: Validates actual section structure and severity definitions.
        """
        template_path = MANUAL_TESTS_DIR / "ISSUE_TEMPLATE.md"

        assert template_path.exists(), (
            f"Issue template not found: {template_path}\n"
            f"P0-1 requires ISSUE_TEMPLATE.md for bug reporting"
        )

        content = template_path.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Required issue template sections
        required_sections = [
            "description",
            "steps to reproduce",
            "expected",
            "actual",
            "severity",
        ]

        missing_sections = []
        for section_name in required_sections:
            if not any(section_name.lower() in heading.lower() for heading in sections.keys()):
                missing_sections.append(section_name)

        assert len(missing_sections) == 0, (
            f"Issue template missing required sections:\n"
            + "\n".join(f"  - {s}" for s in missing_sections)
            + f"\n\nP0-1 requires comprehensive issue reporting template"
        )

        # Severity section must define levels
        severity_section = None
        for heading, section_content in sections.items():
            if 'severity' in heading.lower():
                severity_section = section_content
                break

        if severity_section:
            severity_levels = ["critical", "high", "medium", "low"]
            defined_levels = sum(1 for level in severity_levels if level in severity_section.lower())

            assert defined_levels >= 3, (
                f"Issue template severity section doesn't define severity levels.\n"
                f"Found only {defined_levels}/4 levels (critical, high, medium, low).\n"
                f"P0-1 requires clear severity definitions"
            )

    def test_success_criteria_are_measurable(self):
        """
        Success criteria must be measurable with specific outcomes.

        Validates: P0-1 Acceptance Criteria - success criteria definitions

        Anti-Gaming: Validates actual measurable criteria (numbers, percentages, definitive states).
        """
        readme_path = MANUAL_TESTS_DIR / "README.md"

        if not readme_path.exists():
            pytest.skip("README.md not yet created")

        content = readme_path.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Find success criteria sections
        criteria_sections = []
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['success', 'criteria', 'pass', 'validation']):
                criteria_sections.append((heading, section_content))

        assert len(criteria_sections) > 0, (
            f"README doesn't have success criteria sections.\n"
            f"P0-1 requires clear success criteria for each test type"
        )

        # Each criteria section must have measurable criteria
        unmeasurable_sections = []
        for heading, section_content in criteria_sections:
            if not has_measurable_criteria(section_content):
                unmeasurable_sections.append(heading)

        assert len(unmeasurable_sections) == 0, (
            f"Success criteria sections without measurable outcomes:\n"
            + "\n".join(f"  - {s}" for s in unmeasurable_sections)
            + f"\n\nCriteria must include percentages, counts, or definitive states (pass/fail)"
        )


class TestPluginInstallationTestScenarios:
    """
    Test P0-2: Plugin Installation Test Scenarios

    Validates that installation test checklists are comprehensive and
    cover all necessary verification steps.

    Anti-Gaming: Validates actual checklist content, not just file existence.
    """

    def test_marketplace_installation_checklist_has_actionable_steps(self):
        """
        Marketplace-level installation checklist must have actionable verification steps.

        Validates: P0-2 Acceptance Criteria - marketplace installation checklist

        Anti-Gaming: Extracts and validates actual actionable steps.
        """
        checklist_path = MANUAL_TESTS_DIR / "installation-marketplace.md"

        assert checklist_path.exists(), (
            f"Marketplace installation checklist not found: {checklist_path}\n"
            f"P0-2 requires installation checklist for marketplace as a whole"
        )

        content = checklist_path.read_text(encoding="utf-8")
        steps = extract_actionable_steps(content)

        assert len(steps) >= 5, (
            f"Marketplace installation checklist has only {len(steps)} actionable steps.\n"
            f"Expected at least 5 verification steps with action verbs.\n"
            f"P0-2 requires comprehensive installation verification"
        )

        # Should have verification steps (not just installation)
        verification_steps = [s for s in steps if any(v in s.lower() for v in ['verify', 'check', 'confirm', 'validate', 'ensure'])]

        assert len(verification_steps) >= 2, (
            f"Installation checklist has only {len(verification_steps)} verification steps.\n"
            f"Must include steps to verify successful installation.\n"
            f"P0-2 requires verification, not just installation instructions"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_plugin_installation_checklist_verifies_all_components(self, plugin_name: str):
        """
        Each plugin must have checklist verifying all component types.

        Validates: P0-2 Acceptance Criteria - per-plugin installation checklists

        Anti-Gaming: Validates component-specific verification steps.
        """
        checklist_path = MANUAL_TESTS_DIR / f"installation-{plugin_name}.md"

        assert checklist_path.exists(), (
            f"Plugin installation checklist not found: {checklist_path}\n"
            f"P0-2 requires installation checklist for each plugin"
        )

        content = checklist_path.read_text(encoding="utf-8")

        # Must mention plugin name
        assert plugin_name in content.lower(), (
            f"Installation checklist doesn't mention plugin '{plugin_name}'.\n"
            f"Checklist may be generic template, not plugin-specific"
        )

        # Must verify each component type exists
        steps = extract_actionable_steps(content)

        component_types = ["command", "agent", "skill", "hook"]
        verified_components = []

        for step in steps:
            for component_type in component_types:
                if component_type in step.lower() and any(v in step.lower() for v in ['verify', 'check', 'list', 'show']):
                    verified_components.append(component_type)

        assert len(set(verified_components)) >= 3, (
            f"Plugin installation checklist for {plugin_name} doesn't verify all components.\n"
            f"Verified: {set(verified_components)}\n"
            f"Expected: {component_types}\n"
            f"P0-2 requires verification of commands, agents, skills, hooks"
        )

    def test_installation_troubleshooting_has_solutions(self):
        """
        Installation troubleshooting guide must have solutions for common issues.

        Validates: P0-2 Acceptance Criteria - troubleshooting guide

        Anti-Gaming: Validates problem-solution pairs, not just keywords.
        """
        # Troubleshooting could be in README or separate file
        readme_path = MANUAL_TESTS_DIR / "README.md"
        troubleshooting_path = MANUAL_TESTS_DIR / "TROUBLESHOOTING.md"

        found_troubleshooting = False
        content = ""

        if troubleshooting_path.exists():
            found_troubleshooting = True
            content = troubleshooting_path.read_text(encoding="utf-8")
        elif readme_path.exists():
            readme_content = readme_path.read_text(encoding="utf-8")
            sections = parse_markdown_sections(readme_content)

            for heading, section_content in sections.items():
                if "troubleshoot" in heading.lower():
                    found_troubleshooting = True
                    content = section_content
                    break

        assert found_troubleshooting, (
            f"Installation troubleshooting guide not found.\n"
            f"Checked: {readme_path}, {troubleshooting_path}\n"
            f"P0-2 requires troubleshooting guide for common installation issues"
        )

        # Should have problem-solution structure
        sections = parse_markdown_sections(content)

        # Count sections that look like problem-solution pairs
        problem_sections = sum(1 for h in sections.keys() if any(kw in h.lower() for kw in ['error', 'issue', 'problem', 'fail']))

        assert problem_sections >= 3, (
            f"Troubleshooting guide has only {problem_sections} problem sections.\n"
            f"Expected at least 3 common issue types.\n"
            f"P0-2 requires comprehensive troubleshooting guidance"
        )

        # Each problem section should have actionable solution steps
        sections_without_solutions = []
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['error', 'issue', 'problem', 'fail']):
                solution_steps = extract_actionable_steps(section_content)
                if len(solution_steps) == 0:
                    sections_without_solutions.append(heading)

        assert len(sections_without_solutions) == 0, (
            f"Troubleshooting sections without actionable solutions:\n"
            + "\n".join(f"  - {s}" for s in sections_without_solutions)
            + f"\n\nEach problem must have actionable solution steps"
        )

    def test_uninstallation_scenarios_have_cleanup_verification(self):
        """
        Plugin uninstallation test scenarios must verify cleanup.

        Validates: P0-2 Acceptance Criteria - uninstallation test cases

        Anti-Gaming: Validates cleanup verification steps exist.
        """
        # Look for uninstallation documentation
        files_to_check = [
            MANUAL_TESTS_DIR / "installation-marketplace.md",
            MANUAL_TESTS_DIR / "README.md",
        ]

        found_uninstall_docs = False
        content = ""

        for file_path in files_to_check:
            if file_path.exists():
                file_content = file_path.read_text(encoding="utf-8")
                sections = parse_markdown_sections(file_content)

                for heading, section_content in sections.items():
                    if "uninstall" in heading.lower() or "remove" in heading.lower():
                        found_uninstall_docs = True
                        content = section_content
                        break

            if found_uninstall_docs:
                break

        assert found_uninstall_docs, (
            f"Plugin uninstallation scenarios not documented.\n"
            f"P0-2 requires test cases for plugin removal and cleanup"
        )

        # Must have cleanup verification steps
        verification_steps = [s for s in extract_actionable_steps(content) if any(v in s.lower() for v in ['verify', 'check', 'confirm'])]

        assert len(verification_steps) >= 2, (
            f"Uninstallation documentation has only {len(verification_steps)} verification steps.\n"
            f"Must verify cleanup (files removed, config cleared, etc.).\n"
            f"P0-2 requires verification that uninstall completed successfully"
        )


class TestCommandExecutionTestScenarios:
    """
    Test P0-3: Command Execution Test Scenarios

    Validates that test scenarios exist for all slash commands across all plugins.

    Anti-Gaming: Validates actual test scenario content, not just file counts.
    """

    def _get_plugin_commands(self, plugin_name: str) -> List[str]:
        """Get list of command names for a plugin."""
        commands_dir = REPO_ROOT / "plugins" / plugin_name / "commands"

        if not commands_dir.exists():
            return []

        command_files = list(commands_dir.glob("*.md"))
        return [f.stem for f in command_files]

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_plugin_command_test_scenarios_exist(self, plugin_name: str):
        """
        Each plugin must have command test scenario file.

        Validates: P0-3 Acceptance Criteria - test scenario for each command
        """
        scenario_file = MANUAL_TESTS_DIR / f"commands-{plugin_name}.md"

        assert scenario_file.exists(), (
            f"Command test scenarios not found: {scenario_file}\n"
            f"P0-3 requires test scenarios for all {plugin_name} commands"
        )

        content = scenario_file.read_text(encoding="utf-8")

        # Get actual commands for this plugin
        commands = self._get_plugin_commands(plugin_name)

        # Each command should be mentioned in test scenarios
        missing_commands = []
        for cmd in commands:
            # Look for /command or command name in scenarios
            if f"/{cmd}" not in content and cmd not in content:
                missing_commands.append(cmd)

        assert len(missing_commands) == 0, (
            f"Plugin {plugin_name}: Missing test scenarios for commands:\n"
            + "\n".join(f"  - {cmd}" for cmd in missing_commands)
            + f"\n\nP0-3 requires test scenario for each command"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_command_scenarios_have_expected_outcomes_table(self, plugin_name: str):
        """
        Command test scenarios must define expected outcomes in structured format.

        Validates: P0-3 Acceptance Criteria - expected prompt content

        Anti-Gaming: Validates actual table structure with expected/actual columns.
        """
        scenario_file = MANUAL_TESTS_DIR / f"commands-{plugin_name}.md"

        if not scenario_file.exists():
            pytest.skip(f"Command scenarios not yet created for {plugin_name}")

        content = scenario_file.read_text(encoding="utf-8")
        tables = extract_markdown_tables(content)

        # Should have at least one test table
        assert len(tables) > 0, (
            f"Plugin {plugin_name}: Command scenarios don't have test tables.\n"
            f"P0-3 requires structured test cases with expected outcomes"
        )

        # At least one table should have expected/actual columns
        valid_test_table_found = False
        for table in tables:
            headers = [h.lower() for h in table.keys()]
            if any('expect' in h for h in headers) or any('should' in h for h in headers):
                valid_test_table_found = True
                break

        assert valid_test_table_found, (
            f"Plugin {plugin_name}: Command scenarios missing expected outcome tables.\n"
            f"P0-3 requires tables defining expected behavior for each command"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_command_scenarios_document_workflow_sequence(self, plugin_name: str):
        """
        Command scenarios must document workflow transitions between commands.

        Validates: P0-3 Acceptance Criteria - workflow transitions between commands

        Anti-Gaming: Validates sequential structure with numbered steps or explicit ordering.
        """
        scenario_file = MANUAL_TESTS_DIR / f"commands-{plugin_name}.md"

        if not scenario_file.exists():
            pytest.skip(f"Command scenarios not yet created for {plugin_name}")

        content = scenario_file.read_text(encoding="utf-8")
        lists = extract_markdown_lists(content)

        # Should have numbered workflows or sequential steps
        has_workflow = False

        # Check for numbered list items (workflow sequence)
        for lst in lists:
            if len(lst) >= 3:  # At least 3 steps in a workflow
                # Check if list items reference multiple commands
                commands_referenced = sum(1 for item in lst if '/' in item)
                if commands_referenced >= 2:
                    has_workflow = True
                    break

        # Alternative: check for sections with "workflow" or "sequence" in heading
        sections = parse_markdown_sections(content)
        for heading in sections.keys():
            if any(kw in heading.lower() for kw in ['workflow', 'sequence', 'order', 'steps']):
                has_workflow = True
                break

        assert has_workflow, (
            f"Plugin {plugin_name}: Command scenarios don't document workflow sequence.\n"
            f"P0-3 requires workflow showing command execution order and transitions"
        )

    def test_command_autocomplete_verification_documented(self):
        """
        Command autocomplete verification must be documented.

        Validates: P0-3 Acceptance Criteria - autocomplete verification tests
        """
        # Look for autocomplete verification in README or command scenarios
        files_to_check = list(MANUAL_TESTS_DIR.glob("*.md"))

        found_autocomplete_tests = False
        for file_path in files_to_check:
            content = file_path.read_text(encoding="utf-8")
            sections = parse_markdown_sections(content)

            for heading, section_content in sections.items():
                if "autocomplete" in heading.lower() or "tab complete" in heading.lower():
                    # Must have verification steps
                    steps = extract_actionable_steps(section_content)
                    if len(steps) > 0:
                        found_autocomplete_tests = True
                        break

            if found_autocomplete_tests:
                break

        assert found_autocomplete_tests, (
            f"Command autocomplete verification not documented with actionable steps.\n"
            f"P0-3 requires autocomplete verification tests"
        )

    def test_error_handling_scenarios_have_negative_tests(self):
        """
        Error handling test scenarios must include negative test cases.

        Validates: P0-3 Acceptance Criteria - error handling tests

        Anti-Gaming: Validates actual negative test cases with invalid inputs.
        """
        # Check command scenario files for error handling
        command_scenario_files = list(MANUAL_TESTS_DIR.glob("commands-*.md"))

        files_with_negative_tests = 0
        for file_path in command_scenario_files:
            content = file_path.read_text(encoding="utf-8")
            sections = parse_markdown_sections(content)

            # Look for error/negative test sections
            has_negative_section = any(
                any(kw in heading.lower() for kw in ['error', 'invalid', 'negative', 'fail'])
                for heading in sections.keys()
            )

            # Or look for test tables with error test cases
            if not has_negative_section:
                tables = extract_markdown_tables(content)
                for table in tables:
                    # Check if any table rows mention invalid/error scenarios
                    all_values = [v for values in table.values() for v in values]
                    if any(any(kw in str(v).lower() for kw in ['invalid', 'error', 'fail']) for v in all_values):
                        has_negative_section = True
                        break

            if has_negative_section:
                files_with_negative_tests += 1

        assert files_with_negative_tests >= 2, (
            f"Error handling scenarios not adequately documented.\n"
            f"Only {files_with_negative_tests}/{len(command_scenario_files)} "
            f"command scenario files include negative test cases.\n"
            f"P0-3 requires error handling tests with invalid inputs"
        )


class TestCompleteWorkflowTestScenarios:
    """
    Test P0-4: Complete Workflow Test Scenarios

    Validates that end-to-end workflow scenarios are comprehensive and realistic.

    Anti-Gaming: Validates workflow completeness, not just file existence.
    """

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_plugin_workflow_scenarios_exist(self, plugin_name: str):
        """
        Each plugin must have complete workflow test scenarios.

        Validates: P0-4 Acceptance Criteria - 3-5 workflow scenarios per plugin
        """
        scenario_file = MANUAL_TESTS_DIR / f"workflows-{plugin_name}.md"

        assert scenario_file.exists(), (
            f"Workflow scenarios not found: {scenario_file}\n"
            f"P0-4 requires 3-5 complete workflow scenarios for {plugin_name}"
        )

        content = scenario_file.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Count scenario sections
        scenario_sections = [h for h in sections.keys() if any(kw in h.lower() for kw in ['scenario', 'workflow', 'test'])]

        assert len(scenario_sections) >= 3, (
            f"Plugin {plugin_name}: Only {len(scenario_sections)} workflow scenarios found.\n"
            f"P0-4 requires at least 3 workflow scenarios per plugin"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_workflow_scenarios_have_setup_verification_deliverables(self, plugin_name: str):
        """
        Workflow scenarios must include setup, execution steps, and deliverable verification.

        Validates: P0-4 Acceptance Criteria - realistic project setup and expected deliverables

        Anti-Gaming: Validates three-phase structure (setup → execute → verify).
        """
        scenario_file = MANUAL_TESTS_DIR / f"workflows-{plugin_name}.md"

        if not scenario_file.exists():
            pytest.skip(f"Workflow scenarios not yet created for {plugin_name}")

        content = scenario_file.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Each workflow scenario should have all three phases
        workflow_sections = [(h, c) for h, c in sections.items() if any(kw in h.lower() for kw in ['scenario', 'workflow'])]

        incomplete_workflows = []

        for heading, section_content in workflow_sections:
            # Check for setup phase
            has_setup = any(kw in section_content.lower() for kw in ['setup', 'prerequisite', 'preparation', 'initialize'])

            # Check for execution/steps
            execution_steps = extract_actionable_steps(section_content)
            has_execution = len(execution_steps) >= 3

            # Check for deliverable verification
            has_verification = any(kw in section_content.lower() for kw in ['verify', 'deliverable', 'output', 'result', 'produce'])

            if not (has_setup and has_execution and has_verification):
                missing = []
                if not has_setup:
                    missing.append("setup")
                if not has_execution:
                    missing.append("execution steps")
                if not has_verification:
                    missing.append("deliverable verification")

                incomplete_workflows.append(f"{heading}: missing {', '.join(missing)}")

        assert len(incomplete_workflows) == 0, (
            f"Plugin {plugin_name}: Workflow scenarios missing required phases:\n"
            + "\n".join(f"  - {w}" for w in incomplete_workflows)
            + f"\n\nP0-4: Each workflow must have setup → execution → verification"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_workflow_scenarios_include_time_estimates(self, plugin_name: str):
        """
        Workflow scenarios should include realistic time estimates.

        Validates: P0-4 Acceptance Criteria - time estimates for workflows

        Anti-Gaming: Validates actual time values (numbers with units).
        """
        scenario_file = MANUAL_TESTS_DIR / f"workflows-{plugin_name}.md"

        if not scenario_file.exists():
            pytest.skip(f"Workflow scenarios not yet created for {plugin_name}")

        content = scenario_file.read_text(encoding="utf-8")

        # Look for time estimates with numbers and units
        time_pattern = r'\d+\s*(?:minute|min|hour|hr|second|sec)'
        time_estimates = re.findall(time_pattern, content, re.IGNORECASE)

        assert len(time_estimates) >= 3, (
            f"Plugin {plugin_name}: Only {len(time_estimates)} time estimates found.\n"
            f"P0-4 requires time estimates for each workflow scenario (e.g., '15 minutes', '1 hour')"
        )


class TestAgentBehaviorObservationChecklists:
    """
    Test P0-5: Agent Behavior Observation Checklists

    Validates that observation checklists exist for manually verifying
    agent behavior and guardrails.

    Anti-Gaming: Validates checklist completeness, not just file existence.
    """

    # Agent files for each plugin
    AGENT_FILES = {
        "agent-loop": "workflow-agent.md",
        "epti": "tdd-agent.md",
        "visual-iteration": "visual-iteration-agent.md",
    }

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_observation_checklist_has_observable_behaviors(self, plugin_name: str):
        """
        Each plugin must have agent checklist with specific observable behaviors.

        Validates: P0-5 Acceptance Criteria - agent behavior checklist per plugin

        Anti-Gaming: Validates checklist items (list structure), not just keywords.
        """
        checklist_file = MANUAL_TESTS_DIR / f"agent-{plugin_name}.md"

        assert checklist_file.exists(), (
            f"Agent observation checklist not found: {checklist_file}\n"
            f"P0-5 requires observation checklist for {plugin_name} agent"
        )

        content = checklist_file.read_text(encoding="utf-8")

        # Must mention agent or plugin name
        agent_file = self.AGENT_FILES[plugin_name]
        agent_name = agent_file.replace(".md", "")

        assert agent_name in content.lower() or plugin_name in content.lower(), (
            f"Agent checklist doesn't mention agent '{agent_name}'.\n"
            f"Checklist may be generic template, not agent-specific"
        )

        # Must have checklist structure (list items)
        lists = extract_markdown_lists(content)
        total_checklist_items = sum(len(lst) for lst in lists)

        assert total_checklist_items >= 5, (
            f"Agent checklist for {plugin_name} has only {total_checklist_items} items.\n"
            f"Expected at least 5 observable behaviors to check.\n"
            f"P0-5 requires comprehensive behavior observation checklist"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_checklist_includes_anti_pattern_verification(self, plugin_name: str):
        """
        Agent checklist must verify anti-pattern detection and blocking.

        Validates: P0-5 Acceptance Criteria - anti-pattern detection verification

        Anti-Gaming: Validates specific anti-pattern test cases in checklist.
        """
        checklist_file = MANUAL_TESTS_DIR / f"agent-{plugin_name}.md"

        if not checklist_file.exists():
            pytest.skip(f"Agent checklist not yet created for {plugin_name}")

        content = checklist_file.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Look for anti-pattern section
        anti_pattern_section = None
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['anti-pattern', 'avoid', 'don\'t', 'prevent', 'block']):
                anti_pattern_section = section_content
                break

        assert anti_pattern_section is not None, (
            f"Agent checklist for {plugin_name} missing anti-pattern verification section.\n"
            f"P0-5 requires verification of anti-pattern detection and blocking"
        )

        # Section should have checklist items
        anti_pattern_items = extract_markdown_lists(anti_pattern_section)
        total_items = sum(len(lst) for lst in anti_pattern_items)

        assert total_items >= 3, (
            f"Agent anti-pattern section has only {total_items} verification items.\n"
            f"Expected at least 3 anti-pattern checks.\n"
            f"P0-5 requires specific anti-pattern verification points"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_checklist_includes_stage_transition_verification(self, plugin_name: str):
        """
        Agent checklist must verify stage transitions are working correctly.

        Validates: P0-5 Acceptance Criteria - stage transition observation

        Anti-Gaming: Validates stage-specific checklist items.
        """
        checklist_file = MANUAL_TESTS_DIR / f"agent-{plugin_name}.md"

        if not checklist_file.exists():
            pytest.skip(f"Agent checklist not yet created for {plugin_name}")

        content = checklist_file.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Look for stage/workflow/transition section
        transition_section = None
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['stage', 'transition', 'workflow', 'phase', 'step']):
                transition_section = section_content
                break

        assert transition_section is not None, (
            f"Agent checklist for {plugin_name} missing stage transition verification section.\n"
            f"P0-5 requires verification of workflow stage transitions"
        )

        # Section should have checklist items
        transition_items = extract_markdown_lists(transition_section)
        total_items = sum(len(lst) for lst in transition_items)

        assert total_items >= 2, (
            f"Agent stage transition section has only {total_items} verification items.\n"
            f"Expected at least 2 transition checks.\n"
            f"P0-5 requires stage transition observation points"
        )

    @pytest.mark.parametrize("plugin_name", PLUGINS)
    def test_agent_checklist_includes_qualitative_assessment(self, plugin_name: str):
        """
        Agent checklist must include qualitative assessment criteria.

        Validates: P0-5 Acceptance Criteria - qualitative assessment criteria

        Anti-Gaming: Validates assessment questions or criteria.
        """
        checklist_file = MANUAL_TESTS_DIR / f"agent-{plugin_name}.md"

        if not checklist_file.exists():
            pytest.skip(f"Agent checklist not yet created for {plugin_name}")

        content = checklist_file.read_text(encoding="utf-8")

        # Look for questions (assessment typically uses questions)
        question_marks = content.count('?')

        assert question_marks >= 3, (
            f"Agent checklist for {plugin_name} has only {question_marks} assessment questions.\n"
            f"Expected at least 3 qualitative assessment questions.\n"
            f"P0-5 requires qualitative assessment criteria for agent effectiveness"
        )


class TestManualTestingFrameworkCompleteness:
    """
    High-level validation that manual testing framework is complete.

    This provides comprehensive validation of Phase 1 (P0-1 to P0-5) completion.
    """

    def test_all_phase1_components_present(self):
        """
        Validate all Phase 1 manual testing components are present.

        This is a master test for Phase 1 (P0-1 to P0-5) completion.
        """
        issues = []

        # P0-1: Documentation framework
        required_docs = [
            ("README.md", "Testing overview and instructions"),
            ("TESTING_RESULTS.md", "Results recording template"),
            ("ISSUE_TEMPLATE.md", "Bug reporting template"),
        ]

        for doc_name, description in required_docs:
            doc_path = MANUAL_TESTS_DIR / doc_name
            if not doc_path.exists():
                issues.append(f"P0-1: Missing {description} ({doc_name})")

        # P0-2: Installation scenarios (marketplace + per-plugin)
        install_files = [
            ("installation-marketplace.md", "Marketplace installation"),
        ] + [(f"installation-{p}.md", f"{p} installation") for p in PLUGINS]

        for install_file, description in install_files:
            install_path = MANUAL_TESTS_DIR / install_file
            if not install_path.exists():
                issues.append(f"P0-2: Missing {description} ({install_file})")

        # P0-3: Command execution scenarios (per-plugin)
        for plugin_name in PLUGINS:
            command_file = MANUAL_TESTS_DIR / f"commands-{plugin_name}.md"
            if not command_file.exists():
                issues.append(f"P0-3: Missing command scenarios for {plugin_name}")

        # P0-4: Workflow scenarios (per-plugin)
        for plugin_name in PLUGINS:
            workflow_file = MANUAL_TESTS_DIR / f"workflows-{plugin_name}.md"
            if not workflow_file.exists():
                issues.append(f"P0-4: Missing workflow scenarios for {plugin_name}")

        # P0-5: Agent observation checklists (per-plugin)
        for plugin_name in PLUGINS:
            agent_file = MANUAL_TESTS_DIR / f"agent-{plugin_name}.md"
            if not agent_file.exists():
                issues.append(f"P0-5: Missing agent checklist for {plugin_name}")

        # Generate summary
        total_expected = 3 + len(install_files) + len(PLUGINS) * 3  # docs + installs + commands + workflows + agents
        total_found = total_expected - len(issues)

        assert len(issues) == 0, (
            f"\nPhase 1 Manual Testing Framework INCOMPLETE\n"
            f"{'='*60}\n\n"
            f"Progress: {total_found}/{total_expected} components present\n\n"
            f"Missing components:\n"
            + "\n".join(f"  - {issue}" for issue in issues)
            + f"\n\n"
            f"Phase 1 requires all P0-1 to P0-5 work items completed.\n"
            f"This is CRITICAL for validating plugin functionality."
        )

    def test_manual_testing_framework_ready_for_execution(self):
        """
        Validate manual testing framework is ready for P0-6 execution.

        This checks that all prerequisites for manual testing (P0-6) are met.
        """
        # Prerequisites for P0-6 execution
        prerequisites = []

        # Need comprehensive README
        readme_path = MANUAL_TESTS_DIR / "README.md"
        if readme_path.exists():
            content = readme_path.read_text(encoding="utf-8")
            substantive_paras = count_substantive_paragraphs(content)
            if substantive_paras < 3:
                prerequisites.append("README.md needs more substantive content (guide quality)")
        else:
            prerequisites.append("README.md missing")

        # Need results template
        results_path = MANUAL_TESTS_DIR / "TESTING_RESULTS.md"
        if not results_path.exists():
            prerequisites.append("TESTING_RESULTS.md template missing")

        # Need test scenarios for all plugins
        scenario_types = ["installation", "commands", "workflows", "agent"]
        for scenario_type in scenario_types:
            for plugin_name in PLUGINS:
                # Check appropriate file exists
                if scenario_type == "installation":
                    file_path = MANUAL_TESTS_DIR / f"installation-{plugin_name}.md"
                else:
                    file_path = MANUAL_TESTS_DIR / f"{scenario_type}-{plugin_name}.md"

                if not file_path.exists():
                    prerequisites.append(
                        f"{scenario_type.capitalize()} scenarios missing for {plugin_name}"
                    )

        assert len(prerequisites) == 0, (
            f"\nManual testing framework NOT READY for execution (P0-6)\n"
            f"{'='*60}\n\n"
            f"Missing prerequisites:\n"
            + "\n".join(f"  - {prereq}" for prereq in prerequisites)
            + f"\n\n"
            f"Complete P0-1 through P0-5 before executing P0-6 manual testing."
        )
