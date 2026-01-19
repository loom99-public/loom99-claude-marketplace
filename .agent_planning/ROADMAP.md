---
version: "1.0"
created: 2026-01-18-224500
updated: 2026-01-18-224500
---

# Project Roadmap

## Phase 1: Plugin Cleanup
Goal: Fix orphaned components and documentation inconsistencies
Status: active

### Topics

- connect-orphaned-agents [PROPOSED]
  - Summary: Connect 3 orphaned agents (execution-summarizer, test-auditor, gabe) to workflows. execution-summarizer needs hooks wiring, test-auditor needs skill connection, gabe needs a command.
  - Directory: .agent_planning/connect-orphaned-agents/
  - Labels: P1, agents, do-more

- remove-duplicate-gabe [PROPOSED]
  - Summary: Remove duplicate gabe agent from do-extra plugin. Keep canonical version in do-more only. Violates one-source-of-truth principle.
  - Directory: .agent_planning/remove-duplicate-gabe/
  - Labels: P1, cleanup, do-extra

- fix-empty-hooks [PROPOSED]
  - Summary: do-more hooks.json is empty but CLAUDE.md documents execution logging via hooks. Either implement hooks or update documentation to reflect reality.
  - Directory: .agent_planning/fix-empty-hooks/
  - Labels: P1, hooks, do-more

## Phase 2: Feature Completion
Goal: Complete stub features and resolve namespace issues
Status: queued

### Topics

- implement-release-skill [PROPOSED]
  - Summary: /do:release is marked as STUB with no functionality. Implement version bumping, changelog generation, release notes, git tagging, or remove the command entirely.
  - Directory: .agent_planning/implement-release-skill/
  - Labels: P2, feature, do-more

- fix-research-command-collision [PROPOSED]
  - Summary: /do:research exists in both do (internal research) and do-more (external/market research) with different purposes. Rename do-more version to /do:market-research or /do:external-research.
  - Directory: .agent_planning/fix-research-command-collision/
  - Labels: P2, commands, namespace

## Phase 3: Maintainability
Goal: Improve long-term maintainability and consistency
Status: queued

### Topics

- standardize-skill-naming [PROPOSED]
  - Summary: Inconsistent skill naming - some use -skill suffix (it-skill, plan-skill), some don't (refactor, debug, fix). Establish and enforce naming convention.
  - Directory: .agent_planning/standardize-skill-naming/
  - Labels: P2, naming, consistency

- add-skill-agent-mapping [PROPOSED]
  - Summary: CLAUDE.md documents agent mapping but doesn't show which skills invoke which agents. Add skill→agent mapping table and workflow diagrams for better understanding.
  - Directory: .agent_planning/add-skill-agent-mapping/
  - Labels: P2, documentation

- archive-dead-docs [PROPOSED]
  - Summary: Dead documentation files in do-more (DESIGNING-AN-AGENT.md, FEATURE_PROPOSAL_subagent_execution_logging.md, HANDOFF.md) should be archived or deleted.
  - Directory: .agent_planning/archive-dead-docs/
  - Labels: P3, cleanup, documentation

- planning-artifact-cleanup [PROPOSED]
  - Summary: 8+ file types accumulate in .agent_planning/<topic>/. Consider adding cleanup command or archival strategy for stale artifacts.
  - Directory: .agent_planning/planning-artifact-cleanup/
  - Labels: P3, tooling

