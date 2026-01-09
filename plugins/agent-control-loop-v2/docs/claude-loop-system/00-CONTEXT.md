# Context: The Problem This System Solves

## The 80% Stall Phenomenon

LLMs excel at **expansive, low-risk work**:
- Moving files, renaming symbols, updating imports
- Mechanical edits with high pattern similarity
- Obvious transformations with low ambiguity

LLMs stall at **convergent, high-risk work**:
- Edge cases and cross-cutting invariants
- Data model inconsistencies and migration logic
- Backward compatibility and tests that no longer compile

When faced with uncertainty, internal objectives conflict:
- "Make progress" vs. "Don't introduce errors"
- "Don't hallucinate" vs. "Don't break tests"

The agent cannot trade these off, so it **escapes via deferral**:
> "We should handle this later." / "This is out of scope." / "Add a TODO."

This is not laziness. This is **uncertainty collapse**.

---

## The Three Failure Modes

### 1. Deferral
Creating "future sprint" items instead of resolving blockers. The agent pushes hard work into the future indefinitely.

**Example:**
> "We'll handle this edge case in Phase 2"
> "Adding TODO for later cleanup"
> "This is out of scope for now"

### 2. Resurrection
Reintroducing legacy code to make tests pass. When tests fail after removing old code, the agent brings back the old code rather than migrating the tests.

**Example:**
> "Test needs legacy store, so I imported it directly"
> "Added compatibility mode that detects legacy usage"

### 3. Plan Drift
Following outdated plans that refer to a past target state. Old plans in context compete with new reality, causing inconsistent behavior.

**Example:**
> Following a plan from 50 messages ago that's been superseded
> Satisfying constraints from an old design doc that no longer applies

---

## The Core Insight

### What Agents Actually Need

Agents do not need comprehensive governance documents with long rule lists.

Long lists of instructions create **internal conflict**. Conflict manifests as drift, deferral, vagueness, and resurrection.

Agents need **three pressure gradients** that make bad behavior expensive and good behavior cheap:

1. **Target Pressure** — A visible target that defines "done"
2. **Boundary Pressure** — A visible boundary that defines what is forbidden
3. **Closure Pressure** — A visible notion of "not done" that forces finishing

Within these gradients, LLMs can explore and solve. But they cannot escape and defer.

### Local Gradients, Not Rules

Transformers don't "remember" rules. They re-weight what looks relevant to the current moment. Rules survive only if:
- Kept near the present (restated/used immediately before work)
- Expressed in compressed, conflict-free form

LLMs operate on local gradients:
- "Am I closer to target?"
- "Am I violating a boundary?"
- "Is there still a blocker?"
- "Did the number go down?"

The system creates these gradients mechanically. The agent cannot escape them.

---

## The Minimal Control Loop

The solution is a **phase-based ritual** with four live artifacts.

### Four Live Artifacts

Each must fit on one screen. Updated continuously. Located in `governance/live/`.

| Artifact | Purpose |
|----------|---------|
| `TARGET.md` | Target end state + Definition of Done |
| `BOUNDARY.md` | Single boundary rule + allowed bridge |
| `BLOCKERS.md` | Exhaustive list of ship-stoppers (the only work queue) |
| `METRICS.md` | 2-4 monotonic measures of convergence |

### The Phase Ritual

At the start of every work phase:

1. **Restate artifacts** — Ground in current reality
2. **Select single blocker** — Force focus on highest-value work
3. **Plan phase** — 3-7 steps with verifications
4. **Execute** — Work until blocker eliminated or escalated
5. **Record outcome** — Update artifacts, log phase

### Prohibited Behaviors

- Creating "future sprint" items instead of resolving blockers
- Expanding scope not tied to a blocker
- Reintroducing legacy code paths to satisfy tests
- Declaring completion without meeting DoD and clearing BLOCKERS

---

## Convergence Mode

When work reaches ~80% completion, activate convergence mode:

> "We are entering convergence mode. The only goal is to eliminate blockers and make the system build and pass tests. No new features. No deferrals. Every remaining issue must be either fixed or explicitly resolved."

Convergence mode changes:
- **Zero tolerance for deferral** — Every issue is either a blocker or not needed
- **No new features** — Only blocker elimination work
- **Aggressive escalation** — Escalate after N=1 attempt (not N=2)
- **Enumerate all blockers** — Force explicit listing of everything preventing shipment

---

## Why This Works

### The Quiet Truth

LLMs do not fail at the last 5% because they are bad at code.

They fail because **the last 5% is no longer a pattern problem—it is a responsibility problem**.

Unless you explicitly tell the agent "you are responsible for closure," it will always try to push the stairs into the future.

### Pressure Gradients Create Convergence

The system creates three gradients:

1. **Target pressure** (TARGET.md) — pulls toward done
2. **Boundary pressure** (BOUNDARY.md) — prevents backward coupling
3. **Closure pressure** (BLOCKERS + METRICS) — forces finishing

LLMs operate well inside these gradients:
- They can explore
- But cannot escape
- And are forced to finish

