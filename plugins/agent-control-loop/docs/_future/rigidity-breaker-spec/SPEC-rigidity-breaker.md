## Response:
Specification: “Rigidity Breaker” Agent (Nucleation-Site Hunter + Boundary Setter)
----------------------------------------------------------------------------------

### 1) Mission

Given a software repository, identify the smallest set of structural causes that make changes cascade, couple, and harden (“rigidification”), then perform aggressive interventions to restore **locality of change** by:

*   isolating or removing the structural causes,
*   breaking coupling patterns that force global coordination,
*   and installing enforceable boundaries so subsequent cleanup/refactoring can proceed without re-knotting.

This agent is allowed to:

*   delete code paths, features, and legacy shims,
*   introduce hard boundaries and temporary stubs,
*   leave the repository in a temporarily failing state,  
    provided it produces a precise stabilization plan and containment rules that make recovery straightforward.

No runtime assumptions. No code required by this spec.

* * *

2) Definitions (Operational)
----------------------------

### 2.1 Rigidification

A project is “rigidified” when small intended changes require edits across many modules/layers and trigger widespread test/build fallout unrelated to the change’s domain intent.

### 2.2 Nucleation site

A “nucleation site” is a structural element that causes rigidification to propagate outward. Typical examples include:

*   duplicated cross-cutting rules enforced in many places,
*   mode/configuration explosion that multiplies behavior regimes,
*   cyclic dependencies or bidirectional coupling,
*   shared mutable global state used as a coordination substrate,
*   god modules (high fan-in/high fan-out) that become a universal attachment point.

### 2.3 Knot

A “knot” is a region where responsibilities, state, and invariants are interwoven such that disentangling one concern forces coordination with several others.

### 2.4 Boundary

A “boundary” is an enforced rule that restricts what may depend on what, and where cross-cutting policies may be implemented. A boundary is only real if it is mechanically enforceable (e.g., CI checks, lint rules, dependency validation).

* * *

3) Inputs and Capabilities
--------------------------

### 3.1 Inputs

*   Repository access (read/write).
*   Ability to run: build, tests, linters, static analysis, and repo queries (grep/ripgrep).
*   Optional: commit history, PR history, CI logs.

### 3.2 Required configuration (minimal)

*   “Don’t break” list: critical release-blocking behaviors, interfaces, or subsystems.
*   Allowed damage envelope:
    *   Can tests fail? (yes/no)
    *   Can build fail? (yes/no)
    *   Can non-critical features be removed? (yes/no)
*   Max intervention batch size (to avoid unreviewable diffs).
*   Decision authority identity (human approver).

* * *

4) Outputs (Artifacts)
----------------------

All outputs must be generated in a dedicated folder, e.g. `/rigidity_breaker/`.

### 4.1 `SYSTEM_MAP.md` (required)

A compact map of:

*   modules/layers/services and dependency directions,
*   major data/state flows,
*   known global invariants and where enforced.

### 4.2 `NUCLEATION_SITES.md` (required)

Ranked list of candidate nucleation sites, each with:

*   location(s),
*   why it’s a nucleation site (structural evidence),
*   symptoms it causes (what changes it makes expensive),
*   estimated blast radius (low/med/high),
*   recommended intervention type(s).

### 4.3 `INTERVENTION_PLAN.md` (required)

A short plan of “moves,” each move with:

*   objective (what rigidity pattern it breaks),
*   exact scope (files/modules),
*   expected before/after dependency changes,
*   verification criteria (even if partial),
*   rollback strategy (commit-level or patch-level).

### 4.4 `BOUNDARIES.md` (required)

Defines enforceable constraints to prevent re-knotting, including:

*   dependency direction rules,
*   forbidden edges and exception mechanism,
*   designated integration/adapter points,
*   centralized enforcement points for cross-cutting policies.

### 4.5 `STABILIZATION_QUEUE.md` (required if leaving repo failing)

A prioritized list of steps to return repo to a green state, each with:

*   what is broken,
*   why it was broken (ties back to an intervention),
*   minimal fix strategy,
*   acceptance criteria.

### 4.6 `WAIVERS.md` (optional but recommended)

Explicitly permitted violations with:

*   owner,
*   rationale,
*   expiry condition.

* * *

5) Operating Model (Core Loop)
------------------------------

### Phase A: Baseline and symptom acquisition

1.  Run baseline build/tests (or minimal checks if full suite is too slow).
2.  Record:
    *   failing tests,
*   build failures,
*   CI pain points if available.
    3.  Identify “change friction indicators”:
    *   high fan-in/out modules,
*   cyclic dependencies,
*   long feedback loops,
*   large integration-only test surfaces,
*   repeated touching of the same files across unrelated changes.

**Output updates:** `SYSTEM_MAP.md` initial draft.

* * *

### Phase B: Nucleation site discovery (multi-signal ranking)

The agent must compute a ranked set using multiple independent signals, avoiding single-metric decisions.

Required signals (use as many as available):

1.  **Dependency centrality**
    *   modules imported by many others,
*   modules that import widely,
*   edges that cross architectural layers.
    2.  **Cycle and bidirectional coupling detection**
    *   import cycles,
*   mutual references between layers,
*   back-edges in pipelines.
    3.  **Invariant scattering**
    *   repeated validation/policy logic copied across call sites,
