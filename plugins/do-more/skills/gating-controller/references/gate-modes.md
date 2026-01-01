# Gate Modes

How each gate mode processes decisions and checkpoints.

## Overview

| Mode | Decision Gates | End-of-Command Checkpoint |
|------|----------------|---------------------------|
| BLOCKING | All decisions need approval | Full verification |
| VERIFIED | Auto-approve decisions | Full verification at end |
| HYBRID | Only HIGH risk needs approval | No checkpoint |
| NONBLOCKING | All auto-approved | No checkpoint |

**Key insight**: BLOCKING and VERIFIED both provide user verification opportunities, but at different points:
- BLOCKING: Stops at each decision (frequent, granular)
- VERIFIED: Stops at end of command (less frequent, batch review)

---

## VERIFIED Mode (Checkpoint-Based)

**Auto-approve decisions during work**, but present **full verification checkpoint at command end**.

This mode is for users who want to:
- Let Claude work autonomously through a task
- Review all completed work before moving on
- Provide feedback on the actual results, not just the decisions

Process:
1. Auto-approve all decisions during execution (like NONBLOCKING)
2. At end of command, invoke `work-checkpoint` skill
3. Present each work item for user verification
4. Collect feedback and determine next action

**Example**:
```
User: /do:it implement auth (VERIFIED mode)

[Claude works through task, auto-approving decisions]

At completion:
┌─────────────────────────────────────────────────────────────┐
│ Work Completed - Please Verify                               │
├─────────────────────────────────────────────────────────────┤
│ 1. User Authentication Module                                │
│    Files: src/auth.py, tests/test_auth.py                   │
│    How to verify: Run `pytest tests/test_auth.py -v`        │
│                                                              │
│    How does this look?                                       │
│    [ ] Looks great!  [ ] It's okay  [ ] Needs work          │
└─────────────────────────────────────────────────────────────┘

User: "It's okay" + "Need rate limiting"

┌─────────────────────────────────────────────────────────────┐
│ What would you like to do next?                              │
│ [ ] Address feedback  [ ] Continue work  [ ] Stop here      │
└─────────────────────────────────────────────────────────────┘
```

---

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

### Intent Detection (from user input)

| User Signals | Mode |
|--------------|------|
| "carefully", "approve each decision", "ask before each choice" | BLOCKING |
| "verify", "check my work", "review when done", "let me test" | VERIFIED |
| "guided", "review major", "important decisions only" | HYBRID |
| "autonomous", "auto", "just do it", "trust your judgment" | NONBLOCKING |

### User Prompt (when no intent detected)

Ask a simple question users can understand:

```
When should I stop for your review?
- "When done" → VERIFIED (work through task, verify results)
- "Each decision" → BLOCKING (stop before each choice)
- "Keep going" → NONBLOCKING (work until complete)
```

HYBRID is available via intent detection but not in the simplified prompt (too confusing for most users).

**Choosing between BLOCKING and VERIFIED**:
- BLOCKING: User wants to approve decisions *before* they're implemented
- VERIFIED: User wants to review *results* after implementation

**Recommendation**: VERIFIED ("When done") is the best default - it lets Claude work efficiently while still giving users the review checkpoint they want.
