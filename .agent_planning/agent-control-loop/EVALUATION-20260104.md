# Evaluation: agent-control-loop Plugin Implementation
**Generated:** 2026-01-04
**Status:** CONTINUE - Ready for planning

## Summary

The agent-control-loop plugin is a **design documentation repository with no plugin implementation yet**. It contains extensive, well-thought-out specifications for a minimal-control-loop system to drive LLM agents toward convergence on complex, high-risk software engineering work. The documentation is comprehensive (~2,800 lines across 13 key documents) but the plugin structure itself is empty.

---

## What Exists

### Design & Specification (Complete)
1. **Core Control Loop System** (docs/_now/control-loop-system/)
   - Problem statement: Why LLMs fail at convergence (80% stall)
   - Solution: Minimal control loop with 4 live artifacts
   - Two agent specs: Governor (required), Design Curator (design plane management)
   - Work tracking structure: governance/live/ + governance/roadmap/ + design/

2. **Governance Artifacts Specified** (CONTEXT-PRIME.md)
   - TARGET.md: Goal + non-goals + target shape + Definition of Done
   - BOUNDARY.md: Single boundary law + bridge definition + forbidden dependencies
   - BLOCKERS.md: Exhaustive list of ship-stoppers (work queue)
   - METRICS.md: 2-4 monotonic convergence measures

3. **Design Plane Specified** (3-design-hub.md)
   - /design/current/ - Authoritative big picture (binding)
   - /design/proposals/ - Candidate futures (non-binding)
   - /design/active/ - Designs under execution
   - /design/archive/ - Immutable history
   - DESIGN_LINKS.md - Bridge between design and governance

4. **Intake Surface** (CONTROL-SURFACE-intake.md)
   - /design/intake/ for human-authored intent injection
   - INTAKE.md: User-facing outcome + technical outcome + constraints + acceptance checks

5. **Token Efficiency Guidelines** (docs/_now/lightweight-governance/)
   - How to compress hard rules into minimal contract
   - How to compress soft rules into operating philosophy

---

## What's Missing (Plugin Implementation)

### Required Plugin Structure
- `.claude-plugin/plugin.json` manifest - **MISSING**
- `commands/` directory - **MISSING**
- `agents/` directory - **MISSING**
- `skills/` directory - **MISSING**
- `hooks/` directory - **MISSING**
- Marketplace registration - **NOT IN marketplace.json**

### Required Commands
1. **/loop:init** - Initialize governance/ and design/ directories with templates
2. **/loop:phase** - Execute phase ritual (restate artifacts, select blocker, plan, execute)
3. **/loop:convergence** - Activate convergence mode
4. **/loop:status** - Quick snapshot of TARGET/BLOCKERS/METRICS state
5. **/loop:escalate** - Escalate decisions to human with options
6. **/loop:design** - Access design curation interface

### Required Agents
1. **Governor** - Owns control loop execution (phase ritual, blocker selection, deferral detection)
2. **Design Curator** - Manages design plane lifecycle
3. **Consistency Auditor** - Checks design↔governance↔repo alignment

### Required Skills
1. **control-loop-initialization** - Bootstrap governance/ + design/ directories
2. **artifact-restatement** - Restate TARGET/BOUNDARY/BLOCKERS/METRICS
3. **blocker-selection** - Justify single blocker selection
4. **convergence-checker** - Detect deferral/resurrection/drift patterns
5. **design-state-machine** - Validate design artifact lifecycle transitions

---

## Gaps Between Design & Plugin Requirements

1. **Command-Agent Mapping Undefined** - Design doesn't specify which command calls which agent
2. **Artifact I/O Not Specified** - No templating system, diff mechanism, or format validation
3. **Escalation UI Underspecified** - Protocol exists but presentation format missing
4. **Metrics Measurement Automation Unspecified** - No scripts for automated measurement

---

## Dependencies & Risks

### Hard Blockers
1. Plugin manifest required for Claude Code to recognize plugin
2. Marketplace registration required for skill auto-discovery

### Moderate Risks
1. Token budget for artifact restatement (phase ritual restates all 4 artifacts)
2. Five mandatory human gates could become bottleneck
3. Boundary enforcement without CI integration is advisory only

---

## Ambiguities & Open Questions

1. **Proposal Compilation** - How does agent present multiple candidate architectures?
2. **Blockers vs Roadmap Boundary** - Can roadmap items be promoted mid-phase?
3. **Test Triage Classification** - How is classification stored?
4. **Metrics Staleness Threshold** - What is N for "escalate after N stagnant phases"?
5. **"One Screen" Definition** - What's the token/line budget for artifacts?

---

## Recommended Implementation Order

**Phase 1 (Minimal Viable Product):**
1. Create plugin.json manifest
2. Implement `/loop:init` command (scaffold governance/ + design/ with templates)
3. Implement Governor agent (phase ritual + blocker selection)
4. Create 4 artifact templates with schemas
5. Implement `/loop:phase` command
6. Implement `/loop:status` command
7. Add to marketplace.json

**Phase 2 (Design Plane):**
8. Implement Design Curator agent
9. Implement `/loop:design` command
10. Add proposal lifecycle management

**Phase 3 (Audit & Escalation):**
11. Implement Consistency Auditor agent
12. Implement `/loop:escalate` command
13. Add hooks for artifact validation

---

## Readiness Assessment

| Dimension | Status | Notes |
|-----------|--------|-------|
| Design Completeness | 90% | Comprehensive; needs clarification on escalation UI |
| Plugin Structure | 0% | Only docs; missing all plugin components |
| Pattern Alignment | 70% | Matches Claude Code patterns; needs skill patterns |
| Implementation Risk | Medium | High artifact overhead; needs testing at scale |

**Verdict: CONTINUE** - Sufficient design clarity for Phase 1 implementation.
