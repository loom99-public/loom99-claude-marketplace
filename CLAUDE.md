# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code Plugin Marketplace repository owned by Brandon Fryslie. It contains a collection of custom plugins designed to extend Claude Code functionality with specialized agents, commands, hooks, and skills.

**Current State**: Production-ready. The marketplace contains approximately 21,000 lines of plugin implementation code across 6 plugins. All core components are implemented and validated.

**Plugin Count**: 6 plugins (agent-loop, epti, visual-iteration, promptctl, do-more-now, claude4claude)

## Repository Structure

```
loom99-claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest defining available plugins
├── plugins/
│   ├── agent-loop/               # Agentic Software Engineering Loop (1,848 lines)
│   ├── epti/                     # Evaluate-Plan-Test-Implement TDD (3,211 lines)
│   ├── visual-iteration/         # Visual iteration with screenshots (3,273 lines)
│   ├── promptctl/                # Hook-based workflow automation (3,734 lines)
│   ├── do-more-now/              # Evaluate, plan, and implement workflow (4,922 lines)
│   └── claude4claude/            # Claude artifact creation skills (4,284 lines)
```

## Architecture

### Marketplace Structure

The marketplace is defined in `.claude-plugin/marketplace.json` and follows this pattern:
- Each plugin is self-contained in `plugins/<plugin-name>/`
- Plugins define metadata, author info, licensing, and version
- The `strict` mode is enabled for all plugins, enforcing validation

### Plugin Structure

Each plugin follows the standard Claude Code plugin architecture:
- **agents/**: Custom agent definitions with specialized behaviors
- **commands/**: Slash commands (e.g., `/custom-command`) that expand to prompts
- **hooks/**: Lifecycle hooks that execute shell commands in response to events
- **skills/**: Reusable skill definitions
- **.mcp.json**: MCP (Model Context Protocol) server configurations
- **.claude-plugin/plugin.json**: Plugin manifest with metadata and paths

## Plugins

### 1. agent-loop (v0.1.0)

**Purpose**: Agentic Software Engineering Loop implementing a structured 4-stage workflow: Explore, Plan, Code, Commit

**Components**:
- 1 agent (workflow-agent.md)
- 4 commands: `/explore`, `/plan`, `/code`, `/commit`
- 4 skills: code-exploration, plan-generation, verification, git-operations

**Total Lines**: 1,848

### 2. epti (v0.1.0)

**Purpose**: Evaluate-Plan-Test-Implement workflow enforcing test-first TDD discipline

**Components**:
- 1 agent (tdd-agent.md)
- 6 commands: `/write-tests`, `/verify-fail`, `/commit-tests`, `/implement`, `/iterate`, `/commit-code`
- 5 skills: test-generation, test-execution, implementation-with-protection, overfitting-detection, refactoring

**Total Lines**: 3,211

**Framework Support**: pytest (Python), jest (JavaScript), go test (Go), JUnit (Java), RSpec (Ruby)

### 3. visual-iteration (v0.1.0)

**Purpose**: Visual iteration workflow enabling pixel-perfect UI implementation through screenshot feedback

**Components**:
- 1 agent (visual-iteration-agent.md)
- 6 commands: `/screenshot`, `/feedback`, `/refine`, `/iterate-loop`, `/commit-visual`, `/compare`
- 4 skills: screenshot-capture, visual-analysis, refinement-guidance, iteration-management
- MCP Integration: browser-tools for automated screenshot capture

**Total Lines**: 3,273

### 4. promptctl (v0.1.0)

**Purpose**: Hook-based workflow automation for Claude Code with event-driven automation

**Architecture**: Hooks-only (no agents or commands)
- Persistent MCP server handles hook events and configuration
- YAML-based handler configuration
- LogFlow logging system

**Components**:
- MCP Server (server.py)
- Dispatch Script (bin/dispatch.py)
- LogFlow logging (logflow.py)
- CLI Tools (logs.py)

**Total Lines**: 3,734

### 5. do-more-now (v0.1.0)

**Purpose**: Comprehensive evaluate, plan, and implement workflow with TDD and iterative modes

**Components**:
- 9 agents: functional-tester, iterative-implementer, product-visionary, project-architect, project-evaluator, researcher, status-planner, test-driven-implementer, work-evaluator
- 5 commands: `/plan`, `/feature-proposal`, `/init-project`, `/learn`, `/it`

**Total Lines**: 4,922

**Key Features**:
- Project initialization with adaptive questioning
- TDD workflow (tests first, then implement)
- Iterative workflow (implement, then validate)
- Research-driven ambiguity resolution

### 6. claude4claude (v0.1.0)

**Purpose**: Skills for creating Claude Code artifacts (MCP servers, skills, plugins, agents, commands)

**Components**:
- 2 skills: mcp-builder, skill-creator

**Total Lines**: 4,284

## Project Statistics

### Implementation Metrics

| Plugin | Lines | Agents | Commands | Skills |
|--------|-------|--------|----------|--------|
| agent-loop | 1,848 | 1 | 4 | 4 |
| epti | 3,211 | 1 | 6 | 5 |
| visual-iteration | 3,273 | 1 | 6 | 4 |
| promptctl | 3,734 | 0 | 0 | 0 |
| do-more-now | 4,922 | 9 | 5 | 0 |
| claude4claude | 4,284 | 0 | 0 | 2 |
| **Total** | **21,272** | **12** | **21** | **15** |

### Configuration Quality

- All JSON files valid
- All plugin paths verified
- Metadata accurate

## Development Workflow

### Adding a New Plugin

1. Create plugin directory: `plugins/<plugin-name>/`
2. Set up standard plugin structure (agents/, commands/, hooks/, skills/)
3. Create `.claude-plugin/plugin.json` with plugin metadata
4. Add plugin entry to `.claude-plugin/marketplace.json`
5. Configure MCP servers in `.mcp.json` if needed
6. Implement agents, commands, hooks, or skills as needed

### Plugin Component Development

- **Agents**: Define specialized behavior for specific tasks
- **Commands**: Markdown files that define slash commands
- **Hooks**: JSON configurations that trigger shell commands on events
- **Skills**: Reusable functionality that can be invoked

### Testing Plugins

Testing involves:
1. Loading the marketplace in Claude Code
2. Installing individual plugins from the marketplace
3. Testing agent behaviors, commands, hooks, and skills in context
4. Verifying MCP server integrations work correctly

## Licensing and Ownership

- This marketplace is intended for personal use by Brandon Fryslie
- All plugins use MIT license
- Plugin manifests contain proper author attribution

## File Paths

When referencing files in this repository from outside the working directory, use the symlink path:
- `~/icode/loom99-claude-marketplace/...`

This provides a shorter, stable path compared to the iCloud Documents path.
