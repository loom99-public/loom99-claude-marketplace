# Commands: Slash Command Specifications

This document defines all slash commands for the agent-control-loop plugin.

---

## Command Namespaces

| Namespace | Purpose |
|-----------|---------|
| `/loop:*` | Execution plane — phase ritual, governance management |
| `/design:*` | Design plane — proposals, lifecycle, consistency |
| `/intake:*` | Intent injection — human → design compilation |

---

## Execution Plane Commands

### /loop:init

**Purpose:** Bootstrap governance/ directory with 4 live artifacts.

**Signature:**
```
/loop:init [optional: goal statement]
```

**Arguments:**
- `goal` (optional): 1-2 sentence description of end state. If omitted, prompts interactively.

**Behavior:**

1. **Check existing governance**
   - If `governance/live/` exists: warn, offer backup + overwrite
   - If not: proceed

2. **Gather goal statement**
   - Use argument if provided
   - Otherwise: AskUserQuestion with examples

3. **Scan for boundaries**
   - Script: `scan-boundaries.sh`
   - Detect legacy/new code splits
   - Present options via AskUserQuestion

4. **Generate artifacts**
   - Spawn Governor agent (init mode)
   - Use artifact-io skill with artifact-templates
   - Script: `init-governance.sh` creates directory structure
   - Prompt for: non-goals, DoD items, metrics (via AskUserQuestion)

5. **Measure baselines**
   - Script: `measure-metrics.sh`
   - Capture initial values

6. **Generate compressed artifacts**
   - Skill: compressed-artifacts
   - Write A₀, B₀ to `governance/compressed/`

7. **Display summary**
   - Show created structure
   - Show baseline metrics
   - Suggest: `/loop:phase` to begin

**Agent:** Governor (init mode)

**Skills Used:**
- artifact-io
- compressed-artifacts
- decision-gate (for prompts)

**Scripts Used:**
- scan-boundaries.sh
- init-governance.sh
- measure-metrics.sh

**Output:**
```
═══════════════════════════════════════════════════════
Control Loop Initialized
═══════════════════════════════════════════════════════

Goal: [goal statement]

Directory Structure:
governance/
├── live/
│   ├── TARGET.md           [DoD: 0/N complete]
│   ├── BOUNDARY.md         [Bridge: path]
│   ├── BLOCKERS.md         [N active blockers]
│   └── METRICS.md          [N metrics tracking]
├── compressed/
│   ├── A0-contract.md
│   └── B0-playbooks/
└── PHASE-LOG.md            [Phase 0 recorded]

Baseline Metrics:
- [Metric 1]: [value] → [target]
- [Metric 2]: [value] → [target]

Next: /loop:phase to begin work
═══════════════════════════════════════════════════════
```

---

### /loop:phase

**Purpose:** Execute one phase of the minimal control loop.

**Signature:**
```
/loop:phase
```

**Arguments:** None

**Prerequisites:**
- `governance/live/` exists
- All 4 artifacts present

**Behavior:**

1. **Pre-flight checks**
   - Verify governance/ exists
   - Verify all artifacts readable
   - (Hook handles compressed artifact injection)

2. **Spawn Governor agent**
   - Pass phase ritual task

3. **Governor executes 5-step ritual**
   - Step 1: Restate artifacts (artifact-io skill)
   - Step 2: Select blocker (blocker-scoring skill)
   - Step 3: Generate plan
   - Step 4: Execute/delegate
   - Step 5: Record outcome (artifact-io skill)

4. **Handle outcomes**
   - ELIMINATED: Continue to summary
   - TRANSFORMED: Update blockers, continue
   - ESCALATED: Present via decision-gate skill (AskUserQuestion)
   - FAILED: Record failure, check attempt count

5. **Display summary**
   - Outcome, blocker addressed
   - Metrics delta
   - DoD progress
   - Next action recommendation

**Agent:** Governor

**Skills Used:**
- phase-ritual
- artifact-io
- blocker-scoring
- metric-measurement
- decision-gate (if escalation)

**Scripts Used:**
- measure-metrics.sh

