---
name: feature-proposal
description: Design a new feature with user value focus. Use when user wants to propose, design, or spec a new feature.
---

# Feature Proposal

Design high-value features that are innovative yet pragmatic.

## Process

Use do:product-visionary agent to:

1. **Understand**: What problem does this solve? Who benefits?
2. **Design**: Core functionality, user experience, technical approach
3. **Assess**: Effort, risks, dependencies
4. **Generate**: Feature proposal document

## Beads Integration (if available)

After proposal is complete, create tracking epic:
```bash
bd create "Epic: <feature name>" \
  --description="<problem statement + proposed solution summary>" \
  -t epic -p <priority based on value assessment> --json
# Returns bd-xxx

# If user stories are defined, create as children:
bd create "Story: <user story 1>" -p <priority> --json  # bd-xxx.1
bd create "Story: <user story 2>" -p <priority> --json  # bd-xxx.2

bd sync
```

## Output

Feature proposal with:
- Problem statement
- Proposed solution
- User stories
- Technical considerations
- Success metrics
- Beads epic ID (if created)

```
═══════════════════════════════════════
Feature Proposal Complete
  Feature: [name]
  Value: [1-sentence benefit]
  Report: FEATURE-<name>-<timestamp>.md
  Beads: bd-xxx (epic with n stories)
Next: /do:plan to incorporate into roadmap
═══════════════════════════════════════
```
