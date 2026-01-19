# Implementation Context: skill-mapping

**Sprint**: skill-mapping
**Generated**: 2026-01-19

## Background

The audit found that while CLAUDE.md documents agents and commands, it lacks:
- Skill-level granularity (which skills invoke which agents)
- Skill-to-skill dependencies
- Visual workflow decision trees

This makes understanding plugin internals require reading many files.

## Critical Files

### File to Modify

**`plugins/do-more/CLAUDE.md`**
- Add ~65 lines of documentation
- Insert after line 88 (existing Agent Mapping section)

### Reference Files (for accuracy verification)

- `plugins/do-more/skills/tdd-workflow/SKILL.md` - TDD agent sequence
- `plugins/do-more/skills/stuff-skill/SKILL.md` - Orchestration pattern
- `plugins/do-more/skills/audit-master/SKILL.md` - Audit dimension routing
- `plugins/do-more/skills/iterative-workflow/SKILL.md` - Implementation loop
- `plugins/do-more/skills/testing-master/SKILL.md` - Testing pipeline

## Content to Add

### Section 1: Skill-Agent Invocations Table

Maps each skill to the agents it spawns via Task tool.

Key mappings:
- `tdd-workflow` → functional-tester, project-evaluator, test-driven-implementer, work-evaluator
- `iterative-workflow` → iterative-implementer, work-evaluator
- `fix` → researcher, iterative-implementer, work-evaluator
- `debug` → researcher, work-evaluator
- `refactor` → project-evaluator, iterative-implementer, work-evaluator

### Section 2: Skill Dependencies Graph

Shows how skills chain together in pipelines:
- Audit pipeline: audit-master → dimension-specific skills
- Testing pipeline: testing-master → setup/audit/recommend/plan
- Implementation pipeline: stuff-skill → research/evaluate/implement

### Section 3: Workflow Decision Trees

Shows how user intent maps to skill selection for:
- `/do:it` - keyword detection to skill routing
- `/do:test` - action detection to test workflow skills

## Format Consistency

Match existing CLAUDE.md patterns:
- Tables use `| col | col |` format
- Code blocks use triple backticks
- Headers use `##` for major sections
- Indentation with spaces
