---
name: artifact-templates
description: Templates for the 4 live governance artifacts (TARGET, BOUNDARY, BLOCKERS, METRICS) used in the minimal control loop
---

# Artifact Templates Skill

## Purpose

Provides canonical templates for the 4 live artifacts that drive the minimal control loop. These templates ensure consistency and completeness when initializing or updating governance artifacts.

## When to Use

- During `/loop:init` to bootstrap governance directory
- When creating new governance artifacts
- When validating existing artifacts for completeness
- As reference for artifact structure and required fields

## The Four Live Artifacts

All artifacts live in `governance/live/` and must fit on one screen (< 50 lines).

### 1. TARGET.md

Defines the target end state and Definition of Done.

**Template:**

```markdown
# Target End State

## Goal
[1-2 sentence description of what "done" means]

## Non-Goals
[Explicit exclusions - what we will NOT do]
- [Non-goal 1]
- [Non-goal 2]

## Target Shape
[5-10 bullets describing the desired end state]
- [Module/component structure]
- [Key interfaces and APIs]
- [Behavior characteristics]
- [Data model state]
- [Integration points]

## Definition of Done
[Checklist of observable completion criteria]
- [ ] System builds without errors
- [ ] All must-pass tests passing
- [ ] No forbidden legacy imports (outside bridge)
- [ ] Migration completed (old system unreachable)
- [ ] Smoke tests passing
- [ ] [Project-specific criterion]
- [ ] [Project-specific criterion]

## Last Updated
[YYYY-MM-DD HH:MM] - [brief change description]
```

**Required Fields:**
- Goal (must be 1-2 sentences)
- Non-Goals (at least 1 item)
- Target Shape (5-10 bullets)
- Definition of Done (minimum 5 items, all testable)

**Validation Rules:**
- DoD items must be observable/testable (not "code is clean")
- Target shape should describe structure, not implementation details
- Non-goals prevent scope creep

---

### 2. BOUNDARY.md

Defines the boundary law between legacy and new systems.

**Template:**

```markdown
# Boundary Law

## The Law
[Single sentence defining the boundary rule]

**Example:** "New code must not import or call legacy code except through the `compatibility` bridge module."

## Bridge Definition
[Specification of the allowed bridge/adapter]

**Module/Path:** `[path to bridge module]`

**Allowed Surface:**
- [API/function allowed through bridge]
- [API/function allowed through bridge]
- [API/function allowed through bridge]

**Bridge Constraints:**
- Bridge must be stateless
- Bridge may not expose legacy data structures
- Bridge surface area must shrink toward zero

## Forbidden Dependencies
[Explicit list of disallowed imports/calls]

**Legacy modules (no direct imports):**
- `[legacy module 1]`
- `[legacy module 2]`
- `[legacy module 3]`

**Legacy symbols (no direct calls):**
- `[legacy function/class 1]`
- `[legacy function/class 2]`

## Temporary Exceptions
[Time-bounded exceptions to the boundary law]

| Exception | Reason | Expires When | Owner |
|-----------|--------|--------------|-------|
| [Component X may call legacy Y] | [blocker-id] | [blocker eliminated] | [name] |

**Rules for exceptions:**
- Every exception must cite a blocker ID
- Exception expires when blocker is eliminated
- No exception without expiry condition
- Monthly review of all exceptions

## Enforcement
[How the boundary law is enforced]
- [ ] CI linter checks imports
- [ ] Manual code review checklist
- [ ] Automated tests for forbidden calls
- [ ] [Project-specific enforcement]

## Last Updated
[YYYY-MM-DD HH:MM] - [brief change description]
```

**Required Fields:**
- The Law (single sentence)
- Bridge Definition (module path + allowed surface)
- Forbidden Dependencies (at least 3 items)
- Enforcement mechanisms (at least 2)

**Validation Rules:**
- Law must be enforceable (not subjective)
- Bridge must have explicit allowed surface
- Temporary exceptions must have expiry conditions

---

### 3. BLOCKERS.md

Exhaustive list of ship-stoppers. The only work queue.

**Template:**

```markdown
# Blockers

## Active Blockers
[Numbered list of all issues preventing shipment]

### BLOCKER-001: [Short identifier]
**Observable Failure:** [Exact error, failing test, broken behavior]

**Impact:** Blocks DoD item "[which DoD item]"

**Evidence:**
- Error message: `[exact error text]`
- File/line: `[path:line]`
- Test: `[failing test name]`
- Log: `[link or path]`

**Context:** [Why this blocks progress]

**Last Attempt:** [YYYY-MM-DD] - [what was tried, why it failed]

---

### BLOCKER-002: [Short identifier]
[Same structure as above]

---

## Escalations Needed
[Blockers requiring human decisions]

### ESCALATION-001: [Decision needed]
**Blocked By:** BLOCKER-[id]

**Question:** [Specific question requiring user input]

**Options:**
1. **Option A:** [description]
   - Pros: [list]
   - Cons: [list]
   - Impact: [specific consequences]

2. **Option B:** [description]
   - Pros: [list]
   - Cons: [list]
   - Impact: [specific consequences]

**Recommended:** [Option X] because [rationale]

**Decision Required By:** [Date or phase]

---

## Recently Eliminated
[Blockers resolved in last 5 phases - provides context]

| ID | Eliminated | Method | Outcome |
|----|------------|--------|---------|
| BLOCKER-000 | 2025-01-03 | [approach] | [result] |

## Last Updated
[YYYY-MM-DD HH:MM] - [brief change description]
```

