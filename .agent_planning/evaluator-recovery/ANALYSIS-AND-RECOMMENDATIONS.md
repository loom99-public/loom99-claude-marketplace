# Evaluator Recovery: Analysis and Recommendations

**Generated**: 2025-12-10
**Purpose**: Analyze what was lost in the "lean" evaluator changes and provide recommendations for a consolidated approach

---

## Executive Summary

The evaluator optimization effort started with good intentions but went sideways in several key areas:

1. **Gates were deprioritized**: The second plan (PLAN-2025-12-09-051425.md.archived) had excellent gate specifications (P1-1) but these were abandoned in the "lean" version
2. **Over-emphasis on "lean"**: The third plan removed too much useful content in pursuit of token efficiency
3. **Lost specificity**: Detailed validation guidance was replaced with "see skill" references, reducing effectiveness
4. **Critical skill usage pattern ignored**: Subagents cannot ask questions directly - they must use a SKILL to gate/pause, which was never addressed

### Key Files Recovered

**Plans** (in chronological order):
1. `PLAN-2025-12-09-040520.md` - Initial optimization plan (profile integration, duplication removal)
2. `PLAN-2025-12-09-051425.md.archived` - Effectiveness plan with gates, validation debt, confidence levels
3. `PLAN-2025-12-09-054129.md` - Lean plan that over-stripped content

**Evaluators** (in chronological order):
- `00_ORIGINAL_*` - Before any optimization (rich, detailed, ~395 and ~374 lines)
- `01_d9cb966_*` - After profile integration
- `02_043e660_*` - Added "not verified" section
- `03_4bb075c_*` - Elevated "runtime trumps tests"
- `04_4baa246_*` - Removed automation recommendations, added test quality rubric
- `05_HEAD_*` - Current state (~347 and ~350 lines)

---

## What Was Lost

### 1. Detailed Test Assessment Section (CRITICAL)
**Original** (lines 54-83):
```markdown
### 3. Test Suite Assessment
**Don't trust passing tests. Evaluate the tests themselves.**

#### Test Quality Scoring Rubric
| Question | Yes | No |
|----------|-----|-----|
| If I delete the implementation and leave stubs, do tests fail? | Good | **WORTHLESS TESTS** |
| If I introduce an obvious bug, do tests catch it? | Good | **BLIND SPOT** |
| Do tests exercise real user flows end-to-end? | Good | **COVERAGE GAP** |
| Do tests use real systems or mock everything? | Good | **FALSE CONFIDENCE** |
| Do tests cover error conditions users will hit? | Good | **HAPPY PATH ONLY** |

#### Test the Tests
Actually try this:
1. Find a critical function
2. Make it return a wrong value or throw an error
3. Run the tests
4. **If tests still pass, the tests are worthless**

Document which tests are real vs. theater.
```

**Current** (line 66-80): Shortened version that lost 2 key rows from rubric ("real systems vs mocks", "error conditions") and removed explicit instructions to "actually try this".

### 2. Detailed LLM Blind Spots (SIGNIFICANT)
**Original** had expanded descriptions for each blind spot:
- Pagination: "Page 1 works, but what about page 2? Page 100? Empty list? Single item? Thousands?"
- State: "Second run when data exists? After restart? Concurrent access?"
- Cleanup: "Temp files? Connections closed? Event listeners? Memory leaks?"
- Error Messages: "Generic vs helpful? Internal details exposed?"
- Edge Cases: "Empty string vs null? Zero vs negative? Timezones? Unicode?"

**Current**: Condensed to brief categories with "see skill" references. The specific questions that prompt thinking were removed.

### 3. Implementation Red Flags Detail (MODERATE)
**Original** had two categories:
- "Fake completeness" (TODO/FIXME, placeholders, silent error swallowing, hardcoded returns)
- "Test-specific cheating" (code paths only in tests, env checks, hardcoded test values)
- "Over-engineering" (abstractions without purpose)

**Current**: "See evaluation-profiles skill" with a quick grep pattern.

