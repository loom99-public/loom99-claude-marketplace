# Human Gates: AskUserQuestion Interactions

This document defines all mandatory human decision points using Claude Code's AskUserQuestion tool.

---

## Design Principle: Structured Decisions

Human decisions are collected via `AskUserQuestion`, never free-form prose.

**Never:** "Edit this file and re-run"
**Always:** Structured options with clear consequences

Benefits:
- Decisions are explicit and recorded
- Options have clear pros/cons/impacts
- Recommendations guide but don't force
- User can always select "Other" for custom input

---

## Gate Summary

| Gate | Trigger | Decision Type |
|------|---------|---------------|
| #1: Accept Proposal | Proposal ready | Accept, Reject, OnIce, Evidence |
| #2: Ship Design | Implementation complete | Ship, Keep Active, Needs Work |
| #3: Supersede | Conflict detected | Supersede, Keep Current, Merge |
| #4: Reject | Feasibility fails | Reject, Revise, Archive |
| #5: Boundary Change | Coupling needed | Expand Bridge, Change Law, Alternative |
| Blocker Escalation | Attempts exhausted | [Custom options] |
| Init Prompts | During /loop:init | Goal, Boundary, Metrics |

---

## Gate #1: Accept Proposal

**Trigger:** Design proposal is ready to become binding.

**Presented By:** Design-Curator agent via decision-gate skill

**Context Required:**
- Proposal summary
- Governance deltas (TARGET, BOUNDARY, METRICS changes)
- Key risks
- Open questions (if any)

**AskUserQuestion Format:**

```yaml
questions:
  - question: "Accept proposal P-0001: New Authentication System?"
    header: "Accept"
    options:
      - label: "Accept (Recommended)"
        description: "Promote to Active. Apply governance deltas: +2 DoD items, +1 metric. Risk: Auth migration may surface edge cases."
      - label: "Reject"
        description: "Archive proposal. No changes to governance. Reason will be recorded."
      - label: "Request More Evidence"
        description: "Keep in review. Specify what evidence is needed before decision."
      - label: "Put On Ice"
        description: "Pause proposal. Revisit later. No changes to governance."
    multiSelect: false
```

**Post-Decision Actions:**

| Decision | Actions |
|----------|---------|
| Accept | Create active design, apply deltas, update DESIGN_LINKS, regenerate compressed |
| Reject | Move to archive/rejected, record reason in HISTORY.md |
| Evidence | Add to STATUS.md, keep in InReview |
| OnIce | Update STATUS.md state=OnIce, record reason |

---

## Gate #2: Ship Design

**Trigger:** Active design implementation claims completion.

**Presented By:** Design-Curator agent via decision-gate skill

**Context Required:**
- Acceptance criteria checklist with pass/fail
- Metric values vs targets
- Remaining gaps (if any)
- Evidence links

**AskUserQuestion Format:**

```yaml
questions:
  - question: "Ship design A-0001: Authentication Migration?"
    header: "Ship"
    options:
      - label: "Ship (Recommended)"
        description: "Mark complete. Criteria: 5/5 passed. Metrics at target. Archive design."
      - label: "Keep Active"
        description: "Not ready. Specify what's missing. Design stays in Active state."
      - label: "Ship with Known Gaps"
        description: "Accept as complete with documented limitations. Gaps become new blockers or roadmap items."
    multiSelect: false
```

**Post-Decision Actions:**

| Decision | Actions |
|----------|---------|
| Ship | Transition to Shipped, archive, update DESIGN_LINKS |
| Keep Active | Record reason, continue execution |
| Ship with Gaps | Create follow-up blockers/slices, then ship |

---

## Gate #3: Supersede Design

**Trigger:** Conflict between design/current and reality, or new proposal obsoletes existing.

**Presented By:** Design-Curator agent via decision-gate skill

