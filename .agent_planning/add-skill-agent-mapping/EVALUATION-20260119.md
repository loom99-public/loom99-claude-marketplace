# Evaluation: Add Skill-Agent Mapping Documentation

**Generated**: 2026-01-19
**Topic**: Add missing skill→agent mapping documentation

## Current State

The `plugins/do-more/CLAUDE.md` currently documents:
1. Commands and their intent detection (lines 26-64)
2. Agent Mapping table showing "Used By" at command level (lines 66-88)
3. Skills Reference table with just purpose (lines 169-186)

**What's Missing** (per audit finding):
- Which skills invoke which agents (skill-level granularity)
- Complete skill dependency graph (skill-to-skill relationships)
- Workflow decision trees (visual flow understanding)

## Skill-to-Agent Mappings Discovered

| Skill | Invokes Agents | Notes |
|-------|----------------|-------|
| **Implementation Skills** | | |
| `tdd-workflow` | functional-tester, project-evaluator, test-driven-implementer, work-evaluator | Loops between agents |
| `iterative-workflow` | iterative-implementer, work-evaluator | Main implementation loop |
| `fix` | researcher, iterative-implementer, work-evaluator | Bug fix with verification |
| `debug` | researcher, work-evaluator | Root cause investigation only |
| `refactor` | project-evaluator, iterative-implementer, work-evaluator | Safe restructuring |
| `review` | project-evaluator | Code review mode |
| `add-tests` | project-evaluator, functional-tester, work-evaluator | Retroactive testing |
| **Audit Skills** | | |
| `audit-master` | None (self-contained) | Multi-dimension audit |
| `competitive-audit` | researcher | External research required |
| **Testing Skills** | | |
| `test-coverage-audit` | None (should invoke test-auditor) | Orphan connection needed |
| `testing-master` | Orchestrates test workflow skills | Pipeline coordinator |
| **Entry Point Skills** | | |
| `stuff-skill` | project-evaluator, status-planner, researcher, (tdd or iterative) | Full orchestration |
| `explore-skill` | researcher (explore mode) | Codebase-only |

## What Needs to Change

Add three new sections to CLAUDE.md after line 88:
1. **Skill-Agent Invocations table** (~20 lines)
2. **Skill Dependencies graph** (~25 lines)
3. **Workflow Decision Trees** (~20 lines)

## Verdict

**CONTINUE** - Clear documentation addition with well-defined content.
