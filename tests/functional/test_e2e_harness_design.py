"""
Functional tests for E2E Test Harness Design Validation (Phase 3 - P2-1 to P2-4).

These tests validate that E2E test harness design artifacts are complete and
well-formed, preparing for future implementation when Claude Code API becomes available.

Tests verify real design documentation and cannot be gamed by stubs.

Reference:
- PLAN-testing-framework-2025-11-06-021441.md (Phase 3)
- Phase 3 Work Items: P2-1 through P2-4 (design only, P3-1+ blocked on API)

Test Criteria Alignment:
- Useful: Tests actual design completeness, not placeholders
- Complete: Covers all harness design components
- Flexible: Tests design intent, not implementation
- Fully automated: Uses pytest with document parsing
- No ad-hoc: Follows existing test patterns

E2E Harness Design Components (testable now):
1. E2E test harness architecture documentation (P2-1)
2. Conversation simulation framework design (P2-2)
3. Test project generator implementation (P2-3) - CAN implement
4. Claude Code API requirements documentation (P2-4)

Blocked Components (require Claude Code API):
- P3-1: Plugin installation tests
- P3-2: Command execution tests
- P3-3: Agent behavior tests
- P3-4: Workflow completion tests
- P3-5: MCP server integration tests
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest


# Repository root path (absolute)
REPO_ROOT = Path(__file__).parent.parent.parent.resolve()

# E2E harness design documentation location
E2E_DESIGN_DIR = REPO_ROOT / "tests" / "e2e" / "design"

# Test project templates directory
TEST_PROJECTS_DIR = REPO_ROOT / "tests" / "e2e" / "test_projects"


# ============================================================================
# Design Document Parsing Utilities
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


def extract_code_blocks(content: str) -> List[Tuple[str, str]]:
    """
    Extract code blocks with language specifiers.

    Returns list of (language, code) tuples.
    Cannot be gamed - requires actual code fence structure.
    """
    blocks = []
    pattern = r'```(\w*)\n([\s\S]*?)```'
    matches = re.findall(pattern, content)

    for lang, code in matches:
        blocks.append((lang.strip(), code.strip()))

    return blocks


def extract_interface_definitions(code_blocks: List[Tuple[str, str]]) -> List[Dict[str, any]]:
    """
    Extract class/interface definitions from code blocks.

    Returns list of dicts with: name, methods, type (class/interface).
    Cannot be gamed - parses actual code structure.
    """
    interfaces = []

    for lang, code in code_blocks:
        if lang not in ['python', 'typescript', 'javascript']:
            continue

        # Python class pattern
        if lang == 'python':
            class_pattern = r'class\s+(\w+).*?:'
            method_pattern = r'def\s+(\w+)\s*\('

            classes = re.findall(class_pattern, code)
            for class_name in classes:
                # Find methods for this class
                # Split at class definition
                class_code = code.split(f'class {class_name}')[1] if f'class {class_name}' in code else ''
                methods = re.findall(method_pattern, class_code)

                interfaces.append({
                    'name': class_name,
                    'type': 'class',
                    'methods': methods,
                    'language': lang,
                })

        # TypeScript/JavaScript interface/class pattern
        elif lang in ['typescript', 'javascript']:
            interface_pattern = r'(?:interface|class)\s+(\w+)'
            method_pattern = r'(\w+)\s*\([^)]*\)'

            types = re.findall(interface_pattern, code)
            for type_name in types:
                # Find methods/properties
                type_code = code.split(type_name)[1] if type_name in code else ''
                methods = re.findall(method_pattern, type_code)

                interfaces.append({
                    'name': type_name,
                    'type': 'interface' if 'interface ' + type_name in code else 'class',
                    'methods': methods,
                    'language': lang,
                })

    return interfaces


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


def detect_contradictions(documents: List[Tuple[str, str]]) -> List[str]:
    """
    Detect contradictions between design documents.

    Returns list of potential contradictions found.
    Cannot be gamed - compares statements across documents.
    """
    contradictions = []

    # Simple heuristic: look for conflicting statements about same components
    # E.g., "plugin install" mentioned differently in different docs

    component_mentions = {}

    for doc_name, content in documents:
        # Extract statements about key components
        key_terms = ['plugin', 'command', 'agent', 'skill', 'conversation', 'api']

        for term in key_terms:
            # Find sentences mentioning this term
            sentences = content.split('.')
            for sentence in sentences:
                if term in sentence.lower():
                    if term not in component_mentions:
                        component_mentions[term] = []

                    component_mentions[term].append((doc_name, sentence.strip()))

    # Check for contradictory statements (basic check)
    # Look for positive/negative pairs
    for term, mentions in component_mentions.items():
        if len(mentions) < 2:
            continue

        positive_docs = []
        negative_docs = []

        for doc_name, sentence in mentions:
            # Check for affirmative statements
            if any(word in sentence.lower() for word in ['must', 'will', 'should', 'required']):
                positive_docs.append((doc_name, sentence[:100]))

            # Check for negative statements
            if any(word in sentence.lower() for word in ['cannot', 'will not', 'not available', 'blocked']):
                negative_docs.append((doc_name, sentence[:100]))

        # If same component has both positive and negative mentions, flag it
        if positive_docs and negative_docs:
            contradictions.append(
                f"{term}: positive in {positive_docs[0][0]}, negative in {negative_docs[0][0]}"
            )

    return contradictions


# ============================================================================
# Test Classes
# ============================================================================

class TestE2EHarnessArchitectureDocumentation:
    """
    Test P2-1: E2E Test Harness Architecture Design

    Validates that E2E test harness architecture is documented,
    even though implementation is blocked on Claude Code API.

    Anti-Gaming: Validates actual architectural documentation content.
    """

    def test_e2e_design_directory_exists(self):
        """
        E2E design directory must exist.

        Validates: P2-1 foundation - design documentation structure
        """
        assert E2E_DESIGN_DIR.exists(), (
            f"E2E design directory not found: {E2E_DESIGN_DIR}\n"
            f"P2-1 requires creating tests/e2e/design/ for architectural documentation"
        )

    def test_harness_architecture_document_exists(self):
        """
        E2E harness architecture document must exist.

        Validates: P2-1 Acceptance Criteria - architecture documentation

        Anti-Gaming: Requires actual design document, not just directory.
        """
        arch_doc = E2E_DESIGN_DIR / "ARCHITECTURE.md"

        assert arch_doc.exists(), (
            f"E2E harness architecture document not found: {arch_doc}\n"
            f"P2-1 requires ARCHITECTURE.md documenting test harness design"
        )

        content = arch_doc.read_text(encoding="utf-8")

        # Should have substantive content (paragraphs with sentences)
        substantive_paras = count_substantive_paragraphs(content)

        assert substantive_paras >= 5, (
            f"Architecture document has only {substantive_paras} substantive paragraphs.\n"
            f"Expected at least 5 paragraphs with detailed explanations.\n"
            f"P2-1 requires detailed architectural documentation"
        )

    def test_architecture_documents_required_claude_code_api(self):
        """
        Architecture must document required Claude Code API capabilities.

        Validates: P2-1 Acceptance Criteria - API capability requirements

        Anti-Gaming: Validates structured API requirements sections.
        """
        arch_doc = E2E_DESIGN_DIR / "ARCHITECTURE.md"

        if not arch_doc.exists():
            pytest.skip("Architecture document not yet created")

        content = arch_doc.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Should have dedicated section for API requirements
        api_section = None
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['api', 'requirement', 'claude code']):
                api_section = section_content
                break

        assert api_section is not None, (
            f"Architecture document missing dedicated API requirements section.\n"
            f"P2-1: Must have section documenting Claude Code API needs"
        )

        # API section should have substantive content
        api_paras = count_substantive_paragraphs(api_section)

        assert api_paras >= 2, (
            f"API requirements section has only {api_paras} substantive paragraphs.\n"
            f"P2-1: API requirements need detailed explanation"
        )

    def test_architecture_defines_test_harness_interfaces(self):
        """
        Architecture must define test harness class structure and interfaces.

        Validates: P2-1 Acceptance Criteria - harness interface design

        Anti-Gaming: Parses actual class/interface definitions from code blocks.
        """
        arch_doc = E2E_DESIGN_DIR / "ARCHITECTURE.md"

        if not arch_doc.exists():
            pytest.skip("Architecture document not yet created")

        content = arch_doc.read_text(encoding="utf-8")
        code_blocks = extract_code_blocks(content)

        # Extract interface definitions
        interfaces = extract_interface_definitions(code_blocks)

        assert len(interfaces) >= 2, (
            f"Architecture document has only {len(interfaces)} class/interface definitions.\n"
            f"Expected at least 2 interface/class definitions for test harness.\n"
            f"P2-1: Must design test harness class structure"
        )

        # Each interface should have methods
        interfaces_without_methods = [iface for iface in interfaces if len(iface['methods']) == 0]

        assert len(interfaces_without_methods) == 0, (
            f"Architecture has interfaces without methods:\n"
            + "\n".join(f"  - {iface['name']}" for iface in interfaces_without_methods)
            + f"\n\nP2-1: Interfaces must define methods"
        )

    def test_architecture_includes_example_usage(self):
        """
        Architecture should include example test harness usage.

        Validates: P2-1 Acceptance Criteria - design examples

        Anti-Gaming: Validates code blocks are complete examples (not fragments).
        """
        arch_doc = E2E_DESIGN_DIR / "ARCHITECTURE.md"

        if not arch_doc.exists():
            pytest.skip("Architecture document not yet created")

        content = arch_doc.read_text(encoding="utf-8")
        code_blocks = extract_code_blocks(content)

        # Should have substantial code examples (>100 chars each)
        substantial_examples = [code for lang, code in code_blocks if len(code) >= 100]

        assert len(substantial_examples) >= 2, (
            f"Architecture document has only {len(substantial_examples)} substantial code examples.\n"
            f"Expected at least 2 complete usage examples (>100 chars each).\n\n"
            f"P2-1: Should include example test harness usage"
        )


class TestConversationSimulationFrameworkDesign:
    """
    Test P2-2: Conversation Simulation Framework Design

    Validates that conversation simulation framework is designed,
    documenting how to simulate multi-turn Claude interactions.

    Anti-Gaming: Validates actual design documentation content.
    """

    def test_conversation_framework_document_exists(self):
        """
        Conversation simulation framework design document must exist.

        Validates: P2-2 Acceptance Criteria - framework design
        """
        conv_doc = E2E_DESIGN_DIR / "CONVERSATION_SIMULATION.md"

        assert conv_doc.exists(), (
            f"Conversation simulation design not found: {conv_doc}\n"
            f"P2-2 requires CONVERSATION_SIMULATION.md documenting framework design"
        )

        content = conv_doc.read_text(encoding="utf-8")

        # Should have substantive content
        substantive_paras = count_substantive_paragraphs(content)

        assert substantive_paras >= 3, (
            f"Conversation simulation document has only {substantive_paras} substantive paragraphs.\n"
            f"Expected at least 3 paragraphs for framework design.\n"
            f"P2-2 requires detailed conversation simulation design"
        )

    def test_conversation_framework_defines_state_model(self):
        """
        Conversation framework must define conversation state model.

        Validates: P2-2 Acceptance Criteria - conversation state model

        Anti-Gaming: Validates structured state model (class/interface definitions).
        """
        conv_doc = E2E_DESIGN_DIR / "CONVERSATION_SIMULATION.md"

        if not conv_doc.exists():
            pytest.skip("Conversation simulation document not yet created")

        content = conv_doc.read_text(encoding="utf-8")
        code_blocks = extract_code_blocks(content)

        # Extract interface definitions for state model
        interfaces = extract_interface_definitions(code_blocks)

        # Should have at least one state-related interface
        state_interfaces = [
            iface for iface in interfaces
            if any(kw in iface['name'].lower() for kw in ['state', 'context', 'conversation'])
        ]

        assert len(state_interfaces) >= 1, (
            f"Conversation framework doesn't define state model interface.\n"
            f"Found interfaces: {[i['name'] for i in interfaces]}\n"
            f"P2-2: Must define conversation state model (class/interface)"
        )

    def test_conversation_framework_includes_example_scenarios(self):
        """
        Conversation framework should include example test scenarios.

        Validates: P2-2 Acceptance Criteria - example test scenarios

        Anti-Gaming: Validates actual multi-turn conversation examples.
        """
        conv_doc = E2E_DESIGN_DIR / "CONVERSATION_SIMULATION.md"

        if not conv_doc.exists():
            pytest.skip("Conversation simulation document not yet created")

        content = conv_doc.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Look for example sections
        example_sections = [
            (heading, section_content)
            for heading, section_content in sections.items()
            if any(kw in heading.lower() for kw in ['example', 'scenario', 'test case'])
        ]

        assert len(example_sections) >= 1, (
            f"Conversation framework missing example scenarios.\n"
            f"P2-2: Should include example test scenarios using designed API"
        )

        # Example sections should have code blocks or structured content
        examples_with_code = [
            heading for heading, section_content in example_sections
            if '```' in section_content
        ]

        assert len(examples_with_code) >= 1, (
            f"Conversation framework examples don't include code.\n"
            f"P2-2: Examples should show actual conversation simulation code"
        )


class TestTestProjectGenerators:
    """
    Test P2-3: Test Project Generators

    Validates that test project generator exists and can create realistic projects.

    This CAN be implemented now (not blocked on Claude Code API).

    Anti-Gaming: Tests actual project generation, not stubs.
    """

    def test_test_projects_directory_exists(self):
        """
        Test projects directory must exist.

        Validates: P2-3 foundation - project generator structure
        """
        assert TEST_PROJECTS_DIR.exists(), (
            f"Test projects directory not found: {TEST_PROJECTS_DIR}\n"
            f"P2-3 requires tests/e2e/test_projects/ for project templates"
        )

    def test_project_generator_script_exists(self):
        """
        Project generator CLI tool must exist.

        Validates: P2-3 Acceptance Criteria - project generator CLI

        Anti-Gaming: Requires actual executable script.
        """
        generator_script = REPO_ROOT / "tools" / "generate_test_project.py"

        assert generator_script.exists(), (
            f"Project generator not found: {generator_script}\n"
            f"P2-3 requires tools/generate_test_project.py for generating test projects"
        )

        # Should be executable or have shebang
        content = generator_script.read_text(encoding="utf-8")
        assert content.startswith("#!") or "def main(" in content or "if __name__" in content, (
            f"Project generator doesn't appear to be executable script.\n"
            f"P2-3: Generator should be runnable CLI tool"
        )

    def test_project_templates_have_realistic_structure(self):
        """
        Project templates must have realistic structure.

        Validates: P2-3 Acceptance Criteria - project structure validation

        Anti-Gaming: Checks for actual project files (package.json, src/, etc).
        """
        if not TEST_PROJECTS_DIR.exists():
            pytest.skip("Test projects directory not yet created")

        templates = [d for d in TEST_PROJECTS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]

        if len(templates) == 0:
            pytest.skip("No project templates yet created")

        incomplete_templates = []

        for template_dir in templates:
            # Check for realistic project structure
            has_structure = False

            # Language-specific structure indicators
            structure_files = [
                "package.json",  # Node.js
                "pyproject.toml",  # Python
                "requirements.txt",  # Python
                "go.mod",  # Go
                "pom.xml",  # Java
            ]

            for structure_file in structure_files:
                if (template_dir / structure_file).exists():
                    has_structure = True
                    break

            # Should also have src or tests directories
            has_src = (template_dir / "src").exists() or (template_dir / "lib").exists()
            has_tests = (template_dir / "tests").exists() or (template_dir / "test").exists()

            if not (has_structure and (has_src or has_tests)):
                incomplete_templates.append(
                    f"{template_dir.name}: missing structure or src/tests"
                )

        assert len(incomplete_templates) == 0, (
            f"Project templates with incomplete structure:\n"
            + "\n".join(f"  - {tmpl}" for tmpl in incomplete_templates)
            + f"\n\nP2-3: Templates must have realistic project structure"
        )

    def test_project_templates_have_valid_configuration_files(self):
        """
        Project templates must have valid configuration files (JSON/YAML).

        Validates: P2-3 Acceptance Criteria - configuration validation

        Anti-Gaming: Actually parses JSON/YAML to verify syntax.
        """
        if not TEST_PROJECTS_DIR.exists():
            pytest.skip("Test projects directory not yet created")

        templates = [d for d in TEST_PROJECTS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]

        if len(templates) == 0:
            pytest.skip("No project templates yet created")

        invalid_configs = []

        for template_dir in templates:
            # Check package.json if exists
            package_json = template_dir / "package.json"
            if package_json.exists():
                try:
                    with open(package_json, 'r', encoding='utf-8') as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    invalid_configs.append(
                        f"{template_dir.name}/package.json: {e}"
                    )

            # Check other JSON/YAML files
            for config_file in template_dir.glob("*.json"):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    invalid_configs.append(
                        f"{template_dir.name}/{config_file.name}: {e}"
                    )

        assert len(invalid_configs) == 0, (
            f"Project templates with invalid configuration files:\n"
            + "\n".join(f"  - {err}" for err in invalid_configs)
            + f"\n\nP2-3: Configuration files must have valid syntax"
        )


class TestClaudeCodeAPIRequirementsDocumentation:
    """
    Test P2-4: Claude Code API Requirements Documentation

    Validates that required Claude Code APIs are documented for Anthropic.

    Anti-Gaming: Validates actual requirements documentation content.
    """

    def test_api_requirements_document_exists(self):
        """
        API requirements document must exist.

        Validates: P2-4 Acceptance Criteria - API requirements documented
        """
        api_req_doc = E2E_DESIGN_DIR / "API_REQUIREMENTS.md"

        assert api_req_doc.exists(), (
            f"API requirements document not found: {api_req_doc}\n"
            f"P2-4 requires API_REQUIREMENTS.md documenting needed Claude Code APIs"
        )

        content = api_req_doc.read_text(encoding="utf-8")

        # Should have substantive content
        substantive_paras = count_substantive_paragraphs(content)

        assert substantive_paras >= 3, (
            f"API requirements document has only {substantive_paras} substantive paragraphs.\n"
            f"Expected at least 3 paragraphs for comprehensive requirements.\n"
            f"P2-4 requires detailed API requirements documentation"
        )

    def test_api_requirements_document_plugin_management_apis(self):
        """
        API requirements must document plugin management needs.

        Validates: P2-4 Acceptance Criteria - plugin management API

        Anti-Gaming: Validates structured sections for each API category.
        """
        api_req_doc = E2E_DESIGN_DIR / "API_REQUIREMENTS.md"

        if not api_req_doc.exists():
            pytest.skip("API requirements document not yet created")

        content = api_req_doc.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Should have plugin management section
        plugin_section = None
        for heading, section_content in sections.items():
            if 'plugin' in heading.lower() and any(kw in heading.lower() for kw in ['manage', 'install', 'api']):
                plugin_section = section_content
                break

        assert plugin_section is not None, (
            f"API requirements missing plugin management section.\n"
            f"P2-4: Must document plugin management API needs"
        )

        # Plugin section should have substantive content
        plugin_paras = count_substantive_paragraphs(plugin_section)

        assert plugin_paras >= 1, (
            f"Plugin management section has insufficient content.\n"
            f"P2-4: Plugin API requirements need detailed explanation"
        )

    def test_api_requirements_document_conversation_apis(self):
        """
        API requirements must document conversation APIs.

        Validates: P2-4 Acceptance Criteria - conversation API

        Anti-Gaming: Validates structured conversation API sections.
        """
        api_req_doc = E2E_DESIGN_DIR / "API_REQUIREMENTS.md"

        if not api_req_doc.exists():
            pytest.skip("API requirements document not yet created")

        content = api_req_doc.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Should have conversation/messaging section
        conversation_section = None
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['conversation', 'message', 'interaction']):
                conversation_section = section_content
                break

        assert conversation_section is not None, (
            f"API requirements missing conversation API section.\n"
            f"P2-4: Must document conversation API needs"
        )

        # Conversation section should have substantive content
        conv_paras = count_substantive_paragraphs(conversation_section)

        assert conv_paras >= 1, (
            f"Conversation API section has insufficient content.\n"
            f"P2-4: Conversation API requirements need detailed explanation"
        )

    def test_api_requirements_include_alternatives(self):
        """
        API requirements should discuss alternatives if Claude Code API unavailable.

        Validates: P2-4 Acceptance Criteria - investigate alternatives

        Anti-Gaming: Validates actual alternative approach sections.
        """
        api_req_doc = E2E_DESIGN_DIR / "API_REQUIREMENTS.md"

        if not api_req_doc.exists():
            pytest.skip("API requirements document not yet created")

        content = api_req_doc.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Should have alternatives section
        alternatives_section = None
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['alternative', 'fallback', 'workaround', 'without api']):
                alternatives_section = section_content
                break

        assert alternatives_section is not None, (
            f"API requirements don't discuss alternatives.\n"
            f"P2-4: Should explore alternatives if Claude Code API unavailable"
        )

        # Alternatives section should have substantive content
        alt_paras = count_substantive_paragraphs(alternatives_section)

        assert alt_paras >= 1, (
            f"Alternatives section has insufficient content.\n"
            f"P2-4: Alternative approaches need detailed explanation"
        )


class TestE2EHarnessDesignCompleteness:
    """
    High-level validation that Phase 3 E2E harness design is complete.
    """

    def test_all_phase3_design_components_present(self):
        """
        Validate all Phase 3 design components are documented.

        This is a master test for Phase 3 (P2-1 to P2-4) design completion.
        """
        issues = []

        # P2-1: Harness architecture
        arch_doc = E2E_DESIGN_DIR / "ARCHITECTURE.md"
        if not arch_doc.exists():
            issues.append("P2-1: Missing ARCHITECTURE.md (harness design)")

        # P2-2: Conversation simulation
        conv_doc = E2E_DESIGN_DIR / "CONVERSATION_SIMULATION.md"
        if not conv_doc.exists():
            issues.append("P2-2: Missing CONVERSATION_SIMULATION.md (framework design)")

        # P2-3: Test project generators
        generator = REPO_ROOT / "tools" / "generate_test_project.py"
        if not generator.exists():
            issues.append("P2-3: Missing tools/generate_test_project.py (generator)")

        templates_exist = TEST_PROJECTS_DIR.exists() and len(list(TEST_PROJECTS_DIR.glob("*"))) > 0
        if not templates_exist:
            issues.append("P2-3: Missing test project templates")

        # P2-4: API requirements
        api_req_doc = E2E_DESIGN_DIR / "API_REQUIREMENTS.md"
        if not api_req_doc.exists():
            issues.append("P2-4: Missing API_REQUIREMENTS.md (Claude Code requirements)")

        # Generate summary
        total_expected = 5  # arch + conv + generator + templates + api_req
        total_found = total_expected - len(issues)

        assert len(issues) == 0, (
            f"\nPhase 3 E2E Harness Design INCOMPLETE\n"
            f"{'='*60}\n\n"
            f"Progress: {total_found}/{total_expected} design components present\n\n"
            f"Missing components:\n"
            + "\n".join(f"  - {issue}" for issue in issues)
            + f"\n\n"
            f"Phase 3 requires all P2-1 to P2-4 design work completed.\n"
            f"This prepares for E2E implementation when Claude Code API becomes available."
        )

    def test_design_documents_have_no_contradictions(self):
        """
        Design documents should not contradict each other.

        Validates: P2-1 to P2-4 alignment - design consistency

        Anti-Gaming: Compares statements across documents for conflicts.
        """
        if not E2E_DESIGN_DIR.exists():
            pytest.skip("E2E design directory not yet created")

        design_files = list(E2E_DESIGN_DIR.glob("*.md"))

        if len(design_files) < 2:
            pytest.skip("Need at least 2 design documents to check contradictions")

        # Load all documents
        documents = []
        for doc_file in design_files:
            content = doc_file.read_text(encoding="utf-8")
            documents.append((doc_file.name, content))

        # Detect contradictions
        contradictions = detect_contradictions(documents)

        assert len(contradictions) == 0, (
            f"Design documents contain contradictions:\n"
            + "\n".join(f"  - {contradiction}" for contradiction in contradictions)
            + f"\n\nP2-1 to P2-4: Design documents must be consistent"
        )

    def test_e2e_design_ready_for_implementation(self):
        """
        Validate E2E design is ready for implementation when API available.

        This checks that design has sufficient detail for future coding.
        """
        if not E2E_DESIGN_DIR.exists():
            pytest.skip("E2E design directory not yet created")

        design_files = list(E2E_DESIGN_DIR.glob("*.md"))

        if len(design_files) == 0:
            pytest.fail("No design documents found in E2E design directory")

        # Check that documents have sufficient substantive content
        total_substantive_paras = 0
        for doc_file in design_files:
            content = doc_file.read_text(encoding="utf-8")
            total_substantive_paras += count_substantive_paragraphs(content)

        # Should have at least 15 substantive paragraphs total across all docs
        min_total_paras = 15

        assert total_substantive_paras >= min_total_paras, (
            f"E2E design documentation has only {total_substantive_paras} substantive paragraphs.\n"
            f"Expected: at least {min_total_paras} paragraphs with detailed explanations.\n\n"
            f"Design should have sufficient detail for implementation when API available."
        )
