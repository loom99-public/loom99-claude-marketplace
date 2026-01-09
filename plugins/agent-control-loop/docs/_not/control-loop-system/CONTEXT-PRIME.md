# CONTEXT-PRIME: Minimal Control Loop System

This document primes an agent to implement or iterate on the minimal control loop system for driving LLM agents toward convergence on complex, high-risk software engineering work.

CRITICAL: use the following agents whenever appropriate: agent-creator, skill-reviewer, plugin-validator
agent-creator: when creating an agent
skill-reviewer: when reviewing a skill
plugin-validator: when validating a plugin

CRITICAL: use the following skills:
command-development: any time you are creating or updating a command
skill-development: any time you are creating or updating a skill
plugin-settings: any time you are creating or updating a plugin
hook-development: any time you are creating or updating a hook
agent-development: any time you are creating or updating a agent

This plugin should be designed with a workflow that is slash command driven (using command-development) and calls out to agents (agent-creator, agent-development) within the slash commands

Keep the implementation tight, intentional, and light-touch.

---

## Part I: The Problem Space

### Why LLMs Fail at Complex Work

LLMs excel at **expansive, low-risk work**:
- Moving files, renaming symbols, updating imports
- Mechanical edits with high pattern similarity
- Obvious transformations with low ambiguity

LLMs struggle with **convergent, high-risk work**:
- Edge cases and cross-cutting invariants
- Data model inconsistencies and migration logic
- Backward compatibility and tests that no longer compile

When faced with uncertainty, internal objectives conflict:
- "Make progress" vs. "Don't introduce errors"
- "Don't hallucinate" vs. "Don't break tests"
- "Don't touch unknowns"

The agent cannot trade these off, so it **escapes via deferral**:
> "We should handle this later." / "This is out of scope." / "Add a TODO."

This is not laziness. This is **uncertainty collapse**.

### The 80% Stall Phenomenon

Large refactors have two phases:

**Phase 1 (0-80%)**: Expansive work. High pattern similarity, low risk. Transformers love this.

**Phase 2 (80-95%+)**: Convergent work. Every change risks breaking something. The model's escape hatch is deferral.

The last 20% is not a pattern problem—it is a **responsibility problem**. Unless explicitly told "you are responsible for closure," the agent will push hard work into the future indefinitely.

### The Three Classic Failure Modes

1. **Deferral**: Creating "future sprint" items instead of resolving blockers
2. **Resurrection**: Reintroducing legacy code to make tests pass
3. **Plan Drift**: Following outdated plans that refer to a past target state

---

## Part II: The Core Insight

### What Agents Actually Need

Agents do not need comprehensive governance documents.

They need **three pressure gradients** that make bad behavior expensive and good behavior cheap:

1. **A visible target** — what "done" means
2. **A visible boundary** — what is forbidden
3. **A visible notion of "not done"** — what blocks completion

Everything else is refinement.

### Local Gradients, Not Rules

Transformers don't remember rules. They re-weight what looks relevant to the current moment. Rules survive only if:
- Kept near the present (restated/used immediately before work)
- Expressed in compressed, conflict-free form

LLMs operate on local gradients:
- "Am I closer to target?"
- "Am I violating a boundary?"
- "Is there still a blocker?"
- "Did the number go down?"

The system creates these gradients mechanically. The agent cannot escape them.

---

## Part III: The Minimal Control Loop

### Four Live Artifacts

These define **what must be true right now**. Each must fit on one screen. Updated continuously.

```
/governance/live/
  TARGET.md     — target end state + Definition of Done
  BOUNDARY.md   — single boundary rule + allowed bridge
  BLOCKERS.md   — exhaustive list of ship-stoppers (the only work queue)
  METRICS.md    — 2-4 monotonic measures of convergence
```

#### TARGET.md Structure
- **Goal statement** (1-2 lines)
- **Non-goals** (explicit exclusions)
- **Target shape** (5-10 bullets: modules, interfaces, behaviors)
- **Definition of Done** (checklist: build, tests, runtime smoke, migration)

**Agent rule**: Any proposed work must cite which DoD item or target-shape bullet it advances.

#### BOUNDARY.md Structure
- **Boundary law** (single sentence): "New code must not import/call legacy except through `<bridge>`."
- **Bridge definition**: module/path and allowed surface (APIs)
- **Forbidden dependencies**: list of disallowed modules/symbols outside bridge
- **Temporary exceptions**: each with expiry condition tied to a blocker

**Agent rule**: If a test failure tempts "bring back old code," the agent must instead: migrate the test, gate behind bridge/flag, or escalate.

