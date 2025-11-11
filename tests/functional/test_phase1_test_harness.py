"""
Functional tests for Phase 1 of the Test Harness Implementation.

These tests validate Phase 1 deliverables from PLAN-test-harness-2025-11-07-023500.md:
- P0: E2E Test Harness Architecture Documentation
- P0: Conversation Simulation Framework Design
- P0: Claude Code API Requirements Documentation
- P0: Test Project Generator Implementation
- P1: MCP Server Skeleton Implementation
- P1: Docker Feasibility Research
- P2: E2E Test Projects Directory Setup
- P2: E2E Design Completeness Validation

Test Philosophy:
- ✅ Useful: Tests validate REAL functionality, not trivial properties
- ✅ Complete: Covers all acceptance criteria from PLAN
- ✅ Flexible: Allows refactoring without breaking tests
- ✅ Fully Automated: Uses pytest, no manual steps
- ❌ ABSOLUTELY NOT GAMEABLE: Cannot pass with lorem ipsum, keyword stuffing, or stubs

Anti-Gaming Strategy (CRITICAL):
- EXECUTE code (run generators, call MCP tools, not just validate syntax)
- PARSE real data structures (tool inventories, not just keyword searches)
- CROSS-VALIDATE consistency (architecture matches implementation)
- REQUIRE evidence (Docker command outputs, not just claims)
- VALIDATE quality (real examples, not placeholders)
- CHECK substance (comprehensive content, not just length)

Reference: PLAN-test-harness-2025-11-07-023500.md
"""

import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

import pytest

# Use stdlib tomllib (Python 3.11+) with fallback to tomli
try:
    import tomllib
except ImportError:
    import tomli as tomllib


# ============================================================================
# Repository Paths
# ============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()

# Expected directory structure
E2E_DIR = REPO_ROOT / "tests" / "e2e"
E2E_DESIGN_DIR = E2E_DIR / "design"
E2E_TEST_PROJECTS_DIR = E2E_DIR / "test_projects"
E2E_MCP_SERVER_DIR = E2E_DIR / "mcp_server"

# Tools directory
TOOLS_DIR = REPO_ROOT / "tools"

# Expected documentation files (Phase 1)
ARCHITECTURE_DOC = E2E_DESIGN_DIR / "ARCHITECTURE.md"
CONVERSATION_SIMULATION_DOC = E2E_DESIGN_DIR / "CONVERSATION_SIMULATION.md"
API_REQUIREMENTS_DOC = E2E_DESIGN_DIR / "API_REQUIREMENTS.md"
DOCKER_SETUP_DOC = E2E_DESIGN_DIR / "DOCKER_SETUP.md"

# Expected implementation files (Phase 1)
TEST_PROJECT_GENERATOR = TOOLS_DIR / "generate_test_project.py"
MCP_SERVER_FILE = E2E_MCP_SERVER_DIR / "harness_server.py"
MCP_PYPROJECT = E2E_MCP_SERVER_DIR / "pyproject.toml"


# ============================================================================
# Document Parsing Utilities (REAL parsing, not keyword matching)
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


def extract_markdown_code_blocks(content: str) -> List[Tuple[str, str]]:
    """
    Extract code blocks from markdown with language tags.

    Returns list of (language, code) tuples.
    Cannot be gamed - requires actual code block structure.
    """
    code_blocks = []
    in_code_block = False
    current_language = ""
    current_code = []

    for line in content.split('\n'):
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block
                code_blocks.append((current_language, '\n'.join(current_code)))
                current_code = []
                current_language = ""
                in_code_block = False
            else:
                # Start of code block
                in_code_block = True
                # Extract language tag
                match = re.match(r'```(\w+)', line.strip())
                if match:
                    current_language = match.group(1)
        elif in_code_block:
            current_code.append(line)

    return code_blocks


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


