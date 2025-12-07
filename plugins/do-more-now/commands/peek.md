---
argument-hint: [question about the codebase]
description: Fast codebase navigation for "where/how/what files" questions. Quick answers in 30s-2min.
---

Quick codebase exploration. Answers "where is X", "how does Y work", "what files do Z" questions.

<question>
$ARGUMENTS
</question>

## Purpose

Fast navigation and understanding of the codebase. Fills the gap between:
- Instant Claude answers (unstructured, may miss files)
- Full `/do:status` evaluation (2-5 min comprehensive diagnostic)

**Target time**: 30 seconds - 2 minutes
**Scope**: Codebase-only (no external research)

## When to Use

Good for:
- "Where is user authentication implemented?"
- "How does the payment flow work?"
- "What files are involved in database migrations?"
- "Is there a pattern for error handling here?"
- "What calls the X function?"

Not good for:
- "Should we use library A or B?" → Use `/do:learn`
- "Is the auth system working correctly?" → Use `/do:status auth`
- "What's the overall project status?" → Use `/do:status`

## Workflow

Use the do:researcher agent in **peek mode**.

**Peek mode constraints**:
1. **Single-pass search** - Find answer quickly, don't iterate
2. **Codebase-only** - No WebSearch, no WebFetch
3. **Fast exit** - If answer is clear, stop immediately
4. **Minimal output** - Inline answers preferred over files

**Search strategy**:
1. Use Grep/Glob to locate relevant files
2. Read key files to understand the pattern/location
3. Summarize findings concisely

## Output Format

**For simple queries (1-3 files)**:
Answer inline with file paths and brief explanation.

```
═══════════════════════════════════════
Peek: [question summary]

[Concise answer with file:line references]

Files: [list of relevant files]
═══════════════════════════════════════
```

**For complex queries (4+ files)**:
Create `PEEK-<topic>-<timestamp>.md` in `.agent_planning/` with:
- Answer summary
- File list with purposes
- Key code snippets if helpful

Then display:
```
═══════════════════════════════════════
Peek: [question summary]

[Brief answer]

Details: .agent_planning/PEEK-<topic>-<timestamp>.md
Files: [count] files identified
═══════════════════════════════════════
```

## Fast Exit Conditions

Exit immediately with brief response if:
- Question is too vague ("How does this work?" with no context)
- Question needs external research (redirect to `/do:learn`)
- Question is about correctness/quality (redirect to `/do:status`)
- Answer is trivially found in one file

## Workflow Progression

After `/do:peek`, users typically:
1. Read the identified files directly
2. Run `/do:status [area]` to evaluate if it's working
3. Run `/do:plan` to plan changes
4. Run `/do:it` to implement

## Example Questions

| Question | Answer Type |
|----------|-------------|
| "Where is auth?" | Inline (1-2 files) |
| "How does payment work?" | PEEK.md (flow across files) |
| "What uses the User model?" | PEEK.md (grep results) |
| "Is there a logger?" | Inline (yes/no + location) |
