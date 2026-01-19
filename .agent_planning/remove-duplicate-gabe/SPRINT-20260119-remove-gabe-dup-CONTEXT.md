# Implementation Context: remove-gabe-dup

**Sprint**: remove-gabe-dup
**Generated**: 2026-01-19

## Background

The gabe agent is an "elite software architecture surgeon" for structural rigidity analysis. It was duplicated across two plugins:

1. **do-more** - Primary development workflow plugin (canonical location)
2. **do-extra** - Experimental niche tools plugin (inappropriate location)

The files are byte-for-byte identical (verified via diff).

## Why This Cleanup

- **One Source of Truth**: gabe must exist in exactly one location
- **Maintenance Risk**: Duplicates can drift over time
- **Semantic Fit**: gabe is serious development tooling, belongs in do-more not do-extra

## File Locations

```
plugins/
├── do-more/
│   └── agents/
│       └── gabe.md           # KEEP - canonical version
└── do-extra/
    ├── agents/
    │   └── gabe.md           # DELETE - duplicate
    └── README.md             # UPDATE - remove gabe references
```

## Related Context

- **Audit Source**: `.agent_planning/AUDIT-plugin-workflows-20260118.md` identified this as P1 issue
- **Roadmap**: `.agent_planning/ROADMAP.md` lists this in Phase 1: Plugin Cleanup
- **Related Work**: `connect-orphaned-agents` roadmap item will later create command to invoke gabe

## What gabe Does

The gabe agent specializes in:
- Structural rigidity analysis
- Dependency centrality detection
- Cycle and coupling identification
- Boundary insertion recommendations

It produces artifacts in `.agent_planning/rigidity_breaker/<date>-<topic>/`:
- SYSTEM_MAP.md
- NUCLEATION_SITES.md
- INTERVENTION_PLAN.md
- BOUNDARIES.md
- STABILIZATION_QUEUE.md

## After This Sprint

gabe will exist only in do-more. A future sprint (connect-orphaned-agents) will create a `/do:rigidity` command to invoke gabe.