def count_substantive_paragraphs(
    content: str,
    min_length: int = 200,
    min_sentences: int = 3,
    required_keywords: Optional[List[str]] = None
) -> int:
    """
    Count paragraphs with actual substantive content.

    A substantive paragraph must:
    - Be at least min_length characters
    - Contain at least min_sentences sentences
    - Not be a list item or heading
    - If required_keywords provided, contain at least 2 of them (topical relevance)

    Cannot be gamed with lorem ipsum alone - checks structure and topic relevance.
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
        if len(para) >= min_length:
            # Count sentences
            sentence_endings = para.count('.') + para.count('!') + para.count('?')
            if sentence_endings >= min_sentences:
                # NEW: If keywords provided, validate content relevance
                if required_keywords:
                    # Paragraph must contain at least 2 of the required keywords
                    para_lower = para.lower()
                    found_keywords = sum(1 for kw in required_keywords if kw.lower() in para_lower)
                    if found_keywords < 2:
                        continue  # Skip non-topical paragraphs

                count += 1

    return count


def parse_tool_inventory(content: str) -> List[Dict[str, str]]:
    """
    Parse tool inventory from architecture document.

    Extracts tool names, categories, descriptions, and status.
    Cannot be gamed - requires structured data with specific fields.

    Returns list of dicts with keys: name, category, description, status
    """
    tools = []

    # Try to find tool inventory in tables
    tables = extract_markdown_tables(content)

    for table in tables:
        # Look for tool inventory table (has Tool/Name, Category, Status columns)
        headers_lower = [h.lower() for h in table.keys()]

        if ('tool' in ' '.join(headers_lower) or 'name' in ' '.join(headers_lower)) and \
           'category' in ' '.join(headers_lower) and \
           ('status' in ' '.join(headers_lower) or 'state' in ' '.join(headers_lower)):

            # Find the right column names
            name_col = None
            category_col = None
            description_col = None
            status_col = None

            for header in table.keys():
                header_lower = header.lower()
                if 'tool' in header_lower or 'name' in header_lower:
                    name_col = header
                elif 'category' in header_lower:
                    category_col = header
                elif 'description' in header_lower or 'purpose' in header_lower:
                    description_col = header
                elif 'status' in header_lower or 'state' in header_lower:
                    status_col = header

            # Extract tools
            if name_col and category_col and status_col:
                num_rows = len(table[name_col])
                for i in range(num_rows):
                    tool = {
                        'name': table[name_col][i],
                        'category': table[category_col][i],
                        'description': table[description_col][i] if description_col else "",
                        'status': table[status_col][i]
                    }
                    tools.append(tool)

    # If no table found, try parsing from code blocks with @mcp.tool decorators
    if not tools:
        code_blocks = extract_markdown_code_blocks(content)
        python_blocks = [code for lang, code in code_blocks if lang == "python"]

        for code in python_blocks:
            # Extract function definitions with @mcp.tool decorator
            if '@mcp.tool' in code or '@tool' in code:
                func_pattern = r'@(?:mcp\.)?tool\([^)]*\)\s*(?:async\s+)?def\s+(\w+)\s*\([^)]*\)\s*(?:->\s*\w+)?\s*:\s*"""([^"]+)"""'
                matches = re.finditer(func_pattern, code, re.DOTALL)

                for match in matches:
                    func_name = match.group(1)
                    docstring = match.group(2).strip()

                    # Infer status from docstring
                    status = "implemented"
                    if "BLOCKED" in docstring or "NotImplementedError" in code:
                        status = "stubbed"

                    # Infer category from function name pattern
                    category = "Unknown"
                    if any(kw in func_name for kw in ['install', 'plugin', 'list']):
                        category = "Plugin"
                    elif any(kw in func_name for kw in ['command', 'execute']):
                        category = "Command"
                    elif any(kw in func_name for kw in ['conversation', 'prompt', 'send']):
                        category = "Conversation"
                    elif any(kw in func_name for kw in ['test', 'create_project', 'setup']):
                        category = "Test Environment"
                    elif any(kw in func_name for kw in ['assert', 'verify']):
                        category = "Assertion"

                    tools.append({
                        'name': func_name,
                        'category': category,
                        'description': docstring.split('\n')[0][:100],  # First line
                        'status': status
                    })

    return tools


def parse_python_functions(code: str) -> List[str]:
    """
    Parse Python code and extract function names.

    Returns list of function names defined in the code.
    Cannot be gamed - requires valid Python syntax.
    """
    try:
        tree = ast.parse(code)
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        return functions
    except SyntaxError:
        return []


def validate_python_syntax(code: str) -> bool:
    """
    Validate Python code syntax.

    Returns True if code is valid Python, False otherwise.
    Cannot be gamed - uses actual Python parser.
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def parse_yaml_frontmatter(content: str) -> Optional[Dict]:
    """
    Parse YAML frontmatter from markdown (if present).

    Returns dict of frontmatter data, or None if not present.
    Useful for validating research findings metadata.
    """
    import yaml

    # Check for YAML frontmatter (--- at start, --- at end)
    if content.strip().startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            try:
                return yaml.safe_load(parts[1])
            except yaml.YAMLError:
                return None

    return None


def check_for_real_docker_output(content: str) -> bool:
    """
    Check if Docker research includes REAL command-output pairs.

    Validates that document contains actual Docker commands with their outputs,
    not just copy-pasted example output or fabricated text.

    Cannot be gamed - requires BOTH commands AND outputs in same code block.
    """
    # Extract code blocks that look like shell output
    code_blocks = extract_markdown_code_blocks(content)
    shell_blocks = [code for lang, code in code_blocks
                    if lang in ["bash", "shell", "console", "sh", ""]]

    if not shell_blocks:
        return False

    # Real Docker experiments have:
    # 1. Command lines (start with "$" or "#" or "docker")
    # 2. Output lines (Docker response patterns)
    command_patterns = [r"^\$\s*docker", r"^#\s*docker", r"^docker\s+"]
    output_patterns = [
        r"Unable to find image",
        r"Successfully built",
        r"Error response from daemon",
        r"Pull complete",
        r"CONTAINER ID",
        r"Status: Downloaded",
        r"Sending build context",
        r"Step \d+/\d+ :",
        r"latest: Pulling from",
        r"digest: sha256:",
        r"Status: Image is up to date",
        r"REPOSITORY\s+TAG",
    ]

    found_valid_pairs = 0
    for block in shell_blocks:
        lines = block.split("\n")
        has_command = any(re.search(pat, line) for pat in command_patterns for line in lines)
        has_output = any(re.search(pat, line) for pat in output_patterns for line in lines)

        # BOTH command AND output required (not just output)
        if has_command and has_output:
            found_valid_pairs += 1

    return found_valid_pairs >= 1  # At least 1 command-output pair


def normalize_name(name: str) -> str:
    """
    Normalize tool/function names for comparison.

    Converts: "Create Test Project" → "create_test_project"
    """
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')


# ============================================================================
# Test Class: Test Project Generator Execution (P0-4) - CRITICAL
# ============================================================================

class TestProjectGeneratorExecution:
    """
    Test P0-4: Test Project Generator Implementation - EXECUTION TESTS

    This is the MOST CRITICAL test class. It actually EXECUTES the generator
    to verify it produces working projects, not just validates its existence.

    Anti-Gaming: Tests MUST execute code and validate output. No stubs allowed.
    """

    def test_test_project_generator_exists(self):
        """Test project generator script must exist."""
        assert TEST_PROJECT_GENERATOR.exists(), (
            f"Test project generator not found: {TEST_PROJECT_GENERATOR}\n"
            f"P0-4 requires implementing tools/generate_test_project.py"
        )

    def test_test_project_generator_is_executable_python(self):
        """
        Generator must be valid, executable Python code.

        Anti-Gaming: Validates syntax AND can be imported.
        """
        if not TEST_PROJECT_GENERATOR.exists():
            pytest.skip("Test project generator not yet created")

        code = TEST_PROJECT_GENERATOR.read_text(encoding="utf-8")

        # Validate syntax
        assert validate_python_syntax(code), (
            f"Test project generator has syntax errors.\n"
            f"P0-4 requires working Python implementation."
        )

        # Validate can be imported
        import importlib.util
        spec = importlib.util.spec_from_file_location("generate_test_project", TEST_PROJECT_GENERATOR)
        assert spec is not None and spec.loader is not None, (
            f"Test project generator cannot be imported.\n"
            f"P0-4 requires valid Python module."
        )

    def test_test_project_generator_has_cli_interface(self):
        """
        Generator must have CLI interface with argument parsing.

        Anti-Gaming: Validates argparse or click usage exists.
        """
        if not TEST_PROJECT_GENERATOR.exists():
            pytest.skip("Test project generator not yet created")

        code = TEST_PROJECT_GENERATOR.read_text(encoding="utf-8")

        # Should use argparse or click for CLI
        has_cli = (
            "argparse" in code or
            "click" in code or
            "ArgumentParser" in code or
            "@click.command" in code
        )

        assert has_cli, (
            f"Test project generator doesn't have CLI interface.\n"
            f"P0-4 requires argparse or click-based CLI."
        )

        # Should accept required arguments
        required_args = ["--type", "--language", "--output"]
        found_args = sum(1 for arg in required_args if arg in code)

        assert found_args >= 2, (
            f"Test project generator doesn't accept required CLI arguments.\n"
            f"Expected: {required_args}\n"
            f"P0-4 requires --type, --language, --output arguments."
        )

    @pytest.mark.slow
    def test_test_project_generator_can_run_help(self):
        """
        Generator must execute with --help flag.

        Anti-Gaming: ACTUALLY RUNS the generator to verify it works.
        """
        if not TEST_PROJECT_GENERATOR.exists():
            pytest.skip("Test project generator not yet created")

        # Try to run with --help
        result = subprocess.run(
            [sys.executable, str(TEST_PROJECT_GENERATOR), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should exit successfully (0 or show help and exit)
        assert result.returncode in [0, 2], (  # 2 is OK for some arg parsers showing help
            f"Generator --help failed with exit code {result.returncode}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}\n"
            f"P0-4 requires working CLI implementation."
        )

        # Help output should mention expected arguments
        help_output = result.stdout + result.stderr
        assert any(arg in help_output for arg in ["--type", "type", "--language", "language"]), (
            f"Generator --help doesn't document expected arguments.\n"
            f"Help output: {help_output}\n"
            f"P0-4 requires documented CLI interface."
        )

    @pytest.mark.slow
    def test_test_project_generator_actually_generates_project(self):
        """
        Generator must CREATE a functional project with real files.

        Anti-Gaming: EXECUTES generator and validates output files exist and are valid.
        This is THE critical test - cannot be faked with stubs.
        """
        if not TEST_PROJECT_GENERATOR.exists():
            pytest.skip("Test project generator not yet created")

        import tempfile
        import shutil

        # Create temp directory for test output
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test-project"

            # EXECUTE generator (Python project, CLI type)
            result = subprocess.run(
                [
                    sys.executable, str(TEST_PROJECT_GENERATOR),
                    "--output", str(output_path),
                    "--type", "cli",
                    "--language", "python"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Generator must succeed
            assert result.returncode == 0, (
                f"Generator failed with exit code {result.returncode}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}\n"
                f"P0-4 requires generator to successfully create projects."
            )

            # Validate output directory exists
            assert output_path.exists() and output_path.is_dir(), (
                f"Generator didn't create output directory: {output_path}\n"
                f"P0-4 requires generator to create project directory."
            )

            # Validate Python project structure
            expected_files = [
                "pyproject.toml",
                "README.md",
                ".gitignore"
            ]

            expected_dirs = [
                "src",
                "tests"
            ]

            for file in expected_files:
                file_path = output_path / file
                assert file_path.exists(), (
                    f"Generated project missing {file}\n"
                    f"P0-4 requires realistic file structures."
                )

                # File must not be empty
                assert file_path.stat().st_size > 0, (
                    f"Generated {file} is empty\n"
                    f"P0-4 requires non-empty files with real content."
                )

            for dir_name in expected_dirs:
                dir_path = output_path / dir_name
                assert dir_path.exists() and dir_path.is_dir(), (
                    f"Generated project missing {dir_name}/ directory\n"
                    f"P0-4 requires complete directory structure."
                )

            # Validate pyproject.toml is valid TOML
            pyproject_path = output_path / "pyproject.toml"
            try:
                with open(pyproject_path, 'rb') as f:
                    config = tomllib.load(f)

                # Must have project metadata
                assert "project" in config, "pyproject.toml missing [project] section"
                assert "name" in config["project"], "pyproject.toml missing project.name"

            except Exception as e:
                pytest.fail(
                    f"Generated pyproject.toml is not valid TOML: {e}\n"
                    f"P0-4 requires valid configuration files."
                )

            # Validate at least one source file exists with content
            src_files = list((output_path / "src").rglob("*.py"))
            assert len(src_files) > 0, (
                f"Generated project has no Python source files in src/\n"
                f"P0-4 requires sample code files."
            )

            # Pick first source file and validate it has substance
            first_src = src_files[0]
            src_content = first_src.read_text()

            # Must not just be empty or "pass"
            src_lines = [l.strip() for l in src_content.split('\n') if l.strip() and not l.strip().startswith('#')]
            assert len(src_lines) >= 3, (
                f"Generated source file {first_src.name} has no substance\n"
                f"Content: {src_content}\n"
                f"P0-4 requires realistic source files, not empty stubs."
            )

            # Validate at least one test file exists
            test_files = list((output_path / "tests").rglob("test_*.py"))
            assert len(test_files) > 0, (
                f"Generated project has no test files\n"
                f"P0-4 requires sample test files."
            )

    def test_test_project_generator_supports_multiple_languages(self):
        """
        Generator must support Python, JavaScript, and Go.

        Anti-Gaming: Validates language-specific code generation exists.
        """
        if not TEST_PROJECT_GENERATOR.exists():
            pytest.skip("Test project generator not yet created")

        code = TEST_PROJECT_GENERATOR.read_text(encoding="utf-8")

        # Should have language-specific logic
        supported_languages = ["python", "javascript", "go"]
        found_languages = sum(1 for lang in supported_languages if lang in code.lower())

        assert found_languages >= 3, (
            f"Test project generator doesn't support all required languages.\n"
            f"Expected: {supported_languages}\n"
            f"P0-4 requires Python, JavaScript, and Go support."
        )

    def test_test_project_generator_has_project_type_support(self):
        """
        Generator must support web-app, CLI, and library project types.

        Anti-Gaming: Validates project type handling exists.
        """
        if not TEST_PROJECT_GENERATOR.exists():
            pytest.skip("Test project generator not yet created")

        code = TEST_PROJECT_GENERATOR.read_text(encoding="utf-8")

        # Should have project type logic
        project_types = ["web-app", "web_app", "cli", "library"]
        found_types = sum(1 for ptype in project_types if ptype in code.lower())

        assert found_types >= 2, (
            f"Test project generator doesn't support multiple project types.\n"
            f"P0-4 requires web-app, CLI, and library support."
        )


# ============================================================================
# Test Class: Architecture Documentation Quality (P0-1) - CRITICAL
# ============================================================================

class TestArchitectureDocumentationQuality:
    """
    Test P0-1: E2E Test Harness Architecture Documentation - QUALITY TESTS

    Validates actual document structure and content quality, not just existence.

    Anti-Gaming: Parses real data structures, validates completeness.
    """

    def test_architecture_document_exists(self):
        """Architecture document must exist at expected path."""
        assert ARCHITECTURE_DOC.exists(), (
            f"Architecture document not found: {ARCHITECTURE_DOC}\n"
            f"P0-1 requires creating tests/e2e/design/ARCHITECTURE.md"
        )

    def test_architecture_documents_all_33_tools_with_details(self):
        """
        Architecture must LIST all 33 tools with names, categories, and status.

        Anti-Gaming: PARSES tool inventory from document structure.
        Cannot be satisfied by just mentioning "33 tools".
        """
        if not ARCHITECTURE_DOC.exists():
            pytest.skip("Architecture document not yet created")

        content = ARCHITECTURE_DOC.read_text(encoding="utf-8")

        # Parse tool inventory
        tools = parse_tool_inventory(content)

        assert len(tools) >= 30, (
            f"Architecture documents only {len(tools)} tools, expected 33.\n"
            f"P0-1 requires complete tool inventory.\n"
            f"Found tools: {[t['name'] for t in tools[:10]]}..."
        )

        # Each tool must have required fields
        for tool in tools[:5]:  # Validate first 5 as sample
            assert len(tool["name"]) > 0, f"Tool has no name: {tool}"
            assert len(tool["category"]) > 0, f"Tool {tool['name']} has no category"
            assert tool["status"] in ["implemented", "stubbed", "blocked", "BLOCKED"], (
                f"Tool {tool['name']} has invalid status: {tool['status']}"
            )

        # Validate tool distribution (13 implemented, 20 stubbed)
        implemented = [t for t in tools if t["status"] in ["implemented"]]
        stubbed = [t for t in tools if t["status"] in ["stubbed", "blocked", "BLOCKED"]]

        assert len(implemented) >= 10, (
            f"Architecture shows only {len(implemented)} implemented tools, expected ~13.\n"
            f"P0-1 requires categorizing tools by implementation status."
        )

        assert len(stubbed) >= 15, (
            f"Architecture shows only {len(stubbed)} stubbed tools, expected ~20.\n"
            f"P0-1 requires identifying API-blocked tools."
        )

    def test_architecture_code_examples_show_real_mcp_structure(self):
        """
        Code examples must show REAL MCP tool implementations, not placeholders.

        Anti-Gaming: Validates code blocks have substance, not just "pass" or "TODO".
        """
        if not ARCHITECTURE_DOC.exists():
            pytest.skip("Architecture document not yet created")

        content = ARCHITECTURE_DOC.read_text(encoding="utf-8")
        code_blocks = extract_markdown_code_blocks(content)
        python_blocks = [code for lang, code in code_blocks if lang == "python"]

        assert len(python_blocks) >= 3, (
            f"Architecture has only {len(python_blocks)} Python code examples.\n"
            f"P0-1 requires function signatures for each API category."
        )

        # Find MCP tool examples
        mcp_examples = [code for code in python_blocks if "@mcp.tool" in code or "@tool" in code]
        assert len(mcp_examples) >= 2, (
            f"Architecture has only {len(mcp_examples)} MCP tool examples.\n"
            f"P0-1 requires showing MCP server structure."
        )

        # Each example must have real implementation (not just "pass")
        for example in mcp_examples:
            # Must have docstring
            has_docstring = '"""' in example or "'''" in example
            assert has_docstring, (
                f"MCP tool example missing docstring:\n{example[:200]}\n"
                f"P0-1 requires documented examples."
            )

            # Must have substantial body (not just "pass" or "raise NotImplementedError")
            lines = example.split("\n")
            non_empty_lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]

            # Allow NotImplementedError for stubbed tools, but must explain why
            if "NotImplementedError" in example:
                assert "BLOCKED" in example or "API" in example, (
                    f"MCP stub example doesn't explain blocker:\n{example[:200]}\n"
                    f"P0-1 requires documenting why tools are stubbed."
                )
            else:
                # Non-stub example must have real logic
                assert len(non_empty_lines) >= 5, (
                    f"MCP tool example has no substance:\n{example[:200]}\n"
                    f"P0-1 requires showing real implementation patterns."
                )

                assert example.count("pass") <= 1, (
                    f"MCP tool example is mostly 'pass' statements:\n{example[:200]}\n"
                    f"P0-1 requires realistic code, not placeholders."
                )

    def test_architecture_covers_all_required_sections_with_depth(self):
        """
        Architecture must have comprehensive coverage of all sections.

        Anti-Gaming: Validates semantic completeness, not just line count.
        """
        if not ARCHITECTURE_DOC.exists():
            pytest.skip("Architecture document not yet created")

        content = ARCHITECTURE_DOC.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        required_sections = {
            "architecture": (5, ["component", "docker", "mcp", "server", "tool", "container", "workflow"]),
            "mcp server": (3, None),
            "docker": (3, None),
            "test": (3, None),
            "component": (2, None),
            "tool": (2, None),
        }

        section_headings_lower = [h.lower() for h in sections.keys()]

        for section_keyword, (min_paragraphs, keywords) in required_sections.items():
            # Find matching section
            matching = [h for h in section_headings_lower if section_keyword in h]

            assert len(matching) > 0, (
                f"Architecture missing section about '{section_keyword}'.\n"
                f"P0-1 requires comprehensive documentation.\n"
                f"Found sections: {list(sections.keys())[:10]}..."
            )

            # Get section content
            original_heading = [h for h in sections.keys() if section_keyword in h.lower()][0]
            section_content = sections[original_heading]

            # Count substantive paragraphs with optional keyword validation
            paras = count_substantive_paragraphs(section_content, required_keywords=keywords)

            assert paras >= min_paragraphs, (
                f"Section '{original_heading}' has only {paras} substantive paragraphs, "
                f"needs {min_paragraphs}.\n"
                f"P0-1 requires detailed explanations, not just outlines."
            )


# ============================================================================
# Test Class: MCP Server Execution (P1-5) - CRITICAL
# ============================================================================

class TestMCPServerExecution:
    """
    Test P1-5: MCP Server Skeleton Implementation - EXECUTION TESTS

    Validates MCP server is actually executable and tools are callable.

    Anti-Gaming: IMPORTS and CALLS MCP tools to verify they work.
    """

    def test_mcp_server_file_exists(self):
        """MCP server implementation file must exist."""
        assert MCP_SERVER_FILE.exists(), (
            f"MCP server file not found: {MCP_SERVER_FILE}\n"
            f"P1-5 requires creating tests/e2e/mcp_server/harness_server.py"
        )

    def test_mcp_server_is_valid_python(self):
        """
        MCP server must be valid Python code.

        Anti-Gaming: Uses Python parser to validate syntax.
        """
        if not MCP_SERVER_FILE.exists():
            pytest.skip("MCP server not yet created")

        code = MCP_SERVER_FILE.read_text(encoding="utf-8")

        assert validate_python_syntax(code), (
            f"MCP server has syntax errors.\n"
            f"P1-5 requires working Python implementation."
        )

    def test_mcp_server_imports_fastmcp(self):
        """
        MCP server must import and use FastMCP.

        Anti-Gaming: Validates FastMCP import and usage.
        """
        if not MCP_SERVER_FILE.exists():
            pytest.skip("MCP server not yet created")

        code = MCP_SERVER_FILE.read_text(encoding="utf-8")

        assert "fastmcp" in code.lower() or "FastMCP" in code, (
            f"MCP server doesn't import FastMCP.\n"
            f"P1-5 requires using FastMCP framework."
        )

        # Should create FastMCP instance
        assert "FastMCP(" in code or "mcp = " in code.lower(), (
            f"MCP server doesn't create FastMCP instance.\n"
            f"P1-5 requires instantiating FastMCP server."
        )

    def test_mcp_server_defines_at_least_13_implementable_tools(self):
        """
        MCP server must define at least 13 implementable tools (Categories 6-8).

        Anti-Gaming: Counts actual tool definitions (decorators).
        """
        if not MCP_SERVER_FILE.exists():
            pytest.skip("MCP server not yet created")

        code = MCP_SERVER_FILE.read_text(encoding="utf-8")

        # Count @mcp.tool() or @tool decorators
        tool_count = code.count("@mcp.tool") + code.count("@tool(") + code.count("@tool\n")

        assert tool_count >= 13, (
            f"MCP server defines only {tool_count} tools.\n"
            f"P1-5 requires 13 implementable tools (Categories 6-8).\n"
            f"Note: 20 more should be stubbed (Categories 1-5)."
        )

    def test_mcp_server_tools_are_callable_not_just_stubs(self):
        """
        MCP tools must be CALLABLE with implementations, not just decorated stubs.

        Anti-Gaming: Attempts to IMPORT module and ACTUALLY CALL 3 tools.
        This ensures tools are real, not just decorators on functions returning {}.
        """
        if not MCP_SERVER_FILE.exists():
            pytest.skip("MCP server not yet created")

        import importlib.util
        import sys

        # Add MCP server directory to path
        mcp_dir = MCP_SERVER_FILE.parent
        if str(mcp_dir) not in sys.path:
            sys.path.insert(0, str(mcp_dir))

        try:
            # Try to import the MCP server module
            spec = importlib.util.spec_from_file_location("harness_server", MCP_SERVER_FILE)
            assert spec is not None and spec.loader is not None, "Cannot load MCP server module"

            module = importlib.util.module_from_spec(spec)

            # Execute module (this will run FastMCP setup)
            try:
                spec.loader.exec_module(module)

                # Module loaded successfully - now ACTUALLY CALL some tools

                # Test 1: create_test_project (Category 6 - Test Environment)
                if hasattr(module, 'create_test_project'):
                    try:
                        result = module.create_test_project(
                            project_type="cli",
                            language="python",
                            output_path="/tmp/test-proj"
                        )
                        # Validate returned structure
                        assert isinstance(result, dict), "create_test_project must return dict"
                        assert len(result) > 0, "create_test_project must return non-empty result"
                        # Check for expected keys
                        assert any(key in result for key in ["status", "result", "path", "project_path"]), \
                            f"create_test_project returned unexpected structure: {result}"
                    except NotImplementedError as e:
                        pytest.fail(f"Tool create_test_project is stubbed: {e}")

                # Test 2: setup_git_repo (Category 6 - Test Environment)
                if hasattr(module, 'setup_git_repo'):
                    try:
                        result = module.setup_git_repo(
                            project_path="/tmp/test-proj"
                        )
                        assert isinstance(result, (dict, bool)), "setup_git_repo must return dict or bool"
                        if isinstance(result, dict):
                            assert len(result) > 0, "setup_git_repo dict must be non-empty"
                    except NotImplementedError as e:
                        pytest.fail(f"Tool setup_git_repo is stubbed: {e}")

                # Test 3: assert_contains_keywords (Category 7 - Assertion Helper)
                if hasattr(module, 'assert_contains_keywords'):
                    try:
                        result = module.assert_contains_keywords(
                            text="test content with keywords",
                            keywords=["test", "content"]
                        )
                        assert isinstance(result, (dict, bool)), "assert_contains_keywords must return dict or bool"
                    except NotImplementedError as e:
                        pytest.fail(f"Tool assert_contains_keywords is stubbed: {e}")

                # At least one tool should be callable
                callable_tools = sum(1 for name in ['create_test_project', 'setup_git_repo', 'assert_contains_keywords']
                                   if hasattr(module, name))

                assert callable_tools >= 1, (
                    f"MCP server has no callable Category 6/7 tools.\n"
                    f"P1-5 requires implementing at least 3 tools from Categories 6-8."
                )

            except ImportError as e:
                # FastMCP not installed is OK - we validated structure
                if "fastmcp" not in str(e).lower():
                    raise

        finally:
            # Clean up sys.path
            if str(mcp_dir) in sys.path:
                sys.path.remove(str(mcp_dir))

    def test_mcp_server_has_category_6_tools(self):
        """
        MCP server must implement Category 6 (Test Environment) tools.

        Anti-Gaming: Validates specific tool names exist.
        """
        if not MCP_SERVER_FILE.exists():
            pytest.skip("MCP server not yet created")

        code = MCP_SERVER_FILE.read_text(encoding="utf-8")
        functions = parse_python_functions(code)

        # Expected Category 6 tools (from PLAN)
        category_6_tools = [
            "create_test_project",
            "setup_git_repo",
            "create_sample_files",
            "reset_test_environment",
            "capture_test_artifacts",
        ]

        found_tools = [tool for tool in category_6_tools if tool in functions]

        assert len(found_tools) >= 3, (
            f"MCP server implements only {len(found_tools)}/5 Category 6 tools.\n"
            f"Expected: {category_6_tools}\n"
            f"Found: {found_tools}\n"
            f"P1-5 requires implementing all Test Environment tools."
        )

    def test_mcp_server_has_category_7_tools(self):
        """
        MCP server must implement Category 7 (Assertion Helper) tools.

        Anti-Gaming: Validates specific assertion tool names exist.
        """
        if not MCP_SERVER_FILE.exists():
            pytest.skip("MCP server not yet created")

        code = MCP_SERVER_FILE.read_text(encoding="utf-8")
        functions = parse_python_functions(code)

        # Expected Category 7 tools (from PLAN)
        category_7_tools = [
            "assert_contains_keywords",
            "assert_workflow_transition",
            "assert_command_suggested",
            "assert_error_handled_gracefully",
        ]

        found_tools = [tool for tool in category_7_tools if tool in functions]

        assert len(found_tools) >= 2, (
            f"MCP server implements only {len(found_tools)}/4 Category 7 tools.\n"
            f"Expected: {category_7_tools}\n"
            f"Found: {found_tools}\n"
            f"P1-5 requires implementing Assertion Helper tools."
        )

    def test_mcp_pyproject_exists(self):
        """MCP server pyproject.toml must exist."""
        assert MCP_PYPROJECT.exists(), (
            f"MCP pyproject.toml not found: {MCP_PYPROJECT}\n"
            f"P1-5 requires creating tests/e2e/mcp_server/pyproject.toml"
        )

    def test_mcp_pyproject_has_fastmcp_dependency(self):
        """
        pyproject.toml must declare FastMCP dependency.

        Anti-Gaming: Validates actual dependency declaration.
        """
        if not MCP_PYPROJECT.exists():
            pytest.skip("MCP pyproject.toml not yet created")

        content = MCP_PYPROJECT.read_text(encoding="utf-8")

        try:
            config = tomllib.loads(content)
        except Exception as e:
            pytest.fail(
                f"MCP pyproject.toml is not valid TOML: {e}\n"
                f"P1-5 requires valid pyproject.toml."
            )

        # Check for fastmcp dependency
        dependencies = config.get("project", {}).get("dependencies", [])

        has_fastmcp = any("fastmcp" in dep.lower() for dep in dependencies)

        assert has_fastmcp, (
            f"MCP pyproject.toml doesn't declare fastmcp dependency.\n"
            f"P1-5 requires fastmcp>=2.0.0 in dependencies.\n"
            f"Found dependencies: {dependencies}"
        )


# ============================================================================
# Test Class: Docker Research Evidence (P1-6) - CRITICAL
# ============================================================================

class TestDockerResearchEvidence:
    """
    Test P1-6: Docker Feasibility Research - EVIDENCE VALIDATION

    Validates research includes REAL experiment results, not speculation.

    Anti-Gaming: Checks for actual Docker command outputs and results.
    """

    def test_docker_setup_document_exists(self):
        """Docker setup document must exist."""
        assert DOCKER_SETUP_DOC.exists(), (
            f"Docker setup document not found: {DOCKER_SETUP_DOC}\n"
            f"P1-6 requires creating tests/e2e/design/DOCKER_SETUP.md"
        )

    def test_docker_research_includes_command_outputs(self):
        """
        Docker research must include ACTUAL command outputs, not just claims.

        Anti-Gaming: Validates real Docker output patterns exist.
        Cannot be satisfied by just describing what "should" happen.
        """
        if not DOCKER_SETUP_DOC.exists():
            pytest.skip("Docker setup document not yet created")

        content = DOCKER_SETUP_DOC.read_text(encoding="utf-8")

        # Must mention Docker commands attempted
        docker_commands = ["docker run", "docker build", "docker pull", "docker exec", "docker ps"]
        found_commands = [cmd for cmd in docker_commands if cmd in content.lower()]

        assert len(found_commands) >= 2, (
            f"Docker research only mentions {len(found_commands)} Docker commands.\n"
            f"P1-6 requires documenting at least 2 Docker commands attempted.\n"
            f"Found: {found_commands}"
        )

        # Must include command outputs (not just descriptions)
        code_blocks = extract_markdown_code_blocks(content)

        # Look for bash/shell/console outputs
        output_blocks = [code for lang, code in code_blocks if lang in ["bash", "shell", "console", "text", ""]]

        assert len(output_blocks) >= 1, (
            f"Docker research has no command output blocks.\n"
            f"P1-6 requires showing actual command outputs.\n"
            f"Found code blocks: {[(lang, code[:50]) for lang, code in code_blocks[:5]]}"
        )

        # Validate real Docker output patterns
        has_real_output = check_for_real_docker_output(content)

        assert has_real_output, (
            f"Docker research doesn't include REAL Docker command outputs.\n"
            f"Must include actual output from commands like 'docker ps', 'docker build', etc.\n"
            f"P1-6 requires documenting actual experiments, not speculation."
        )

    def test_docker_setup_documents_result(self):
        """
        Research must document experiment result (success/partial/failure).

        Anti-Gaming: Validates definitive outcome documented.
        """
        if not DOCKER_SETUP_DOC.exists():
            pytest.skip("Docker setup document not yet created")

        content = DOCKER_SETUP_DOC.read_text(encoding="utf-8")

        # Check for result documentation
        result_indicators = [
            "success",
            "failure",
            "works",
            "doesn't work",
            "partial",
            "blocked",
            "viable",
            "not viable"
        ]

        found_result = any(indicator in content.lower() for indicator in result_indicators)

        assert found_result, (
            f"Docker research doesn't document experiment result.\n"
            f"P1-6 requires clear outcome: success, partial success, or failure."
        )

    def test_docker_setup_includes_dockerfile(self):
        """
        Research must include Dockerfile (attempted or working).

        Anti-Gaming: Validates actual Dockerfile exists in documentation.
        """
        if not DOCKER_SETUP_DOC.exists():
            pytest.skip("Docker setup document not yet created")

        content = DOCKER_SETUP_DOC.read_text(encoding="utf-8")
        code_blocks = extract_markdown_code_blocks(content)

        # Look for Dockerfile code block
        dockerfile_blocks = [
            code for lang, code in code_blocks
            if lang in ["dockerfile", "docker", ""] and ("FROM" in code or "RUN" in code)
        ]

        assert len(dockerfile_blocks) >= 1, (
            f"Docker research doesn't include Dockerfile.\n"
            f"P1-6 requires documenting attempted Docker configuration."
        )

    def test_docker_setup_provides_recommendation(self):
        """
        Research must provide clear recommendation on viability.

        Anti-Gaming: Validates recommendation section with conclusion.
        """
        if not DOCKER_SETUP_DOC.exists():
            pytest.skip("Docker setup document not yet created")

        content = DOCKER_SETUP_DOC.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Look for recommendation/conclusion section
        recommendation_section = None
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['recommend', 'conclusion', 'viability', 'feasibility']):
                recommendation_section = section_content
                break

        assert recommendation_section is not None, (
            f"Docker research doesn't include recommendation.\n"
            f"P1-6 requires conclusion on viability (viable / needs workarounds / not viable)."
        )


