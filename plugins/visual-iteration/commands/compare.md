# Visual Comparison: Mockup vs Implementation

Activates Stage 4 of visual-iteration-agent.md: AI-powered visual analysis between mockup and implementation.

## Purpose

Analyze mockup (target) and screenshot (actual) using AI vision to identify SPECIFIC, MEASURABLE differences across layout, colors, typography, and spacing. Provide exact measurements (px, hex codes) and actionable guidance.

## Prerequisites

- Mockup loaded (via `/load-mock`)
- Implementation created (via `/implement-design`)
- Screenshot captured (via `/screenshot`)
- Both images in context

Missing images? Run prerequisite commands first.

## Workflow

### 1. Confirm Comparison Context

```
🔍 VISUAL COMPARISON ANALYSIS

TARGET (Mockup): design-mockup.png (1920x1080)
ACTUAL (Screenshot): implementation-screenshot.png (1920x1080)

Viewport match: ✓
Proceeding with four-dimensional analysis...
```

### 2. Perform Pixel-Level Analysis

Use AI vision to compare images across four dimensions:

**LAYOUT** (structural positioning):
- Element positions (absolute px from edges)
- Heights and widths
- Alignment and distribution
- Container dimensions

**COLORS** (exact values):
- Background colors (hex codes)
- Text colors (hex codes)
- Border colors (hex codes)
- Shadow values (rgba)

**TYPOGRAPHY** (text properties):
- Font sizes (px)
- Font weights (100-900)
- Line heights (px or unitless)
- Letter spacing (px or em)

**SPACING** (margins and padding):
- Container padding (top, right, bottom, left)
- Margins between elements
- Gaps in flex/grid layouts
- Border widths

### 3. Generate Specific Feedback

Output format with EXACT measurements:

```
📊 COMPARISON RESULTS

OVERALL MATCH: 70%

DIFFERENCES DETECTED: 17

P0 - LAYOUT (3 issues):
❌ Submit button position
   Mockup: 24px from bottom
   Actual: 32px from bottom
   Delta: -8px (move up)

❌ Email input height
   Mockup: 52px
   Actual: 48px
   Delta: +4px (increase)

P1 - COLORS (4 issues):
❌ Page background
   Mockup: #FFFFFF
   Actual: #F8F9FA
   Delta: Change to pure white

❌ Button color
   Mockup: #007BFF
   Actual: #0066CC
   Delta: Update hex code

P2 - TYPOGRAPHY (6 issues):
❌ Heading size
   Mockup: 32px
   Actual: 24px
   Delta: +8px

❌ Heading weight
   Mockup: 700 (bold)
   Actual: 400 (normal)
   Delta: Make bold

P3 - SPACING (4 issues):
❌ Container padding
   Mockup: 32px
   Actual: 24px
   Delta: +8px

[...more specific issues]
```

### 4. Prioritize and Summarize

```
📋 IMPLEMENTATION GUIDANCE

PRIORITY BREAKDOWN:
P0 (Blocking): 3 layout issues - fix first
P1 (High visibility): 4 color issues - fix second
P2 (Readability): 6 typography issues - fix third
P3 (Polish): 4 spacing details - fix last

PROJECTED ITERATION PATH:
Current: 70% match, 17 issues
After Cycle 1: 85-90% match, ~8 issues
After Cycle 2: 95-97% match, ~3 issues
After Cycle 3: 98-100% match, pixel-perfect

NEXT ACTION: /iterate (apply these 17 changes systematically)
```

## Key Principles

1. **Specificity**: Never "button is wrong" - always "button is 32px, should be 24px"
2. **Measurements**: Exact values (px, hex, numeric) not descriptions
3. **Priorities**: Categorize as P0 (layout), P1 (colors), P2 (typography), P3 (spacing)
4. **Deltas**: Show difference direction (+/-) and magnitude
5. **Actionable**: Each issue directly translates to code change
6. **Honest**: Don't downplay issues, accurate match percentage

## Example Comparison Output

```
LAYOUT: 85% match
✓ Overall structure correct (centered card)
❌ Button 8px too low
❌ Input heights inconsistent

COLORS: 60% match
❌ Background #F8F9FA should be #FFFFFF
❌ Button #0066CC should be #007BFF
✓ Border colors match
❌ Label color #868E96 should be #6C757D

TYPOGRAPHY: 70% match
❌ Heading 24px should be 32px
❌ Heading weight 400 should be 700
✓ Body font correct (14px)
❌ Button weight 400 should be 600

SPACING: 75% match
❌ Container padding 24px should be 32px
✓ Field gaps correct (16px)
❌ Label-input gap 4px should be 8px
```

## Anti-Patterns

❌ **Vague Feedback**: "Colors seem off"
✅ **Specific Feedback**: "Button #0066CC should be #007BFF"

❌ **No Measurements**: "Heading is too small"
✅ **Exact Values**: "Heading 24px should be 32px (+8px)"

❌ **Missing Priorities**: Random list of issues
✅ **Categorized**: P0 layout, P1 colors, P2 typography, P3 spacing

❌ **Dishonest Assessment**: "Looks good!" when 50% match
✅ **Accurate Assessment**: "70% match, needs refinement"

## Troubleshooting

**Images not comparable**: Check resolutions match, same viewport size

**Too many differences**: Expected on first comparison (15-25 issues typical)

**Match percentage unclear**: Base on visual similarity, not exact pixels (±1-2px tolerance)

**Can't identify colors**: Use color picker tools, extract hex from images

## Success Criteria

- ✅ Both images analyzed in detail
- ✅ Specific measurements for every difference
- ✅ Deltas calculated (+/- values)
- ✅ Issues prioritized (P0-P3)
- ✅ Match percentage estimated
- ✅ Actionable guidance generated
- ✅ User ready to /iterate with clear targets

## Transition

**Next**: `/iterate` (apply comparison feedback systematically)
**Loop**: After iteration, return to `/screenshot` → `/compare` → `/iterate`
**Finalize**: When match ≥95%, proceed to `/visual-commit`

See visual-iteration-agent.md Stage 4 and visual-comparison skill for full guidance.
