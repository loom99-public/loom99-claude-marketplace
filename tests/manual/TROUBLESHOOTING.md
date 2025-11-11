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

