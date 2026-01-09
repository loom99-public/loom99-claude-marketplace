# Scripts: Deterministic Operations

This document defines all scripts in the agent-control-loop plugin. Scripts handle deterministic operations that must be reliable and repeatable.

---

## Design Principle: Scripts Are Reliable

Scripts handle operations where determinism matters:
- File creation with exact structure
- Running measurement commands
- Scanning for patterns
- Archiving and moving files
- Validation checks

Skills invoke scripts. Scripts never invoke agents.

```
Agent → Skill → Script
         │        │
         │        └─ Bash (deterministic)
         └─ Prompt (adaptive)
```

---

## Script Summary

| Script | Purpose | Called By |
|--------|---------|-----------|
| init-governance.sh | Create governance/ directory structure | artifact-io skill |
| measure-metrics.sh | Execute metric measurement commands | metric-measurement skill |
| validate-boundary.sh | Check imports against boundary law | boundary-guard hook |
| scan-boundaries.sh | Detect legacy/new code boundaries | Governor (init mode) |
| regenerate-compressed.sh | Generate A₀/B₀ from live artifacts | compressed-artifacts skill |
| archive-slice.sh | Archive completed work | design-lifecycle skill |
| validate-artifact.sh | Validate artifact structure | artifact-io skill |

---

## init-governance.sh

**Purpose:** Create the `governance/` directory structure.

**Location:** `scripts/init-governance.sh`

```bash
#!/bin/bash
# scripts/init-governance.sh
# Creates governance directory structure for minimal control loop

set -e

# Default values
GOAL="${1:-TBD}"
BRIDGE="${2:-none}"
FORBIDDEN="${3:-none}"

# Create directory structure
mkdir -p governance/live
mkdir -p governance/compressed/B0-playbooks
mkdir -p governance/roadmap/slices
mkdir -p governance/completed/slices

# Timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")

# Create TARGET.md
cat > governance/live/TARGET.md << EOF
# Target End State

## Goal
$GOAL

## Non-Goals
- TBD (define during first phase)

## Target Shape
- TBD (define during first phase)

## Definition of Done

### Build & Test
- [ ] System builds without errors
- [ ] All must-pass tests passing
- [ ] No forbidden legacy imports (outside bridge)

### Project-Specific
- [ ] TBD

## Convergence Mode
ACTIVE: no

## Last Updated
$TIMESTAMP - Initial creation
EOF

# Create BOUNDARY.md
cat > governance/live/BOUNDARY.md << EOF
# Boundary Law

## The Law
New code must not import or call legacy code except through the bridge.

## Bridge Definition

**Module/Path:** \`$BRIDGE\`

**Allowed Surface:**
- TBD (define during first phase)

**Bridge Constraints:**
- Bridge must be stateless
- Bridge may not expose legacy data structures directly
- Bridge surface must shrink toward zero

## Forbidden Dependencies

**Legacy Modules (no direct imports):**
- $FORBIDDEN

## Temporary Exceptions

| Exception | Reason | Expires When | Blocker |
|-----------|--------|--------------|---------|
| (none) | - | - | - |

## Enforcement
- [ ] CI linter checks imports
- [ ] Pre-tool hook blocks forbidden writes
- [ ] Code review checklist

## Last Updated
$TIMESTAMP - Initial creation
EOF

# Create BLOCKERS.md
cat > governance/live/BLOCKERS.md << EOF
# Blockers

## Active Blockers

### BLOCKER-001: Enumerate all blockers
**Observable Failure:** Blocker queue is incomplete

**Impact:** Blocks DoD item "accurate progress tracking"

**Evidence:**
- Bootstrap blocker
- First phase should enumerate all known obstacles

**Attempts:** 0 / 2

**Last Attempt:** $TIMESTAMP - Initial creation

---

## Escalations Needed

(none)

---

## Recently Eliminated

| ID | Eliminated | Method | Outcome |
|----|------------|--------|---------|
| - | - | - | - |

## Last Updated
$TIMESTAMP - Initial creation
EOF

# Create METRICS.md
cat > governance/live/METRICS.md << EOF
# Convergence Metrics

## Metric 1: Active Blockers

**Definition:** Count of active blockers

**Measurement:**
\`\`\`bash
grep -c "^### BLOCKER-" governance/live/BLOCKERS.md
\`\`\`

**Values:**
- Current: 1
- Target: 0
- Delta: -1 to go

**Trend:**
- $TIMESTAMP: 1 (baseline)

**Escalation Threshold:** No progress after 3 phases

---

## Summary

| Metric | Current | Target | Delta | Status |
|--------|---------|--------|-------|--------|
| Active Blockers | 1 | 0 | -1 | ⚠ |

## Last Updated
$TIMESTAMP - Initial creation
EOF

# Create DESIGN_LINKS.md
cat > governance/live/DESIGN_LINKS.md << EOF
# Design Links

## Canonical Design Documents
- (none yet)

## Active Designs
| ID | Title | Status | SPEC Location |
|----|-------|--------|---------------|
| - | - | - | - |

## Precedence Rule
If design/current conflicts with governance/live, **governance/live wins** until this file is updated.

## Last Updated
$TIMESTAMP - Initial creation
EOF

# Create PHASE-LOG.md
cat > governance/PHASE-LOG.md << EOF
# Phase Log

---

## Phase 0 - Initialization - $TIMESTAMP

**Action:** Governance structure initialized

**Artifacts Created:**
- TARGET.md (Goal: $GOAL)
- BOUNDARY.md (Bridge: $BRIDGE)
- BLOCKERS.md (1 initial blocker)
- METRICS.md (1 metric)

**Next:** Run \`/loop:phase\` to begin work

---
EOF

# Create HISTORY.md
cat > governance/HISTORY.md << EOF
# Decision History

---

## $TIMESTAMP - Control Loop Initialized

**Context:** Beginning minimal control loop for project

**Decision:** Initialize governance structure

**Rationale:** Bootstrap convergence-driven workflow

**Impact:**
- TARGET: Created with goal "$GOAL"
- BOUNDARY: Created with bridge "$BRIDGE"
- METRICS: 1 metric established

---
EOF

echo "Governance directory initialized at governance/"
echo "Next: Run /loop:phase to begin work"
```

