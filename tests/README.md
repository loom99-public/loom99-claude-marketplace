# Functional Tests - Skills Restructuring

This directory contains comprehensive functional tests for the skills restructuring work described in `NEXT_STEPS.md`.

## Overview

The loom99 Claude marketplace has a critical issue: all 13 skills across 3 plugins use flat markdown files instead of the required subdirectory structure with `SKILL.md` files. This prevents the plugins from functioning in Claude Code.

These tests validate that the restructuring work is complete and correct.

## What These Tests Validate

### 1. Directory Structure (Issue #1 from NEXT_STEPS.md)

**Requirements:**
- Each skill must be in its own subdirectory
- Each subdirectory must contain a `SKILL.md` file
- No flat `.md` files should remain in `skills/` directories

**Tests:**
- `test_plugin_skills_directory_exists` - Validates skills directories exist
- `test_all_skills_use_subdirectories` - Checks each skill has a subdirectory
- `test_no_flat_markdown_files_in_skills_directory` - Ensures old flat structure removed
- `test_each_skill_has_skill_md_file` - Verifies SKILL.md files present
- `test_total_skill_count` - Confirms all 13 skills are restructured
- `test_skill_subdirectories_match_expected_names` - Validates naming correctness

### 2. YAML Frontmatter (Issue #2 from NEXT_STEPS.md)

**Requirements:**
- Each `SKILL.md` must have YAML frontmatter
- Must contain `name` and `description` fields
- Name must match directory name
- Description must be non-empty and ≤1024 characters

**Tests:**
- `test_all_skills_have_yaml_frontmatter` - Validates frontmatter exists
- `test_yaml_frontmatter_has_required_fields` - Checks required fields present
- `test_yaml_name_matches_directory_name` - Ensures name consistency
- `test_yaml_description_is_valid` - Validates description format/length

### 3. Plugin Configuration

**Requirements:**
- Each `plugin.json` must have a `skills` key
- Skills path must point to valid directory

**Tests:**
- `test_plugin_json_exists` - Validates plugin.json files exist
- `test_plugin_json_is_valid_json` - Ensures valid JSON format
- `test_plugin_json_has_skills_path` - Checks skills key present
- `test_skills_path_points_to_valid_directory` - Verifies path correctness

### 4. Content Preservation

**Requirements:**
- All original skill content must be preserved
- Skills should have substantial content (100+ lines)
- Markdown content must exist after frontmatter

**Tests:**
- `test_skill_files_have_substantial_content` - Validates minimum 100 lines
- `test_skill_has_markdown_content_after_frontmatter` - Ensures content exists
- `test_total_content_size_preserved` - Verifies ~8,921 total lines preserved

### 5. Completeness Checks

**Meta-tests that validate all requirements:**
- `test_all_plugins_have_all_expected_skills` - Comprehensive structure check
- `test_no_unexpected_files_in_skills_directories` - Catches leftover files
- `test_restructuring_meets_all_requirements` - Final validation of all requirements

## Test Coverage

**Plugins tested:** 3
- agent-loop (4 skills)
- epti (5 skills)
- visual-iteration (4 skills)

**Total skills validated:** 13

**Test categories:**
- Structure validation: 6 test functions
- YAML frontmatter: 4 test functions
- Plugin configuration: 4 test functions
- Content preservation: 3 test functions
- Completeness: 3 test functions

**Total test cases:** 20 test functions × multiple parametrizations = **60+ individual test cases**

## Why These Tests Are Un-Gameable

These tests cannot be satisfied by stubs, mocks, or shortcuts because:

1. **Real File System Validation**: Tests verify actual directories and files exist on disk
2. **Content Parsing**: Tests parse actual YAML and validate structure
3. **Multiple Verification Points**: Each aspect is checked from multiple angles
4. **Concrete Assertions**: Tests check specific, observable outcomes (file sizes, YAML fields, directory names)
5. **Cross-Validation**: Tests validate consistency between multiple sources (directory names vs YAML names vs expected skills)
6. **Content Size Checks**: Tests ensure substantial content exists (not just empty files with frontmatter)

An AI cannot fake:
- Actual directory structure on filesystem
- Valid YAML that parses correctly
- Specific file sizes and line counts
- Consistency between file names and YAML content

## Running the Tests

### Prerequisites

Install dependencies using `uv`:

```bash
cd /Users/bmf/Library/Mobile\ Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace
uv pip install -e .
```

Or using the symlink:

```bash
cd ~/icode/loom99-claude-marketplace
uv pip install -e .
```

### Run All Tests

