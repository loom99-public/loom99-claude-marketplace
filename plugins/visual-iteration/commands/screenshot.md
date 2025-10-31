# Screenshot: Capture Implementation State

Activates Stage 3 of visual-iteration-agent.md: Capture current UI state for visual comparison.

## Purpose

Capture screenshot of current implementation for comparison with mockup. Use browser automation (MCP browser-tools) if available, or manual screenshot workflow.

## Prerequisites

- Implementation exists and is viewable in browser
- Dev server running (if applicable)
- Browser displaying current state

## Workflow

### 1. Choose Screenshot Method

**Option A: Automated (MCP browser-tools)**
```
🤖 AUTOMATED SCREENSHOT

Using browser-tools MCP server...
- URL: http://localhost:3000
- Viewport: 1920x1080
- Wait for: Page load complete

Capturing screenshot...
```

**Option B: Manual**
```
📸 MANUAL SCREENSHOT GUIDE

1. Open browser to implementation
2. Set viewport to mockup size (e.g., 1920x1080)
3. Take screenshot (full viewport)
4. Save as: implementation-screenshot.png
5. Provide file path when ready

Waiting for screenshot path...
```

### 2. Capture Screenshot

Use appropriate method:

**Automated**:
- Invoke browser-tools MCP
- Navigate to localhost URL
- Set viewport size
- Capture and save

**Manual**:
- Guide user through process
- Wait for file path
- Load image when provided

### 3. Verify Screenshot Quality

```
✅ SCREENSHOT CAPTURED

File: implementation-screenshot.png
Resolution: 1920x1080
Size: 245 KB
Viewport: Desktop

Quality check:
✓ Full page visible
✓ No browser chrome (clean screenshot)
✓ Resolution matches mockup
✓ Content fully loaded

Ready for comparison with mockup.
```

### 4. Prepare for Comparison

```
📊 READY FOR VISUAL COMPARISON

IMAGES IN CONTEXT:
Target (mockup): design-mockup.png
Actual (screenshot): implementation-screenshot.png

NEXT ACTION: /compare
- AI will analyze both images
- Identify specific differences
- Generate actionable refinement guidance

Expected differences on first screenshot: 15-25 issues
After iterations: Converge to 0-3 issues
```

## Key Principles

1. **Match Viewport**: Screenshot should match mockup dimensions
2. **Clean Capture**: No browser UI, dev tools, or artifacts
3. **Complete Render**: Wait for page fully loaded
4. **Consistent Zoom**: 100% zoom, no browser scaling
5. **Same State**: Capture neutral state (no hovers, focus, etc.)

## Screenshot Best Practices

**Good Screenshot**:
- Full viewport visible
- 100% zoom level
- Clean (no dev tools)
- Content fully rendered
- Matching mockup dimensions

**Poor Screenshot**:
- Partial content
- Zoomed in/out
- Browser UI visible
- Loading spinners present
- Different viewport size

## Automated vs Manual

**Use Automated (MCP browser-tools) when**:
- browser-tools MCP server configured
- Implementation hosted locally (localhost:XXXX)
- Consistent screenshot timing needed

**Use Manual when**:
- MCP not available
- Complex auth/state required
- Special browser conditions needed
- User prefers manual control

## MCP Browser-Tools Example

```javascript
// If browser-tools available:
const screenshot = await browserTools.screenshot({
  url: 'http://localhost:3000',
  viewport: { width: 1920, height: 1080 },
  waitUntil: 'networkidle',
  fullPage: false
});
```

See .mcp.json and MCP documentation for setup.

## Anti-Patterns

❌ **Wrong Viewport**: Screenshot 375px mobile when mockup is 1920px desktop
✅ **Match Dimensions**: Same viewport size as mockup

❌ **Partial Capture**: Only part of UI visible
✅ **Full Capture**: Complete UI in viewport

❌ **Browser Chrome**: Dev tools, address bar visible
✅ **Clean Screenshot**: Only implementation, no browser UI

❌ **Loading State**: Spinners, skeleton screens
✅ **Fully Rendered**: Complete, stable content

## Troubleshooting

**MCP not working**: Fall back to manual screenshot workflow

**Screenshot different size**: Adjust browser viewport, retake

**Content not loaded**: Wait longer, check network tab, refresh

**Can't access localhost**: Verify dev server running, check port

## Success Criteria

- ✅ Screenshot captured successfully
- ✅ Dimensions match mockup
- ✅ Quality sufficient for comparison (clear, sharp)
- ✅ Full UI visible
- ✅ No artifacts or browser chrome
- ✅ Image loaded into context for comparison

## Transition

**Next**: `/compare` (analyze mockup vs screenshot to identify refinements)
**Loop**: After `/iterate`, return to `/screenshot` to verify changes
**Typical**: 3-4 screenshots total (initial + 2-3 iterations)

See visual-iteration-agent.md Stage 3 and screenshot-capture skill for full guidance.
