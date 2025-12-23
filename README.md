# dev-loop

A Claude Code plugin that runs your development workflow as a continuous feedback loop. Evaluate, plan, implement, verify—repeat.

## Installation

### From the Marketplace

```bash
# Add the marketplace
claude plugin marketplace add loom99-public/loom99-claude-marketplace

# Install the plugin
claude plugin install lp
```

Or from within Claude Code:
```
/plugin marketplace add loom99-public/loom99-claude-marketplace
/plugin install lp
```

### Local Development

```bash
claude --plugin-dir ./plugins/dev-loop
```

**Requirements:** Claude Code 1.0.33+

## Quick Start

```bash
# Implement something (chains to /lp:plan if needed)
/lp:impl add user authentication

# Just plan first
/lp:plan add user authentication

# Quick status check
/lp:status
```

## Commands

| Command | What it does |
|---------|--------------|
| `/lp:impl` | Implement a feature with planning and verification |
| `/lp:plan` | Evaluate current state and create implementation plan |
| `/lp:tdd` | Test-driven development: tests first, then implement |
| `/lp:status` | Quick status check: WIP, uncommitted changes, next work |
| `/lp:init-project` | Initialize a new project with comprehensive spec |
| `/lp:feature-proposal` | Design a new feature |
| `/lp:research` | Investigate ambiguities and options |
| `/lp:roadmap` | View or add to project roadmap |

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTER LOOP (Planning)                       │
│                                                                     │
│    ┌──────────┐     ┌──────────┐     ┌──────────┐                  │
│    │ EVALUATE │ ◀─▶ │ RESEARCH │ ──▶ │   PLAN   │                  │
│    └──────────┘     └──────────┘     └──────────┘                  │
│          │                                │                         │
│    Updates cache                    ONE SPRINT only                │
│          │                                │                         │
│          ▼                                ▼                         │
│    ┌────────────────────────────────────────────────────────────┐  │
│    │                  INNER LOOP (Implementation)               │  │
│    │                                                            │  │
│    │  ┌──────────────┐    ┌───────────┐    ┌──────────┐        │  │
│    │  │ DEFINITION   │───▶│ IMPLEMENT │───▶│  VERIFY  │        │  │
│    │  │   OF DONE    │    │           │    │          │        │  │
│    │  └──────────────┘    └───────────┘    └──────────┘        │  │
│    │         │                  │               │              │  │
│    │         └──────────────────┴───────────────┘              │  │
│    │                    Feedback loop                          │  │
│    └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

**Outer Loop**: Evaluate project state → research unknowns → plan ONE sprint

**Inner Loop**: Define acceptance criteria → implement → verify → get user feedback

## Workflows

### TDD Workflow (`/lp:tdd`)

Best for: APIs, backend services, libraries, clear requirements

1. Writes functional tests first
2. Implements until tests pass
3. No shortcuts—tests must validate real behavior

### Iterative Workflow (`/lp:impl`)

Best for: UI work, exploratory features, visual validation

1. Implements incrementally
2. Validates with runtime evidence (screenshots, logs)
3. User reviews after each task

## Key Principles

- **One sprint at a time**: 2-3 deliverables max. Everything else is explicitly deferred.
- **Definition of Done first**: Clear acceptance criteria before any coding.
- **Frequent feedback**: User review after every significant task.
- **Evaluation caching**: Don't re-evaluate what hasn't changed.
- **No shortcuts**: Tests must fail with stubs. Implementation must be real.

## Planning Documents

All workflow state lives in `.agent_planning/`:

```
.agent_planning/
├── PROJECT_SPEC.md      # Requirements (authoritative)
├── ROADMAP.md           # High-level phases and topics
├── STATUS-*.md          # Current implementation state
├── PLAN-*.md            # Sprint backlog
├── RESEARCH-*.md        # Research findings
└── archive/             # Superseded documents
```

## Example

```bash
# Start with planning
/lp:plan add OAuth login

# Claude evaluates codebase, asks clarifying questions
# > "Which OAuth providers should we support?"
# You answer: "Google and GitHub"

# Claude generates plan with 2 deliverables:
# 1. Google OAuth integration
# 2. GitHub OAuth integration
# (Microsoft, Apple deferred to future sprint)

# Implement with user feedback after each task
/lp:impl

# Claude implements Google OAuth → you test → approve
# Claude implements GitHub OAuth → you test → "callback URL wrong" → fix → approve
# Validation phase → all criteria met → complete
```

## License

PolyForm Internal Use License 1.0.0

---

**Version**: 0.2.2 | **Author**: Brandon Fryslie
