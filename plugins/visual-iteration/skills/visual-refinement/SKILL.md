---
name: visual-refinement
description: Iterative visual improvement through specific CSS and DOM refinements based on screenshot feedback. Use to achieve pixel-perfect results, fix visual bugs, or polish UI implementations.
---

# Visual Refinement Skill

## Purpose

Guide systematic iteration cycles that progressively improve visual accuracy from initial implementation (70-80% match) to pixel-perfect (95-100% match). Ensures focused, incremental refinements that avoid regression while closing the gap between implementation and mockup.

## When to Use

- After receiving specific feedback from visual comparison
- When implementation doesn't match mockup (3+ issues identified)
- During iteration cycles (Stage 5 of visual iteration workflow)
- When polishing UI to meet pixel-perfect standards

## Core Procedure

### Step 1: Review Comparison Feedback

Parse feedback into actionable items:

**Understand Current State:**
- Match quality percentage
- Number of issues by category
- Priority breakdown (P0/P1/P2/P3)

**Extract Actionable Items:**
```markdown
ACTIONABLE ITEMS FOR THIS ITERATION:

P0 - Layout (MUST FIX):
1. [Issue]: [current] → [target] ([delta])

P1 - Colors (HIGH PRIORITY):
2. [Issue]: [current hex] → [target hex]

Deferred to next iteration:
- P2 items
- P3 items
```

### Step 2: Prioritize Changes

Apply priority framework:

**P0 - Blocking Issues:**
- Layout structure problems (positioning, alignment)
- Missing critical elements
- Elements that obscure content
- **Fix first**: Establishes correct structure

**P1 - High Visibility Issues:**
- Primary colors (backgrounds, CTAs)
- Major typography (headings)
- High-contrast elements
- **Fix second**: Immediate visual impact

**P2 - Medium Impact Issues:**
- Secondary typography (labels, body)
- Fine spacing differences
- Minor color variations
- **Fix third**: Professional polish

**P3 - Polish Issues:**
- Subtle spacing (±2-4px)
- Micro-typography (line-height)
- Hover state refinements
- **Fix last**: Pixel-perfect finish

**Iteration Strategy:**
```markdown
ITERATION 1: P0 + P1 (5 issues)
Expected improvement: +20-30% match
Time: 15-20 minutes

ITERATION 2: P2 (4 issues)
Expected improvement: +10-15% match
Time: 10-15 minutes

ITERATION 3: P3 (remaining issues)
Expected improvement: +5-10% match
Time: 5-10 minutes
```

### Step 3: Apply Changes Systematically

Make changes one category at a time:

**For Each Issue:**
1. Identify exact CSS property to change
2. Locate file and line number
3. Update value to match target
4. Document change made
5. Verify no syntax errors

**Example Change Process:**
```markdown
FIXING: Submit button color

Current: background-color: #0066CC
Expected: background-color: #007BFF
File: src/components/Button.css line 24

Change applied:
- Before: background-color: #0066CC;
+ After: background-color: #007BFF;

Status: ✓ Complete, no errors
```

**Change Categories:**

**Layout Changes:**
- Position properties (top, left, bottom, right)
- Flexbox/Grid properties (justify-content, align-items)
- Width/Height dimensions
- Display properties

**Color Changes:**
- Background colors (background-color)
- Text colors (color)
- Border colors (border-color)
- Shadow colors (box-shadow)

**Typography Changes:**
- Font sizes (font-size)
- Font weights (font-weight)
- Line heights (line-height)
- Font families (font-family)

**Spacing Changes:**
- Margins (margin, margin-top, etc.)
- Padding (padding, padding-left, etc.)
- Gaps (gap, row-gap, column-gap)

### Step 4: Test and Verify

After applying changes:

**Local Verification:**
- Check browser console for errors
- Verify changes visible in browser
- Test interactive states (hover, focus)
- Confirm no regressions

**Screenshot Verification:**
1. Capture new screenshot (same viewport)
2. Return to comparison stage
3. Run comparison again
4. Validate improvements made
5. Identify remaining issues

**Track Progress:**
```markdown
ITERATION 1 RESULTS:

Before: 58% match (12 of 21 items)
After: 78% match (16 of 21 items)
Improvement: +20% (+4 items fixed)

Issues fixed: 5 (all P0 and P1)
Issues remaining: 9 (P2 and P3)

Next iteration: Focus on P2 typography (4 issues)
```

### Step 5: Decide Next Action

Evaluate convergence:

**Continue Iterating If:**
- Match quality < 95%
- 3+ issues remaining
- P0 or P1 issues exist
- User wants further refinement

**Stop Iterating If:**
- Match quality ≥ 95%
- ≤ 2 minor (P3) issues remaining
- User satisfied with result
- Diminishing returns (< 5% improvement)

**Typical Iteration Count:**
- 2-3 cycles: Most cases
- 1-2 cycles: Simple implementations
- 4+ cycles: Complex or highly detailed mockups

## Key Principles

**Prioritization is Critical**: Fix P0 (layout) and P1 (colors) first for maximum visual improvement. P2/P3 can wait.

**Focused, Incremental Changes**: One category at a time (all colors, then typography). Don't try to fix everything simultaneously.

**Iteration Cycles Expected**: Minimum 2-3 cycles for pixel-perfect. Don't expect perfection in one pass.

**Verify After Each Change**: Always capture screenshot and re-compare. Visual verification ensures progress and catches regressions.

**Never Change the Mockup**: Implementation must match mockup, not vice versa. Mockup is source of truth.

## Example

### Iteration Cycle

**Scenario:** Login form refinement after initial comparison

```markdown
ITERATION 1: REFINEMENT

**Starting State:**
- Match quality: 58% (12 of 21 items)
- Issues: 14 total (2 P0, 3 P1, 4 P2, 5 P3)

**Strategy:**
Focus on P0 + P1 (5 issues)
Target: 75-85% match

**Changes Applied:**

1. Layout: Submit button position
   - File: LoginForm.css line 45
   - Before: bottom: 48px;
   - After: bottom: 32px;
   - Status: ✓ Applied

2. Layout: Input field alignment
   - File: FormInput.css line 12
   - Before: padding-left: 8px;
   - After: padding-left: 16px;
   - Status: ✓ Applied

3. Color: Page background
   - File: App.css line 3
   - Before: background-color: #F8F9FA;
   - After: background-color: #FFFFFF;
   - Status: ✓ Applied

4. Color: Submit button
   - File: Button.css line 24
   - Before: background-color: #0066CC;
   - After: background-color: #007BFF;
   - Status: ✓ Applied

5. Color: Input placeholder
   - File: FormInput.css line 18
   - Before: color: #6C757D;
   - After: color: #ADB5BD;
   - Status: ✓ Applied

**Verification:**
- Browser: No console errors ✓
- Visual: All changes visible ✓
- Interactive: Focus states still work ✓

**Screenshot Captured:**
Returning to comparison stage for iteration 2 evaluation.

**Expected Result:**
75-85% match, 9 issues remaining (P2 and P3)
```

**Iteration 2 Preview:**
```markdown
ITERATION 2: PLANNED

Focus: P2 typography issues (4 items)
- Heading font size: 24px → 32px
- Input label size: 12px → 14px
- Input line-height: 1.3 → 1.5
- Button font weight: 500 → 600

Target: 88-93% match
```

## Anti-Patterns

❌ **Fixing Everything At Once**: Changing 14 items simultaneously
✅ **Do**: Fix 5 P0/P1 items, then iterate

❌ **Random Order**: Fixing P3 issues before P0
✅ **Do**: Follow priority order (P0 → P1 → P2 → P3)

❌ **No Verification**: Assuming changes worked, moving on
✅ **Do**: Capture screenshot and re-compare after each iteration

❌ **Changing Mockup**: "Let's adjust the design to match our implementation"
✅ **Do**: Implementation must match mockup exactly

❌ **Ignoring Regressions**: New issues introduced but not noticed
✅ **Do**: Check for regressions in each comparison

❌ **Infinite Iteration**: Continuing past 95% match for P3 issues
✅ **Do**: Stop when diminishing returns reached

## Integration

**Visual Iteration Context:**
- **Stage 5**: This skill applies refinements from comparison
- **Input**: Specific feedback from comparison (Stage 4)
- **Output**: Updated implementation files
- **Next**: Return to screenshot capture (Stage 3) for re-verification

**Iteration Loop:**
```
Refine (Stage 5) → Screenshot (Stage 3) → Compare (Stage 4) → Refine...
Stop when match ≥ 95% or user satisfied
```

**Typical Convergence:**
```
Iteration 1: 58% → 78% (+20%)
Iteration 2: 78% → 91% (+13%)
Iteration 3: 91% → 97% (+6%)
Stop: 97% is pixel-perfect
```

**Works With:**
- visual-comparison: Receives feedback, provides updated state
- screenshot-capture: Re-captures after refinements
- design-implementation: Refines initial implementation
