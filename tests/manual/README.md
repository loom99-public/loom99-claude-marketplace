# Manual Testing Guide for Claude Plugin Marketplace

This directory contains comprehensive manual testing documentation for the Claude Plugin Marketplace and its three plugins: agent-loop, epti, and visual-iteration.

## Overview

The Claude Plugin Marketplace contains three advanced plugins that extend Claude Code with specialized agents, commands, hooks, and skills. These plugins enable sophisticated software development workflows including agentic engineering loops, test-driven development discipline, and visual iteration cycles. Manual testing is essential because automated tests cannot fully validate the interactive, conversational nature of agent behaviors, the subjective quality of command prompt expansions, or the effectiveness of multi-stage workflows. Human testers must verify that commands produce helpful guidance, agents provide clear direction, workflows transition smoothly between stages, and the overall user experience meets quality standards for production deployment.

The manual testing framework documented here provides systematic guidance for human testers to validate all plugin functionality in real Claude Code environments. The framework covers five test dimensions: installation verification, command execution testing, complete workflow scenarios, agent behavior observation, and results recording. Each dimension includes detailed checklists, test scenarios, expected outcomes, and troubleshooting guidance to ensure comprehensive coverage of all plugin features.

## Quick Start

Begin manual testing by following these actionable steps:

- Install Claude Code (latest version) on your system if not already installed
- Clone this repository to your local machine using git clone command
- Navigate to your Claude Code plugins directory (typically ~/.claude/plugins/)
- Load the Claude Plugin Marketplace by following installation-marketplace.md checklist
- Select one plugin to test first (recommend starting with agent-loop for simplicity)
- Read the installation checklist for your chosen plugin in installation-<plugin>.md file
- Install the selected plugin following the checklist steps provided
- Verify all plugin components are visible (commands, agent, skills, hooks in Claude Code)
- Open the command scenarios file for your plugin (commands-<plugin>.md)
- Execute each command scenario and record results in TESTING_RESULTS.md template
- Review the workflow scenarios file for your plugin (workflows-<plugin>.md)
- Complete at least 2-3 end-to-end workflow scenarios to verify functionality
- Use the agent observation checklist (agent-<plugin>.md) to evaluate agent behavior quality
- Report any issues discovered using ISSUE_TEMPLATE.md with proper severity levels
- Repeat the process for the remaining two plugins to achieve comprehensive coverage

## Testing Framework Structure

Execute manual testing using these five complementary test dimensions:

- Verify installation by checking all plugins load correctly and components register in Claude Code
- Test commands individually to validate slash command execution and prompt expansion quality
- Execute complete workflows using multiple commands in sequence to simulate real user journeys
- Observe agent behavior during interactive sessions to assess guidance quality and anti-pattern detection
- Record all test results systematically using structured templates for analysis and production readiness decisions

### Installation Testing

Verify that plugins install correctly and all components are accessible. This includes marketplace-level installation (installation-marketplace.md) which tests that the marketplace itself loads and makes plugins discoverable. It also includes plugin-specific installation testing (installation-<plugin>.md for each of agent-loop, epti, and visual-iteration) which verifies that individual plugins install cleanly, all commands appear in autocomplete, agents are registered, skills are loaded, hooks are configured, and MCP servers initialize correctly.

### Command Execution Testing

Validate that slash commands work correctly and expand to expected prompts. Command scenarios (commands-<plugin>.md) provide test cases for all 16 commands across the three plugins. Tests verify command autocomplete functions properly, prompt expansion produces comprehensive guidance matching command definition files, parameter handling works correctly for parameterized commands, and error handling provides helpful messages for invalid inputs or usage.

### Complete Workflow Testing

Execute realistic end-to-end scenarios using multiple commands in sequence. Workflow scenarios (workflows-<plugin>.md) include 3-5 complete workflows per plugin, testing typical user journeys from initial setup through final deliverable production. Tests verify stage transitions occur smoothly, deliverables match expectations (plans, code implementations, git commits, screenshots), time estimates are accurate, and workflows can be completed without confusion or blockage.

### Agent Behavior Testing

Observe and evaluate agent guidance during interactive sessions. Agent checklists (agent-<plugin>.md) provide qualitative assessment criteria for each plugin's agent. Tests verify anti-pattern detection works and blocks inappropriate actions, workflow stage guidance is clear and actionable, stage transitions are communicated effectively, and agent responses align with plugin documentation and intended behavior.

### Results Recording

Document test outcomes for tracking and analysis. The testing results template (TESTING_RESULTS.md) provides structured table format for recording all test executions with dates, testers, results, and observations. The issue template (ISSUE_TEMPLATE.md) standardizes bug reporting with severity levels, reproduction steps, and impact assessment.

