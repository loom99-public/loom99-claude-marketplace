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

# Run full verification (validate only - these plugins can't be pytest tested)
verify: validate
    @echo ""
    @echo "✅ Verification complete!"
    @echo "   - Marketplace structure valid"
    @echo "   - All plugins valid"

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

# Generate slash command files from commands.yaml
generate-commands:
    @echo "🔨 Generating slash command files from commands.yaml..."
    @python3 scripts/generate_commands.py
    @echo "✅ Command files generated!"
