---
argument-hint: [question about the codebase]
description: Fast codebase navigation. "Where is X?", "How does Y work?", "What files handle Z?"
---

Fast codebase questions. Target time: 30 seconds - 2 minutes.

<question>
$ARGUMENTS
</question>

## Scope

**Codebase-only**. No external research, no evaluation, no planning.

**Good for**:
- "Where is user authentication implemented?"
- "How does the payment flow work?"
- "What files handle database migrations?"
- "Is there a pattern for error handling?"
- "What does function X do?"

**Not for** (redirect user):
- Decisions/tradeoffs → "Use `/do2:learn` for that"
- Correctness checks → "Use `/do2:plan status` for that"
- External research → "Use `/do2:learn market` for that"

## Process

Use do2:researcher in **peek mode**:

1. **Understand**: What/where/how is the user asking about?
2. **Search**: Use Grep/Glob to locate relevant files quickly
3. **Read**: Examine key files to confirm understanding
4. **Answer**: Respond concisely

**Constraints**:
- Single-pass search - don't iterate multiple times
- Fast exit - if answer is clear, stop immediately
- Minimal output - inline answers preferred

## Output

**Simple queries** (1-3 files): Answer inline with `file:line` references
```
Authentication is handled in:
- src/auth/login.ts:45 - main login logic
- src/auth/middleware.ts:12 - session validation
- src/routes/auth.ts:8 - route definitions
```

**Complex queries** (4+ files): Create PEEK-<topic>-<timestamp>.md with full details, display summary inline.

## Fast Exit Conditions

Stop immediately if:
- Question is too vague → Ask for clarification
- Question needs external research → "Use `/do2:learn` for external research"
- Question is about correctness → "Use `/do2:plan status` to check correctness"
- Answer found in one file → Just answer it
