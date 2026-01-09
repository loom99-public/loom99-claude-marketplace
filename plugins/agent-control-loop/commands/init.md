---
argument-hint: [optional: goal statement]
description: Bootstrap governance/ directory with 4 live artifacts. Prompts for goal, scans repo for boundaries, generates initial TARGET, BOUNDARY, BLOCKERS, METRICS files.
---

# /loop:init - Initialize Governance

Creates the minimal control loop infrastructure by bootstrapping the `governance/live/` directory with the 4 live artifacts.

## Prerequisites

**None.** This is the entry point to the control loop system.

## What This Command Does

1. Creates `governance/live/` directory structure
2. Prompts user for goal statement (if not provided)
3. Scans repository for architecture boundaries
4. Generates 4 artifact files from templates:
   - `TARGET.md` - Goal, non-goals, target shape, DoD
   - `BOUNDARY.md` - Boundary law, bridge, forbidden deps
   - `BLOCKERS.md` - Initial blocker queue
   - `METRICS.md` - 2-4 convergence metrics
5. Creates `governance/PHASE-LOG.md` for historical record
6. Displays initialization summary

## Step 1: Check for Existing Governance

Before initializing, check if `governance/live/` already exists:

```bash
ls governance/live/ 2>/dev/null
```

**If exists:**
- Display warning: "Governance directory already exists. Reinitializing will overwrite existing artifacts."
- Ask user: "Continue and overwrite? (yes/no)"
- If "no": Exit gracefully
- If "yes": Proceed (backup existing to `governance/live.backup-YYYYMMDD/`)

**If not exists:**
- Proceed to Step 2

---

## Step 2: Gather Goal Statement

**If goal provided as argument:**
```bash
/loop:init "Migrate frontend from Redux to Zustand"
```
Use provided goal statement.

**If no argument provided:**

Prompt user:

```markdown
┌─ Control Loop Initialization ─────────────────────────┐
│                                                        │
│ What is the goal of this work?                        │
│ (1-2 sentence description of "done")                  │
│                                                        │
│ Examples:                                              │
│ - "Migrate all frontend state to new store"           │
│ - "Replace legacy auth with OAuth2"                   │
│ - "Eliminate circular dependencies in core modules"   │
│                                                        │
└────────────────────────────────────────────────────────┘

Goal: _
```

**Validation:**
- Goal must be 1-2 sentences
- Goal must describe end state (not process)
- Goal must be specific and testable

**If invalid:** Re-prompt with feedback.

---

## Step 3: Scan Repository for Boundaries

Detect likely architecture boundaries to suggest for BOUNDARY.md:

```bash
# Common boundary patterns

# 1. Directory structure (most common)
find . -type d -maxdepth 3 | grep -E "(legacy|old|deprecated|v1|compat)"

# 2. Import patterns
grep -r "^import.*from" --include="*.ts" --include="*.js" | cut -d: -f2 | sort | uniq -c | sort -rn | head -20

# 3. Module naming
find . -name "*.ts" -o -name "*.js" | grep -E "(legacy|old|deprecated)"

# 4. Package.json dependencies (if exists)
cat package.json | grep -E "(legacy|old|deprecated)" 2>/dev/null
```

**Analyze results:**
- Group by common patterns (e.g., `src/legacy/*`, `old-api/*`)
- Identify candidate "new" vs "old" divisions
- Look for existing bridge/compat modules

**Present findings to user:**

```markdown
┌─ Boundary Detection ──────────────────────────────────┐
│                                                        │
│ Detected potential boundaries:                        │
│                                                        │
│ 1. src/legacy/ (47 files)                             │
│    Imported by: src/components/ (12 imports)          │
│    Bridge candidate: src/compat/                      │
│                                                        │
│ 2. old-api/ (23 files)                                │
│    Imported by: src/services/ (8 imports)             │
│    Bridge candidate: src/api-adapter/                 │
│                                                        │
│ 3. No clear boundary detected                         │
│                                                        │
│ Which boundary describes your migration?              │
│ (Enter number, or 'custom' for manual entry)          │
│                                                        │
└────────────────────────────────────────────────────────┘

Choice: _
```

**If user chooses custom:**

```markdown
┌─ Custom Boundary Definition ──────────────────────────┐
│                                                        │
│ What modules/paths are FORBIDDEN for new code?        │
│ (Comma-separated, e.g., src/legacy/*, old-api/*)      │
│                                                        │
└────────────────────────────────────────────────────────┘

Forbidden: _

┌─ Bridge Module ───────────────────────────────────────┐
│                                                        │
│ What module can new code use to call legacy?          │
│ (Path to bridge/adapter, e.g., src/compat/)           │
│                                                        │
└────────────────────────────────────────────────────────┘

Bridge: _
```

---

## Step 4: Generate TARGET.md

Use `artifact-templates` skill to create TARGET.md:

