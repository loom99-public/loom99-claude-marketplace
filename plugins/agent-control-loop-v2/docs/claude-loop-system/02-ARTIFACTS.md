# Artifacts: Templates and Compressed Forms

This document defines the structure and templates for all governance artifacts, plus the compressed forms (A₀/B₀) used for attention anchoring.

---

## Core Principle: One Screen, Always Current

Every artifact must:
- Fit on one screen (~50 lines max)
- Be updated continuously (not batched)
- Use exact, testable language (not vague prose)
- Contain only current truth (not history)

---

## Execution Plane Artifacts

Located in `governance/live/`

### TARGET.md

**Purpose:** Define what "done" means. The target end state and Definition of Done.

**Template:**

```markdown
# Target End State

## Goal
[1-2 sentence description of the end state]

## Non-Goals
- [Explicit exclusion 1]
- [Explicit exclusion 2]
- [Explicit exclusion 3]

## Target Shape
[5-10 bullets describing the desired architecture]

- [Module/component that must exist]
- [Interface/contract that must be satisfied]
- [Behavior that must work]
- [Performance constraint if applicable]
- [Integration point if applicable]

## Definition of Done

### Build & Test
- [ ] System builds without errors
- [ ] All must-pass tests passing
- [ ] No forbidden legacy imports (outside bridge)

### Migration (if applicable)
- [ ] Legacy entrypoints unreachable or flagged
- [ ] Bridge surface area at target (or zero)
- [ ] Cutover smoke tests passing

### Project-Specific
- [ ] [Custom DoD item 1]
- [ ] [Custom DoD item 2]

## Convergence Mode
ACTIVE: [yes/no]
[If active: "Activated YYYY-MM-DD. Zero deferrals. Escalate after N=1 attempt."]

## Last Updated
[YYYY-MM-DD HH:MM] - [Brief change note]
```

**Rules:**
- Any proposed work must cite which DoD item or target-shape bullet it advances
- If work diverges from TARGET, either TARGET or work must change (never improvise)
- DoD checkboxes require verification evidence, not just "looks done"

---

### BOUNDARY.md

**Purpose:** Prevent resurrection. Define what new code may not touch.

**Template:**

```markdown
# Boundary Law

## The Law
New code must not import or call legacy code except through `[bridge module path]`.

## Bridge Definition

**Module/Path:** `[path/to/bridge]`

**Allowed Surface:**
- `[function/method 1]` — [what it does]
- `[function/method 2]` — [what it does]
- `[function/method 3]` — [what it does]

**Bridge Constraints:**
- Bridge must be stateless
- Bridge may not expose legacy data structures directly
- Bridge surface must shrink toward zero

## Forbidden Dependencies

**Legacy Modules (no direct imports):**
- `[path/pattern 1]`
- `[path/pattern 2]`
- `[path/pattern 3]`

**Legacy Symbols (no direct calls):**
- `[symbol 1]`
- `[symbol 2]`

## Temporary Exceptions

| Exception | Reason | Expires When | Blocker |
|-----------|--------|--------------|---------|
| [module] may use [legacy] | [why] | BLOCKER-### resolved | BLOCKER-### |

**Exception Rules:**
- Every exception must cite a blocker ID
- Exception expires when blocker eliminated
- No exception without expiry condition

## Enforcement
- [ ] CI linter checks imports
- [ ] Pre-tool hook blocks forbidden writes
- [ ] Code review checklist

## Last Updated
[YYYY-MM-DD HH:MM] - [Brief change note]
```

**Rules:**
- If test failure tempts "bring back old code," agent must: migrate test, gate behind bridge, or escalate
- Never reintroduce legacy outside bridge
- Resurrection = immediate escalation

---

### BLOCKERS.md

**Purpose:** The only work queue. Nothing justifies work except a blocker or DoD item.

**Template:**

```markdown
# Blockers

## Active Blockers

### BLOCKER-001: [Short identifier]
**Observable Failure:** [Exact error, failing test, broken behavior]

**Impact:** Blocks DoD item "[which item]"

**Evidence:**
- [Link, file:line, command output]
- [Metric affected]

**Attempts:** [N] / [max before escalate]

**Last Attempt:** [YYYY-MM-DD] - [What was tried, why it failed]

---

### BLOCKER-002: [Short identifier]
[Same structure]

---

## Escalations Needed

### ESCALATION: BLOCKER-###
**Trigger:** [Why escalating: attempts exhausted, ambiguity, boundary violation]

**Options:**
1. [Option A] — [pros, cons, impact]
2. [Option B] — [pros, cons, impact]

**Recommended:** [Option X] because [rationale]

**Decision Required By:** [Date or phase]

---

## Recently Eliminated

| ID | Eliminated | Method | Outcome |
|----|------------|--------|---------|
| BLOCKER-### | YYYY-MM-DD | [approach] | [result] |

[Keep last 5 only]

## Last Updated
[YYYY-MM-DD HH:MM] - [Brief change note]
```