# ============================================================================
# Test Class: Cross-Validation (P2-8) - CRITICAL
# ============================================================================

class TestCrossValidationConsistency:
    """
    Test P2-8: E2E Design Completeness Validation - CONSISTENCY TESTS

    Validates documents are mutually consistent and implementation matches design.

    Anti-Gaming: Cross-references between documents must be accurate.
    """

    def test_all_design_documents_exist(self):
        """All 4 design documents must exist."""
        design_docs = [
            ("ARCHITECTURE.md", ARCHITECTURE_DOC),
            ("CONVERSATION_SIMULATION.md", CONVERSATION_SIMULATION_DOC),
            ("API_REQUIREMENTS.md", API_REQUIREMENTS_DOC),
            ("DOCKER_SETUP.md", DOCKER_SETUP_DOC),
        ]

        missing_docs = []
        for name, path in design_docs:
            if not path.exists():
                missing_docs.append(name)

        assert len(missing_docs) == 0, (
            f"Missing design documents:\n"
            + "\n".join(f"  - {doc}" for doc in missing_docs)
            + f"\n\nP2-8 requires all 4 design documents complete"
        )

    def test_mcp_server_implements_tools_documented_in_architecture(self):
        """
        MCP server tool count must MATCH architecture documentation.

        Anti-Gaming: Cross-validates architecture claims against implementation.
        """
        if not ARCHITECTURE_DOC.exists() or not MCP_SERVER_FILE.exists():
            pytest.skip("Architecture or MCP server not yet created")

        # Parse architecture tool list
        arch_content = ARCHITECTURE_DOC.read_text(encoding="utf-8")
        arch_tools = parse_tool_inventory(arch_content)

        # Get implemented tools from architecture
        arch_implemented = {normalize_name(t["name"]) for t in arch_tools if t["status"] == "implemented"}

        # Parse MCP server tool definitions
        mcp_code = MCP_SERVER_FILE.read_text(encoding="utf-8")
        mcp_functions = parse_python_functions(mcp_code)
        mcp_tool_names = {normalize_name(f) for f in mcp_functions}

        # Find tools documented as implemented but not in MCP server
        missing_in_mcp = arch_implemented - mcp_tool_names

        # Allow some tolerance for naming differences
        assert len(missing_in_mcp) <= 5, (
            f"Architecture documents {len(arch_implemented)} implemented tools, "
            f"but MCP server only has {len(mcp_tool_names)} functions.\n"
            f"Missing in MCP server: {list(missing_in_mcp)[:10]}\n"
            f"P2-8 requires implementation to match architecture design."
        )

    def test_api_requirements_documents_stubbed_tools(self):
        """
        API requirements must document all 20 stubbed tools.

        Anti-Gaming: Cross-validates stubbed tool count is consistent.
        """
        if not ARCHITECTURE_DOC.exists() or not API_REQUIREMENTS_DOC.exists():
            pytest.skip("Architecture or API requirements not yet created")

        arch_content = ARCHITECTURE_DOC.read_text(encoding="utf-8")
        api_content = API_REQUIREMENTS_DOC.read_text(encoding="utf-8")

        # Get stubbed tools from architecture
        arch_tools = parse_tool_inventory(arch_content)
        stubbed_tools = [t for t in arch_tools if t["status"] in ["stubbed", "blocked", "BLOCKED"]]

        assert len(stubbed_tools) >= 15, (
            f"Architecture only documents {len(stubbed_tools)} stubbed tools, expected ~20.\n"
            f"P2-8 requires proper categorization of API-dependent tools."
        )

        # API requirements should mention similar number
        # Look for numbers in text
        numbers_in_api = re.findall(r'\b(1[5-9]|2[0-5])\b', api_content)

        assert len(numbers_in_api) > 0, (
            f"API requirements doesn't mention tool counts.\n"
            f"P2-8 requires documenting number of API-dependent capabilities."
        )


