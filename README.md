---

![do-more-now](https://raw.githubusercontent.com/loom99-public/loom99-claude-marketplace/refs/heads/master/assets/do-more-now-2.svg)

Do More Now is a Claude Code plugin that adds structured workflow commands for development.  This is not designed for one particular language or way of working.  It's a
simple, flexible, and incredibly powerful toolkit for all type of software engineering.

### What makes it great?

#### Minimal

Just 7 powerful commands and minimal intrusion on your context.  Do More Now makes heavy use of Claude Skills to abstract common functionality and only brings it in when needed

We do not include any MCP servers, but we do recommend installing the Beads MCP server to improve structured planning.  Works great without it too.

#### So easy

Here's how to use the plugin in it's most basic form:

```bash
/do:it
```

That's all you need.  That will kick off a structured workflow that will find the most important work and work on it.

You can pass a specific topic:

```bash
/do:it Fix that bug!
```

Internally, the plugins name is 'do'.  This allows us to type `/do:<command>`, which is easy and memorable.  

In docs and online, the plugin is named Do More Now.  Because it's the quickest way to make that happen. 

Note: This document is under heavy revision and is not currently fully up to date.  Better docs coming soon.  

Here's a quick overview of the commands:

```bash
# All commands follow this pattern:
/do:<command> [Intent signal] [Area of focus]

# type this into claude. /do:it is used for implementing
/do:it [Area of focus]

# used for planning
/do:plan [init|audit|status|feature|track] [Area of focus]

# Exploring the codebase (internal learning)
/do:explore [Area of focus]

# External learning (googling stuff, comparing projects, finding answers online, etc
/do:research [market|docs|patterns] [Area of focus]

# Write docs
/do:docs [readme|api|architecture|changelog] [Area of focus]

# Maintenance and housekeeping. Tidying up of any sort.
/do:chores [quick|thorough|git|planning|dead-code|deps|debt] [Area of focus]

```

Both `[Intent signal]` and `[Area of focus]` are optional.  Claude will figure it out.

`[Intent signal]` does not need to match exactly.  Claude will use those keywords to pull in the right skills and route you to the right agent.

`[Area of focus]` Can be anything you want, from 1 word to 5 paragraphs of prompt.  Take whatever you'd normally send to Claude and enter it here.  It will get you further and the results will be better.

You can even enter more slash commands in your prompt and claude will execute all of them, allowing you to easily chain workflows.  Claude will rewrite the input to each command intelligently.

---

## Quickstart

```bash
# Install the marketplace
claude plugin marketplace add loom99-public/loom99-claude-marketplace

# On the cli
claude plugin install do

# Or in Claude Code:
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

## License

This software is licensed under: **PolyForm Internal Use License 1.0.0** 

This Claude Code plugin is free to use by individuals and organizations for internal purposes.
You’re welcome to load it into Claude, use it in your workflows, and adapt it for your own internal needs.

Please don’t redistribute, repackage, or publish derivative versions without permission.
If you’d like to do that, reach out and let's chat. I'm open to licensing or possibly even contributing directly to
your excellent organization.