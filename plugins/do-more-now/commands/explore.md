---
argument-hint: [question about the codebase]
description: Explore codebase - ask questions, compare ideas, understand internals. Internal only.
---

Explore the codebase. Internal-only - no external research.

<user-input>$ARGUMENTS</user-input>
<current-command>explore</current-command>

## Step 1: Route Subcommands (REQUIRED)

**Invoke `do:route-subcommands` skill FIRST.**

This skill will:
1. Analyze `$ARGUMENTS` for any `/do:*` commands
2. Execute pre-commands (commands that should run before main workflow)
3. Return `main_instructions` and `post_commands`

If no subcommands found, it returns immediately with `main_instructions = $ARGUMENTS`.

**Store the returned `post_commands` for later.**

---

## Step 2: Main Workflow

**Scope**: Codebase-only. Learn from internal sources, ask about the project, compare ideas within the project.

Use do:researcher in **explore mode** with `main_instructions`:

1. **Understand**: What/where/how is being asked?
2. **Search**: Grep/Glob to locate files quickly
3. **Read**: Examine key files
4. **Answer**: Respond concisely with `file:line` references

**Constraints**:
- Single-pass search for simple questions
- Multi-pass allowed for "compare" or "how does X relate to Y" questions
- Target: 30 seconds - 5 minutes depending on complexity

## Output

**Simple** (1-3 files): Answer inline with references
**Complex** (4+ files): EXPLORE-*.md with summary inline

## Redirects

- Needs external research → "Use `/do:research`"
- Needs correctness/status check → "Use `/do:plan status`"

---

## Step 3: Execute Post-Commands

If `post_commands` from Step 1 is non-empty, execute each one now using `SlashCommand` tool.
