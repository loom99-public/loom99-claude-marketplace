---
argument-hint: (none)
description: Quick snapshot of governance state. Displays TARGET goal, DoD progress, active blockers, metrics, and recommended next action.
---

# /loop:status - Governance Status

Provides a quick, at-a-glance view of the current governance state without executing a phase. Useful for checking progress, reviewing blockers, and deciding next actions.

## Prerequisites

**Required:**
- `governance/live/` directory exists (created by `/loop:init`)

**If missing:** Display helpful error and suggest `/loop:init`

## What This Command Does

1. Reads all 4 governance artifacts
2. Parses and summarizes current state
3. Displays:
   - TARGET goal and DoD progress
   - Active blockers (count + top 3)
   - Escalations pending (if any)
   - Metric values and deltas
   - Recommended next action
4. Validates artifact health (warnings if issues detected)

No artifacts are modified. This is read-only.

---

## Step 1: Pre-Flight Checks

Verify governance structure exists:

```bash
if [ ! -d "governance/live" ]; then
  echo "ERROR: Governance directory not found."
  echo ""
  echo "The control loop has not been initialized."
  echo "Run '/loop:init' to create governance structure."
  exit 1
fi

# Check which artifacts exist
existing=()
missing=()
artifacts=("TARGET.md" "BOUNDARY.md" "BLOCKERS.md" "METRICS.md")

for artifact in "${artifacts[@]}"; do
  if [ -f "governance/live/$artifact" ]; then
    existing+=("$artifact")
  else
    missing+=("$artifact")
  fi
done

if [ ${#missing[@]} -gt 0 ]; then
  echo "WARNING: Missing artifacts:"
  for artifact in "${missing[@]}"; do
    echo "  - governance/live/$artifact"
  done
  echo ""
  echo "Run '/loop:init' to create missing artifacts."
  echo "Showing status for available artifacts only."
  echo ""
fi
```

---

## Step 2: Parse Artifacts

Read and parse each artifact:

### Parse TARGET.md

```python
# Pseudocode for parsing

def parse_target(filepath):
    content = read_file(filepath)

    # Extract goal (first line after "## Goal")
    goal = extract_section(content, "## Goal")

    # Extract DoD checklist
    dod_section = extract_section(content, "## Definition of Done")
    dod_items = []
    for line in dod_section.split("\n"):
        if match := re.match(r"- \[([ x])\] (.+)", line):
            checked = match.group(1) == "x"
            item = match.group(2)
            dod_items.append({"checked": checked, "item": item})

    dod_complete = sum(1 for item in dod_items if item["checked"])
    dod_total = len(dod_items)
    dod_pct = (dod_complete / dod_total * 100) if dod_total > 0 else 0

    return {
        "goal": goal.strip(),
        "dod_items": dod_items,
        "dod_complete": dod_complete,
        "dod_total": dod_total,
        "dod_pct": dod_pct
    }
```

### Parse BOUNDARY.md

