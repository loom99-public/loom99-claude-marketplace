---
argument-hint: [topic to research]
description: [market|docs|patterns] Research external sources - market analysis, competitors, external docs.
---

Research from external sources. Web search, market analysis, competitor comparison.

<user-input>$ARGUMENTS</user-input>
<current-command>research</current-command>

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

**Scope**: External-only. Learn from web, compare with external tools/projects, market viability.

For internal codebase questions → Use `/do:explore`

### Intent Detection

Using `main_instructions`:

| Intent signals | Workflow |
|----------------|----------|
| "market", "competitors", "alternatives", "demand" | Market research (competitive analysis) |
| "docs", "documentation", "how to use X" | External docs research |
| "best practices", "patterns", "how others do" | Industry research |
| *(default)* | General external research |

### Process

Use do:researcher in **external mode**:

1. **Search**: Web search for relevant sources
2. **Gather**: Collect information from multiple sources
3. **Compare**: Contrast with project context
4. **Synthesize**: Form recommendations with tradeoffs

### Output

```
═══════════════════════════════════════
Research Complete
  Topic: [summary]
  Sources: [count] external sources
  Report: RESEARCH-<topic>-<timestamp>.md
Next: /do:plan to incorporate findings
═══════════════════════════════════════
```

---

## Step 3: Execute Post-Commands

If `post_commands` from Step 1 is non-empty, execute each one now using `SlashCommand` tool.
