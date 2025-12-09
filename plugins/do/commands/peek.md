---
argument-hint: [question about the codebase]
description: Fast codebase navigation. 30 seconds - 2 minutes.
---

Fast codebase questions. No skills needed - direct execution.

<question>
$ARGUMENTS
</question>

## Scope

**Codebase-only**. No external research, no evaluation, no planning.

## Process

Use do3:researcher in **peek mode**:

1. **Understand**: What/where/how is being asked?
2. **Search**: Grep/Glob to locate files quickly
3. **Read**: Examine key files
4. **Answer**: Respond concisely with `file:line` references

**Constraints**:
- Single-pass search
- Fast exit if answer is clear
- Target: 30 seconds - 2 minutes

## Output

**Simple** (1-3 files): Answer inline with references
**Complex** (4+ files): PEEK-*.md with summary inline

## Redirects

- Needs external research → "Use `/do3:learn`"
- Needs correctness check → "Use `/do3:plan status`"
