
## Prompt:
Give me the comprehensive spec for the Design Hub agent (or agents) that keep this system working autonomously (with guidance).  Minimal control loops.  Specify human touch points where the big picture decision making must be injected

## Response:
Design Hub Agent Spec
---------------------

### Objective

Maintain a long-lived, versioned “design hub” that stays consistent with repo reality and governance/live constraints, while enabling proposals, acceptance, execution linkage, and archival—using minimal control loops and explicit human decision injection points.

No code. Behavioral + artifact spec.

* * *

1) Agent Topology
   =================

1.1 Required Agents (logical roles)
-----------------------------------

### A) **Design Curator** (primary)

Owns design namespace integrity and state transitions.

*   Keeps `/design/current` coherent and minimal.
*   Ensures every design artifact has an explicit lifecycle state.
*   Prevents “zombie docs” influencing execution.

### B) **Consistency Auditor** (secondary; can be merged into Curator)

Periodically checks:

*   design/current vs governance/live for conflicts
*   design/current vs repository reality for drift
*   active designs vs roadmap/live blockers alignment

### C) **Decision Gatekeeper** (human-in-the-loop interface; can be a mode of Curator)

Generates bounded decision requests when:

*   conflicts exist
*   acceptance/supersession needed
*   design claims exceed evidence

In implementation, A/B/C can be one agent with modes; spec remains.

* * *

2) Minimal Control Loops
   ========================

2.1 Loop A: **Design State Loop** (event-driven)
------------------------------------------------

Triggers:

*   new proposal added
*   proposal status changed
*   active work begins/ends
*   governance/live artifacts updated
*   PR merged touching architecture boundaries

Cycle:

1.  Detect changed design artifact(s)
2.  Validate required metadata/state
3.  Enforce allowed transition rules
4.  Update indices/links
5.  If ambiguity/conflict: raise a human decision gate

Output: updated status files + updated `/design/index.md` + optional decision request.

* * *

2.2 Loop B: **Design ↔ Governance Consistency Loop** (periodic or on-demand)
----------------------------------------------------------------------------

Triggers:

*   daily/weekly scheduled run OR when major governance/live changes
*   before promotion of roadmap slice into blockers
*   before declaring phase complete

Cycle:

1.  Parse `/design/current` “binding surface”
2.  Parse `/governance/live` constraints
3.  Compare for contradiction
4.  If contradiction:
    *   classify as: stale design, stale governance, or unknown
    *   generate bounded resolution options
5.  Apply edits only after decision gate (unless purely mechanical/obvious)

Output: “consistency report” + decision gates where required.

* * *

2.3 Loop C: **Design Drift Loop** (repo reality check)
------------------------------------------------------

Triggers:

*   when architecture-affecting files change
*   when metrics regress
*   when blockers persist > N phases

Cycle:

1.  Infer architecture facts from repo (module graph, boundaries, key interfaces)
2.  Compare to design/current claims
3.  Identify drift deltas
4.  Either:
    *   update design/current (if it should follow reality), or
    *   create governance blockers (if reality violates intended design), or
    *   gate for human decision

Output: drift deltas + either doc update PR suggestion or blocker additions.

* * *

3) Artifact Requirements (Design Hub)
   =====================================

3.1 Directory contract
----------------------

```
/design
  README.md
  index.md

/design/current
  /north-star
    OVERVIEW.md
    ARCHITECTURE.md
    CONSTRAINTS.md
    ADR-INDEX.md
    /adr
      ADR-XXXX-*.md
  /features
  /ux

/design/proposals
  /P-####-slug
    PROPOSAL.md
    STATUS.md
    EVIDENCE/

/design/active
  /A-####-slug
    SPEC.md
    STATUS.md
    GOVERNANCE-DELTA.md
    LINKS.md
    EVIDENCE/

/design/archive
  /YYYY/
  /rejected/
```

3.2 Mandatory metadata (in each proposal/active folder)
-------------------------------------------------------

`STATUS.md` fields (machine-parseable):

*   `id`: P-#### / A-####
*   `title`
*   `state`: Proposed | InReview | Accepted | Active | Shipped | Superseded | Rejected | OnIce
*   `owner`: human owner
*   `last_reviewed`: date
*   `supersedes`: optional list
*   `superseded_by`: optional pointer
*   `governance_links`: paths into `/governance/live` and/or roadmap slice ids

3.3 Binding surface definition
------------------------------

`/design/current/north-star/ADR-INDEX.md` is the binding surface for decisions.

*   ADRs must be the only place irreversible decisions are encoded.
*   OVERVIEW/ARCHITECTURE describe intent; ADRs define constraints.

3.4 Design ↔ Execution link artifact
------------------------------------

`/governance/live/DESIGN_LINKS.md` must exist and include:

*   canonical pointers to relevant design/current docs
*   list of active design ids
*   precedence rule (governance wins until updated)

Design Curator maintains it.

* * *

4) State Machine and Transitions (Enforced)
   ===========================================

4.1 Allowed transitions
-----------------------

*   Proposed → InReview → Accepted → Active → Shipped
*   Active → Superseded (if replaced mid-flight)
*   InReview → Rejected
*   Any → OnIce (temporary pause)
*   Shipped/Superseded/Rejected → Archive (immutable)

4.2 Transition guards (must be checked)
---------------------------------------

### Proposed → InReview

*   PROPOSAL.md complete (see template below)
*   minimal evidence included or explicit “evidence missing” section

