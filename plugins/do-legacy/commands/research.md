---
argument-hint: [topic to research externally, or empty for competitive analysis]
description: External/market research - competitive landscape, viability assessment, approach comparison. No args = full competitive analysis of current project.
---

Research external sources to assess market viability, discover alternatives, and identify improvement opportunities.

<research-focus>
$ARGUMENTS
</research-focus>

## Determine Research Scope

**If no arguments provided** (competitive analysis mode):
1. Read PROJECT_SPEC.md or CLAUDE.md to understand project vision/goals
2. Frame research question as: "What similar tools/projects exist, what approaches do they take, how does this project compare, and what opportunities exist?"

**If arguments provided** (focused external research):
Use the provided topic directly, but frame it for external/market research context.

## Research Prompt Construction

Build the research prompt for the do:researcher agent:

**For competitive analysis** (no args):
```
Research the competitive landscape for this project.

Project context:
[Summary from PROJECT_SPEC.md - what it does, target users, key features]

Research questions:
1. What similar tools/projects exist? (open source and commercial)
2. How popular/in-demand are they? (GitHub stars, downloads, discussions, complaints about existing solutions)
3. What approaches do they take? (architecture, key features, UX patterns)
4. Where does this project differentiate or fall short?
5. What ideas are worth adapting? What gaps exist in the market?

Output a competitive landscape analysis with:
- Overview of alternatives (top 5-10)
- Demand signals (is there a market/need?)
- Approach comparison (how we differ)
- Opportunities (improvements, gaps we could fill)
- Threats (what competitors do better)

Focus on actionable insights - what should we consider incorporating?
```

**For focused research** (with args):
```
Research: [user's topic]

Project context:
[Brief summary from PROJECT_SPEC.md]

Research externally to find:
- How others approach this problem
- Best practices and common patterns
- Pitfalls and lessons learned
- Opportunities relevant to our project

Ground findings in our project context - what's applicable here?
```

## Execution

**Step 1: Gather project context**
- Read PROJECT_SPEC.md (or CLAUDE.md if no spec exists)
- Extract: project purpose, target users, key features, current approach

**Step 2: Invoke researcher**
Use do:researcher agent with the constructed prompt.
The researcher will use WebSearch and WebFetch to gather external information.

**Step 2b: Display results** - Show researcher's findings summary.

**Step 3: Evaluate**
Use do:project-evaluator to assess:
- Did research answer the questions?
- Are findings grounded in project context?
- Are recommendations actionable?

If INSUFFICIENT, iterate (max 2 times for external research - web results are what they are).

## Output

The researcher generates `RESEARCH-market-<timestamp>.md` or `RESEARCH-<topic>-<timestamp>.md`.

After research completes, display:

```
═══════════════════════════════════════
External Research Complete
  Topic: [competitive analysis | user's topic]
  Alternatives found: [count]
  Key insight: [1-sentence summary]

  Report: RESEARCH-<topic>-<timestamp>.md
Next: Review findings, /do:plan to incorporate
═══════════════════════════════════════
```

## Execution Summary (Final Step)

After all agents complete:
1. Read `.agent_planning/.exec/CURRENT_EXECUTION_ID.txt` to get execution ID
2. If exists, invoke do:execution-summarizer agent to aggregate PARTIAL files into an EXEC report
3. Display the executive summary from the generated EXEC report
4. Show file path to full report

**Display format**:
```
═══════════════════════════════════════
Execution Summary: <EXECUTION_ID>
  Agents: [count] | Duration: [approx]

[Executive summary from EXEC report - 2-3 sentences]

Full report: .agent_planning/EXEC-research-<timestamp>.md
═══════════════════════════════════════
```

If state files don't exist, skip this step (non-tracked execution).

## Difference from /do:learn

| Command | Focus | Primary Sources |
|---------|-------|-----------------|
| `/do:learn` | Technical decisions, design ambiguities | Codebase + docs |
| `/do:research` | Market viability, competitive landscape | Web search, external projects |

Use `/do:learn` for "how should we implement X?"
Use `/do:research` for "what else is out there and how do we compare?"