## Setup Instructions

Before beginning manual testing, ensure you have all required software and a clean testing environment. You need Claude Code installed (latest version of CLI or desktop application), a working directory for test projects (recommend creating a dedicated test repository separate from production code), Git installed and configured for commit and workflow testing (username, email, SSH keys if needed), and language-specific testing tools if you plan to test with real code execution (pytest for Python workflows, jest for JavaScript, go test for Go, etc.). Setting up prerequisites properly before testing begins will prevent environment issues from interfering with plugin validation.

Follow these steps to create a clean testing environment:

- Navigate to your Claude Code plugins directory (typically ~/.claude/plugins/ on macOS/Linux, or %APPDATA%/.claude/plugins/ on Windows)
- Clear any existing marketplace configurations to ensure you start from a known clean state
- Create a dedicated test project directory using mkdir ~/test-claude-plugins && cd ~/test-claude-plugins command
- Initialize git in the test directory with git init to enable commit workflow testing functionality
- Create sample files for testing workflows using touch README.md src/main.py tests/test_main.py or equivalent commands for your preferred language
- Verify git is configured properly by running git config --list to check username and email settings
- Install any required testing tools like pytest for Python or jest for JavaScript if workflows will execute real code
- Open Claude Code and verify it detects your plugins directory correctly before proceeding

This clean environment setup ensures test results reflect actual plugin behavior rather than environmental factors or configuration conflicts.

## Test Execution Workflow

For comprehensive coverage while building familiarity with plugin patterns, test in this specific order. Start with agent-loop which is the simplest plugin with 4 commands implementing a straightforward explore-plan-code-commit workflow. Progress to epti which has intermediate complexity with 6 commands and enforces strict test-driven development discipline. Complete with visual-iteration which is the most complex plugin with 6 commands requiring browser automation integration and screenshot analysis. This progression allows you to learn plugin testing patterns incrementally before encountering the most complex scenarios.

For each plugin, follow this systematic test iteration cycle:

- Complete the installation phase by working through the installation checklist and verifying all components are visible in Claude Code interface
- Enter the command phase where you test each command individually using command scenarios with various inputs and edge cases
- Execute the workflow phase by completing end-to-end workflow scenarios using multiple commands in proper sequence to simulate real usage
- Perform the agent phase where you observe agent behavior during guided sessions using agent checklists to assess guidance quality
- Complete the recording phase by documenting all results in TESTING_RESULTS.md with detailed observations and timing information
- File issues for any unexpected behavior using ISSUE_TEMPLATE.md with appropriate severity levels and reproduction steps

Estimated testing time per plugin breaks down as follows. Installation testing requires 10 to 15 minutes per plugin to verify loading and component visibility. Command testing requires 30 to 45 minutes per plugin (approximately 5 to 10 minutes per command) to execute all command scenarios. Workflow testing requires 60 to 90 minutes per plugin (approximately 15 to 20 minutes per workflow) to complete 3-5 end-to-end scenarios. Agent testing requires 20 to 30 minutes per plugin for qualitative observation and checklist completion. Total testing time per plugin is 2 to 3 hours. Testing all three plugins comprehensively requires 6 to 9 hours total. Plan to conduct testing over multiple sessions to avoid fatigue and maintain attention to detail throughout the validation process.

## Success Criteria

Installation success is achieved when 100% of plugins (all 3 plugins) install without errors or warnings, all 16 commands agents skills and hooks are visible in Claude Code interface, plugin metadata including name version description and author is correctly displayed, and no configuration conflicts occur with existing plugins or Claude Code settings.

Command execution success requires 100% of the 16 commands execute without errors for valid inputs, command autocomplete works correctly with tab completion showing all available commands, prompt expansion produces expected guidance content matching command definition markdown files, and error handling provides helpful clear messages for invalid inputs or incorrect usage patterns.

Workflow success is measured by 95% or higher of complete workflows completing successfully from start to finish, stage transitions occurring smoothly without user confusion or blockage, deliverables being produced as expected including plans code implementations git commits and screenshots, and workflow time estimates being accurate within 25% variance from documented estimates.

Agent behavior success requires agents providing clear actionable guidance at each workflow stage with specific next steps, anti-patterns being detected and blocked with helpful explanations of why actions are inappropriate, stage transitions being clearly communicated so users understand when to move forward, and agent responses being consistent with plugin documentation and intended workflow design. Success means at least 3 test scenarios pass for agent guidance quality, at least 2 test scenarios pass for anti-pattern detection, and at least 2 test scenarios pass for stage transition clarity.