**Required Fields:**
- At least 1 active blocker (or "none" with justification)
- Each blocker must have: ID, Observable Failure, Impact, Evidence
- Escalations must have: Options (min 2), Recommendation

**Validation Rules:**
- Observable failure must be specific (exact error, test name, file:line)
- Impact must cite a DoD item or metric
- Evidence must be verifiable (error log, test output, file path)
- No blocker without observable failure
- Escalations must present bounded options (not open-ended questions)

---

### 4. METRICS.md

2-4 monotonic measures of convergence.

**Template:**

```markdown
# Convergence Metrics

## Metrics
[2-4 metrics that must move monotonically toward targets]

### Metric 1: [Name]
**Definition:** [What this measures]

**Measurement Method:**
```bash
[Exact command or script to measure]
# Example: grep -r "import.*legacy" src/ | wc -l
```

**Current Value:** [number] (as of [YYYY-MM-DD HH:MM])

**Target Value:** [number]

**Delta:** [+/- number] (direction: [toward/away from] target)

**Trend:** [last 5 measurements]
- [YYYY-MM-DD]: [value]
- [YYYY-MM-DD]: [value]
- [YYYY-MM-DD]: [value]

**Threshold for Escalation:** No progress after [N] phases

---

### Metric 2: [Name]
[Same structure as above]

---

## Metric Selection Guidelines

**Good metrics:**
- Automated measurement (no human judgment)
- Monotonic (should only move toward target)
- Directly related to DoD items
- Measurable multiple times per day
- Clear target value

**Bad metrics:**
- "Code quality" (subjective)
- "Developer happiness" (not measurable)
- Metrics that can move backward arbitrarily
- Metrics requiring manual counting

## Recommended Metrics for Migrations

1. **Legacy Import Count**
   - Count of imports to forbidden legacy modules
   - Target: 0
   - Command: `grep -r "import.*legacy" src/ --exclude-dir=bridge | wc -l`

2. **Failing Tests in Must-Pass Category**
   - Count of tests that must pass before shipment
   - Target: 0
   - Command: `pytest tests/must_pass/ --tb=no -q | grep "failed" | cut -d' ' -f1`

3. **Quarantined Test Count**
   - Tests temporarily disabled during migration
   - Target: 0
   - Command: `grep -r "@pytest.mark.quarantine" tests/ | wc -l`

4. **Legacy UI Entrypoint Count**
   - Reachable routes to old system
   - Target: 0
   - Command: `grep -r "route.*legacy" src/routes/ | wc -l`

## Last Updated
[YYYY-MM-DD HH:MM] - [brief change description]
```

**Required Fields:**
- 2-4 metrics (not fewer, not more)
- Each metric must have: Definition, Measurement Method, Current/Target/Delta
- Trend data (at least 3 measurements)
- Threshold for escalation

**Validation Rules:**
- Measurement method must be executable command or script
- Target must be numeric and specific
- Delta must show direction (toward/away from target)
- Metrics must be monotonic (if not, requires justification)
- Stagnation threshold must be specified

---

## Usage Patterns

### Pattern 1: Bootstrap New Governance

```markdown
Used by: /loop:init command

1. User provides goal statement
2. Generate TARGET.md with goal + empty DoD template
3. Scan repo for architecture, suggest boundary candidates
4. User selects boundary, generate BOUNDARY.md
5. Initial BLOCKERS.md with placeholder
6. Initial METRICS.md with recommended metrics
```

### Pattern 2: Validate Existing Artifacts

```markdown
Used by: Governor agent pre-phase check

For each artifact:
1. Check required fields present
2. Validate field formats
3. Check artifact is < 50 lines
4. Warn if validation fails
5. Suggest corrections
```

### Pattern 3: Update Artifact Post-Phase

```markdown
Used by: Governor agent post-phase

1. Read current artifact
2. Apply delta (add blocker, update metric, etc.)
3. Update "Last Updated" timestamp
4. Validate updated artifact
5. Write back to file
```

## Error Handling

**Missing Required Field:**
- Template provides default placeholder
- Warn user to fill in
- Block phase execution if critical field empty

**Artifact Too Large (> 50 lines):**
- Warn that artifact is unreadable in one screen
- Suggest splitting into current + archive
- Block phase execution until trimmed

**Invalid Metric:**
- Non-executable measurement method → provide example command
- Non-numeric target → request specific number
- Missing trend data → initialize with current value only

**Blocker Without Evidence:**
- Refuse to add blocker
- Request observable failure and evidence link
- Suggest running tests/checks to capture evidence

## Integration Points

**Commands:**
- `/loop:init` - Uses all 4 templates to bootstrap
- `/loop:status` - Reads all 4 artifacts
- `/loop:phase` - Governor updates artifacts using templates as validation

**Agents:**
- Governor - Validates artifacts against templates before each phase
- (Future) Consistency Auditor - Uses templates to check artifact completeness

**Skills:**
- phase-ritual - References templates when restating artifacts
- (Future) artifact-validator - Deep validation against templates

## Best Practices

1. **Keep artifacts one-screen** - If > 50 lines, move details to supporting docs
2. **Update timestamps** - Every artifact change must update "Last Updated"
3. **Preserve history in comments** - Major changes noted in artifact
4. **Validate before commit** - Run artifact validation before phase ends
5. **Link artifacts** - Blockers cite DoD items, Metrics align with Target

## See Also

- `docs/_now/control-loop-system/CONTEXT-PRIME.md` - Full system specification
- `agents/governor.md` - Governor agent (uses these templates)
- `skills/phase-ritual/SKILL.md` - Phase ritual (restates artifacts)
- `commands/init.md` - Initialization command (creates artifacts from templates)