```bash
# Using pytest directly
pytest tests/functional/

# Using uv
uv run pytest tests/functional/

# Verbose output
pytest tests/functional/ -v

# Show test summary
pytest tests/functional/ -v --tb=short
```

### Run Specific Test Categories

```bash
# Structure tests only
pytest tests/functional/test_skills_structure.py::TestSkillsDirectoryStructure -v

# YAML frontmatter tests only
pytest tests/functional/test_skills_structure.py::TestSkillsYAMLFrontmatter -v

# Plugin configuration tests only
pytest tests/functional/test_skills_structure.py::TestPluginConfiguration -v

# Content preservation tests only
pytest tests/functional/test_skills_structure.py::TestContentPreservation -v

# Completeness tests only
pytest tests/functional/test_skills_structure.py::TestCompletenessAndCorrectness -v
```

### Run Tests for Specific Plugin

```bash
# Test only agent-loop
pytest tests/functional/ -k "agent-loop" -v

# Test only epti
pytest tests/functional/ -k "epti" -v

# Test only visual-iteration
pytest tests/functional/ -k "visual-iteration" -v
```

## Expected Test Results

### Current State (Before Restructuring)

**Status**: ❌ **ALL TESTS SHOULD FAIL**

Expected failures:
- Structure tests fail: Skills are flat `.md` files, not in subdirectories
- YAML tests fail: No frontmatter exists yet
- Config tests fail: `plugin.json` files missing `skills` key
- Content tests fail: Files don't exist in expected locations

Example output:
```
FAILED tests/functional/test_skills_structure.py::TestSkillsDirectoryStructure::test_all_skills_use_subdirectories[agent-loop]
FAILED tests/functional/test_skills_structure.py::TestSkillsDirectoryStructure::test_no_flat_markdown_files_in_skills_directory[agent-loop]
...
============ 60 failed in 2.43s ============
```

### After Restructuring (Success State)

**Status**: ✅ **ALL TESTS SHOULD PASS**

Expected results:
- All directory structure tests pass
- All YAML frontmatter tests pass
- All plugin configuration tests pass
- All content preservation tests pass
- All completeness checks pass

Example output:
```
tests/functional/test_skills_structure.py::TestSkillsDirectoryStructure::test_plugin_skills_directory_exists[agent-loop] PASSED
tests/functional/test_skills_structure.py::TestSkillsDirectoryStructure::test_all_skills_use_subdirectories[agent-loop] PASSED
...
============ 60 passed in 3.12s ============
```

## Traceability to NEXT_STEPS.md

This test suite directly validates the requirements in `NEXT_STEPS.md`:

| NEXT_STEPS.md Section | Test Class | Validation |
|----------------------|------------|------------|
| Issue #1: Skills Directory Structure | `TestSkillsDirectoryStructure` | ✅ Subdirectories, SKILL.md files, no flat files |
| Issue #2: Missing YAML Frontmatter | `TestSkillsYAMLFrontmatter` | ✅ Frontmatter format, required fields, validation |
| Step 4: Update plugin.json References | `TestPluginConfiguration` | ✅ Skills key, valid paths |
| Content Preservation | `TestContentPreservation` | ✅ Line counts, content size |
| Validation Checklist | `TestCompletenessAndCorrectness` | ✅ All requirements met |

## Test Metrics

**Lines of Test Code**: ~700 lines
**Test Functions**: 20
**Parametrized Test Cases**: 60+
**Plugins Covered**: 3 (100%)
**Skills Covered**: 13 (100%)

## Continuous Integration

These tests are designed to be run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Validate Skills Structure

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e .
      - name: Run tests
        run: pytest tests/functional/ -v
```

## Contributing

When adding new skills or plugins:

1. Update `EXPECTED_SKILLS` dict in `test_skills_structure.py`
2. Update `TOTAL_EXPECTED_SKILLS` constant
3. Run tests to verify new skills follow correct structure
4. Ensure all tests pass before committing

## References

- **NEXT_STEPS.md**: Complete problem description and fix plan
- **CLAUDE.md**: Project overview and implementation metrics
- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Claude Code Plugin Structure](https://docs.claude.com/en/docs/claude-code/plugins)

## Questions?

If tests fail unexpectedly:

1. Check that skills are in subdirectories with `SKILL.md` files
2. Verify YAML frontmatter is properly formatted
3. Ensure `plugin.json` files have `skills` key
4. Confirm no flat `.md` files remain in `skills/` directories

For issues with the test suite itself, see the test file docstrings for detailed explanations of what each test validates and why it's structured that way.