Overall production readiness is achieved when all critical issues are resolved with zero critical or high severity bugs that block core workflows, medium and low severity issues are documented for future fixes but do not prevent production deployment, at least 2 complete end-to-end workflows are tested per plugin with 100% success rate, and agent behavior is rated good or excellent for clarity and effectiveness based on qualitative assessment. These criteria represent the minimum bar for declaring plugins ready for production use.

## Recording and Reporting

Record every test execution using the structured table format provided in TESTING_RESULTS.md. Each test row must include date in ISO format (YYYY-MM-DD) for tracking when testing occurred, tester name for accountability, plugin name identifying which plugin was tested (agent-loop epti visual-iteration or marketplace), test type categorizing as installation command workflow or agent test, test name providing specific identifier like "command /explore" or "workflow simple-feature-add", result status using PASS FAIL BLOCKED or SKIP, expected outcome briefly describing what should happen, actual outcome describing what did happen (especially critical for failures), and notes section for additional context observations or issue references. Complete documentation enables trend analysis and production readiness assessment.

When you encounter unexpected behavior during testing, immediately create a detailed bug report using these steps:

- Use ISSUE_TEMPLATE.md as the structure for all issue reports to maintain consistency across testing sessions
- Include all template sections without omitting information to ensure complete problem documentation
- Write description section with summary and detailed explanation of what went wrong and why it matters
- Document steps to reproduce with precise sequence allowing others to recreate the issue independently
- Specify expected behavior referencing documentation or test specifications that define correct behavior
- Describe actual behavior with specific details about what went wrong including error messages or unexpected outputs
- Assign severity level with justification based on impact considering user effect frequency and workaround availability
- Provide environment information including Claude Code version operating system and plugin versions for debugging context
- Attach screenshots or terminal output if available to provide visual evidence of the problem
- Reference the specific test scenario that revealed the issue for traceability back to testing documentation

Critical severity applies when the issue blocks core functionality and prevents plugin use entirely, such as plugin failing to install, commands crashing Claude Code, or data loss occurring. High severity applies when major features are broken causing significant workflow disruption, such as agent providing incorrect guidance leading to wrong implementation or workflows being unable to complete. Medium severity applies when features work but have problems and workarounds are available, such as commands working but error messages being unclear or agent guidance being confusing but technically correct. Low severity applies to minor cosmetic issues or nice-to-have improvements, such as typos in documentation or inconsistent formatting. Severity assignment should consider impact on users, availability of workarounds, and frequency of occurrence.

## Troubleshooting


### Error: Marketplace not found


- Verify the marketplace.json file exists in .claude-plugin/ directory at the repository root by running ls -la .claude-plugin/marketplace.json
- Check JSON syntax is valid by running cat .claude-plugin/marketplace.json | jq which will report any syntax errors or formatting problems
- Ensure marketplace path is correctly configured in Claude Code settings pointing to the repository by checking settings configuration
- Restart Claude Code after adding marketplace to force reload of plugin configurations and registry
- Check file permissions are readable by running ls -l .claude-plugin/marketplace.json to verify proper access rights
- Review Claude Code startup logs for any error messages related to marketplace loading that might indicate root cause
- Try loading marketplace in a different Claude Code instance or clean user profile to isolate configuration issues

### Error: Plugin failed to load


- Check plugin.json file exists in the plugin's .claude-plugin/ directory (for example plugins/agent-loop/.claude-plugin/plugin.json) by verifying file presence
- Validate JSON syntax by running cat plugins/<plugin>/.claude-plugin/plugin.json | jq to detect any formatting errors or invalid JSON structure
- Verify all referenced paths in plugin.json actually exist including commands directory agents files skills directory and hooks configuration file
- Check file permissions to ensure all files are readable by the user running Claude Code using ls -la commands
- Review Claude Code error logs for specific failure details that indicate root cause like missing files or invalid configurations
- Test with a minimal plugin configuration to isolate whether issue is with plugin structure or content
- Compare working plugin configuration with broken one to identify structural differences causing loading failure

### Error: Commands not showing in autocomplete


- Verify commands directory exists by running ls plugins/<plugin>/commands/ to see all command markdown files present
- Check that command files use markdown .md format extension and are not text files or other formats
- Confirm plugin is fully loaded by checking plugin list in Claude Code settings or interface to verify registration
- Try reloading the plugin configuration or restarting Claude Code completely to refresh the command registry and clear any cached state
- Test with simple /help command to verify command system in Claude Code works at all before debugging plugin-specific issues
- Examine command file names for special characters or spaces that might interfere with command registration
- Verify file encoding is UTF-8 by checking with file command or text editor to ensure proper reading

### Error: Command not recognized


