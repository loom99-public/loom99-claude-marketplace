# do-more-now

A Claude Code plugin that adds structured workflow commands for development. Two main approaches: write tests first (TDD), or implement and validate as you go.

---

## Quickstart

```bash
# Install the marketplace
git clone https://github.com/loom99/loom99-claude-marketplace.git
cd loom99-claude-marketplace

# In Claude Code:
/plugin marketplace add .
/plugin install do
```

### Build something with TDD

```bash
# Start with evaluation to understand current state
/do:plan user authentication

# Implement (auto-selects TDD or iterative)
/do:it

# Or force TDD mode:
/do:it tdd
```

### Build something without tests upfront

```bash
# Evaluate and plan first
/do:plan dashboard navigation

# Build incrementally with runtime validation
/do:it iterate
```

---

## Commands

- **`/do:plan`** - Analyzes current state, creates prioritized work plan
- **`/do:it`** - Implement (auto-selects TDD or iterative, or pass 'tdd'/'iterate')
- **`/do:learn`** - Research a question or problem
- **`/do:init-project`** - Initialize a new project with guided interview
- **`/do:feature-proposal`** - Generates design proposals for new features

All workflows use `.agent_planning/` directory for status and planning documents.

---

## Agents

| Agent | What it does |
|-------|--------------|
| `project-evaluator` | Analyzes current state, finds gaps |
| `status-planner` | Creates work backlog from gaps |
| `functional-tester` | Writes tests (TDD workflow) |
| `test-driven-implementer` | Implements to pass tests (TDD) |
| `iterative-implementer` | Implements incrementally (non-TDD) |
| `work-evaluator` | Validates with runtime evidence (non-TDD) |
| `product-visionary` | Designs new features |
| `project-architect` | Initializes new projects |
| `researcher` | Explores ambiguities and options |

---

## When to use which mode

**Use TDD (`/do:it tdd`):**
- APIs, backend services
- Libraries, frameworks
- When requirements are clear

**Use Iterative (`/do:it iterate`):**
- UI/frontend work
- Exploratory features
- When visual validation matters

**Auto mode (`/do:it`):**
- Let Claude decide based on context

---

## Requirements

- Claude Code (latest)
- git (for commit functionality)

---

## Documentation

- `plugins/do-more-now/CLAUDE.md` - Detailed plugin guide

---

MIT License