**Output:**
```
═══════════════════════════════════════════════════════
Phase Complete
═══════════════════════════════════════════════════════

Outcome: ELIMINATED

Blocker: BLOCKER-001 - [description]
Method: [approach]
Evidence:
- [key evidence 1]
- [key evidence 2]

Metrics Delta:
  [Metric 1]: 12 → 11 (-1) ✓
  [Metric 2]: 8 → 5 (-3) ✓

DoD Progress: 4/7 complete (+1)

Blockers Remaining: 3

═══════════════════════════════════════════════════════
Next: /loop:phase (attack BLOCKER-002)
═══════════════════════════════════════════════════════
```

---

### /loop:status

**Purpose:** Quick snapshot of governance state without executing a phase.

**Signature:**
```
/loop:status
```

**Arguments:** None

**Behavior:**

1. **Read all artifacts**
   - Use artifact-io skill

2. **Calculate summaries**
   - DoD progress
   - Blocker count
   - Metric trends
   - Escalation count

3. **Display snapshot**
   - Current state
   - Health indicators
   - Recommended next action

**Agent:** None (command-level only, no agent spawn)

**Skills Used:**
- artifact-io (read-only)

**Output:**
```
═══════════════════════════════════════════════════════
Control Loop Status
═══════════════════════════════════════════════════════

Goal: [from TARGET.md]

DoD Progress: ████████░░ 5/7 (71%)

Convergence Mode: [active/inactive]

Blockers:
  Active: 4
  Top 3:
    1. BLOCKER-003: [description]
    2. BLOCKER-001: [description]
    3. BLOCKER-007: [description]
  Escalations: 1 pending decision

Metrics:
  Legacy imports:    12 → 0    (12 remaining)  ⚠
  Failing tests:     5 → 0     (5 remaining)   ✓
  Migration coverage: 75% → 100% (75% done)    ✓

Last Phase: [N] - [YYYY-MM-DD] - [outcome]

═══════════════════════════════════════════════════════
Recommended: /loop:escalate (resolve pending decision)
═══════════════════════════════════════════════════════
```

---

### /loop:escalate

**Purpose:** Present and resolve pending escalations.

**Signature:**
```
/loop:escalate [optional: blocker-id]
```

**Arguments:**
- `blocker-id` (optional): Specific blocker to escalate. If omitted, presents all pending.

**Behavior:**

1. **Load escalations from BLOCKERS.md**
   - Parse "Escalations Needed" section

2. **For each escalation:**
   - Spawn Escalation-Handler agent
   - Use decision-gate skill
   - Present AskUserQuestion with options

3. **Record decision**
   - Update BLOCKERS.md
   - Add to HISTORY.md
   - Update related artifacts if needed

**Agent:** Escalation-Handler

**Skills Used:**
- artifact-io
- decision-gate

**Output:**
```
═══════════════════════════════════════════════════════
Escalation: BLOCKER-005
═══════════════════════════════════════════════════════

Trigger: Boundary violation required to proceed

Context:
Test `test_user_profile` requires legacy store API not in bridge.
Attempts: 2/2 exhausted.

┌─────────────────────────────────────────────────────┐
│ Options:                                             │
│                                                      │
│ 1. Expand bridge                                    │
│    Add `getLegacyUser` to bridge surface            │
│    Pros: Unblocks immediately                       │
│    Cons: Bridge grows, more cleanup later           │
│                                                      │
│ 2. Quarantine test                                  │
│    Mark test as migration-pending                   │
│    Pros: No bridge expansion                        │
│    Cons: Test coverage gap until migrated           │
│                                                      │
│ 3. Delete test                                      │
│    Test behavior no longer needed                   │
│    Pros: Clean, no future work                      │
│    Cons: Potential behavior loss                    │
│                                                      │
│ Recommended: Option 1 (Expand bridge)               │
│                                                      │
└─────────────────────────────────────────────────────┘

[AskUserQuestion presented]
```

---

## Design Plane Commands

### /design:propose

**Purpose:** Create a new design proposal.

**Signature:**
```
/design:propose [description]
```

**Arguments:**
- `description`: Brief description of what's being proposed

**Behavior:**

1. **Generate proposal ID**
   - Format: `P-####-slug`

2. **Create proposal directory**
   - `design/proposals/P-####-slug/`

3. **Spawn Design-Curator agent**
   - Use design-lifecycle skill