#### BLOCKERS.md Structure
- **Active blockers** (bulleted list):
  - Short identifier
  - Observable failure mode (exact error, failing test, broken path)
  - Impact (which DoD item it blocks)
  - Evidence link
- **Escalations needed**: questions requiring user decisions with options + consequences

**Agent rule**: Only blockers can justify work. Anything else is either unnecessary or should be added as a blocker with evidence.

#### METRICS.md Structure
- 2-4 metrics with: definition, measurement method, current value, target value, last delta
- **Recommended metrics**:
  - Count of forbidden legacy imports (outside bridge)
  - Count of failing tests in "must-pass" category
  - Count of quarantined tests
  - Count of reachable legacy UI entrypoints

**Agent rule**: Each phase must move at least one metric or eliminate a blocker. Stagnation triggers escalation.

### The Phase Ritual

At the start of every work phase, the agent must:

1. **Restate artifacts**: Current contents of TARGET, BOUNDARY, BLOCKERS, METRICS (verbatim or near-verbatim)
2. **Select single blocker**: Exactly one, justified using TARGET and METRICS (not preferences)
3. **Plan for phase**: Max 3-7 steps, each with observable verification
4. **Define stop conditions**: When to escalate, when to update artifacts

At the end of each phase:
- Record outcome: eliminated / transformed / escalated
- Update artifacts accordingly
- Update metrics with delta

### Prohibited Behaviors (Global)

- Creating "future sprint" items instead of resolving blockers
- Expanding scope not tied to a blocker
- Reintroducing legacy code paths to satisfy tests (unless explicitly permitted)
- Declaring completion without meeting DoD and clearing BLOCKERS

### Convergence Mode

When reaching ~80% completion, activate convergence mode explicitly:

> "We are entering convergence mode. The only goal is to eliminate blockers and make the system build and pass tests. No new features. No deferrals. Every remaining issue must be either fixed or explicitly resolved."

Force three behaviors:
1. **Enumerate blockers**: List everything preventing correctness/build/release
2. **Choose one**: Pick the single highest-risk blocker. No parallelism.
3. **Require closure**: Produce a patch or explain precisely why it cannot be resolved

---

## Part IV: Agent Roles

### Governor (Required)

Owns the minimal control loop:
- Maintains 4 live artifacts
- Chooses next blocker to attack
- Decides when to escalate to user
- Prevents scope drift, resurrection, and unbounded planning

### Executor (Optional)

Performs repo modifications as directed:
- Reports concrete results (diffs, test output, logs, metrics deltas)

### Inspector (Optional)

Collects repo facts:
- Dependency graph, failing tests, legacy import coverage
- Produces evidence for the Governor

The Governor can subsume Executor/Inspector if the runtime supports it.

---

## Part V: The Design Plane

### Two Planes of Truth

**Execution Plane** (`/governance/live/`): What must be true right now. Binding.

**Design Plane** (`/design/`): What we intend to build. Influences execution only via explicit bridge.

### Design Hub Structure

```
/design/
  README.md                  — taxonomy + state machine + linking rules
  index.md                   — curated entrypoints

/design/current/             — authoritative big picture (binding via DESIGN_LINKS)
  /north-star/
    OVERVIEW.md              — functional architecture + UX goals + non-goals
    ARCHITECTURE.md          — component model, interfaces, data/control flow
    CONSTRAINTS.md           — perf, latency, security, operability limits
    ADR-INDEX.md             — links to binding ADRs
    /adr/
      ADR-XXXX-*.md

/design/proposals/           — candidate futures (non-binding)
  /P-####-slug/
    PROPOSAL.md
    STATUS.md
    EVIDENCE/

/design/active/              — accepted designs under execution (binding via DESIGN_LINKS)
  /A-####-slug/
    SPEC.md
    STATUS.md
    GOVERNANCE-DELTA.md      — exact deltas for governance/live/*
    LINKS.md

/design/archive/             — immutable history
  /YYYY/
  /rejected/
```

### Authority Model

- `/governance/live/*` is binding for execution
- `/design/current/*` is binding only via `DESIGN_LINKS.md` references
- If conflict: execution follows governance/live, agent raises supersession gate

### Design ↔ Governance Bridge

```
/governance/live/DESIGN_LINKS.md
```

Contains:
- Pointers to canonical design/current docs
- List of active design IDs
- Precedence rule: "governance wins until DESIGN_LINKS is updated"

### Lifecycle State Machine

