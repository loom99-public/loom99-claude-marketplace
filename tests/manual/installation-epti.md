# epti Plugin Installation Checklist

This checklist guides you through installing and verifying the epti plugin, which enforces test-driven development discipline through a 6-stage workflow: Write Tests → Verify Fail → Commit Tests → Implement → Iterate → Commit Code.

## Prerequisites

Before installing epti:

- [ ] Marketplace is successfully installed and loaded
- [ ] epti plugin is visible in marketplace plugin list
- [ ] Claude Code is running without errors
- [ ] You have a test project directory ready with testing tools (pytest, jest, etc.)

## Installation Steps

Install the epti plugin:

1. Open Claude Code and navigate to plugins or marketplace section
2. Locate "epti" in the available plugins list
3. Click install or enable button for epti
4. Wait for installation to complete
5. Restart Claude Code if prompted
6. Verify plugin appears in installed plugins list
7. Check that plugin status shows as "active" or "enabled"

## Component Verification

Verify all plugin components are installed:

- Verify all commands are accessible via autocomplete
- Check agent file exists and is loaded
- Verify all skill files are present in the skills directory
- Check each hook configuration file to verify all hook setups are correct



### Commands Verification (6 Commands)

Verify all 6 TDD workflow commands are accessible:

- [ ] `/write-tests` command appears in autocomplete
- [ ] `/verify-fail` command appears in autocomplete
- [ ] `/commit-tests` command appears in autocomplete
- [ ] `/implement` command appears in autocomplete
- [ ] `/iterate` command appears in autocomplete
- [ ] `/commit-code` command appears in autocomplete

**Test command autocomplete:**
1. Start a new conversation in Claude Code
2. Type `/` and check for all 6 epti commands
3. Verify command descriptions mention TDD or testing
4. Confirm commands are distinguishable from other plugins

### Agent Verification

Verify the TDD agent is loaded:

- [ ] Agent file exists: `ls plugins/epti/agents/tdd-agent.md`
- [ ] Agent enforces test-first discipline during conversations
- [ ] Agent detects and blocks anti-patterns (coding without tests)

**Test agent TDD enforcement:**
1. Start a new conversation
2. Try to implement code without writing tests first
3. Observe if agent blocks or warns about skipping test writing
4. Verify agent guides towards test-first approach

### Skills Verification (5 Skills)

Verify all 5 TDD support skills are loaded:

- [ ] test-generation skill is loaded
- [ ] test-execution skill is loaded
- [ ] implementation-with-protection skill is loaded
- [ ] overfitting-detection skill is loaded
- [ ] refactoring skill is loaded

**Check skills installation:**
1. List skill files: `ls plugins/epti/skills/`
2. Verify 5 .md files exist
3. Check each skill file has substantive content (>400 lines)

### Hooks Verification (3 Hooks)

Verify all 3 TDD discipline hooks are configured:

- [ ] pre-implementation hook is configured (verify tests defined)
- [ ] post-code hook is configured (run test suite)
- [ ] pre-commit hook is configured (gate on all tests passing)

**Check hooks configuration:**
1. Verify hooks file exists: `cat plugins/epti/hooks/hooks.json`
2. Confirm JSON is valid: `cat plugins/epti/hooks/hooks.json | jq`
3. Verify hooks enforce TDD discipline (test-first, tests must pass)

## Functional Testing

### Test 1: Command Execution

Execute each TDD command to verify prompt expansion:

1. Type `/write-tests` and verify guidance for test writing (should be ~400+ lines)
2. Type `/verify-fail` and verify guidance for confirming tests fail properly
3. Type `/commit-tests` and verify guidance for committing tests separately
4. Type `/implement` and verify guidance for implementation with test validation
5. Type `/iterate` and verify guidance for refinement and improvement
6. Type `/commit-code` and verify guidance for final code commit

**Success Criteria:**
- All 6 commands expand with comprehensive TDD guidance
- Guidance emphasizes test-first discipline
- No errors during command execution

### Test 2: TDD Workflow Sequence

Test complete TDD workflow:

1. Start conversation for a new feature
2. Use `/write-tests` to create tests before implementation
3. Use `/verify-fail` to confirm tests fail without code
4. Use `/commit-tests` to commit tests separately
5. Use `/implement` to create code that makes tests pass
6. Use `/iterate` if refinement needed
7. Use `/commit-code` to finalize implementation

**Success Criteria:**
- Workflow enforces test-first order
- Agent blocks attempts to skip test writing
- Tests must fail before implementation begins
- Tests must pass before final commit

## Troubleshooting

### Issue: TDD discipline not enforced

**Solution:**
1. Verify tdd-agent.md file has content about anti-patterns
2. Check agent is active (agent list in Claude Code)
3. Start fresh conversation to reset agent context
4. Review agent definition for expected behavior

### Issue: Commands overlap with agent-loop

**Solution:**
1. Check command names are distinct (epti uses /write-tests, /implement vs agent-loop's /code)
2. Verify both plugins can coexist
3. Use full command names to disambiguate
4. Test each plugin in separate conversations if needed

### Issue: Test execution integration not working

**Solution:**
1. Verify testing tools installed (pytest, jest, etc.)
2. Check post-code hook can execute test commands
3. Review hook configuration for test execution
4. Test hooks manually if possible

## Uninstallation Testing

Test plugin removal:

- Disable or uninstall epti plugin from Claude Code
- Restart Claude Code
- Verify 6 TDD commands no longer appear in autocomplete
- Confirm TDD agent is no longer enforcing discipline
- Test that plugin can be reinstalled successfully

## Installation Success Criteria

epti installation is successful when:

- All 6 TDD commands are accessible via autocomplete
- Command prompt expansion works with comprehensive TDD guidance
- Agent enforces test-first discipline and blocks anti-patterns
- All 5 TDD skills are loaded and accessible
- All 3 discipline hooks are configured correctly
- No errors appear in Claude Code logs
- Complete TDD workflow (write-tests→verify-fail→commit-tests→implement→commit-code) executes properly

## Next Steps

After successful installation:

1. Review command scenarios in `commands-epti.md`
2. Execute individual TDD command tests
3. Complete workflow scenarios in `workflows-epti.md`
4. Observe agent TDD enforcement using `agent-epti.md` checklist
5. Record all test results in TESTING_RESULTS.md

## Test Results Recording

Record your epti installation test results:

- Test Date: [YYYY-MM-DD]
- Tester Name: [Your Name]
- Plugin: epti
- Test Type: installation
- Result: [PASS / FAIL / BLOCKED]
- Expected: All 6 commands, TDD agent, 5 skills, 3 hooks installed and enforcing TDD discipline
- Actual: [What actually happened]
- Notes: [TDD enforcement observations]
