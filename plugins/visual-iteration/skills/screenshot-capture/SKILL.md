---
name: screenshot-capture
description: Automated and manual screenshot capture of UI implementations using MCP browser tools or manual workflows. Use to document current state, create visual baselines, or capture specific viewport sizes.
---

# Screenshot Capture Skill

## Purpose

Enable reliable screenshot capture across different environments and tooling configurations. Provides automated capture via MCP servers when available, with graceful fallback to manual workflows.

## When to Use

- Capturing current implementation state for visual comparison
- Creating visual regression test baselines
- Verifying responsive behavior at different viewport sizes
- Generating screenshots for documentation

## Core Procedure

### Step 1: Detect Mode

Determine appropriate capture mode based on environment:

**Check for MCP Availability**
- browser-tools MCP: Lightweight browser automation
- playwright MCP: Full browser automation with multi-browser support
- No MCP or native app: Manual mode

**Decision Matrix**
- Web app + MCP available → Automated
- Web app + no MCP → Manual
- Native/desktop app → Manual
- User preference → Respect choice

### Step 2: Execute Capture (Automated)

**browser-tools MCP:**
1. Verify MCP availability
2. Ensure browser positioned at URL
3. Call `mcp__browser-tools__takeScreenshot`
4. Verify capture success
5. Load screenshot into context

**playwright MCP:**
1. Verify MCP availability
2. Navigate to URL: `browser_navigate`
3. Set viewport dimensions (optional)
4. Wait for rendering complete
5. Call `browser_take_screenshot`
6. Verify and load

### Step 3: Execute Capture (Manual)

**When Automated Unavailable:**
1. Inform user of manual mode and reason
2. Provide platform-specific instructions
3. Wait for user to provide screenshot path
4. Validate file exists and is readable
5. Load screenshot into context

**Platform Instructions:**
- macOS: ⌘ + ⇧ + 4 (area) or ⌘ + ⇧ + 3 (full screen)
- Windows: ⊞ + ⇧ + S (Snipping Tool)
- Linux: gnome-screenshot, spectacle, flameshot
- iOS Simulator: ⌘ + S
- Android Emulator: Camera icon or Volume Down + Power

### Step 4: Validate Quality

**Check Resolution:**
- Minimum: 1280x720
- Recommended: 1920x1080
- Mobile: 375x667 or 390x844

**Check Format:**
- Preferred: PNG (lossless)
- Acceptable: JPEG (quality 90+)
- Avoid: WebP, GIF, BMP

**Check Rendering:**
- All content loaded (no skeletons)
- All images loaded (no broken icons)
- All fonts loaded (no FOUT/FOIT)
- Animations in stable state
- No loading spinners

### Step 5: Load and Confirm

Load screenshot and confirm quality:
- Display resolution and format
- Describe visible content
- Confirm ready for comparison

## Key Principles

**Mode Flexibility**: Both automated and manual are first-class workflows. Choose based on scenario, not preference hierarchy.

**Quality Over Speed**: A clear, complete screenshot saves iteration time. Wait for full rendering before capture.

**Consistency Across Iterations**: Use same mode, viewport size, and zoom level for all captures in an iteration cycle.

**Graceful Fallback**: If automation fails, fall back to manual mode immediately. Document reason for fallback.

**Clear Communication**: When manual mode required, provide explicit instructions and wait for user confirmation.

**Environment Awareness**: Detect capabilities automatically but allow manual override when needed.

## Example

### Automated Capture (playwright)

**Scenario:** Web app on localhost, playwright MCP configured

```markdown
Screenshot Mode: Automated (playwright)

Step 1: Navigate to implementation
- URL: http://localhost:3000/login
- Browser: Chromium
- Wait: networkidle

Step 2: Set viewport
- Dimensions: 1920x1080
- Device pixel ratio: 1

Step 3: Wait for render
- Selector: .login-form
- Found: ✓

Step 4: Capture
- Full page: No (viewport only)
- Format: PNG

Screenshot captured:
- Resolution: 1920x1080
- Size: 287 KB
- Content: Login form with email/password fields, blue submit button

Ready for visual comparison.
```

### Manual Capture (iOS Simulator)

**Scenario:** iOS app, no MCP applicable

```markdown
Screenshot Mode: Manual

Implementation: iOS app in Simulator

Please capture screenshot:

1. Display login screen in Simulator
2. Press ⌘ + S
3. Screenshot saves to Desktop
4. Provide file path

Example: /Users/yourname/Desktop/Screen Shot 2024-01-15 at 10.30.45 AM.png

[User provides: /Users/bmf/Desktop/ios-login.png]

Screenshot loaded:
- Path: /Users/bmf/Desktop/ios-login.png
- Format: PNG
- Dimensions: 1170x2532 (iPhone 14 Pro)
- Size: 412 KB
- Content: iOS login screen with email, password fields, blue button

Ready for visual comparison.
```

### Fallback from Failed Automation

**Scenario:** playwright timeout, switching to manual

```markdown
Screenshot Mode: Automated (playwright)

Attempting automated capture...

⚠️ playwright failed:
Error: Navigation timeout of 30000ms exceeded

Falling back to manual mode.

Reason: Automation timed out (slow server or network issue)

Manual steps:
1. Open browser: http://localhost:3000/login
2. Verify page fully loaded
3. Capture screenshot:
   - Mac: ⌘ + ⇧ + 4
   - Windows: ⊞ + ⇧ + S
4. Provide file path

Waiting for screenshot path...
```

## Anti-Patterns

❌ **Capturing Too Soon**: Screenshot before content fully loaded
✅ **Do**: Wait for all resources, fonts, and images to load

❌ **Inconsistent Viewport**: Changing viewport size mid-iteration
✅ **Do**: Use same viewport for all captures in an iteration cycle

❌ **Low Quality**: JPEG with compression artifacts or low resolution
✅ **Do**: Use PNG at 1920x1080 or higher

❌ **Browser UI Included**: Chrome toolbar visible in screenshot
✅ **Do**: Capture implementation only, exclude browser chrome

❌ **No Validation**: Assuming screenshot is good without checking
✅ **Do**: Verify screenshot content and quality before proceeding

❌ **Forcing Automation**: Retrying failed automation indefinitely
✅ **Do**: Fall back to manual mode after 1-2 failed attempts

## Integration

**Visual Iteration Context:**
- **Stage 3**: This skill captures screenshot for comparison
- **Input**: Implementation files created, dev server running
- **Output**: Screenshot loaded and validated
- **Next**: Transition to comparison stage

**Iteration Cycles:**
After each refinement (Stage 5), return to screenshot capture:
- Use same mode as initial capture
- Use same viewport settings
- Verify changes visible before capturing
- Track iteration count ("Iteration 2 screenshot")

**Responsive Testing:**
Capture multiple viewports sequentially:
1. Desktop (1920x1080) → compare → iterate
2. Tablet (768x1024) → compare → iterate
3. Mobile (375x667) → compare → iterate

Each viewport is independent iteration cycle.

**Works With:**
- design-implementation: Captures output of implementation
- visual-comparison: Provides screenshot for comparison analysis
- visual-refinement: Captures state after refinements applied

## Quality Checklist

Before proceeding with captured screenshot:
- [ ] All content fully rendered (no loading states)
- [ ] Resolution meets minimum requirements
- [ ] Screenshot clearly shows implementation details