4. **Prompt for proposal content**
   - AskUserQuestion for: problem, goals, non-goals, approach, risks

5. **Generate PROPOSAL.md and STATUS.md**

6. **Display summary**
   - Proposal location
   - Next steps

**Agent:** Design-Curator

**Skills Used:**
- design-lifecycle
- decision-gate

**Output:**
```
═══════════════════════════════════════════════════════
Proposal Created: P-0003-new-auth-system
═══════════════════════════════════════════════════════

Location: design/proposals/P-0003-new-auth-system/

Files:
- PROPOSAL.md
- STATUS.md (state: Proposed)

Next:
- Review and refine PROPOSAL.md
- When ready: /design:accept P-0003
═══════════════════════════════════════════════════════
```

---

### /design:accept

**Purpose:** Accept a proposal and promote to active design.

**Signature:**
```
/design:accept [proposal-id]
```

**Arguments:**
- `proposal-id`: ID of proposal to accept (e.g., `P-0003`)

**Behavior:**

1. **Validate proposal exists and is in InReview state**

2. **Spawn Design-Curator agent**

3. **Generate GOVERNANCE-DELTA.md**
   - What changes to TARGET, BOUNDARY, METRICS

4. **Present Gate #1 (AskUserQuestion)**
   - Show governance deltas
   - Show risks
   - Confirm acceptance

5. **If accepted:**
   - Create `design/active/A-####-slug/`
   - Copy SPEC.md
   - Apply governance deltas
   - Update DESIGN_LINKS.md
   - Regenerate compressed artifacts

**Agent:** Design-Curator

**Skills Used:**
- design-lifecycle
- artifact-io
- decision-gate
- compressed-artifacts

**Human Gate:** Gate #1 (Accept Proposal)

---

### /design:ship

**Purpose:** Mark an active design as shipped/complete.

**Signature:**
```
/design:ship [active-id]
```

**Arguments:**
- `active-id`: ID of active design to ship (e.g., `A-0003`)

**Behavior:**

1. **Validate active design exists**

2. **Spawn Design-Curator agent**

3. **Verify acceptance criteria**
   - Check metrics reached targets
   - Check DoD items complete

4. **Present Gate #2 (AskUserQuestion)**
   - Show acceptance criteria checklist
   - Show any gaps
   - Confirm ship

5. **If shipped:**
   - Transition state: Active → Shipped
   - Archive to `design/archive/YYYY/`
   - Update DESIGN_LINKS.md
   - Create completion snapshot

**Agent:** Design-Curator

**Skills Used:**
- design-lifecycle
- artifact-io
- decision-gate

**Human Gate:** Gate #2 (Ship Design)

---

### /design:sync

**Purpose:** Check consistency between design plane and execution plane.

**Signature:**
```
/design:sync
```

**Arguments:** None

**Behavior:**

1. **Spawn Design-Curator agent**

2. **Compare design/current vs governance/live**
   - Check for conflicts

3. **Compare design/current vs repo reality**
   - Check for drift

4. **Compare active designs vs blockers**
   - Check alignment

5. **Report findings**
   - Conflicts found
   - Drift detected
   - Recommendations

6. **If issues found:**
   - Present options via AskUserQuestion
   - May trigger Gate #3 (Supersede) if needed

**Agent:** Design-Curator

**Skills Used:**
- design-lifecycle
- artifact-io
- decision-gate (if issues found)

---

## Intake Commands

### /intake:create

**Purpose:** Create a new intake document for human intent injection.

**Signature:**
```
/intake:create [description]
```

**Arguments:**
- `description`: Brief description of the new intent

**Behavior:**

1. **Generate intake ID**
   - Format: `I-####-slug`

2. **Create intake directory**
   - `design/intake/I-####-slug/`

3. **Spawn Intake-Compiler agent**

4. **Prompt for intake primitives**
   - AskUserQuestion for each:
     - User-facing outcome
     - Technical outcome
     - Constraints
     - Non-goals
     - Acceptance checks
     - Open questions

5. **Generate INTAKE.md and STATUS.md**

**Agent:** Intake-Compiler

**Skills Used:**
- decision-gate

---

### /intake:compile

