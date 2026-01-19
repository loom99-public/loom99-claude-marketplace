# Evaluation: Remove Duplicate Gabe Agent

**Generated**: 2026-01-19
**Topic**: Remove duplicate gabe agent from do-extra plugin

## Current State

### Two Identical Files Exist

| Location | Size | Purpose |
|----------|------|---------|
| `plugins/do-more/agents/gabe.md` | 151 lines | Canonical rigidity analysis agent |
| `plugins/do-extra/agents/gabe.md` | 151 lines | DUPLICATE - identical content |

Files verified identical via `diff` - no differences.

### Reference Analysis

**do-extra references to gabe:**
- `plugins/do-extra/README.md:16` - Lists gabe as available agent
- `plugins/do-extra/README.md:22` - Documents when to use gabe

**do-more references to gabe:**
- Agent file only (no commands/skills invoke it yet)

### Plugin Fit Analysis

| Plugin | Fit for gabe | Reasoning |
|--------|-------------|-----------|
| do-more | HIGH | Development workflow plugin, gabe analyzes code structure |
| do-extra | LOW | Experimental plugin for niche tools, gabe is serious tooling |

## What Needs to Change

### DELETE: do-extra/agents/gabe.md
- Exact duplicate of do-more version
- Violates One Source of Truth principle
- Creates maintenance burden and potential drift

### UPDATE: do-extra/README.md
- Remove gabe from Agents section
- Remove gabe from "When to Use" section

### KEEP: do-more/agents/gabe.md
- The one source of truth for gabe agent
- Remains available for future command integration

## Verdict

**CONTINUE** - Clear path forward. Simple deletion with documentation update.
