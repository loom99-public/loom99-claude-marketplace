---
name: route-subcommands
description: Parse and execute inline /do: subcommands before/after the main workflow. Used by all /do: commands to handle chained command execution like "/do:it /do:plan then fix bug /do:chores".
---

# Route Subcommands

Parse user input for inline `/do:*` commands and execute them in correct order.

**IMPORTANT: Be silent.** If no subcommands found, return immediately without any output or explanation. Only output if there ARE subcommands to process.

## Process

**Step 1**: Quick scan for `/do:` patterns in input.

**If NO `/do:` patterns found** → Return silently to parent. No output needed.

**If `/do:` patterns found** → Continue to Step 2.

**Step 2**: Categorize commands:

| Category | Signals |
|----------|---------|
| Pre-commands | "first", "start with", before main task |
| Post-commands | "then", "after", "finally", at end |
| Main instructions | Everything else |

**Step 3**: Execute pre-commands via `SlashCommand` tool.

**Step 4**: Return to parent with:
- `main_instructions`: cleaned task
- `post_commands`: list for parent to execute after

For detailed examples, see `references/examples.md`.
For edge cases, see `references/edge-cases.md`.
