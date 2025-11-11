# Issue Report Template

Use this template to report bugs, unexpected behavior, or issues discovered during manual testing of the Claude Plugin Marketplace.

---

## Issue Information

**Issue ID**: [Unique identifier, e.g., ISSUE-001]
**Date Reported**: [YYYY-MM-DD]
**Reported By**: [Your Name]
**Plugin**: [marketplace / agent-loop / epti / visual-iteration]
**Component**: [installation / command / workflow / agent / skill / hook / other]

## Description

**Summary**: [One-sentence description of the issue]

**Detailed Description**:
[Comprehensive description of what went wrong. Include context about what you were trying to accomplish and where the issue occurred in the workflow.]

## Steps to Reproduce

Provide precise steps that allow others to reproduce this issue:

1. [First step]
2. [Second step]
3. [Third step]
4. [Continue until issue occurs]

**Reproducibility**: [Always / Sometimes / Once / Unable to reproduce]

## Expected Behavior

[Describe what you expected to happen. Reference documentation, workflow scenarios, or test specifications if applicable.]

## Actual Behavior

[Describe what actually happened. Include specific details about error messages, unexpected outputs, or deviations from expected behavior.]

## Environment Information

**Claude Code Version**: [e.g., 1.2.3]
**Operating System**: [e.g., macOS 14.0, Ubuntu 22.04, Windows 11]
**Shell**: [e.g., zsh, bash, PowerShell]
**Python Version** (if relevant): [e.g., 3.11.5]
**Node Version** (if relevant): [e.g., 20.0.0]
**Git Version** (if relevant): [e.g., 2.42.0]

**Plugin Versions**:
- agent-loop: [version]
- epti: [version]
- visual-iteration: [version]

## Evidence

### Screenshots
[Attach or describe relevant screenshots showing the issue]

### Terminal Output
```
[Paste relevant terminal output, error messages, or stack traces]
```

### Log Files
[Reference or attach relevant log files from Claude Code or plugin execution]

### Code/Configuration
[Include relevant code snippets, configuration files, or command definitions that relate to the issue]

## Severity

Select the appropriate severity level based on impact:

- [ ] **Critical** - Blocks core functionality, prevents plugin use entirely
  - Examples: Plugin won't install, commands crash Claude Code, data loss occurs
  - **Impact**: Complete blocker, no workaround available
  - **Urgency**: Must fix before production release

- [ ] **High** - Major feature broken, significant workflow disruption
  - Examples: Agent provides incorrect guidance leading to wrong implementation, workflow cannot complete, command produces wrong output
  - **Impact**: Major functionality broken, difficult workaround required
  - **Urgency**: Should fix before production release

- [ ] **Medium** - Feature works but with problems, workaround available
  - Examples: Command works but error message is unclear, agent guidance is confusing but correct, performance degradation
  - **Impact**: Annoying but usable, reasonable workaround exists
  - **Urgency**: Should fix soon, may defer if limited resources

- [ ] **Low** - Minor cosmetic issue, nice-to-have improvement
  - Examples: Typo in documentation, inconsistent formatting, minor UI inconsistency
  - **Impact**: Minimal, purely cosmetic or minor convenience
  - **Urgency**: Fix when convenient, may be deferred

**Selected Severity**: [Critical / High / Medium / Low]

**Justification for Severity**:
[Explain why you assigned this severity level. Consider impact on users, availability of workarounds, and frequency of occurrence.]

## Impact Assessment

**Affected Users**: [All users / Users of specific plugin / Users in specific scenarios / Edge case]

**Frequency**: [Every time / Frequently / Occasionally / Rarely]

**Workaround Available**: [Yes / No]

**Workaround Description** (if applicable):
[Describe the workaround that allows users to avoid or mitigate the issue]

## Root Cause Analysis (Optional)

If you have insight into why this issue occurs, document it here:

