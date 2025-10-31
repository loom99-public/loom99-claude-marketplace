---
name: design-implementation
description: Pixel-perfect UI implementation from design mockups or specifications. Use when building new UI components, implementing design systems, or translating visual designs into code.
---

# Design Implementation Skill

## Purpose

Transform visual design mockups into functional, pixel-accurate implementations using extracted specifications. This skill bridges the gap between static design and working code through systematic analysis and structured implementation.

## When to Use

- Implementing UI from design mockups or screenshots
- Building components based on visual specifications
- Converting prototypes to production code
- Developing design systems from mockup libraries

## Core Procedure

### Step 1: Analyze Mockup

Extract precise specifications before coding:

**Layout Structure**
- Identify positioning method (flexbox, grid, absolute)
- Map element hierarchy
- Document dimensions and constraints

**Visual Properties**
- Colors: Extract exact hex values
- Typography: Font family, sizes, weights, line-heights
- Spacing: Measure padding, margins, gaps
- Effects: Shadows, borders, opacity

**Interactive States**
- Hover, focus, active, disabled states
- Transitions and timing
- Error and validation states

### Step 2: Plan Implementation

**Technology Choice**
- Select framework based on project context
- Choose styling approach (CSS, Tailwind, CSS-in-JS)
- Define component structure

**Component Breakdown**
- Identify reusable patterns
- Plan file structure
- Define props and state needs

### Step 3: Implement Code

Write clean, semantic implementation:

**HTML Structure**
- Use semantic elements (form, button, label)
- Proper nesting and hierarchy
- Accessibility attributes (ARIA, labels)

**Styling**
- Apply exact extracted values
- Implement all interactive states
- Add responsive behavior if needed

**JavaScript Logic**
- Form handling and validation
- State management
- Event handlers

### Step 4: Verify Quality

**Code Quality**
- Semantic HTML structure
- Clean, readable code
- No console errors
- Proper error handling

**Visual Accuracy**
- Layout matches mockup
- Colors and typography exact
- Spacing consistent
- States working

## Key Principles

**Extract, Don't Guess**: Measure exact values from mockups. Use precise specifications, not approximations.

**Clean, Semantic Code**: Write production-quality markup. Use proper HTML elements, accessible patterns, maintainable structure.

**Framework-Agnostic Analysis**: Extract specifications first, then translate to chosen framework idioms.

**Iteration Expected**: Aim for 70-80% accuracy initially. Visual comparison will refine to pixel-perfect.

**Design Tokens**: Extract reusable values (colors, spacing scales) for design system consistency.

## Example

### Login Form Implementation (React + Tailwind)

**Mockup Analysis Output:**
```
Layout: Centered card, 400px width, flexbox centering
Colors: Primary #007BFF, Text #212529, Border #CED4DA, Focus #86B7FE
Typography: Inter font, Heading 32px/700, Body 16px/400, Labels 14px/500
Spacing: Container 24px padding, Fields 16px gap, Input 12px/16px padding
States: Focus (2px blue border), Hover (darker blue), Error (red border)
```

**Implementation:**
```tsx
import { useState } from 'react';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};

    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // Submit logic
    console.log('Submitting:', { email, password });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <form
        className="w-full max-w-[400px] p-6 bg-white rounded-lg shadow-[0_4px_12px_rgba(0,0,0,0.1)]"
        onSubmit={handleSubmit}
      >
        <h1 className="text-[32px] font-bold text-black mb-6">
          Sign In
        </h1>

        <div className="mb-4">
          <label className="block text-sm font-medium text-[#212529] mb-1.5">
            Email
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 text-base border border-[#CED4DA] rounded focus:outline-none focus:border-[#86B7FE] focus:border-2"
            placeholder="Enter your email"
          />
          {errors.email && (
            <span className="text-sm text-red-600 mt-1">{errors.email}</span>
          )}
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-[#212529] mb-1.5">
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 text-base border border-[#CED4DA] rounded focus:outline-none focus:border-[#86B7FE] focus:border-2"
            placeholder="Enter your password"
          />
          {errors.password && (
            <span className="text-sm text-red-600 mt-1">{errors.password}</span>
          )}
        </div>

        <button
          type="submit"
          className="w-full px-6 py-3 text-base font-semibold text-white bg-[#007BFF] rounded hover:bg-[#0056B3] active:scale-[0.98] transition-all duration-150"
        >
          Sign In
        </button>
      </form>
    </div>
  );
}
```

**Key Features:**
- Exact extracted values used (colors, spacing, typography)
- Semantic HTML (form, label, button)
- All interactive states (focus, hover, active, error)
- Clean component structure
- TypeScript for type safety
- Ready for screenshot comparison

**Plain HTML/CSS Version:**
```html
<div class="page-wrapper">
  <form class="login-form" id="loginForm">
    <h1 class="form-heading">Sign In</h1>

    <div class="form-group">
      <label for="email" class="form-label">Email</label>
      <input id="email" type="email" class="form-input" placeholder="Enter your email" required />
      <span class="form-error" id="emailError"></span>
    </div>

    <div class="form-group">
      <label for="password" class="form-label">Password</label>
      <input id="password" type="password" class="form-input" placeholder="Enter your password" required />
      <span class="form-error" id="passwordError"></span>
    </div>

    <button type="submit" class="submit-button">Sign In</button>
  </form>
</div>
```

```css
/* Extracted values applied */
.page-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #FFFFFF;
}

.login-form {
  width: 100%;
  max-width: 400px;
  padding: 24px;
  background-color: #FFFFFF;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.form-heading {
  font-size: 32px;
  font-weight: 700;
  color: #000000;
  margin: 0 0 24px 0;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  border: 1px solid #CED4DA;
  border-radius: 4px;
  transition: border-color 150ms;
}

.form-input:focus {
  outline: none;
  border-color: #86B7FE;
  border-width: 2px;
}

.submit-button {
  width: 100%;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  color: #FFFFFF;
  background-color: #007BFF;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 150ms;
}

.submit-button:hover {
  background-color: #0056B3;
}
```

## Anti-Patterns

❌ **Guessing Values**: Approximating colors or spacing leads to cumulative errors
✅ **Do**: Use color picker and measurement tools for exact values

❌ **Div Soup**: Using generic divs for everything
✅ **Do**: Use semantic elements (button, form, label, section)

❌ **Hardcoded Everywhere**: Inline values with no design tokens
✅ **Do**: Extract reusable values as variables or CSS custom properties

❌ **Skipping States**: Only implementing default appearance
✅ **Do**: Implement hover, focus, active, disabled, and error states

❌ **Over-Engineering**: Complex abstractions on first pass
✅ **Do**: Keep initial implementation simple, refactor during iteration

❌ **Ignoring Accessibility**: No labels, ARIA, or keyboard navigation
✅ **Do**: Use semantic HTML, proper labels, ARIA attributes

## Integration

**Visual Iteration Workflow Context:**
- **Stage 2**: This skill IS the implementation stage
- **Input**: Mockup analysis from Stage 1
- **Output**: Implementation files ready for Stage 3 (screenshot capture)
- **Next Step**: Screenshot comparison will identify refinements

**Works With:**
- screenshot-capture: Provides input for visual comparison
- visual-refinement: Receives refinement tasks based on comparison
- visual-comparison: Implementation is subject of comparison analysis

**Handoff:**
After implementation complete, transition to screenshot capture with summary of what was built, expected accuracy (70-80%), and list of created files.
