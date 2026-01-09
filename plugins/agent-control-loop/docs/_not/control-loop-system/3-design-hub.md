## Prompt:
Let's say I have high level architectural design documents, a proposed state of the system.  How do I integrate into this system the higher level big picture (but still highly technical and detailed, may include functional architecture, user facing features, desired UX outcomes or goals) documents into this system.  These documents may be: proposals for the future, concrete 'this is the architecture we need to ship feature XYZ or UX necessity ABC', previous design documents which were once true but are now legacy, or rejected proposals that didn't work out.  Everything a real world product that has been shipped and iterated on over time necessarily accumulates

## Response:
### 1) Add a single “Design Hub” namespace with strict states

```
/design
  README.md                 # taxonomy + state machine + linking rules
  index.md                  # curated entrypoints (current + active proposals)

/design/current             # authoritative “big picture” for what we’re building now
  /north-star
    OVERVIEW.md             # functional architecture + UX goals + non-goals
    ARCHITECTURE.md         # component model, interfaces, data/control flow
    CONSTRAINTS.md          # perf, latency, security, operability, platform limits
    ADR-INDEX.md            # links to ADRs that bind this architecture
  /features
    F-0123-xyz.md           # design spec for feature XYZ (current version)
  /ux
    UX-0045-abc.md          # UX requirement/goal spec (current version)

/design/proposals           # not authoritative; candidate futures
  /P-0201-new-renderer
    PROPOSAL.md             # problem, goals, design, risks, migration impact
    STATUS.md               # Proposed | InReview | Accepted | Rejected | OnIce
    EVIDENCE/               # benchmarks, experiments, links

/design/active              # accepted proposals under execution (bridge to governance)
  /A-0201-new-renderer
    SPEC.md                 # “accepted design” pinned for current execution window
    GOVERNANCE-DELTA.md     # exact deltas intended for governance/live/*
    RISKS.md                # only if needed; otherwise reference governance/RISK_REGISTER
    LINKS.md                # pointers to slices, PRs, benchmarks

/design/archive              # immutable history (was true, now legacy)
  /2025
    /D-0140-old-compiler-arch__superseded-2025-11-03
      DOCS/                 # frozen snapshot
      SUPERSEDED-BY.md      # points to new current docs + why it changed
  /rejected
    /R-0099-foo
      PROPOSAL.md
      REJECTION.md
      EVIDENCE/
```

* * *

### 2) Make “current” authoritative, everything else non-binding

*   `/design/current/**` is the _only_ place the agent treats as “big picture truth”.
*   `/design/proposals/**` is input material; it cannot justify work directly.
*   `/design/archive/**` is read-only; it exists to prevent archaeology and re-litigation.

This mirrors the governance separation:

*   **governance/live** = operational constraints “now”
*   **design/current** = architectural intent “now”
*   proposals/archive = memory and options

* * *

### 3) Link design ↔ governance with a single explicit interface

Add one file under governance that defines what parts of design are binding:

```
/governance/live/DESIGN_LINKS.md
```

Contents:

*   Pointers to the canonical “current” design docs (paths, versions)
*   A rule: “If design/current conflicts with governance/live, governance wins until DESIGN\_LINKS is updated.”

Purpose: prevents the agent from “choosing” whichever doc it likes.

* * *

### 4) Use lightweight ADRs for binding decisions only

Introduce:

```
/design/current/north-star/adr/
  ADR-0001-bridge-boundary.md
  ADR-0002-cutover-strategy.md
  ...
```

Rules:

*   ADRs record **irreversible** or **cross-cutting** decisions only.
*   ADRs are short, and each ADR must link to the specific sections in:
    *   design/current that it supports
    *   governance/live that it constrains

This prevents design docs from becoming a second governance system.

* * *

### 5) Define a lifecycle state machine for every design artifact

In `/design/README.md`, define states and transitions:

*   **Proposed** → **InReview** → **Accepted** → **Active** → **Superseded** → **Archived**
*   **Rejected** is terminal

Mechanics:

*   “Accepted” means: copied/linked into `/design/active/*` and referenced in `DESIGN_LINKS.md`
*   “Active” means: slice work exists in `/governance/roadmap` or `/governance/live/BLOCKERS.md`
*   “Superseded” means: moved to `/design/archive` with `SUPERSEDED-BY.md`

No doc is “sort of true.” It has a state.

* * *

### 6) Integrate with roadmap/completed slices via deltas, not duplication

When a design becomes active, add `GOVERNANCE-DELTA.md` under `/design/active/<id>/` that contains _only_:

*   changes required to `TARGET.md`
*   changes required to `BOUNDARY.md`
*   any new metrics required
*   any new blockers that must be created

Then, when work completes:

*   snapshot the final `SPEC.md` into `/governance/completed/...` alongside governance snapshots
*   and mark the active design as **Superseded** or **Shipped** (your choice of vocabulary)

This gives you traceability without turning design into a second plan.

* * *

### 7) Practical rules that keep it sane

1.  **One canonical current architecture**: `/design/current/north-star/*`
2.  **Everything else must declare its state** (`STATUS.md` or filename suffix)
3.  **Only “current” + “active” may influence execution**
4.  **Anything superseded must point forward** (`SUPERSEDED-BY.md`)
5.  **The only bridge into execution is governance deltas** (prevents scope creep)