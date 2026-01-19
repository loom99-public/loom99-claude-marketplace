# Sprint: connect-agents

**Generated**: 2026-01-19
**Confidence**: HIGH
**Status**: READY FOR IMPLEMENTATION

## Sprint Goal

Connect 3 orphaned agents to their intended workflows, making them accessible to users.

## Scope

**Deliverables:**
1. Wire execution-summarizer via Stop hook
2. Connect test-auditor to test-coverage-audit skill
3. Create /do:rigidity command for gabe agent

## Work Items

### P0: Wire execution-summarizer via hooks

**Files to modify:**
- `plugins/do-more/hooks/hooks.json` - Add Stop hook entry

**Hook Pattern** (based on do/hooks/hooks.json):
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check for partial execution logs in .agent_logs/do/partials/. If any exist, spawn execution-summarizer agent to aggregate them into final report."
          }
        ]
      }
    ]
  }
}
```

**Acceptance Criteria:**
- [ ] hooks.json has Stop hook configured
- [ ] execution-summarizer is invoked at end of commands
- [ ] EXEC-*.md reports are created when partial logs exist

### P1: Connect test-auditor to test-coverage-audit skill

**Files to modify:**
- `plugins/do-more/skills/test-coverage-audit/SKILL.md` - Add agent spawn

**Pattern:**
```markdown
For phases 2-5, use the Task tool to spawn `test-auditor` agent with:
- Project path
- Detected framework (from Phase 1)
- Intensity level (quick/medium/thorough)
```

**Acceptance Criteria:**
- [ ] test-coverage-audit skill spawns test-auditor agent
- [ ] test-auditor produces TEST-AUDIT-*.md output
- [ ] Existing skill orchestration preserved

### P2: Create /do:rigidity command for gabe

**Files to create:**
1. `plugins/do-more/commands/rigidity.md` - New command
2. `plugins/do-more/skills/rigidity-skill/SKILL.md` - New skill

**Command Pattern:**
```markdown
---
argument-hint: [quick|diagnose|intervene]
description: "Analyze codebase rigidity - coupling, dependencies, change friction"
---

Invoke the plugin skill "rigidity-skill".
```

**Acceptance Criteria:**
- [ ] `/do:rigidity` command exists
- [ ] rigidity-skill spawns gabe agent
- [ ] gabe produces expected artifacts (SYSTEM_MAP.md, etc.)
- [ ] Human approval checkpoints work

## Dependencies

All tasks can run in parallel - no dependencies between them.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hook fails silently | Low | Medium | Add error logging |
| gabe actions are destructive | Low | High | Require user approval |