This is the smallest structure that reliably turns open-ended, uncertain, multi-month software efforts into convergent, shippable outcomes.

---

## Attention and Rule Survival

### How Rules Fade in Long Contexts

In long conversations, early instructions lose influence because:
1. **Geometric crowding** — Later tokens create vectors closer to the current query
2. **Semantic drift** — The "what is this moment about?" signal no longer activates early rules

Your instruction "Always format in JSON" fades not because it's forgotten, but because the current moment no longer "looks like" it needs formatting rules.

### How to Keep Rules Alive

Three techniques:

1. **Restatement near the present** — Every time you restate a rule, you create new tokens close to the current semantic state
2. **Embedding rules into the task** — Active constraints work better than passive memories
3. **Structural reinforcement** — Patterns in output keep echoing forward

### Compressed Artifacts

Instead of long rule lists, we maintain:

- **A₀ (Always-On Contract)** — 5-10 hard rules that define identity, restated constantly
- **B₀ (Playbooks)** — Task-type-specific checklists, loaded only when relevant

These are pre-generated and committed (not compressed on-the-fly). Hooks inject them into context at the right moments.

---

## The Two Planes of Truth

### Execution Plane (what must be true right now)

```
/governance/live/
  TARGET.md     — what "done" means
  BOUNDARY.md   — what may call what
  BLOCKERS.md   — the only work queue
  METRICS.md    — monotonic convergence signals
```

These four files are binding. They are small, frequently restated, and continuously updated.

### Design Plane (what we intend to build)

```
/design/
  current/      — canonical architecture & UX truth (binding via DESIGN_LINKS)
  proposals/    — candidate futures (non-binding)
  active/       — accepted designs under execution (binding via DESIGN_LINKS)
  archive/      — immutable history (non-binding)
```

Only `/design/current` and `/design/active` influence execution, via explicit bridge: `/governance/live/DESIGN_LINKS.md`

### Authority Model

- `/governance/live/*` is binding for execution
- `/design/current/*` is binding only via `DESIGN_LINKS.md` references
- If conflict: execution follows governance/live, agent escalates to resolve

---

## Three Time Domains

| Domain | Files | Purpose |
|--------|-------|---------|
| **Now** | governance/live/* | What must be true right now |
| **Later** | governance/roadmap/* | What we might do |
| **Past** | governance/completed/*, HISTORY.md | What we already decided/did |

**Agent rule:** May read Past, may plan from Later, but only act on Now.

---

## Intake: Human Intent Injection

Humans are the only source of **new ends**. Agents are the source of **means**.

Without an intake layer, the agent can only rearrange existing context.

### Intake Primitives

A human injects new work by providing:
1. **Outcome** — What must become true
2. **Constraints** — What must not be violated
3. **Acceptance checks** — How we'll know it's done
4. **Non-goals** — What we explicitly won't do
5. **Priorities** — What matters most if tradeoffs appear

### From Intake to Shipping

1. **Human creates Intake** — The creative act, injecting new intent
2. **Agent compiles Intake → Design** — Generates candidate architectures, identifies unknowns
3. **Human selects/edits design** — Shaping draft built from intake primitives
4. **Agent promotes accepted design → Active** — Updates DESIGN_LINKS, applies governance deltas
5. **Execution loop runs** — Eliminate blockers, drive metrics
6. **Ship** — Acceptance checks pass, archive snapshots

---

## Human Touch Points (Decision Gates)

These are the only mandatory human decision points. Everything else is autonomous.

| Gate | Trigger | Agent Presents |
|------|---------|----------------|
| **Accept Proposal** | Proposal ready to become binding | Options, governance deltas, risks, recommendation |
| **Ship Design** | Implementation claims completion | Acceptance criteria checklist, metrics, gaps |
| **Supersede Design** | Conflict between design and reality | What's superseded, replacement, migration impact |
| **Reject Proposal** | Evidence or feasibility fails | Failure evidence, alternative paths |
| **Change Boundary** | Cross-world coupling becomes necessary | Boundary options, blast radius, resurrection risk |

All gates use `AskUserQuestion` for structured decision collection.

---

## Success Criteria

The system is working correctly when:

1. **Work is always justified** by a blocker or DoD item
2. **Drift is corrected** by editing TARGET.md, not improvisation
3. **Resurrection is prevented** by enforcing BOUNDARY.md
4. **Each phase eliminates a blocker** or produces a bounded decision request
5. **Metrics move monotonically** toward targets or force escalation when stuck
6. **Token overhead remains low** (artifacts are one-screen documents)
7. **Human gates are explicit** using AskUserQuestion, not prose

---

## Summary

This system is a **light-touch, convergent control plane** for long-running, high-risk software programs executed by LLMs with humans in the loop.

- **Core mechanism:** Four live artifacts + a phase ritual + hooks for injection
- **Design layer:** Proposals → Active → Shipped with explicit human gates
- **Work tracking:** Roadmap (future) → Blockers (now) → Completed (past)
- **Intake:** Humans inject new ends; agents compile means
- **Result:** LLMs cannot escape, cannot defer, cannot resurrect. They are forced to finish.