**Context Required:**
- What is being superseded
- What replaces it (or why it's invalid)
- Migration impact
- Risk assessment

**AskUserQuestion Format:**

```yaml
questions:
  - question: "Supersede current auth design with new OAuth2 proposal?"
    header: "Supersede"
    options:
      - label: "Supersede (Recommended)"
        description: "Archive current design. New proposal becomes canonical. Migration: 3 active blockers will need re-evaluation."
      - label: "Keep Current"
        description: "Reject new proposal. Current design remains authoritative. New proposal archived."
      - label: "Merge Designs"
        description: "Incorporate elements of both. Creates new merged proposal for review."
    multiSelect: false
```

**Post-Decision Actions:**

| Decision | Actions |
|----------|---------|
| Supersede | Archive old, promote new, update DESIGN_LINKS, re-evaluate blockers |
| Keep Current | Archive proposal, record reason |
| Merge | Create new proposal combining elements, requires review |

---

## Gate #4: Reject Proposal

**Trigger:** Evidence or feasibility fails during review.

**Presented By:** Design-Curator agent via decision-gate skill

**Context Required:**
- What failed
- Why it's not viable
- Alternative approaches (if any)

**AskUserQuestion Format:**

```yaml
questions:
  - question: "Proposal P-0002 failed feasibility review. How to proceed?"
    header: "Reject"
    options:
      - label: "Reject (Recommended)"
        description: "Archive as rejected. Failure reason: Performance requirements cannot be met with proposed architecture."
      - label: "Revise"
        description: "Return to Proposed state. Author should address feasibility issues."
      - label: "Archive for Reference"
        description: "Keep as historical reference but mark non-viable. May inform future proposals."
    multiSelect: false
```

---

## Gate #5: Boundary Change

**Trigger:** Cross-world coupling becomes necessary for progress.

**Presented By:** Escalation-Handler agent via decision-gate skill

**Context Required:**
- Current boundary law
- What coupling is needed
- Why it's needed (blocker context)
- Blast radius analysis

**AskUserQuestion Format:**

```yaml
questions:
  - question: "BLOCKER-007 requires access to legacy store. Change boundary?"
    header: "Boundary"
    options:
      - label: "Expand Bridge (Recommended)"
        description: "Add getLegacyUser() to bridge surface. Allows progress on BLOCKER-007. Bridge grows by 1 function. Plan: remove after migration complete."
      - label: "Change Boundary Law"
        description: "Allow direct legacy access for auth module only. Higher risk: resurrection possible. Requires temporary exception with expiry."
      - label: "Find Alternative"
        description: "Reject boundary change. Find different approach to BLOCKER-007. May require more time."
      - label: "Escalate Further"
        description: "Need more information. Provide specific questions."
    multiSelect: false
```

**Post-Decision Actions:**

| Decision | Actions |
|----------|---------|
| Expand Bridge | Update BOUNDARY.md bridge surface, regenerate compressed |
| Change Law | Add exception to BOUNDARY.md with expiry condition |
| Alternative | Return to phase, try different approach |
| Escalate | Add specific questions, keep escalation open |

---

## Blocker Escalation

**Trigger:** Blocker attempts exhausted (N≥2 normal, N≥1 convergence).

**Presented By:** Escalation-Handler agent via decision-gate skill

**Context Required:**
- Blocker description
- What was attempted
- Why it failed
- Relevant evidence

**AskUserQuestion Format (varies by blocker):**

```yaml
questions:
  - question: "BLOCKER-003: Test test_profile_render fails after migration. Attempts exhausted. How to proceed?"
    header: "Escalate"
    options:
      - label: "Quarantine Test"
        description: "Mark test as migration-pending. Blocker becomes: migrate test. Coverage gap until resolved."
      - label: "Expand Bridge"
        description: "Add legacy dependency to bridge for this test. Increases bridge surface."
      - label: "Delete Test"
        description: "Test behavior is no longer needed. Remove test permanently. Document reasoning."
      - label: "Different Approach"
        description: "Specify alternative strategy to try."
    multiSelect: false
```

**Post-Decision Actions:**

| Decision | Actions |
|----------|---------|
| Quarantine | Update blocker, create new blocker for migration |
| Expand Bridge | Update BOUNDARY.md, continue phase |
| Delete | Remove test, document in HISTORY.md |
| Different | Record approach, reset attempts, continue phase |

---

## Init Prompts

**Trigger:** During `/loop:init` initialization.

**Presented By:** Governor agent (init mode) via decision-gate skill

### Goal Statement

```yaml
questions:
  - question: "What is the goal of this work? (1-2 sentence end state)"
    header: "Goal"
    options:
      - label: "Migration"
        description: "Move from legacy to new system (e.g., 'Migrate frontend state from Redux to Zustand')"
      - label: "Refactor"
        description: "Restructure without behavior change (e.g., 'Eliminate circular dependencies in core modules')"
      - label: "Feature"
        description: "Add new functionality (e.g., 'Implement OAuth2 authentication')"
      - label: "Other"
        description: "Describe your goal"
    multiSelect: false
```

### Boundary Selection

```yaml
questions:
  - question: "Select the boundary between legacy and new code:"
    header: "Boundary"
    options:
      - label: "src/legacy/ (detected)"
        description: "47 files. Imported by 12 components. Bridge candidate: src/compat/"
      - label: "old-api/ (detected)"
        description: "23 files. Imported by 8 services. Bridge candidate: src/api-adapter/"
      - label: "No boundary needed"
        description: "This work doesn't involve legacy/new separation"
      - label: "Custom"
        description: "Define custom boundary (forbidden paths and bridge)"
    multiSelect: false
```

### Metrics Selection

```yaml
questions:
  - question: "Select metrics to track convergence:"
    header: "Metrics"
    options:
      - label: "Recommended for migration"
        description: "Legacy imports, failing tests, migration coverage %"
      - label: "Recommended for refactor"
        description: "Circular dependencies, module coupling, test pass rate"
      - label: "Custom metrics"
        description: "Define your own measurement commands"
    multiSelect: false
```

---

## Implementation: decision-gate Skill

The `decision-gate` skill formats and presents all gates:

```markdown
## Procedure

1. Gather context for the decision
2. Determine gate type
3. Format options with:
   - Clear labels
   - Detailed descriptions with pros/cons/impact
   - Recommended option (if applicable)
4. Call AskUserQuestion tool
5. Process response
6. Update relevant artifacts
7. Record in HISTORY.md if significant

## AskUserQuestion Tool Call

```json
{
  "questions": [
    {
      "question": "[Clear question ending with ?]",
      "header": "[Short label, max 12 chars]",
      "options": [
        {
          "label": "[Option text]",
          "description": "[Explanation with consequences]"
        },
        {
          "label": "[Option text] (Recommended)",
          "description": "[Explanation + why recommended]"
        }
      ],
      "multiSelect": false
    }
  ]
}
```

## Response Handling

- User response comes as `answers` object
- Match to option selected
- If "Other" selected, parse custom text
- Execute corresponding actions
- Confirm result to user
```

---

## Recording Decisions

All significant decisions are recorded in `governance/HISTORY.md`:

```markdown
## [YYYY-MM-DD] - [Decision Title]

**Gate:** [Gate #N or Blocker Escalation]

**Context:** [What triggered the decision]

**Options Presented:**
1. [Option A]
2. [Option B]
3. [Option C]

**Decision:** [What was chosen]

**Rationale:** [Why, if provided]

**Impact:**
- TARGET: [change or "no change"]
- BOUNDARY: [change or "no change"]
- BLOCKERS: [change or "no change"]
- METRICS: [change or "no change"]

---
```

---

## Best Practices

### Writing Options

1. **Be specific** — "Add function X to bridge" not "Expand bridge"
2. **Include consequences** — What happens if they choose this?
3. **Show tradeoffs** — Pros AND cons for each option
4. **Make recommendation clear** — Append "(Recommended)" to label
5. **Explain recommendation** — Why this option over others?

### Handling Responses

1. **Confirm understanding** — "You chose X, which means Y"
2. **Execute immediately** — Don't defer artifact updates
3. **Record decision** — Add to HISTORY.md
4. **Regenerate compressed** — If governance changed

### When to Escalate vs. When to Gate

- **Escalation:** Blocker-specific, attempts exhausted, need direction
- **Gate:** Lifecycle transition, affects binding authority

---

## Summary

Human gates ensure critical decisions are explicit and structured:

| Gate | Key Decision |
|------|--------------|
| #1 Accept | Proposal → Active |
| #2 Ship | Active → Shipped |
| #3 Supersede | Replace canonical design |
| #4 Reject | Archive as non-viable |
| #5 Boundary | Change coupling rules |
| Escalation | Resolve stuck blocker |
| Init | Goal, boundary, metrics |

All use AskUserQuestion with clear options, consequences, and recommendations.
