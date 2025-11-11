# agent-loop Plugin Installation Checklist

This checklist guides you through installing and verifying the agent-loop plugin, which provides a 4-stage agentic software engineering workflow: Explore → Plan → Code → Commit.

## Prerequisites

Before installing agent-loop:

- [ ] Marketplace is successfully installed and loaded
- [ ] agent-loop plugin is visible in marketplace plugin list
- [ ] Claude Code is running without errors
- [ ] You have a test project directory ready for workflow testing

## Installation Steps

Install the agent-loop plugin:

1. Open Claude Code and navigate to plugins or marketplace section
2. Locate "agent-loop" in the available plugins list
3. Click install or enable button for agent-loop
4. Wait for installation to complete (should take a few seconds)
5. Restart Claude Code if prompted to complete installation
6. Verify plugin appears in installed plugins list
7. Check that plugin status shows as "active" or "enabled"

## Component Verification

Verify all plugin components are installed:

- Verify all commands are accessible via autocomplete
- Check agent file exists and is loaded
- Verify all skill files are present in the skills directory
- Check each hook configuration file to verify all hook setups are correct



Verify all agent-loop components are correctly installed and accessible:

### Commands Verification

The agent-loop plugin provides 4 slash commands. Verify each command is accessible:

- [ ] `/explore` command appears in autocomplete
- [ ] `/plan` command appears in autocomplete
- [ ] `/code` command appears in autocomplete
- [ ] `/commit` command appears in autocomplete

**Test command autocomplete:**
1. Start a new conversation in Claude Code
2. Type `/` and wait for autocomplete suggestions
3. Verify all 4 agent-loop commands appear in the list
4. Confirm command descriptions are visible and correct

### Agent Verification

Verify the workflow-agent is loaded:

- [ ] Agent file exists: `ls plugins/agent-loop/agents/workflow-agent.md`
- [ ] Agent is registered in Claude Code (check agent list if available)
- [ ] Agent guidance is accessible during conversations

**Test agent accessibility:**
1. Start a new conversation
2. Mention workflow stages (explore, plan, code, commit)
3. Observe if agent provides stage-appropriate guidance
4. Verify agent responses align with workflow methodology

### Skills Verification

Verify all 4 skills are loaded:

- [ ] code-exploration skill is loaded
- [ ] plan-generation skill is loaded
- [ ] verification skill is loaded
- [ ] git-operations skill is loaded

**Check skills installation:**
1. List skill files: `ls plugins/agent-loop/skills/`
2. Verify 4 .md files exist (code-exploration.md, plan-generation.md, verification.md, git-operations.md)
3. Check Claude Code recognizes skills (if skill list is available in UI)

### Hooks Verification

Verify all 3 hooks are configured:

- [ ] pre-commit hook is configured
- [ ] post-code hook is configured
- [ ] commit-msg hook is configured

**Check hooks configuration:**
1. Verify hooks file exists: `cat plugins/agent-loop/hooks/hooks.json`
2. Confirm JSON is valid: `cat plugins/agent-loop/hooks/hooks.json | jq`
3. Verify all 3 hooks are defined in the file
4. Check hook events are properly specified

## Functional Testing

Perform basic functional tests to ensure plugin works:

### Test 1: Command Execution

Execute each command to verify prompt expansion:

1. Type `/explore` and press Enter
2. Verify prompt expands with exploration guidance (should be ~50-70 lines)
3. Type `/plan` and press Enter
4. Verify prompt expands with planning guidance
5. Type `/code` and press Enter
6. Verify prompt expands with implementation guidance
7. Type `/commit` and press Enter
8. Verify prompt expands with commit guidance

**Success Criteria:**
- All 4 commands expand correctly with non-empty guidance
- Guidance content is relevant to the command name
- No error messages appear during command execution

### Test 2: Workflow Sequence

Test basic workflow sequence:

1. Start a new conversation for a simple task
2. Use `/explore` to investigate codebase
3. Use `/plan` to create implementation plan
4. Use `/code` to implement changes
5. Use `/commit` to finalize with git commit

**Success Criteria:**
- Commands execute in sequence without errors
- Agent provides appropriate guidance at each stage
- Workflow transitions feel natural and clear

## Troubleshooting

### Issue: Commands not appearing in autocomplete

**Solution:**
1. Verify plugin is enabled: Check installed plugins list
2. Restart Claude Code to refresh command registry
3. Check command files exist: `ls plugins/agent-loop/commands/`
4. Verify files are .md format: `ls plugins/agent-loop/commands/*.md`
5. Review Claude Code logs for command loading errors

### Issue: Command prompt expansion is empty

**Solution:**
1. Check command file has content: `cat plugins/agent-loop/commands/explore.md`
2. Verify file encoding is UTF-8
3. Check for markdown syntax errors in command files
4. Try reloading the plugin
5. Test with other plugin commands to isolate issue

### Issue: Agent guidance not working

**Solution:**
1. Verify agent file exists and has content: `cat plugins/agent-loop/agents/workflow-agent.md`
2. Check plugin.json references agent correctly
3. Restart conversation with fresh context
4. Review agent behavior expectations in plugin documentation

### Issue: Hooks not executing

**Solution:**
1. Verify hooks.json file is valid JSON
2. Check hook commands are executable on your system
3. Review Claude Code hook execution logs
4. Test hooks manually if possible
5. Verify hook events are correctly specified

## Uninstallation Testing

Test plugin removal:

- Navigate to installed plugins in Claude Code
- Disable or uninstall agent-loop plugin
- Restart Claude Code
- Verify commands no longer appear in autocomplete
- Confirm agent is no longer active
- Check that plugin files remain in plugins directory (if applicable)
- Test that plugin can be reinstalled successfully

## Installation Success Criteria

agent-loop installation is successful when:

- All 4 commands are accessible via autocomplete
- Command prompt expansion works for all commands
- Agent provides workflow guidance during conversations
- All 4 skills are loaded and accessible
- All 3 hooks are configured correctly
- No errors appear in Claude Code logs
- Basic workflow sequence (explore→plan→code→commit) executes without issues

## Next Steps

After successful installation:

1. Review command scenarios in `commands-agent-loop.md`
2. Execute individual command tests
3. Complete workflow scenarios in `workflows-agent-loop.md`
4. Observe agent behavior using `agent-agent-loop.md` checklist
5. Record all test results in TESTING_RESULTS.md

## Test Results Recording

Record your agent-loop installation test results:

- Test Date: [YYYY-MM-DD]
- Tester Name: [Your Name]
- Plugin: agent-loop
- Test Type: installation
- Result: [PASS / FAIL / BLOCKED]
- Expected: All 4 commands, agent, 4 skills, 3 hooks installed and working
- Actual: [What actually happened]
- Notes: [Component-specific observations]
