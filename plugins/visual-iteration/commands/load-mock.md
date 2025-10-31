# Load Visual Mockup

Activates Stage 1 of visual-iteration-agent.md: Load design mockup and extract visual specifications.

## Purpose

Accept design mockup (image file, URL, or clipboard) and analyze to extract layout, colors, typography, and spacing specifications. This becomes the target for implementation.

## Workflow

### 1. Accept Mockup

Prompt user if mockup not provided:

```
Please provide your design mockup:

1. File path: /path/to/mockup.png (preferred)
2. Clipboard: Say "from clipboard" if copied
3. URL: https://example.com/mockup.png
4. Description: "It's in designs/ folder named login.png"
```

Accept any format and load accordingly:
- **File path**: Use Read tool
- **Clipboard**: Acknowledge clipboard access
- **URL**: Fetch from web
- **Description**: Use Glob to search, present options

### 2. Perform Visual Analysis

Once loaded, extract specifications:

```
🔍 ANALYZING MOCKUP

File: design-mockup.png
Resolution: 1920x1080
Format: PNG

EXTRACTION:
```

**Layout Structure**:
- Container type (card, full-page, split)
- Dimensions (width, height)
- Positioning (centered, left, right)
- Component hierarchy

**Color Palette**:
- Background colors (hex codes)
- Primary colors (buttons, links)
- Text colors (headings, body, labels)
- Border/divider colors

**Typography**:
- Font families (if identifiable)
- Heading sizes (px, estimate)
- Body text sizes
- Font weights (normal, bold, etc.)

**Spacing System**:
- Container padding
- Margins between elements
- Field gaps
- Button sizing

### 3. Document Findings

```
📋 MOCKUP SPECIFICATIONS

LAYOUT:
- Type: Centered card layout
- Card width: ~400px
- Card padding: ~32px
- Positioning: Vertically and horizontally centered

COLORS:
- Background: #FFFFFF (white)
- Button primary: #007BFF (blue)
- Text labels: #6C757D (gray)
- Input borders: #DEE2E6 (light gray)

TYPOGRAPHY:
- Heading: ~32px, bold (likely 700 weight)
- Labels: ~14px, normal (400 weight)
- Input text: ~16px, normal
- Button text: ~16px, semibold (600 weight)

SPACING:
- Container padding: ~32px all sides
- Field gaps: ~16px vertical
- Label-to-input gap: ~8px
- Button margin-top: ~24px

NOTES:
- Mobile responsive indicators: None visible (desktop layout)
- Interactive states: Not shown in static mockup
```

### 4. Clarify Technology Stack

```
🛠️ TECHNOLOGY CONFIRMATION

To implement this design, I'll need to know:

1. Framework preference?
   - React + Tailwind
   - Vue + CSS
   - Plain HTML/CSS
   - Other: [specify]

2. Responsive requirements?
   - Desktop only
   - Mobile-first responsive
   - Specific breakpoints

3. Accessibility needs?
   - Standard (ARIA labels, keyboard nav)
   - Enhanced (screen reader optimized)

Please confirm preferences, or I'll use React + Tailwind by default.
```

### 5. Transition to Implementation

```
✅ MOCKUP ANALYSIS COMPLETE

Specifications extracted and documented.

NEXT STEPS:
1. /implement-design - Generate initial implementation (80% accuracy)
2. /screenshot - Capture implementation for comparison
3. /compare - Identify differences
4. /iterate - Refine to pixel-perfect (2-3 cycles)
5. /visual-commit - Finalize and commit

Estimated timeline: 2-3 iteration cycles to pixel-perfect

Ready to proceed with implementation?
```

## Key Principles

1. **Extract, Don't Guess**: Use actual values from mockup, not assumptions
2. **Document Ranges**: Use ~ for estimates when exact values uncertain
3. **Note Ambiguities**: Flag areas needing clarification
4. **Technology Agnostic**: Specs work for any framework
5. **Set Expectations**: 80% on first implementation, iterate to 100%

## Anti-Patterns

❌ **Vague Analysis**: "Button looks blue"
✅ **Specific Analysis**: "Button #007BFF, ~16px text, semibold"

❌ **Skipping Analysis**: Jump to implementation without specs
✅ **Document First**: Extract all specs before coding

❌ **Perfect First Pass**: Expecting pixel-perfect from mockup alone
✅ **Iterative Approach**: Extract specs, implement 80%, refine via comparison

## Troubleshooting

**Mockup won't load**: Verify path, check permissions, try alternative method

**Low resolution**: Work with what's available, note limitations

**Multiple mockups**: Clarify which is current, load correct version

**Details unclear**: Document best estimates, refine in iteration cycles

## Success Criteria

- ✅ Mockup image loaded successfully
- ✅ Visual analysis performed (layout, colors, typography, spacing)
- ✅ Specifications documented with measurements
- ✅ Technology stack confirmed
- ✅ Ambiguities noted for clarification
- ✅ User ready to proceed to implementation

## Transition

**Next**: `/implement-design` (create initial UI matching these specs)

See visual-iteration-agent.md Stage 1 for full guidance.
