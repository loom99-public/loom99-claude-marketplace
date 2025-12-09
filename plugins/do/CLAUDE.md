# do - Development Workflow with Skills

5 commands + 14 skills. Commands route to specialized skills based on intent.

## Commands (visible in autocomplete)

| Command | Purpose |
|---------|---------|
| `/do:plan` | Planning & evaluation |
| `/do:it` | Implementation & action |
| `/do:peek` | Fast codebase questions |
| `/do:learn` | Research |
| `/do:track` | Quick backlog capture |

## Skills (invoked by commands based on intent)

### Planning Skills (via `/do:plan`)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| `init-project` | "init", "new project", "start" | Initialize project |
| `audit` | "audit", "deep dive", "forensic" | Deep examination |
| `status-check` | "status", "check", "progress" | Quick diagnostic |
| `feature-proposal` | "feature", "proposal", "design" | Feature design |

### Implementation Skills (via `/do:it`)
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

### Research Skills (via `/do:learn`)
| Skill | Triggers | Purpose |
|-------|----------|---------|
| `market-research` | "market", "competitors", "external" | External/market research |

### Evaluator Skills (internal)
| Skill | Purpose |
|-------|---------|
| `evaluation-profiles` | Context-aware validation criteria for evaluators |

## Quick Reference

```bash
# Planning
/do:plan                    # Evaluate + plan (default)
/do:plan init my app        # → init-project skill
/do:plan audit security     # → audit skill
/do:plan status             # → status-check skill
/do:plan feature payments   # → feature-proposal skill

# Implementation
/do:it auth system          # Auto-select TDD/iterative
/do:it refactor auth        # → refactor skill
/do:it debug login failing  # → debug skill
/do:it fix issue #123       # → fix skill
/do:it review               # → review skill
/do:it test auth module     # → add-tests skill
/do:it chores               # → chores skill
/do:it tdd new feature      # → tdd-workflow skill

# Fast questions
/do:peek where is auth      # Direct execution

# Research
/do:learn jwt vs sessions   # Internal research (default)
/do:learn market            # → market-research skill

# Quick capture
/do:track fix login bug     # Direct execution
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
plugins/do/
├── commands/        # 5 visible commands
│   ├── plan.md
│   ├── it.md
│   ├── peek.md
│   ├── learn.md
│   └── track.md
├── skills/          # 14 skills (13 workflow + 1 internal)
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
│   ├── market-research.md
│   └── evaluation-profiles/  # Internal skill for evaluators
└── agents/          # 10 agents (execution engines)
```

## Beads Integration

If beads MCP tools available:
- `/do:track` creates issues directly
- `/do:plan` syncs P0/P1 items after planning
- `/do:it` updates issue status after implementation

No beads? Everything still works.