**Suspected Root Cause**:
[Your hypothesis about what's causing the issue]

**Relevant Code/Configuration**:
[Point to specific files, functions, or configuration that may be involved]

## Related Issues

**Related Test Scenario**: [Reference the test scenario from command-scenarios or workflow-scenarios that revealed this issue]

**Related Issues**: [List any related or duplicate issue IDs]

**Blocking Issues**: [List any issues that must be resolved before this one can be addressed]

**Blocked Issues**: [List any issues that are blocked by this one]

## Suggested Fix (Optional)

If you have ideas about how to fix this issue, document them here:

**Proposed Solution**:
[Describe how you think this issue should be resolved]

**Alternative Approaches**:
1. [Alternative 1]
2. [Alternative 2]

**Implementation Complexity**: [Trivial / Simple / Moderate / Complex / Very Complex]

## Verification Steps

Once this issue is fixed, verify the fix using these steps:

1. [Verification step 1]
2. [Verification step 2]
3. [Verification step 3]

**Success Criteria**: [Define what "fixed" means - specific measurable outcomes]

## Additional Context

[Any other information that might be helpful for understanding or resolving this issue. Include links to relevant documentation, related discussions, or background information.]

## Attachments

List any files attached to this issue report:
- [ ] Screenshots
- [ ] Log files
- [ ] Configuration files
- [ ] Screen recordings
- [ ] Minimal reproduction repository

---

## Issue Tracking

**Status**: [Open / In Progress / Resolved / Closed / Won't Fix / Duplicate]

**Assigned To**: [Name or team]

**Target Resolution**: [YYYY-MM-DD or milestone]

**Resolution Notes**:
[Once resolved, document the fix applied, validation performed, and any follow-up actions]

**Resolved By**: [Name]
**Resolution Date**: [YYYY-MM-DD]
**Resolved In Version**: [Plugin version]

---

## Example Issue Report

Below is an example of a complete issue report:

---

**Issue ID**: ISSUE-001
**Date Reported**: 2025-11-06
**Reported By**: Alice Tester
**Plugin**: agent-loop
**Component**: command

### Description

**Summary**: /explore command produces empty prompt expansion

**Detailed Description**:
When executing the /explore command in agent-loop plugin, the command is recognized and autocomplete works, but the prompt expansion that should contain exploration guidance is completely empty. This prevents the exploration phase from being usable.

### Steps to Reproduce

1. Install agent-loop plugin successfully
2. Verify plugin is loaded (commands visible in autocomplete)
3. Open a new conversation in Claude Code
4. Type `/explore` and press Enter
5. Observe the resulting prompt expansion

**Reproducibility**: Always

### Expected Behavior

The /explore command should expand to a comprehensive prompt containing:
- Systematic code exploration guidance
- Questions to ask about the codebase
- Tools to use for investigation
- Next steps after exploration completes

This is documented in `commands/explore.md` and should be approximately 50-70 lines of guidance.

### Actual Behavior

The command is recognized (autocomplete shows it), but after pressing Enter, the prompt expansion is completely empty. No guidance text appears. The conversation proceeds with no additional context provided to Claude.

### Environment Information

**Claude Code Version**: 1.2.0
**Operating System**: macOS 14.0 (Sonoma)
**Shell**: zsh
**Python Version**: 3.11.5

**Plugin Versions**:
- agent-loop: 0.1.0

### Evidence

**Terminal Output**:
```
> /explore
[Empty expansion - no guidance displayed]
```

**File Check**:
```bash
$ cat plugins/agent-loop/commands/explore.md
# [File has 57 lines of content - file is not empty]
```

### Severity

**Selected Severity**: High

**Justification for Severity**:
The /explore command is the first step in the agent-loop workflow. Without working command expansion, users cannot use the plugin's core functionality. While the agent can still be invoked manually, the command-based workflow is broken. This is a major feature failure but the entire plugin is not blocked (workaround exists).

### Impact Assessment

**Affected Users**: All users of agent-loop plugin

**Frequency**: Every time

**Workaround Available**: Yes

**Workaround Description**:
Users can manually paste the content of `commands/explore.md` into their conversation. However, this defeats the purpose of the command system and is very cumbersome.

### Root Cause Analysis

**Suspected Root Cause**:
Command file may not be correctly linked in plugin.json, or file encoding issue preventing content from being read.

**Relevant Code/Configuration**:
- `plugins/agent-loop/.claude-plugin/plugin.json` - check commands path
- `plugins/agent-loop/commands/explore.md` - verify file encoding is UTF-8

### Related Issues

**Related Test Scenario**: commands-agent-loop.md, Test Case: /explore command execution

### Suggested Fix

**Proposed Solution**:
1. Verify `plugin.json` has correct `"commands": "./commands/"` path
2. Check file permissions on explore.md (should be readable)
3. Validate file encoding is UTF-8 without BOM
4. Test command loading in isolation to verify file can be read

**Implementation Complexity**: Simple

### Verification Steps

1. Reload agent-loop plugin in Claude Code
2. Start new conversation
3. Execute `/explore` command
4. Verify prompt expansion contains approximately 50-70 lines of guidance text
5. Verify guidance text matches content of commands/explore.md

**Success Criteria**: /explore command expands to full guidance content, matching the explore.md file, every time.

---
