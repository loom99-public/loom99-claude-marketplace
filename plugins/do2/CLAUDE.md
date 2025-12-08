# do2 - Streamlined Development Workflow

5 commands. That's it.

## Commands

| Command | Purpose | Modes |
|---------|---------|-------|
| `/do2:plan` | Planning & evaluation | `init`, `audit`, `status`, `feature`, default |
| `/do2:it` | Implementation & action | `refactor`, `debug`, `fix`, `review`, `test`, `chores`, `tdd`, `iterate`, default |
| `/do2:peek` | Fast codebase questions | - |
| `/do2:learn` | Research | `market`, `external`, default (internal) |
| `/do2:track` | Quick backlog capture | - |

## Quick Reference

### `/do2:plan`

```bash
/do2:plan                    # Evaluate + plan (default)
/do2:plan init my app        # Initialize new project
/do2:plan audit security     # Deep audit
/do2:plan status             # Quick status check
/do2:plan feature payments   # Feature proposal
```

### `/do2:it`

```bash
/do2:it auth system          # Implement (auto-select TDD/iterative)
/do2:it refactor auth        # Refactoring workflow
/do2:it debug login failing  # Debug investigation
/do2:it fix issue #123       # Bug fix workflow
/do2:it review               # Code review (recent changes)
/do2:it test auth module     # Add tests to existing code
/do2:it chores               # Maintenance (quick)
/do2:it chores thorough      # Maintenance (deep)
/do2:it tdd new feature      # Explicit TDD
/do2:it iterate ui work      # Explicit iterative
```

### `/do2:peek`

```bash
/do2:peek where is auth      # Fast codebase navigation
/do2:peek how does X work    # Quick understanding
```

### `/do2:learn`

```bash
/do2:learn jwt vs sessions   # Internal/technical research
/do2:learn market            # Competitive analysis
/do2:learn market auth libs  # External research on topic
/do2:learn external trends   # General web research
```

### `/do2:track`

```bash
/do2:track fix login bug     # P2 task (defaults)
/do2:track 1 bug auth fails  # P1 bug
/do2:track 0 feature export  # P0 feature
```

## Philosophy

**Fewer commands, more capability.**

Each command detects intent from the first word and routes to the appropriate workflow. Power users discover modes through docs. Casual users stick to defaults.

**Planning docs are source of truth.**

All state lives in `.agent_planning/`. Beads integration is optional enhancement.

**No magic, just routing.**

Mode detection is explicit (first word), not fuzzy NLP. You know what you're getting.

## File Structure

```
plugins/do2/
├── .claude-plugin/plugin.json
├── commands/
│   ├── plan.md      # /do2:plan
│   ├── it.md        # /do2:it
│   ├── peek.md      # /do2:peek
│   ├── learn.md     # /do2:learn
│   └── track.md     # /do2:track
├── agents/
│   ├── project-architect.md      # Project initialization
│   ├── project-evaluator.md      # Gap analysis, audits
│   ├── status-planner.md         # Backlog generation
│   ├── functional-tester.md      # Test design (TDD)
│   ├── test-driven-implementer.md # TDD implementation
│   ├── iterative-implementer.md  # Iterative implementation
│   ├── work-evaluator.md         # Runtime validation
│   ├── researcher.md             # Research (internal + external)
│   ├── product-visionary.md      # Feature proposals
│   └── execution-summarizer.md   # Execution logging
└── CLAUDE.md
```

## Agents

| Agent | Used By | Purpose |
|-------|---------|---------|
| project-architect | `plan init` | Adaptive project initialization |
| project-evaluator | `plan`, `plan audit`, `plan status`, `it review` | Gap analysis, evaluation |
| status-planner | `plan` | Backlog generation |
| functional-tester | `it tdd`, `it test` | Test design |
| test-driven-implementer | `it tdd` | TDD implementation |
| iterative-implementer | `it`, `it iterate`, `it refactor`, `it fix` | Iterative implementation |
| work-evaluator | `it`, `plan status` | Runtime validation |
| researcher | `learn`, `peek`, `it debug` | Research and investigation |
| product-visionary | `plan feature` | Feature proposals |
| execution-summarizer | All commands (optional) | Execution logging |

## Beads Integration

If beads MCP tools are available:
- `/do2:track` creates issues directly
- `/do2:plan` syncs P0/P1 items after planning
- `/do2:it` updates issue status after implementation

No beads? Everything still works - beads is optional enhancement.

## Migration from do-more-now

| Old Command | New Command |
|-------------|-------------|
| `/do:plan` | `/do2:plan` |
| `/do:it` | `/do2:it` |
| `/do:status` | `/do2:plan status` |
| `/do:peek` | `/do2:peek` |
| `/do:audit` | `/do2:plan audit` |
| `/do:chores` | `/do2:it chores` |
| `/do:learn` | `/do2:learn` |
| `/do:research` | `/do2:learn market` or `/do2:learn external` |
| `/do:track` | `/do2:track` |
| `/do:init-project` | `/do2:plan init` |
| `/do:feature-proposal` | `/do2:plan feature` |