### InReview → Accepted

Human touch required (Decision Gate #1).

*   acceptance rationale recorded
*   `GOVERNANCE-DELTA.md` present
*   explicit mapping to TARGET/BOUNDARY/METRICS impact
*   risk notes: unknowns that become blockers vs acceptable

### Accepted → Active

*   referenced in `/governance/roadmap` slices OR `/governance/live/BLOCKERS.md`
*   LINKS.md includes PR/slice linkage
*   DESIGN\_LINKS.md updated to include active id

### Active → Shipped

Human touch required (Decision Gate #2) unless criteria are purely mechanical.

*   acceptance criteria satisfied (defined in SPEC.md)
*   governance metrics and DoD satisfied

### Any → Superseded

Human touch required (Decision Gate #3).

*   must create `SUPERSEDED-BY.md` pointer (or equivalent in STATUS)
*   must update DESIGN\_LINKS and indexes

### Rejected

Human touch required (Decision Gate #4).

*   must create `REJECTION.md` with reason + evidence

* * *

5) Document Templates (Production-Grade, Minimal)
   =================================================

5.1 `PROPOSAL.md` (required sections)
-------------------------------------

*   **Problem statement**
*   **Goals / Non-goals**
*   **Proposed design** (component/interface level)
*   **Alternatives considered**
*   **Risks / unknowns**
*   **Migration/cutover impact** (even if “none”)
*   **Validation plan** (what evidence would convince us)
*   **Governance impact summary**
    *   TARGET deltas
    *   boundary implications
    *   new metrics needed
    *   anticipated blockers

5.2 `SPEC.md` (active)
----------------------

*   **Accepted design** (what is now intended)
*   **Interfaces/contracts**
*   **Operational constraints** (perf, safety, observability)
*   **Acceptance criteria** (measurable)
*   **Out-of-scope**
*   **Rollback/cutover considerations** (if applicable)

5.3 `GOVERNANCE-DELTA.md`
-------------------------

Exact edits required to:

*   `/governance/live/TARGET.md`
*   `/governance/live/BOUNDARY.md`
*   `/governance/live/METRICS.md`
*   optional seeds for blockers

This must be expressed as “add/remove/replace” in plain text chunks (not diffs, but diff-like intent).

* * *

6) Human Touch Points (Big Picture Injection)
   =============================================

These are the only mandatory decision points.

Gate #1: Accept a proposal
--------------------------

Triggered when a proposal is ready to be binding.  
Agent must present:

*   2–3 options (accept / reject / on-ice / request evidence)
*   governance deltas
*   key risks/unknowns
*   recommended option
*   decision request

Gate #2: Declare a design “shipped”
-----------------------------------

Triggered when implementation claims completion.  
Agent must present:

*   acceptance criteria checklist with evidence pointers
*   metrics deltas
*   remaining known gaps
*   decision request: ship vs keep active (with why)

Gate #3: Supersede current architecture/design
----------------------------------------------

Triggered on conflict between design/current and reality or new proposal.  
Agent must present:

*   what is being superseded
*   what replaces it
*   migration impact
*   risk and schedule implications
*   decision request

Gate #4: Reject a proposal
--------------------------

Triggered when evidence or feasibility fails.  
Agent must present:

*   failure evidence
*   alternative paths
*   decision request

Gate #5: Introduce or change boundary law
-----------------------------------------

Triggered when cross-world coupling becomes necessary.  
Agent must present:

*   boundary change options
*   blast radius analysis
*   explicit “resurrection risk” assessment
*   decision request

* * *

7) Autonomy Rules (What the agent may do without asking)
   ========================================================

Allowed autonomous edits:

*   fix metadata, indices, broken links
*   move docs to archive when state is terminal and referenced pointers exist
*   update `index.md` to reflect states
*   request evidence / add TODO placeholders in proposals (non-binding)
*   generate consistency/drift reports
*   propose governance deltas (never apply to governance/live without approval unless purely clerical)

Not allowed autonomously:

*   marking proposals Accepted/Rejected/Shipped/Superseded
*   changing boundary law
*   changing TARGET.md meaning (can propose edits)
*   deleting historical documents

* * *

8) Integration with Minimal Governance Loop
   ===========================================

8.1 Authority model
-------------------

*   `/governance/live/*` is binding for execution.
*   `/design/current/*` is binding only via `DESIGN_LINKS.md` references.
*   If conflict:
    *   execution follows governance/live
    *   agent raises Gate #3 (supersede or reconcile)

8.2 Promotion mechanism
-----------------------

When a design becomes Active:

*   Curator ensures:
    *   roadmap slice exists (or blockers exist)
    *   `GOVERNANCE-DELTA.md` is applied via human approval
    *   DESIGN\_LINKS updated
    *   indexes updated

When work completes:

*   Curator snapshots:
    *   SPEC.md + evidence into `/design/archive/YYYY/...`
    *   optionally copy to `/governance/completed/...` folder
    *   updates status and pointers

* * *

9) Acceptance Criteria for the Design Hub Agent
   ===============================================

System is functioning if:

*   Every design artifact has an explicit state and valid pointers.
*   Only “current” + “active” influence execution; proposals/archive do not.
*   Conflicts between design/current and governance/live are detected and gated.
*   Superseded/rejected docs are preserved and forward-linked, not silently ignored.
*   The number of “zombie” docs with unclear truth value trends toward zero.

* * *

