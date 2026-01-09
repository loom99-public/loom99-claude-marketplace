# Design Hub: Design Plane Details

This document defines the design plane — how architecture intent is captured, evolved, and bridged to execution.

---

## Design Principle: Two Planes of Truth

The system maintains two separate planes:

**Execution Plane** (`governance/live/`) — What must be true right now
- 4 live artifacts: TARGET, BOUNDARY, BLOCKERS, METRICS
- Binding for all execution decisions
- Updated every phase

**Design Plane** (`design/`) — What we intend to build
- Architecture vision and specs
- Proposals and active designs
- Historical record
- Influences execution only via explicit bridge

The planes are connected by `governance/live/DESIGN_LINKS.md`.

---

## Directory Structure

```
design/
├── README.md                    # Taxonomy, state machine, rules
├── index.md                     # Curated entrypoints
│
├── current/                     # Authoritative big picture
│   └── north-star/
│       ├── OVERVIEW.md          # Functional architecture + UX goals
│       ├── ARCHITECTURE.md      # Component model, interfaces, data flow
│       ├── CONSTRAINTS.md       # Perf, latency, security limits
│       ├── ADR-INDEX.md         # Links to binding ADRs
│       └── adr/
│           └── ADR-XXXX-*.md    # Architecture Decision Records
│
├── proposals/                   # Candidate futures (non-binding)
│   └── P-####-slug/
│       ├── PROPOSAL.md          # The proposal content
│       ├── STATUS.md            # Lifecycle state
│       └── EVIDENCE/            # Supporting evidence
│
├── active/                      # Under execution (binding via DESIGN_LINKS)
│   └── A-####-slug/
│       ├── SPEC.md              # Full specification
│       ├── STATUS.md            # Lifecycle state
│       ├── GOVERNANCE-DELTA.md  # Changes to governance/live/*
│       └── LINKS.md             # References to blockers, slices
│
├── intake/                      # Human intent injection
│   └── I-####-slug/
│       ├── INTAKE.md            # Intent primitives
│       ├── STATUS.md            # Compilation state
│       └── NOTES.md             # Discussion, decisions
│
└── archive/                     # Immutable history
    ├── YYYY/                    # By year
    │   └── A-####-slug/         # Shipped designs
    └── rejected/                # Rejected proposals
        └── P-####-slug/
```

---

## Authority Model

| Source | Binding? | Scope |
|--------|----------|-------|
| `governance/live/*` | **YES** | Execution decisions |
| `design/current/*` | YES (via DESIGN_LINKS) | Architecture intent |
| `design/active/*` | YES (via DESIGN_LINKS) | Active specifications |
| `design/proposals/*` | NO | Candidate futures |
| `design/intake/*` | NO | Raw intent |
| `design/archive/*` | NO | Historical reference |

### Conflict Resolution

