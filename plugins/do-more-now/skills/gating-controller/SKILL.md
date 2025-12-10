---
name: gating-controller
description: Process pending decisions from agents, ask user for approvals based on gate mode (BLOCKING/HYBRID/NONBLOCKING). Runs in main context so CAN use AskUserQuestion. Routes HIGH-risk decisions to user, auto-approves LOW-risk.
---

# Gating Controller

Review pending agent decisions and determine if they need user approval.

**Critical**: You run in main Claude context, so you CAN use AskUserQuestion directly.

## Process

**Step 1**: Read gate config

```
.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt
```

Get EXEC_ID from `.agent_planning/do-command-logs/CURRENT_EXECUTION_ID.txt`.
If no config exists, return "CONTINUE: No gating active".

**Step 2**: Collect pending decisions

Glob: `.agent_planning/do-command-state/<EXEC_ID>/DECISIONS/*.txt`
Look for `APPROVAL_STATUS: PENDING` or no approval block yet.

**Step 3**: Process each decision by mode

| Mode | HIGH Risk | MEDIUM Risk | LOW Risk |
|------|-----------|-------------|----------|
| BLOCKING | Ask user | Ask user | Ask user |
| HYBRID | Ask user | Auto-approve | Auto-approve |
| NONBLOCKING | Auto-approve | Auto-approve | Auto-approve |

For mode-specific logic and examples, see `references/gate-modes.md`.
For AskUserQuestion format, see `references/decision-templates.md`.

**Step 4**: Update decision files

Append approval block to each file. See `references/file-formats.md`.

**Step 5**: Return status

- Any USER_REJECTED → `"STOP: User rejected - [summary]. Reason: [feedback]"`
- All approved → `"CONTINUE: Processed N decisions (X user, Y auto)"`

## Error Handling

| Condition | Response |
|-----------|----------|
| Missing EXEC_ID file | "CONTINUE: No execution tracking" |
| Missing GATE_CONFIG | "CONTINUE: No gating active" |
| Missing DECISIONS dir | "CONTINUE: No decisions directory" |
| No pending decisions | "CONTINUE: No pending decisions" |

## References

- `references/gate-modes.md` - Mode processing logic and examples
- `references/decision-templates.md` - AskUserQuestion format
- `references/file-formats.md` - File structure specifications
