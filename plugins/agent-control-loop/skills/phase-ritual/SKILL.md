---
name: phase-ritual
description: Execute the 5-step phase ritual that drives the minimal control loop - artifact restatement, blocker selection, planning, execution, outcome recording
---

# Phase Ritual Skill

## Purpose

Implements the core phase ritual that drives convergent work. Ensures every phase of work is grounded in current reality (artifacts), focused on a single high-value blocker, and produces observable progress.

## When to Use

- During `/loop:phase` command execution
- When Governor agent begins a work phase
- Any time convergent, blocker-driven work is needed
- When work has stalled and needs forced focus

## The Five-Step Ritual

Each phase follows this exact sequence. No steps may be skipped.

### Step 1: Artifact Restatement

**Purpose:** Ground the agent in current reality before making decisions.

**Procedure:**

1. Read all 4 artifacts from `governance/live/`:
   - `TARGET.md`
   - `BOUNDARY.md`
   - `BLOCKERS.md`
   - `METRICS.md`

2. Restate each artifact's current content:

```markdown
=== ARTIFACT RESTATEMENT ===

TARGET:
Goal: [exact goal statement from TARGET.md]
DoD Progress: [X/Y items complete]
Key Target Shape:
- [bullet 1]
- [bullet 2]
- [bullet 3]

BOUNDARY:
Law: [exact boundary law]
Bridge: [bridge module path]
Forbidden: [top 3 forbidden dependencies]
Exceptions: [count] active

BLOCKERS:
Active: [count] blockers
Top 3 by Impact:
1. BLOCKER-[id]: [short description] - blocks [DoD item]
2. BLOCKER-[id]: [short description] - blocks [DoD item]
3. BLOCKER-[id]: [short description] - blocks [DoD item]

Escalations: [count] pending decisions

METRICS:
[Metric 1]: [current] → [target] (delta: [+/-])
[Metric 2]: [current] → [target] (delta: [+/-])
[Metric 3]: [current] → [target] (delta: [+/-])

=== END RESTATEMENT ===
```

**Critical Rules:**
- Use exact text from artifacts (not paraphrasing)
- Include ALL metrics (not selective)
- State blocker count even if zero
- Note DoD progress explicitly

**If artifacts missing:** Halt and require `/loop:init` first.

---

### Step 2: Single-Blocker Selection

**Purpose:** Force focus on the highest-value work. Prevent paralysis and diffusion.

**Selection Criteria (in order):**

1. **Blocks DoD item** - Directly prevents completion
2. **High blast radius** - Blocks multiple other blockers
3. **Blocking metric progress** - Prevents metric from moving
4. **Oldest blocker** - Been stuck longest
5. **Most evidence** - Best understood, most actionable

**Procedure:**

1. List all active blockers with selection score:

```markdown
=== BLOCKER SELECTION ===

Candidates:
1. BLOCKER-001: [description]
   - Blocks DoD: "System builds" ✓ (+10)
   - Blast radius: Blocks BLOCKER-002, BLOCKER-005 (+5)
   - Metric impact: Blocks "failing tests" metric (+3)
   - Age: 3 days (+1)
   - Evidence: Complete (+2)
   SCORE: 21

2. BLOCKER-002: [description]
   - Blocks DoD: None (0)
   - Blast radius: Independent (0)
   - Metric impact: None (0)
   - Age: 1 day (0)
   - Evidence: Incomplete (-2)
   SCORE: -2

[... all blockers scored ...]
```

2. Select highest-scoring blocker
3. Justify selection explicitly:

```markdown
SELECTED: BLOCKER-001

JUSTIFICATION:
- Directly blocks DoD item "System builds"
- Eliminates this blocker → unblocks BLOCKER-002 and BLOCKER-005
- Will move "failing tests" metric by estimated -5
- Strong evidence available (exact error, file:line, test output)
- High confidence in resolution path
```

**Anti-Patterns to Prevent:**

- ❌ "Let's work on multiple blockers" → REJECTED, select ONE
- ❌ "This looks easier" → Justify by impact, not ease
- ❌ "We should do this later" → No deferrals, select NOW
- ❌ "Not enough info" → Escalate or gather evidence first

**If zero blockers:** Verify DoD complete. If not, work is missing from BLOCKERS.md.

---

### Step 3: Phase Plan Generation

**Purpose:** Create executable, verifiable plan for eliminating the blocker.

**Plan Structure:**