**Rules:**
- Only blockers justify work
- Anything not in blockers is either unnecessary or should be added with evidence
- No "future sprint" items — either it's a blocker or it's not needed
- Escalate after N=2 attempts (N=1 in convergence mode)

---

### METRICS.md

**Purpose:** Monotonic convergence pressure. Numbers that must move toward targets.

**Template:**

```markdown
# Convergence Metrics

## Metric 1: [Name]

**Definition:** [What this measures]

**Measurement:**
```bash
[exact command to measure]
```

**Values:**
- Current: [N]
- Target: [M]
- Delta: [+/- change]

**Trend:**
- [YYYY-MM-DD]: [value] (baseline)
- [YYYY-MM-DD]: [value] ([+/- delta])
- [YYYY-MM-DD]: [value] ([+/- delta])

**Escalation Threshold:** No progress after [N] phases

---

## Metric 2: [Name]
[Same structure]

---

## Metric 3: [Name]
[Same structure]

---

## Summary

| Metric | Current | Target | Delta | Status |
|--------|---------|--------|-------|--------|
| [Name] | [N] | [M] | [+/-] | [✓/⚠] |

## Last Updated
[YYYY-MM-DD HH:MM] - [Brief change note]
```

**Recommended Metrics by Goal Type:**

| Goal Type | Metrics |
|-----------|---------|
| Migration | Legacy import count, failing tests, migration coverage % |
| Refactor | Circular dependencies, module coupling, cyclomatic complexity |
| Feature | Feature coverage %, acceptance tests passing, API coverage |

**Rules:**
- Each phase must move at least one metric toward target
- If metric regresses: acceptable only if discovering hidden work or refining measurement
- Stagnation for N=3 phases triggers escalation

---

### DESIGN_LINKS.md

**Purpose:** Bridge between design plane and execution plane.

**Template:**

```markdown
# Design Links

## Canonical Design Documents
- [path/to/design/current/north-star/OVERVIEW.md]
- [path/to/design/current/north-star/ARCHITECTURE.md]

## Active Designs
| ID | Title | Status | SPEC Location |
|----|-------|--------|---------------|
| A-0001 | [title] | Active | /design/active/A-0001/ |

## Precedence Rule
If design/current conflicts with governance/live, **governance/live wins** until this file is updated.

## Last Updated
[YYYY-MM-DD HH:MM] - [Brief change note]
```

---

## Compressed Artifacts

Located in `governance/compressed/`

These are pre-generated at init time and regenerated when live artifacts change. Hooks inject them into context.

### A₀: Always-On Contract

**Purpose:** 5-10 hard rules that define session identity. Injected before every `/loop:` command.

**Template:** `governance/compressed/A0-contract.md`

```markdown
# Always-On Contract

You are operating under the minimal control loop.

## Hard Rules

1. **Work justified by blocker or DoD.** Never work on anything not in BLOCKERS.md or TARGET.md DoD.

2. **No deferral.** If stuck, escalate with options. Never "handle later."

3. **No resurrection.** Never reintroduce legacy code outside bridge. If tempted, escalate.

4. **Boundary law absolute.** [Single sentence from BOUNDARY.md]

5. **Metrics move monotonically.** Each phase moves at least one metric. Stagnation = escalate.

6. **Evidence required.** Every claim cites observable fact: test output, metric value, error message.

7. **Single blocker per phase.** No parallelization. Force focus.

8. **Update artifacts immediately.** Same phase, not deferred.

## Current State

- Goal: [from TARGET.md]
- Blockers: [count] active
- DoD Progress: [X]/[Y] complete
- Convergence Mode: [yes/no]

## Escalation Threshold
Normal: N=2 attempts
Convergence: N=1 attempt
```

**Generation:** Script extracts from TARGET, BOUNDARY, BLOCKERS, METRICS

---

### B₀: Playbooks

**Purpose:** Task-type-specific checklists. Injected only when relevant.

**Location:** `governance/compressed/B0-playbooks/`

#### migration.md

```markdown
# Playbook: Migration

**Active when:** Goal involves migrating from legacy to new

## Pre-Phase Checklist
- [ ] Boundary law understood
- [ ] Bridge surface documented
- [ ] Legacy imports baseline measured

## During Phase
- If test fails after removing legacy: migrate test, don't resurrect
- If new code needs legacy: use bridge only
- If bridge needs expansion: escalate

## Post-Phase Checklist
- [ ] Legacy import count decreased (or justified)
- [ ] No new bridge surface added (or justified)
- [ ] No resurrection occurred
```

