# Skills: Shared Behaviors

This document defines all skills in the agent-control-loop plugin. Skills are reusable procedures called by agents.

---

## Design Principle: Skills Are Procedures

Skills contain **shared behavior** that multiple agents need. They are:
- Procedural (step-by-step)
- Deterministic where possible
- May call scripts for file operations
- Never make routing decisions

Agents own goals. Skills own procedures.

---

## Skill Summary

| Skill | Purpose | Used By |
|-------|---------|---------|
| phase-ritual | 5-step phase execution | Governor |
| artifact-io | Read/write/validate artifacts | All agents |
| blocker-scoring | Score and rank blockers | Governor |
| metric-measurement | Measure and track metrics | Governor |
| decision-gate | Present AskUserQuestion | All agents |
| design-lifecycle | State machine transitions | Design-Curator |
| compressed-artifacts | Generate A₀/B₀ | Governor, Design-Curator |

---

## phase-ritual

**Purpose:** Execute the 5-step phase ritual that drives convergent work.

**Location:** `skills/phase-ritual/SKILL.md`

### Frontmatter

```yaml
---
name: phase-ritual
description: Execute the 5-step phase ritual - artifact restatement, blocker selection, planning, execution, outcome recording
---
```

### When to Use

- During `/loop:phase` execution
- When Governor begins a work phase
- When work has stalled and needs forced focus

### The Five Steps

#### Step 1: Artifact Restatement

**Purpose:** Ground in current reality before making decisions.

**Procedure:**

1. Use `artifact-io` skill to read all 4 artifacts
2. Restate each artifact's current content:

```markdown
=== ARTIFACT RESTATEMENT ===

TARGET:
Goal: [exact text]
DoD Progress: [X/Y items]
Key Target Shape: [top 3 bullets]

BOUNDARY:
Law: [exact law sentence]
Bridge: [path]
Exceptions: [count] active

BLOCKERS:
Active: [count]
Top 3 by Impact:
1. BLOCKER-###: [description]
2. BLOCKER-###: [description]
3. BLOCKER-###: [description]
Escalations: [count] pending

METRICS:
[Metric 1]: [current] → [target] (delta: [+/-])
[Metric 2]: [current] → [target] (delta: [+/-])

=== END RESTATEMENT ===
```

**Rules:**
- Use exact text (not paraphrased)
- Include ALL metrics
- State blocker count even if zero
- If artifacts missing: halt, require `/loop:init`

#### Step 2: Blocker Selection

**Purpose:** Force focus on highest-value work.

**Procedure:**

1. Use `blocker-scoring` skill to score all blockers
2. Select highest-scoring blocker
3. Justify selection:

```markdown
=== BLOCKER SELECTION ===

Candidates:
1. BLOCKER-###: [description]
   - Blocks DoD: [item] (+10)
   - Blast radius: Blocks [other blockers] (+5)
   - Metric impact: [which metric] (+3)
   - Age: [N days] (+1)
   - Evidence: [quality] (+/-2)
   SCORE: [total]

[... all blockers scored ...]

SELECTED: BLOCKER-###

JUSTIFICATION:
- [Why this blocker has highest value]
- [What eliminating it unblocks]
- [Expected metric impact]

=== END SELECTION ===
```

**Rules:**
- Select ONE blocker only
- Justify by impact, not ease
- If zero blockers but DoD incomplete: work is missing, halt

#### Step 3: Phase Plan Generation

**Purpose:** Create executable, verifiable plan.

**Procedure:**

Generate plan with 3-7 steps:

```markdown
=== PHASE PLAN: BLOCKER-### ===

GOAL: Eliminate BLOCKER-### - [description]

APPROACH: [One sentence strategy]

STEPS:
1. [Action]
   - Verification: [observable check]
   - Risk: [potential failure]
   - Fallback: [alternative if fails]

2. [Action]
   - Verification: [observable check]
   - Risk: [potential failure]
   - Fallback: [alternative if fails]

[3-7 steps total]

VERIFICATION CRITERIA:
- [ ] [Specific test/check 1]
- [ ] [Specific test/check 2]
- [ ] [Metric delta expected]

STOP CONDITIONS:
- Success: All verification criteria met
- Escalate: After N=2 failed attempts
- Pause: If boundary violation required

=== END PLAN ===
```