**Arguments:**
- `$1` — Goal statement
- `$2` — Bridge path
- `$3` — Forbidden patterns (comma-separated)

---

## measure-metrics.sh

**Purpose:** Execute metric measurement commands and return values.

**Location:** `scripts/measure-metrics.sh`

```bash
#!/bin/bash
# scripts/measure-metrics.sh
# Measures all metrics defined in METRICS.md

set -e

METRICS_FILE="governance/live/METRICS.md"

if [ ! -f "$METRICS_FILE" ]; then
  echo "ERROR: METRICS.md not found"
  exit 1
fi

# Extract and run each measurement command
# Format: ```bash\n[command]\n```

CURRENT_METRIC=""
IN_MEASUREMENT=false

while IFS= read -r line; do
  # Detect metric header
  if [[ "$line" =~ ^##\ Metric\ [0-9]+:\ (.+)$ ]]; then
    CURRENT_METRIC="${BASH_REMATCH[1]}"
  fi

  # Start of measurement block
  if [[ "$line" == '```bash' ]] && [ -n "$CURRENT_METRIC" ]; then
    IN_MEASUREMENT=true
    COMMAND=""
    continue
  fi

  # End of measurement block
  if [[ "$line" == '```' ]] && [ "$IN_MEASUREMENT" = true ]; then
    IN_MEASUREMENT=false
    if [ -n "$COMMAND" ]; then
      # Execute and capture result
      RESULT=$(eval "$COMMAND" 2>/dev/null || echo "ERROR")
      echo "$CURRENT_METRIC: $RESULT"
    fi
    CURRENT_METRIC=""
    continue
  fi

  # Accumulate command
  if [ "$IN_MEASUREMENT" = true ]; then
    COMMAND="$line"
  fi
