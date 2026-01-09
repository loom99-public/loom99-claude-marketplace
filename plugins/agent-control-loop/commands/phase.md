---
argument-hint: (none)
description: Execute one phase of the control loop. Invokes Governor agent to run phase ritual, select blocker, plan work, delegate execution, and update artifacts.
---

# /loop:phase - Execute Phase

Runs the Governor agent through one complete phase of the minimal control loop. This is the primary command for making progress on convergent, high-risk work.

## Prerequisites

**Required:**
- `governance/live/` directory exists (created by `/loop:init`)
- All 4 artifacts present: TARGET.md, BOUNDARY.md, BLOCKERS.md, METRICS.md

**If missing:** Display helpful error and suggest `/loop:init`

## What This Command Does

1. Verifies governance structure exists
2. Spawns Governor agent
3. Governor executes 5-step phase ritual:
   - Step 1: Restate artifacts (ground in reality)
   - Step 2: Select single blocker (force focus)
   - Step 3: Generate phase plan (3-7 executable steps)
   - Step 4: Delegate execution (to implementer or self)
   - Step 5: Record outcome (update artifacts)
4. Displays phase summary
5. Suggests next action

## Step 1: Pre-Flight Checks

Before spawning Governor, verify prerequisites:

### Check 1: Governance Directory Exists

```bash
if [ ! -d "governance/live" ]; then
  echo "ERROR: Governance directory not found."
  echo ""
  echo "Run '/loop:init' first to bootstrap the control loop."
  exit 1
fi
```

### Check 2: Required Artifacts Present

```bash
required_files=(
  "governance/live/TARGET.md"
  "governance/live/BOUNDARY.md"
  "governance/live/BLOCKERS.md"
  "governance/live/METRICS.md"
)

missing=()
for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    missing+=("$file")
  fi
done

if [ ${#missing[@]} -gt 0 ]; then
  echo "ERROR: Missing required artifacts:"
  for file in "${missing[@]}"; do
    echo "  - $file"
  done
  echo ""
  echo "Run '/loop:init' to create missing files."
  exit 1
fi
```

### Check 3: Artifacts Are Readable

```bash
# Attempt to read each artifact
for file in "${required_files[@]}"; do
  if ! cat "$file" > /dev/null 2>&1; then
    echo "ERROR: Cannot read $file (permissions or corruption)"
    exit 1
  fi
done
```

**If all checks pass:** Proceed to Step 2

**If any check fails:** Display error, suggest fix, exit

---

## Step 2: Spawn Governor Agent

Invoke the Governor agent with the phase ritual task:

```markdown
=== SPAWNING GOVERNOR AGENT ===

Task: Execute one phase of the minimal control loop

Context:
- Governance artifacts: governance/live/
- Phase log: governance/PHASE-LOG.md
- Working directory: [current directory]

Instructions:
You are executing a phase of the minimal control loop. Follow the
phase-ritual skill exactly:

1. Restate all 4 artifacts (TARGET, BOUNDARY, BLOCKERS, METRICS)
2. Select single highest-value blocker
3. Generate 3-7 step plan with verifications
4. Execute plan (delegate if appropriate)
5. Record outcome and update artifacts

See agents/governor.md for your behavioral rules.
See skills/phase-ritual/SKILL.md for ritual procedure.

Critical Reminders:
- Work only justified by blocker or DoD item
- No deferral (escalate instead)
- No resurrection (respect BOUNDARY.md)
- Evidence required for all claims
- Metrics must move monotonically

Begin phase ritual now.

=== END GOVERNOR SPAWN ===
```

**Governor will:**
- Read artifacts
- Execute phase ritual
- Return control when phase complete or escalation needed

---

## Step 3: Monitor Governor Execution

While Governor is running, watch for:

### Normal Completion

Governor completes all 5 ritual steps and returns summary:

```markdown
OUTCOME: ELIMINATED | TRANSFORMED | ESCALATED

BLOCKER: BLOCKER-[id]
[... evidence and details ...]

ARTIFACTS UPDATED:
[... list of changes ...]

NEXT: [recommended action]
```

**Action:** Proceed to Step 4 (display summary)

### Escalation Required

Governor encounters decision point and escalates:

```markdown
OUTCOME: ESCALATED

ESCALATION: BLOCKER-[id]

TRIGGER: [Why escalating]

OPTIONS:
1. [Option A]
   [... details ...]
2. [Option B]
   [... details ...]

RECOMMENDED: [Option X]

DECISION REQUIRED
```