**Rules:**
- 3-7 steps (not fewer, not more)
- Every step has verification, risk, fallback
- Stop conditions explicit
- No "defer" as a stop condition

#### Step 4: Execution

**Purpose:** Carry out the plan, capturing evidence.

**Procedure:**

This skill does NOT execute code. It provides the execution protocol:

```markdown
=== EXECUTION LOG ===

Step 1: [action]
├─ Started: [timestamp]
├─ Output: [result]
├─ Verification: [pass/fail]
├─ Status: ✓/❌/⚠
└─ Notes: [observations]

[Continue for all steps]

=== END EXECUTION ===
```

**Failure Handling:**
1. Record failure evidence
2. Try fallback
3. If fallback fails: increment attempt counter
4. If attempts ≥ N: trigger escalation
5. Never silently skip

#### Step 5: Outcome Recording

**Purpose:** Update artifacts to reflect post-phase reality.

**Procedure:**

1. Determine outcome: ELIMINATED | TRANSFORMED | ESCALATED | FAILED

2. Update BLOCKERS.md:
   - ELIMINATED: Remove, add to Recently Eliminated
   - TRANSFORMED: Update description and evidence
   - ESCALATED: Move to Escalations Needed
   - FAILED: Update attempt count, check if should escalate

3. Update METRICS.md:
   - Use `metric-measurement` skill
   - Calculate delta
   - Verify monotonic movement

4. Update TARGET.md if DoD item now complete

5. Update BOUNDARY.md if exception expired

6. Append to PHASE-LOG.md:

```markdown
## Phase [N] - [YYYY-MM-DD HH:MM]

**Blocker:** BLOCKER-### - [description]
**Outcome:** [outcome]
**Method:** [approach]
**Evidence:** [key results]
**Metrics Delta:** [changes]
**Next:** [recommendation]
```

---

## artifact-io

**Purpose:** Read, write, and validate governance artifacts.

**Location:** `skills/artifact-io/SKILL.md`

### Frontmatter

```yaml
---
name: artifact-io
description: Read, write, and validate governance artifacts. Provides consistent artifact access layer.
---
```

### Operations

#### Read Artifact

```markdown
Read [artifact] from governance/live/

Returns:
- Content (full text)
- Metadata (last updated, line count)
- Validation status
```

#### Write Artifact

```markdown
Write [artifact] to governance/live/

Before write:
1. Validate against template
2. Check < 50 lines
3. Verify required fields present

After write:
1. Update "Last Updated" timestamp
2. Trigger compressed artifact regeneration if needed
```

#### Validate Artifact

```markdown
Validate [artifact]

Checks:
- Structure matches template
- Required fields present
- Cross-references valid
- < 50 lines
- Measurement commands work (for METRICS.md)

Returns:
- Valid/Invalid
- List of issues
- Fix suggestions
```

### Scripts Called

- `validate-artifact.sh` — Structure validation
- `measure-metrics.sh` — Metric command validation

---

## blocker-scoring

**Purpose:** Score and rank blockers for selection.

**Location:** `skills/blocker-scoring/SKILL.md`

### Frontmatter

```yaml
---
name: blocker-scoring
description: Score and rank blockers by value. Used for single-blocker selection in phase ritual.
---
```

### Scoring Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| Blocks DoD item | +10 | Directly prevents completion |
| Blast radius | +5 per blocked blocker | Blocks other blockers |
| Metric impact | +3 | Prevents metric from moving |
| Age | +1 per day (max +5) | Been stuck longest |
| Evidence quality | +2 (complete) / -2 (incomplete) | How actionable |

### Procedure

