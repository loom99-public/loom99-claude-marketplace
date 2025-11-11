# visual-iteration Command Test Scenarios

Test scenarios for all 6 visual iteration commands in the visual-iteration plugin.

## Command Test Matrix

| Command | Purpose | Expected Content |
|---------|---------|------------------|
| /screenshot | Capture UI state | Screenshot capture guidance (manual/automated) |
| /implement-design | Implement from design | Design implementation methodology |
| /iterate | Visual refinement cycle | Specific feedback, CSS/pixel guidance |
| /visual-commit | Commit visual work | Visual work commit workflow |
| /compare | Before/after comparison | Comparison methodology, diff analysis |
| /load-mock | Load design mockups | Mockup loading and reference guidance |

## Test Scenario: /screenshot

**Purpose:** Verify screenshot capture guidance

**Steps:**
- Type `/screenshot` and press Enter
- Observe prompt expansion

**Expected:**
- Comprehensive screenshot capture guidance (800+ lines)
- Both manual and automated approaches
- Puppeteer/browser-tools integration guidance
- Image analysis preparation
- No errors

**Error Scenarios:**

| Scenario | Expected Behavior |
|----------|-------------------|
| /screenshot without browser automation | Should fall back to manual screenshot guidance |
| Typo: /screen | Command not found |

## Test Scenario: /implement-design

**Purpose:** Verify design implementation guidance

**Steps:**
- Type `/implement-design` and press Enter
- Observe prompt expansion

**Expected:**
- Guidance on implementing from mockups/designs
- HTML/CSS implementation strategies
- Responsive design considerations
- No errors

## Test Scenario: /iterate

**Purpose:** Verify visual refinement guidance

**Steps:**
- Type `/iterate` and press Enter
- Observe prompt expansion

**Expected:**
- Visual iteration cycle guidance
- SPECIFIC feedback format (e.g., "24px should be 32px")
- CSS property recommendations
- Pixel-perfect refinement strategies
- Typical 2-3 iteration cycle guidance
- No errors

**Error Scenarios:**

| Scenario | Expected Behavior |
|----------|-------------------|
| /iterate without screenshot | Should prompt to capture screenshot first |
| /iterate with generic feedback | Agent should provide specific pixel/CSS values |

## Test Scenario: /visual-commit

**Purpose:** Verify visual work commit guidance

**Steps:**
- Type `/visual-commit` and press Enter
- Observe prompt expansion

**Expected:**
- Visual work commit workflow
- Screenshot inclusion in commit
- Visual changes documentation
- No errors

## Test Scenario: /compare

**Purpose:** Verify before/after comparison guidance

**Steps:**
- Type `/compare` and press Enter
- Observe prompt expansion

**Expected:**
- Side-by-side comparison methodology
- Visual diff analysis
- Progress tracking
- No errors

**Error Scenarios:**

| Scenario | Expected Behavior |
|----------|-------------------|
| /compare without multiple screenshots | Should guide on capturing before/after states |

## Test Scenario: /load-mock

**Purpose:** Verify mockup loading guidance

**Steps:**
- Type `/load-mock` and press Enter
- Observe prompt expansion

**Expected:**
- Mockup/design file loading guidance
- Reference image handling
- Target specification guidance
- No errors

## Complete Visual Iteration Workflow Test

**Execute full iteration cycle:**

- Use `/screenshot` to capture current UI state
- Use `/iterate` to get specific visual feedback
- Make refinements based on specific feedback
- Use `/screenshot` again to capture refined state
- Use `/compare` to see before/after differences
- Repeat iteration 2-3 times for pixel-perfect result
- Use `/visual-commit` to finalize visual work

**Expected:**
- All 6 commands work in sequence
- Screenshot capture works (manual or automated)
- Agent provides SPECIFIC feedback (pixel values, CSS properties)
- Iteration converges in 2-3 cycles
- Visual improvements are measurable
- Workflow integrates with git

## Feedback Specificity Testing

### Verify Specific vs Generic Feedback

**Agent should provide:**
- ✅ "Button padding should be 16px instead of 12px"
- ✅ "Border radius should be 8px, currently appears to be 0"
- ✅ "Font size should be 18px, currently 14px"
- ❌ "Button looks too small" (too generic)
- ❌ "Colors need adjustment" (too vague)

**Test Steps:**
- Use `/iterate` after capturing screenshot
- Observe feedback specificity
- Verify feedback includes actual measurements

## Negative Test Scenarios

### Invalid Commands

| Invalid Command | Expected |
|----------------|----------|
| /screen | Not found error |
| /visual | Ambiguous or not found |
| /commit | May conflict with agent-loop (should be /visual-commit) |

### Workflow Issues

| Issue | Expected Agent Behavior |
|-------|------------------------|
| Skip screenshot capture | Agent prompts to capture screenshot first |
| Generic feedback provided | Agent should self-correct to specific measurements |
| Infinite iteration loop | Agent should suggest convergence after 3-4 cycles |
| No visual changes between iterations | Agent should question if refinements were applied |

## MCP Browser Automation Testing

### Test Automated Screenshot Capture

**Prerequisites:**
- browser-tools MCP server configured
- Puppeteer installed

**Steps:**
- Request automated screenshot via `/screenshot`
- Verify browser automation triggers
- Confirm screenshot captures successfully

**Expected:**
- Browser launches automatically
- Screenshot captured via Puppeteer
- Falls back to manual if automation unavailable

**Error Scenarios:**

| Scenario | Expected Behavior |
|----------|-------------------|
| Puppeteer not installed | Graceful fallback to manual screenshots |
| Browser automation fails | Clear error message, manual fallback offered |

## Success Criteria

- All 6 commands accessible via autocomplete
- Each command provides comprehensive visual guidance
- Agent provides SPECIFIC feedback (pixel values, CSS properties)
- Screenshot capture works (manual and/or automated)
- Complete iteration workflow (screenshot→iterate→refine→compare→commit) executes successfully
- Iteration typically converges in 2-3 cycles
- MCP browser-tools integration works (if available)
- Negative tests handle errors appropriately