### 4. Assessment Protocol Steps (SIGNIFICANT)
**Original** (lines 175-194): Clear 6-step process
1. Run It First
2. Follow the Data
3. Test the Tests
4. Check Blind Spots
5. Hunt for Ambiguity
6. Code Inspection

**Current** (lines 128-137): Reduced to 5 vague steps with profile references.

### 5. Never-Implemented Features from PLAN-2025-12-09-051425.md

These were planned but abandoned:

#### P1-1: Workflow Gates (CRITICAL - YOUR TOP PRIORITY)
```markdown
- Gate 1: Critical Issues Resolved (no P0/P1 bugs, no BROKEN features)
- Gate 2: Validation Confidence Threshold (VERIFIED+LIKELY >= 60%)
- Gate 3: Manual Debt Bounded (<=5 items, no HIGH >3 days)
- Gate 4: No Active PAUSE

Modes: BLOCKING (must pass), ADVISORY (warn), DISABLED (no gates)
```

#### P0-2: Confidence Level Markers
```markdown
- ✅ VERIFIED (ran it, works)
- ✅ LIKELY (tests pass, code reasonable)
- ⚠️ UNCERTAIN (can't verify)
- ❌ BROKEN (ran it, fails)
- ❓ UNKNOWN (not evaluated)
```

#### P1-2: VALIDATION_DEBT.md Ledger
Tracking manual validation items across sessions.

---

## What Was Gained (Keep These)

1. **"Runtime Evidence First" section** (lines 39-46 in current): Good addition, prominent placement
2. **"What Could Not Be Verified" section** in STATUS template: Transparency improvement
3. **Evaluation profiles integration**: Good efficiency gain for profile-specific validation
4. **Compressed feedback examples**: Token efficiency without losing pedagogical value

---

## Critical Missing Piece: Subagent Question Mechanism

**The Problem**: Subagents (like evaluators) cannot ask questions directly to users. They run autonomously and return results.

**What Was Planned** (PLAN-2025-12-09-051425.md, P1-1):
> "Commands (/do:it) accept `--gates=blocking|advisory|disabled` parameter"
> "If `--gates` not specified, command prompts user"

**What's Actually Needed**:
When an evaluator needs to PAUSE or has questions requiring user input:

1. The evaluator should invoke a **SKILL** that handles the gate/question mechanism
2. The skill would:
   - Format the question(s)
   - Use appropriate tools to present to user
   - Capture response
   - Return to evaluator to continue or stop

**Proposed Solution**: Create a `gate-question` skill that evaluators can invoke:

```markdown
---
name: gate-question
description: Allows subagents to pause execution and ask questions requiring user input
---

## When to Invoke

Call this skill when you (as an evaluator or other subagent) need to:
- PAUSE for clarification before continuing
- Ask the user to validate something manually
- Present options requiring a decision

## How to Use

1. Invoke skill with your questions structured as:
   - Question text
   - Context/why it matters
   - Options if applicable
   - Impact of wrong choice

2. Skill will use AskUserQuestion tool to present to user

3. Skill returns user's response for you to incorporate
```

---

## Recommendations

### Immediate Actions

1. **Restore the ORIGINAL evaluators** as baseline
   - Use `00_ORIGINAL_project-evaluator.md` and `00_ORIGINAL_work-evaluator.md`
   - These are comprehensive and proven

2. **Apply ONLY these improvements from the optimization work**:
   - Add "Runtime Evidence First" H2 section (from commits 03/04)
   - Add "What Could Not Be Verified" section to templates (from commit 02)
   - Keep evaluation-profiles references but DON'T replace content with them

3. **Create the gate-question skill** to enable subagent questioning

4. **Implement Gates** (from PLAN-2025-12-09-051425.md P1-1):
   - Add confidence level markers to evaluator output
   - Create gate checking logic that references evaluator confidence
   - Allow command-level gate strictness (`--gates=blocking|advisory|disabled`)

### What to IGNORE from the Plans

