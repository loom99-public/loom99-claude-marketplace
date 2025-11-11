# Marketplace Installation Checklist

This checklist guides you through installing the Claude Plugin Marketplace and verifying that all three plugins are discoverable and ready for individual installation.

## Pre-Installation Checklist

Before installing the marketplace:

- Verify Claude Code is installed and working on your system
- Check Claude Code version is compatible (v1.0.0 or later recommended)
- Confirm you have read access to this repository
- Identify your Claude Code plugins directory location (~/.claude/plugins/)
- Backup any existing plugin configurations if present

## Installation Steps

Follow these steps to install the marketplace:

1. Clone or download this repository to your local machine
2. Navigate to the repository root directory in your terminal
3. Verify the marketplace manifest exists: `ls -la .claude-plugin/marketplace.json`
4. Check marketplace manifest is valid JSON: `cat .claude-plugin/marketplace.json | jq`
5. Open Claude Code application or CLI
6. Navigate to Claude Code settings or plugins configuration
7. Add this repository as a marketplace source (specify repository path)
8. Restart Claude Code to load the marketplace
9. Verify marketplace appears in Claude Code plugins list
10. Confirm all three plugins are visible in marketplace: agent-loop, epti, visual-iteration

## Verification Checklist

After installation, verify the following:

- [ ] Marketplace loads without errors in Claude Code
- [ ] Marketplace manifest displays correctly (name, version, description)
- [ ] All 3 plugins are visible in the marketplace plugin list
- [ ] Plugin metadata is correct for each plugin (names, versions, descriptions)
- [ ] No error messages appear in Claude Code logs related to marketplace loading
- [ ] Marketplace does not conflict with any existing plugins or configurations

### Plugin Visibility Verification

For each plugin, verify it appears in the marketplace with correct information:

**agent-loop**:
- [ ] Plugin name: "agent-loop"
- [ ] Version: "0.1.0"
- [ ] Description: "Agentic Software Engineering Loop - Explore, plan, code, commit workflow"
- [ ] Author: Brandon Fryslie

**epti**:
- [ ] Plugin name: "epti"
- [ ] Version: "0.1.0"
- [ ] Description: "Evaluate-Plan-Test-Implement - Test-driven development workflow"
- [ ] Author: Brandon Fryslie

**visual-iteration**:
- [ ] Plugin name: "visual-iteration"
- [ ] Version: "0.1.0"
- [ ] Description: "Visual iteration workflow - Screenshot-driven UI development and refinement"
- [ ] Author: Brandon Fryslie

## Troubleshooting

### Issue: Marketplace not found in Claude Code

**Solution:**
1. Verify marketplace.json file exists in .claude-plugin/ directory
2. Check file permissions are readable: `ls -l .claude-plugin/marketplace.json`
3. Validate JSON syntax: `cat .claude-plugin/marketplace.json | jq '.'`
4. Confirm repository path is correctly specified in Claude Code settings
5. Restart Claude Code after configuring marketplace path
6. Check Claude Code startup logs for marketplace loading errors

### Issue: Plugins not visible in marketplace

**Solution:**
1. Verify each plugin has .claude-plugin/plugin.json file
2. Check plugin directories exist: `ls -la plugins/`
3. Validate each plugin.json file: `cat plugins/*/. claude-plugin/plugin.json | jq '.'`
4. Ensure marketplace.json references all three plugins correctly
5. Reload marketplace or restart Claude Code
6. Check for path resolution issues in marketplace manifest

### Issue: Marketplace conflicts with existing plugins

**Solution:**
1. Review existing plugin names for conflicts
2. Check if any existing plugins use same command names
3. Temporarily disable conflicting plugins
4. Install marketplace in clean Claude Code profile for testing
5. Review Claude Code logs for specific conflict details

## Uninstallation Testing

To test marketplace removal:

- Navigate to Claude Code plugins settings
- Remove the marketplace source from configuration
- Restart Claude Code
- Verify marketplace no longer appears in plugins list
- Confirm all three plugins are no longer accessible
- Check that no marketplace configuration remains in Claude Code settings
- Verify no leftover files in Claude Code plugins directory
- Test that marketplace can be cleanly reinstalled after removal

## Installation Success Criteria

Installation is successful when:

- Marketplace loads without any errors or warnings
- All 3 plugins appear in marketplace with correct metadata
- Plugin installation buttons/options are functional for each plugin
- No conflicts with existing Claude Code configuration
- Marketplace can be cleanly uninstalled and reinstalled

## Next Steps

After successful marketplace installation:

1. Review individual plugin installation checklists
2. Select first plugin to install (recommend agent-loop for simplicity)
3. Follow plugin-specific installation checklist
4. Proceed with command and workflow testing for installed plugin

## Test Results Recording

Record your marketplace installation test results in TESTING_RESULTS.md:

- Test Date: [YYYY-MM-DD]
- Tester Name: [Your Name]
- Plugin: marketplace
- Test Type: installation
- Result: [PASS / FAIL / BLOCKED]
- Expected: Marketplace loads with all 3 plugins visible
- Actual: [What actually happened]
- Notes: [Any observations, issues, or comments]