```markdown
For each blocker in BLOCKERS.md:

1. Check if it blocks a DoD item
   - Parse DoD in TARGET.md
   - Check "Impact" field references DoD
   - If yes: +10 points

2. Check blast radius
   - Look for blockers that depend on this one
   - +5 per dependent blocker

3. Check metric impact
   - Does resolving this move a metric?
   - +3 if yes

4. Calculate age
   - Parse "Last Attempt" date
   - +1 per day, max +5

5. Assess evidence quality
   - Has observable failure? Has file:line? Has test name?
   - +2 if complete, -2 if incomplete

6. Sum total score

Return: Ordered list of blockers by score
```

---

## metric-measurement

**Purpose:** Measure metrics and track trends.

**Location:** `skills/metric-measurement/SKILL.md`

### Frontmatter

```yaml
---
name: metric-measurement
description: Measure metrics using defined commands. Track trends and verify monotonic progress.
---
```

### Procedure

```markdown
For each metric in METRICS.md:

1. Parse measurement command
   - Extract bash command from "Measurement" section

2. Execute measurement
   - Script: measure-metrics.sh [command]
   - Capture output
   - Parse numeric value

3. Calculate delta
   - Compare to previous value
   - Record +/- change

4. Update METRICS.md
   - Current Value: [new value]
   - Delta: [change]
   - Trend: append "[date]: [value] ([delta])"

5. Check monotonicity
   - If moving toward target: ✓
   - If stagnant: ⚠ (warn)
   - If moving away: ⚠ (require justification)

Return: Measurement results and any warnings
```

### Scripts Called

- `measure-metrics.sh` — Execute measurement commands

---

## decision-gate

**Purpose:** Present structured options via AskUserQuestion.

**Location:** `skills/decision-gate/SKILL.md`

### Frontmatter

```yaml
---
name: decision-gate
description: Present decision gates via AskUserQuestion. Collects structured human decisions.
---
```

### Procedure

```markdown
To present a decision:

1. Gather context
   - What triggered this decision
   - What's at stake

2. Generate options (2-4)
   - Each option has: label, description, pros, cons, impact

3. Determine recommendation
   - Based on evidence and constraints
   - Always include rationale

4. Format for AskUserQuestion:

questions:
  - question: "[The decision question]"
    header: "[Short label]"
    options:
      - label: "[Option 1]"
        description: "[Explanation + pros/cons/impact]"
      - label: "[Option 2]"
        description: "[Explanation + pros/cons/impact]"
      - label: "[Option 3] (Recommended)"
        description: "[Explanation + pros/cons/impact + why recommended]"
    multiSelect: false

5. Invoke AskUserQuestion tool

6. Process response
   - Record decision
   - Update relevant artifacts
   - Add to HISTORY.md if significant

Return: Selected option and any follow-up actions
```

### Gate Types

| Gate | Typical Options |
|------|-----------------|
| Accept Proposal | Accept, Reject, OnIce, Request Evidence |
| Ship Design | Ship, Keep Active, Needs Work |
| Supersede | Supersede, Keep Current, Merge |
| Reject | Reject, Revise, Archive |
| Boundary Change | Expand Bridge, Change Law, Alternative |
| Blocker Escalation | [Custom based on blocker] |

---

## design-lifecycle

**Purpose:** Manage design proposal state transitions.

**Location:** `skills/design-lifecycle/SKILL.md`

### Frontmatter

```yaml
---
name: design-lifecycle
description: Manage design proposal lifecycle. State transitions, validation, and archival.
---
```

### State Machine

```
Drafted → Proposed → InReview → Accepted → Active → Shipped → Archived
                            ↘ Rejected ──────────────────────→ Archived
                   Any → OnIce (pause)
                   Any → Superseded → Archived
```

### Transitions

#### Proposed → InReview

**Requirements:**
- PROPOSAL.md complete
- Evidence included or "evidence missing" noted

**Actions:**
- Update STATUS.md: state = InReview
- Update design/index.md

#### InReview → Accepted