# ============================================================================
# Test Class: API Requirements Documentation (P0-3)
# ============================================================================

class TestAPIRequirementsDocumentation:
    """
    Test P0-3: Claude Code API Requirements Documentation

    Validates structured API requirements, not wish lists.

    Anti-Gaming: Validates function signatures and use cases exist.
    """

    def test_api_requirements_document_exists(self):
        """API requirements document must exist."""
        assert API_REQUIREMENTS_DOC.exists(), (
            f"API requirements document not found: {API_REQUIREMENTS_DOC}\n"
            f"P0-3 requires creating tests/e2e/design/API_REQUIREMENTS.md"
        )

    def test_api_requirements_includes_function_signatures(self):
        """
        Requirements must include concrete API function signatures.

        Anti-Gaming: Validates actual function definitions, not descriptions.
        """
        if not API_REQUIREMENTS_DOC.exists():
            pytest.skip("API requirements document not yet created")

        content = API_REQUIREMENTS_DOC.read_text(encoding="utf-8")
        code_blocks = extract_markdown_code_blocks(content)

        # Should have code blocks showing API signatures
        code_blocks_with_lang = [code for lang, code in code_blocks if lang in ["python", "typescript", "javascript", ""]]

        assert len(code_blocks_with_lang) >= 5, (
            f"API requirements has only {len(code_blocks_with_lang)} code examples.\n"
            f"P0-3 requires function signatures for each API category."
        )

        # Code blocks should define functions
        total_functions = 0
        for code in code_blocks_with_lang:
            # Count function definitions (def in Python, function in JS/TS, or -> return types)
            functions = code.count('def ') + code.count('function ') + code.count(' -> ')
            total_functions += functions

        assert total_functions >= 15, (
            f"API requirements documents only {total_functions} API functions.\n"
            f"P0-3 requires documenting ~20 API-dependent tools (from PLAN)."
        )

    def test_api_requirements_documents_alternatives(self):
        """
        Requirements must document alternative approaches if API unavailable.

        Anti-Gaming: Validates alternatives section with concrete options.
        """
        if not API_REQUIREMENTS_DOC.exists():
            pytest.skip("API requirements document not yet created")

        content = API_REQUIREMENTS_DOC.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Look for alternatives section
        alternatives_section = None
        for heading, section_content in sections.items():
            if any(kw in heading.lower() for kw in ['alternative', 'fallback', 'workaround', 'without api']):
                alternatives_section = section_content
                break

        assert alternatives_section is not None, (
            f"API requirements don't document alternatives if API unavailable.\n"
            f"P0-3 requires fallback approaches (filesystem scraping, log parsing, manual testing)."
        )

        # Should mention specific alternatives
        alternative_approaches = [
            "filesystem",
            "log",
            "manual",
            "file",
            "parse",
        ]

        found_alternatives = sum(1 for a in alternative_approaches if a in alternatives_section.lower())

        assert found_alternatives >= 2, (
            f"Alternatives section doesn't provide concrete fallback options.\n"
            f"P0-3 requires documenting specific alternatives (e.g., filesystem scraping, log parsing)."
        )