```markdown
=== PHASE PLAN: BLOCKER-[id] ===

GOAL: Eliminate BLOCKER-[id] - [description]

APPROACH: [One sentence describing the strategy]

STEPS:
1. [Action step 1]
   - Verification: [How to confirm this step worked]
   - Risk: [What could go wrong]
   - Fallback: [What to do if it fails]

2. [Action step 2]
   - Verification: [Observable check]
   - Risk: [Potential failure mode]
   - Fallback: [Alternative approach]

3. [Action step 3]
   - Verification: [Test to run, metric to check]
   - Risk: [Edge case to watch]
   - Fallback: [Escalation if stuck]

[4-7 total steps maximum]

VERIFICATION CRITERIA:
- [ ] [Specific test passes]
- [ ] [Metric moves by X]
- [ ] [Error no longer appears]
- [ ] [DoD item checkable]

STOP CONDITIONS:
- Success: All verification criteria met
- Escalate: After N=2 failed attempts
- Pause: If boundary law violation required
- Defer: NEVER (must escalate instead)

=== END PLAN ===
```

**Plan Constraints:**

- **3-7 steps** - Not fewer (too vague), not more (too complex)
- **Every step verifiable** - Must have observable check
- **No unbounded loops** - Each step has max attempts
- **Explicit fallbacks** - What to do when step fails
- **No deferred work** - Must finish or escalate

**Verification Criteria Quality:**

✅ **Good:** "Test `test_auth_flow` passes"
❌ **Bad:** "Auth feels better"

✅ **Good:** "Legacy import count decreases by >= 5"
❌ **Bad:** "Code is cleaner"

✅ **Good:** "Build completes with exit code 0"
❌ **Bad:** "Build is fixed"

**Stop Conditions:**

- **Success** - Observable, testable
- **Escalate** - Specific trigger (N failed attempts, ambiguity found, boundary violation needed)
- **Pause** - Only if user input required (never "we'll do it later")
- **Defer** - FORBIDDEN (escalate instead)

---

### Step 4: Execution (Delegated to Implementer)

**Purpose:** Carry out the plan, capturing evidence at each step.

**This skill does NOT execute code.** It generates the plan. Execution is delegated to:
- Governor agent (if capable)
- iterative-implementer agent (common)
- User (for manual steps)

**Execution Protocol:**

```markdown
=== EXECUTION LOG ===

Step 1: [action]
├─ Started: [timestamp]
├─ Output: [command output, error messages, file changes]
├─ Verification: [test result, metric value]
├─ Status: ✓ SUCCESS | ❌ FAILED | ⚠️ PARTIAL
└─ Notes: [observations, unexpected behavior]

Step 2: [action]
[... same structure ...]

[Continue for all steps]

=== END EXECUTION ===
```

**Evidence Requirements:**

- Capture exact error messages
- Record test output (pass/fail counts, specific failures)
- Note metric deltas (before/after values)
- Link to file diffs or commits
- Timestamp each step

**Failure Handling:**

If a step fails:
1. Record failure evidence
2. Try fallback (if specified)
3. If fallback fails, increment attempt counter
4. If attempt counter >= N (usually 2-3), trigger escalation
5. NEVER silently skip or defer

---

### Step 5: Outcome Recording

**Purpose:** Update artifacts to reflect reality post-phase. Create historical record.

**Procedure:**

1. **Determine Outcome:**

   - **ELIMINATED** - Blocker fully resolved, verification passed
   - **TRANSFORMED** - Blocker changed form (update BLOCKERS.md)
   - **ESCALATED** - Stuck, needs user decision (add to escalations)
   - **FAILED** - Attempted but verification failed (stays in BLOCKERS.md)

2. **Update BLOCKERS.md:**

   ```markdown
   If ELIMINATED:
   - Remove blocker from Active Blockers
   - Add to Recently Eliminated table with method and outcome

   If TRANSFORMED:
   - Update blocker description and evidence
   - Note transformation in "Last Attempt"

   If ESCALATED:
   - Move to Escalations Needed section
   - Add options, recommendation, decision deadline

   If FAILED:
   - Update "Last Attempt" with failure evidence
   - Increment attempt counter
   - Check if should escalate (attempts >= N)
   ```

3. **Update METRICS.md:**

   ```markdown
   For each affected metric:
   - Measure new value (run measurement command)
   - Calculate delta
   - Update Current Value
   - Add to Trend history
   - Verify monotonic movement (or justify regression)
   ```

