---
argument-hint: [market|external] [topic] OR [technical question]
description: Research. Default is internal/technical. Use "market" or "external" prefix for web research.
---

Unified research command. Detects internal vs external from first word.

<research-topic>
$ARGUMENTS
</research-topic>

## Mode Detection

| First word | Mode | Action |
|------------|------|--------|
| `market` | Market research | Competitive landscape, demand signals, alternatives |
| `external` | External research | Web research on any topic |
| *(anything else)* | Internal research | Technical decisions, design ambiguities (codebase + docs) |

---

## Mode: Market Research

**Trigger**: `/do2:learn market [topic or empty]`

External research focused on competitive landscape and market viability.

**If no topic** (competitive analysis):
1. Read PROJECT_SPEC.md to understand project vision
2. Research: similar tools/projects, demand signals, approach comparison
3. Output: competitive landscape with opportunities/threats

**If topic specified**:
Research that specific market/external topic in context of the project.

**Process**:

**Step 1**: Gather project context from PROJECT_SPEC.md or CLAUDE.md.

**Step 2**: Use do2:researcher with web research enabled:
- Search for similar projects (open source and commercial)
- Assess demand (GitHub stars, downloads, discussions)
- Compare approaches
- Identify opportunities and threats

**Step 3**: Generate RESEARCH-market-<timestamp>.md

**Output**:
```
═══════════════════════════════════════
Market Research Complete
  Topic: [competitive analysis | specific topic]
  Alternatives found: [count]
  Key insight: [1-sentence summary]

  Report: RESEARCH-market-<timestamp>.md
Next: /do2:plan to incorporate findings
═══════════════════════════════════════
```

---

## Mode: External Research

**Trigger**: `/do2:learn external [topic]`

General web research on any topic, grounded in project context.

**Process**:

**Step 1**: Use do2:researcher with WebSearch/WebFetch enabled.

**Step 2**: Research the topic externally, ground findings in project context.

**Step 3**: Generate RESEARCH-<topic>-<timestamp>.md

---

## Mode: Internal Research (Default)

**Trigger**: `/do2:learn [technical question]`

Technical decisions, design ambiguities. Codebase + docs focused.

**Research Loop** (max 3 iterations):

**Step 1: Research**
Use do2:researcher to explore the problem:
- Gather context from codebase and project artifacts
- Identify all viable options
- Document tradeoffs specific to this project
- Form a recommendation

**Step 1b**: Display researcher's summary (options found, recommendation).

**Step 2: Evaluate**
Use appropriate evaluator to assess research sufficiency:
- Project-wide questions → do2:project-evaluator
- Focused questions → do2:work-evaluator

Verdict: SUFFICIENT or INSUFFICIENT

**Step 2b**: Display verdict and any gaps.

**Continue** if INSUFFICIENT and iteration < 3.
**Exit** if SUFFICIENT or iteration limit reached.

**Step 3: Decision**
If SUFFICIENT, evaluator chooses recommendation or alternative.

**Output**:
```
═══════════════════════════════════════
Research Complete
  Question: [summary]
  Iterations: n | Decision: [chosen option]
  Report: RESEARCH-<topic>-<timestamp>.md
Next: /do2:plan to incorporate into plan
═══════════════════════════════════════
```

---

## Difference Summary

| Invocation | Focus | Sources |
|------------|-------|---------|
| `/do2:learn [question]` | Technical decisions | Codebase, docs |
| `/do2:learn market [topic]` | Competitive landscape | Web search |
| `/do2:learn external [topic]` | Any external topic | Web search |
