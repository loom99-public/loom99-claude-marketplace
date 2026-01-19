# Implementation Context: fix-hooks

**Sprint**: fix-hooks
**Generated**: 2026-01-19

## Background

The do-more plugin documentation claims extensive hook functionality:
- SessionStart hook for initialization
- Stop hook for aggregating execution logs
- Scripts in `bin/` directory

**None of this exists.** The hooks.json is empty, and the `bin/` directory doesn't exist.

This creates active harm:
- Users may expect features that don't work
- Documentation misleads developers
- Violates "documentation matches code" principle

## Why Remove, Not Implement

1. **Immediate debt**: False documentation is actively misleading NOW
2. **Unclear value**: Execution logging was a proposal that was never validated
3. **Complexity**: do plugin already has hooks; more creates conflicts
4. **Incremental approach**: Clean up now, implement later with clear requirements

## Files to Modify

```
plugins/do-more/
├── CLAUDE.md                     # Remove hook claims
├── README.md                     # Remove execution log references
├── architecture/
│   ├── README.md                 # Remove bin/ and hook sections
│   └── EXECUTION-FLOW.md         # Remove "Hook Execution Flow"
├── FEATURE_PROPOSAL_...md        # Archive to .agent_planning/archive/
└── hooks/
    └── hooks.json                # Delete or document as empty
```

## What Gets Removed

### From CLAUDE.md
- Hook architecture section
- Execution tracking documentation
- References to `bin/init.py` and `bin/aggregate-exec.py`

### From README.md
- "Stop hook aggregates execution report"
- ".agent_logs/do/ has the receipts"

### From architecture/README.md
- Hook Integration section
- `bin/` directory in structure
- Runtime files execution log references

### From architecture/EXECUTION-FLOW.md
- Entire "Hook Execution Flow" section

## What Stays

- `agents/execution-summarizer.md` - Agent exists and is valid
- Empty `hooks/hooks.json` - May be kept with explanatory note
- General hook capability documentation (just not false claims)

## Related Work

The `connect-orphaned-agents` roadmap item will later wire execution-summarizer via actual hooks, at which point that functionality can be documented.
