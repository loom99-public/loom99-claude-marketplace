---
name: audit
description: Deep forensic examination of the codebase. Use for comprehensive quality, security, architecture, or debt analysis.
---

# Audit

Exhaustive, in-depth evaluation. Full forensic examination.

## Process

Use do3:project-evaluator in **audit mode**:

1. **Scope**: If area specified, focus there. Otherwise, audit entire project.
2. **Examine**: Architecture, code quality, dependencies, security, documentation, technical debt
3. **Generate**: AUDIT-*.md with comprehensive findings

## Output Format

Problem inventory with priorities:
- **P0**: Critical - fix immediately
- **P1**: High - fix soon
- **P2**: Medium - plan to address
- **P3**: Low - nice to have

```
═══════════════════════════════════════
Audit Complete
  Scope: [entire project | specific area]
  Findings: P0: n | P1: n | P2: n | P3: n
  Report: AUDIT-<area>-<timestamp>.md
═══════════════════════════════════════
```