done < "$METRICS_FILE"
```

**Output:** Metric name and measured value for each metric

**Example Output:**
```
Active Blockers: 3
Legacy Imports: 47
Failing Tests: 12
```

---

## validate-boundary.sh

**Purpose:** Check if a file/content violates boundary law.

**Location:** `scripts/validate-boundary.sh`

```bash
#!/bin/bash
# scripts/validate-boundary.sh
# Checks for boundary violations in code

set -e

FILE_PATH="$1"
CONTENT="$2"  # Optional: content to check (if not provided, reads file)

BOUNDARY_FILE="governance/live/BOUNDARY.md"

if [ ! -f "$BOUNDARY_FILE" ]; then
  echo "No boundary file found, skipping check"
  exit 0
fi

# Extract forbidden patterns
FORBIDDEN=$(grep -A50 "^## Forbidden Dependencies" "$BOUNDARY_FILE" | \
  grep "^\- " | \
  sed 's/^- //' | \
  sed 's/`//g' | \
  head -20)

# Extract bridge path
BRIDGE=$(grep "^**Module/Path:**" "$BOUNDARY_FILE" | \
  sed 's/.*`\([^`]*\)`.*/\1/')

# Check if file is in bridge (allowed)
if [ -n "$BRIDGE" ] && [ "$BRIDGE" != "none" ]; then
  if echo "$FILE_PATH" | grep -q "$BRIDGE"; then
    echo "File is in bridge, allowed"
    exit 0
  fi
fi

# Get content to check
if [ -n "$CONTENT" ]; then
  CHECK_CONTENT="$CONTENT"
elif [ -f "$FILE_PATH" ]; then
  CHECK_CONTENT=$(cat "$FILE_PATH")
else
  echo "No content to check"
  exit 0
fi

# Check for violations
VIOLATIONS=()
for PATTERN in $FORBIDDEN; do
  if echo "$CHECK_CONTENT" | grep -q "$PATTERN"; then
    VIOLATIONS+=("$PATTERN")
  fi
done

