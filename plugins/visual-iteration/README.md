# visual-iteration Plugin

Pixel-Perfect UI Development: **Design → Implement → Screenshot → Compare → Refine**

**Version**: 0.1.0 | **Status**: Production Ready | **License**: MIT

## Quick Start

```bash
# Install
/marketplace install visual-iteration

# Visual workflow
/load-mock               # Load design mockup
/implement-design        # Build from design specs
/screenshot              # Capture current state
/feedback                # AI visual analysis
/refine                  # Apply improvements
/iterate-loop            # Full iteration cycle
/visual-commit           # Finalize polished UI
/compare                 # Before/after comparison
```

## Five-Stage Visual Workflow

### 1. Design Analysis
Analyze mockup/design to extract specifications (colors, spacing, typography, layout).

**Command**: `/load-mock [path-to-mockup]`
**Output**: Detailed specifications (hex codes, pixel values, font properties)

---

### 2. Implementation
Build UI from extracted specifications. Aim for 70-80% accuracy initially.

**Command**: `/implement-design`
**Activities**: Write HTML/CSS/JS, apply exact values, build structure
**Exit**: Working implementation ready for screenshot

---

### 3. Screenshot Capture 📸
**Commands**: `/screenshot [mode]`

Capture current state via automated (MCP) or manual screenshot.

**Automated**: browser-tools MCP, playwright MCP
**Manual**: Platform screenshot tools (⌘⇧4 Mac, ⊞⇧S Windows)
**Exit**: Screenshot loaded and validated

---

### 4. Visual Comparison 🔍
**Command**: `/feedback`

AI-powered comparison: mockup vs screenshot. Generates specific, measurable feedback.

**Analyzes**:
- Layout (positions, dimensions, alignment)
- Colors (exact hex values)
- Typography (sizes, weights, line-heights)
- Spacing (margins, padding, gaps)

**Output**: Detailed differences with measurements
Example: "Button width: 120px should be 140px (+20px)"

---

### 5. Visual Refinement 🎨
**Commands**:
- `/refine [apply feedback]` - Single refinement pass
- `/iterate-loop` - Full feedback → refinement cycle

Apply specific improvements based on comparison feedback. Prioritize P0/P1 issues.

**Priority Levels**:
- P0 (Blocking): Layout structure, positioning
- P1 (High): Colors, major typography
- P2 (Medium): Spacing, secondary typography
- P3 (Polish): Subtle refinements

**Activities**: Update CSS/HTML, fix identified issues, re-screenshot
**Exit**: Improvements applied, ready for re-comparison

**Typical Convergence**: 2-3 iterations to pixel-perfect (95%+ match)

---

### 6. Finalize
**Commands**:
- `/visual-commit [what changed]` - Commit polished implementation
- `/compare` - Side-by-side before/after comparison

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/load-mock` | Load design mockup for analysis |
| `/implement-design` | Build initial implementation from specs |
| `/screenshot` | Capture current UI state |
| `/feedback` | AI comparison analysis |
| `/refine` | Apply specific improvements |
| `/iterate-loop` | Full feedback + refinement cycle |
| `/visual-commit` | Commit polished UI |
| `/compare` | Before/after comparison |

## Skills

- **design-implementation**: Pixel-perfect UI from mockups
- **screenshot-capture**: Automated/manual screenshot capture
- **visual-comparison**: AI-powered visual analysis
- **visual-refinement**: Iterative improvement to pixel-perfect

## MCP Integration

**Supported MCP Servers**:
- `browser-tools`: Lightweight browser automation
- `playwright`: Full browser automation

**Configuration** (.mcp.json):
```json
{
  "mcpServers": {
    "browser-tools": {
      "command": "npx",
      "args": ["-y", "browser-tools-mcp"]
    }
  }
}
```

## Iteration Workflow

```bash
# 1. Initial Implementation
/load-mock mockups/login.png
# Analyze: Extract colors, spacing, typography

/implement-design
# Build: Create HTML/CSS from specs (70% match expected)

# 2. First Iteration
/screenshot
# Captures state: 70% match

/feedback
# Analysis: 11 issues (2 P0, 3 P1, 4 P2, 2 P3)
# Focus: P0 + P1 (5 issues)

/refine
# Apply P0/P1 fixes

/screenshot
# New state: 85% match

# 3. Second Iteration
/feedback
# Analysis: 6 issues remaining (4 P2, 2 P3)

/refine
# Apply P2 fixes

/screenshot
# New state: 95% match

# 4. Final Polish
/feedback
# Analysis: 2 P3 issues remaining

/refine
# Apply final tweaks

/screenshot
# Final state: 98% match - pixel-perfect!

