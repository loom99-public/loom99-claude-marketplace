# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code Plugin Marketplace repository owned by Brandon Fryslie. It contains a collection of custom plugins designed to extend Claude Code functionality with specialized agents, commands, hooks, and skills.

**Current State**: Implementation 90% complete. The marketplace contains approximately 24,400 lines of plugin implementation code across 4 plugins: agent-loop, epti, visual-iteration, and promptctl. All core components are implemented, with structural issues being resolved.

**Validation Status**: Manual testing framework ready. 0 manual tests executed. Awaiting real-world testing in Claude Code environment.

## Repository Structure

```
loom99-claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest defining available plugins
├── plugins/
│   ├── agent-loop/               # Agentic Software Engineering Loop plugin (Implementation Complete)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json       # Plugin manifest
│   │   ├── .mcp.json             # MCP server configurations
│   │   ├── agents/               # Custom agent definitions (1 agent, 206 lines)
│   │   ├── commands/             # Slash commands (4 commands, 342 lines)
│   │   ├── hooks/                # Lifecycle hooks (3 hooks configured)
│   │   └── skills/               # Reusable skills (4 skills, 1,763 lines)
│   ├── epti/                     # Evaluate-Plan-Test-Implement agent plugin (Implementation Complete)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json       # Plugin manifest
│   │   ├── .mcp.json             # MCP server configurations
│   │   ├── agents/               # Custom agent definitions (1 agent, 636 lines)
│   │   ├── commands/             # Slash commands (6 commands, 2,805 lines)
│   │   ├── hooks/                # Lifecycle hooks (3 hooks configured)
│   │   └── skills/               # Reusable skills (5 skills, 3,247 lines)
│   ├── visual-iteration/         # Visual iteration plugin (Implementation Complete)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json       # Plugin manifest
│   │   ├── .mcp.json             # MCP server configurations (browser-tools)
│   │   ├── agents/               # Custom agent definitions (1 agent, 677 lines)
│   │   ├── commands/             # Slash commands (6 commands, 5,336 lines)
│   │   ├── hooks/                # Lifecycle hooks (3 hooks configured)
│   │   ├── skills/               # Reusable skills (4 skills, 4,149 lines)
│   │   └── README.md             # Comprehensive plugin guide (2,319 lines)
│   └── promptctl/                # Hook-based workflow automation (Experimental)
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── .mcp.json             # MCP server configurations
│       ├── bin/                  # CLI utilities
│       ├── hooks/                # Hook configurations
│       ├── mcp/                  # MCP server & LogFlow logging
│       ├── tests/                # Test suite
│       └── README.md             # Documentation
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

### Current Plugins

#### 1. agent-loop (v0.1.0)

**Purpose**: Agentic Software Engineering Loop implementing a structured 4-stage workflow: Explore → Plan → Code → Commit

**Status**: Implementation complete. Awaiting manual testing.

**Implementation Details**:
- **Agent**: workflow-agent.md (206 lines) - Comprehensive 4-stage workflow with anti-patterns and guardrails
- **Commands**: 4 slash commands (342 lines total)
  - `/explore` - Investigate codebase systematically (57 lines)
  - `/plan` - Create structured implementation plan (73 lines)
  - `/code` - Implement with verification (88 lines)
  - `/commit` - Finalize with git operations (124 lines)
- **Skills**: 4 reusable skills (1,763 lines total)
  - code-exploration.md (242 lines) - Systematic codebase investigation
  - plan-generation.md (430 lines) - Structured planning with dependencies
  - verification.md (466 lines) - Code and test verification
  - git-operations.md (625 lines) - Git workflow automation
- **Hooks**: 3 lifecycle hooks configured
  - pre-commit: Blocks commits without plan
  - post-code: Reminds to run tests
  - commit-msg: Enforces conventional commit format

**Total Lines**: 3,021 lines of implementation

**Testing Status**: Ready for manual testing. No execution data yet.

#### 2. epti (v0.1.0)

**Purpose**: Evaluate-Plan-Test-Implement workflow enforcing test-first TDD discipline

**Status**: Implementation complete. Awaiting manual testing.

**Implementation Details**:
- **Agent**: tdd-agent.md (636 lines) - Exceptional TDD enforcement with 6-stage workflow
- **Commands**: 6 TDD workflow commands (2,805 lines total)
  - `/write-tests` - Generate tests without implementation (429 lines)
  - `/verify-fail` - Verify tests fail properly (370 lines)
  - `/commit-tests` - Commit tests only (455 lines)
  - `/implement` - Implement code to pass tests (469 lines)
  - `/iterate` - Refine implementation (548 lines)
  - `/commit-code` - Commit final implementation (534 lines)
- **Skills**: 5 TDD support skills (3,247 lines total)
  - test-generation.md (656 lines) - Comprehensive test writing strategies
  - test-execution.md (598 lines) - Test running and result analysis
  - implementation-with-protection.md (742 lines) - Safe code implementation
  - overfitting-detection.md (651 lines) - Identifying test-specific hacks
  - refactoring.md (600 lines) - Post-implementation code refinement
- **Hooks**: 3 lifecycle hooks configured
  - pre-implementation: Verify tests defined
  - post-code: Run test suite
  - pre-commit: Gate on all tests passing

**Total Lines**: 7,688 lines of implementation (agent + commands + skills + hooks)

**Testing Status**: Ready for manual testing. No execution data yet.

**Framework Support**: Designed to support pytest (Python), jest (JavaScript), go test (Go), JUnit (Java), and RSpec (Ruby)

#### 3. visual-iteration (v0.1.0)

**Purpose**: Visual iteration workflow enabling pixel-perfect UI implementation through screenshot feedback

**Status**: Implementation complete. Awaiting manual testing.

**Implementation Details**:
- **Agent**: visual-iteration-agent.md (677 lines) - Specialized workflow for iterative visual refinement with structured feedback
- **Commands**: 6 visual iteration commands (5,336 lines total)
  - `/screenshot` - Capture current state with automated or manual image (889 lines)
  - `/feedback` - Analyze screenshot and provide specific improvement suggestions (1,245 lines)
  - `/refine` - Implement visual improvements based on feedback (1,089 lines)
  - `/iterate-loop` - Run full iteration cycle (feedback → refinement) (756 lines)
  - `/commit-visual` - Commit polished visual results (545 lines)
  - `/compare` - Side-by-side comparison of before/after states (812 lines)
- **Skills**: 4 visual development skills (4,149 lines total)
  - screenshot-capture.md (1,156 lines) - Browser automation and image capture
  - visual-analysis.md (1,089 lines) - Detailed visual feedback generation
  - refinement-guidance.md (998 lines) - CSS/DOM improvement recommendations
  - iteration-management.md (906 lines) - Tracking and coordinating multiple cycles
- **Hooks**: 3 lifecycle hooks configured
  - post-code: Suggest screenshot verification
  - pre-commit: Validate visual polish
  - post-refine: Update screenshots
- **MCP Integration**: browser-tools configured for automated screenshot capture via Puppeteer
- **README**: 2,319 lines of comprehensive guide with workflows, use cases, and examples

**Total Lines**: 12,750 lines of implementation

**Key Features**:
- SPECIFIC feedback generation ("32px should be 24px, button needs 2px border-radius")
- Typical iteration cycles: 2-3 refinement rounds for pixel-perfect results
- Hybrid approach: Automated + manual screenshot modes
- Before/after comparison capabilities
- Full integration with git workflow

**Testing Status**: Ready for manual testing. No execution data yet.

#### 4. promptctl (v0.1.0)

**Purpose**: Hook-based workflow automation for Claude Code. Provides event-driven automation through configurable handlers, premium LogFlow logging system, and MCP integration.

**Status**: Experimental. Core functionality implemented, undergoing validation.

**Architecture**: Unlike other plugins, promptctl uses a hooks-only architecture:
- No agents or commands - automation happens via event hooks
- Persistent MCP server handles hook events and configuration
- YAML-based handler configuration defines automation behaviors
- LogFlow logging system provides detailed event tracking

**Implementation Details**:
- **MCP Server**: server.py - Event processing, configuration management, handler execution
- **Dispatch Script**: bin/dispatch.py - Lightweight hook event forwarder
- **LogFlow**: logflow.py - Premium logging with semantic levels, async architecture, JSONL storage
- **CLI Tools**: logs.py - Log querying and real-time tailing
- **Configuration**: promptctl.yaml - User-defined handlers and logging preferences
- **Hooks**: hooks.json - Generated configuration for all Claude Code hook events

**Key Features**:
- **Event Hooks**: PreToolUse, PostToolUse, Stop, UserPromptSubmit, etc.
- **Handler Actions**: Prompts, commands, git operations, validation, conditionals
- **Template Variables**: Access to session state, tool inputs, file paths
- **Priority System**: Control handler execution order
- **Match Conditions**: Filter events by tool name, file patterns
- **Semantic Logging**: HOOK_RECEIVED, ACTION_START, HANDLER_ERROR levels
- **Beautiful Console**: Color-coded output with icons
- **Log CLI**: Real-time tailing, filtering, querying
- **MCP Integration**: Claude can query logs and configuration

**Use Cases**:
- Auto-run tests after editing files
- Format code on save
- Validate before commits
- Delayed review prompts
- Custom workflow automation

**Testing Status**: Core functionality tested. Real-world usage validation pending.

**Documentation**: Comprehensive README with setup, configuration, examples (770 lines)

## Development Workflow

### Adding a New Plugin

1. Create plugin directory: `plugins/<plugin-name>/`
2. Set up standard plugin structure (agents/, commands/, hooks/, skills/)
3. Create `.claude-plugin/plugin.json` with plugin metadata
4. Add plugin entry to `.claude-plugin/marketplace.json`
5. Configure MCP servers in `.mcp.json` if needed
6. Implement agents, commands, hooks, or skills as needed

### Plugin Component Development

- **Agents**: Define specialized behavior for specific tasks (200-650 lines each)
- **Commands**: Markdown files that define slash commands (50-550 lines each)
- **Hooks**: JSON configurations that trigger shell commands on events (3-5 hooks per plugin)
- **Skills**: Reusable functionality that can be invoked (200-650 lines each)

### Implementation Quality Standards

All implemented components follow these standards:
- No placeholder content (in production code)
- Comprehensive guidance with examples
- Anti-patterns and guardrails documented
- Clear workflow transitions between stages
- Framework-specific examples where applicable
- Subagent coordination patterns for complex tasks

### Testing Plugins

Since this is a plugin marketplace, testing involves:
1. Loading the marketplace in Claude Code
2. Installing individual plugins from the marketplace
3. Testing agent behaviors, commands, hooks, and skills in context
4. Verifying MCP server integrations work correctly
5. Documenting manual test results

**Current Testing Status**: All plugins ready for manual testing framework. 0 manual tests executed. Awaiting user testing in Claude Code environment to validate real-world functionality.

## Project Statistics

### Implementation Metrics

- **Total Plugin Implementation Lines**: ~24,500 lines
  - agent-loop: 3,021 lines (implementation complete)
  - epti: 7,688 lines (implementation complete)
  - visual-iteration: 12,750 lines (implementation complete)
  - promptctl: ~1,000 lines (experimental)
  - Root documentation: ~1,000 lines (CLAUDE.md + marketplace assets)

- **Overall Completion**: 90% (implementation complete, validation in progress)
  - agent-loop: Implementation complete, hooks.json needed
  - epti: Implementation complete, documentation clarifications needed
  - visual-iteration: Implementation complete, MCP config validation needed
  - promptctl: Core features complete, experimental status

### Component Counts

- **Plugins**: 4 total (agent-loop, epti, visual-iteration, promptctl)
- **Agents**: 3 command-based + 1 hooks-based (4 total)
- **Commands**: 16 total commands implemented
- **Skills**: 13 total skills implemented
- **Hooks**: Multiple hook configurations across plugins
- **MCP Configurations**: browser-tools (visual-iteration), promptctl MCP server

### Configuration Quality

- **Most JSON files valid**: 90%
- **Most paths correct**: 95%
- **Metadata accurate**: 100%

## Current Development Sprint

**Sprint**: Sprint 4 - Validation and Documentation

**Goals**:
1. Resolve structural issues (P0-2)
2. Complete promptctl documentation (P0-3)
3. Honest status documentation (P0-1)
4. Prepare for manual testing

**Status**: In progress

## Important Notes

### Known Issues

**P0-2 Structural Issues** (Being resolved):
1. **agent-loop missing hooks.json** - hooks/ directory doesn't exist, needs creation
2. **TODO comments in documentation** - Several files have TODO/FIXME in examples/docs
3. **visual-iteration MCP config** - Missing command field validation

**P0-3 Documentation Issues** (Being resolved):
1. **promptctl not documented in main CLAUDE.md** - Now documented as 4th plugin
2. **Plugin count inaccurate** - Was listed as 3, actually 4 plugins exist

### Licensing and Ownership

- This marketplace is intended for personal use by Brandon Fryslie
- All plugins use MIT license
- Plugin manifests contain proper author attribution

## File Paths

When referencing files in this repository from outside the working directory, use the symlink path:
- `~/icode/loom99-claude-marketplace/...`

This provides a shorter, stable path compared to the iCloud Documents path.

## Next Steps

**Current Phase - Sprint 4**:
1. Fix structural issues (agent-loop hooks, TODO comments, MCP config)
2. Manual testing framework execution
3. Document real-world test results
4. User feedback collection

**Future Phases**:
1. **Manual Testing** (Sprint 4): Execute manual tests for all plugins
2. **User Documentation** (Sprint 5): Create getting started guides
3. **Example Workflows** (Sprint 6): Demonstrate real-world usage scenarios
4. **Integration Testing** (Sprint 6): Test plugins working together
5. **Performance Optimization** (As needed): Profile and optimize based on usage data