**Purpose:** Compile an intake into one or more design proposals.

**Signature:**
```
/intake:compile [intake-id]
```

**Arguments:**
- `intake-id`: ID of intake to compile (e.g., `I-0001`)

**Behavior:**

1. **Read intake document**

2. **Spawn Intake-Compiler agent**

3. **Analyze and generate candidate designs**
   - May generate 1-3 alternatives

4. **Present options via AskUserQuestion**
   - Show each candidate
   - Show tradeoffs
   - Recommend one

5. **Create proposal(s)**
   - Call `/design:propose` internally
   - Link back to intake

6. **Update intake STATUS.md**
   - Mark as: Compiled

**Agent:** Intake-Compiler

**Skills Used:**
- design-lifecycle
- decision-gate

---

## Command Frontmatter Templates

### /loop:init

```yaml
---
argument-hint: [optional: goal statement]
description: Bootstrap governance/ directory with 4 live artifacts. Prompts for goal, scans repo for boundaries, generates TARGET, BOUNDARY, BLOCKERS, METRICS.
---
```

### /loop:phase

```yaml
---
argument-hint: (none)
description: Execute one phase of the control loop. Runs phase ritual via Governor agent.
---
```

### /loop:status

```yaml
---
argument-hint: (none)
description: Quick snapshot of governance state. Shows DoD progress, blockers, metrics, recommendations.
---
```

### /loop:escalate

```yaml
---
argument-hint: [optional: blocker-id]
description: Present and resolve pending escalations via structured decision prompts.
---
```

### /design:propose

```yaml
---
argument-hint: [description]
description: Create a new design proposal. Prompts for problem, goals, approach, risks.
---
```

### /design:accept

```yaml
---
argument-hint: [proposal-id]
description: Accept a proposal and promote to active design. Applies governance deltas.
---
```

### /design:ship

```yaml
---
argument-hint: [active-id]
description: Mark an active design as shipped. Verifies acceptance criteria, archives.
---
```

### /design:sync

```yaml
---
argument-hint: (none)
description: Check consistency between design plane and execution plane. Reports conflicts and drift.
---
```

### /intake:create

```yaml
---
argument-hint: [description]
description: Create a new intake document for human intent injection.
---
```

### /intake:compile

```yaml
---
argument-hint: [intake-id]
description: Compile an intake into design proposals. Analyzes intent, generates candidates.
---
```

---

## Error Handling

### Governance Missing

```
ERROR: Governance directory not found.

The control loop has not been initialized.

To fix: Run /loop:init to create governance structure
```

### Artifact Missing

```
ERROR: Missing required artifact: governance/live/BLOCKERS.md

To fix:
1. Check if file was accidentally deleted
2. Or run /loop:init to regenerate (will overwrite existing)
```

### Artifact Validation Failed

```
ERROR: Artifact validation failed: TARGET.md

Issues:
- Goal is empty
- DoD has only 1 item (minimum 3)

To fix: Edit governance/live/TARGET.md and correct issues
```

### Proposal Not Found

```
ERROR: Proposal not found: P-9999

Available proposals:
- P-0001-auth-refactor (Proposed)
- P-0002-new-store (InReview)

To fix: Check proposal ID and try again
```

### No Blockers But DoD Incomplete

```
WARNING: Zero blockers but DoD is only 5/7 complete

Work is missing from the blocker queue.

To fix:
1. Review governance/live/TARGET.md DoD section
2. For each incomplete item, identify what blocks it
3. Add blockers to governance/live/BLOCKERS.md
4. Run /loop:phase
```

---

## Summary

| Command | Agent | Purpose |
|---------|-------|---------|
| `/loop:init` | Governor | Bootstrap governance |
| `/loop:phase` | Governor | Execute one phase |
| `/loop:status` | (none) | Quick snapshot |
| `/loop:escalate` | Escalation-Handler | Resolve escalations |
| `/design:propose` | Design-Curator | Create proposal |
| `/design:accept` | Design-Curator | Accept → active |
| `/design:ship` | Design-Curator | Active → shipped |
| `/design:sync` | Design-Curator | Check consistency |
| `/intake:create` | Intake-Compiler | Create intake |
| `/intake:compile` | Intake-Compiler | Intake → proposal |