/visual-commit
# feat(ui): implement pixel-perfect login form
```

## Screenshot Modes

**Automated (browser-tools)**:
```javascript
// Triggered automatically when available
// Captures browser viewport
// Requires web server running
```

**Automated (playwright)**:
```javascript
// Multi-browser support
// Viewport configuration
// Wait for rendering
```

**Manual (Fallback)**:
- **macOS**: ⌘ + ⇧ + 4 (area) or ⌘ + ⇧ + 3 (full)
- **Windows**: ⊞ + ⇧ + S (Snipping Tool)
- **Linux**: gnome-screenshot, spectacle, flameshot
- **iOS Simulator**: ⌘ + S
- **Android Emulator**: Camera icon

## Feedback Format

**Example Output**:
```markdown
LAYOUT FINDINGS:
✓ Matches (3): Container width correct, button centered, fields full-width
✗ Issues (2):
  - Button position: 48px from bottom should be 32px (-16px)
  - Container margin: 64px should be 80px (+16px)

COLOR FINDINGS:
✓ Matches (2): Text #212529 correct, borders #DEE2E6 correct
✗ Issues (3):
  - Background: #F8F9FA should be #FFFFFF
  - Button: #0066CC should be #007BFF
  - Focus border: #80BDFF should be #86B7FE

TYPOGRAPHY FINDINGS:
✓ Matches (3): Body 16px correct, weight 400 correct, Inter applied
✗ Issues (2):
  - Heading: 24px should be 32px (+8px)
  - Labels: 12px should be 14px (+2px)

SPACING FINDINGS:
✗ Issues (4):
  - Container padding: 16px should be 24px (+8px)
  - Field spacing: 12px should be 16px (+4px)
  - Heading margin: 16px should be 24px (+8px)
  - Button margin: 16px should be 24px (+8px)

OVERALL: 48% match (10 of 21 items correct)
TARGET: Fix P0+P1 (5 issues) → expect 75-85% match
```

## Key Principles

**Specificity Over Vagueness**: Always provide exact measurements. "Button width: 120px should be 140px (+20px)" not "Button too narrow".

**Iterative Convergence**: 2-3 cycles typical. Iteration 1: 70%→85%, Iteration 2: 85%→95%, Iteration 3: 95%→98%.

**Prioritized Refinement**: Fix P0 (layout), then P1 (colors), then P2 (spacing), then P3 (polish). Don't fix everything at once.

**Four-Dimension Analysis**: Every comparison covers Layout, Colors, Typography, Spacing. Comprehensive coverage.

**Extract, Don't Guess**: Use exact values from mockups. Measure with tools, don't approximate.

## Typical Results

**Initial Implementation**: 70-80% match (expected)
**After Iteration 1**: 75-85% match (P0+P1 fixed)
**After Iteration 2**: 88-95% match (P2 fixed)
**After Iteration 3**: 95-100% match (pixel-perfect)

**Iteration Count**: 2-3 typical, 4+ for complex/detailed UIs

## Use Cases

**Landing Pages**: Pixel-perfect marketing pages from designs
**Component Libraries**: Build design system components
**UI Polish**: Refine existing implementations
**Responsive Design**: Test multiple viewports sequentially
**Cross-Browser**: Verify consistent rendering

## Integration

Works with:
- Any frontend framework (React, Vue, Angular, plain HTML/CSS)
- Any CSS methodology (Tailwind, styled-components, CSS modules)
- Design tools (Figma, Sketch exports)
- Responsive workflows (test desktop→tablet→mobile)
- Git workflows (commit visual milestones)

## Best Practices

1. **Extract Specs First**: Analyze mockup before implementing
2. **Accept Initial Imperfection**: 70-80% on first try is normal
3. **Iterate Systematically**: P0 → P1 → P2 → P3, don't randomize
4. **Screenshot Consistency**: Same mode, viewport, zoom throughout iteration
5. **Stop at Diminishing Returns**: 95%+ is pixel-perfect, don't over-iterate

## When to Use

**Use visual-iteration when**:
- Implementing from design mockups
- Pixel-perfect accuracy required
- Building design systems
- Polishing UI implementations
- Learning visual development

**Not suitable for**:
- Exploratory prototypes (no target design)
- Backend/API development
- Quick mockups/wireframes
- Purely functional code

## Anti-Patterns

❌ Guessing colors/spacing
❌ Fixing everything simultaneously
❌ Skipping screenshot verification
❌ Changing target mockup to match implementation
❌ Infinite iteration (>4 cycles)

✅ Extract exact specifications
✅ Prioritized, incremental fixes
✅ Screenshot after each change
✅ Implementation matches mockup
✅ Stop at 95%+ match

## Configuration

**Optional .mcp.json** (for automated screenshots):
```json
{
  "mcpServers": {
    "browser-tools": {
      "command": "npx",
      "args": ["-y", "browser-tools-mcp"]
    }
  }
}
```

Manual mode works without configuration.

## Support

- **Documentation**: See `skills/` directory
- **Issues**: GitHub repository
- **Author**: Brandon Fryslie
- **License**: MIT

## Version History

- **0.1.0** (Current): Initial release with full visual workflow
