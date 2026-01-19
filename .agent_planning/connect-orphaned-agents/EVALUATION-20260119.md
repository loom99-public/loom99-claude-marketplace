# Evaluation: Connect Orphaned Agents

**Generated**: 2026-01-19
**Topic**: Connect 3 orphaned agents to workflows

## Current State

### Three Orphaned Agents Identified

| Agent | File | Issue |
|-------|------|-------|
| `execution-summarizer` | `plugins/do-more/agents/execution-summarizer.md` | Documented in CLAUDE.md but hooks.json is empty |
| `test-auditor` | `plugins/do-more/agents/test-auditor.md` | No skill invokes it |
| `gabe` | `plugins/do-more/agents/gabe.md` | Well-documented but no command/skill |

### Agent Analysis

**execution-summarizer**:
- Purpose: Aggregates partial execution traces from subagents into a single coherent report
- Expected input: `.agent_logs/do/partials/<execution-id>-PARTIAL-*.txt`
- Expected output: `.agent_planning/EXEC-<cmd>-<timestamp>.md`
- Designed to run via Stop hook
- Current state: hooks.json is `{"hooks": {}}` - empty

**test-auditor**:
- Purpose: Forensic test coverage auditor
- Expected outputs: `TEST-AUDIT-<timestamp>.md`, `EXISTING_TEST_CONVENTIONS.md`
- Should be spawned by test-coverage-audit skill
- Current state: test-coverage-audit skill does work inline, never spawns agent

**gabe**:
- Purpose: Elite architecture surgeon for structural rigidity analysis
- Expected outputs: SYSTEM_MAP.md, NUCLEATION_SITES.md, INTERVENTION_PLAN.md, BOUNDARIES.md
- Has 5 phases (A-E) with clear workflow
- Current state: No command exists to invoke it

## What Needs to Change

1. **execution-summarizer**: Wire via Stop hook in hooks.json
2. **test-auditor**: Connect to test-coverage-audit skill
3. **gabe**: Create `/do:rigidity` command with skill wrapper

## Dependencies and Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hook execution fails | Low | Medium | Test in isolation, add error handling |
| Agent invocation breaks skill flow | Low | Medium | Test with mock execution |
| gabe requires careful user approval | Low | Medium | Add confirmation prompts |

## Verdict

**CONTINUE** - Clear path forward with established patterns to follow.
