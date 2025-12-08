# do3 - Development Workflow with Skills

5 commands + 13 skills. Commands route to specialized skills based on intent.

## Commands (visible in autocomplete)

| Command | Purpose |
|---------|---------|
| `/do3:plan` | Planning & evaluation |
| `/do3:it` | Implementation & action |
| `/do3:peek` | Fast codebase questions |
| `/do3:learn` | Research |
| `/do3:track` | Quick backlog capture |

## Skills (invoked by commands based on intent)

### Planning Skills (via `/do3:plan`)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| `init-project` | "init", "new project", "start" | Initialize project |
| `audit` | "audit", "deep dive", "forensic" | Deep examination |
| `status-check` | "status", "check", "progress" | Quick diagnostic |
| `feature-proposal` | "feature", "proposal", "design" | Feature design |

### Implementation Skills (via `/do3:it`)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| `refactor` | "refactor", "restructure", "clean up" | Safe restructuring |
| `debug` | "debug", "investigate", "root cause" | Bug investigation |
| `fix` | "fix", "bug", "broken" | Bug fix |
| `review` | "review", "PR", "code review" | Code review |
| `add-tests` | "test", "add tests", "coverage" | Retroactive testing |
| `chores` | "chores", "cleanup", "maintenance" | Housekeeping |
| `tdd-workflow` | "tdd", "test first" | TDD implementation |
| `iterative-workflow` | "iterate", "iterative" | Iterative implementation |

### Research Skills (via `/do3:learn`)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| `market-research` | "market", "competitors", "external" | External/market research |

## Quick Reference

```bash
# Planning
/do3:plan                    # Evaluate + plan (default)
/do3:plan init my app        # → init-project skill
/do3:plan audit security     # → audit skill
/do3:plan status             # → status-check skill
/do3:plan feature payments   # → feature-proposal skill

# Implementation
/do3:it auth system          # Auto-select TDD/iterative
/do3:it refactor auth        # → refactor skill
/do3:it debug login failing  # → debug skill
/do3:it fix issue #123       # → fix skill
/do3:it review               # → review skill
/do3:it test auth module     # → add-tests skill
/do3:it chores               # → chores skill
/do3:it tdd new feature      # → tdd-workflow skill

# Fast questions
/do3:peek where is auth      # Direct execution

# Research
/do3:learn jwt vs sessions   # Internal research (default)
/do3:learn market            # → market-research skill

# Quick capture
/do3:track fix login bug     # Direct execution
```

## How It Works

1. User types command with natural language
2. Command detects intent from keywords
3. Command invokes appropriate skill using the Skill tool
4. Skill has access to conversation context
5. Skill executes specialized workflow

**Progressive disclosure**: Only 5 commands in autocomplete. Skills are invisible but discoverable via docs.

## File Structure

```
plugins/do3/
├── commands/        # 5 visible commands
│   ├── plan.md
│   ├── it.md
│   ├── peek.md
│   ├── learn.md
│   └── track.md
├── skills/          # 13 invisible skills
│   ├── init-project.md
│   ├── audit.md
│   ├── status-check.md
│   ├── feature-proposal.md
│   ├── refactor.md
│   ├── debug.md
│   ├── fix.md
│   ├── review.md
│   ├── add-tests.md
│   ├── chores.md
│   ├── tdd-workflow.md
│   ├── iterative-workflow.md
│   └── market-research.md
└── agents/          # 10 agents (execution engines)
```

## Beads Integration

If beads MCP tools available:
- `/do3:track` creates issues directly
- `/do3:plan` syncs P0/P1 items after planning
- `/do3:it` updates issue status after implementation

No beads? Everything still works.

## Migration

| do-more-now (11 commands) | do3 (5 commands) |
|---------------------------|------------------|
| `/do:plan` | `/do3:plan` |
| `/do:status` | `/do3:plan status` |
| `/do:audit` | `/do3:plan audit` |
| `/do:init-project` | `/do3:plan init` |
| `/do:feature-proposal` | `/do3:plan feature` |
| `/do:it` | `/do3:it` |
| `/do:chores` | `/do3:it chores` |
| `/do:peek` | `/do3:peek` |
| `/do:learn` | `/do3:learn` |
| `/do:research` | `/do3:learn market` |
| `/do3:track` | `/do3:track` |
