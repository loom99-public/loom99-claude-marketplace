# visual-iteration Plugin Installation Checklist

This checklist guides you through installing and verifying the visual-iteration plugin, which enables pixel-perfect UI implementation through screenshot-driven iterative refinement workflows.

## Prerequisites

Before installing visual-iteration:

- [ ] Marketplace is successfully installed and loaded
- [ ] visual-iteration plugin is visible in marketplace plugin list
- [ ] Claude Code is running without errors
- [ ] You have a test project with UI components to iterate on
- [ ] Browser available for screenshot capture (Chrome, Firefox, Safari)
- [ ] Puppeteer or browser automation tools installed (for automated screenshots)

## Installation Steps

Install the visual-iteration plugin:

1. Open Claude Code and navigate to plugins or marketplace section
2. Locate "visual-iteration" in the available plugins list
3. Click install or enable button for visual-iteration
4. Wait for installation to complete
5. Restart Claude Code if prompted
6. Verify plugin appears in installed plugins list
7. Check that plugin status shows as "active" or "enabled"
8. Verify MCP browser-tools server is configured (if using automated screenshots)

## Component Verification

Verify all plugin components are installed:

- Verify all commands are accessible via autocomplete
- Check agent file exists and is loaded
- Verify all skill files are present in the skills directory
- Check each hook configuration file to verify all hook setups are correct



### Commands Verification (6 Commands)

Verify all 6 visual iteration commands are accessible:

- [ ] `/screenshot` command appears in autocomplete
- [ ] `/implement-design` command appears in autocomplete
- [ ] `/iterate` command appears in autocomplete
- [ ] `/visual-commit` command appears in autocomplete
- [ ] `/compare` command appears in autocomplete
- [ ] `/load-mock` command appears in autocomplete

**Test command autocomplete:**
1. Start a new conversation in Claude Code
2. Type `/` and check for all 6 visual-iteration commands
3. Verify command descriptions mention visual, screenshot, or UI
4. Confirm commands are distinguishable from other plugins

### Agent Verification

Verify the visual-iteration agent is loaded:

- [ ] Agent file exists: `ls plugins/visual-iteration/agents/visual-iteration-agent.md`
- [ ] Agent provides specific visual feedback (pixel values, CSS properties)
- [ ] Agent tracks iteration cycles and convergence

**Test agent visual feedback:**
1. Start a new conversation about UI refinement
2. Describe a visual discrepancy
3. Observe if agent provides specific pixel or CSS measurements
4. Verify agent suggests concrete visual improvements

### Skills Verification (4 Skills)

Verify all 4 visual development skills are loaded:

- [ ] screenshot-capture skill is loaded
- [ ] visual-analysis skill is loaded
- [ ] refinement-guidance skill is loaded
- [ ] iteration-management skill is loaded

**Check skills installation:**
1. List skill files: `ls plugins/visual-iteration/skills/`
2. Verify 4 .md files exist
3. Check each skill file has substantial content (>900 lines)

### Hooks Verification (3 Hooks)

Verify all 3 visual workflow hooks are configured:

- [ ] post-code hook is configured (suggest screenshot verification)
- [ ] pre-commit hook is configured (validate visual polish)
- [ ] post-refine hook is configured (update screenshots)

**Check hooks configuration:**
1. Verify hooks file exists: `cat plugins/visual-iteration/hooks/hooks.json`
2. Confirm JSON is valid: `cat plugins/visual-iteration/hooks/hooks.json | jq`
3. Verify hooks support visual verification workflow

### MCP Server Verification

Verify browser-tools MCP server is configured:

- [ ] MCP config file exists: `cat plugins/visual-iteration/.mcp.json`
- [ ] browser-tools server is defined in MCP config
- [ ] Puppeteer is installed (if using automated screenshots): `npm list puppeteer` or `which puppeteer`

**Test MCP browser-tools:**
1. Check .mcp.json file content
2. Verify browser-tools server configuration is valid
3. Test that browser automation can be invoked (if possible)
4. Confirm fallback to manual screenshots works if automation unavailable

## Functional Testing

### Test 1: Command Execution

Execute each visual command to verify prompt expansion:

1. Type `/screenshot` and verify guidance for capturing UI state (~800+ lines)
2. Type `/implement-design` and verify guidance for implementing from design
3. Type `/iterate` and verify guidance for visual refinement cycle
4. Type `/visual-commit` and verify guidance for committing visual work
5. Type `/compare` and verify guidance for before/after comparison
6. Type `/load-mock` and verify guidance for loading design mockups

**Success Criteria:**
- All 6 commands expand with comprehensive visual guidance
- Guidance includes specific pixel, CSS, and layout advice
- No errors during command execution

### Test 2: Visual Iteration Workflow

Test basic visual iteration workflow:

1. Start conversation for UI refinement task
2. Use `/screenshot` to capture current UI state
3. Use `/iterate` to get specific visual feedback
4. Make refinements based on feedback
5. Use `/screenshot` again to capture refined state
6. Use `/compare` to see before/after differences
7. Use `/visual-commit` to finalize changes

**Success Criteria:**
- Screenshot capture works (manual or automated)
- Agent provides specific feedback (e.g., "24px should be 32px")
- Iteration cycle completes 2-3 times for refinement
- Visual improvements are measurable

### Test 3: MCP Browser Automation (If Available)

Test automated screenshot capture:

1. Start conversation requesting screenshot
2. Verify agent can trigger Puppeteer/browser-tools
3. Check automated screenshot is captured and analyzed
4. Confirm automation falls back to manual if unavailable

**Success Criteria:**
- Browser automation launches successfully
- Screenshots are captured automatically
- Fallback to manual screenshots works if automation fails

## Troubleshooting

### Issue: MCP browser-tools not working

**Solution:**
1. Verify Puppeteer is installed: `npm list puppeteer` or `npm install puppeteer`
2. Check .mcp.json file has correct browser-tools configuration
3. Review Claude Code MCP server logs for connection errors
4. Test browser-tools manually if possible
5. Use manual screenshot workflow as fallback

### Issue: Screenshot analysis provides generic feedback

**Solution:**
1. Verify agent has access to high-quality screenshots
2. Provide specific context about what to analyze
3. Check that visual-analysis skill is loaded correctly
4. Review agent definition for feedback specificity expectations

### Issue: Iteration not converging

**Solution:**
1. Verify feedback is specific (pixel values, CSS properties)
2. Check that refinements are actually being applied
3. Use /compare command to see if changes are visible
4. Limit iterations to 2-3 cycles as recommended

### Issue: Commands overlap with other plugins

**Solution:**
1. Check command names are distinct (visual-iteration uses /screenshot, /visual-commit)
2. Use full command names to disambiguate
3. Verify plugin can coexist with agent-loop and epti
4. Test visual-iteration in dedicated conversation if needed

## Uninstallation Testing

Test plugin removal:

- Disable or uninstall visual-iteration plugin from Claude Code
- Restart Claude Code
- Verify 6 visual commands no longer appear in autocomplete
- Confirm visual agent is no longer active
- Check MCP browser-tools server is unloaded
- Test that plugin can be reinstalled successfully

## Installation Success Criteria

visual-iteration installation is successful when:

- All 6 visual commands are accessible via autocomplete
- Command prompt expansion works with detailed visual guidance
- Agent provides specific pixel-perfect feedback
- All 4 visual skills are loaded and accessible
- All 3 visual workflow hooks are configured correctly
- MCP browser-tools server is configured (automation optional)
- No errors appear in Claude Code logs
- Complete iteration workflow (screenshot→feedback→refine→compare→commit) executes successfully

## Next Steps

After successful installation:

1. Review command scenarios in `commands-visual-iteration.md`
2. Execute individual visual command tests
3. Complete workflow scenarios in `workflows-visual-iteration.md`
4. Observe agent feedback specificity using `agent-visual-iteration.md` checklist
5. Record all test results in TESTING_RESULTS.md

## Test Results Recording

Record your visual-iteration installation test results:

- Test Date: [YYYY-MM-DD]
- Tester Name: [Your Name]
- Plugin: visual-iteration
- Test Type: installation
- Result: [PASS / FAIL / BLOCKED]
- Expected: All 6 commands, visual agent, 4 skills, 3 hooks, MCP browser-tools installed and working
- Actual: [What actually happened]
- Notes: [MCP/screenshot observations]