#### refactor.md

```markdown
# Playbook: Refactor

**Active when:** Goal involves restructuring without behavior change

## Pre-Phase Checklist
- [ ] All tests passing before change
- [ ] Behavior contract documented

## During Phase
- Every change must be behavior-preserving
- Tests must stay green after each step
- If tests fail: roll back, understand, retry

## Post-Phase Checklist
- [ ] All tests still passing
- [ ] Coupling metrics improved (or justified)
- [ ] No new technical debt introduced
```

#### feature.md

```markdown
# Playbook: Feature

**Active when:** Goal involves adding new functionality

## Pre-Phase Checklist
- [ ] Feature scope defined in TARGET
- [ ] Acceptance criteria in DoD
- [ ] No legacy entanglement required

## During Phase
- Build incrementally with verification at each step
- If legacy code needed: escalate, don't couple directly
- Keep feature isolated until integration point

## Post-Phase Checklist
- [ ] Feature tests passing
- [ ] Integration tests passing
- [ ] No boundary violations
```

**Generation:** Script generates based on goal keywords and TARGET content

---

## Historical Artifacts

### PHASE-LOG.md

**Purpose:** Append-only history of all phases.

**Location:** `governance/PHASE-LOG.md`

**Template:**

```markdown
# Phase Log

---

## Phase [N] - [YYYY-MM-DD HH:MM]

**Blocker:** BLOCKER-### - [description]

**Outcome:** ELIMINATED | TRANSFORMED | ESCALATED | FAILED

**Method:** [Brief approach description]

**Evidence:**
- [Key result 1]
- [Key result 2]

**Metrics Delta:**
- [Metric 1]: [old] → [new] ([+/- delta])

**Next:** [Recommended action]

---

## Phase [N-1] - [YYYY-MM-DD HH:MM]
[Same structure]
```

---

### HISTORY.md

**Purpose:** Append-only ledger of major decisions.

**Location:** `governance/HISTORY.md`

**Template:**

```markdown
# Decision History

---

## [YYYY-MM-DD] - [Decision Title]

**Context:** [Why decision was needed]

**Decision:** [What was decided]

**Rationale:** [Why this option]

**Impact:**
- TARGET: [change or "no change"]
- BOUNDARY: [change or "no change"]
- METRICS: [change or "no change"]

**Decided By:** [human / escalation resolution]

---
```

---

## Roadmap Artifacts

### slice.md

**Purpose:** Future work waiting to be promoted to blockers.

**Location:** `governance/roadmap/slices/S-####-slug/slice.md`

**Template:**

```markdown
# Slice: [Title]

## Goal
[What this slice accomplishes]

## Scope
[Boundaries of this work]

## Success Checks
- [ ] [Observable verification 1]
- [ ] [Observable verification 2]

## Dependencies
- Requires: [other slice IDs or blockers]
- Blocks: [what this enables]

## Anticipated Blockers
- [Likely blocker 1]
- [Likely blocker 2]

## Risk Notes
[Known unknowns, potential issues]

## Status
QUEUED | READY | PROMOTED

## Promoted To
[BLOCKER-### when promoted, or "not yet"]
```

---

## Completed Artifacts

### summary.md

**Purpose:** Record of completed slice.

**Location:** `governance/completed/slices/S-####-slug__YYYY-MM-DD/summary.md`

**Template:**

```markdown
# Completed: [Title]

## Completed
[YYYY-MM-DD HH:MM]

## What Changed
[Summary of changes made]

## Validation
- [Test result 1]
- [Test result 2]
- [Metric result]

## Blockers Eliminated
- BLOCKER-###: [description]

## Key Decisions
- [Decision 1]: [rationale]

## Remaining Follow-ups
- [Any deferred work that became new slices]
```

---

## Artifact Validation Rules

Used by `artifact-validator` agent and `artifact-io` skill.

### TARGET.md Validation

- [ ] Goal is 1-2 sentences
- [ ] Goal describes end state (not process)
- [ ] Non-goals has at least 1 item
- [ ] Target shape has 5-10 bullets
- [ ] DoD has at least 3 checkable items
- [ ] Last Updated is present
- [ ] < 50 lines total

### BOUNDARY.md Validation

- [ ] Law is single sentence
- [ ] Bridge path exists (or "none")
- [ ] Forbidden list has at least 1 item (or "none")
- [ ] All exceptions have expiry condition
- [ ] All exceptions cite blocker ID
- [ ] Last Updated is present
- [ ] < 50 lines total