```python
def parse_boundary(filepath):
    content = read_file(filepath)

    # Extract boundary law
    law = extract_section(content, "## The Law")

    # Extract bridge path
    bridge_section = extract_section(content, "## Bridge Definition")
    bridge_match = re.search(r"Module/Path.*?`([^`]+)`", bridge_section)
    bridge = bridge_match.group(1) if bridge_match else "Unknown"

    # Count forbidden dependencies
    forbidden_section = extract_section(content, "## Forbidden Dependencies")
    forbidden_count = len([line for line in forbidden_section.split("\n") if line.strip().startswith("-")])

    # Count temporary exceptions
    exceptions_section = extract_section(content, "## Temporary Exceptions")
    exception_rows = [line for line in exceptions_section.split("\n") if line.startswith("|") and not line.startswith("|-") and "Exception" not in line]
    exception_count = len(exception_rows) - 1 if exception_rows else 0  # -1 for header

    return {
        "law": law.strip(),
        "bridge": bridge,
        "forbidden_count": forbidden_count,
        "exception_count": exception_count
    }
```

### Parse BLOCKERS.md

```python
def parse_blockers(filepath):
    content = read_file(filepath)

    # Extract active blockers
    active_section = extract_section(content, "## Active Blockers")
    blockers = []

    # Find all blocker entries (### BLOCKER-XXX:)
    blocker_pattern = r"### (BLOCKER-\d+): (.+)"
    matches = re.finditer(blocker_pattern, active_section)

    for match in matches:
        blocker_id = match.group(1)
        title = match.group(2)

        # Extract impact (which DoD item it blocks)
        # Look for "Impact: Blocks DoD item"
        impact_match = re.search(rf"{blocker_id}.*?Impact:\*\*\s*(.+?)(?:\n\n|\*\*)", active_section, re.DOTALL)
        impact = impact_match.group(1).strip() if impact_match else "Unknown"

        blockers.append({
            "id": blocker_id,
            "title": title,
            "impact": impact
        })

    # Extract escalations
    escalations_section = extract_section(content, "## Escalations Needed")
    escalation_pattern = r"### (ESCALATION-\d+): (.+)"
    escalation_matches = re.finditer(escalation_pattern, escalations_section)
    escalations = [{"id": m.group(1), "title": m.group(2)} for m in escalation_matches]

    return {
        "blockers": blockers,
        "blocker_count": len(blockers),
        "escalations": escalations,
        "escalation_count": len(escalations)
    }
```

### Parse METRICS.md

```python
def parse_metrics(filepath):
    content = read_file(filepath)

    metrics = []

    # Find metric sections (### Metric N:)
    metric_pattern = r"### Metric \d+: (.+)"
    matches = re.finditer(metric_pattern, content)

    for match in matches:
        name = match.group(1).strip()

        # Extract current, target, delta
        # Look for **Current Value:** [number]
        current_match = re.search(rf"{name}.*?Current Value:\*\*\s*(\d+)", content, re.DOTALL)
        target_match = re.search(rf"{name}.*?Target Value:\*\*\s*(\d+)", content, re.DOTALL)
        delta_match = re.search(rf"{name}.*?Delta:\*\*\s*([+-]?\d+)", content, re.DOTALL)

        current = int(current_match.group(1)) if current_match else None
        target = int(target_match.group(1)) if target_match else None
        delta = int(delta_match.group(1)) if delta_match else 0

        # Determine if moving toward target
        if current is not None and target is not None:
            if target > current:  # Want to increase
                moving_right_direction = delta > 0
            elif target < current:  # Want to decrease
                moving_right_direction = delta < 0
            else:  # At target
                moving_right_direction = True
        else:
            moving_right_direction = None

        metrics.append({
            "name": name,
            "current": current,
            "target": target,
            "delta": delta,
            "moving_right_direction": moving_right_direction
        })

    return {"metrics": metrics}
```

---

## Step 3: Display Status

Format and display the parsed information:

```markdown
═══════════════════════════════════════════════════════
Control Loop Status
═══════════════════════════════════════════════════════

[If convergence mode active:]
⚡ CONVERGENCE MODE ACTIVE ⚡
Zero tolerance for deferral | Escalate after 1 attempt

TARGET: [goal statement (first 80 chars)]
  DoD Progress: [X]/[Y] complete ([pct]%)
  [If < 100%:]
    Incomplete:
    - [ ] [DoD item 1]
    - [ ] [DoD item 2]
    [... up to 5 incomplete items, or "and N more"]

BOUNDARY:
  Law: [boundary law (first 80 chars)]
  Bridge: [bridge path]
  Forbidden: [count] modules
  Exceptions: [count] active [⚠ if > 0]

BLOCKERS: [count] active [⚠ if > 5]
  [If > 0:]
    Top 3 by Impact:
    1. [BLOCKER-id]: [title (first 60 chars)]
       → Blocks: [impact]
    2. [BLOCKER-id]: [title]
       → Blocks: [impact]
    3. [BLOCKER-id]: [title]
       → Blocks: [impact]
  [If > 3:]
    ... and [N] more blockers
  [If 0:]
    ✓ No active blockers

ESCALATIONS: [count] pending [⚠ if > 0]
  [If > 0:]
    1. [ESCALATION-id]: [title]
    2. [ESCALATION-id]: [title]
    [... all escalations]

METRICS:
  [For each metric:]
  [name]: [current] → [target] (Δ [+/-delta]) [✓ | ⚠ | ✗]
    [✓ = moving toward target, ⚠ = stagnant, ✗ = moving away]

[If convergence mode and close to done:]
🎯 APPROACHING COMPLETION 🎯
  DoD: [X]/[Y]
  Blockers: [N]
  Metrics: [N] at/near target

═══════════════════════════════════════════════════════
Recommended Next Action:

[See Step 4 for logic]

═══════════════════════════════════════════════════════
```

---

## Step 4: Recommend Next Action

Based on current state, suggest what user should do next:

### Case 1: Escalations Pending

```markdown
⚠ ESCALATIONS REQUIRE DECISIONS

You have [N] pending escalation(s) blocking progress.

Next:
1. Review governance/live/BLOCKERS.md (Escalations Needed)
2. Make decisions, update file
3. Run /loop:phase to continue
```

### Case 2: Blockers Present, No Escalations

```markdown
→ Ready for Next Phase

Active blockers: [N]
Next blocker: [BLOCKER-id] - [title]

Run: /loop:phase
```

### Case 3: Zero Blockers, DoD Incomplete

```markdown
⚠ MISSING WORK DETECTED

DoD is [X]/[Y] complete but no active blockers.
Work is missing from the queue!

Next:
1. Review governance/live/TARGET.md DoD section
2. For each incomplete item, identify what blocks it
3. Add blockers to governance/live/BLOCKERS.md
4. Run /loop:phase
```

### Case 4: Zero Blockers, DoD Complete

```markdown
✓ WORK COMPLETE - READY TO SHIP

All DoD items complete, zero blockers remaining.

Final Verification:
1. Review governance/PHASE-LOG.md for audit trail
2. Verify metrics at target values
3. Run final smoke tests
4. Archive governance/ for historical record
5. Ship!

Optional:
- Run /loop:status again for confirmation
- Review boundary exceptions (should be empty)
```

### Case 5: Metrics Stagnant or Regressing

```markdown
⚠ METRICS NOT MOVING

[Metric name] has [not changed | moved away from target] in [N] phases.

Possible causes:
- Blocker selection not targeting this metric
- Metric measurement method incorrect
- Truly stuck (needs escalation)

Next:
1. Review governance/live/BLOCKERS.md
2. Ensure blockers cite metric impact
3. Run /loop:phase (Governor should escalate if stuck)
```

### Case 6: High Blocker Count (> 10)

```markdown
⚠ HIGH BLOCKER COUNT

You have [N] active blockers. Recommend prioritization.

Next:
1. Review governance/live/BLOCKERS.md
2. Mark some blockers as lower priority (move to "Deferred" section)
3. Or remove blockers that are no longer relevant
4. Focus on blockers that directly block DoD items
5. Run /loop:phase
```

### Case 7: Convergence Approaching

```markdown
🎯 ENTERING CONVERGENCE ZONE

DoD: [pct]% complete
Blockers: [N] remaining

Consider activating convergence mode:
- Zero tolerance for deferral
- Escalate after N=1 attempt
- Enumerate all remaining work explicitly

Convergence auto-activates at 80%+ DoD completion.

Run: /loop:phase
```

---

## Step 5: Artifact Health Warnings

After displaying status, check for common issues:

### Warning: Artifacts Too Large

```markdown
⚠ ARTIFACT SIZE WARNING

These artifacts exceed 50 lines (recommend < 50 for one-screen view):
- governance/live/BLOCKERS.md: 73 lines
- governance/live/METRICS.md: 58 lines

Recommendation:
- Move resolved blockers to "Recently Eliminated" (keep last 5)
- Trim metric trend history (keep last 5 measurements)
- Archive old details in governance/PHASE-LOG.md
```

### Warning: Stale Artifacts

```markdown
⚠ STALE ARTIFACT WARNING

These artifacts have not been updated recently:
- METRICS.md: Last updated 5 days ago
- BLOCKERS.md: Last updated 3 days ago

Recommendation:
- Run /loop:phase to continue work
- Or review artifacts and update manually if needed
```

### Warning: Broken References

```markdown
⚠ BROKEN REFERENCE WARNING

Found references to non-existent items:
- BLOCKER-005 cited in TARGET.md DoD but not in BLOCKERS.md
- DoD item "All tests pass" cited in BLOCKER-003 but not in TARGET.md

Recommendation:
- Review and fix references manually
- Ensure artifact consistency
```

### Warning: Metric Measurement Failures

```markdown
⚠ METRIC MEASUREMENT WARNING

These metrics could not be measured (command failed):
- Legacy import count: Command `grep -r "legacy" | wc -l` failed

Recommendation:
- Test measurement commands manually
- Update METRICS.md with working commands
- Remove metrics that are no longer relevant
```

---

## Alternative Display Modes

### Compact Mode (Optional)

For quick checks, show minimal output:

```bash
/loop:status --compact
```

Output:

```markdown
DoD: [X]/[Y] ([pct]%) | Blockers: [N] | Escalations: [N] | Next: [action]
```

### Detailed Mode (Optional)

Show full artifact content:

```bash
/loop:status --detailed
```

Includes:
- All DoD items (not just incomplete)
- All blockers (not just top 3)
- Full metric trend history
- Complete boundary exception table

### JSON Mode (Optional)

For integration with other tools:

```bash
/loop:status --json
```

Output:

```json
{
  "target": {
    "goal": "...",
    "dod_complete": 3,
    "dod_total": 7,
    "dod_pct": 42.9
  },
  "boundary": {
    "law": "...",
    "bridge": "src/compat",
    "forbidden_count": 12,
    "exception_count": 1
  },
  "blockers": {
    "active": 4,
    "escalations": 0,
    "list": [...]
  },
  "metrics": [
    {"name": "...", "current": 47, "target": 0, "delta": -5},
    ...
  ],
  "recommendation": "run_phase"
}
```

---

## Error Handling

### Governance Not Initialized

```markdown
ERROR: Governance directory not found

The control loop has not been initialized.

To fix:
Run /loop:init to create governance structure

Then run /loop:status to view state
```

### Artifact Parse Failure

```markdown
ERROR: Cannot parse artifact

File: governance/live/[artifact].md

Possible causes:
- Malformed markdown
- Missing required sections
- Encoding issues

To fix:
1. Open file in editor
2. Check for structural issues (missing headers, etc.)
3. Restore from backup: governance/live.backup-*/
4. Or regenerate with /loop:init (caution: overwrites)
```

### Empty Artifacts

```markdown
WARNING: Empty artifacts detected

These artifacts are empty or nearly empty:
- governance/live/BLOCKERS.md (no active blockers)
- governance/live/METRICS.md (no metrics defined)

This may be intentional if work is complete, or may indicate
initialization issue.

To fix:
- If work is complete: Verify with /loop:status
- If incomplete: Add missing content manually
- Or re-run /loop:init to regenerate
```

---

## Integration Points

**Commands:**
- Before: `/loop:init` creates structure
- Check between phases: `/loop:status`
- Execute work: `/loop:phase`

**Skills:**
- Uses parsing logic similar to `phase-ritual` artifact restatement
- Can use `artifact-templates` for validation

**No agents invoked:** This command is read-only, no execution.

---

## Best Practices

1. **Run frequently** - Check status before each `/loop:phase`
2. **Use for planning** - Identify next blocker before starting phase
3. **Monitor metrics** - Ensure they're moving monotonically
4. **Watch escalations** - Don't let them accumulate
5. **Validate artifacts** - Check for warnings and fix issues

---

## See Also

- `commands/init.md` - Initialize governance structure
- `commands/phase.md` - Execute work phase
- `agents/governor.md` - Governor uses similar parsing logic
- `skills/phase-ritual/SKILL.md` - Artifact restatement step
- `skills/artifact-templates/SKILL.md` - Artifact structure reference
