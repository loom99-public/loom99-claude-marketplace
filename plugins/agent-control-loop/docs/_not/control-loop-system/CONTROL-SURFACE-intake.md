a “Spec Intake” control surface (human-authored primitives)
------------------------------------------------------------------------------

You need a place where the human can inject _new truth_ into the system in a form the agent can operationalize, without turning everything into free-form chat.

That means defining a small set of **human-authored primitives** that can generate new work.

### The primitives

A human must be able to create any new feature/design by providing one (or more) of:

1.  **Outcome** (what must become true in the world)
2.  **Constraints** (what must not be violated)
3.  **Acceptance checks** (how we’ll know it’s done)
4.  **Non-goals** (what we explicitly won’t do)
5.  **Priorities** (what matters most if tradeoffs appear)

These are not “options.” They are **new constraints injected into the attractor**.

* * *

Concrete artifact: `INTAKE.md` (or `/design/intake/*`)
------------------------------------------------------

Add:

```
/design/intake
  README.md
  /I-####-slug
    INTAKE.md
    STATUS.md
    NOTES.md
```

### `INTAKE.md` structure (minimal, generative)

*   **User-facing outcome**
*   **Technical outcome**
*   **Constraints** (perf, safety, compatibility, etc.)
*   **Non-goals**
*   **Acceptance checks** (observable)
*   **Open questions** (optional)

This is how a new feature gets added.

The human writes _this_, not the agent.

* * *

The agent’s job changes: from “offer options” to “compile intent”
-----------------------------------------------------------------

Given an intake, the agent must produce (and propose) the downstream artifacts:

*   Proposal(s) in `/design/proposals`
*   Deltas to `/governance/live/TARGET.md` and `BOUNDARY.md`
*   Initial blockers and metrics
*   A slice plan in roadmap

The human can still decide between options, but the source of novelty is the intake.

* * *

How you go from 0 → shipping (workflow)
---------------------------------------

1.  **Human creates an Intake**
    *   This is the creative act.
    *   It injects new intent into the system.
2.  **Agent compiles Intake → Design**
    *   Generates one or more candidate architectures/specs
    *   Identifies unknowns and risks
    *   Maps to governance deltas
3.  **Human selects / edits the resulting design**
    *   Human is not picking arbitrary LLM ideas; they’re shaping a draft built from their intake primitives.
4.  **Agent promotes accepted design → Active**
    *   Updates DESIGN\_LINKS
    *   Applies governance deltas
    *   Seeds blockers/metrics/roadmap
5.  **Execution loop runs (your minimal control loop)**
    *   eliminate blockers
    *   drive metrics
6.  **Ship**
    *   acceptance checks pass
    *   archive snapshots

* * *

Why this is the right missing layer
-----------------------------------

Because it restores the missing asymmetry:

*   Humans are the only source of **new ends**
*   Agents are the source of **means**

Without an intake layer, the agent can only rearrange existing context.  
With it, you can continuously add brand-new features, UX goals, and architectural direction in a controlled, auditable way.

* * *

Minimal additions to your existing system
-----------------------------------------

Add exactly two things:

1.  `/design/intake/*` (human-authored intent injection)
2.  A policy: “Nothing enters roadmap or blockers unless it traces back to an Intake or an explicit TARGET change.”

That’s enough to go from 0 to shipping without turning the system into either:

*   “LLM invents the product”  
    or
*   “human writes everything in chat.”

If you want, I can give you the intake template and the exact compilation outputs the agent must produce (proposals + governance deltas + blockers + metrics) in the same ARD-grade style.
