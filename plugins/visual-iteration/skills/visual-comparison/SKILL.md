---
name: visual-comparison
description: Side-by-side visual comparison analysis identifying specific differences and generating actionable feedback. Use when comparing implementations to designs, before/after states, or cross-browser rendering.
---

# Visual Comparison Skill

## Purpose

Enable precise visual comparison between design mockups and implementations through structured AI analysis. Transforms subjective visual assessment into objective, actionable feedback with exact measurements for clear implementation guidance.

## When to Use

- Comparing implementation screenshot to design mockup
- Identifying specific visual differences and discrepancies
- Generating actionable feedback for iteration
- Validating pixel-perfect implementation accuracy

## Core Procedure

### Step 1: Load Both Images

Prepare images for comparison:
1. Verify mockup loaded (from Stage 1)
2. Verify screenshot loaded (from Stage 3)
3. Confirm both images visible and analyzable
4. Check quality sufficient (1280x720 minimum, PNG preferred)

If quality issues detected, request better images before proceeding.

### Step 2: Spawn Visual Comparison Subagent

Create specialized comparison subagent with structured prompt:

**Subagent Prompt Template:**
```markdown
You are a visual design comparison expert analyzing differences between mockup and implementation.

TASK: Compare these two images and identify SPECIFIC, MEASURABLE differences.

MOCKUP (target): [provide mockup image]
IMPLEMENTATION (current): [provide screenshot image]

ANALYZE FOUR DIMENSIONS:

1. LAYOUT: Element positions, dimensions, alignment, hierarchy
2. COLORS: Exact hex values for all colors
3. TYPOGRAPHY: Font families, sizes, weights, line-heights
4. SPACING: Margins, padding, gaps in px

OUTPUT FORMAT:

**[DIMENSION] FINDINGS:**

✓ **Matches:**
- [Element]: [value] correct ✓

✗ **Differences:**
- [Element]: Actual [A], should be [B], delta [±C]

EXAMPLES OF GOOD FEEDBACK:
✅ "Submit button width: 120px should be 140px (+20px)"
✅ "Heading color: #333333 should be #000000"
✅ "Container padding-top: 16px should be 24px (+8px)"

EXAMPLES OF BAD FEEDBACK:
❌ "Button too narrow" (no measurement)
❌ "Wrong color" (no hex values)
❌ "Needs more padding" (no specific value)

Analyze thoroughly and provide comprehensive, measurable feedback.
```

**Why Spawn Subagent:**
- Dedicated focus on visual analysis
- Structured prompt ensures consistent output
- Clean separation between analysis and synthesis
- Reusable pattern

### Step 3: Receive and Parse Analysis

Process subagent output:
1. Receive structured feedback by dimension
2. Parse matches and differences
3. Extract actionable items (✗ differences)
4. Verify feedback is specific and measurable
5. Flag vague feedback for clarification

**Quality Validation:**
- All differences have measurements (px, hex, numeric)
- Each issue has actual vs expected
- Delta values calculated
- Element identifiers clear

### Step 4: Synthesize Feedback

Organize feedback into clear sections:

**Format:**
```markdown
**LAYOUT FINDINGS:**
Matches (3): ✓ [items correct]
Issues (2): ✗ [specific problems with measurements]

**COLOR FINDINGS:**
Matches (2): ✓ [items correct]
Issues (3): ✗ [hex values actual vs expected]

**TYPOGRAPHY FINDINGS:**
Matches (3): ✓ [items correct]
Issues (4): ✗ [sizes, weights with deltas]

**SPACING FINDINGS:**
Matches (2): ✓ [items correct]
Issues (5): ✗ [padding, margins with deltas]

**OVERALL ASSESSMENT:**
- Matches: X items correct (Y%)
- Issues: X items need adjustment (Y%)
- Quality: [descriptive summary]
```

### Step 5: Provide Implementation Guidance

Translate findings into actionable code changes:

**Organize by Priority:**
1. High-impact layout issues
2. Color mismatches
3. Typography adjustments
4. Spacing refinements

**Format:**
```markdown
**IMPLEMENTATION GUIDANCE:**

1. Layout Adjustments:
   - [Specific change with exact values]
   - CSS: [property]: [value]

2. Color Fixes:
   - [Element]: Change #XXXXXX to #YYYYYY
   - CSS: [property]: #YYYYYY

3. Typography Updates:
   - [Element]: [size] → [new size]
   - CSS: [property]: [value]

4. Spacing Changes:
   - [Element]: [current] → [target] ([delta])
   - CSS: [property]: [value]
```

## Key Principles

**Specificity Over Vagueness**: Always provide measurable feedback with exact values (px, hex, numeric). Never "looks off" or "seems wrong".