4. **Update TARGET.md (if applicable):**

   ```markdown
   If DoD item now checkable:
   - Check the box: [ ] → [x]
   - Update DoD progress count

   If target shape changed:
   - Note the change in "Last Updated"
   - Explain why (usually blocker revealed new information)
   ```

5. **Update BOUNDARY.md (if applicable):**

   ```markdown
   If exception expired:
   - Remove from Temporary Exceptions table
   - Verify enforcement now applies

   If bridge surface changed:
   - Update Allowed Surface list
   - Note reduction in bridge scope (surface should shrink)
   ```

6. **Record Phase Summary:**

   Create or append to `governance/PHASE-LOG.md`:

   ```markdown
   ## Phase [N] - [YYYY-MM-DD HH:MM]

   **Blocker:** BLOCKER-[id] - [description]

   **Outcome:** ELIMINATED | TRANSFORMED | ESCALATED | FAILED

   **Method:** [Brief description of approach]

   **Evidence:**
   - [Key result 1]
   - [Key result 2]

   **Metrics Delta:**
   - [Metric 1]: [old] → [new] ([+/- delta])
   - [Metric 2]: [old] → [new] ([+/- delta])

   **Next:** [Recommended next blocker or action]

   ---
   ```

**Validation Post-Update:**

- All artifacts still < 50 lines
- No broken references (blocker IDs, DoD items)
- Metrics moved monotonically (or justified)
- "Last Updated" timestamp refreshed

---

## Complete Phase Ritual Example

```markdown
=== PHASE RITUAL EXECUTION ===

[STEP 1: ARTIFACT RESTATEMENT]
TARGET:
Goal: Migrate frontend from legacy to new architecture
DoD Progress: 3/7 complete
Key Target Shape:
- All UI components use new state management
- Zero direct imports of legacy store
- Feature parity with legacy UI

BOUNDARY:
Law: New components must not import legacy store except through compatibility layer
Bridge: src/compat/legacy-bridge.ts
Forbidden: src/legacy/store/*, src/legacy/actions/*
Exceptions: 1 active (Dashboard may use legacy store until BLOCKER-003 resolved)

BLOCKERS:
Active: 4 blockers
Top 3 by Impact:
1. BLOCKER-003: UserProfile component imports legacy store - blocks DoD "zero legacy imports"
2. BLOCKER-001: New store missing subscription API - blocks UserProfile migration
3. BLOCKER-004: Tests fail when legacy store removed - blocks DoD "all tests pass"

Escalations: 0 pending

METRICS:
Legacy store imports: 12 → 0 (delta: -12, 4 remaining)
Failing tests: 15 → 0 (delta: -15, 8 remaining)
Migration coverage: 60% → 100% (delta: +40%, currently 75%)

[STEP 2: BLOCKER SELECTION]
SELECTED: BLOCKER-001 (New store missing subscription API)

JUSTIFICATION:
- Blocks BLOCKER-003 (UserProfile migration)
- Blocking metric: "Legacy store imports" cannot decrease until this is fixed
- Blast radius: 3 components waiting for this API
- Strong evidence: Exact API contract needed is documented
- High confidence: Implementation pattern is clear

[STEP 3: PHASE PLAN]
GOAL: Add subscription API to new store to enable UserProfile migration

STEPS:
1. Add `subscribe(selector, callback)` method to new store
   - Verification: Unit test `test_store_subscription` passes
   - Risk: API signature might not match legacy exactly
   - Fallback: Check UserProfile usage, adjust signature

2. Implement subscription cleanup on component unmount
   - Verification: No memory leaks in test `test_subscription_cleanup`
   - Risk: React lifecycle timing issues
   - Fallback: Use useEffect cleanup pattern

3. Migrate UserProfile to use new store subscription API
   - Verification: UserProfile renders correctly, all existing tests pass
   - Risk: Subtle state timing differences
   - Fallback: Add compatibility shim if needed

4. Remove UserProfile from boundary exception list
   - Verification: Linter passes, no legacy store imports
   - Risk: None
   - Fallback: N/A

VERIFICATION CRITERIA:
- [ ] test_store_subscription passes
- [ ] test_subscription_cleanup passes
- [ ] UserProfile component tests all pass (5 tests)
- [ ] Linter shows 0 legacy store imports in UserProfile
- [ ] Metric "Legacy store imports" decreased by >= 1

STOP CONDITIONS:
- Success: All verification criteria met
- Escalate: After 2 failed attempts at any step
- Pause: If API contract ambiguity discovered

[STEP 4: EXECUTION]
(Delegated to iterative-implementer)

[STEP 5: OUTCOME]
OUTCOME: ELIMINATED

BLOCKERS.md updated:
- BLOCKER-001 moved to Recently Eliminated
- BLOCKER-003 ready to attack (blocker removed)

METRICS.md updated:
- Legacy store imports: 12 → 11 (delta: -1) ✓
- Test count: 8 failing → 5 failing (delta: -3) ✓

BOUNDARY.md updated:
- UserProfile removed from Temporary Exceptions

Phase Log entry created.

NEXT: Attack BLOCKER-003 (UserProfile migration now unblocked)

=== END PHASE RITUAL ===
```