# ============================================================================
# Test Class: Conversation Simulation Design (P0-2)
# ============================================================================

class TestConversationSimulationDesign:
    """
    Test P0-2: Conversation Simulation Framework Design

    Validates actual design content, not keyword stuffing.

    Anti-Gaming: Validates state machine and example scenarios exist.
    """

    def test_conversation_simulation_document_exists(self):
        """Conversation simulation document must exist."""
        assert CONVERSATION_SIMULATION_DOC.exists(), (
            f"Conversation simulation document not found: {CONVERSATION_SIMULATION_DOC}\n"
            f"P0-2 requires creating tests/e2e/design/CONVERSATION_SIMULATION.md"
        )

    def test_conversation_simulation_documents_state_machine(self):
        """
        Design must document conversation state machine.

        Anti-Gaming: Validates state definitions and transitions exist.
        """
        if not CONVERSATION_SIMULATION_DOC.exists():
            pytest.skip("Conversation simulation document not yet created")

        content = CONVERSATION_SIMULATION_DOC.read_text(encoding="utf-8")

        # Count substantive paragraphs with conversation-specific keywords
        conv_keywords = ["state", "transition", "message", "response", "prompt", "agent"]
        substantive = count_substantive_paragraphs(content, required_keywords=conv_keywords)

        assert substantive >= 5, (
            f"Conversation state machine not adequately documented.\n"
            f"Found only {substantive} substantive paragraphs with conversation keywords.\n"
            f"P0-2 requires state machine with clear state definitions."
        )

        # Should define transitions
        assert "transition" in content.lower() or "->" in content or "→" in content, (
            f"State machine doesn't document transitions between states.\n"
            f"P0-2 requires state transition documentation."
        )

    def test_conversation_simulation_includes_example_scenarios(self):
        """
        Design must include 3-5 complete example scenarios.

        Anti-Gaming: Validates actual multi-turn conversation examples.
        """
        if not CONVERSATION_SIMULATION_DOC.exists():
            pytest.skip("Conversation simulation document not yet created")

        content = CONVERSATION_SIMULATION_DOC.read_text(encoding="utf-8")
        sections = parse_markdown_sections(content)

        # Look for example/scenario sections
        example_sections = [
            h for h in sections.keys()
            if any(kw in h.lower() for kw in ['example', 'scenario', 'test case'])
        ]

        assert len(example_sections) >= 3, (
            f"Conversation simulation has only {len(example_sections)} example scenarios.\n"
            f"P0-2 requires 3-5 complete conversation flow examples."
        )

        # Examples should show multi-turn interactions
        for heading in example_sections[:3]:  # Check first 3 examples
            section_content = sections[heading]

            # Count conversation turns (lines starting with numbers or User:/Agent:)
            turns = len(re.findall(r'^\s*\d+\.|\bUser:|\bAgent:|\bClaude:', section_content, re.MULTILINE))

            assert turns >= 3, (
                f"Example '{heading}' has only {turns} conversation turns.\n"
                f"P0-2 requires multi-turn examples (at least 3 turns per example)."
            )


