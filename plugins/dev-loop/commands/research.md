---
argument-hint: [question or problem to research]
description: Research a problem or question through iterative exploration. Loops researcher->evaluator until sufficient, then auto-selects recommendation. Output feeds into /evaluate-and-plan.
---

Research a question or problem to produce a well-considered decision.

<research-question>
$ARGUMENTS
</research-question>

## Scope Selection

Determine scope based on the question:

- **Project-wide** (architecture, patterns, major decisions): Use project-evaluator for evaluation
- **Focused/specific** (implementation detail, concrete problem): Use work-evaluator for evaluation

Default to **focused** unless the question clearly affects project-wide architecture.

## Research Loop

Repeat until research is SUFFICIENT:

**Step 1: Research**
Use the dev-loop:researcher agent to explore the problem:
- Gather context from codebase and external sources
- Identify all viable options
- Document tradeoffs specific to this project
- Form a recommendation

**Step 1b: Display results** - Show researcher's summary (options found, recommendation) to user.

**Step 2: Evaluate**
Use the appropriate evaluator based on scope:
- **Project-wide**: dev-loop:project-evaluator (research evaluation mode)
- **Focused**: dev-loop:work-evaluator (research evaluation mode)

The evaluator assesses:
- Does research answer the actual question?
- Are options genuinely different and complete?
- Are tradeoffs specific to this project?
- Is the recommendation actionable?

Verdict: **SUFFICIENT** or **INSUFFICIENT**

**Step 2b: Display results** - Show evaluator's verdict and any gaps identified.

**Continue Condition**:
If INSUFFICIENT, provide evaluator's feedback to researcher and continue loop.

**Exit Condition**:
When evaluator returns SUFFICIENT, exit loop and proceed to decision.

## Decision Step

After loop exits with SUFFICIENT:

**Step 3: Make Decision**
Use the same evaluator to **choose** the recommendation:
- Review recommendation against project constraints
- Either ACCEPT recommendation or CHOOSE ALTERNATIVE with rationale
- Output a clear decision

**Step 3b: Display decision** - Show chosen option and rationale.

## Output Format

Generate decision output that feeds into /evaluate-and-plan:

```markdown
## Research Decision: [Topic]

**Question**: [Original question]
**Research**: RESEARCH-<topic>-<timestamp>.md

**Decision**: [Chosen option]
**Rationale**: [Why this fits the project]
**Tradeoffs Accepted**: [What we're giving up]

**Implementation Impact**:
- [How this affects existing code]
- [New components/patterns needed]
- [Files likely to change]

**Next**: /evaluate-and-plan to incorporate into project plan
```

## Final Summary

Display:
```
═══════════════════════════════════════
Research Complete
  Question: [summary]
  Iterations: n | Decision: [chosen option]
  Research: RESEARCH-<topic>-<timestamp>.md
Next: /evaluate-and-plan to create implementation plan
═══════════════════════════════════════
```

## Important Notes

- Research loop continues until evaluator is satisfied, removing user from iteration
- Evaluator auto-selects recommendation based on project fit
- Output is designed to feed directly into planning workflow
- Use project-evaluator for architectural questions, work-evaluator for specific technical questions
- Maximum 3 iterations to prevent infinite loops - if still INSUFFICIENT, surface to user
