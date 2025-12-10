# Execution Tracking

This skill provides the mechanism for tracking work across subagent invocations. It enables the execution summary system.

## Overview

Every `/do:*` command creates an **execution context** - a unique ID that links all work done during that command's execution. Subagents write **partial summaries** tagged with this ID. At the end, the orchestrator invokes the **execution-summarizer** agent to aggregate everything into a final report.

## Execution ID Format

```
EXEC-<command>-<YYYYMMDD-HHmmss>-<random4>
```

Example: `EXEC-plan-20251207-143052-a7b3`

The random suffix prevents collisions if the same command is run multiple times per second.

## Directory Structure

```
.agent_planning/
├── .exec/                              # Ephemeral execution traces
│   ├── PARTIAL-EXEC-plan-...-001-project-evaluator.txt
│   ├── PARTIAL-EXEC-plan-...-002-researcher.txt
│   └── PARTIAL-EXEC-plan-...-003-status-planner.txt
└── EXEC-plan-20251207-143052.md        # Final aggregated report
```

## For Commands: Starting Execution

At the START of every `/do:*` command, generate an execution ID and set the context:

```markdown
## Execution Context

Generate execution ID: `EXEC-<command>-<YYYYMMDD-HHmmss>-<random4>`

Create execution directory if needed:
```bash
mkdir -p .agent_planning/.exec
```

Pass execution context to all subagent invocations:
- Include `EXECUTION_ID: <id>` in the prompt
- Track sequence number (increment for each subagent)
```

## For Subagents: Writing Partial Summaries

Every subagent MUST write a partial summary at completion.

**Location**: `.agent_planning/.exec/PARTIAL-<execution-id>-<sequence>-<agent-name>.txt`

**Sequence**: 3-digit zero-padded number (001, 002, etc.) provided by orchestrator

**Format**:
```
EXECUTION: <execution-id>
SEQUENCE: <sequence-number>
AGENT: <agent-name>
STARTED: <ISO timestamp>
COMPLETED: <ISO timestamp>
STATUS: success | partial | failed | skipped

## Work Performed
- <action 1>
- <action 2>
- ...

## Key Findings
- <finding 1> (or "None")
- ...

## Artifacts Created
- <file path 1>
- <file path 2>
- (or "None")

## Issues Encountered
- <issue 1> (or "None")
- ...

## Handoff Notes
<what the next agent or orchestrator should know>
```

**Example** (`PARTIAL-EXEC-plan-20251207-143052-a7b3-001-project-evaluator.txt`):
```
EXECUTION: EXEC-plan-20251207-143052-a7b3
SEQUENCE: 001
AGENT: project-evaluator
STARTED: 2025-12-07T14:30:52Z
COMPLETED: 2025-12-07T14:31:15Z
STATUS: success

## Work Performed
- Evaluated project against PROJECT_SPEC.md
- Analyzed 47 source files
- Compared implementation to 12 spec requirements

## Key Findings
- 3 major gaps identified (auth, caching, logging)
- 2 ambiguities need resolution
- Overall completion: 65%

## Artifacts Created
- .agent_planning/STATUS-20251207-143115.md

## Issues Encountered
- None

## Handoff Notes
Found 2 ambiguities that need research before planning can complete.
Recommend researcher agent for: (1) caching strategy, (2) logging framework choice.
```

## For Commands: Finalizing Execution

At the END of every `/do:*` command, invoke the execution-summarizer:

```markdown
## Finalize Execution

Use the do:execution-summarizer agent to aggregate all partial summaries:
- Pass the execution ID
- Agent will read all PARTIAL files
- Agent will create EXEC-<command>-<timestamp>.md
- Agent will clean up PARTIAL files

Display the executive summary from the report to the user.
```

## Sequence Tracking

The orchestrator (command) tracks the sequence number:

```
sequence = 1

invoke project-evaluator with:
  EXECUTION_ID: EXEC-plan-20251207-143052-a7b3
  SEQUENCE: 001

sequence = 2

invoke researcher with:
  EXECUTION_ID: EXEC-plan-20251207-143052-a7b3
  SEQUENCE: 002

... and so on
```

## Error Handling

If a subagent fails to write its partial:
- The execution-summarizer will note the gap
- Final report will be marked as "partial"
- Cleanup will still proceed

If execution-summarizer fails:
- Partial files remain in .exec/ for debugging
- User can manually inspect or re-run summarization

## Context Efficiency

This system is designed for minimal context overhead:

1. **Partials are ephemeral**: Written to disk, not kept in context
2. **Summarizer uses haiku**: Cheap, fast aggregation
3. **Final report is concise**: Executive summary for quick scanning
4. **Cleanup is automatic**: No accumulation of trace files

## Integration Checklist

For each subagent:
- [ ] Accept EXECUTION_ID and SEQUENCE in prompt
- [ ] Write PARTIAL file at completion (before final output)
- [ ] Include all 6 required sections

For each command:
- [ ] Generate execution ID at start
- [ ] Pass ID and sequence to each subagent invocation
- [ ] Invoke execution-summarizer at end
- [ ] Display executive summary to user
