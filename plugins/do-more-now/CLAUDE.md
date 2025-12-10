# do - Development Workflow

7 commands organized by functional area.

## Commands

| Command | Category | Purpose |
|---------|----------|---------|
| `/do:it` | Implement | Build, fix, refactor, debug, test, review |
| `/do:plan` | Plan | Evaluate status, create plans, track backlog |
| `/do:explore` | Explore | Ask questions about codebase, compare internal ideas |
| `/do:research` | Research | Learn from external sources, market analysis |
| `/do:chores` | Chores | Maintenance, cleanup, housekeeping |
| `/do:docs` | Docs | README, API docs, architecture docs |
| `/do:release` | Release | Versioning, changelog, release notes (stub) |

## Quick Reference

### `/do:it` - Implement

```bash
/do:it auth system          # Auto-select TDD/iterative
/do:it tdd new feature      # Explicit TDD workflow
/do:it iterate ui work      # Explicit iterative workflow
/do:it fix issue #123       # Bug fix
/do:it refactor auth        # Refactoring
/do:it debug login failing  # Debug investigation
/do:it test auth module     # Add tests
/do:it review               # Code review
```

### `/do:plan` - Plan & Track

```bash
/do:plan                    # Evaluate + plan (default)
/do:plan status             # Quick status check
/do:plan audit security     # Deep audit
/do:plan init my app        # Initialize new project
/do:plan feature payments   # Feature proposal
/do:plan track fix bug      # Quick backlog capture (requires beads)
```

### `/do:explore` - Internal Questions

```bash
/do:explore where is auth   # Find code locations
/do:explore how does X work # Understand internals
/do:explore compare A vs B  # Compare internal approaches
```

### `/do:research` - External Research

```bash
/do:research jwt best practices    # Industry patterns
/do:research competitors           # Market analysis
/do:research react docs hooks      # External documentation
```

### `/do:chores` - Maintenance

```bash
/do:chores                  # Quick cleanup (default)
/do:chores thorough         # Deep cleanup
/do:chores git              # Git hygiene only
/do:chores deps             # Dependencies only
/do:chores debt             # Tech debt inventory
```

### `/do:docs` - Documentation

```bash
/do:docs                    # Assess and suggest
/do:docs readme             # Update README
/do:docs api                # Generate API docs
/do:docs architecture       # Update architecture docs
```

### `/do:release` - Release (Stub)

```bash
/do:release                 # Shows stub message
```

## Category Philosophy

| Category | Focus | Sources |
|----------|-------|---------|
| **Implement** | Build and change code | Codebase |
| **Plan** | Where are we, where to go | Status, specs, backlog |
| **Explore** | Learn from project | Codebase only |
| **Research** | Learn from outside | Web, docs, competitors |
| **Chores** | Keep things clean | Git, deps, code |
| **Docs** | Keep docs current | README, API, arch |
| **Release** | Ship it | Version, changelog, tags |

## File Structure

```
plugins/do-more-now/
├── commands/           # 7 commands
│   ├── it.md           # Implement
│   ├── plan.md         # Plan & track
│   ├── explore.md      # Internal exploration
│   ├── research.md     # External research
│   ├── chores.md       # Maintenance
│   ├── docs.md         # Documentation
│   └── release.md      # Release (stub)
├── skills/             # Specialized workflows
│   ├── init-project.md
│   ├── audit.md
│   ├── status-check.md
│   ├── feature-proposal.md
│   ├── refactor.md
│   ├── debug.md
│   ├── fix.md
│   ├── review.md
│   ├── add-tests.md
│   ├── tdd-workflow.md
│   ├── iterative-workflow.md
│   ├── market-research.md
│   └── evaluation-profiles/
└── agents/             # 10 execution engines
```

## Agents

| Agent | Used By | Purpose |
|-------|---------|---------|
| project-architect | `plan init` | Project initialization |
| project-evaluator | `plan`, `plan audit` | Gap analysis |
| status-planner | `plan` | Backlog generation |
| functional-tester | `it tdd`, `it test` | Test design |
| test-driven-implementer | `it tdd` | TDD implementation |
| iterative-implementer | `it`, `chores`, `docs` | Iterative work |
| work-evaluator | `it`, `plan status` | Runtime validation |
| researcher | `explore`, `research` | Investigation |
| product-visionary | `plan feature` | Feature proposals |
| execution-summarizer | All commands | Execution logging |

## Beads Integration

If beads MCP tools available:
- `/do:plan track` creates issues
- `/do:plan` syncs P0/P1 items
- `/do:it` updates issue status

No beads? Everything still works.
