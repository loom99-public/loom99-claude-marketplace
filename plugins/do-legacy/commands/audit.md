---
argument-hint: [area to audit]
description: In-depth evaluation of the repo. Exhaustive analysis with maximum detail.
---

Comprehensive, in-depth audit of the repository. Provides as much information and analysis as possible.

<audit-target>
$ARGUMENTS
</audit-target>

## Purpose

Unlike `/do:status` (quick diagnostic) or `/do:plan` (actionable planning), `/do:audit` is an exhaustive deep-dive that leaves no stone unturned. Think of it as a full forensic examination.

**Time**: 10-30 minutes depending on scope
**Output**: AUDIT-*.md with comprehensive findings

## Scope Selection

**No arguments**: Audit the entire project
- Architecture and structure
- Code quality and patterns
- Dependencies and security
- Documentation completeness
- Testing coverage
- Technical debt
- Performance considerations
- Maintainability assessment

**With arguments**: Focused audit on specified area
- Deep dive into that subsystem/component
- All related files and dependencies
- Integration points
- Edge cases and error handling
- Historical context from git

## Workflow

### Phase 1: Structural Analysis

Use do:project-evaluator in **exhaustive mode**:
- Inventory ALL files, not just key ones
- Document every pattern found
- List every dependency
- Map all integration points
- Identify every TODO/FIXME/HACK comment

### Phase 2: Quality Assessment

Continue with do:project-evaluator:
- Code complexity metrics
- Duplication detection
- Error handling patterns
- Logging and observability
- Security considerations
- Performance hotspots

### Phase 3: Documentation Review

- README completeness
- Code comments quality
- API documentation
- Architecture decision records
- Changelog maintenance

### Phase 4: Dependency Analysis

- Direct dependencies audit
- Transitive dependency risks
- Version currency (outdated packages)
- License compatibility
- Security vulnerabilities (if tools available)

### Phase 5: Historical Context

Use git history:
- Recent change velocity
- Areas of high churn
- Contributors and ownership
- Stale areas (no recent changes)
- Revert frequency

### Phase 6: Problem Inventory

Compile comprehensive list:
- **Critical**: Must fix immediately
- **High**: Should fix soon
- **Medium**: Fix when convenient
- **Low**: Nice to have
- **Future**: Long-term considerations

## Output Format

Create `AUDIT-<target>-<timestamp>.md` in `.agent_planning/`:

```markdown
# Audit: [Target]

**Date**: [timestamp]
**Scope**: [full project | specific area]
**Duration**: [time spent]

## Executive Summary
[1-2 paragraph overview of findings]

## Structural Analysis
### File Inventory
[Complete file listing with purposes]

### Architecture
[Diagram or description of structure]

### Patterns Identified
[List of patterns in use]

## Quality Assessment
### Code Quality
[Metrics and observations]

### Error Handling
[Patterns and gaps]

### Security Considerations
[Findings]

### Performance
[Observations]

## Documentation Status
[Completeness assessment]

## Dependencies
### Direct Dependencies
[List with versions and purposes]

### Concerns
[Outdated, vulnerable, unnecessary]

## Historical Context
### Change Velocity
[Recent activity patterns]

### Ownership
[Who maintains what]

## Problem Inventory

### Critical (P0)
| Issue | Location | Impact |
|-------|----------|--------|
| ... | ... | ... |

### High (P1)
[Same format]

### Medium (P2)
[Same format]

### Low (P3)
[Same format]

### Future Considerations
[Long-term items]

## Recommendations
[Prioritized action items]

## Appendix
[Raw data, full file lists, detailed metrics]
```

## Display Summary

```
═══════════════════════════════════════
Audit Complete: [target]

  Duration: [time]
  Files analyzed: [count]
  Issues found: [P0: n, P1: n, P2: n, P3: n]

  Report: .agent_planning/AUDIT-<target>-<ts>.md

Next: Review findings, then /do:plan for action items
═══════════════════════════════════════
```

## Relationship to Other Commands

| Command | Depth | Time | Purpose |
|---------|-------|------|---------|
| `/do:peek` | Surface | 30s-2min | Find things |
| `/do:status` | Diagnostic | 2-5min | Health check |
| `/do:plan` | Actionable | 5-10min | Create backlog |
| `/do:audit` | Exhaustive | 10-30min | Full examination |

Use `/do:audit` when you need complete understanding, not just actionable items.