**Requirements:**
- Human decision (Gate #1)
- GOVERNANCE-DELTA.md present
- Risk notes documented

**Actions:**
- Create design/active/A-####/
- Copy SPEC.md
- Update STATUS.md: state = Accepted
- Apply GOVERNANCE-DELTA to governance/live/*
- Update DESIGN_LINKS.md
- Regenerate compressed artifacts

#### Accepted → Active

**Requirements:**
- Referenced in roadmap OR blockers exist

**Actions:**
- Update STATUS.md: state = Active
- Update LINKS.md with blocker/slice references

#### Active → Shipped

**Requirements:**
- Human decision (Gate #2)
- Acceptance criteria satisfied
- Metrics at targets

**Actions:**
- Update STATUS.md: state = Shipped
- Create archive snapshot
- Update DESIGN_LINKS.md

#### Any → Superseded

**Requirements:**
- Human decision (Gate #3)
- Replacement identified

**Actions:**
- Update STATUS.md: state = Superseded
- Add SUPERSEDED-BY reference
- Move to archive
- Update indexes

---

## compressed-artifacts

**Purpose:** Generate pre-compressed A₀ and B₀ artifacts.

**Location:** `skills/compressed-artifacts/SKILL.md`

### Frontmatter

```yaml
---
name: compressed-artifacts
description: Generate pre-compressed A₀ (always-on contract) and B₀ (playbooks) from live artifacts.
---
```

### Procedure

#### Generate A₀

```markdown
Read governance/live/*

Extract:
- Goal from TARGET.md
- Boundary law from BOUNDARY.md
- Blocker count from BLOCKERS.md
- DoD progress from TARGET.md
- Convergence mode from TARGET.md

Generate A0-contract.md:

# Always-On Contract

## Hard Rules
1. Work justified by blocker or DoD
2. No deferral (escalate instead)
3. No resurrection (boundary law: [extracted])
4. Metrics move monotonically
5. Evidence required
6. Single blocker per phase
7. Update artifacts immediately

## Current State
- Goal: [extracted]
- Blockers: [N] active
- DoD Progress: [X]/[Y]
- Convergence Mode: [yes/no]

## Escalation Threshold
Normal: N=2 | Convergence: N=1

Write to: governance/compressed/A0-contract.md
```

#### Generate B₀

```markdown
Analyze TARGET.md goal keywords

Determine applicable playbooks:
- "migrate" → migration.md
- "refactor" → refactor.md
- "feature" → feature.md
- [other patterns]

For each applicable playbook:
- Copy template
- Fill in project-specific context
- Write to governance/compressed/B0-playbooks/

Update governance/compressed/B0-playbooks/index.md
```

### Scripts Called

- `regenerate-compressed.sh` — File operations

### When to Regenerate

- After `/loop:init`
- After any phase that updates TARGET, BOUNDARY, or METRICS
- After `/design:accept` applies governance deltas
- Manual trigger if artifacts edited directly

---

## Skill Interaction Patterns

### Phase Ritual Flow

```
Governor uses phase-ritual
    │
    ├── Step 1: artifact-io (read all)
    │
    ├── Step 2: blocker-scoring
    │
    ├── Step 3: (plan generation - internal)
    │
    ├── Step 4: (execution - may delegate)
    │      │
    │      └── If escalation: decision-gate
    │
    └── Step 5: artifact-io (write)
              │
              └── metric-measurement
                        │
                        └── compressed-artifacts (if changes)
```

### Design Acceptance Flow

```
Design-Curator uses design-lifecycle (accept)
    │
    ├── decision-gate (Gate #1)
    │
    ├── artifact-io (apply deltas)
    │
    └── compressed-artifacts (regenerate)
```

---

## Summary

Seven skills providing shared behavior:

| Skill | Core Function |
|-------|---------------|
| phase-ritual | 5-step convergence ritual |
| artifact-io | Artifact CRUD + validation |
| blocker-scoring | Prioritize blockers |
| metric-measurement | Measure + track metrics |
| decision-gate | Human decisions via AskUserQuestion |
| design-lifecycle | Proposal state machine |
| compressed-artifacts | Generate A₀/B₀ |

Agents call skills. Skills call scripts. Clean separation.
