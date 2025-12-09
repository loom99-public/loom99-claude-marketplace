---
argument-hint: [topic to research]
description: Research. Routes to market-research skill for external/market topics.
---

Research command. Detects internal vs external research.

<research-topic>
$ARGUMENTS
</research-topic>

## Intent Detection

| Intent signals | Skill to invoke |
|----------------|-----------------|
| "market", "competitors", "alternatives", "demand", "external" | `do3:market-research` |
| *(default - technical/internal research)* | Internal research workflow below |

**Use the Skill tool** for market research. Otherwise, run internal workflow.

---

## Default: Internal Research

Technical decisions, design ambiguities. Codebase + docs focused.

**Research Loop** (max 3 iterations):

**Step 1**: Use do3:researcher to explore:
- Gather context from codebase
- Identify options
- Document tradeoffs
- Form recommendation

**Step 2**: Use evaluator to assess sufficiency.
- Project-wide → do3:project-evaluator
- Focused → do3:work-evaluator

**Loop** until SUFFICIENT or 3 iterations.

**Step 3**: Evaluator makes decision.

**Output**:
```
═══════════════════════════════════════
Research Complete
  Question: [summary]
  Decision: [chosen option]
  Report: RESEARCH-<topic>-<timestamp>.md
Next: /do3:plan to incorporate
═══════════════════════════════════════
```