*   same rule implemented differently in multiple places.
    4.  **Mode/branch proliferation**
    *   configuration toggles causing deep branching,
*   feature-flag conditioned behavior inside core modules,
*   combinatorial regime count.
    5.  **Shared mutable state hubs**
    *   globals/singletons/registries,
*   implicit ambient context,
*   caches with unclear ownership.
    6.  **Change-correlation hotspots (if history available)**
    *   files that change together frequently,
*   modules that trigger broad test failures.
    7.  **Test brittleness coupling**
    *   tests that fail widely on local edits,
*   tests asserting internal wiring vs externally meaningful contracts.

**Output updates:** `NUCLEATION_SITES.md` ranked list with evidence.

* * *

### Phase C: Intervention selection (aggressive but contained)

The agent must select 1–3 top sites at a time and choose intervention types designed to **restore locality**, not “beautify code.”

Allowed intervention types:

1.  **Encapsulation move**
    *   create a single enforcement point for a rule,
*   route all callers through it,
*   delete duplicated logic.
    2.  **Boundary insertion move**
    *   isolate legacy/unsafe areas behind an adapter,
*   enforce that new code cannot depend on old code except through the adapter.
    3.  **Cycle breaking move**
    *   introduce an interface seam,
*   invert dependency direction,
*   split modules by responsibility,
*   remove back-edges.
    4.  **Mode collapse move**
    *   remove or hard-disable low-value regimes,
*   move variability to edges,
*   define one canonical path.
    5.  **Shared-state elimination move**
    *   restrict mutation to one owner,
*   replace implicit global with explicit dependency injection,
*   add immutable snapshots as handoff points.
    6.  **Excision move (cut without mercy)**
    *   delete a feature/path that forces pervasive coupling,
*   replace with a stub/tombstone,
*   document user impact and recovery options.

**Output updates:** `INTERVENTION_PLAN.md` and a human decision request if excision affects user-facing behavior.

* * *

### Phase D: Execute moves (bounded batches)

Execution constraints:

*   Each batch must be reviewable (bounded diff size).
*   Each batch must update `BOUNDARIES.md` if it changes structure.
*   Each batch must produce a measurable structural effect (e.g., fewer forbidden edges, cycle removed, branching reduced).

If execution breaks build/tests:

*   breakage must be intentional and documented in `STABILIZATION_QUEUE.md` with minimal recovery steps.

* * *

### Phase E: Install enforceable boundaries (“healing begins”)

Boundaries are installed immediately after breaking moves to prevent relapse.

Minimum requirements:

*   one declared dependency direction (layering) with explicit exceptions,
*   a single sanctioned adapter for cross-zone calls if needed,
*   forbidden imports list with narrow waivers,
*   a policy that cross-cutting invariants live in exactly one module (or one per layer) and nowhere else.

The agent must ensure boundaries are mechanically checkable:

*   through existing tooling where possible,
*   otherwise by introducing minimal checks in CI scripts or lint configuration (describe, don’t implement, if runtime constraints forbid).

**Output updates:** `BOUNDARIES.md` finalized for the current round.

* * *

6) Human Touch Points (Mandatory)
---------------------------------

The agent must stop and request approval for:

1.  **Behavior removal or user-facing degradation**
    *   any deletion/tombstone of features,
*   any breaking change to public interfaces.
    2.  **Boundary hardening that could block future work**
    *   introducing strict forbidden edges that may require organizational buy-in.
    3.  **Intentional “broken state” acceptance**
    *   if build/test will be left red after a batch, human must explicitly accept the stabilization queue and the rationale.

Approval requests must be:

*   bounded (2–4 options),
*   consequences explicit,
*   and tied to a specific nucleation site and intervention.

* * *

7) Success Criteria (What “worked” means)
-----------------------------------------

A round is successful if it produces at least one of:

*   reduced dependency centrality of previously dominant modules,
*   eliminated a dependency cycle or back-edge,
*   reduced mode/branch proliferation in core modules,
*   centralized a scattered invariant into one enforcement point,
*   reduced shared mutable state surface area,
*   reduced change fan-out for representative edits (qualitative evidence acceptable).

Additionally, boundaries must exist that prevent reintroduction of the removed rigidity pattern.

* * *

8) Failure Modes and Safety Constraints
---------------------------------------

### 8.1 Failure modes

*   Cosmetic refactoring without locality restoration.
*   Introducing new “universal abstractions” that become new nucleation sites.
*   Excessive batch size causing unreviewable diffs.
*   Boundary rules without enforcement (paper boundaries).
*   Leaving repo broken without a minimal, actionable stabilization queue.

### 8.2 Safety constraints

*   Never delete or mutate artifacts without recording impact and recovery path.
*   Never “fix tests” by reintroducing removed coupling unless explicitly approved.
*   Never broaden a waiver set silently; waivers must be explicit and time-bounded.

* * *

9) Default Cadence
------------------

*   Run discovery continuously but apply interventions in bounded rounds.
*   After each round, force a stabilization checkpoint:
    *   either return to green,
    *   or obtain explicit acceptance of a temporary broken state plus a short stabilization queue.

* * *

This spec defines an agent that:

1.  finds the structural seeds of rigidity,
2.  breaks them using aggressive, contained interventions,
3.  immediately installs enforceable boundaries,
4.  and provides a precise stabilization queue when collateral damage is acceptable.

