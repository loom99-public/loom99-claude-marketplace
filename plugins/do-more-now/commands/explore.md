---
argument-hint: [question about the codebase]
description: Explore codebase - ask questions, compare ideas, understand internals.
---

Explore the codebase. Internal-only - no external research.

<question>
$ARGUMENTS
</question>

## Subcommand Detection

If $ARGUMENTS contains any `/do:` command reference (e.g., `/do:plan`, `/do:it`), run that command first with its relevant arguments, then continue with this command's main workflow.

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
