---
name: gating-controller
description: Process gates (decision-gate, security-gate, checkpoint-gate) based on user-configured rules. Supports BLOCKING, NONBLOCKING, and CUSTOM modes per gate type. Runs in main context so CAN use AskUserQuestion. For CUSTOM mode, invokes gate-evaluator skill.
---

# Gating Controller

Process gates based on user-configured rules for each gate type.

**Critical**: You run in main Claude context, so you CAN use AskUserQuestion directly.

## Gate Types

| Gate | When Called | Log Location | Purpose |
|------|-------------|--------------|---------|
| `decision-gate` | Agent logs architecture/technology choice | `DECISIONS/` | Review before continuing |
| `security-gate` | Agent logs security-sensitive change | `SECURITY/` | Immediate review |
| `checkpoint-gate` | Command completes | N/A (no log) | Verify work before continuing |
| `agent-gate` | Task analyzed as concrete | N/A (no log) | Choose execution mode: agent vs main context |

## Process

**Step 1**: Load gate config

Read from `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt`.
Get EXEC_ID from `.agent_logs/do-more-now/CURRENT_EXECUTION_ID.txt`.

If no config exists, return "CONTINUE: No gating active".

**Step 2**: Collect pending items for requested gate type

For `decision-gate`:
- Glob: `.agent_planning/do-command-state/<EXEC_ID>/DECISIONS/*.txt`
- Look for files without `APPROVAL_STATUS:` block

For `security-gate`:
- Glob: `.agent_planning/do-command-state/<EXEC_ID>/SECURITY/*.txt`
- Look for files without `APPROVAL_STATUS:` block

For `checkpoint-gate`:
- No files to collect - invoke `work-checkpoint` skill directly

For `agent-gate`:
- No files to collect - evaluate based on task analysis context passed from command

**Step 3**: Get mode for gate type

```
DECISION_GATE: BLOCKING | NONBLOCKING | CUSTOM
DECISION_PROMPT: <if CUSTOM>

SECURITY_GATE: BLOCKING | NONBLOCKING | CUSTOM
SECURITY_PROMPT: <if CUSTOM>

CHECKPOINT_GATE: BLOCKING | NONBLOCKING | CUSTOM
CHECKPOINT_PROMPT: <if CUSTOM>

AGENT_GATE: BLOCKING | NONBLOCKING | CUSTOM
AGENT_PROMPT: <if CUSTOM>
```

**Step 4**: Process based on mode

| Mode | Action |
|------|--------|
| BLOCKING | Always trigger - ask user for each pending item |
| NONBLOCKING | Never trigger - auto-approve all, mark files |
| CUSTOM | Invoke `gate-evaluator` skill for each item |

**For CUSTOM mode**:
1. Invoke `do:gate-evaluator` skill with:
   - `gate_type`: The gate being evaluated
   - `context`: Content of the logged decision/security event
   - `user_prompt`: The user's custom rule
2. If result is `TRIGGER` → Ask user
3. If result is `SKIP` → Auto-approve, log rationale

**Step 5**: If triggered, ask user

Use AskUserQuestion. See `references/decision-templates.md` for format.

**For agent-gate specifically**:
```json
{
  "questions": [{
    "question": "This task looks concrete and well-scoped. How should I execute it?",
    "header": "Execution",
    "options": [
      {
        "label": "Use agent",
        "description": "Token-efficient, autonomous execution. Less visible progress. Best for well-defined tasks."
      },
      {
        "label": "Work with me",
        "description": "Interactive, visible progress. Easier to redirect. Best for exploratory work."
      },
      {
        "label": "Plan first",
        "description": "Create detailed plan, then decide execution mode"
      }
    ],
    "multiSelect": false
  }]
}
```

**Return value for agent-gate**:
- "Use agent" → `"USE_AGENT"`
- "Work with me" → `"STAY_MAIN"`
- "Plan first" → `"PLAN_FIRST"`

**Step 6**: Mark files as processed

Append to each processed file:
```
---
APPROVAL_STATUS: USER_APPROVED | USER_REJECTED | AUTO_APPROVED
APPROVED_AT: <timestamp>
APPROVED_BY: user | auto (<mode>)
USER_FEEDBACK: <if rejected or has comments>
```

**Step 7**: Return status

- Any USER_REJECTED → `"STOP: User rejected - [summary]"`
- All approved → `"CONTINUE: [gate_type] processed (N items)"`

## Calling From Commands

Commands should invoke gating-controller at key points:

```
After agent returns:
  → Process decision-gate (if agent logged decisions)
  → Process security-gate (if agent logged security events)

After command completes:
  → Process checkpoint-gate
```

## References

- `references/gate-config-format.md` - Config format and hierarchy
- `references/gate-modes.md` - Mode processing logic
- `references/decision-templates.md` - AskUserQuestion format
