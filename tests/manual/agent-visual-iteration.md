# visual-iteration Agent Observation Checklist

Qualitative assessment checklist for observing the visual-iteration-agent behavior during visual-iteration plugin usage.

## Agent Identity and Purpose

**Agent Name:** visual-iteration-agent
**Plugin:** visual-iteration
**Purpose:** Guide pixel-perfect UI implementation through screenshot-driven iterative refinement cycles

## Observable Behaviors Checklist

### Feedback Specificity

- [ ] Does agent provide SPECIFIC pixel measurements (e.g., "24px should be 32px")?
- [ ] Does agent provide CSS property recommendations?
- [ ] Does agent provide color values with hex codes?
- [ ] Does agent avoid generic feedback like "looks too small"?
- [ ] Is feedback actionable and implementable?

### Iteration Tracking

- [ ] Does agent track iteration count (cycle 1, 2, 3, etc.)?
- [ ] Does agent indicate convergence progress?
- [ ] Does agent suggest when iteration goal is achieved (typically 2-3 cycles)?
- [ ] Does agent detect when no progress is being made?

### Visual Analysis Quality

- [ ] Does agent analyze screenshots effectively?
- [ ] Does agent identify visual discrepancies?
- [ ] Does agent prioritize most important issues?
- [ ] Does agent provide comprehensive vs piecemeal feedback?

### Workflow Guidance

- [ ] Does agent guide screenshot capture process?
- [ ] Does agent explain when to iterate vs when to commit?
- [ ] Does agent coordinate before/after comparisons?
- [ ] Does agent integrate visual work with git workflow?

### MCP Browser Automation (if available)

- [ ] Does agent successfully trigger Puppeteer automation?
- [ ] Does agent handle automation gracefully if unavailable?
- [ ] Does agent provide fallback to manual screenshots?

## Anti-Pattern Detection

Test these scenarios and verify agent response:

- [ ] **Generic feedback provided**: Does agent self-correct to specific measurements?
- [ ] **Infinite iteration loop**: Does agent suggest convergence after 3-4 cycles?
- [ ] **No visual changes between iterations**: Does agent question if refinements applied?
- [ ] **Skipping screenshot capture**: Does agent require screenshots before feedback?

## Feedback Specificity Testing

For at least 5 visual issues, verify feedback format:

**Issue 1:**
- Generic version: "Button too small"
- Agent's specific version: [Record agent's actual feedback]
- Contains measurements? Yes / No

**Issue 2:**
- Generic version: "Spacing off"
- Agent's specific version: [Record agent's actual feedback]
- Contains CSS properties? Yes / No

**Issue 3:**
- Generic version: "Colors wrong"
- Agent's specific version: [Record agent's actual feedback]
- Contains hex values? Yes / No

## Qualitative Assessment Questions

**Feedback Specificity:** Does agent consistently provide pixel-level specific feedback?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

**Iteration Effectiveness:** Do iterations converge to pixel-perfect in 2-3 cycles?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

**Visual Analysis:** Does agent accurately identify visual issues?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

**Workflow Integration:** Does visual iteration integrate well with development workflow?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

## Visual Iteration Scenarios to Test

Test at least 3 visual refinement workflows:

1. **Button Styling Refinement**
   - How specific is feedback on padding, border-radius, etc.?
   - How many iterations to pixel-perfect?
   - Is feedback consistently actionable?

2. **Layout Implementation from Mockup**
   - Does agent provide detailed comparison to mockup?
   - Are measurements accurate?
   - Does iteration converge to match?

3. **Multi-Component Visual Polish**
   - Does agent maintain context across components?
   - Does agent ensure global consistency?
   - Does feedback prioritize correctly?

## Iteration Convergence Tracking

**Component 1:**
- Iteration 1 feedback: [Key issues identified]
- Iteration 2 feedback: [Remaining issues]
- Iteration 3 feedback: [Final polish or achieved]
- Total iterations to pixel-perfect: ___

**Component 2:**
- Iteration 1 feedback: [Key issues identified]
- Iteration 2 feedback: [Remaining issues]
- Iteration 3 feedback: [Final polish or achieved]
- Total iterations to pixel-perfect: ___

## Overall Assessment

**Does agent provide pixel-perfect feedback?** Yes / No / Sometimes
**Why or why not?**

**Most valuable agent capability:**

**Biggest gap in visual iteration support:**

**Suggestions for improvement:**

**Overall visual iteration agent effectiveness:** Excellent / Good / Fair / Poor / Unusable
