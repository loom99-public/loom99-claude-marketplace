#!/bin/bash
#
# Quick test runner for skills restructuring validation
#
# Usage:
#   ./run_tests.sh              # Run all tests
#   ./run_tests.sh structure    # Run structure tests only
#   ./run_tests.sh frontmatter  # Run YAML frontmatter tests only
#   ./run_tests.sh config       # Run plugin config tests only
#   ./run_tests.sh content      # Run content preservation tests only
#   ./run_tests.sh complete     # Run completeness tests only
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${YELLOW}Skills Restructuring Test Suite${NC}"
echo "================================"
echo ""

# Check if dependencies are installed
if ! python3 -c "import pytest" 2>/dev/null; then
    echo -e "${YELLOW}Installing test dependencies...${NC}"
    uv pip install -e .
    echo ""
fi

# Determine which tests to run
TEST_FILTER=""
case "${1:-all}" in
    structure)
        TEST_FILTER="TestSkillsDirectoryStructure"
        echo "Running: Structure validation tests"
        ;;
    frontmatter)
        TEST_FILTER="TestSkillsYAMLFrontmatter"
        echo "Running: YAML frontmatter tests"
        ;;
    config)
        TEST_FILTER="TestPluginConfiguration"
        echo "Running: Plugin configuration tests"
        ;;
    content)
        TEST_FILTER="TestContentPreservation"
        echo "Running: Content preservation tests"
        ;;
    complete)
        TEST_FILTER="TestCompletenessAndCorrectness"
        echo "Running: Completeness validation tests"
        ;;
    all|*)
        echo "Running: All functional tests"
        ;;
esac

echo ""

# Run tests
if [ -n "$TEST_FILTER" ]; then
    pytest tests/functional/test_skills_structure.py::$TEST_FILTER -v
else
    pytest tests/functional/ -v
fi

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "Skills restructuring is complete and correct."
else
    echo -e "${RED}✗ Some tests failed.${NC}"
    echo ""
    echo "Skills restructuring is incomplete or has issues."
    echo "See test output above for details."
    echo ""
    echo "Expected failures BEFORE restructuring:"
    echo "  - Structure tests (skills not in subdirectories)"
    echo "  - YAML tests (no frontmatter yet)"
    echo "  - Config tests (missing skills key in plugin.json)"
    echo ""
    echo "After restructuring, all tests should pass."
fi

exit $TEST_EXIT_CODE
