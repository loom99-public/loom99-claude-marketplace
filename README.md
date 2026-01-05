# do

**Get out of the weeds. Stay in the loop.**

A Claude Code plugin for structured development workflows.

## Why?

You want Claude to do the work. But full delegation usually means losing visibility. `do` gives you both.

**Claude handles the weeds:**
- Evaluates your codebase to find gaps
- Proposes a plan with clear scope
- Implements incrementally
- Verifies against acceptance criteria

**You stay in the loop:**
- Approve the plan before work begins
- Answer clarifying questions that shape the approach
- Review after each step, course-correct as needed
- Decide when it's done

## In Practice

```bash
# Add a feature
/do:plan add user authentication
/do:it

# Fix something
/do:plan fix the checkout flow breaking on mobile
/do:it

# Refactor
/do:plan migrate from REST to GraphQL
/do:it

# Or skip straight to implementation (chains to planning if needed)
/do:it add dark mode toggle
```

Claude evaluates your codebase, asks clarifying questions, proposes a scoped plan, and waits for your approval before implementing. After each step, you review and decide whether to continue.

## Installation

```bash
# Add the marketplace
claude plugin marketplace add loom99-public/loom99-claude-marketplace

# Install the core plugin
claude plugin install do

# Optional: install extended tools
claude plugin install do-more
```

**Requirements:** Claude Code 1.0.33+

## The Workflow

```
/do:plan <prompt>  →  /do:it <prompt>
```

That's it. Plan what you want to build, then build it.

```bash
# Plan first
/do:plan add user authentication

# Then implement
/do:it

# Or go straight to implementation (chains to plan if needed)
/do:it add user authentication
```

The `<prompt>` can be anything—a feature, a bug fix, a refactor. Medium-sized units of work tend to flow best.

## Core Commands

| Command | Purpose |
|---------|---------|
| `/do:plan <prompt>` | Evaluate project state, create implementation plan |
| `/do:it <prompt>` | Implement with planning and verification |
| `/do:status` | Quick status check: WIP, uncommitted changes, next work |
| `/do:roadmap` | View or build a longer-term project roadmap |
| `/do:research <question>` | Investigate options, look things up online |

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

**Outer Loop** (`/do:plan`): Evaluate project state → research unknowns → plan one sprint

**Inner Loop** (`/do:it`): Define acceptance criteria → implement → verify → iterate

Planning documents live in `.agent_planning/`:
- `EVALUATION-*.md` — Gap analysis of current state
- `PLAN-*.md` — Prioritized work items with acceptance criteria
- `ROADMAP.md` — High-level phases and topics (optional)

## Example

```bash
/do:plan add OAuth login

# Claude evaluates codebase, asks:
# > "Which OAuth providers? Google, GitHub, others?"
# You: "Google and GitHub"

# Claude creates plan:
# 1. Google OAuth integration
# 2. GitHub OAuth integration

/do:it

# Claude implements Google OAuth → you test → approve
# Claude implements GitHub OAuth → you test → approve
# Done
```

## do-more (Optional)

Extended tools for specific tasks:

| Command | Purpose |
|---------|---------|
| `/do:audit` | Code quality, security, or test coverage audit |
| `/do:fix <issue>` | Fix a specific bug |
| `/do:debug <problem>` | Investigate root cause |
| `/do:refactor <target>` | Restructure without behavior change |
| `/do:test` | Testing audit and implementation |
| `/do:tdd` | Test-driven development workflow |
| `/do:chores` | Maintenance and cleanup tasks |

Install with: `claude plugin install do-more`

## License

PolyForm Internal Use License 1.0.0

---

**Author**: Brandon Fryslie