### BLOCKERS.md Validation

- [ ] Every blocker has observable failure
- [ ] Every blocker cites DoD impact
- [ ] Every blocker has evidence
- [ ] Every blocker has attempt count
- [ ] Escalations have options (2+)
- [ ] Escalations have recommendation
- [ ] Last Updated is present
- [ ] < 50 lines total (move history to PHASE-LOG if needed)

### METRICS.md Validation

- [ ] 2-4 metrics defined
- [ ] Every metric has measurement command
- [ ] Measurement commands execute successfully
- [ ] Current values are populated
- [ ] Target values are populated
- [ ] Trend has at least baseline entry
- [ ] Last Updated is present
- [ ] < 50 lines total

---

## Compressed Artifact Generation

### When to Regenerate

- After `/loop:init`
- After any `/loop:phase` that updates TARGET, BOUNDARY, or METRICS
- After any `/design:accept` that applies governance deltas
- Manually via script if artifacts edited directly

### Generation Process

1. Read live artifacts
2. Extract key fields per template
3. Write to `governance/compressed/`
4. Validate result

**Script:** `scripts/regenerate-compressed.sh`

```bash
#!/bin/bash
# Regenerate compressed artifacts from live artifacts

LIVE_DIR="governance/live"
COMPRESSED_DIR="governance/compressed"

# Validate live artifacts exist
for file in TARGET.md BOUNDARY.md BLOCKERS.md METRICS.md; do
  if [ ! -f "$LIVE_DIR/$file" ]; then
    echo "ERROR: Missing $LIVE_DIR/$file"
    exit 1
  fi
done

# Extract goal from TARGET.md
GOAL=$(grep -A1 "^## Goal" "$LIVE_DIR/TARGET.md" | tail -1)

# Extract boundary law from BOUNDARY.md
LAW=$(grep -A1 "^## The Law" "$LIVE_DIR/BOUNDARY.md" | tail -1)

# Count blockers
BLOCKER_COUNT=$(grep -c "^### BLOCKER-" "$LIVE_DIR/BLOCKERS.md")

# Count DoD items
DOD_TOTAL=$(grep -c "^\- \[ \]" "$LIVE_DIR/TARGET.md")
DOD_COMPLETE=$(grep -c "^\- \[x\]" "$LIVE_DIR/TARGET.md")

# Check convergence mode
if grep -q "ACTIVE: yes" "$LIVE_DIR/TARGET.md"; then
  CONVERGENCE="yes"
else
  CONVERGENCE="no"
fi

# Generate A0-contract.md
cat > "$COMPRESSED_DIR/A0-contract.md" << EOF
# Always-On Contract

You are operating under the minimal control loop.

## Hard Rules

1. **Work justified by blocker or DoD.** Never work on anything not in BLOCKERS.md or TARGET.md DoD.
2. **No deferral.** If stuck, escalate with options. Never "handle later."
3. **No resurrection.** Never reintroduce legacy code outside bridge. If tempted, escalate.
4. **Boundary law absolute.** $LAW
5. **Metrics move monotonically.** Each phase moves at least one metric. Stagnation = escalate.
6. **Evidence required.** Every claim cites observable fact.
7. **Single blocker per phase.** No parallelization. Force focus.
8. **Update artifacts immediately.** Same phase, not deferred.

## Current State
- Goal: $GOAL
- Blockers: $BLOCKER_COUNT active
- DoD Progress: $DOD_COMPLETE/$DOD_TOTAL complete
- Convergence Mode: $CONVERGENCE

## Escalation Threshold
Normal: N=2 attempts | Convergence: N=1 attempt
EOF

echo "Regenerated $COMPRESSED_DIR/A0-contract.md"
```

---

## Summary

| Artifact | Location | Purpose | Binding? |
|----------|----------|---------|----------|
| TARGET.md | governance/live/ | What "done" means | YES |
| BOUNDARY.md | governance/live/ | What is forbidden | YES |
| BLOCKERS.md | governance/live/ | The only work queue | YES |
| METRICS.md | governance/live/ | Convergence pressure | YES |
| DESIGN_LINKS.md | governance/live/ | Bridge to design plane | YES |
| A0-contract.md | governance/compressed/ | Always-on rules | YES (injected) |
| B0-playbooks/* | governance/compressed/ | Task-type checklists | YES (when active) |
| PHASE-LOG.md | governance/ | Phase history | NO (read-only) |
| HISTORY.md | governance/ | Decision ledger | NO (read-only) |
| slice.md | governance/roadmap/ | Future work | NO (non-binding) |
| summary.md | governance/completed/ | Past work | NO (read-only) |