```markdown
# Target End State

## Goal
[User-provided goal statement]

## Non-Goals
[Prompt user: "What will we explicitly NOT do?"]
- [User input, or default: "Rewriting code that already works"]
- [User input, or default: "Changing APIs without migration path"]

## Target Shape
[Inferred from goal + boundary + user input]

**Prompt user:**
"Describe the desired end state in 5-10 bullets (modules, interfaces, behaviors):"

[Accept 5-10 bullets, or provide defaults based on goal]

## Definition of Done
[Generate based on goal type]

Standard DoD items for migrations:
- [ ] System builds without errors
- [ ] All must-pass tests passing
- [ ] No forbidden legacy imports (outside bridge)
- [ ] Bridge surface area reduced to zero (or minimal documented set)
- [ ] Migration smoke tests passing
- [ ] [Project-specific items from user]

**Prompt user:**
"Any additional completion criteria? (press Enter to skip)"

[Accept additional DoD items]

## Last Updated
[Current timestamp] - Initial creation
```

**Write to:** `governance/live/TARGET.md`

---

## Step 5: Generate BOUNDARY.md

Use `artifact-templates` skill to create BOUNDARY.md:

```markdown
# Boundary Law

## The Law
New code must not import or call legacy code except through the [bridge module] bridge.

[Use forbidden modules from Step 3]
[Use bridge path from Step 3]

## Bridge Definition

**Module/Path:** `[bridge path from Step 3]`

**Allowed Surface:**
[Prompt user: "What APIs/functions can new code use through the bridge?"]
[Or default: "TBD - define during first phase"]

**Bridge Constraints:**
- Bridge must be stateless
- Bridge may not expose legacy data structures directly
- Bridge surface area must shrink toward zero over time

## Forbidden Dependencies

**Legacy modules (no direct imports):**
[List from Step 3]

**Legacy symbols (no direct calls):**
[Default: "TBD - enumerate during first phase"]

## Temporary Exceptions

[Empty table initially]

| Exception | Reason | Expires When | Owner |
|-----------|--------|--------------|-------|
| (none) | - | - | - |

**Rules for exceptions:**
- Every exception must cite a blocker ID
- Exception expires when blocker is eliminated
- No exception without expiry condition
- Monthly review of all exceptions

## Enforcement

**Planned enforcement mechanisms:**
- [ ] TODO: Add CI linter to check imports
- [ ] TODO: Add manual code review checklist
- [ ] TODO: Add automated tests for forbidden calls

## Last Updated
[Current timestamp] - Initial creation
```

**Write to:** `governance/live/BOUNDARY.md`

---

## Step 6: Generate BLOCKERS.md

Use `artifact-templates` skill to create BLOCKERS.md:

```markdown
# Blockers

## Active Blockers

[Prompt user: "What are the top 1-3 known blockers preventing completion?"]
[Accept blocker descriptions, or default to bootstrap blocker]

### BLOCKER-001: Enumerate all blockers
**Observable Failure:** Blocker queue is incomplete

**Impact:** Blocks accurate DoD progress tracking

**Evidence:**
- This is the bootstrap blocker
- First phase should enumerate all known obstacles

**Context:**
We need to identify all issues preventing completion before we can drive to 100%.

**Last Attempt:** [Current timestamp] - Initial creation

---

[Additional blockers from user input, if provided]

---

## Escalations Needed

[Empty initially]

(none)

---

## Recently Eliminated

[Empty initially]

| ID | Eliminated | Method | Outcome |
|----|------------|--------|---------|
| - | - | - | - |

## Last Updated
[Current timestamp] - Initial creation
```

**Write to:** `governance/live/BLOCKERS.md`

---

## Step 7: Generate METRICS.md

Use `artifact-templates` skill to create METRICS.md:

**Recommend metrics based on goal type:**

- **Migration goal** → Legacy import count, failing tests
- **Refactor goal** → Circular dependencies, module coupling
- **Feature goal** → Feature coverage %, acceptance tests passing

**Prompt user:**

```markdown
┌─ Metrics Selection ───────────────────────────────────┐
│                                                        │
│ Recommended metrics for this goal:                    │
│                                                        │
│ 1. [Metric 1 name] (auto-detected)                    │
│    Command: [measurement command]                     │
│                                                        │
│ 2. [Metric 2 name] (auto-detected)                    │
│    Command: [measurement command]                     │
│                                                        │
│ Accept recommendations? (yes/no/custom)               │
│                                                        │
└────────────────────────────────────────────────────────┘

Choice: _
```

**If custom:**
```markdown
Metric 1 name: _
Measurement command: _

Metric 2 name: _
Measurement command: _

[Repeat for up to 4 metrics]
```

**Generate METRICS.md:**

