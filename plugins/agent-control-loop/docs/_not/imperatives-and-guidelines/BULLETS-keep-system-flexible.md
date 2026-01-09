## Response:
10 “MUST” rules (non-negotiable)
--------------------------------

1.  **Preserve locality of change:** no change may require coordinated edits across unrelated layers without introducing/using a stable seam (interface/adapter).
2.  **Enforce directional dependencies:** architecture must have a declared dependency direction; cycles and “upward” calls are forbidden unless explicitly waived.
3.  **Single enforcement point for global invariants:** any cross-cutting invariant (auth, determinism, serialization, timing, etc.) must be enforced in one module/boundary—not duplicated across callsites.
4.  **No shared mutable global state:** global registries/singletons/context globals are forbidden except behind a single owning module with explicit API and documented invariants.
5.  **No mode explosion:** new modes/flags/options must not multiply behavior regimes without a documented cap and an exit plan; default path must remain canonical.
6.  **One canonical source of truth for state:** each domain concept has one authoritative representation; any secondary representations must be derived and explicitly synchronized.
7.  **Tests may not encode implementation coupling:** tests must assert contracts; if a test forces legacy structure or internal details, it must be migrated, rewritten, or quarantined—not satisfied by reintroducing internals.
8.  **Boundaries are mechanically enforced:** forbidden imports/calls must be checked (CI/lint/test gates) with a narrow waiver mechanism and expiry.
9.  **Every non-trivial change must include a verification story:** what proves correctness (tests/props/checks) and what proves no hidden coupling was added.
10.  **Any waiver must be explicit and time-bounded:** exceptions to any MUST rule require an owner, rationale, and removal condition; waivers may not accumulate silently.

* * *

50 “SHOULD” rules (strong defaults)
-----------------------------------

1.  Prefer **deleting** features/paths over carrying compatibility shims indefinitely.
2.  Keep a **single canonical path** per use-case; treat alternate paths as adapters at edges.
3.  Treat “flexibility” as a cost: require a **value justification** for every new configuration knob.
4.  Keep module responsibilities **small and crisp**; refactor when a module becomes “where things go.”
5.  Prefer **composition over inheritance** for behavior variation.
6.  Prefer **data-oriented contracts** (stable data shapes) over implicit object graphs.
7.  Make state transitions explicit: use **state machines** for multi-phase workflows.
8.  Restrict side effects to well-defined layers; keep domain logic **pure where possible**.
9.  Prefer **immutable snapshots** for coordination over shared mutable references.
10.  Make concurrency boundaries explicit; avoid “ambient async” behavior.
11.  Keep dependency edges few: optimize for **low fan-out** from core modules.
12.  Limit fan-in to “god APIs”; split interfaces when callers have different needs.
13.  Introduce **anti-corruption layers** at legacy/new boundaries.
14.  Use **ports/adapters** where integration details threaten to leak inward.
15.  Centralize cross-cutting policies (auth, logging, validation) in **policy modules**.
16.  Prefer **capabilities** over passing omniscient “context” objects.
17.  Avoid “event bus as architecture”; events should not replace clear call graphs.
18.  Keep event schemas versioned and minimal; avoid turning events into hidden RPC.
19.  Avoid generalized DSLs unless they have a strict, small contract and tooling.
20.  When a DSL exists, constrain expressivity to preserve predictability and testability.
21.  Maintain a small set of **architecture fitness checks** (cycles, forbidden deps, layering).
22.  Track and reduce **mode count** (flags × permutations) as a first-class risk.
23.  Require every new flag to include: owner, default, rollout plan, and deletion date.
24.  Prefer feature toggles that gate _entrypoints_ over toggles that branch deep logic.
25.  Ensure each “feature” has a clearly defined **footprint** (entrypoints, data, runtime).
26.  Avoid “optional” behavior inside core invariants; push variability to the edges.
27.  Maintain stable **domain contracts** even when implementations change.
28.  Separate **contract tests** from **implementation tests**; keep the latter local and cheap.
29.  Prefer many small, fast unit tests over slow integration suites; integration tests should be **few and surgical**.
30.  When integration tests are needed, ensure they validate contracts, not internal wiring.
31.  Keep build/test feedback loop short; treat long feedback loops as architectural debt.
32.  Make failures diagnosable: errors should include context sufficient to localize responsibility.
33.  Avoid “silent fallback” behavior; prefer explicit errors to hidden compatibility paths.
34.  Maintain strict boundaries for serialization/compatibility; don’t let versioning leak everywhere.
35.  Prefer explicit schema migrations and explicit rollback paths for data changes.
36.  Avoid dual-write unless strictly necessary; if used, bound it with explicit cutover criteria.
37.  Maintain “one source of truth” for timing semantics (especially for animation/rendering).
38.  Keep compiler/renderer pipelines staged with explicit inputs/outputs per stage.
39.  Avoid stage back-edges; do not let later stages mutate earlier-stage representations.
40.  Treat caches as derived state; cache invalidation rules must be owned and centralized.
41.  Reduce “hidden coupling” by documenting invariants at the module boundary, not in comments deep inside.
42.  Prefer small, explicit interfaces over passing wide structs with unrelated fields.
43.  When adding a new abstraction, require a “what it forbids” section (guardrails against abuse).
44.  When a module grows, split by _reason to change_, not by file size.
45.  Use consistent naming to reveal boundaries (package/module prefixes that encode layer).
46.  Keep a living list of **hotspots** where changes routinely cascade; prioritize reducing their centrality.
47.  Regularly retire dead code, unused flags, and dormant paths; don’t let them become latent coupling.
48.  When requirements change, update the target state explicitly; don’t let “ghost requirements” linger.
49.  Prefer “make it impossible” over “tell people not to”: enforce constraints mechanically where feasible.
50.  Optimize architecture for **predictable change**, not maximal generality: default toward fewer degrees of freedom unless proven necessary.

## Prompt:
Now give me the comprehensive specification for the agent that hunts down the nucleation sites, untangles the knots (or cuts through them without mercy), and, even if it leaves things as a broken mess for someone to clean up, sets the right boundaries for the healing to begin

Propose this spec without directly referencing any terms or previous concepts without explaining them.  this spec should stand on its own without any chat history to contextualize it

