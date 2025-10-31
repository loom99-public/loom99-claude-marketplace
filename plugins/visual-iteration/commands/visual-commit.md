# Visual Commit: Finalize Pixel-Perfect Implementation

Activates Stage 6 of visual-iteration-agent.md: Finalize and commit pixel-perfect UI implementation.

## Purpose

Verify user satisfaction, document iteration journey, create comprehensive commit message, and execute git workflow to finalize visual iteration work.

## Prerequisites

- Visual match ≥95% OR user explicitly satisfied
- Final comparison completed
- No broken functionality
- All iteration cycles complete

If not ready: Continue `/iterate` or fix issues before committing.

## Workflow

### 1. Verify Final State

```
🎯 FINAL VERIFICATION

Visual match quality: 98%
Iteration cycles: 3
Outstanding issues: 0
Functionality: Working ✓

MATCH BREAKDOWN:
✓ Layout: 100% (±1px tolerance)
✓ Colors: 100% (exact hex)
✓ Typography: 100% (sizes/weights match)
✓ Spacing: 100% (±2px tolerance)

READY TO COMMIT?
1. Satisfied with visual match?
2. Implementation functions correctly?
3. Any intentional deviations to document?

Reply "yes" to commit or provide final feedback.
```

**Wait for confirmation** before proceeding.

### 2. Document Iteration Journey

```
📊 ITERATION SUMMARY

Starting point: 60% match, 24 issues
Cycle 1: 60% → 85% (17 changes: layout, colors)
Cycle 2: 85% → 95% (8 changes: typography, spacing)
Cycle 3: 95% → 98% (3 changes: micro-adjustments)

Final: 98% match, pixel-perfect accuracy
Total changes: 28 applied across 3 cycles
```

### 3. Note Intentional Deviations

If any deliberate differences from mockup:

```
📝 INTENTIONAL DEVIATIONS

1. Button hover state: Added subtle lift effect (not in mockup)
   Reason: Better UX, modern convention

2. Form validation: Red border on error (not in mockup)
   Reason: Essential functionality, user clarity
```

### 4. Generate Commit Message

```
feat(ui): implement pixel-perfect login form from design mockup

Implemented login form matching mockup.png with 98% visual accuracy
achieved through 3 iteration cycles.

Visual Implementation:
- Layout: Centered card, 400px width, responsive padding
- Colors: #007BFF button, #6C757D labels, #FFFFFF background
- Typography: Inter font, 32px heading (bold), 14px labels
- Spacing: 32px container padding, 16px field gaps

Iteration Journey:
- Cycle 1 (60% → 85%): Fixed layout structure, major colors
- Cycle 2 (85% → 95%): Refined typography, spacing
- Cycle 3 (95% → 98%): Micro-adjustments for pixel perfection

Technical Notes:
- Framework: [React/Vue/HTML/CSS]
- Responsive: Mobile-first, breakpoints at 768px
- Accessibility: ARIA labels, focus states, keyboard navigation

Intentional Deviations:
- Added hover states for better UX (not in static mockup)
- Enhanced focus indicators for accessibility

Match Quality: 98% (within ±1-2px tolerance)
Files: src/components/LoginForm.[tsx|vue], src/styles/login.css

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### 5. Stage and Commit

```
📋 STAGING FILES

git status
git add [implementation files]
git commit -m "[message from step 4]"
```

See agent-loop/skills/git-operations for detailed git workflow guidance.

### 6. Verify Commit

```
✅ COMMIT SUCCESSFUL

Commit: abc123f
Files: 2 changed, 85 insertions
Branch: feature/login-form-implementation

git log -1 --stat
[Shows commit details]
```

### 7. Completion Summary

```
✅ VISUAL ITERATION WORKFLOW COMPLETE

FINAL RESULTS:
- Visual accuracy: 98%
- Iterations: 3 cycles
- Changes: 28 total
- Quality: Pixel-perfect ✓

DELIVERABLE:
- Implementation matches mockup
- Functionality preserved
- Code committed to git
- Documentation complete

WORKFLOW STAGES COMPLETED:
✅ Stage 1: Mockup loaded
✅ Stage 2: Implementation created
✅ Stage 3: Screenshots captured (4x)
✅ Stage 4: Comparisons performed (3x)
✅ Stage 5: Iterations applied (3x)
✅ Stage 6: Committed to git

Next: Push to remote, create PR, or start next feature.
```

## Key Principles

1. **User Confirmation**: Always get explicit satisfaction before committing
2. **Document Journey**: Include iteration summary in commit message
3. **Note Deviations**: Explain intentional differences from mockup
4. **Comprehensive Message**: Detail what, why, and how (not just "updated UI")
5. **Verify Functionality**: Ensure nothing broke during iterations
6. **Git Best Practices**: Follow conventional commits, stage correctly

## Commit Message Template

```
feat(scope): short description (imperative mood)

Detailed description of what was implemented and why.

Visual Implementation:
- [Key visual characteristics]

Iteration Journey:
- [Summary of cycles and improvements]

Technical Notes:
- [Framework, approach, considerations]

Intentional Deviations:
- [Any deliberate differences from mockup]

Match Quality: [N]%
Files: [list]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Anti-Patterns

❌ **Committing Without Confirmation**: Auto-commit without asking user
✅ **Get Confirmation**: Wait for explicit "yes" before proceeding

❌ **Vague Message**: "updated UI" or "fixed styling"
✅ **Detailed Message**: Comprehensive description with iteration journey

❌ **Skipping Iteration Summary**: No context on refinement process
✅ **Document Journey**: Show progression from initial to final state

❌ **Committing Broken Code**: Visual perfect but functionality broken
✅ **Verify Function**: Test all interactions before committing

## Troubleshooting

**Git commit fails**: Check git status, verify staged files, check pre-commit hooks

**User not satisfied**: Return to `/iterate`, apply final adjustments, re-verify

**Files not staged**: Use `git add` for correct implementation files, check gitignore

**Pre-commit hook fails**: Fix linting/formatting issues, re-commit

## Success Criteria

- ✅ User confirmed satisfaction
- ✅ Iteration journey documented
- ✅ Intentional deviations noted
- ✅ Comprehensive commit message generated
- ✅ Files staged correctly
- ✅ Git commit executed successfully
- ✅ No functionality broken
- ✅ Match quality ≥95% (or user satisfied)

## Transition

**Workflow Complete**: Visual iteration cycle finished
**Next Actions**: Push to remote, create PR, start new feature, or deploy

See visual-iteration-agent.md Stage 6 and agent-loop/skills/git-operations for full guidance.