```markdown
# Convergence Metrics

## Metrics

### Metric 1: [Name]
**Definition:** [Description]

**Measurement Method:**
```bash
[Command provided or detected]
```

**Current Value:** [Run command now to get baseline]

**Target Value:** [Infer from goal, or prompt user]

**Delta:** 0 (baseline measurement)

**Trend:**
- [Current timestamp]: [current value] (baseline)

**Threshold for Escalation:** No progress after 3 phases

---

### Metric 2: [Name]
[Same structure]

---

[Additional metrics if provided]

---

## Last Updated
[Current timestamp] - Initial creation
```

**Write to:** `governance/live/METRICS.md`

---

## Step 8: Create PHASE-LOG.md

Initialize the historical phase log:

```markdown
# Phase Log

Record of all phases executed during this control loop.

---

## Phase 0 - Initialization - [Current timestamp]

**Action:** Governance structure initialized

**Artifacts Created:**
- TARGET.md (Goal: [goal statement])
- BOUNDARY.md (Law: [boundary law])
- BLOCKERS.md ([N] initial blockers)
- METRICS.md ([N] metrics established)

**Baseline Metrics:**
- [Metric 1]: [value]
- [Metric 2]: [value]

**Next:** Run `/loop:phase` to begin first work phase

---
```

**Write to:** `governance/PHASE-LOG.md`

---

## Step 9: Validation

After all files created, validate structure:

```bash
# Check all required files exist
required_files=(
  "governance/live/TARGET.md"
  "governance/live/BOUNDARY.md"
  "governance/live/BLOCKERS.md"
  "governance/live/METRICS.md"
  "governance/PHASE-LOG.md"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "ERROR: Missing required file: $file"
    exit 1
  fi
done

# Check artifacts are < 50 lines
for file in governance/live/*.md; do
  lines=$(wc -l < "$file")
  if [ "$lines" -gt 50 ]; then
    echo "WARNING: $file has $lines lines (recommend < 50)"
  fi
done

# Validate metrics measurement commands work
# (Run each metric command, ensure exit code 0)
```

**If validation fails:**
- Display specific errors
- Suggest fixes
- Do not proceed to summary

**If validation passes:**
- Proceed to Step 10

---

## Step 10: Display Initialization Summary

```markdown
═══════════════════════════════════════════════════════
Control Loop Initialized
═══════════════════════════════════════════════════════

Goal: [goal statement]

Directory Structure Created:
governance/
├── live/
│   ├── TARGET.md           [DoD: 0/[N] complete]
│   ├── BOUNDARY.md         [Bridge: [path]]
│   ├── BLOCKERS.md         [[N] active blockers]
│   └── METRICS.md          [[N] metrics tracking]
└── PHASE-LOG.md            [Phase 0 recorded]

Baseline Metrics:
- [Metric 1]: [value] → [target]
- [Metric 2]: [value] → [target]

Top Blockers:
1. BLOCKER-001: [description]
2. BLOCKER-002: [description] (if exists)
3. BLOCKER-003: [description] (if exists)

Next Steps:
1. Review artifacts in governance/live/
2. Update DoD items if needed (edit TARGET.md)
3. Add any missing blockers (edit BLOCKERS.md)
4. Run `/loop:phase` to begin work

═══════════════════════════════════════════════════════
```

---

## Error Handling

**User cancels during prompts:**
- Save partial state to `governance/live/.init-incomplete`
- Suggest resuming or cleaning up

**Metric measurement command fails:**
- Warn user
- Suggest fixing command
- Allow placeholder value with TODO

**No clear boundary detected:**
- Provide "No boundary" option
- Skip bridge definition (can add later)
- Focus on goal and DoD

**Goal statement unclear:**
- Provide examples
- Allow "TBD - refine during first phase"
- Warn that vague goals lead to drift

**Directory already exists with content:**
- Always backup before overwriting
- Show backup location
- Offer to restore if initialization fails

---

## Integration Points

**Skills Used:**
- `artifact-templates` - Templates for all 4 artifacts
- (Optional) `prompt-questioning` - Enhanced user prompts

**Commands:**
- After init: User typically runs `/loop:status` to review
- Then: `/loop:phase` to start first phase

**Agents:**
- Governor will validate artifacts on first `/loop:phase` invocation

---

## Best Practices

1. **Keep goal specific** - Vague goals lead to drift
2. **Enumerate blockers early** - Better to over-list than under-list
3. **Choose measurable metrics** - Subjective metrics are useless
4. **Define boundary clearly** - Ambiguous boundaries enable resurrection
5. **Start with minimal DoD** - Can expand during first phase
6. **Backup existing state** - Always preserve user's work

---

## See Also

- `skills/artifact-templates/SKILL.md` - Artifact templates and structure
- `commands/status.md` - Review initialized governance
- `commands/phase.md` - Begin first work phase
- `agents/governor.md` - Governor agent that uses these artifacts
