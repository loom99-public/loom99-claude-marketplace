---
name: gate-evaluator
description: Evaluates whether a gate should trigger based on context and user-configured rules. Takes gate type, context summary, and user's custom prompt. Returns TRIGGER or SKIP with rationale. Use when processing gates with CUSTOM mode configuration.
---

# Gate Evaluator

Evaluate whether a gate should trigger based on user-defined rules.

## Input

You receive:
1. **gate_type**: Which gate is being evaluated (e.g., `decision-gate`, `checkpoint-gate`)
2. **context**: Summary of what triggered the gate (decision made, work completed, etc.)
3. **user_prompt**: The user's custom rule for this gate

## Process

**Step 1**: Parse the user's prompt to understand their intent

Common patterns:
- "Ask me if X" → Trigger when X is present
- "Only stop for Y" → Trigger only when Y applies
- "Skip unless Z" → Skip by default, trigger for Z
- "Always/never" → Absolute rules

**Step 2**: Evaluate context against the rule

Ask: Does this context match the user's criteria?

**Step 3**: Return decision

```
GATE_RESULT: TRIGGER | SKIP
GATE_TYPE: <gate_type>
RATIONALE: <1-2 sentence explanation>
CONTEXT_MATCHED: <what in the context matched or didn't match the rule>
```

## Examples

See `references/evaluation-examples.md` for common scenarios.

## Edge Cases

| Situation | Decision |
|-----------|----------|
| Ambiguous context | TRIGGER (err on side of asking) |
| Rule doesn't apply | SKIP with explanation |
| Multiple rules conflict | TRIGGER (conservative) |
| Empty context | SKIP (nothing to evaluate) |

## Output

Write evaluation to `.agent_planning/do-command-state/<EXEC_ID>/gate-evaluations.log`:

```
[<timestamp>] <gate_type>: <TRIGGER|SKIP>
  Rule: "<user_prompt summary>"
  Context: "<brief context>"
  Rationale: "<why>"
```

Return to caller:
```
GATE_RESULT: TRIGGER
```
or
```
GATE_RESULT: SKIP
```
