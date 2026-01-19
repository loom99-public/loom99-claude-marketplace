# Implementation Context: connect-agents

**Sprint**: connect-agents
**Generated**: 2026-01-19

## Background

The audit found three well-designed agents that exist but have no invocation path:
- execution-summarizer: Designed for Stop hook aggregation
- test-auditor: Designed for forensic test analysis
- gabe: Designed for rigidity/coupling analysis

This sprint connects them to their intended workflows.

## Critical Files

### Files to Modify

1. **`plugins/do-more/hooks/hooks.json`**
   - Current: `{"hooks": {}}`
   - Add: Stop hook for execution-summarizer

2. **`plugins/do-more/skills/test-coverage-audit/SKILL.md`**
   - Add: Agent spawn for test-auditor in phases 2-5

### Files to Create

1. **`plugins/do-more/commands/rigidity.md`**
   - Command wrapper for rigidity-skill

2. **`plugins/do-more/skills/rigidity-skill/SKILL.md`**
   - Skill that spawns gabe agent
   - Should follow patterns from other skills

### Reference Files

- `plugins/do/hooks/hooks.json` - Pattern for hook configuration
- `plugins/do/skills/it-skill/SKILL.md` - Pattern for agent invocation
- `plugins/do-more/agents/gabe.md` - Agent specification

## Agent Capabilities

### execution-summarizer
- Uses haiku model (context-efficient)
- Reads partial logs from `.agent_logs/do/partials/`
- Writes summary to `.agent_planning/EXEC-<cmd>-<timestamp>.md`

### test-auditor
- Forensic analysis across 6 phases
- Detects testing infrastructure
- Analyzes complexity sources
- Identifies coverage gaps

### gabe
- 5-phase workflow (A-E)
- Phase A: System survey
- Phase B: Nucleation site identification
- Phase C: Intervention design
- Phase D: Boundary installation
- Phase E: Stabilization
- Requires human approval for destructive actions

## Workflow Integration

### execution-summarizer Flow
```
Any /do:* command completes
    └── Stop hook fires
        └── Check for partial logs
            └── If exist: spawn execution-summarizer
                └── Agent aggregates into EXEC-*.md
```

### test-auditor Flow
```
/do:test audit
    └── test-coverage-audit skill
        └── Phase 1: Infrastructure detection (skill)
        └── Phases 2-5: spawn test-auditor agent
            └── Agent produces TEST-AUDIT-*.md
```

### gabe Flow
```
/do:rigidity [quick|diagnose|intervene]
    └── rigidity-skill
        └── spawn gabe agent
            └── Phase A: Survey → SYSTEM_MAP.md
            └── Phase B: Analysis → NUCLEATION_SITES.md
            └── [Checkpoint: User approval]
            └── Phase C: Design → INTERVENTION_PLAN.md
            └── Phase D: Install → BOUNDARIES.md
            └── Phase E: Stabilize → STABILIZATION_QUEUE.md
```
