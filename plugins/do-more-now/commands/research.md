---
argument-hint: [topic to research]
description: Research external sources - market analysis, competitors, external docs.
---

Research from external sources. Web search, market analysis, competitor comparison.

<research-topic>
$ARGUMENTS
</research-topic>

## Scope

**External-only**. Learn from web, compare with external tools/projects, market viability.

For internal codebase questions → Use `/do:explore`

## Intent Detection

| Intent signals | Workflow |
|----------------|----------|
| "market", "competitors", "alternatives", "demand" | Market research (competitive analysis) |
| "docs", "documentation", "how to use X" | External docs research |
| "best practices", "patterns", "how others do" | Industry research |
| *(default)* | General external research |

## Process

Use do:researcher in **external mode**:

1. **Search**: Web search for relevant sources
2. **Gather**: Collect information from multiple sources
3. **Compare**: Contrast with project context
4. **Synthesize**: Form recommendations with tradeoffs

## Output

```
═══════════════════════════════════════
Research Complete
  Topic: [summary]
  Sources: [count] external sources
  Report: RESEARCH-<topic>-<timestamp>.md
Next: /do:plan to incorporate findings
═══════════════════════════════════════
```
