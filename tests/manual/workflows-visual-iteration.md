# visual-iteration Workflow Test Scenarios

Complete visual iteration workflow scenarios for the visual-iteration plugin testing screenshot-driven UI refinement cycles.

## Workflow 1: UI Component Refinement


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 25 minutes

### Setup
- Web application with UI component to refine (e.g., button styling)
- Browser available for screenshots
- Puppeteer installed (optional, for automation)

### Prerequisites
- Development server running
- UI component accessible in browser

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- Capture Initial State - Use `/screenshot`
   - Capture screenshot of current button state
   - Document current visual properties
   - Note areas needing refinement

- Get Specific Feedback - Use `/iterate`
   - Agent analyzes screenshot
   - Receives SPECIFIC feedback: "Button padding should be 16px instead of current 8px"
   - Gets CSS property recommendations
   - Identifies pixel-level discrepancies

- Make Refinements
   - Update CSS based on specific feedback
   - Reload page to see changes
   - Verify refinements applied correctly

- Capture Refined State - Use `/screenshot`
   - Capture new screenshot after refinements
   - Compare with initial state

- Iterate Again - Use `/iterate`
   - Get feedback on remaining issues
   - Make additional refinements
   - Typical 2-3 iteration cycles to pixel-perfect

- Final Comparison - Use `/compare`
   - Compare before/after states side-by-side
   - Verify all feedback addressed
   - Document visual improvements

- Commit - Use `/visual-commit`
   - Stage CSS changes
   - Include screenshots in commit
   - Commit with visual change description

### Expected Deliverables
- UI component visually refined
- 2-3 iteration cycles completed
- Before/after screenshots documenting improvement
- Git commit with visual changes

### Verification
- Verify visual improvements are measurable
- Verify feedback was specific (pixel values, CSS properties)
- Verify commit includes screenshots
- Verify CSS changes match feedback

## Workflow 2: Design Mockup Implementation


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 35 minutes

### Setup
- Design mockup file (PNG, Figma export, etc.)
- Empty or basic HTML template to implement design

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- Load Mockup - Use `/load-mock`
   - Load design mockup file
   - Document target visual specifications
   - Identify key measurements

- Implement Initial Design - Use `/implement-design`
   - Create HTML structure
   - Apply initial CSS
   - Get close to mockup appearance

- Capture Implementation - Use `/screenshot`
   - Screenshot current implementation
   - Prepare for comparison with mockup

- Get Refinement Feedback - Use `/iterate`
   - Agent compares implementation to mockup
   - Receives specific differences: "Header height should be 80px, currently 64px"
   - Gets detailed CSS adjustments needed

- Refine Implementation
   - Apply CSS adjustments from feedback
   - Make incremental improvements

- Iterate to Pixel-Perfect - Repeat `/screenshot` + `/iterate`
   - Continue refinement cycles
   - Aim for <5px differences from mockup
   - Typical 3-4 iterations needed

- Final Comparison - Use `/compare`
   - Compare implementation with original mockup
   - Verify pixel-perfect match achieved

- Commit - Use `/visual-commit`
   - Commit HTML/CSS implementation
   - Include mockup and screenshots

### Expected Deliverables
- Design mockup implemented in HTML/CSS
- Pixel-perfect match to mockup (within 5px)
- 3-4 iteration cycles documented
- Git commit with implementation

### Verification
- Verify implementation matches mockup visually
- Verify all measurements within tolerance (<5px)
- Verify responsive behavior if applicable

## Workflow 3: Multi-Component Visual Polish


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 40 minutes

### Setup
- Page with multiple components needing visual polish
- Examples: navigation bar, hero section, footer

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- Initial Screenshot - Use `/screenshot`
   - Capture full page state
   - Document all components

- Component-by-Component Iteration
   - For each component:
     - Use `/iterate` to get specific feedback
     - Make refinements
     - Use `/screenshot` to verify
   - Work through navigation, hero, footer

- Global Consistency Check - Use `/iterate`
   - Review overall page consistency
   - Check spacing, colors, typography across components
   - Get feedback on global visual harmony

- Final Polish - Use `/iterate`
   - Address any remaining visual issues
   - Ensure pixel-perfect consistency

- Complete Comparison - Use `/compare`
   - Compare initial vs final state
   - Document all improvements

- Commit - Use `/visual-commit`
   - Commit all visual refinements
   - Include comprehensive screenshots

### Expected Deliverables
- All page components visually polished
- Consistent visual language across components
- Comprehensive before/after documentation

### Verification
- Verify each component individually refined
- Verify global consistency maintained
- Verify commit documents all changes

## Feedback Specificity Testing

### Verify SPECIFIC Feedback in Iteration

For each workflow, verify agent provides:

✅ Specific measurements: "24px should be 32px"
✅ CSS properties: "border-radius should be 8px"
✅ Color values: "#333333 should be #000000"
✅ Numeric differences: "Currently 16px padding, should be 20px"

❌ Generic feedback: "Button looks too small"
❌ Vague suggestions: "Colors need work"

## Success Criteria

Visual iteration workflow testing is successful when:

- All 3 workflows complete with measurable visual improvements
- Feedback is consistently SPECIFIC (pixel values, CSS properties)
- Iteration typically converges in 2-3 cycles for simple components, 3-4 for complex
- Screenshots successfully captured (manual or automated)
- Visual improvements documented in git commits
- Before/after comparisons show clear progress
- Time estimates accurate within 25%