**Four-Dimension Analysis**: Systematically analyze Layout, Colors, Typography, and Spacing. Cover all aspects, report all findings.

**Subagent-Driven**: Use dedicated comparison subagent for focused analysis. Structured prompt ensures consistent, quality output.

**Implementation Guidance Required**: Never provide feedback without solutions. State problem + measurements, provide fix + exact values, explain application, prioritize by impact.

**Positive + Negative**: Report what matches correctly AND what needs fixing. Acknowledge good work, focus on improvements.

## Example

### Comparison Analysis Output

**Scenario:** Login form implementation vs mockup

```markdown
**VISUAL COMPARISON RESULTS:**

**LAYOUT FINDINGS:**
Matches (3):
✓ Form container: 400px width, centered correctly
✓ Button: Centered horizontally
✓ Input fields: Full-width within container

Issues (2):
✗ Submit button position: 48px from bottom, should be 32px (-16px)
✗ Form container top margin: 64px should be 80px (+16px)

**COLOR FINDINGS:**
Matches (2):
✓ Text color: #212529 correct
✓ Border color: #DEE2E6 correct

Issues (3):
✗ Page background: #F8F9FA should be #FFFFFF
✗ Submit button: #0066CC should be #007BFF
✗ Input focus border: #80BDFF should be #86B7FE

**TYPOGRAPHY FINDINGS:**
Matches (3):
✓ Body text: 16px, weight 400, line-height 1.5 correct
✓ Font family: Inter applied correctly
✓ Button text: Weight 600 matches

Issues (2):
✗ Heading font size: 24px should be 32px (+8px)
✗ Input label size: 12px should be 14px (+2px)

**SPACING FINDINGS:**
Matches (2):
✓ Button padding: 12px 24px correct
✓ Input height: 44px matches

Issues (4):
✗ Container padding: 16px should be 24px (+8px all sides)
✗ Field margin-bottom: 12px should be 16px (+4px)
✗ Heading margin-bottom: 16px should be 24px (+8px)
✗ Button margin-top: 16px should be 24px (+8px)

**OVERALL ASSESSMENT:**
- Matches: 10 items (48%)
- Issues: 11 items (52%)
- Quality: Strong foundation, needs refinement in spacing and colors

**IMPLEMENTATION GUIDANCE:**

1. Layout Adjustments:
   - Reduce button bottom position by 16px
   - Increase container top margin by 16px

2. Color Fixes:
   - Page: background-color: #FFFFFF
   - Button: background-color: #007BFF
   - Input focus: border-color: #86B7FE

3. Typography Updates:
   - Heading: font-size: 32px (increase 8px)
   - Labels: font-size: 14px (increase 2px)

4. Spacing Changes:
   - Container: padding: 24px (increase 8px)
   - Fields: margin-bottom: 16px (increase 4px)
   - Heading: margin-bottom: 24px (increase 8px)
   - Button: margin-top: 24px (increase 8px)

**NEXT STEP:** Apply these changes and capture new screenshot for iteration 2.
```

## Anti-Patterns

❌ **Vague Feedback**: "Spacing looks off", "Colors don't match"
✅ **Do**: "Container padding: 16px should be 24px (+8px)"

❌ **No Measurements**: "Button too small", "Font too large"
✅ **Do**: "Button width: 120px should be 140px (+20px)"

❌ **Missing Context**: "#007BFF" without specifying which element
✅ **Do**: "Submit button background: #0066CC should be #007BFF"

❌ **Only Negatives**: List only problems, ignore correct items
✅ **Do**: Report matches AND differences for complete picture

❌ **No Implementation Guidance**: List problems without solutions
✅ **Do**: State problem + exact fix with CSS property and value

❌ **Relative Terms**: "Lighter", "bigger", "more space"
✅ **Do**: Exact deltas: "+8px", "-2px", "#ABC → #DEF"

## Integration

**Visual Iteration Context:**
- **Stage 4**: This skill performs the comparison analysis
- **Input**: Mockup (Stage 1) + Screenshot (Stage 3)
- **Output**: Specific feedback with measurements
- **Next**: Transition to refinement (Stage 5) with guidance

**Iteration Cycles:**
After each refinement, re-run comparison:
- Compare against original mockup (not previous screenshot)
- Track improvements ("11 issues → 6 issues")
- Focus feedback on remaining differences only
- Acknowledge fixes applied successfully

**Convergence Criteria:**
- Stop when ≤ 2 minor issues remain
- Typical cycles: 2-3 iterations to pixel-perfect
- Diminishing returns after 4+ iterations
- User satisfaction primary metric

**Works With:**
- screenshot-capture: Receives screenshot for comparison
- visual-refinement: Provides specific guidance for fixes
- design-implementation: Initial implementation based on mockup