- Verify plugin is installed and loaded by checking plugin list in Claude Code interface or settings panel
- Check command file exists in plugin's commands directory using ls plugins/<plugin>/commands/<command>.md to confirm file presence
- Ensure command name matches filename exactly without .md extension since command names are derived directly from filenames
- Try tab completion to see which commands are actually available and registered in the current session
- Restart Claude Code to refresh command registry in case of stale state or registration failures
- Check for typos in command name or incorrect plugin selection if multiple plugins are loaded

### Error: Prompt expansion is empty or incorrect


- Open the command markdown file directly and verify it contains actual content using cat plugins/<plugin>/commands/<command>.md to see full text
- Check for markdown syntax errors in the command file that might prevent proper parsing of content
- Ensure frontmatter (if present at top of file) uses valid YAML format without syntax errors
- Verify file encoding is UTF-8 not UTF-16 or other encoding that might cause reading issues
- Test with a known-working command from a different plugin to isolate whether issue is plugin-specific or system-wide problem
- Review Claude Code logs for parsing errors that might indicate markdown processing failures

### Error: Agent provides confusing or contradictory guidance


- Review the agent markdown file directly to understand intended behavior patterns using cat plugins/<plugin>/agents/*.md to see full definition
- Check if you are at the correct workflow stage since agent guidance is stage-specific and context-dependent
- Verify prerequisite steps were completed including any required file creation or setup tasks
- Try restarting the conversation with fresh context to eliminate state confusion from previous interactions
- Document specific confusion points in detail for agent improvement including exact agent responses that were unclear or contradictory
- Compare agent guidance with workflow documentation to identify mismatches between intended and actual behavior

### Error: Workflow stuck - unclear how to proceed


- Review workflow scenario documentation to find the documented next steps for your current stage in the process
- Check agent observation checklist for expected stage transitions and trigger conditions that should move workflow forward
- Try using explicit stage commands (for example /plan to explicitly move to planning stage) rather than waiting for automatic transitions
- Examine any error messages or warnings from previous steps that might indicate blocked state or missing prerequisites
- Consider starting workflow from beginning with clear setup to ensure all prerequisites are properly met before proceeding

### Error: Test results differ from documented expectations


- Verify you are using the latest version of all plugins by checking version numbers in plugin.json files
- Check test environment setup matches prerequisites documented in Setup Instructions section including correct Claude Code version git configuration and required testing tools
- Confirm git is properly configured for commit testing by running git config --list to see username and email settings
- Review any local customizations in Claude Code settings or shell environment that might affect plugin behavior or test outcomes
- Test in a completely clean environment using a new test directory and fresh Claude Code installation to isolate local configuration issues from actual plugin issues

## Additional Resources

Each plugin includes comprehensive documentation explaining its purpose, commands, workflows, and usage patterns. Plugin README files are located at plugins/<plugin>/README.md and provide overview and getting started information. Agent definitions describing agent behavior are in plugins/<plugin>/agents/ directory. Command definitions showing full prompt content are in plugins/<plugin>/commands/ directory. Skill definitions documenting reusable capabilities are in plugins/<plugin>/skills/ directory. Reviewing plugin documentation helps understand expected behavior during testing and provides context for evaluation.

Official Claude Code plugin documentation provides architectural context at claude.com/code/plugins for understanding the plugin system design and capabilities. Plugin API reference documentation explains plugin manifest format, command structure, agent definitions, and hook systems in detail. MCP (Model Context Protocol) documentation at modelcontextprotocol.io covers server integrations for capabilities like browser automation and external tool access. Understanding Claude Code's plugin architecture helps diagnose issues and verify correct plugin behavior against system specifications.

Review existing test results in TESTING_RESULTS.md to see if others encountered similar issues during their testing sessions. Check filed issue reports for known bugs and documented workarounds that may apply to problems you are experiencing. Consult plugin-specific troubleshooting sections in workflow scenario files for common problems and solutions specific to each plugin. Reach out to plugin authors or the testing team lead if you encounter issues that cannot be resolved using available documentation or known workarounds.

## Contributing Test Results

After completing your manual testing sessions, you must submit comprehensive results to enable production readiness assessment. Contributing thorough documentation of test outcomes, discovered issues, and qualitative observations ensures the development team can make informed decisions about plugin deployment and identify areas requiring improvement.

- Submit your completed TESTING_RESULTS.md file including all test executions with results, observations, and timing data for comprehensive analysis
- Submit all issue reports filed during testing using ISSUE_TEMPLATE.md format to maintain consistent and actionable bug documentation
- Provide qualitative feedback sharing detailed observations about agent effectiveness, workflow clarity, documentation quality, and overall user experience
- Suggest improvements recommending specific enhancements to testing process, additional test scenarios, improved checklists, or documentation updates based on your hands-on testing experience

Your thorough testing is essential for ensuring production readiness and plugin quality validation. Thank you for contributing to comprehensive plugin testing!