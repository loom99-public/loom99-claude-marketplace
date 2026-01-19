# Evaluation: Fix Research Command Collision

**Generated**: 2026-01-19
**Topic**: Rename do-more's /do:research to eliminate namespace collision

## Current State

### Two /do:research Commands Exist

| Plugin | Skill | Purpose |
|--------|-------|---------|
| **do** | `research-skill` | Internal research - iterative exploration, decision-making, feeds into /plan |
| **do-more** | `research-external-skill` | External research - web search, docs, market analysis, competitors |

### The do Plugin Version (research-skill)
- Loops researcher->evaluator until research is SUFFICIENT
- Maximum 3 iterations
- Auto-selects recommendation
- Output feeds into `/plan` workflow
- **Scope**: Project-wide or focused internal exploration

### The do-more Plugin Version (research-external-skill)
- Uses WebSearch/WebFetch for external sources
- Three sub-modes:
  - "market/competitors" → delegates to `do:market-research` skill
  - "docs/documentation" → uses `do:researcher` in external mode
  - "patterns/best practices" → uses `do:researcher` in external mode
- **Scope**: External-only (web, competitors, external docs)

## Recommendation: Rename to `/do:external-research`

**Rationale:**
1. The skill is already named `research-external-skill`
2. `market-research` would be too narrow (command handles docs and patterns too)
3. `external-research` clearly distinguishes from internal research
4. Aligns with existing skill naming convention

## Files to Update

### Primary Changes
| File | Change |
|------|--------|
| `commands.yaml:104-108` | Change `name: research` to `name: external-research` |
| `plugins/do-more/commands/research.md` | Rename to `external-research.md` |

### Documentation Updates (26+ references in do-more docs)
- CLAUDE.md, README.md
- docs/COMMANDS.md, AGENTS.md, EXAMPLES.md
- docs/GETTING-STARTED.md, GATING.md, WORKFLOWS.md
- architecture/README.md

## Verdict

**CONTINUE** - Clear path forward with low risk.
