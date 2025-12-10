---
argument-hint: [question about the codebase]
description: Explore codebase - ask questions, compare ideas, understand internals. Internal only.
---

Explore the codebase. Internal-only - no external research.

<question>
$ARGUMENTS
</question>

## Subcommand Detection (REQUIRED)

**STOP. Check $ARGUMENTS for any `/do:` command references.**

If $ARGUMENTS contains `/do:plan`, `/do:it`, `/do:research`, `/do:chores`, `/do:docs`, or `/do:release`:
1. **IMMEDIATELY** use the SlashCommand tool to run that command first
2. Wait for it to complete
3. Then continue with this command's main workflow below

**Do NOT skip this step.**

---

## Scope

**Codebase-only**. Learn from internal sources, ask about the project, compare ideas within the project.

## Process

Use do:researcher in **explore mode**:

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