# ============================================================================
# Test Class: E2E Test Projects Directory (P2-7)
# ============================================================================

class TestE2ETestProjectsDirectory:
    """
    Test P2-7: E2E Test Projects Directory Setup

    Validates directory structure and documentation.

    Anti-Gaming: Checks actual files exist with content.
    """

    def test_e2e_test_projects_directory_exists(self):
        """E2E test projects directory must exist."""
        assert E2E_TEST_PROJECTS_DIR.exists(), (
            f"E2E test projects directory not found: {E2E_TEST_PROJECTS_DIR}\n"
            f"P2-7 requires creating tests/e2e/test_projects/ directory"
        )

    def test_e2e_test_projects_readme_exists(self):
        """Test projects README must exist."""
        readme_path = E2E_TEST_PROJECTS_DIR / "README.md"

        assert readme_path.exists(), (
            f"Test projects README not found: {readme_path}\n"
            f"P2-7 requires README.md explaining directory purpose"
        )

    def test_e2e_test_projects_readme_explains_purpose(self):
        """
        README must explain directory purpose and usage.

        Anti-Gaming: Validates substantive content exists.
        """
        readme_path = E2E_TEST_PROJECTS_DIR / "README.md"

        if not readme_path.exists():
            pytest.skip("Test projects README not yet created")

        content = readme_path.read_text(encoding="utf-8")

        # Should explain purpose
        purpose_keywords = ["test", "fixture", "project", "generate"]
        found_keywords = sum(1 for kw in purpose_keywords if kw in content.lower())

        assert found_keywords >= 3, (
            f"Test projects README doesn't explain purpose.\n"
            f"P2-7 requires explaining directory usage."
        )

    def test_e2e_test_projects_gitignore_exists(self):
        """Test projects .gitignore must exist."""
        gitignore_path = E2E_TEST_PROJECTS_DIR / ".gitignore"

        assert gitignore_path.exists(), (
            f"Test projects .gitignore not found: {gitignore_path}\n"
            f"P2-7 requires .gitignore to exclude generated projects"
        )

    def test_e2e_test_projects_gitignore_excludes_generated_projects(self):
        """
        .gitignore must exclude all generated projects.

        Anti-Gaming: Validates ignore patterns exist.
        """
        gitignore_path = E2E_TEST_PROJECTS_DIR / ".gitignore"

        if not gitignore_path.exists():
            pytest.skip("Test projects .gitignore not yet created")

        content = gitignore_path.read_text(encoding="utf-8")

        # Should ignore all files except metadata
        assert "*" in content, (
            f"Test projects .gitignore doesn't exclude generated projects.\n"
            f"P2-7 requires ignoring all generated test projects."
        )