1. **All "lean" optimization** - token efficiency is not the problem, effectiveness is
2. **VALIDATION_DEBT.md ledger** - adds complexity without clear benefit
3. **Moving content to skills** - keeps evaluators fat and self-contained
4. **Automation recommendation removal** - "prefer automation" rule was useful

### Consolidated Plan

Instead of 3 separate plans with conflicting goals, here's what we should do:

#### Phase 1: Restore & Enhance (Keep Fat)
1. Start with ORIGINAL evaluators
2. Add "Runtime Evidence First" section prominently
3. Add "What Could Not Be Verified" to output templates
4. Add confidence markers to output format

#### Phase 2: Enable Questions (Critical)
1. Create `gate-question` skill
2. Modify evaluators to invoke skill when PAUSE needed
3. Test that questions reach user and responses work

#### Phase 3: Implement Gates (After Questions Work)
1. Add gate definitions to evaluators
2. Modify implementer agents to check gates
3. Add `--gates` parameter to commands
4. Test blocking/advisory modes

---

## File Inventory

### Plans (in `plans/` subdirectory)
| File | Date | Purpose | Status |
|------|------|---------|--------|
| PLAN-2025-12-09-040520.md | Dec 9 04:05 | Profile integration, duplication | Partially implemented, over-stripped |
| PLAN-2025-12-09-051425.md.archived | Dec 9 05:14 | Gates, confidence, validation debt | Best plan, never implemented |
| PLAN-2025-12-09-054129.md | Dec 9 05:41 | Lean optimization | Over-stripped, caused problems |

### Evaluators (in `evaluators/chronological/` subdirectory)
| File | Commit | Lines | Key Changes |
|------|--------|-------|-------------|
| 00_ORIGINAL_project-evaluator.md | 3b26e00 | 395 | Pre-optimization baseline |
| 00_ORIGINAL_work-evaluator.md | 3b26e00 | 374 | Pre-optimization baseline |
| 01_d9cb966_project-evaluator.md | d9cb966 | 412 | Added profile integration |
| 01_d9cb966_work-evaluator.md | d9cb966 | 413 | Added profile integration |
| 02_043e660_project-evaluator.md | 043e660 | 405 | Added "not verified" section |
| 02_043e660_work-evaluator.md | 043e660 | 394 | Added "not verified" section |
| 03_4bb075c_project-evaluator.md | 4bb075c | 419 | Elevated "runtime trumps tests" |
| 03_4bb075c_work-evaluator.md | 4bb075c | 410 | Elevated "runtime trumps tests" |
| 04_4baa246_project-evaluator.md | 4baa246 | 391 | Removed automation recs, added test rubric |
| 04_4baa246_work-evaluator.md | 4baa246 | 375 | Removed automation recs, compressed examples |
| 05_HEAD_project-evaluator.md | HEAD | 347 | Current state (over-stripped) |
| 05_HEAD_work-evaluator.md | HEAD | 350 | Current state (over-stripped) |

---

## Decision Points for User

1. **Baseline**: Start from ORIGINAL (recommended) or current HEAD?
2. **Gates**: Implement from PLAN-2025-12-09-051425.md?
3. **Question mechanism**: Create gate-question skill?
4. **Profile integration**: Keep "see skill" references or inline content?

---

## Appendix: Key Quotes from Plans

### From PLAN-2025-12-09-051425.md (the good one that was abandoned):

> "Current STATUS report has no enforcement mechanism preventing implementers from proceeding when validation is incomplete."

> "Gates check: Critical issues resolved, validation confidence threshold, manual debt bounded, no active PAUSE."

> "BLOCKING mode: If gates fail, implementers output STOP message with details and refuse to proceed"

### From PLAN-2025-12-09-054129.md (the over-lean one):

> "EVALUATORS should be LEAN, RELIABLE, AND MAXIMUM QUALITY"

> "KEEP IT SIMPLE, LEAN, FLEXIBLE, TOKEN EFFICIENT. LESS IS MORE."

> "NET CHANGE: -30 lines"

The problem: "lean" was prioritized over "maximum quality", leading to content removal that hurt effectiveness.
