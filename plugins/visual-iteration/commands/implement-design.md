# Implement Design: Create Initial Implementation

Activates Stage 2 of visual-iteration-agent.md: Create initial UI implementation from mockup analysis.

## Purpose

Generate working UI code based on mockup analysis, matching visual specifications (layout, colors, typography, spacing) identified in Stage 1. Creates foundation for iterative refinement.

## Prerequisites

- Mockup loaded and analyzed (via `/load-mock`)
- Visual specifications extracted (colors, sizes, spacing)
- Technology stack confirmed (React, Vue, HTML/CSS)

Missing analysis? Run `/load-mock` first.

## Workflow

### 1. Review Mockup Specifications

```
📐 IMPLEMENTING FROM SPECIFICATIONS

Mockup: design-mockup.png
Target specs from analysis:
- Layout: Centered card, 400px width
- Colors: #007BFF button, #6C757D labels, #FFFFFF background
- Typography: 32px heading (bold), 14px labels, 16px inputs
- Spacing: 32px padding, 16px gaps

Framework: [React/Vue/HTML/CSS]
```

### 2. Generate Implementation Code

Create working code matching specifications:

**Focus on**:
- Structural layout (containers, positioning)
- Core colors (backgrounds, borders, text)
- Typography (sizes, weights, families)
- Spacing (padding, margins, gaps)

**Start with 80% accuracy** - don't aim for pixel-perfect on first pass.

### 3. Write Files

```
💾 CREATING IMPLEMENTATION

Writing files:
✅ [Component file: LoginForm.tsx/vue/html]
✅ [Styles: styles.css OR inline styles]
✅ [Assets: Any required imports]

Implementation ready for browser viewing.
```

### 4. Set up for Verification

```
✅ INITIAL IMPLEMENTATION COMPLETE

Files created:
- src/components/LoginForm.[tsx|vue]
- src/styles/login.css
- src/index.[tsx|html]

NEXT STEPS:
1. Start dev server if not running
2. View implementation in browser
3. Run /screenshot to capture current state
4. Run /compare to identify refinements needed

Expected: 60-80% match on first implementation
Refinement: 2-3 iteration cycles to reach pixel-perfect
```

## Key Principles

1. **80% Target**: Don't overthink first pass - refinement comes in iterations
2. **Working Code**: Must be functional, not just visually accurate
3. **Clean Structure**: Organized, readable code for easy refinement
4. **Framework Match**: Use conventions of user's chosen framework
5. **Accessibility**: Include ARIA labels, semantic HTML, keyboard nav
6. **Responsive**: Mobile-first, handle different viewports

## Example Implementation Structure

```jsx
// LoginForm.tsx (React + Tailwind)
export function LoginForm() {
  return (
    <div className="min-h-screen bg-white flex items-center justify-center">
      <div className="w-[400px] bg-white p-8 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold mb-8 text-gray-900">Sign In</h1>

        <form className="space-y-4">
          <div>
            <label className="text-sm text-[#6C757D] mb-2 block">Email</label>
            <input
              type="email"
              className="w-full h-[52px] border border-gray-300 rounded px-4"
            />
          </div>

          <div>
            <label className="text-sm text-[#6C757D] mb-2 block">Password</label>
            <input
              type="password"
              className="w-full h-[52px] border border-gray-300 rounded px-4"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-[#007BFF] text-white h-[48px] rounded font-semibold"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}
```

(Adapt to plain CSS, Vue, or other frameworks as needed)

## Anti-Patterns

❌ **Pixel-Perfect First Pass**: Spending hours on exact measurements
✅ **Good Enough**: Get 80% right, iterate to 100%

❌ **Broken Functionality**: Pretty but non-functional
✅ **Working Implementation**: Functions correctly from start

❌ **Messy Code**: Hard-to-modify structure
✅ **Clean Code**: Easy to refine in iterations

❌ **Ignoring Accessibility**: Visual only
✅ **Inclusive Design**: ARIA labels, keyboard nav, semantic HTML

## Troubleshooting

**Framework unclear**: Ask user for preference (React, Vue, plain HTML/CSS)

**Mockup details missing**: Use best judgment, note assumptions in comments

**Complex layout uncertain**: Start with simpler version, refine in iterations

**Assets not available**: Use placeholder colors/fonts, document in comments

## Success Criteria

- ✅ Working code generated and saved
- ✅ Matches mockup structure (layout correct)
- ✅ Core colors implemented (80% accuracy)
- ✅ Typography close (sizes approximate)
- ✅ Spacing reasonable (doesn't need to be exact)
- ✅ Functionality preserved (forms work, buttons click)
- ✅ Code is clean and modifiable
- ✅ User can view in browser

## Transition

**Next**: `/screenshot` (capture initial implementation for comparison)
**Then**: `/compare` → `/iterate` → refine to pixel-perfect

See visual-iteration-agent.md Stage 2 and design-implementation skill for full guidance.