States: Proposed → InReview → Accepted → Active → Shipped → Superseded → Archived

Transitions requiring human approval:
- **InReview → Accepted** (Gate #1)
- **Active → Shipped** (Gate #2)
- **Any → Superseded** (Gate #3)
- **→ Rejected** (Gate #4)

---

## Part VI: Work Tracking

### Repository Layout

```
/governance/
  /live/                     — minimal control loop (binding)
    TARGET.md
    BOUNDARY.md
    BLOCKERS.md
    METRICS.md
    DESIGN_LINKS.md

  /roadmap/                  — future work (non-binding)
    README.md
    index.md
    /slices/
      /S-####-slug/
        slice.md             — goal, scope, success checks, dependencies
        target.partial.md    — optional delta to TARGET
        boundary.partial.md  — optional delta to BOUNDARY
        blockers.seed.md     — anticipated blockers
        metrics.seed.md      — proposed metrics

  /completed/                — historical record (immutable)
    README.md
    index.md
    /slices/
      /S-####-slug__YYYY-MM-DD/
        summary.md
        diffs.md
        TARGET.final.md
        BOUNDARY.final.md
        BLOCKERS.final.md
        METRICS.final.md
        decisions.md

  HISTORY.md                 — append-only ledger of major events
```

### Three Time Domains

| Domain | Files | Purpose |
|--------|-------|---------|
| **Now** | TARGET / BOUNDARY / BLOCKERS / METRICS | What must be true right now |
| **Later** | ROADMAP | What we might do |
| **Past** | HISTORY + completed | What we already decided/did |

**Agent rule**: May read Past, may plan from Later, but only act on Now.

### Promotion & Retirement

- **Begin work**: Move from ROADMAP → BLOCKERS with evidence
- **Complete work**: Remove from BLOCKERS, update METRICS, append to HISTORY

---

## Part VII: Human Touch Points

These are the only mandatory decision gates. All other work is autonomous.

### Gate #1: Accept a Proposal

Triggered: Proposal ready to become binding.

Agent presents:
- 2-3 options (accept / reject / on-ice / request evidence)
- Governance deltas
- Key risks/unknowns
- Recommended option

### Gate #2: Declare Design Shipped

Triggered: Implementation claims completion.

Agent presents:
- Acceptance criteria checklist with evidence pointers
- Metrics deltas
- Remaining known gaps
- Decision: ship vs keep active

### Gate #3: Supersede Current Design

Triggered: Conflict between design/current and reality or new proposal.

Agent presents:
- What is superseded
- What replaces it
- Migration impact
- Risk and schedule implications

### Gate #4: Reject a Proposal

Triggered: Evidence or feasibility fails.

Agent presents:
- Failure evidence
- Alternative paths

### Gate #5: Change Boundary Law

Triggered: Cross-world coupling becomes necessary.

Agent presents:
- Boundary change options
- Blast radius analysis
- Resurrection risk assessment

---

## Part VIII: Intake — Injecting New Intent

### The Creative Act

Humans are the only source of **new ends**. Agents are the source of **means**.

Without an intake layer, the agent can only rearrange existing context.

### Intake Structure

```
/design/intake/
  /I-####-slug/
    INTAKE.md
    STATUS.md
    NOTES.md
```

#### INTAKE.md (Human-Authored)

- **User-facing outcome**: What must become true for users
- **Technical outcome**: What must become true in the system
- **Constraints**: Perf, safety, compatibility
- **Non-goals**: What we explicitly won't do
- **Acceptance checks**: Observable verification
- **Open questions**: Unknowns to resolve

### From Intake to Shipping

1. **Human creates Intake** — The creative act, injecting new intent
2. **Agent compiles Intake → Design** — Generates candidate architectures, identifies unknowns, maps to governance deltas
3. **Human selects/edits design** — Shaping a draft built from their intake primitives
4. **Agent promotes accepted design → Active** — Updates DESIGN_LINKS, applies governance deltas, seeds blockers/metrics
5. **Execution loop runs** — Eliminate blockers, drive metrics
6. **Ship** — Acceptance checks pass, archive snapshots

---

## Part IX: Escalation Protocol

### When to Escalate

The agent must escalate when:
- Ambiguity in contract blocks blocker resolution
- Repeated attempts (N=2-3) fail to reduce a blocker
- Boundary law would be violated to proceed
- Migration/cutover choice required
- Evidence insufficient to proceed safely

### Escalation Format

Compact, structured:
- What is blocked (link to BLOCKER id)
- What is unknown
- 2-3 options
- Recommended option
- Decision request

---

## Part X: Handling Known Failure Modes

### Non-Essential UI on Legacy

Policy options (express in TARGET DoD or BOUNDARY exceptions):
- **Gate off**: Unreachable by default
- **Tombstone**: "Temporarily unavailable" placeholder
- **Delete**: With removal ledger

If legacy UI remains reachable and broken, it must be a blocker.

### Tests That Incentivize Resurrection

Do 3-way test triage:
1. **Still-valid behavior**: Rewrite test to target new API
2. **Legacy-only behavior**: Convert to deprecation test
3. **Unknown/ambiguous**: Quarantine with marker and deadline

Add no-resurrection guardrail:
- Denylist of legacy modules
- CI fails if new code imports them (except bridge)

### Superseded Plans

- Treat TARGET.md as canonical
- Ignore conflicting older plans unless user updates TARGET
- Old plans get stamped "SUPERSEDED as of YYYY-MM-DD"

---

## Part XI: Why This Converges

### The Three Gradients

1. **Target pressure** (TARGET.md) — pulls toward done
2. **Boundary pressure** (BOUNDARY.md) — prevents backward coupling
3. **Closure pressure** (BLOCKERS + METRICS) — forces finishing

LLMs operate well inside these gradients:
- They can explore
- But cannot escape
- And are forced to finish

### The Quiet Truth

LLMs do not fail at the last 5% because they are bad at code.

They fail because **the last 5% is no longer a pattern problem—it is a responsibility problem**.

This system explicitly assigns responsibility for closure.

---

## Part XII: Implementation Guidance

### Acceptance Criteria

An implementation is correct if:
- Work is always justified by a blocker or DoD item
- Drift is corrected by editing TARGET.md, not improvisation
- Legacy resurrection is prevented by enforcing BOUNDARY.md
- Each phase either eliminates a blocker or produces a bounded decision request
- Metrics move monotonically toward targets or force escalation when stuck
- Token overhead remains low (artifacts are one-screen documents)

### Design Curator Responsibilities

- Keep `/design/current` coherent and minimal
- Ensure every design artifact has explicit lifecycle state
- Maintain `DESIGN_LINKS.md` bridge to governance
- Prevent "zombie docs" influencing execution

### Consistency Auditor Responsibilities

- Check design/current vs governance/live for conflicts
- Check design/current vs repo reality for drift
- Compare active designs vs roadmap/live blockers alignment

### Autonomy Rules

**Allowed without human approval:**
- Fix metadata, indices, broken links
- Move docs to archive when terminal
- Update index.md to reflect states
- Generate consistency/drift reports
- Propose governance deltas

**Requires human approval:**
- Marking proposals Accepted/Rejected/Shipped/Superseded
- Changing boundary law
- Changing TARGET.md meaning
- Deleting historical documents

---

## Part XIII: The Governance Kernel (Reference)

These 15 questions, when answered, create a behavioral attractor that prevents drift, resurrection, and endless refactor loops:

1. What is the explicit **Definition of Done**?
2. What is the **target end state**, and what is explicitly out of scope?
3. What **invariants** must never be violated, and how are they enforced?
4. What is the **cutover and rollback strategy**?
5. What is the **boundary law** between legacy and new systems?
6. What is the **single bridge or adapter**, and how is its growth constrained?
7. What is the **smallest shippable unit of work**, and what order must units be done in?
8. What work is allowed to be **temporarily broken or quarantined**, and how is it made unreachable?
9. How are **tests classified** (migrate / deprecate / unknown), and how is resurrection prevented?
10. What is the **single canonical source of truth** for the current plan and target state?
11. What are the **stop-and-escalate conditions** when ambiguity or risk is encountered?
12. What **progress metrics** must monotonically move toward completion?
13. What **gates must be green** before a phase is considered complete?
14. What is the **review and batching protocol** for agent-produced changes?
15. What **final validations** prove the system is truly done and releasable?

---

## Summary

This system is a **light-touch, convergent control plane** for long-running, high-risk software programs executed by LLMs with humans in the loop.

**Core mechanism**: Four live artifacts + a phase ritual restated every phase.

**Design layer**: Proposals → Active → Shipped with explicit human gates.

**Work tracking**: Roadmap (future) → Blockers (now) → Completed (past).

**Intake**: Humans inject new ends; agents compile means.

**Result**: LLMs cannot escape, cannot defer, cannot resurrect. They are forced to finish.

This is the smallest structure that reliably turns open-ended, uncertain, multi-month software efforts into convergent, shippable outcomes.
