---

![do-more-now](https://raw.githubusercontent.com/loom99-public/loom99-claude-marketplace/refs/heads/master/assets/do-more-now-2.svg)

**What you already know you should be doing - only better.**

A Claude Code plugin that adds structured workflow commands for development. Seven commands. Ten specialized agents. Zero opinions about your stack.

---

## The Pitch

```bash
/do:it
```

That's it. That kicks off a structured workflow that finds the most important work and does it.

Want to be more specific?

```bash
/do:it fix the auth bug
/do:it add user preferences
/do:it refactor the database layer
```

Claude figures out the intent, pulls in the right skills, and executes. You get consistent, repeatable workflows instead of "it depends on how you phrased your prompt."

Think of it as mise en place for software engineering. Everything in its place, ready to use. No hunting around, no crossed wires, no "oops I refactored your entire codebase when you asked me to fix a typo."

---

## Installation

```bash
# Add the marketplace
claude plugin marketplace add loom99-public/loom99-claude-marketplace

# Install the plugin
claude plugin install do
```

Or from within Claude Code:
```bash
/plugin marketplace add loom99-public/loom99-claude-marketplace
/plugin install do
```

**Requirements:** Claude Code (latest), git

**Optional:** [Beads](https://github.com/loom99-public/beads) for issue tracking integration

---

## The Seven Commands

All commands follow: `/do:<command> [intent] [area]`. Both optional. Claude figures it out.

| Command | What it does |
|---------|--------------|
| `/do:it` | **Implement**: build, fix, refactor, debug, test, review |
| `/do:plan` | **Plan**: evaluate status, create plans, manage backlog |
| `/do:explore` | **Explore**: ask questions about codebase internals |
| `/do:research` | **Research**: learn from external sources, web search |
| `/do:chores` | **Chores**: maintenance, cleanup, housekeeping |
| `/do:docs` | **Docs**: README, API, architecture documentation |
| `/do:release` | **Release**: versioning, changelog (stub) |

---

## Quick Examples

### Planning First

```bash
/do:plan user authentication    # Evaluate state, create plan
/do:it                          # Execute the plan
```

### Specific Tasks

```bash
/do:it fix login validation
/do:it refactor the cache layer
/do:it add tests for payment processing
```

### Workflow Modes

```bash
/do:it tdd new API endpoint     # Tests first, then implement
/do:it iterate dashboard UI     # Build incrementally, validate visually
/do:it                          # Auto-select based on context
```

### Research & Exploration

```bash
/do:explore where is auth handled
/do:research JWT best practices 2024
```

### Maintenance

```bash
/do:chores                      # Quick cleanup
/do:chores thorough             # Deep cleanup
/do:chores deps                 # Update dependencies
```

---

## How It Works

Do More Now uses a three-tier architecture:

**Commands** (7) detect intent from natural language.

**Skills** (17) define workflows for specific tasks.

**Agents** (10) execute the actual work.

| Agent | What it does |
|-------|--------------|
| `project-evaluator` | Analyzes current state, finds gaps |
| `status-planner` | Creates prioritized backlog |
| `functional-tester` | Writes tests (TDD mode) |
| `test-driven-implementer` | Implements to pass tests |
| `iterative-implementer` | Implements incrementally |
| `work-evaluator` | Validates with runtime evidence |
| `product-visionary` | Designs new features |
| `project-architect` | Initializes new projects |
| `researcher` | Explores options and ambiguities |
| `execution-summarizer` | Logs execution traces |

You don't need to know any of this. But if something goes wrong, `.agent_planning/do-command-logs/` has the receipts.

---

## When to Use Which Mode

**TDD** (`/do:it tdd`): APIs, backend services, libraries, clear requirements

**Iterative** (`/do:it iterate`): UI work, exploratory features, visual validation

**Auto** (`/do:it`): Let Claude decide based on context. Usually correct.

---

## Decision Handling

Some commands ask how autonomous Claude should be:

| Mode | Behavior |
|------|----------|
| **BLOCKING** | Ask before every significant choice |
| **HYBRID** | Ask about major decisions, auto-approve obvious ones |
| **NONBLOCKING** | Full autonomy, document decisions for review |

Signal your preference: "carefully" → BLOCKING, "guided" → HYBRID, "autonomous" → NONBLOCKING

---

## Documentation

Full documentation in `plugins/do-more-now/`:
- `README.md` - User guide
- `CLAUDE.md` - Technical reference

---

## License

**PolyForm Internal Use License 1.0.0**

Free for individuals and organizations for internal purposes. Don't redistribute or repackage without permission.

Questions? Reach out.

---

**Version**: 0.5.0 | **Author**: Brandon Fryslie