---

## Integration with Governor Agent

The Governor agent uses this skill as its core operating procedure:

```markdown
Governor Workflow:
1. Invoke phase-ritual skill (Steps 1-3)
2. Delegate execution to implementer
3. Monitor execution progress
4. Enforce stop conditions
5. Invoke phase-ritual skill Step 5 (outcome recording)
6. Recommend next phase
```

---

## Anti-Patterns and Enforcement

### Deferral Prevention

❌ **Forbidden:**
- "We'll handle this in a future phase"
- "Out of scope for now"
- "TODO: fix later"

✅ **Required:**
- Add to BLOCKERS.md with evidence
- Escalate if ambiguous
- Work until eliminated or escalated

### Resurrection Prevention

❌ **Forbidden:**
- "Bring back old code to make tests pass"
- "Temporarily use legacy approach"
- "Bridge can call legacy freely"

✅ **Required:**
- Check BOUNDARY.md before any code change
- Escalate if boundary violation needed
- Migrate test, don't resurrect code

### Plan Drift Prevention

❌ **Forbidden:**
- Working on blockers not in BLOCKERS.md
- Skipping artifact restatement
- Ignoring current TARGET

✅ **Required:**
- Restate artifacts every phase (Step 1)
- Only work on selected blocker (Step 2)
- Update artifacts post-phase (Step 5)

### Fake Completion Prevention

❌ **Forbidden:**
- Checking DoD box without verification
- Claiming metric moved without measurement
- "Looks done" without evidence

✅ **Required:**
- Run verification criteria
- Measure metrics with exact commands
- Capture evidence for every claim

---

## Escalation Triggers

The ritual automatically escalates when:

1. **Attempt threshold exceeded** (N=2-3 failures)
2. **Boundary violation required** (need to break boundary law)
3. **Ambiguity blocks progress** (contract unclear, multiple valid approaches)
4. **Metric regression** (metric moved away from target)
5. **Zero blockers but DoD incomplete** (work is missing from queue)

**Escalation Format:**

```markdown
=== ESCALATION: BLOCKER-[id] ===

TRIGGER: [Why escalating]

CONTEXT: [What was attempted, why it failed]

OPTIONS:
1. [Option A]
   - Pros: [list]
   - Cons: [list]
   - Impact: [specific consequences]

2. [Option B]
   - Pros: [list]
   - Cons: [list]
   - Impact: [specific consequences]

RECOMMENDED: [Option X] because [rationale]

REQUIRED BY: [Date or DoD item timeline]

=== END ESCALATION ===
```

---

## Best Practices

1. **Always restate** - Even if "nothing changed," restate artifacts
2. **One blocker only** - Never parallelize blocker work
3. **Verifiable steps** - Every step must have observable check
4. **Capture evidence** - Exact errors, test output, metric values
5. **Update immediately** - Artifacts updated same phase, not deferred
6. **Monotonic metrics** - If metric regresses, escalate or justify
7. **No silent failures** - Every failure recorded, counted, escalated

## Error Handling

**Artifacts missing:** Halt, require `/loop:init`

**Blocker poorly defined:** Refuse to select, require evidence

**Plan too vague:** Reject plan, require verifiable steps

**Execution fails without evidence:** Halt, require error capture

**Metric measurement fails:** Escalate, fix measurement method

**Artifacts exceed 50 lines:** Warn, require trimming before next phase

## See Also

- `skills/artifact-templates/SKILL.md` - Templates for 4 live artifacts
- `agents/governor.md` - Governor agent that drives the ritual
- `commands/phase.md` - /loop:phase command that invokes this skill
- `docs/_now/control-loop-system/CONTEXT-PRIME.md` - Full system specification
