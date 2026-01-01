# Decision Templates

Templates for presenting decisions and collecting approvals.

## AskUserQuestion Format

When presenting a decision in BLOCKING or HYBRID+HIGH mode:

```markdown
## Decision Approval Needed

**Agent**: [agent-name]
**Risk Level**: [HIGH/MEDIUM/LOW]
**Category**: [architecture/technology/implementation/testing/documentation]

### Decision
[One sentence summary of what was decided]

### Options Considered
- **A**: [option] - [tradeoffs]
- **B**: [option] - [tradeoffs]
- **C**: [option] - [tradeoffs]

### Recommended
**[Chosen option]**: [detailed rationale]

### Impact If Wrong
[Consequences if this turns out to be the wrong choice]

---

How would you like to proceed?
```

## AskUserQuestion Options

```json
{
  "question": "How would you like to proceed with this decision?",
  "header": "Decision",
  "options": [
    {"label": "Approve", "description": "Continue with the recommended choice"},
    {"label": "Reject", "description": "Stop workflow for manual intervention"},
    {"label": "Modify", "description": "Provide alternative approach"}
  ],
  "multiSelect": false
}
```

If user selects "Modify", capture their input as USER_FEEDBACK in the decision file.

---

## Decision Categories

| Category | Examples | Typical Risk |
|----------|----------|--------------|
| architecture | Component structure, system boundaries | HIGH |
| technology | Framework choice, library selection | HIGH/MEDIUM |
| implementation | Algorithm choice, data structures | MEDIUM |
| testing | Test strategy, coverage targets | MEDIUM/LOW |
| documentation | Doc format, what to document | LOW |

---

## Risk Level Guidelines

**HIGH**: Expensive to change, affects many components, external-facing
**MEDIUM**: Affects single component, moderate change cost
**LOW**: Easily reversible, localized impact, cosmetic
