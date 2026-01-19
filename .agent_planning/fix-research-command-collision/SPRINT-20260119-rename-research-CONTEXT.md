# Implementation Context: rename-research

**Sprint**: rename-research
**Generated**: 2026-01-19

## Background

The `/do:research` command exists in BOTH plugins:
- **do plugin**: Internal research - iterative exploration for decision-making
- **do-more plugin**: External research - web search, docs, competitors

This causes user confusion about which command to use.

## Why `/do:external-research`

**Considered alternatives:**
1. `/do:market-research` - Too narrow (skill handles docs and patterns too)
2. `/do:web-research` - Also too narrow
3. `/do:external-research` - Accurately describes scope ✓

**Alignment with existing naming:**
- The skill is named `research-external-skill`
- The `do:market-research` skill already exists in do-extra
- `external-research` follows the `*-external-*` pattern

## Architecture Relationship

```
/do:research (do plugin)
└── research-skill
    └── do:researcher agent (internal mode)
    └── do:project-evaluator or do:work-evaluator

/do:external-research (do-more plugin) [NEW NAME]
└── research-external-skill
    └── "market" → do:market-research skill (do-extra)
    └── "docs/patterns" → do:researcher agent (external mode)
```

## File Locations

```
plugins/do-more/
├── commands/
│   └── research.md          # RENAME to external-research.md
├── skills/
│   └── research-external-skill/
│       └── SKILL.md         # KEEP unchanged
└── docs/
    ├── COMMANDS.md          # UPDATE references
    ├── AGENTS.md            # UPDATE references
    └── ...                  # UPDATE all /do:research refs

plugins/do/
├── commands/
│   └── research.md          # UNCHANGED
└── skills/
    └── research-skill/
        └── SKILL.md         # UNCHANGED
```

## Documentation Update Pattern

All these patterns need updating in do-more docs:

| Pattern | Replace With |
|---------|--------------|
| `/do:research` | `/do:external-research` |

**Exception**: References to `do:researcher` agent stay unchanged (it's an agent, not a command).
