# Implementation Context: remove-vestigial-audit-skill

**Sprint**: remove-vestigial-audit-skill
**Generated**: 2026-01-18

## Background

The do-more plugin has three audit-related components:

1. **audit command** (`commands/audit.md`) - User-facing `/do:audit` command
2. **audit skill** (`skills/audit/SKILL.md`) - VESTIGIAL, never invoked
3. **audit-master skill** (`skills/audit-master/SKILL.md`) - The real implementation

The audit command explicitly routes to `audit-master`, bypassing the `audit` skill entirely.

## Why This Consolidation

- **One Source of Truth**: audit-master is the canonical implementation
- **Single Enforcer**: Only audit-master should define audit behavior
- **No Confusion**: Having both `audit` and `audit-master` skills creates ambiguity

## File Locations

```
plugins/do-more/
├── commands/
│   └── audit.md              # KEEP - routes to audit-master
├── skills/
│   ├── audit/                # DELETE - vestigial
│   │   └── SKILL.md
│   └── audit-master/         # KEEP - canonical implementation
│       ├── SKILL.md
│       └── references/       # KEEP - all reference materials
```

## Documentation Files to Update

1. `plugins/do-more/CLAUDE.md` line 171
   - Lists `do:audit` in skills table
   - Should be `do:audit-master` or removed

2. `plugins/do-more/docs/SKILLS.md` lines 32, 287, 471
   - References to `do:audit` skill
   - Should point to `audit-master`

## Verification

The command should continue to work after changes:
```
/do:audit security
```
This invokes the command, which invokes audit-master skill.

## Related But Out of Scope

- `planning-audit` skill - standalone, keep as-is
- `security-audit` skill - standalone, keep as-is
- `competitive-audit` skill - standalone, keep as-is
- `deep-audit` skill - standalone, keep as-is
- `test-coverage-audit` skill - standalone, keep as-is

These skills can be invoked directly for single-dimension audits. audit-master is for multi-dimension comprehensive audits.
