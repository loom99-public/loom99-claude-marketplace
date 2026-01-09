# Evaluation: agent-control-loop Phase 2
**Generated:** 2026-01-04
**Status:** CONTINUE - Ready for planning

## Summary

Phase 1 (MVP) is **complete and shipping-ready**. Phase 2 focuses on the design plane and additional agent roles as specified in CONTEXT-PRIME.md Parts IV-VII.

---

## What Phase 1 Built (Foundation)

- **Governor agent** with 5 behavioral rules
- **Phase ritual skill** (5-step procedure)
- **Artifact templates skill** (4 live artifacts)
- **Three commands**: /loop:init, /loop:phase, /loop:status
- **Plugin infrastructure** valid and registered

---

## Phase 2 Scope (from CONTEXT-PRIME)

### Part IV: Agent Roles

**Design Curator** (Recommended):
- Maintains `/design/current` coherence
- Ensures every design has explicit lifecycle state
- Prevents zombie docs
- Manages state transitions with human approval gates

**Consistency Auditor** (Recommended):
- Compares design/current vs governance/live for conflicts
- Checks design/current vs repo reality for drift
- Generates drift reports + resolution options

### Part V: The Design Plane

```
/design/
  README.md                    # Taxonomy + state machine
  current/                     # BINDING authoritative big picture
  proposals/                   # NON-BINDING candidates
  active/                      # BINDING via DESIGN_LINKS
  archive/                     # IMMUTABLE history
```

**Bridge**: `/governance/live/DESIGN_LINKS.md` links design → governance

### Part VII: Human Touch Points (5 Decision Gates)

1. **Accept Proposal** - Proposal → Accepted (move to active/)
2. **Declare Shipped** - Active → Shipped (evidence checklist)
3. **Supersede Design** - Current → Archive (migration impact)
4. **Reject Proposal** - Proposed → Rejected (failure evidence)
5. **Change Boundary** - Update BOUNDARY.md (blast radius)

---

## What's Needed for Phase 2

### Agents (2)
1. `agents/design-curator.md` - Design plane state machine
2. `agents/consistency-auditor.md` - Drift detection

### Commands (3)
1. `commands/design.md` (/loop:design) - Design curation interface
2. `commands/audit.md` (/loop:audit) - Run consistency checks
3. `commands/escalate.md` (/loop:escalate) - Decision gate interface

### Skills (4)
1. `skills/design-state-validator/SKILL.md` - State machine validation
2. `skills/consistency-checker/SKILL.md` - Design vs governance
3. `skills/drift-detector/SKILL.md` - Repo reality inference
4. `skills/design-index-updater/SKILL.md` - Index maintenance

---

## Dependencies & Implementation Order

```
P1: Design Curator Agent
    ↓ depends on: State machine definition
    ↓ uses: design-state-validator, design-index-updater

P2: Consistency Auditor Agent
    ↓ depends on: Design Curator (understands state machine)
    ↓ uses: consistency-checker, drift-detector

P3: Commands
    ↓ depends on: Both agents above
    /loop:design → Design Curator
    /loop:audit → Consistency Auditor
    /loop:escalate → Decision gates (both agents)
```

---

## Ambiguities

1. **Metrics staleness threshold**: N=2-3 phases (same as blockers)
2. **One screen definition**: ~40 lines warning threshold
3. **Proposal alternatives**: Human-authored only (Curator curates, not generates)

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Design plane overhead | High | DESIGN_LINKS as single bridge; governance wins |
| Conflicting gates | Medium | Only state transitions require gates |
| Auditor complexity | Medium | Start simple; escalate ambiguous drifts |

---

## Readiness Assessment

| Dimension | Status |
|-----------|--------|
| Specifications | Complete (Parts IV-VII) |
| Dependencies | Clear (Phase 1 foundation) |
| Implementation patterns | Reusable from Phase 1 |
| Open questions | Minor clarifications only |

**Verdict: CONTINUE** - Ready for Phase 2 sprint planning
