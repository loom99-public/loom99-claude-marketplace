---
name: route-subcommands
description: Parse and execute inline /do: subcommands before/after the main workflow. Used by all /do: commands to handle chained command execution.
---

# Route Subcommands

Parse user input for inline `/do:*` commands and execute them in the correct order relative to the main workflow.

## When to Use

Invoke this skill at the START of any `/do:` command when `$ARGUMENTS` may contain other `/do:` commands.

## Input

The skill receives context from the invoking command:
- `$ARGUMENTS` - The full user input string
- `$CURRENT_COMMAND` - The command being executed (e.g., "it", "plan", "explore")

## Process

### Step 1: Analyze User Intent

Examine `$ARGUMENTS` for any `/do:*` command references. Identify three categories:

**Pre-commands** (run BEFORE main workflow):
- Commands signaled by: "first", "start with", "begin by", "run X then"
- Commands appearing before the main instructions
- Commands in a sequence before the "main" task

**Post-commands** (run AFTER main workflow):
- Commands signaled by: "then", "after", "finally", "when done", "afterwards"
- Commands appearing after the main instructions
- Cleanup/chores typically go here

**Main instructions**:
- Everything that isn't a `/do:*` command
- The core task the user wants accomplished
- This gets passed to the current command's main workflow

### Step 2: Extract Main Instructions

Strip all `/do:*` command references from `$ARGUMENTS` to produce clean main instructions.

Example:
```
Input:  "/do:explore auth then /do:plan. Fix the login bug. /do:chores cleanup"
Output: "Fix the login bug."
```

### Step 3: Execute Pre-Commands

For each pre-command identified (in order):
1. Use `SlashCommand` tool to execute it
2. Pass the **main instructions** as arguments (so context flows through)
3. Wait for completion before next command

Example:
```
SlashCommand: /do:explore auth Fix the login bug.
SlashCommand: /do:plan Fix the login bug.
```

### Step 4: Return Control

After pre-commands complete, return to the invoking command with:
- `main_instructions`: The cleaned instruction string
- `post_commands`: List of commands to run after main workflow

The invoking command will:
1. Execute its main workflow with `main_instructions`
2. Execute post-commands when done

### Step 5: Execute Post-Commands (Called by Parent)

The parent command calls back to execute post-commands after its main workflow.

## Examples

### Example 1: Pre and Post Commands

**Input**: `/do:it /do:explore understand auth, then /do:plan. Fix the login bug. /do:chores cleanup temp files`

**Analysis**:
- Pre-commands: `/do:explore understand auth`, `/do:plan`
- Main instructions: `Fix the login bug.`
- Post-commands: `/do:chores cleanup temp files`

**Execution Order**:
1. `/do:explore understand auth Fix the login bug.`
2. `/do:plan Fix the login bug.`
3. Main `/do:it` workflow with "Fix the login bug."
4. `/do:chores cleanup temp files Fix the login bug.`

### Example 2: Only Pre-Commands

**Input**: `/do:it First /do:plan, then implement the auth system`

**Analysis**:
- Pre-commands: `/do:plan`
- Main instructions: `implement the auth system`
- Post-commands: none

### Example 3: Only Post-Commands

**Input**: `/do:it Fix the bug, then /do:chores`

**Analysis**:
- Pre-commands: none
- Main instructions: `Fix the bug`
- Post-commands: `/do:chores`

### Example 4: No Subcommands

**Input**: `/do:it Fix the login bug`

**Analysis**:
- Pre-commands: none
- Main instructions: `Fix the login bug`
- Post-commands: none

(Skill returns immediately, no SlashCommand calls needed)

## Edge Cases

### Self-Reference
If user includes the current command (e.g., `/do:it` within `/do:it`), skip it to avoid infinite loops.

### Ambiguous Ordering
When order is unclear, prefer:
- Exploration/research → pre
- Planning → pre
- Implementation → main
- Chores/cleanup → post
- Docs → post

### No Clear Main Instructions
If input is ALL commands with no clear main task:
```
/do:it /do:plan then /do:chores
```
Execute commands in order, main workflow gets empty/minimal instructions.

## Output

Return to parent command:
```
{
  "main_instructions": "The cleaned instruction string",
  "post_commands": ["/do:chores cleanup temp files"],
  "pre_commands_executed": ["/do:explore", "/do:plan"]
}
```

Or if no subcommands found:
```
{
  "main_instructions": "$ARGUMENTS (unchanged)",
  "post_commands": [],
  "pre_commands_executed": []
}
```
