# Iterate: Refine Implementation Based on Feedback

Activates Stage 5 of visual-iteration-agent.md: Apply specific comparison feedback incrementally.

## Purpose

Apply measurable feedback from `/compare` to improve implementation toward pixel-perfect accuracy. Make focused changes prioritized by impact (P0 → P1 → P2 → P3), tracking iteration count and avoiding unrelated modifications.

## Prerequisites

- Comparison feedback available (run `/compare` first)
- Clear list of issues with measurements and priorities
- Current match quality known (e.g., 70%)

If no feedback: Run `/screenshot` → `/compare` first.

## Workflow

### 1. Review and Prioritize Feedback

```
📊 PRIORITIZING ISSUES

P0 (Layout structure): 3 issues
P1 (Colors, major spacing): 4 issues
P2 (Typography, medium spacing): 6 issues
P3 (Polish, details): 4 issues

Total: 17 issues to address
Approach: Fix P0 → P1 → P2 → P3
```

### 2. Apply Changes by Priority

Work through priorities systematically:

**P0 First** (structural):
- Fix layout positioning errors
- Correct element heights/widths
- Adjust structural margins

**P1 Next** (high visibility):
- Update colors to exact hex values
- Fix major spacing discrepancies

**P2 Then** (readability):
- Adjust typography (size, weight)
- Refine medium spacing

**P3 Last** (polish):
- Fine-tune gaps and margins
- Perfect micro-details

### 3. Write Changes and Verify

```
💾 SAVING CHANGES
✅ Updated: [implementation files]
Changes: [N] lines modified

✅ ITERATION CYCLE [N] COMPLETE
Changes: [X] applied (P0: X, P1: X, P2: X, P3: X)
Expected match: [70% → 85-90%]
```

### 4. Return to Verification

```
Ready for verification.
Refresh browser (Cmd+Shift+R), then:
- /screenshot (capture updated state)
- /compare (measure improvement)
- /iterate again OR /visual-commit (if ≥95%)
```

## Key Principles

1. **Focused Changes**: Apply ONLY what feedback specifies
2. **Priority Order**: Always P0 → P1 → P2 → P3
3. **No Refactoring**: Don't restructure unrelated code
4. **Track Progress**: Document iteration count and expected improvement
5. **Verify Always**: Return to /screenshot after every iteration
6. **Expect 2-3 Cycles**: Convergence path: 70% → 85% → 95% → 98-100%

## Example Changes

Changes adapt to your framework (Tailwind, CSS, CSS-in-JS):

**Layout** (P0):
```
Button position: 32px → 24px (move up 8px)
Input height: 48px → 52px (increase 4px)
```

**Colors** (P1):
```
Background: #F8F9FA → #FFFFFF
Button: #0066CC → #007BFF (exact hex)
```

**Typography** (P2):
```
Heading: 24px → 32px, weight 400 → 700
Labels: 12px → 14px
```

**Polish** (P3):
```
Label gaps: 4px → 8px
Margins: Fine-tune 2-4px adjustments
```

Apply to your CSS framework syntax (Tailwind classes, plain CSS, styled-components, etc.).

## Anti-Patterns

❌ **Ignoring Feedback**: Apply random changes not in comparison report
✅ **Follow Feedback**: Apply exactly the specified changes

❌ **Massive Refactoring**: Restructure entire component while fixing colors
✅ **Surgical Changes**: Modify only the properties that need adjustment

❌ **Skipping Verification**: Assume changes worked without screenshot
✅ **Always Verify**: Screenshot → Compare after every iteration

❌ **Settling for Close**: Commit at 85% match
✅ **Push for Excellence**: Iterate to 95-100% match

## Iteration Tracking

**Typical Convergence**:
- Cycle 1: 60-70% → 85-90% (major fixes)
- Cycle 2: 85-90% → 95-97% (refinements)
- Cycle 3: 95-97% → 98-100% (polish)

**If Stalled** (5+ cycles):
- Check if fundamental approach is wrong
- Consider if 92-95% is acceptable tolerance
- Discuss with user before continuing

## Troubleshooting

**Changes not visible**: Hard refresh (Cmd+Shift+R), check dev server, verify file saved

**Match decreased**: Revert changes, review what broke, fix carefully

**Functionality broke**: Rollback immediately, find alternative approach that preserves behavior

## Success Criteria

- ✅ All feedback reviewed and prioritized
- ✅ Changes applied in priority order (P0 → P3)
- ✅ Exactly what feedback specified (no more, no less)
- ✅ Iteration count tracked
- ✅ No regressions or broken features
- ✅ User instructed to verify via /screenshot

## Transition

**Next**: Return to `/screenshot` → `/compare`
**Loop**: Repeat until match ≥95%
**Finalize**: `/visual-commit` when pixel-perfect

See visual-iteration-agent.md Stage 5 for detailed guidance.
