# Gating File Formats

Reference for all file formats used by the gating system.

## GATE_CONFIG.txt

Created when a command initializes with a gate mode.

```
GATE_MODE: BLOCKING | HYBRID | NONBLOCKING
EXEC_ID: <uuid>
CREATED: <iso-timestamp>
COMMAND: /do:<command>
USER_ARGS: <original arguments>
```

**Location**: `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt`

---

## DECISION File (Before Approval)

Created by agents when they make decisions.

```
DECISION_ID: <uuid>
EXEC_ID: <exec_id>
SEQUENCE: <n>
AGENT: <agent-name>
TIMESTAMP: <iso-timestamp>
RISK_LEVEL: HIGH | MEDIUM | LOW
CATEGORY: architecture | technology | implementation | testing | documentation

## Decision
<summary>

## Options Considered
- A: <option> - <tradeoffs>
- B: <option> - <tradeoffs>

## Chosen
<option and rationale>

## Impact If Wrong
<consequences>

## Auto-Approve Rationale
<why this can be auto-approved in HYBRID/NONBLOCKING>
```

**Location**: `.agent_planning/do-command-state/<EXEC_ID>/DECISIONS/<decision-id>.txt`

---

## DECISION File (After Approval)

Append this block after processing:

```
---
APPROVAL_STATUS: USER_APPROVED | AUTO_APPROVED | USER_REJECTED
APPROVED_AT: <iso-timestamp>
APPROVAL_RATIONALE: <rationale>
USER_FEEDBACK: <if provided>
```

---

## CURRENT_EXECUTION_ID.txt

Tracks current execution for continuity.

```
<uuid>
```

**Location**: `.agent_planning/do-command-logs/CURRENT_EXECUTION_ID.txt`
