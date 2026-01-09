# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Plugin Overview

The **agent-control-loop** plugin provides a minimal control loop system that drives LLM agents toward convergence on complex, high-risk software engineering tasks. It addresses the "80% completion problem" where agents stall at late-stage refactors and migrations.

**Status:** Phase 1 MVP - Core control loop implemented

## Commands

| Command | Description |
|---------|-------------|
| `/loop:init` | Bootstrap governance/ directory with 4 live artifacts |
| `/loop:phase` | Execute one phase of the control loop |
| `/loop:status` | Quick snapshot of governance state |

## Core Concepts

### The Problem This Solves

LLMs excel at "expansive, low-risk" work (moving files, renaming symbols, mechanical edits) but struggle with "convergent, high-risk" work (edge cases, cross-cutting invariants, migration logic). When faced with uncertainty, they defer work rather than resolve it, leading to incomplete migrations and resurrections of legacy code.

### Two Planes of Truth

**Execution Plane** (`governance/live/`) — what must be true right now:
- `TARGET.md` — target end state + Definition of Done
- `BOUNDARY.md` — single boundary rule + allowed bridge
- `BLOCKERS.md` — exhaustive list of ship-stoppers (the only work queue)
- `METRICS.md` — 2-4 monotonic measures of convergence

**Design Plane** (`/design/`) — what we intend to build (future):
- `current/` — canonical architecture & UX truth (binding)
- `active/` — accepted designs being executed (binding via DESIGN_LINKS)
- `proposals/` — candidate futures (non-binding)
- `archive/` — immutable history (non-binding)

### The Minimal Control Loop

Phase ritual performed at the start of each work phase:
1. Restate `TARGET`, `BOUNDARY`, `BLOCKERS`, `METRICS`
2. Choose exactly one highest-risk blocker
3. Work only to eliminate that blocker
4. Update artifacts and metrics
5. Repeat

This enforces:
- No deferral (only blockers exist as work)
- No resurrection (boundary law)
- No drift (target is always in view)
- No fake completion (metrics + DoD)

### Convergence Mode

When reaching ~80% completion, activate convergence mode:
- The only goal is eliminating blockers
- No new features, no deferrals
- Every issue must be fixed or explicitly escalated

## Workflow

### 1. Initialize Governance

```bash
/loop:init
```

Creates `governance/live/` directory with four artifact templates:
- Prompts for goal statement
- Scans repo for architecture boundaries
- Generates initial TARGET, BOUNDARY, BLOCKERS, METRICS

### 2. Execute Phase

```bash
/loop:phase
```

Runs the Governor agent through one phase ritual:
- Restates all 4 artifacts
- Selects single blocker to attack
- Plans 3-7 steps with verifications
- Executes work
- Updates artifacts
- Records outcome

### 3. Check Status

```bash
/loop:status
```

Quick snapshot showing:
- TARGET goal + DoD progress
- Active blockers (top 3)
- Metric values + deltas
- Recommended next action

## Key Agent

**Governor** (`agents/governor.md`):
- Owns the minimal control loop
- Maintains 4 live artifacts
- Chooses next blocker to attack
- Decides when to escalate to user
- Prevents scope drift, resurrection, unbounded planning

## Core Skills

**phase-ritual** (`skills/phase-ritual/SKILL.md`):
- Implements the 5-step phase ritual
- Artifact restatement
- Blocker selection with justification
- Phase plan generation (3-7 steps)
- Outcome recording

**artifact-templates** (`skills/artifact-templates/SKILL.md`):
- Templates for 4 live artifacts
- TARGET.md structure
- BOUNDARY.md structure
- BLOCKERS.md structure
- METRICS.md structure

## Anti-Patterns This System Prevents

- **Deferral**: "We should handle this later" — blocked by making blockers the only work queue
- **Resurrection**: Bringing back legacy code to satisfy tests — blocked by boundary law
- **Plan drift**: Following outdated plans — blocked by single canonical source of truth
- **False completion**: Claiming "done" at 80% — blocked by monotonic metrics and DoD

## Future Phases (Not Yet Implemented)

- Design Curator agent and /loop:design command
- Consistency Auditor agent
- /loop:escalate command with Decision Gatekeeper
- Hooks for artifact validation
- CI integration for boundary enforcement

## Documentation Structure

Design documentation lives in `docs/_now/control-loop-system/`:
- `CONTEXT-PRIME.md` — Authoritative specification
- Additional design docs for future phases

## Reading Order for Implementation

1. `docs/_now/control-loop-system/CONTEXT-PRIME.md` — Complete system spec
2. `agents/governor.md` — Governor agent behavior
3. `skills/phase-ritual/SKILL.md` — Phase ritual procedure
4. `skills/artifact-templates/SKILL.md` — Artifact templates
