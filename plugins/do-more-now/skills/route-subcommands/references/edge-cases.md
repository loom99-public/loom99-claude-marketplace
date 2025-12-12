# Route Subcommands Edge Cases

How to handle special situations when routing commands.

## Self-Reference

If user includes the current command (e.g., `/do:it` within `/do:it`), **skip it** to avoid infinite loops.

**Input**: `/do:it /do:it fix the bug`
**Result**: Skip the nested `/do:it`, main instructions = "fix the bug"

---

## Ambiguous Ordering

When order signals are unclear, use this preference:

| Command Type | Default Position |
|--------------|------------------|
| `/do:explore` | Pre |
| `/do:research` | Pre |
| `/do:plan` | Pre |
| Implementation | Main |
| `/do:docs` | Post |
| `/do:chores` | Post |

**Example**: `/do:it /do:plan /do:chores fix bug`
- Pre: `/do:plan`
- Main: `fix bug`
- Post: `/do:chores`

---

## No Clear Main Instructions

If input is ALL commands with no clear main task:

**Input**: `/do:it /do:plan then /do:chores`

**Result**:
- Execute commands in order
- Main workflow gets empty/minimal instructions, which means look at the last 2-3 messages in the context for the instructions.

---

## Command with Arguments vs Separate Command

Distinguish between command arguments and separate commands:

**Input**: `/do:it /do:plan feature auth then /do:chores`
- `/do:plan feature` = command with argument "feature"
- `auth` = start of main instructions
- `/do:chores` = post command

**Heuristic**: Arguments to a command are the words immediately following it until another `/do:` or clear sentence boundary.

---

## Nested Quotes

Preserve quoted strings as atomic units:

**Input**: `/do:it Fix "the login bug" then /do:chores`
- Main: `Fix "the login bug"`
- Post: `/do:chores`

---

## Multiple "then" Keywords

Only first "then" (or equivalent) triggers post-command boundary:

**Input**: `/do:it Fix bug then verify, then /do:chores`
- Main: `Fix bug then verify`
- Post: `/do:chores`

The second "then" is part of the main instructions.
