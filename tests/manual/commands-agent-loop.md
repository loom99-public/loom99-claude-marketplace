# agent-loop Command Test Scenarios

This document provides test scenarios for all 4 slash commands in the agent-loop plugin: /explore, /plan, /code, /commit.

## Command Test Matrix

| Command | Purpose | Expected Prompt Length | Key Content Areas |
|---------|---------|----------------------|-------------------|
| /explore | Systematic codebase investigation | ~50-70 lines | Investigation questions, tools to use, exploration patterns |
| /plan | Implementation planning | ~70-90 lines | Plan structure, dependency analysis, task breakdown |
| /code | Implementation guidance | ~80-100 lines | Implementation steps, verification, testing |
| /commit | Git commit workflow | ~120-140 lines | Commit message format, staging, pushing |

## Test Scenario: /explore Command

### Purpose
Verify that the /explore command expands to comprehensive codebase exploration guidance.

### Setup
- Start new conversation in Claude Code
- Have a test project open (any codebase will work)

### Execution Steps
- Type `/explore` in the conversation
- Press Enter to execute the command
- Observe the prompt expansion

### Expected Outcome
- Command executes without errors
- Prompt expansion appears with exploration guidance
- Guidance includes:
  - Questions to ask about the codebase structure
  - Tools to use for investigation (grep, find, tree, etc.)
  - Systematic exploration methodology
  - Next steps after exploration completes
- Prompt length is approximately 50-70 lines
- Guidance is actionable and specific

### Error Scenarios
| Scenario | Expected Behavior |
|----------|-------------------|
| /explore executed in empty directory | Should still provide guidance, may suggest creating initial structure |
| /explore executed twice | Should work both times, guidance remains consistent |
| /explore with typo (/explor) | Command not recognized error |

## Test Scenario: /plan Command

### Purpose
Verify that the /plan command expands to comprehensive planning guidance.

### Setup
- Start new conversation in Claude Code
- Have completed exploration phase (or simulate having codebase knowledge)

### Execution Steps
- Type `/plan` in the conversation
- Press Enter to execute
- Observe the prompt expansion

### Expected Outcome
- Command executes without errors
- Prompt expansion appears with planning guidance
- Guidance includes:
  - How to structure implementation plans
  - Dependency analysis methodology
  - Task breakdown strategies
  - Priority assessment
  - Risk identification
- Prompt length is approximately 70-90 lines
- Guidance emphasizes writing plans before coding

### Error Scenarios
| Scenario | Expected Behavior |
|----------|-------------------|
| /plan executed without prior exploration | Should still work, may prompt to explore first |
| /plan with no context about what to build | Should guide on gathering requirements |

## Test Scenario: /code Command

### Purpose
Verify that the /code command expands to comprehensive implementation guidance.

### Setup
- Start new conversation in Claude Code
- Have a plan ready (or simulate having planned work)

### Execution Steps
- Type `/code` in the conversation
- Press Enter to execute
- Observe the prompt expansion

### Expected Outcome
- Command executes without errors
- Prompt expansion appears with implementation guidance
- Guidance includes:
  - Implementation methodology
  - Code quality standards
  - Testing requirements
  - Verification steps
  - Common pitfalls to avoid
- Prompt length is approximately 80-100 lines
- Guidance emphasizes following the plan

### Error Scenarios
| Scenario | Expected Behavior |
|----------|-------------------|
| /code executed without a plan | Should warn about coding without planning |
| /code when tests don't exist | Should remind to create tests |

## Test Scenario: /commit Command

### Purpose
Verify that the /commit command expands to comprehensive git workflow guidance.

### Setup
- Start new conversation in Claude Code
- Have changes ready to commit in git repository
- Be in directory with git initialized

### Execution Steps
- Type `/commit` in the conversation
- Press Enter to execute
- Observe the prompt expansion

### Expected Outcome
- Command executes without errors
- Prompt expansion appears with commit guidance
- Guidance includes:
  - Git workflow steps (status, diff, add, commit, push)
  - Commit message format and best practices
  - Code review preparation
  - Verification before pushing
- Prompt length is approximately 120-140 lines
- Guidance includes specific git commands to run

### Error Scenarios
| Scenario | Expected Behavior |
|----------|-------------------|
| /commit in non-git directory | Should suggest initializing git or provide general guidance |
| /commit with no changes | Should handle gracefully, may suggest checking git status |

## Workflow Sequence Testing

### Complete Workflow: explore → plan → code → commit

**Test the full 4-stage workflow in sequence:**

- Execute `/explore` and use guidance to investigate codebase
- Execute `/plan` and use guidance to create implementation plan
- Execute `/code` and use guidance to implement the plan
- Execute `/commit` and use guidance to commit changes

**Expected Outcome:**
- All 4 commands execute successfully in sequence
- Each command's guidance builds on the previous stage
- Workflow feels natural and well-integrated
- Agent provides appropriate guidance at each stage transition

## Autocomplete Verification

### Test Command Autocomplete

**Steps:**
- Start new conversation
- Type `/` (just the slash)
- Observe autocomplete suggestions

**Expected:**
- All 4 agent-loop commands appear: /explore, /plan, /code, /commit
- Commands show helpful descriptions
- Commands are distinguishable from other plugins
- Tab completion works to select commands

## Negative Test Scenarios

### Invalid Command Names

| Invalid Command | Expected Behavior |
|----------------|-------------------|
| /explor | Command not found error |
| /plann | Command not found error |
| /coded | Command not found error |
| /commits | Command not found error |
| /EXPLORE | Should work (commands should be case-insensitive) or show error |

### Out-of-Order Workflow

| Scenario | Expected Agent Behavior |
|----------|------------------------|
| Skip /explore, go directly to /plan | Agent should suggest exploring first |
| Skip /plan, go directly to /code | Agent should warn about coding without a plan |
| Use /commit before implementing | Agent should indicate no changes to commit |

## Test Results Template

Record test results for each command:

| Date | Tester | Command | Result | Expected Outcome | Actual Outcome | Notes |
|------|--------|---------|--------|-----------------|----------------|-------|
| | | /explore | | Guidance expansion works | | |
| | | /plan | | Guidance expansion works | | |
| | | /code | | Guidance expansion works | | |
| | | /commit | | Guidance expansion works | | |

## Success Criteria

Command testing is successful when:

- All 4 commands are accessible via autocomplete
- Each command expands to comprehensive guidance (50+ lines)
- Guidance content matches the command's purpose
- No errors occur during normal command execution
- Workflow sequence (explore→plan→code→commit) executes smoothly
- Negative test scenarios handle errors gracefully
- Agent provides appropriate stage-specific guidance
