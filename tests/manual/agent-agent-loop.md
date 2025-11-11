# agent-loop Agent Observation Checklist

Qualitative assessment checklist for observing the workflow-agent behavior during agent-loop plugin usage.

## Agent Identity and Purpose

**Agent Name:** workflow-agent
**Plugin:** agent-loop
**Purpose:** Guide users through 4-stage agentic software engineering workflow (Explore → Plan → Code → Commit)

## Observable Behaviors Checklist

### Stage Guidance Quality

- [ ] Does agent provide clear guidance at Explore stage?
- [ ] Does agent provide clear guidance at Plan stage?
- [ ] Does agent provide clear guidance at Code stage?
- [ ] Does agent provide clear guidance at Commit stage?
- [ ] Is guidance actionable with specific next steps?
- [ ] Does guidance reference relevant tools and commands?
- [ ] Is guidance consistent with plugin documentation?

### Stage Transition Communication

- [ ] Does agent clearly indicate when to move from Explore to Plan?
- [ ] Does agent clearly indicate when to move from Plan to Code?
- [ ] Does agent clearly indicate when to move from Code to Commit?
- [ ] Are transition triggers explained (e.g., "exploration complete when...")?
- [ ] Does agent prevent premature stage transitions?

### Anti-Pattern Detection and Blocking

Test these scenarios and verify agent blocks them:

- [ ] **Coding without a plan**: Does agent detect and prevent coding before planning?
- [ ] **Skipping exploration**: Does agent warn when implementing in unfamiliar code without exploration?
- [ ] **Committing without testing**: Does agent remind to run tests before committing?
- [ ] **Making large changes without planning**: Does agent require plan for significant work?

**For each blocked anti-pattern, does agent:**
- Explain why the action is inappropriate?
- Suggest correct workflow step?
- Provide helpful guidance to get back on track?

### Workflow Consistency

- [ ] Does agent maintain context across stages?
- [ ] Does agent remember earlier exploration findings during planning?
- [ ] Does agent reference the plan during implementation?
- [ ] Is agent guidance consistent throughout the workflow?

## Qualitative Assessment Questions

Answer these questions based on hands-on usage:

**Clarity:** Is agent guidance easy to understand and follow?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

**Effectiveness:** Does agent help complete workflows successfully?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

**Consistency:** Is agent behavior predictable and reliable?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

**Anti-Pattern Detection:** Does agent successfully prevent workflow violations?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

## Success Scenarios to Test

Test at least 3 successful workflows observing:

1. **Simple Feature Addition**
   - How well does agent guide through explore→plan→code→commit?
   - Are stage transitions smooth?
   - Is guidance helpful at each stage?

2. **Bug Fix Workflow**
   - Does agent help locate bug during exploration?
   - Does agent ensure proper debugging plan?
   - Does agent verify fix before commit?

3. **Refactoring Task**
   - Does agent ensure adequate exploration?
   - Does agent require careful planning for refactoring?
   - Does agent verify tests pass after refactoring?

## Overall Assessment

**Would you use this agent for real work?** Yes / No / Maybe
**Why or why not?**

**Most helpful agent behavior:**

**Least helpful agent behavior:**

**Suggestions for improvement:**

**Overall agent effectiveness rating:** Excellent / Good / Fair / Poor / Unusable
