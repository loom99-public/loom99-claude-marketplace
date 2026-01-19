# Evaluation: Audit Consolidation

**Generated**: 2026-01-18
**Topic**: Consolidate audit command functionality into audit-master skill

## Current State

### Three Components Exist

| Component | Location | Size | Purpose |
|-----------|----------|------|---------|
| **audit command** | `plugins/do-more/commands/audit.md` | 604 bytes, 18 lines | Light wrapper that routes to `audit-master` skill |
| **audit skill** | `plugins/do-more/skills/audit/SKILL.md` | 4,712 bytes, 160 lines | Dimension routing logic with skill invocations |
| **audit-master skill** | `plugins/do-more/skills/audit-master/SKILL.md` | 41,704 bytes, 1065 lines | Comprehensive audit content with all 5 dimensions + references |

### Relationship Analysis

```
audit command (18 lines)
    └── Routes to "audit-master" skill

audit skill (160 lines)
    └── Dimension Selection UI
    └── Routing table pointing to OTHER skills:
        - Code Quality → do:deep-audit
        - Planning → do:planning-audit
        - Security → do:security-audit
        - Competitive → do:competitive-audit
    └── Combined output template

audit-master skill (1065 lines)
    └── Dimension Selection UI (DUPLICATE of audit skill)
    └── ALL FIVE dimensions implemented inline:
        - Code Quality (with sub-dimensions)
        - Planning Alignment
        - Security
        - Competitive
        - Test Coverage
    └── Combined output template
    └── 70+ reference files in references/
```

### Key Observations

1. **The audit command already routes to audit-master**: Line 11 says `Use the Skill tool to invoke 'do:audit-master' skill`

2. **The audit skill is REDUNDANT**:
   - Its dimension selection UI is duplicated in audit-master
   - It routes to OTHER skills (deep-audit, planning-audit, etc.) that may or may not exist
   - audit-master has all dimensions self-contained

3. **audit-master is the canonical implementation**:
   - Contains all 5 dimensions with full workflows
   - Has extensive reference documentation
   - Is what the command actually invokes

4. **Inconsistent skill references in audit skill**:
   - References `do:deep-audit` - may not exist
   - References `do:planning-audit` - EXISTS as separate skill
   - References `do:security-audit` - EXISTS as separate skill
   - References `do:competitive-audit` - EXISTS as separate skill

## What Exists

1. **audit command**: Properly routes to audit-master
2. **audit-master skill**: Complete, authoritative implementation
3. **audit skill**: Vestigial routing layer that's never invoked

## What's Missing

Nothing functionally missing. The audit skill is unused and creates confusion.

## What Needs Changes

### DELETE: audit skill (`plugins/do-more/skills/audit/`)
- Never invoked (command routes directly to audit-master)
- Routing logic duplicates what audit-master does internally
- Creates confusion about which skill is canonical

### KEEP: audit command
- Already works correctly
- Provides nice `/do:audit` user interface
- Routes to the correct skill

### KEEP: audit-master skill
- The one source of truth
- Contains all functionality
- Has all reference materials

## Dependencies and Risks

| Risk | Mitigation |
|------|------------|
| Someone might be invoking `do:audit` skill directly | Search codebase for references first |
| Related skills (planning-audit, security-audit) might be orphaned | Out of scope - they can be invoked directly if desired |

## Ambiguities and Unknowns

1. **Should audit-master be renamed to audit?**
   - Pro: Simpler naming
   - Con: Requires moving references/, updating command
   - Recommendation: NO - "audit-master" name communicates it's the comprehensive version

2. **Are the individual dimension skills (planning-audit, security-audit, etc.) still needed?**
   - They exist separately and can be invoked directly
   - Out of scope for this consolidation
   - Answer: YES, keep them for granular access

## Verdict

**CONTINUE** - Clear path forward. Simple deletion with verification.