if [ ${#VIOLATIONS[@]} -gt 0 ]; then
  echo "BOUNDARY VIOLATION DETECTED"
  echo ""
  echo "File: $FILE_PATH"
  echo "Forbidden imports found:"
  for V in "${VIOLATIONS[@]}"; do
    echo "  - $V"
  done
  echo ""
  echo "Bridge: $BRIDGE"
  echo "Use bridge for legacy access, or escalate for exception."
  exit 1
fi

echo "No boundary violations"
exit 0
```

**Arguments:**
- `$1` — File path
- `$2` — Content to check (optional)

**Exit Codes:**
- 0 = No violation
- 1 = Violation detected

---

## scan-boundaries.sh

**Purpose:** Detect potential legacy/new code boundaries in repository.

**Location:** `scripts/scan-boundaries.sh`

```bash
#!/bin/bash
# scripts/scan-boundaries.sh
# Scans repository for potential architecture boundaries

set -e

echo "Scanning for potential boundaries..."
echo ""

# 1. Directory structure patterns
echo "=== Directory Patterns ==="
LEGACY_DIRS=$(find . -type d -maxdepth 4 2>/dev/null | \
  grep -iE "(legacy|old|deprecated|v1|compat)" | \
  head -10)

if [ -n "$LEGACY_DIRS" ]; then
  echo "Potential legacy directories:"
  echo "$LEGACY_DIRS" | while read dir; do
    COUNT=$(find "$dir" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "  $dir ($COUNT files)"
  done
else
  echo "  No obvious legacy directories found"
fi
echo ""

# 2. Import patterns (for JS/TS projects)
echo "=== Import Patterns ==="
if [ -d "src" ]; then
  TOP_IMPORTS=$(grep -rh "^import.*from" src --include="*.ts" --include="*.js" 2>/dev/null | \
    sed "s/.*from ['\"]\\([^'\"]*\\)['\"].*/\\1/" | \
    grep "^\\.\\|^@" | \
    sort | uniq -c | sort -rn | head -10)

  if [ -n "$TOP_IMPORTS" ]; then
    echo "Most common internal imports:"
    echo "$TOP_IMPORTS"
  fi
fi
echo ""

# 3. Bridge/adapter candidates
echo "=== Bridge Candidates ==="
BRIDGE_DIRS=$(find . -type d -maxdepth 4 2>/dev/null | \
  grep -iE "(adapter|bridge|compat|shim|wrapper)" | \
  head -5)

if [ -n "$BRIDGE_DIRS" ]; then
  echo "Potential bridge modules:"
  echo "$BRIDGE_DIRS"
else
  echo "  No obvious bridge directories found"
fi
echo ""

# 4. Package.json dependencies (if exists)
echo "=== Package Dependencies ==="
if [ -f "package.json" ]; then
  LEGACY_DEPS=$(grep -iE "(legacy|old|deprecated)" package.json 2>/dev/null | head -5)
  if [ -n "$LEGACY_DEPS" ]; then
    echo "Potentially legacy dependencies:"
    echo "$LEGACY_DEPS"
  else
    echo "  No obviously legacy dependencies"
  fi
fi
echo ""

echo "=== Scan Complete ==="
echo "Review above and select appropriate boundary for your migration."
```

**Output:** Report of detected patterns and candidates

---

## regenerate-compressed.sh

**Purpose:** Generate compressed A₀ and B₀ artifacts from live artifacts.

**Location:** `scripts/regenerate-compressed.sh`

```bash
#!/bin/bash
# scripts/regenerate-compressed.sh
# Regenerates compressed artifacts from governance/live/

set -e

LIVE_DIR="governance/live"
COMPRESSED_DIR="governance/compressed"

# Validate live artifacts exist
for file in TARGET.md BOUNDARY.md BLOCKERS.md METRICS.md; do
  if [ ! -f "$LIVE_DIR/$file" ]; then
    echo "ERROR: Missing $LIVE_DIR/$file"
    exit 1
  fi
done

mkdir -p "$COMPRESSED_DIR/B0-playbooks"

# Extract fields
GOAL=$(grep -A1 "^## Goal" "$LIVE_DIR/TARGET.md" | tail -1 | head -c 100)
LAW=$(grep -A1 "^## The Law" "$LIVE_DIR/BOUNDARY.md" | tail -1 | head -c 100)
BLOCKER_COUNT=$(grep -c "^### BLOCKER-" "$LIVE_DIR/BLOCKERS.md" 2>/dev/null || echo "0")

DOD_TOTAL=$(grep -c "^\- \[ \]" "$LIVE_DIR/TARGET.md" 2>/dev/null || echo "0")
DOD_COMPLETE=$(grep -c "^\- \[x\]" "$LIVE_DIR/TARGET.md" 2>/dev/null || echo "0")
DOD_TOTAL=$((DOD_TOTAL + DOD_COMPLETE))

if grep -q "ACTIVE: yes" "$LIVE_DIR/TARGET.md"; then
  CONVERGENCE="yes"
else
  CONVERGENCE="no"
fi

# Generate A0-contract.md
cat > "$COMPRESSED_DIR/A0-contract.md" << EOF
# Always-On Contract

You are operating under the minimal control loop.

## Hard Rules

1. **Work justified by blocker or DoD.** Never work on anything not in BLOCKERS.md or TARGET.md DoD.
2. **No deferral.** If stuck, escalate with options. Never "handle later."
3. **No resurrection.** Never reintroduce legacy code outside bridge. If tempted, escalate.
4. **Boundary law absolute.** $LAW
5. **Metrics move monotonically.** Each phase moves at least one metric. Stagnation = escalate.
6. **Evidence required.** Every claim cites observable fact: test output, metric value, error message.
7. **Single blocker per phase.** No parallelization. Force focus.
8. **Update artifacts immediately.** Same phase, not deferred.

## Current State
- Goal: $GOAL
- Blockers: $BLOCKER_COUNT active
- DoD Progress: $DOD_COMPLETE/$DOD_TOTAL complete
- Convergence Mode: $CONVERGENCE

## Escalation Threshold
Normal: N=2 attempts | Convergence: N=1 attempt
EOF

echo "Generated $COMPRESSED_DIR/A0-contract.md"

# Generate playbooks based on goal keywords
GOAL_LOWER=$(echo "$GOAL" | tr '[:upper:]' '[:lower:]')

# Migration playbook
if echo "$GOAL_LOWER" | grep -qE "migrat|move|port"; then
  cat > "$COMPRESSED_DIR/B0-playbooks/migration.md" << 'EOF'
# Playbook: Migration

**Active when:** Goal involves migrating from legacy to new

## Pre-Phase Checklist
- [ ] Boundary law understood
- [ ] Bridge surface documented
- [ ] Legacy imports baseline measured

## During Phase
- If test fails after removing legacy: migrate test, don't resurrect
- If new code needs legacy: use bridge only
- If bridge needs expansion: escalate

## Post-Phase Checklist
- [ ] Legacy import count decreased (or justified)
- [ ] No new bridge surface added (or justified)
- [ ] No resurrection occurred
EOF
  echo "Generated migration playbook"
fi

# Refactor playbook
if echo "$GOAL_LOWER" | grep -qE "refactor|restructur|reorganiz"; then
  cat > "$COMPRESSED_DIR/B0-playbooks/refactor.md" << 'EOF'
# Playbook: Refactor

**Active when:** Goal involves restructuring without behavior change

## Pre-Phase Checklist
- [ ] All tests passing before change
- [ ] Behavior contract documented

## During Phase
- Every change must be behavior-preserving
- Tests must stay green after each step
- If tests fail: roll back, understand, retry

## Post-Phase Checklist
- [ ] All tests still passing
- [ ] Coupling metrics improved (or justified)
- [ ] No new technical debt introduced
EOF
  echo "Generated refactor playbook"
fi

# Feature playbook
if echo "$GOAL_LOWER" | grep -qE "feature|add|implement|build|create"; then
  cat > "$COMPRESSED_DIR/B0-playbooks/feature.md" << 'EOF'
# Playbook: Feature

**Active when:** Goal involves adding new functionality

## Pre-Phase Checklist
- [ ] Feature scope defined in TARGET
- [ ] Acceptance criteria in DoD
- [ ] No legacy entanglement required

## During Phase
- Build incrementally with verification at each step
- If legacy code needed: escalate, don't couple directly
- Keep feature isolated until integration point

## Post-Phase Checklist
- [ ] Feature tests passing
- [ ] Integration tests passing
- [ ] No boundary violations
EOF
  echo "Generated feature playbook"
fi

# Create playbook index
cat > "$COMPRESSED_DIR/B0-playbooks/index.md" << EOF
# Available Playbooks

Generated from goal: $GOAL

| Playbook | Active |
|----------|--------|
EOF

for pb in "$COMPRESSED_DIR/B0-playbooks"/*.md; do
  if [ "$(basename "$pb")" != "index.md" ]; then
    NAME=$(basename "$pb" .md)
    echo "| $NAME | check goal keywords |" >> "$COMPRESSED_DIR/B0-playbooks/index.md"
  fi
done

echo ""
echo "Compressed artifacts regenerated successfully."
```

---

## archive-slice.sh

**Purpose:** Archive a completed slice of work.

**Location:** `scripts/archive-slice.sh`

```bash
#!/bin/bash
# scripts/archive-slice.sh
# Archives a completed slice to governance/completed/

set -e

SLICE_ID="$1"
OUTCOME="$2"

if [ -z "$SLICE_ID" ]; then
  echo "Usage: archive-slice.sh <slice-id> [outcome]"
  exit 1
fi

TIMESTAMP=$(date +"%Y-%m-%d")
SOURCE_DIR="governance/roadmap/slices/$SLICE_ID"
DEST_DIR="governance/completed/slices/${SLICE_ID}__${TIMESTAMP}"

if [ ! -d "$SOURCE_DIR" ]; then
  echo "ERROR: Source slice not found: $SOURCE_DIR"
  exit 1
fi

# Create destination
mkdir -p "$DEST_DIR"

# Copy slice files
cp -r "$SOURCE_DIR"/* "$DEST_DIR/"

# Create summary
cat > "$DEST_DIR/summary.md" << EOF
# Completed: $SLICE_ID

## Completed
$(date +"%Y-%m-%d %H:%M")

## Outcome
${OUTCOME:-Completed successfully}

## Original Slice
See slice.md in this directory

## Archived From
$SOURCE_DIR

---
EOF

# Remove from roadmap
rm -rf "$SOURCE_DIR"

# Update roadmap index
ROADMAP_INDEX="governance/roadmap/index.md"
if [ -f "$ROADMAP_INDEX" ]; then
  sed -i.bak "/$SLICE_ID/d" "$ROADMAP_INDEX"
  rm -f "${ROADMAP_INDEX}.bak"
fi

echo "Archived $SLICE_ID to $DEST_DIR"
echo "Removed from roadmap"
```

---

## validate-artifact.sh

**Purpose:** Validate artifact structure against template.

**Location:** `scripts/validate-artifact.sh`

```bash
#!/bin/bash
# scripts/validate-artifact.sh
# Validates artifact structure

set -e

ARTIFACT="$1"
FILE_PATH="governance/live/$ARTIFACT"

if [ ! -f "$FILE_PATH" ]; then
  echo "ERROR: File not found: $FILE_PATH"
  exit 1
fi

ERRORS=()
WARNINGS=()

# Count lines
LINE_COUNT=$(wc -l < "$FILE_PATH" | tr -d ' ')
if [ "$LINE_COUNT" -gt 50 ]; then
  WARNINGS+=("File has $LINE_COUNT lines (recommend < 50)")
fi

# Validate based on artifact type
case "$ARTIFACT" in
  TARGET.md)
    # Check required sections
    grep -q "^## Goal" "$FILE_PATH" || ERRORS+=("Missing ## Goal section")
    grep -q "^## Non-Goals" "$FILE_PATH" || ERRORS+=("Missing ## Non-Goals section")
    grep -q "^## Target Shape" "$FILE_PATH" || ERRORS+=("Missing ## Target Shape section")
    grep -q "^## Definition of Done" "$FILE_PATH" || ERRORS+=("Missing ## Definition of Done section")
    grep -q "^## Last Updated" "$FILE_PATH" || ERRORS+=("Missing ## Last Updated section")

    # Check DoD has items
    DOD_COUNT=$(grep -c "^\- \[" "$FILE_PATH" 2>/dev/null || echo "0")
    if [ "$DOD_COUNT" -lt 3 ]; then
      WARNINGS+=("DoD has only $DOD_COUNT items (recommend >= 3)")
    fi
    ;;

  BOUNDARY.md)
    grep -q "^## The Law" "$FILE_PATH" || ERRORS+=("Missing ## The Law section")
    grep -q "^## Bridge Definition" "$FILE_PATH" || ERRORS+=("Missing ## Bridge Definition section")
    grep -q "^## Forbidden Dependencies" "$FILE_PATH" || ERRORS+=("Missing ## Forbidden Dependencies section")
    grep -q "^## Last Updated" "$FILE_PATH" || ERRORS+=("Missing ## Last Updated section")
    ;;

  BLOCKERS.md)
    grep -q "^## Active Blockers" "$FILE_PATH" || ERRORS+=("Missing ## Active Blockers section")
    grep -q "^## Escalations Needed" "$FILE_PATH" || ERRORS+=("Missing ## Escalations Needed section")
    grep -q "^## Last Updated" "$FILE_PATH" || ERRORS+=("Missing ## Last Updated section")

    # Check blocker format
    while IFS= read -r line; do
      if [[ "$line" =~ ^###\ BLOCKER- ]]; then
        BLOCKER_ID=$(echo "$line" | sed 's/### //')
        # Check for required fields in next 20 lines
        NEXT_LINES=$(grep -A20 "^### $BLOCKER_ID" "$FILE_PATH" | head -20)
        echo "$NEXT_LINES" | grep -q "Observable Failure" || WARNINGS+=("$BLOCKER_ID missing Observable Failure")
        echo "$NEXT_LINES" | grep -q "Impact" || WARNINGS+=("$BLOCKER_ID missing Impact")
        echo "$NEXT_LINES" | grep -q "Evidence" || WARNINGS+=("$BLOCKER_ID missing Evidence")
      fi
    done < "$FILE_PATH"
    ;;

  METRICS.md)
    grep -q "^## Metric" "$FILE_PATH" || ERRORS+=("Missing metrics (need at least 1)")
    grep -q "^## Last Updated" "$FILE_PATH" || ERRORS+=("Missing ## Last Updated section")

    METRIC_COUNT=$(grep -c "^## Metric" "$FILE_PATH" 2>/dev/null || echo "0")
    if [ "$METRIC_COUNT" -lt 2 ]; then
      WARNINGS+=("Only $METRIC_COUNT metric(s) (recommend 2-4)")
    fi
    if [ "$METRIC_COUNT" -gt 4 ]; then
      WARNINGS+=("$METRIC_COUNT metrics (recommend 2-4, consider consolidating)")
    fi
    ;;

  *)
    echo "Unknown artifact type: $ARTIFACT"
    exit 1
    ;;
esac

# Report results
if [ ${#ERRORS[@]} -gt 0 ]; then
  echo "VALIDATION FAILED: $ARTIFACT"
  echo ""
  echo "Errors:"
  for err in "${ERRORS[@]}"; do
    echo "  - $err"
  done
fi

if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo ""
  echo "Warnings:"
  for warn in "${WARNINGS[@]}"; do
    echo "  - $warn"
  done
fi

if [ ${#ERRORS[@]} -eq 0 ] && [ ${#WARNINGS[@]} -eq 0 ]; then
  echo "VALID: $ARTIFACT"
fi

# Exit with error if validation failed
if [ ${#ERRORS[@]} -gt 0 ]; then
  exit 1
fi

exit 0
```

---

## Script Location

All scripts live in `plugins/agent-control-loop/scripts/`:

```
plugins/agent-control-loop/
└── scripts/
    ├── init-governance.sh
    ├── measure-metrics.sh
    ├── validate-boundary.sh
    ├── scan-boundaries.sh
    ├── regenerate-compressed.sh
    ├── archive-slice.sh
    └── validate-artifact.sh
```

Scripts should be executable (`chmod +x`).

---

## Summary

Seven scripts for deterministic operations:

| Script | Purpose | Key Behavior |
|--------|---------|--------------|
| init-governance.sh | Create governance/ | Exact file structure |
| measure-metrics.sh | Run measurements | Parse and execute commands |
| validate-boundary.sh | Check imports | Block violations |
| scan-boundaries.sh | Detect boundaries | Pattern matching |
| regenerate-compressed.sh | Generate A₀/B₀ | Extract and template |
| archive-slice.sh | Archive work | Move and record |
| validate-artifact.sh | Validate structure | Check against templates |

Skills invoke scripts for reliability. Scripts are testable and deterministic.