**Action:**
- Display escalation to user
- Await user decision
- Update BLOCKERS.md with decision
- Optionally continue to next blocker if decision allows

### Error/Stuck

Governor fails unexpectedly (e.g., cannot measure metric, artifact corruption):

```markdown
ERROR: [description]

CONTEXT: [what was being attempted]

SUGGESTED FIX: [how to resolve]
```

**Action:**
- Display error to user
- Suggest fixes
- Do not update artifacts (preserve state)
- Exit gracefully

---

## Step 4: Display Phase Summary

After Governor completes successfully, show user-friendly summary:

```markdown
═══════════════════════════════════════════════════════
Phase Complete
═══════════════════════════════════════════════════════

Outcome: [ELIMINATED | TRANSFORMED | ESCALATED | FAILED]

Blocker Addressed:
  BLOCKER-[id]: [description]

[If ELIMINATED:]
✓ Blocker Eliminated
  Method: [brief approach description]
  Evidence:
  - [key evidence 1]
  - [key evidence 2]

[If TRANSFORMED:]
⟳ Blocker Transformed
  New Form: [updated description]
  Reason: [why transformation occurred]
  Evidence: [new evidence]

[If ESCALATED:]
⚠ Escalation Required
  Reason: [trigger]
  Options: [count] presented
  See: governance/live/BLOCKERS.md (Escalations Needed section)

[If FAILED:]
✗ Phase Failed
  Reason: [why verification failed]
  Attempts: [N/M]
  [If attempts < threshold:]
    Retry: Available
  [If attempts >= threshold:]
    Status: Auto-escalated

Metrics Delta:
  [Metric 1]: [old] → [new] ([+/- delta]) [✓ or ⚠]
  [Metric 2]: [old] → [new] ([+/- delta]) [✓ or ⚠]
  [Metric 3]: [old] → [new] ([+/- delta]) [✓ or ⚠]

DoD Progress:
  [X]/[Y] complete ([+N this phase])

Active Blockers Remaining: [count]

═══════════════════════════════════════════════════════
Next Action:

[If blockers remaining and no escalation:]
  → Run /loop:phase to attack next blocker

[If escalation needed:]
  → Review escalation in governance/live/BLOCKERS.md
  → Make decision, update file, then run /loop:phase

[If no blockers and DoD incomplete:]
  ⚠ Zero blockers but DoD not complete - work is missing!
  → Review governance/live/TARGET.md
  → Add missing blockers to BLOCKERS.md
  → Run /loop:phase

[If no blockers and DoD complete:]
  ✓ ALL WORK COMPLETE
  → Run /loop:status for final verification
  → Review governance/PHASE-LOG.md for audit trail

═══════════════════════════════════════════════════════
```

---

## Step 5: Suggest Next Action

Based on current state, recommend what user should do:

### Case 1: Normal Progress (blocker eliminated, more remain)

```markdown
Recommended: /loop:phase

Continue momentum. Next blocker: BLOCKER-[id]
```

### Case 2: Escalation Created

```markdown
Recommended: Review escalation and decide

1. Read governance/live/BLOCKERS.md (Escalations Needed section)
2. Consider options presented
3. Make decision and update file
4. Run /loop:phase to continue

Or: Run /loop:phase to work on different blocker while deciding
```

### Case 3: Convergence Approaching (< 3 blockers left)

```markdown
Recommended: Enter convergence mode

You have [N] blockers remaining and [X]/[Y] DoD complete.

Consider activating convergence mode:
- Zero tolerance for deferral
- Aggressive escalation (N=1 attempt)
- Enumerate all remaining work

Run /loop:phase (convergence mode will auto-activate at 80%+ DoD)
```

### Case 4: Metrics Stagnant

```markdown
Warning: Metrics not moving

[Metric X] has not changed in [N] phases.

Recommended actions:
1. Review BLOCKERS.md - is blocker selection targeting metrics?
2. Check metric measurement method - is it working?
3. Escalate if truly stuck

Run /loop:status to review full state
```

### Case 5: Completion

```markdown
Recommended: Final verification and ship

All blockers eliminated, DoD 100% complete!

Next steps:
1. Run /loop:status for final verification
2. Review governance/PHASE-LOG.md for audit trail
3. Archive governance/ directory for historical record
4. Ship!
```

---

## Error Handling

### Governance Directory Missing

```markdown
ERROR: Governance directory not found

The control loop has not been initialized.

To fix:
1. Run /loop:init to create governance structure
2. Then run /loop:phase to begin work

Alternative:
If governance/ exists elsewhere, ensure you're in the right directory.
```

