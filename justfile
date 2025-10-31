# Justfile for loom99 Claude Marketplace
# Common tasks for marketplace development and validation

# Default recipe - show available commands
default:
    @just --list

# Validate marketplace structure and all plugins
validate:
    @echo "🔍 Validating marketplace structure..."
    claude plugin validate .
    @echo "✅ Validation complete!"

# Run comprehensive test suite
test:
    @echo "🧪 Running functional tests..."
    ./run_tests.sh
    @echo ""
    @echo "📊 Test Summary:"
    @pytest tests/functional/test_skills_structure.py -v --tb=short

# Run quick structure validation tests only
test-structure:
    @echo "🧪 Running structure tests..."
    ./run_tests.sh structure

# Run Phase 2 verbosity reduction tests
test-phase2:
    @echo "🧪 Running Phase 2 reduction tests..."
    @pytest tests/functional/test_phase2_reductions.py -v --tb=short
    @echo ""
    @echo "📊 Phase 2 Status:"
    @pytest tests/functional/test_phase2_reductions.py::TestPhase2ValidationSummary::test_phase2_reduction_targets_met -v --tb=short

# Run Phase 2 tests (quiet mode for quick checks)
test-phase2-quick:
    @echo "🧪 Quick Phase 2 check..."
    @pytest tests/functional/test_phase2_reductions.py --tb=no -q

# Run Phase 2 tests for specific plugin
test-phase2-plugin plugin:
    @echo "🧪 Testing Phase 2 for {{plugin}}..."
    @pytest tests/functional/test_phase2_reductions.py -k "{{plugin}}" -v --tb=short

# Show current Phase 2 metrics
phase2-metrics:
    @echo "📊 Phase 2 Current Metrics"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo ""
    @echo "Skills:"
    @echo "  Total: $(find plugins/*/skills -name "SKILL.md" -exec wc -l {} + | tail -1 | awk '{print $1}') lines (target: 4,030)"
    @echo "  agent-loop:"
    @for skill in plugins/agent-loop/skills/*/SKILL.md; do echo "    - $(basename $(dirname $$skill)): $(wc -l < $$skill) lines"; done
    @echo "  epti:"
    @for skill in plugins/epti/skills/*/SKILL.md; do echo "    - $(basename $(dirname $$skill)): $(wc -l < $$skill) lines"; done
    @echo "  visual-iteration:"
    @for skill in plugins/visual-iteration/skills/*/SKILL.md; do echo "    - $(basename $(dirname $$skill)): $(wc -l < $$skill) lines"; done
    @echo ""
    @echo "READMEs:"
    @echo "  Total: $(wc -l plugins/*/README.md | tail -1 | awk '{print $1}') lines (target: 1,050)"
    @echo "  agent-loop: $(wc -l < plugins/agent-loop/README.md) lines (target: 200)"
    @echo "  epti: $(wc -l < plugins/epti/README.md) lines (target: 350)"
    @echo "  visual-iteration: $(wc -l < plugins/visual-iteration/README.md) lines (target: 500)"

# Install test dependencies
install-deps:
    @echo "📦 Installing test dependencies..."
    uv pip install --system pytest PyYAML
    @echo "✅ Dependencies installed!"

# Run full verification (validate + test)
verify: validate test
    @echo ""
    @echo "✅ All verification checks passed!"
    @echo "   - Marketplace structure valid"
    @echo "   - All plugins valid"
    @echo "   - All functional tests passing"

# Clean test artifacts and caches
clean:
    @echo "🧹 Cleaning test artifacts..."
    rm -rf .pytest_cache
    rm -rf tests/__pycache__
    rm -rf tests/functional/__pycache__
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -delete
    @echo "✅ Cleanup complete!"

# Show marketplace info
info:
    @echo "📦 loom99 Claude Marketplace"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo "Owner: Brandon Fryslie"
    @echo "Plugins: 3"
    @echo ""
    @echo "Available Plugins:"
    @echo "  • agent-loop (v0.1.0) - Agentic Software Engineering Loop"
    @echo "  • epti (v0.1.0) - Evaluate-Plan-Test-Implement TDD Workflow"
    @echo "  • visual-iteration (v0.1.0) - Screenshot-Driven UI Development"
    @echo ""
    @echo "Total Skills: 13"
    @echo "Total Commands: 16"
    @echo "Total Agents: 3"

# Check skills structure (quick diagnostic)
check-skills:
    @echo "🔍 Checking skills structure..."
    @echo ""
    @echo "agent-loop skills:"
    @ls -1 plugins/agent-loop/skills/
    @echo ""
    @echo "epti skills:"
    @ls -1 plugins/epti/skills/
    @echo ""
    @echo "visual-iteration skills:"
    @ls -1 plugins/visual-iteration/skills/

# Show plugin statistics
stats:
    @echo "📊 Marketplace Statistics"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo ""
    @echo "Code Lines:"
    @echo "  agent-loop:        $(find plugins/agent-loop -name "*.md" -exec wc -l {} + | tail -1 | awk '{print $1}') lines"
    @echo "  epti:              $(find plugins/epti -name "*.md" -exec wc -l {} + | tail -1 | awk '{print $1}') lines"
    @echo "  visual-iteration:  $(find plugins/visual-iteration -name "*.md" -exec wc -l {} + | tail -1 | awk '{print $1}') lines"
    @echo ""
    @echo "Components:"
    @echo "  Skills:   $(find plugins/*/skills -name "SKILL.md" | wc -l | tr -d ' ')"
    @echo "  Commands: $(find plugins/*/commands -name "*.md" | wc -l | tr -d ' ')"
    @echo "  Agents:   $(find plugins/*/agents -name "*.md" | wc -l | tr -d ' ')"
    @echo "  Hooks:    $(find plugins/*/hooks -name "hooks.json" | wc -l | tr -d ' ')"

# Initialize git repository (if not already initialized)
git-init:
    @if [ ! -d .git ]; then \
        echo "🔧 Initializing git repository..."; \
        git init; \
        git add .; \
        git commit -m "feat(marketplace): initial commit of loom99 marketplace\n\n- Add agent-loop plugin with 4-stage workflow\n- Add epti plugin with TDD workflow\n- Add visual-iteration plugin with screenshot-driven development\n- Include 24,459 lines of implementation across 3 plugins"; \
        echo "✅ Git repository initialized!"; \
    else \
        echo "ℹ️  Git repository already initialized"; \
    fi

# Run development checks (before committing)
pre-commit: clean validate test
    @echo ""
    @echo "✅ Pre-commit checks passed!"
    @echo "   Safe to commit your changes."
