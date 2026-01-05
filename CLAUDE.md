# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Claude Code Plugin Marketplace containing workflow automation plugins for software development. The marketplace is published at `loom99-public/loom99-claude-marketplace`.

**Requirements:** Claude Code 1.0.33+

## Active Plugins

| Plugin | Alias | Description |
|--------|-------|-------------|
| do | `do` | Ideate, evaluate, research, plan, test, implement, verify |
| do-more | `do-more` | Advanced workflows: audit, docs, handoff, release, research |

## Development Commands

```bash
# Validate marketplace and all plugins
just validate

# Run test suite
just test

# Run structure validation only
just test-structure

# Full verification (validate + test)
just verify

# Pre-commit checks
just pre-commit

# Show plugin statistics
just stats

# Clean test artifacts
just clean
```

## Plugin Structure

Each plugin follows this structure:
```
plugins/<name>/
├── .claude-plugin/plugin.json   # Plugin manifest (required)
├── agents/                      # Agent definitions (*.md)
├── commands/                    # Slash commands (*.md)
├── hooks/                       # Lifecycle hooks (hooks.json)
├── skills/                      # Skills (skill-name/SKILL.md)
└── .mcp.json                    # MCP server config (optional)
```

### Key Files

- **Marketplace manifest**: `.claude-plugin/marketplace.json`
- **Plugin manifests**: `plugins/*/.claude-plugin/plugin.json`
- **Skills**: Must be in `skills/<skill-name>/SKILL.md` with YAML frontmatter
- **Commands**: `commands/<name>.md` → `/name` slash command

## Key Workflows

### do Plugin

Primary commands:
- `/do:it <task>` - Implement with planning and verification
- `/do:plan <task>` - Evaluate and create implementation plan
- `/do:status` - Quick status check
- `/do:chores` - Maintenance tasks

### do-more Plugin

Primary commands:
- `/do:stuff` - Advanced implementation with multiple approaches
- `/do:audit` - Comprehensive code/planning/security audit
- `/do:test` - Testing audit, recommendations, implementation
- `/do:tdd` - Test-driven development workflow
- `/do:feature-proposal` - Generate feature proposals
- `/do:init-project` - Initialize new projects

## Architecture Notes

- **Planning documents**: All workflow state lives in `.agent_planning/`
- **Skills are auto-discoverable**: Claude invokes skills based on description matching
- **Hooks enforce discipline**: Pre-hooks gate operations, post-hooks remind about next steps
- **Testing**: pytest-based functional tests in `tests/functional/`

## Adding New Components

### New Skill
1. Create `plugins/<plugin>/skills/<skill-name>/SKILL.md`
2. Add YAML frontmatter with `name` and `description` fields
3. Reload plugin: `/plugin reload <plugin>`

### New Command
1. Create `plugins/<plugin>/commands/<name>.md`
2. Filename becomes command: `foo.md` → `/foo`
3. Reload plugin

### New Plugin
1. Create plugin directory under `plugins/`
2. Add `.claude-plugin/plugin.json` manifest
3. Add entry to `.claude-plugin/marketplace.json`
4. Run `just validate` to verify
