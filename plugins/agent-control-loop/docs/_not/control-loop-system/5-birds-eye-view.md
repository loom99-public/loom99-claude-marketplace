## Prompt:
NEXT: Give a birds eye view (one page) summary of the system we've built so far

## Response:
Bird’s-Eye View — Minimal-Control-Loop Engineering System
---------------------------------------------------------

This system is a **light-touch, convergent control plane** for long-running, high-risk software programs executed by LLMs (with humans in the loop). It prevents drift, resurrection, and infinite refactor loops while staying small enough to run continuously.

* * *

### 1) Two planes of truth

**Execution Plane (what must be true right now)**

```
/governance/live
  TARGET.md    – what “done” means
  BOUNDARY.md  – what may call what
  BLOCKERS.md  – the only work queue
  METRICS.md   – monotonic convergence signals
```

These four files are binding.  
They are small, frequently restated, and continuously updated.

**Design Plane (what we intend to build)**

```
/design/current     – canonical architecture & UX truth
/design/active      – accepted designs being executed
/design/proposals   – candidate futures
/design/archive     – immutable history
```

Only `/design/current` and `/design/active` are allowed to influence execution, and only via an explicit bridge:

```
/governance/live/DESIGN_LINKS.md
```

* * *

### 2) Minimal control loop (the engine)

Every execution phase follows one ritual:

1.  Restate `TARGET`, `BOUNDARY`, `BLOCKERS`, `METRICS`
2.  Choose **one** highest-risk blocker
3.  Work only to eliminate that blocker
4.  Update artifacts and metrics
5.  Repeat

This enforces:

*   no deferral (only blockers exist)
*   no resurrection (boundary law)
*   no drift (target is always in view)
*   no fake completion (metrics + DoD)

* * *

### 3) What keeps the big picture sane

A **Design Hub** (agent) maintains architecture and UX intent across time.

It runs three light loops:

*   **Design State Loop** – proposals → active → shipped → archived
*   **Design ↔ Governance Consistency Loop** – detect conflicts
*   **Design Drift Loop** – compare repo reality to design truth

All irreversible decisions flow through **explicit human gates**:

*   accept a proposal
*   ship or supersede a design
*   change boundary law
*   reject a design

Everything else is autonomous.

* * *

### 4) How work moves through the system

**Future ideas**  
→ `/design/proposals`

**Accepted architecture**  
→ `/design/active`  
→ deltas applied to `/governance/live`

**Executed work**  
→ `/governance/live/BLOCKERS.md` → cleared  
→ snapshots go to `/design/archive` and `/governance/completed`

**Memory**  
→ `/design/archive` + `/governance/completed` + `HISTORY.md`  
(read-only, never binding)

* * *

### 5) Why this converges

The system creates three gradients:

*   **Target pressure** (TARGET.md)
*   **Boundary pressure** (BOUNDARY.md)
*   **Closure pressure** (BLOCKERS + METRICS)

LLMs operate well inside these gradients:

*   they can explore
*   but cannot escape
*   and are forced to finish

This is the smallest structure that reliably turns open-ended, uncertain, multi-month software efforts into convergent, ship-able outcomes.

## Prompt:
we have the control loop.  We have the design hub.  