### Artifact Corruption

```markdown
ERROR: Artifact is corrupted or unreadable

File: governance/live/[artifact].md

Possible causes:
- File permissions issue
- Merge conflict markers present
- Invalid YAML frontmatter
- File encoding issue

To fix:
1. Check file permissions: ls -l governance/live/
2. Open file in editor and look for corruption
3. Restore from backup: governance/live.backup-*/
4. Or regenerate with /loop:init (caution: overwrites)
```

### Governor Fails to Select Blocker

```markdown
ERROR: No blockers available but DoD incomplete

Governor could not select a blocker because BLOCKERS.md is empty,
but TARGET.md shows DoD is only [X]/[Y] complete.

This means work is missing from the blocker queue.

To fix:
1. Review governance/live/TARGET.md DoD section
2. For each incomplete DoD item, identify what blocks it
3. Add blockers to governance/live/BLOCKERS.md
4. Run /loop:phase again

Example blocker format:
### BLOCKER-00X: [Short identifier]
**Observable Failure:** [Exact error or failing test]
**Impact:** Blocks DoD item "[which item]"
**Evidence:** [Link, file:line, test name]
```

### Metric Measurement Fails

```markdown
ERROR: Cannot measure metric

Metric: [name]
Command: [command that failed]
Error: [error message]

Possible causes:
- Measurement command is incorrect
- Required tools not installed
- Files being measured no longer exist
- Working directory changed

To fix:
1. Test command manually: [command]
2. Update measurement method in governance/live/METRICS.md
3. Run /loop:phase again

If metric is no longer relevant:
1. Remove from METRICS.md (keep 2-4 metrics)
2. Add different metric that tracks progress
```

### Boundary Violation Attempted

```markdown
ERROR: Boundary violation detected

Governor attempted to import forbidden module outside bridge.

File: [file that would violate]
Forbidden import: [module]
Boundary law: [from BOUNDARY.md]

The Governor should have escalated instead of violating the boundary.

To fix:
1. Review governance/live/BOUNDARY.md
2. If import is necessary, add to Temporary Exceptions table
3. Or expand bridge surface (requires justification)
4. Run /loop:phase again
```

---

## Advanced Usage

### Convergence Mode

When DoD is ~80% complete, convergence mode auto-activates:

- N=1 attempt threshold (escalate faster)
- No new features (only blocker elimination)
- Aggressive blocker enumeration
- Zero tolerance for deferral

**Manual activation:**

Edit `governance/live/TARGET.md`, add:

```markdown
## Convergence Mode

ACTIVE: yes
Activated: [timestamp]

Rules:
- Escalate after N=1 attempt (not N=2)
- No new features or scope expansion
- Enumerate all remaining work explicitly
```

### Batch Phases

For rapid iteration on multiple blockers:

```bash
# Run 3 phases in sequence (if no escalations)
for i in {1..3}; do
  /loop:phase || break
done
```

**Caution:** Only do this if blockers are well-understood and low-risk.

### Custom Governor Behavior

Advanced users can override Governor defaults in CLAUDE.md:

```markdown
## agent-control-loop configuration

governor:
  escalation_threshold: 3  # default: 2
  convergence_dod_pct: 75  # default: 80
  max_steps_per_plan: 5    # default: 7
```

---

## Integration Points

**Agents:**
- `governor` - Primary agent invoked by this command
- (Optional) `iterative-implementer` - Delegated execution if Governor chooses

**Skills:**
- `phase-ritual` - Governor uses this for phase execution
- `artifact-templates` - Validates artifacts during phase

**Commands:**
- Before: `/loop:init` creates governance structure
- After: `/loop:status` to review state
- Related: `/loop:status` can be run between phases

---

## Best Practices

1. **Run frequently** - Phases should be small (1-2 hours max)
2. **Review escalations quickly** - Blocked Governor means blocked progress
3. **Trust the ritual** - Don't skip artifact restatement
4. **One blocker at a time** - Resist urge to parallelize
5. **Update artifacts immediately** - Governor does this; verify it happened
6. **Check metrics trend** - Are they moving monotonically?

---

## See Also

- `agents/governor.md` - Governor agent specification
- `skills/phase-ritual/SKILL.md` - Phase ritual procedure
- `commands/status.md` - Review governance state
- `commands/init.md` - Initialize governance
- `docs/_now/control-loop-system/CONTEXT-PRIME.md` - Full system spec
