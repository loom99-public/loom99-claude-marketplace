# Justfile for loom99 Claude Marketplace
# Common tasks for marketplace development and validation

# Default recipe - show available commands
default:
    @just --list

# Validate marketplace structure and all plugins
validate:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🔍 Validating marketplace and all plugins..."
    echo ""
    echo "Marketplace:"
    if claude plugin validate . 2>/dev/null; then
        echo "  ✓ marketplace.json"
    else
        echo "  ✗ marketplace.json"
    fi
    echo ""
    echo "Plugins:"
    for plugin in plugins/*/; do
        if [ -f "$plugin/.claude-plugin/plugin.json" ]; then
            name=$(basename "$plugin")
            if claude plugin validate "$plugin" 2>/dev/null; then
                echo "  ✓ $name"
            else
                echo "  ✗ $name"
            fi
        fi
    done
    echo ""
    echo "✅ Validation complete!"

# Validate a specific plugin
validate-plugin plugin:
    @echo "🔍 Validating plugin: {{plugin}}..."
    @claude plugin validate "plugins/{{plugin}}"

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

# Run Phase 3 agent optimization tests
test-phase3:
    @echo "🧪 Running Phase 3 agent optimization tests..."
    @pytest tests/functional/test_phase3_agents.py -v --tb=short
    @echo ""
    @echo "📊 Phase 3 Status:"
    @pytest tests/functional/test_phase3_agents.py::TestPhase3Summary::test_phase3_optimization_complete -v --tb=short

# Run Phase 3 tests (quiet mode for quick checks)
test-phase3-quick:
    @echo "🧪 Quick Phase 3 check..."
    @pytest tests/functional/test_phase3_agents.py --tb=no -q

# Run Phase 3 tests for specific plugin
test-phase3-plugin plugin:
    @echo "🧪 Testing Phase 3 for {{plugin}}..."
    @pytest tests/functional/test_phase3_agents.py -k "{{plugin}}" -v --tb=short

# Show current Phase 3 metrics
phase3-metrics:
    @echo "📊 Phase 3 Current Metrics"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo ""
    @echo "Agents:"
    @echo "  Total: $(wc -l plugins/*/agents/*.md | tail -1 | awk '{print $1}') lines (target: 1,206)"
    @echo "  agent-loop/workflow-agent: $(wc -l < plugins/agent-loop/agents/workflow-agent.md) lines (target: 206)"
    @echo "  epti/tdd-agent: $(wc -l < plugins/epti/agents/tdd-agent.md) lines (target: 400)"
    @echo "  visual-iteration/visual-iteration-agent: $(wc -l < plugins/visual-iteration/agents/visual-iteration-agent.md) lines (target: 600)"

# Run all phase tests
test-all-phases:
    @echo "🧪 Running all phase tests..."
    @echo ""
    @echo "Phase 2: Skills & READMEs"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @pytest tests/functional/test_phase2_reductions.py -v --tb=line
    @echo ""
    @echo "Phase 3: Agents"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @pytest tests/functional/test_phase3_agents.py -v --tb=line

# Show all phase metrics
metrics:
    @echo "📊 All Phase Metrics"
    @echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    @echo ""
    @just phase2-metrics
    @echo ""
    @just phase3-metrics

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

# Bump all plugins and reload marketplace
bump:
    #!/usr/bin/env bash
    set -euo pipefail
    for plugin in do do-more do-extra; do
        if [ -f "plugins/$plugin/.claude-plugin/plugin.json" ]; then
            just bump-plugin "$plugin"
        fi
    done
    echo "Updating marketplace..."
    claude plugin marketplace update loom99
    echo "Updating Claude's installed plugins..."
    just reload do do-more do-extra
    echo "Done!"

# Bump a single plugin version (no reload)
bump-plugin plugin:
    #!/usr/bin/env bash
    set -euo pipefail
    PLUGIN="{{plugin}}"
    PLUGIN_JSON="plugins/$PLUGIN/.claude-plugin/plugin.json"
    MARKETPLACE_JSON=".claude-plugin/marketplace.json"
    if [ ! -f "$PLUGIN_JSON" ]; then
        echo "Error: Plugin not found: $PLUGIN"
        exit 1
    fi
    CURRENT=$(grep '"version"' "$PLUGIN_JSON" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
    MAJOR=$(echo "$CURRENT" | cut -d. -f1)
    MINOR=$(echo "$CURRENT" | cut -d. -f2)
    PATCH=$(echo "$CURRENT" | cut -d. -f3)
    NEW_PATCH=$((PATCH + 1))
    NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"
    echo "Bumping $PLUGIN: $CURRENT -> $NEW_VERSION"
    sed -i '' "s/\"version\": \"$CURRENT\"/\"version\": \"$NEW_VERSION\"/" "$PLUGIN_JSON"
    echo "  Updated $PLUGIN_JSON"
    python3 -c "import json; f=open('$MARKETPLACE_JSON'); d=json.load(f); f.close(); [p.update({'version':'$NEW_VERSION'}) for p in d['plugins'] if p['name']=='$PLUGIN']; f=open('$MARKETPLACE_JSON','w'); json.dump(d,f,indent=2); f.write('\n'); f.close()"
    echo "  Updated $MARKETPLACE_JSON"
    echo "Done: $PLUGIN is now v$NEW_VERSION"

# Reload one or more plugins
reload +plugins:
    #!/usr/bin/env bash
    set -euo pipefail
    plugin_list=$(claude plugin list 2>/dev/null)
    for plugin in {{plugins}}; do
        if echo "$plugin_list" | grep -A3 "❯ $plugin@loom99" | grep -q "Status: ✔ enabled"; then
            echo "Clearing cache"
            claude plugin uninstall $plugin@loom99
            rm -rf ~/.claude/plugins/cache/loom99/$plugin
            claude plugin install $plugin@loom99
            echo "Updating $plugin..."
            claude plugin update "$plugin@loom99"
        fi
    done

# Tail hook logs in real-time
hook-tail:
    @echo "Tailing hook logs (Ctrl+C to stop)..."
    @echo "Tip: export DO_PLUGIN_DEBUG=1 to enable logging"
    @mkdir -p /tmp/do_plugin && touch /tmp/do_plugin/hooks.log
    @tail -f /tmp/do_plugin/hooks.log

# Clear hook logs
hook-clear:
    @rm -f /tmp/do_plugin/hooks.log 2>/dev/null || true
    @echo "Hook logs cleared."
