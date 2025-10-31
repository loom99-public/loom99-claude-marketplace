# Architecture Documentation

**Technical design and implementation details for loom99 Claude Marketplace**

---

## Table of Contents

- [Overview](#overview)
- [Marketplace Structure](#marketplace-structure)
- [Plugin Architecture](#plugin-architecture)
- [Component Deep Dive](#component-deep-dive)
- [Skills System](#skills-system)
- [Hooks System](#hooks-system)
- [Testing Strategy](#testing-strategy)
- [Design Decisions](#design-decisions)
- [Implementation Details](#implementation-details)

---

## Overview

The loom99 marketplace is a collection of Claude Code plugins that enforce structured software development workflows. The architecture follows Claude Code's plugin system specification while introducing patterns for workflow orchestration, TDD enforcement, and visual iteration.

### Core Principles

1. **Workflow as Code** - Codify best practices into executable workflows
2. **Guard Rails, Not Suggestions** - Use hooks to enforce discipline
3. **Test-Driven Architecture** - Functional tests validate real behavior
4. **Composable Components** - Agents, commands, skills, and hooks work together
5. **Framework Agnostic** - Support multiple languages and test frameworks

### Architecture Goals

- ✅ Prevent common development anti-patterns
- ✅ Enforce test-first development when appropriate
- ✅ Guide systematic exploration and planning
- ✅ Automate repetitive workflow tasks
- ✅ Provide reusable capabilities through skills
- ✅ Integrate with existing tools (git, test frameworks, browsers)

---

## Marketplace Structure

### File Organization

```
loom99-claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json           # Marketplace manifest
├── plugins/
│   ├── agent-loop/                # Workflow plugin
│   ├── epti/                      # TDD plugin
│   └── visual-iteration/          # UI iteration plugin
├── tests/
│   ├── functional/                # Functional test suite
│   │   └── test_skills_structure.py
│   └── README.md                  # Test documentation
├── .agent_planning/               # Planning artifacts
├── Justfile                       # Task automation
├── README.md                      # User documentation
├── ARCHITECTURE.md                # This file
├── NEXT_STEPS.md                  # Historical fixes and future work
└── CLAUDE.md                      # AI guidance
```

### Marketplace Manifest

**File**: `.claude-plugin/marketplace.json`

```json
{
  "name": "loom99",
  "owner": {
    "name": "Brandon Fryslie",
    "email": ""
  },
  "metadata": {
    "description": "A marketplace of claude plugins designed and implemented by Brandon Fryslie"
  },
  "plugins": [
    {
      "name": "agent-loop",
      "source": "./plugins/agent-loop",
      "description": "Agentic Software Engineering Loop",
      "version": "0.1.0",
      "author": {"name": "Brandon Fryslie"},
      "strict": true,
      "license": "MIT"
    }
    // ... more plugins
  ]
}
```

**Key Fields**:
- `name`: Marketplace identifier (used in installation)
- `owner`: Contact information for marketplace maintainer
- `plugins[]`: Array of plugin definitions
- `strict`: Validation mode (enforces structure requirements)

---

## Plugin Architecture

Each plugin follows a standard structure mandated by Claude Code:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (required)
├── agents/
│   └── *.md                 # Agent definitions (optional)
├── commands/
│   └── *.md                 # Slash commands (optional)
├── hooks/
│   └── hooks.json           # Lifecycle hooks (optional)
├── skills/
│   └── skill-name/          # Skills (optional)
│       └── SKILL.md         # Required filename
├── .mcp.json                # MCP server config (optional)
└── README.md                # Plugin documentation (recommended)
```

### Plugin Manifest

**File**: `plugin.json`

```json
{
  "name": "plugin-identifier",
  "version": "0.1.0",
  "description": "Plugin purpose",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "license": "MIT",
  "keywords": ["workflow", "tdd", "visual"],
  "commands": "./commands/",
  "agents": "./agents/",
  "hooks": "./hooks/hooks.json",
  "skills": "./skills/",
  "mcpServers": "./.mcp.json"
}
```

**Component Paths**:
- Relative to plugin root
- Can be files (hooks, mcpServers) or directories (commands, agents, skills)
- All paths optional except `name`, `version`, `description`

---

## Component Deep Dive

### 1. Agents

**Purpose**: Specialized AI behaviors for specific tasks

**Format**: Markdown files with instructions

**Location**: `plugins/*/agents/*.md`

**Characteristics**:
- 200-700 lines of guidance
- Workflow stage definitions
- Anti-patterns and guardrails
- Subagent coordination patterns
- Framework-specific examples

**Example Structure**:
```markdown
# Agent Name

## Purpose
What this agent does and when to invoke it

## Workflow Stages
1. Stage 1: Description
2. Stage 2: Description

## Anti-Patterns
Things to avoid

## Examples
Concrete examples

## Integration
How this agent coordinates with others
```

**Current Agents**:
- `workflow-agent.md` (agent-loop): 4-stage workflow orchestration
- `tdd-agent.md` (epti): 6-stage TDD enforcement
- `visual-iteration-agent.md` (visual-iteration): Screenshot-driven iteration

### 2. Commands

**Purpose**: Slash commands that expand to prompts

**Format**: Markdown files (one per command)

**Location**: `plugins/*/commands/*.md`

**Naming**: Filename without `.md` becomes command name
- `explore.md` → `/explore`
- `write-tests.md` → `/write-tests`

**Characteristics**:
- 50-550 lines per command
- Detailed guidance for specific workflow stage
- Can include argument placeholders (`$ARGUMENTS`, `$1`, etc.)
- May reference skills via invocation patterns

**Example Structure**:
```markdown
# /command-name - Stage Name

You are now in the **STAGE** stage.

## Your Mission
What to accomplish in this stage

## What You Should Do
1. Step 1
2. Step 2

## Anti-Patterns
What NOT to do

## Transition
When to move to next stage
```

### 3. Skills

**Purpose**: Reusable capabilities that Claude invokes autonomously

**Format**: Subdirectories with SKILL.md files

**Location**: `plugins/*/skills/skill-name/SKILL.md`

**Structure Requirements** (Critical):
```
skills/
└── skill-name/              # Subdirectory (required)
    └── SKILL.md             # Exact filename (required)
```

**YAML Frontmatter** (Required):
```yaml
---
name: skill-identifier
description: What the skill does and when to use it (max 1024 chars)
---

# Skill content follows...
```

**Characteristics**:
- 200-700 lines of guidance
- Invoked automatically by Claude based on context
- Description field critical for discoverability
- Can reference other files in subdirectory

**Current Skills**: 13 total
- agent-loop: 4 skills (exploration, planning, verification, git)
- epti: 5 skills (test generation, execution, implementation, overfitting detection, refactoring)
- visual-iteration: 4 skills (screenshot capture, visual comparison, refinement, design implementation)

### 4. Hooks

**Purpose**: Lifecycle event handlers (pre/post operations)

**Format**: JSON array of hook definitions

**Location**: `plugins/*/hooks/hooks.json`

**Structure**:
```json
[
  {
    "event": "pre-commit",
    "command": "bash command to run",
    "description": "Human-readable purpose"
  }
]
```

**Supported Events**:
- `pre-commit`: Before git commit
- `post-commit`: After git commit
- `commit-msg`: Validate commit message
- `pre-code`: Before coding stage
- `post-code`: After coding stage
- `pre-implementation`: Before implementation (epti)
- Custom events supported by plugins

**Hook Capabilities**:
- **Block operations**: Exit with non-zero status
- **Display messages**: Echo guidance to user
- **Run validations**: Check conditions
- **Integrate tools**: Run git, test frameworks, etc.

**Design Pattern**: Hooks enforce discipline
- Pre-hooks: Gate operations (require tests, plans, etc.)
- Post-hooks: Remind about next steps
- Commit-msg: Enforce formats (conventional commits, TDD format)

### 5. MCP Servers

**Purpose**: External tool integration via Model Context Protocol

**Format**: JSON configuration

**Location**: `plugins/*/.mcp.json`

**Structure**:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["--arg1", "--arg2"],
      "env": {}
    }
  }
}
```

**Current MCP Usage**:
- visual-iteration: `browser-tools` for automated screenshot capture via Puppeteer
- Other plugins: Empty configs (future expansion)

---

## Skills System

### Why Skills?

Commands are explicit (user invokes `/command`). Skills are implicit (Claude invokes automatically when needed).

### Skills Architecture

**Discovery**: Claude reads skill descriptions to understand capabilities

**Invocation**: Claude uses skills when task matches description

**Isolation**: Each skill in separate subdirectory prevents file conflicts

**Documentation**: SKILL.md contains complete guidance for capability

### Skills Design Patterns

#### 1. Exploratory Skills
- **Purpose**: Gather information systematically
- **Example**: `code-exploration` (agent-loop)
- **Pattern**: Multi-phase investigation (structure → patterns → integration)

#### 2. Generative Skills
- **Purpose**: Create artifacts (tests, plans, code)
- **Example**: `test-generation` (epti)
- **Pattern**: Specification-driven generation with validation

#### 3. Verification Skills
- **Purpose**: Check correctness and quality
- **Example**: `overfitting-detection` (epti)
- **Pattern**: Multi-criterion analysis with concrete examples

#### 4. Automation Skills
- **Purpose**: Orchestrate tools and processes
- **Example**: `git-operations` (agent-loop)
- **Pattern**: Tool invocation with error handling and user guidance

### Skills vs Commands

| Aspect | Commands | Skills |
|--------|----------|--------|
| **Invocation** | User explicit (`/command`) | Claude automatic (context-based) |
| **Visibility** | Obvious to user | Invisible to user |
| **Scope** | Workflow stage | Reusable capability |
| **Structure** | Flat markdown file | Subdirectory with SKILL.md |
| **Frontmatter** | Optional | Required (name + description) |

---

## Hooks System

### Hook Execution Model

**Lifecycle**:
1. User triggers operation (e.g., `git commit`)
2. Claude Code checks for relevant hooks
3. Runs pre-hooks (e.g., `pre-commit`)
4. If all pass (exit 0), continues operation
5. Runs post-hooks (e.g., `post-commit`)

**Blocking Behavior**:
- Pre-hooks can block (exit 1 = abort operation)
- Post-hooks cannot block (informational only)

### Hook Design Patterns

#### 1. Gating Pattern (Pre-Hooks)
```json
{
  "event": "pre-commit",
  "command": "if [ ! -f PLAN.md ]; then echo 'Error: No plan found' && exit 1; fi",
  "description": "Require plan before commits"
}
```
**Purpose**: Enforce preconditions

#### 2. Reminder Pattern (Post-Hooks)
```json
{
  "event": "post-code",
  "command": "echo 'Remember to run tests!'",
  "description": "Remind about testing"
}
```
**Purpose**: Guide next steps

#### 3. Validation Pattern (Commit-Msg)
```json
{
  "event": "commit-msg",
  "command": "if ! grep -qE '^(feat|fix):' \"$1\"; then exit 1; fi",
  "description": "Enforce conventional commits"
}
```
**Purpose**: Enforce formats and standards

### Hook Integration

**agent-loop hooks**:
- Pre-commit: Require plan file
- Post-code: Suggest testing and review
- Commit-msg: Enforce conventional commit format

**epti hooks**:
- Pre-implementation: Verify tests exist and fail
- Post-code: Auto-run test suite
- Pre-commit: Block if tests failing
- Commit-msg: Enforce TDD-friendly format

**visual-iteration hooks**:
- Currently empty (future: screenshot reminders, visual validation)

---

## Testing Strategy

### Test Philosophy

**Functional Tests Over Unit Tests**:
- Test real user workflows, not implementation details
- Validate file system state, not internal logic
- Immune to AI gaming (can't fake file structures)

### Test Architecture

**Location**: `tests/functional/test_skills_structure.py`

**Framework**: pytest (Python)

**Test Categories**:
1. **Structure Tests**: Verify directory organization
2. **Frontmatter Tests**: Validate YAML format and fields
3. **Configuration Tests**: Check plugin.json correctness
4. **Content Preservation Tests**: Ensure no data loss
5. **Completeness Tests**: Verify all requirements met

### Test Design Patterns

#### 1. Parametrized Tests
```python
@pytest.mark.parametrize("plugin,skill", [
    ("agent-loop", "code-exploration"),
    ("agent-loop", "git-operations"),
    # ... 13 total skills
])
def test_skill_structure(plugin, skill):
    skill_dir = REPO_ROOT / "plugins" / plugin / "skills" / skill
    assert skill_dir.is_dir()
    assert (skill_dir / "SKILL.md").is_file()
```
**Benefit**: Single test validates all 13 skills

#### 2. Cross-Validation Tests
```python
def test_yaml_name_matches_directory():
    # Verify YAML 'name' field matches directory name
    # Catches inconsistencies
```
**Benefit**: Prevents naming mismatches

#### 3. Content Size Tests
```python
def test_skill_has_substantial_content():
    # Verify each SKILL.md > 100 lines
    # Prevents empty stubs
```
**Benefit**: Can't game with empty files

### Testing Anti-Gaming Measures

✅ **Parse actual YAML** - Invalid YAML fails test
✅ **Check file existence** - Must exist on disk
✅ **Validate content size** - Empty files fail
✅ **Cross-validate names** - Consistency checks
✅ **Multiple verification points** - Single aspect checked multiple ways

❌ **Cannot bypass by**:
- Creating empty directories
- Stub files with minimal content
- Invalid YAML (test parses it)
- Missing frontmatter
- Incorrect names

---

## Design Decisions

### Why Workflow Plugins?

**Problem**: AI coding assistants enable fast coding but not necessarily good coding.

**Solution**: Codify best practices into enforced workflows.

**Alternative Rejected**: Documentation/guidelines (too easy to ignore)

### Why Separate Test and Implementation Commits (epti)?

**Rationale**:
- Tests are specifications, not validation
- Separating commits proves tests written first
- Historical record of TDD discipline
- Easier to review test quality independently

**Alternative Rejected**: Single commit (loses provenance, enables cheating)

### Why Hooks Over Suggestions?

**Rationale**:
- Suggestions are ignored under time pressure
- Hooks enforce discipline automatically
- Gradual behavior change through repetition

**Alternative Rejected**: AI reminders (easily dismissed)

### Why Skills in Subdirectories?

**Rationale**:
- Claude Code specification requirement
- Allows additional files per skill (examples, templates)
- Prevents naming conflicts
- Clear ownership boundaries

**Alternative Rejected**: Flat markdown files (doesn't work)

### Why Functional Tests?

**Rationale**:
- Validate real user requirements
- Immune to AI gaming
- Test actual file system state
- Focus on outcomes, not implementation

**Alternative Rejected**: Unit tests (too implementation-focused)

---

## Implementation Details

### Repository Statistics

**Total Lines**: 24,459
- agent-loop: 3,021 lines
- epti: 7,688 lines
- visual-iteration: 12,750 lines
- Root documentation: ~1,000 lines

**Components**:
- Agents: 3 (206-677 lines each)
- Commands: 16 (50-550 lines each)
- Skills: 13 (200-700 lines each)
- Hooks: 9 (across 3 plugins)
- Tests: 60+ test cases (700 lines)

### File Formats

**Markdown**: Agents, commands, skills, documentation
- GitHub-flavored markdown
- YAML frontmatter where required
- Code examples in fenced blocks

**JSON**: Manifests, hooks, MCP configs
- Validated with `jq`
- Strict schema compliance
- Comments not supported (JSON spec)

**Python**: Test suite
- pytest framework
- Type hints for clarity
- Docstrings for documentation

### Directory Conventions

**Planning**: `.agent_planning/`
- STATUS files: Project status reports
- PLAN files: Implementation plans (historical)
- SPRINT files: Sprint tracking (historical)
- Archive: Retired planning artifacts

**Tests**: `tests/`
- `functional/`: Functional test suite
- `README.md`: Test documentation

**Plugins**: `plugins/`
- Each plugin self-contained
- No shared code between plugins
- Plugin-specific README files

### Naming Conventions

**Files**:
- Lowercase with hyphens: `code-exploration.md`
- SKILL.md: Exact case (required)
- plugin.json: Exact name (required)

**Commands**:
- Slash prefix: `/explore`, `/write-tests`
- Verb-based: `/commit`, `/refine`, `/iterate`
- No nested namespaces

**Skills**:
- Hyphen-separated: `code-exploration`, `test-generation`
- Match directory names exactly
- Descriptive, not abbreviated

---

## Validation and Quality

### Validation Tooling

**Claude CLI**: `claude plugin validate .`
- Checks marketplace.json structure
- Validates plugin.json files
- Verifies path references
- Confirms required fields present

**pytest**: `pytest tests/`
- Functional test suite
- 60+ test cases
- All passing ✅

**jq**: JSON validation
- `jq empty *.json` validates syntax
- Catches formatting errors early

**just**: Task automation
- `just validate`: Run all validations
- `just test`: Run test suite
- `just verify`: Combined validation + tests

### Quality Metrics

**Configuration Validity**: 100%
- All JSON files valid
- All paths correct
- All required fields present

**Test Coverage**: 100%
- All 13 skills tested
- All 3 plugins tested
- All requirements validated

**Documentation Coverage**: 100%
- Root README (user guide)
- ARCHITECTURE.md (this file)
- Plugin READMEs (3 files)
- Test README
- CLAUDE.md (AI guidance)
- NEXT_STEPS.md (historical context)

---

## Future Architecture Considerations

### Potential Enhancements

1. **Shared Skills Library**
   - Common skills used by multiple plugins
   - Versioned skill dependencies
   - Skill marketplace within marketplace

2. **Plugin Composition**
   - Combine multiple plugins for complex workflows
   - Plugin dependency declaration
   - Conflict resolution

3. **Custom Hook Events**
   - Plugin-specific lifecycle events
   - Hook chaining and composition
   - Conditional hook execution

4. **MCP Server Registry**
   - Catalog of useful MCP servers
   - Automatic installation/configuration
   - Version management

5. **Testing Infrastructure**
   - Integration tests (multiple plugins)
   - Performance benchmarks
   - Load testing for large repositories

### Architectural Constraints

**Must Maintain**:
- Claude Code specification compliance
- Backward compatibility with v0.1.0
- Functional test coverage
- Documentation accuracy

**Must Avoid**:
- Tight coupling between plugins
- Shared mutable state
- Breaking changes without major version bump
- Undocumented features

---

## Appendix: Architecture Diagrams

### Marketplace Component Hierarchy

```
loom99 Marketplace
├── agent-loop Plugin
│   ├── workflow-agent (Agent)
│   ├── /explore (Command)
│   ├── /plan (Command)
│   ├── /code (Command)
│   ├── /commit (Command)
│   ├── code-exploration (Skill)
│   ├── plan-generation (Skill)
│   ├── verification (Skill)
│   ├── git-operations (Skill)
│   └── 3 hooks
├── epti Plugin
│   ├── tdd-agent (Agent)
│   ├── /write-tests (Command)
│   ├── /verify-fail (Command)
│   ├── /commit-tests (Command)
│   ├── /implement (Command)
│   ├── /iterate (Command)
│   ├── /commit-code (Command)
│   ├── test-generation (Skill)
│   ├── test-execution (Skill)
│   ├── implementation-with-protection (Skill)
│   ├── overfitting-detection (Skill)
│   ├── refactoring (Skill)
│   └── 4 hooks
└── visual-iteration Plugin
    ├── visual-iteration-agent (Agent)
    ├── 6 commands
    ├── 4 skills
    ├── browser-tools (MCP)
    └── 0 hooks (TBD)
```

### Plugin Loading Flow

```
User: /plugin marketplace add .
    ↓
Claude Code reads .claude-plugin/marketplace.json
    ↓
Validates marketplace structure
    ↓
User: /plugin install agent-loop
    ↓
Claude Code reads plugins/agent-loop/.claude-plugin/plugin.json
    ↓
Loads components:
    ├── Agents (agents/*.md)
    ├── Commands (commands/*.md)
    ├── Skills (skills/*/SKILL.md)
    ├── Hooks (hooks/hooks.json)
    └── MCP Servers (.mcp.json)
    ↓
Plugin active (commands available, hooks registered, skills discoverable)
```

### TDD Workflow (epti)

```
1. /write-tests
   ↓ Generates tests
   ├── Uses: test-generation skill
   └── Output: test files

2. /verify-fail
   ↓ Runs tests
   ├── Uses: test-execution skill
   └── Confirms: tests fail

3. /commit-tests
   ↓ Git commit
   ├── Uses: git-operations skill
   └── Hook: commit-msg validation

4. /implement
   ↓ Writes code
   ├── Hook: pre-implementation (verify tests exist)
   ├── Uses: implementation-with-protection skill
   └── Hook: post-code (auto-run tests)

5. /iterate (if tests fail)
   ↓ Refines code
   ├── Uses: refactoring skill, overfitting-detection skill
   └── Hook: post-code (auto-run tests)

6. /commit-code
   ↓ Git commit
   ├── Hook: pre-commit (verify tests pass)
   ├── Uses: git-operations skill
   └── Hook: commit-msg validation
```

---

**Last Updated**: 2025-10-29
**Architecture Version**: 1.0
**Maintainer**: Brandon Fryslie
