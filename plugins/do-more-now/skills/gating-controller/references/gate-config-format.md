# Gate Configuration

How gate settings are determined and stored.

## Configuration Sources

From highest to lowest precedence:

1. **Command-level** - Inline in `/do:` command (e.g., "carefully", "ask about auth")
2. **Session context** - User said earlier "for this session, always verify"
3. **CLAUDE.md** - Natural language in project or user CLAUDE.md
4. **Prompt** - Ask user at command start if not configured

## Gate Types

| Gate | When Triggered | Purpose |
|------|----------------|---------|
| `decision-gate` | Agent makes architecture/technology choice | Review before implementation |
| `security-gate` | Touching auth, credentials, external APIs, deps | Immediate review |
| `checkpoint-gate` | Command completes | Verify work before continuing |

## In CLAUDE.md (Natural Language)

Users can configure gates in plain English:

```markdown
## Gating Preferences

When using /do: commands:
- Always verify my work before moving on
- Ask me immediately about any security-related changes
- Only ask about major architectural decisions
```

Or more specifically:

```markdown
## Gating

- decision-gate: Ask only about major architectural decisions
- security-gate: Always ask immediately
- checkpoint-gate: Always verify when done
```

## Inline in Commands

| User says | Interpretation |
|-----------|----------------|
| "carefully" | All gates → BLOCKING |
| "verify when done" | checkpoint-gate: BLOCKING |
| "autonomous" / "just do it" | All gates → NONBLOCKING |
| "ask about auth decisions" | decision-gate: CUSTOM with that rule |

## Prompting (when not configured)

If no gate config found, show brief context then ask:

```
The do-more-now plugin can work autonomously or stop for your review.
You can configure this permanently in CLAUDE.md or choose now.

[AskUserQuestion: When should I stop for your review?]
```

See it.md Step 0c for the full prompt format.

## Runtime State

Write to `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt`:

```
EXEC_ID: <uuid>
COMMAND: /do:it
CREATED: <timestamp>
SOURCE: command | session | claude-md | prompted

DECISION_GATE: BLOCKING | NONBLOCKING | CUSTOM
DECISION_PROMPT: <if CUSTOM>

SECURITY_GATE: BLOCKING | NONBLOCKING | CUSTOM
SECURITY_PROMPT: <if CUSTOM>

CHECKPOINT_GATE: BLOCKING | NONBLOCKING | CUSTOM
CHECKPOINT_PROMPT: <if CUSTOM>
```

## Example Configurations

**Conservative** (reviews everything):
```
DECISION_GATE: BLOCKING
SECURITY_GATE: BLOCKING
CHECKPOINT_GATE: BLOCKING
```

**Security-focused** (always catch security, trust other decisions):
```
DECISION_GATE: NONBLOCKING
SECURITY_GATE: BLOCKING
CHECKPOINT_GATE: BLOCKING
```

**Verify results only** (trust all decisions, check output):
```
DECISION_GATE: NONBLOCKING
SECURITY_GATE: NONBLOCKING
CHECKPOINT_GATE: BLOCKING
```

**Autonomous**:
```
DECISION_GATE: NONBLOCKING
SECURITY_GATE: NONBLOCKING
CHECKPOINT_GATE: NONBLOCKING
```