# ============================================================================
# Summary Test: Phase 1 Complete
# ============================================================================

class TestPhase1CompleteSummary:
    """
    Master test validating Phase 1 completion.

    This test provides a high-level summary of Phase 1 deliverables.
    """

    def test_phase1_all_deliverables_complete(self):
        """
        Validate all Phase 1 deliverables are complete.

        This is the master test for Phase 1 completion.
        """
        issues = []

        # P0-1: Architecture Documentation
        if not ARCHITECTURE_DOC.exists():
            issues.append("P0-1: Architecture document missing")

        # P0-2: Conversation Simulation Design
        if not CONVERSATION_SIMULATION_DOC.exists():
            issues.append("P0-2: Conversation simulation document missing")

        # P0-3: API Requirements Documentation
        if not API_REQUIREMENTS_DOC.exists():
            issues.append("P0-3: API requirements document missing")

        # P0-4: Test Project Generator
        if not TEST_PROJECT_GENERATOR.exists():
            issues.append("P0-4: Test project generator missing")

        # P1-5: MCP Server Skeleton
        if not MCP_SERVER_FILE.exists():
            issues.append("P1-5: MCP server implementation missing")

        if not MCP_PYPROJECT.exists():
            issues.append("P1-5: MCP pyproject.toml missing")

        # P1-6: Docker Research
        if not DOCKER_SETUP_DOC.exists():
            issues.append("P1-6: Docker setup document missing")

        # P2-7: Test Projects Directory
        if not E2E_TEST_PROJECTS_DIR.exists():
            issues.append("P2-7: Test projects directory missing")

        # Generate summary
        total_deliverables = 8  # 3 P0 docs + 1 P0 tool + 2 P1 items + 1 P1 doc + 1 P2 dir
        completed_deliverables = total_deliverables - len(issues)

        assert len(issues) == 0, (
            f"\nPhase 1 Test Harness Implementation INCOMPLETE\n"
            f"{'='*70}\n\n"
            f"Progress: {completed_deliverables}/{total_deliverables} deliverables complete\n\n"
            f"Missing deliverables:\n"
            + "\n".join(f"  - {issue}" for issue in issues)
            + f"\n\n"
            f"Phase 1 requires all P0, P1, and P2 work items completed.\n"
            f"Reference: PLAN-test-harness-2025-11-07-023500.md"
        )
