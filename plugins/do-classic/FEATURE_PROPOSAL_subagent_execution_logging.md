# Feature Proposal: Subagent Execution Logging

## Goal

Lightweight documentation of work performed when a user runs a `/do:*` slash command. Provides insight into what happened across all subagents (and within the orchestrating top level agent) without polluting the main Claude context.

## Requirements

- User does nothing special - this always happens for any `/do:` command
- Includes detailed summary of everything done (completed work, evaluations, reading docs, "tried stuff and couldn't get it working")
- Also includes executive summary ("summary of the summary") for quick scanning
- Must handle that subagent output is NOT visible to users - all communication via files
- Must use a summarizer subagent to aggregate individual logs (keeps main context clean)
- Final summary written to file, then slash command prints it to console

## File Naming Convention

```
.agent_planning/_slash_command_logs_tmp/<timestamp>-<command_summary>/<N>-<subagent_name>-<5_word_summary>.log
```

Where:
- `<timestamp>` - ensures uniqueness per command execution
- `<command_summary>` - slash command that was run, spaces replaced by `_`, no special characters
- `<N>` - monotonic integer for chronological order (subagents cannot communicate to determine this - must be reliable and token efficient)
- `<subagent_name>` - which agent wrote this
- `<5_word_summary>` - brief description of task

Example:
```
.agent_planning/_slash_command_logs_tmp/20251207-143052-do_plan_authentication/001-project-evaluator-evaluated_auth_system_gaps.log
.agent_planning/_slash_command_logs_tmp/20251207-143052-do_plan_authentication/002-researcher-investigated_jwt_vs_sessions.log
.agent_planning/_slash_command_logs_tmp/20251207-143052-do_plan_authentication/003-status-planner-created_implementation_plan.log
```

## Top Priority Constraints

These are P0 deal-breakers - any possibility of these is itself a P0:
- Must not be confusing, incorrect, or require user effort to get value
- Logs stored per slash command in repo itself - can never overlap with another repo or command
- Raw subagent logs archived after use so they can never conflict with another command's logs

## Hook-Based Architecture

### UserPromptSubmit Hook
- Detects if user is running a `/do:` command
- If not a `/do:` command, exit immediately (allow Claude to continue unaffected)
- If `/do:` command, generate stable ID for "User Prompt Execution Context"
- Creates the directory for this execution's logs

### PreToolUse Hook (matcher: Task)
- Triggered before each subagent invocation
- Use for configuration, validation, logging as needed
- Could inject execution context into subagent prompt
- Could track sequence number (N) for ordering

### SubagentStop Hook
- Gets access to `transcript_path` containing subagent transcript
- Copy relevant content from transcript into the log file for that subagent
- Each subagent should write a brief summary of what it accomplished

### SessionEnd Hook
- Create the overall summary from individual subagent logs
- Uses summarizer subagent to aggregate
- Archives the raw logs
- Writes final EXEC-*.md report

### SessionStart Hook
- Check for leftover files from interrupted sessions
- If processable into something useful, do so
- Otherwise move to `.agent_planning/_subagent_logs_leftover/`
- Any files already in `_subagent_logs_leftover/` on startup are deleted immediately (user expected to back up before starting new session)
- No need to inform user of this

## Agent Changes

Minimal - just a few lines, not paragraphs. Agents already know they're performing tasks. They should be prepared to give a brief summary without extensive explanation.

## Summarizer Agent

The execution-summarizer agent:
- Reads all individual subagent log files for an execution
- Creates chronological timeline
- Generates executive summary (1 paragraph)
- Generates detailed summary
- Writes to `.agent_planning/EXEC-<command>-<timestamp>.md`
- Since it's a subagent, it writes to file - the calling command then prints it

## Key Design Principles

1. **Token minimal** - Add few lines to agents, not paragraphs
2. **Obvious grouping** - File naming makes it trivially obvious which files belong together and their order
3. **No conflicts** - Timestamp + command in directory name prevents any overlap
4. **Cleanup via hooks** - SessionStart/SessionEnd handle stale files automatically
5. **No user effort** - Everything automatic, no maintenance required
6. **Context efficient** - Summarizer subagent keeps aggregation out of main context
