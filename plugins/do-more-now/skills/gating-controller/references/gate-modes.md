# Gate Modes

How each gate mode processes decisions.

## BLOCKING Mode

**ALL decisions need user approval**, regardless of risk level.

Process:
1. Present decision to user with AskUserQuestion
2. Wait for response: Approve, Reject, or Modify
3. Mark as USER_APPROVED, USER_REJECTED, or capture USER_FEEDBACK

**Example**:
```
Input: 3 pending decisions (HIGH, MEDIUM, LOW risk)

1. Present HIGH-risk decision → User approves
2. Present MEDIUM-risk decision → User approves
3. Present LOW-risk decision → User rejects with feedback "Use functional instead"

Return: "STOP: User rejected decision - implementation-approach. Reason: Use functional instead"
```

---

## HYBRID Mode

**Only HIGH risk needs user approval**. Medium/Low are auto-approved.

Process:
- If RISK_LEVEL == HIGH:
  → Present to user (same as BLOCKING)
  → Mark as USER_APPROVED or USER_REJECTED
- If RISK_LEVEL == MEDIUM or LOW:
  → Mark as AUTO_APPROVED
  → Record rationale: "Auto-approved: [MEDIUM/LOW] risk in HYBRID mode"

**Example**:
```
Input: 3 pending decisions (HIGH, MEDIUM, LOW risk)

1. Present HIGH-risk decision → User approves
2. MEDIUM-risk → Auto-approved
3. LOW-risk → Auto-approved

Return: "CONTINUE: Processed 3 decisions (1 user-approved, 2 auto-approved)"
```

---

## NONBLOCKING Mode

**Auto-approve everything**. User reviews decisions after completion.

Process:
- Mark ALL as AUTO_APPROVED
- Record rationale: "Auto-approved: NONBLOCKING mode"

**Example**:
```
Input: 3 pending decisions (HIGH, MEDIUM, LOW risk)

1. HIGH-risk → Auto-approved (NONBLOCKING mode)
2. MEDIUM-risk → Auto-approved
3. LOW-risk → Auto-approved

Return: "CONTINUE: Processed 3 decisions (0 user-approved, 3 auto-approved)"
```

---

## Mode Selection Guidelines

| User Signals | Mode |
|--------------|------|
| "carefully", "approve each", "manual", "review everything" | BLOCKING |
| "guided", "review major", "important decisions only" | HYBRID |
| "autonomous", "auto", "just do it", "trust your judgment" | NONBLOCKING |

When ambiguous, default to HYBRID (recommended balance).
