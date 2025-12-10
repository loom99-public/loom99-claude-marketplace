---
argument-hint: [topic to research]
description: [market|docs|patterns] Research external sources - market analysis, competitors, external docs.
---

Research from external sources. Web search, market analysis, competitor comparison.

<user-input>$ARGUMENTS</user-input>
<current-command>research</current-command>

## Subcommand Detection

**Quick check**: Does `$ARGUMENTS` contain `/do:` patterns?

- **If NO** → `main_instructions = $ARGUMENTS`, proceed
- **If YES** → Invoke `do:route-subcommands` skill first

---

## Main Workflow

**Scope**: External-only. Learn from web, compare with external tools/projects, market viability.

For internal codebase questions → Use `/do:explore`

### Intent Detection

Using `main_instructions`:

| Intent signals | Action |
|----------------|--------|
| "market", "competitors", "alternatives", "demand", "landscape" | Invoke `do:market-research` skill |
| "docs", "documentation", "how to use X" | Use do:researcher (external docs) |
| "best practices", "patterns", "how others do" | Use do:researcher (industry research) |
| *(default)* | Use do:researcher (general external) |

**Use the Skill tool** for market-research. Otherwise continue with do:researcher below.

### Process (for non-market research)

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

## Post-Commands

If subcommands were detected and `post_commands` is non-empty, execute them now.