If `governance/live` conflicts with `design/current`:
1. **Governance wins** for execution
2. Agent raises supersession gate (Gate #3)
3. One must be updated to resolve conflict

If `design/active` conflicts with `design/current`:
1. Raise supersession gate
2. Determine which is canonical
3. Archive the superseded version

---

## Lifecycle State Machine

```
                    ┌──────────────┐
                    │   Drafted    │ (internal only)
                    └──────┬───────┘
                           │ submit
                           ▼
                    ┌──────────────┐
                    │   Proposed   │
                    └──────┬───────┘
                           │ review begins
                           ▼
┌───────────┐       ┌──────────────┐       ┌───────────┐
│   OnIce   │◄──────│   InReview   │──────►│  Rejected │
└───────────┘ defer └──────┬───────┘ reject└─────┬─────┘
                           │ accept              │
                           │ (Gate #1)           │
                           ▼                     │
                    ┌──────────────┐             │
                    │   Accepted   │             │
                    └──────┬───────┘             │
                           │ promote             │
                           ▼                     │
                    ┌──────────────┐             │
                    │    Active    │◄──┐         │
                    └──────┬───────┘   │         │
                           │ complete  │ supersede
                           │ (Gate #2) │ (Gate #3)
                           ▼           │         │
                    ┌──────────────┐   │         │
                    │   Shipped    │───┘         │
                    └──────┬───────┘             │
                           │ archive             │
                           ▼                     ▼
                    ┌──────────────────────────────┐
                    │          Archived            │
                    └──────────────────────────────┘
```

### States

| State | Description | Location |
|-------|-------------|----------|
| Drafted | Work in progress, not yet submitted | `proposals/` |
| Proposed | Submitted for review | `proposals/` |
| InReview | Under active review | `proposals/` |
| OnIce | Paused, revisit later | `proposals/` |
| Accepted | Approved, pending promotion | `proposals/` → `active/` |
| Active | Under execution | `active/` |
| Shipped | Implementation complete | `active/` → `archive/` |
| Superseded | Replaced by newer design | `archive/` |
| Rejected | Not viable | `archive/rejected/` |
| Archived | Historical record | `archive/` |

### Transitions Requiring Human Approval

| Transition | Gate | Presented By |
|------------|------|--------------|
| InReview → Accepted | Gate #1 | Design-Curator |
| Active → Shipped | Gate #2 | Design-Curator |
| Any → Superseded | Gate #3 | Design-Curator |
| Any → Rejected | Gate #4 | Design-Curator |

---

## Document Templates

### PROPOSAL.md

```markdown
# Proposal: [Title]

## ID
P-####-slug

## Status
[Proposed | InReview | OnIce]

## Summary
[1-2 paragraph overview]

## Problem
[What problem does this solve?]

## Goals
- [Goal 1]
- [Goal 2]

## Non-Goals
- [Explicit exclusion 1]
- [Explicit exclusion 2]

## Proposed Approach
[Architecture overview, key decisions]

## Alternatives Considered
1. [Alternative A] — [Why not chosen]
2. [Alternative B] — [Why not chosen]

## Risks
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Open Questions
- [Question 1]
- [Question 2]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## References
- [Link to intake if applicable]
- [Related proposals]
```

### STATUS.md (for proposals)

```markdown
# Status: P-####

## Current State
[Proposed | InReview | OnIce | Accepted]

## History
| Date | From | To | By | Notes |
|------|------|----|----|-------|
| YYYY-MM-DD | - | Proposed | [author] | Initial submission |
| YYYY-MM-DD | Proposed | InReview | system | Review started |

## Review Notes
[Feedback, questions, concerns]

## Blockers to Acceptance
- [What needs to be resolved]
```

### SPEC.md (for active designs)

```markdown
# Specification: [Title]

## ID
A-####-slug

## Origin
Promoted from: P-####

## Overview
[Complete specification of the design]

## Architecture
[Detailed architecture description]

### Components
[Component breakdown]

### Interfaces
[API/interface definitions]

### Data Model
[Data structures, schemas]

### Control Flow
[How components interact]

## Constraints
- [Performance requirement]
- [Security requirement]
- [Compatibility requirement]

## Implementation Notes
[Guidance for implementers]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
```

### GOVERNANCE-DELTA.md

```markdown
# Governance Delta: A-####

## Changes to TARGET.md

### Goal
[No change OR new goal text]

### Non-Goals
- [+] [New non-goal] (add)
- [-] [Old non-goal] (remove)

### Target Shape
- [+] [New bullet] (add)
- [~] [Modified bullet] (update)

### Definition of Done
- [+] [ ] [New DoD item]

## Changes to BOUNDARY.md

### Bridge Surface
- [+] [New function] — [purpose]

### Forbidden Dependencies
[No change OR additions]

### Exceptions
[New exceptions if needed]

## Changes to METRICS.md

### New Metrics
- [Metric name]: [definition, measurement, target]

### Modified Metrics
- [Metric name]: [change description]

## Initial Blockers

### BLOCKER-NEW-1: [Title]
**Observable Failure:** [What fails]
**Impact:** Blocks DoD item "[item]"
**Evidence:** [Initial evidence]
```

---

## Intake System

Intake is how humans inject **new ends** into the system.

### INTAKE.md Template

```markdown
# Intake: [Title]

## ID
I-####-slug

## User-Facing Outcome
[What must become true for users]

## Technical Outcome
[What must become true in the system]

## Constraints
- [Performance constraint]
- [Security constraint]
- [Compatibility constraint]

## Non-Goals
- [What we explicitly won't do]

## Acceptance Checks
- [ ] [Observable verification 1]
- [ ] [Observable verification 2]

## Open Questions
- [Unknown 1]
- [Unknown 2]

## Priority Notes
[What matters most if tradeoffs appear]
```

### Intake Workflow

```
Human creates INTAKE.md
         │
         ▼
/intake:compile I-####
         │
         ▼
┌─────────────────────────────────┐
│ Intake-Compiler agent           │
│ - Analyze intent                │
│ - Generate 1-3 candidate designs│
│ - Present via AskUserQuestion   │
└─────────────────────────────────┘
         │
         ▼
Human selects approach
         │
         ▼
Create proposal in design/proposals/
         │
         ▼
Normal proposal lifecycle
```

---

## Design ↔ Governance Bridge

### DESIGN_LINKS.md

```markdown
# Design Links

## Canonical Design Documents
- design/current/north-star/OVERVIEW.md
- design/current/north-star/ARCHITECTURE.md

## Active Designs
| ID | Title | Status | SPEC Location |
|----|-------|--------|---------------|
| A-0001 | Auth Migration | Active | design/active/A-0001/ |
| A-0002 | New Store | Active | design/active/A-0002/ |

## Precedence Rule
If design/current conflicts with governance/live, **governance/live wins** until this file is updated.

## Last Sync
[YYYY-MM-DD HH:MM] - [Notes on last consistency check]
```

### Sync Process

When `/design:sync` runs:

1. **Compare design/current vs governance/live**
   - Check TARGET aligns with OVERVIEW
   - Check BOUNDARY aligns with ARCHITECTURE
   - Flag conflicts

2. **Compare design/current vs repo reality**
   - Check actual code matches architecture
   - Flag drift

3. **Compare active designs vs blockers**
   - Check active designs have corresponding blockers
   - Flag orphaned designs

4. **Report findings**
   - Present via AskUserQuestion if action needed
   - Update DESIGN_LINKS with sync timestamp

---

## Design-Curator Agent Responsibilities

The Design-Curator agent owns the design plane:

### Autonomy (no human approval needed)

- Fix metadata, indices, broken links
- Move docs to archive when terminal
- Update index.md to reflect states
- Generate consistency reports
- Create GOVERNANCE-DELTA drafts

### Requires Human Approval (via gates)

- Gate #1: Accept proposal (InReview → Accepted)
- Gate #2: Ship design (Active → Shipped)
- Gate #3: Supersede design (Any → Superseded)
- Gate #4: Reject proposal (Any → Rejected)

### Agent Cannot

- Change `design/current` without gate
- Apply governance deltas without acceptance
- Delete historical documents
- Override governance/live authority

---

## Consistency Checks

### Built into /design:sync

Run on-demand to check:

1. **Design/Current ↔ Governance/Live**
   - OVERVIEW goals match TARGET goal
   - ARCHITECTURE constraints match BOUNDARY
   - ADRs don't conflict with active rules

2. **Design/Current ↔ Repo Reality**
   - Documented components exist
   - Documented interfaces match code
   - No undocumented major components

3. **Active Designs ↔ Blockers**
   - Every active design has blockers
   - Blockers reference valid designs
   - No orphaned blockers/designs

### Built into /design:accept

Before accepting proposal:

1. Check GOVERNANCE-DELTA is valid
2. Verify no conflicts with current governance
3. Ensure blockers can be created

### Built into design-sync-check hook

After any `/design:*` command:

1. Quick check: active count matches DESIGN_LINKS
2. Warn if mismatch detected

---

## Archival Process

### When Design Ships (Gate #2)

1. Create archive directory: `design/archive/YYYY/A-####-slug/`
2. Copy all files from `design/active/A-####/`
3. Add ARCHIVED.md with:
   - Ship date
   - Acceptance criteria results
   - Final metrics
   - Lessons learned (if any)
4. Update STATUS.md: state = Archived
5. Remove from DESIGN_LINKS active list
6. Update index.md

### When Design Superseded (Gate #3)

1. Add SUPERSEDED-BY.md pointing to replacement
2. Move to archive
3. Update all references to point to new design
4. Record in HISTORY.md

### When Proposal Rejected (Gate #4)

1. Move to `design/archive/rejected/P-####/`
2. Add REJECTED.md with:
   - Rejection reason
   - Date
   - Alternative paths (if any)
3. Update index.md

---

## ADR (Architecture Decision Records)

### Location

`design/current/north-star/adr/`

### Format

```markdown
# ADR-XXXX: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue we're addressing?]

## Decision
[What did we decide?]

## Consequences
[What are the positive and negative implications?]

## References
- [Related ADRs]
- [Design documents]
```

### ADR Lifecycle

- ADRs in `design/current/adr/` are binding
- Superseded ADRs stay in place with forward pointers
- Never delete ADRs — they are historical record

---

## Commands Summary

| Command | Purpose |
|---------|---------|
| `/design:propose [desc]` | Create new proposal |
| `/design:accept P-####` | Accept proposal → active |
| `/design:ship A-####` | Ship active → archived |
| `/design:sync` | Check consistency |
| `/intake:create [desc]` | Create new intake |
| `/intake:compile I-####` | Compile intake → proposal |

---

## Best Practices

### Proposal Quality

1. **Clear problem statement** — What exactly are we solving?
2. **Explicit non-goals** — What won't we do?
3. **Alternatives considered** — Why this approach?
4. **Risks identified** — What could go wrong?
5. **Acceptance criteria** — How do we know it's done?

### Design Hygiene

1. **One source of truth** — design/current is canonical
2. **No zombie docs** — Archive or delete outdated docs
3. **Forward pointers** — Superseded docs point to replacements
4. **Sync regularly** — Run `/design:sync` periodically

### Intake Quality

1. **User-facing first** — Start with user outcome
2. **Constraints explicit** — Don't leave them implicit
3. **Non-goals clear** — Prevent scope creep
4. **Acceptance observable** — Must be testable

---

## Summary

The design plane provides:

1. **Architecture vision** — `design/current/` holds canonical truth
2. **Proposal lifecycle** — Ideas → Review → Active → Shipped
3. **Intent injection** — Intake captures human creativity
4. **History** — Archive preserves decisions
5. **Governance bridge** — DESIGN_LINKS connects to execution

Design influences execution only through explicit gates and the DESIGN_LINKS bridge. Governance/live always wins for immediate execution decisions.
