# Hooks: Automatic Context Injection

This document defines all hooks in the agent-control-loop plugin. Hooks provide automatic, always-on enforcement without manual invocation.

---

## Design Principle: Hooks Are Always-On

Hooks ensure critical behaviors happen without relying on agent memory:
- **Pre-command hooks:** Inject compressed artifacts before work begins
- **Post-command hooks:** Validate results and suggest next actions
- **Pre-tool hooks:** Prevent boundary violations before writes occur

Hooks are the "attention management" layer. They keep rules alive.

---

## Hook Summary

| Hook | Type | Trigger | Purpose |
|------|------|---------|---------|
| inject-contract | Pre-command | `/loop:*` commands | Inject A₀ always-on contract |
| inject-playbook | Pre-command | `/loop:phase` | Inject relevant B₀ playbook |
| validate-governance | Pre-command | `/loop:phase` | Verify governance exists |
| validate-phase-outcome | Post-command | `/loop:phase` | Check metrics moved |
| suggest-next-action | Post-command | `/loop:*` commands | Recommend next step |
| boundary-guard | Pre-tool | Edit/Write to `src/**` | Detect boundary violations |
| design-sync-check | Post-command | `/design:*` commands | Check consistency |

---

## hooks.json Structure

**Location:** `hooks/hooks.json`

```json
{
  "hooks": [
    {
      "name": "inject-contract",
      "type": "pre_command",
      "command_pattern": "^/loop:",
      "script": "hooks/inject-contract.sh",
      "inject_output": true
    },
    {
      "name": "inject-playbook",
      "type": "pre_command",
      "command_pattern": "^/loop:phase$",
      "script": "hooks/inject-playbook.sh",
      "inject_output": true
    },
    {
      "name": "validate-governance",
      "type": "pre_command",
      "command_pattern": "^/loop:phase$",
      "script": "hooks/validate-governance.sh",
      "block_on_failure": true
    },
    {
      "name": "validate-phase-outcome",
      "type": "post_command",
      "command_pattern": "^/loop:phase$",
      "script": "hooks/validate-phase-outcome.sh",
      "inject_output": true
    },
    {
      "name": "suggest-next-action",
      "type": "post_command",
      "command_pattern": "^/loop:",
      "script": "hooks/suggest-next-action.sh",
      "inject_output": true
    },
    {
      "name": "boundary-guard",
      "type": "pre_tool",
      "tool_pattern": "^(Edit|Write)$",
      "path_pattern": "^src/",
      "script": "hooks/boundary-guard.sh",
      "block_on_failure": true
    },
    {
      "name": "design-sync-check",
      "type": "post_command",
      "command_pattern": "^/design:",
      "script": "hooks/design-sync-check.sh",
      "inject_output": true
    }
  ]
}
```

---

## Hook Specifications

### inject-contract

**Purpose:** Inject A₀ always-on contract before any `/loop:` command.

**Type:** pre_command

**Trigger:** Commands matching `^/loop:`

**Behavior:**

```bash
#!/bin/bash
# hooks/inject-contract.sh

CONTRACT_FILE="governance/compressed/A0-contract.md"

if [ -f "$CONTRACT_FILE" ]; then
  echo "<system-reminder>"
  echo "=== ALWAYS-ON CONTRACT ==="
  cat "$CONTRACT_FILE"
  echo "=== END CONTRACT ==="
  echo "</system-reminder>"
else
  echo "<system-reminder>"
  echo "WARNING: A0-contract.md not found. Run /loop:init to create."
  echo "</system-reminder>"
fi
```

**Output Injection:** Yes — content appears in agent context

**Effect:** Agent sees hard rules at start of every `/loop:` command, keeping them "near the present" in attention.

---

### inject-playbook

**Purpose:** Inject relevant B₀ playbook before `/loop:phase`.

**Type:** pre_command

**Trigger:** Commands matching `^/loop:phase$`

**Behavior:**

```bash
#!/bin/bash
# hooks/inject-playbook.sh

PLAYBOOK_DIR="governance/compressed/B0-playbooks"
TARGET_FILE="governance/live/TARGET.md"

if [ ! -f "$TARGET_FILE" ]; then
  exit 0  # No target, no playbook
fi

# Determine playbook from goal keywords
GOAL=$(grep -A1 "^## Goal" "$TARGET_FILE" | tail -1)

PLAYBOOK=""
if echo "$GOAL" | grep -qi "migrat"; then
  PLAYBOOK="migration.md"
elif echo "$GOAL" | grep -qi "refactor"; then
  PLAYBOOK="refactor.md"
elif echo "$GOAL" | grep -qi "feature\|add\|implement"; then
  PLAYBOOK="feature.md"
fi

if [ -n "$PLAYBOOK" ] && [ -f "$PLAYBOOK_DIR/$PLAYBOOK" ]; then
  echo "<system-reminder>"
  echo "=== ACTIVE PLAYBOOK: $PLAYBOOK ==="
  cat "$PLAYBOOK_DIR/$PLAYBOOK"
  echo "=== END PLAYBOOK ==="
  echo "</system-reminder>"
fi
```

**Output Injection:** Yes — playbook content appears in context

**Effect:** Task-specific rules are loaded only when relevant, reducing noise.

---

### validate-governance

**Purpose:** Verify governance directory exists before `/loop:phase`.

**Type:** pre_command

**Trigger:** Commands matching `^/loop:phase$`

**Behavior:**

```bash
#!/bin/bash
# hooks/validate-governance.sh

LIVE_DIR="governance/live"
REQUIRED_FILES=("TARGET.md" "BOUNDARY.md" "BLOCKERS.md" "METRICS.md")

# Check directory exists
if [ ! -d "$LIVE_DIR" ]; then
  echo "ERROR: Governance directory not found."
  echo ""
  echo "Run '/loop:init' first to bootstrap the control loop."
  exit 1
fi

# Check required files
MISSING=()
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$LIVE_DIR/$file" ]; then
    MISSING+=("$file")
  fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "ERROR: Missing required artifacts:"
  for file in "${MISSING[@]}"; do
    echo "  - $file"
  done
  echo ""
  echo "Run '/loop:init' to create missing files."
  exit 1
fi

exit 0
```

**Block on Failure:** Yes — command is blocked if validation fails

**Effect:** Cannot run `/loop:phase` without proper governance structure.

---

### validate-phase-outcome

**Purpose:** Verify phase produced valid outcome after `/loop:phase`.

**Type:** post_command

**Trigger:** Commands matching `^/loop:phase$`

**Behavior:**

```bash
#!/bin/bash
# hooks/validate-phase-outcome.sh

METRICS_FILE="governance/live/METRICS.md"
PHASE_LOG="governance/PHASE-LOG.md"

# Check if PHASE-LOG was updated (recent timestamp)
if [ -f "$PHASE_LOG" ]; then
  LAST_PHASE=$(grep -m1 "^## Phase" "$PHASE_LOG" | head -1)
  echo "Last phase recorded: $LAST_PHASE"
fi

# Check metrics file for recent update
if [ -f "$METRICS_FILE" ]; then
  LAST_UPDATED=$(grep "^## Last Updated" "$METRICS_FILE" -A1 | tail -1)
  echo "Metrics last updated: $LAST_UPDATED"

  # Check for stagnation warning
  # (This is a simple check; more sophisticated would parse trends)
  if grep -q "⚠" "$METRICS_FILE"; then
    echo ""
    echo "WARNING: Some metrics show stagnation. Review and escalate if stuck."
  fi
fi

# Check for pending escalations
BLOCKERS_FILE="governance/live/BLOCKERS.md"
if [ -f "$BLOCKERS_FILE" ]; then
  ESCALATIONS=$(grep -c "^### ESCALATION:" "$BLOCKERS_FILE" 2>/dev/null || echo "0")
  if [ "$ESCALATIONS" -gt 0 ]; then
    echo ""
    echo "ATTENTION: $ESCALATIONS escalation(s) pending decision."
    echo "Run '/loop:escalate' to resolve."
  fi
fi
```

**Output Injection:** Yes — warnings appear in context

**Effect:** User sees validation feedback after every phase.

---

### suggest-next-action

**Purpose:** Recommend next action after any `/loop:` command.

**Type:** post_command

**Trigger:** Commands matching `^/loop:`

**Behavior:**

```bash
#!/bin/bash
# hooks/suggest-next-action.sh

BLOCKERS_FILE="governance/live/BLOCKERS.md"
TARGET_FILE="governance/live/TARGET.md"

# Count blockers
BLOCKER_COUNT=0
ESCALATION_COUNT=0
if [ -f "$BLOCKERS_FILE" ]; then
  BLOCKER_COUNT=$(grep -c "^### BLOCKER-" "$BLOCKERS_FILE" 2>/dev/null || echo "0")
  ESCALATION_COUNT=$(grep -c "^### ESCALATION:" "$BLOCKERS_FILE" 2>/dev/null || echo "0")
fi

# Count DoD progress
DOD_TOTAL=0
DOD_COMPLETE=0
if [ -f "$TARGET_FILE" ]; then
  DOD_TOTAL=$(grep -c "^\- \[ \]" "$TARGET_FILE" 2>/dev/null || echo "0")
  DOD_COMPLETE=$(grep -c "^\- \[x\]" "$TARGET_FILE" 2>/dev/null || echo "0")
  DOD_TOTAL=$((DOD_TOTAL + DOD_COMPLETE))
fi

echo ""
echo "═══════════════════════════════════════"
echo "SUGGESTED NEXT ACTION:"

if [ "$ESCALATION_COUNT" -gt 0 ]; then
  echo "→ /loop:escalate (resolve $ESCALATION_COUNT pending decision(s))"
elif [ "$BLOCKER_COUNT" -gt 0 ]; then
  echo "→ /loop:phase (attack next blocker)"
elif [ "$DOD_COMPLETE" -lt "$DOD_TOTAL" ]; then
  echo "⚠ Zero blockers but DoD incomplete ($DOD_COMPLETE/$DOD_TOTAL)"
  echo "→ Add missing blockers to BLOCKERS.md"
else
  echo "✓ All work complete!"
  echo "→ /loop:status for final verification"
fi
echo "═══════════════════════════════════════"
```

**Output Injection:** Yes

**Effect:** User always knows what to do next.

---

### boundary-guard

**Purpose:** Detect boundary violations before writes to source code.

**Type:** pre_tool

**Trigger:** Edit or Write tools targeting files in `src/**`

**Behavior:**

```bash
#!/bin/bash
# hooks/boundary-guard.sh
# Receives: $1 = file path, $2 = new content (optional)

FILE_PATH="$1"
BOUNDARY_FILE="governance/live/BOUNDARY.md"

# If no boundary file, can't check
if [ ! -f "$BOUNDARY_FILE" ]; then
  exit 0
fi

# Extract forbidden patterns
FORBIDDEN=$(grep -A20 "^## Forbidden Dependencies" "$BOUNDARY_FILE" | grep "^\- " | sed 's/^- //')

# Extract bridge path
BRIDGE=$(grep "^**Module/Path:**" "$BOUNDARY_FILE" | sed 's/.*: `\(.*\)`/\1/')

# Check if file is in bridge (allowed)
if echo "$FILE_PATH" | grep -q "$BRIDGE"; then
  exit 0  # Bridge files are exempt
fi

# Check if content contains forbidden imports
if [ -n "$2" ]; then
  for PATTERN in $FORBIDDEN; do
    if echo "$2" | grep -q "$PATTERN"; then
      echo "BLOCKED: Boundary violation detected"
      echo ""
      echo "File: $FILE_PATH"
      echo "Forbidden import: $PATTERN"
      echo "Boundary law: New code must not import legacy except through bridge."
      echo ""
      echo "Options:"
      echo "1. Use bridge: Import from $BRIDGE instead"
      echo "2. Escalate: /loop:escalate to request boundary exception"
      echo "3. Fix: Remove the forbidden import"
      exit 1
    fi
  done
fi

exit 0
```

**Block on Failure:** Yes — write is blocked

**Effect:** Resurrection is mechanically prevented at write time.

---

### design-sync-check

**Purpose:** Quick consistency check after design commands.

**Type:** post_command

**Trigger:** Commands matching `^/design:`

**Behavior:**

```bash
#!/bin/bash
# hooks/design-sync-check.sh

DESIGN_LINKS="governance/live/DESIGN_LINKS.md"
ACTIVE_DIR="design/active"

# Check if any active designs exist
if [ -d "$ACTIVE_DIR" ] && [ "$(ls -A $ACTIVE_DIR 2>/dev/null)" ]; then
  ACTIVE_COUNT=$(ls -d $ACTIVE_DIR/*/ 2>/dev/null | wc -l | tr -d ' ')

  # Check if DESIGN_LINKS references them
  if [ -f "$DESIGN_LINKS" ]; then
    LINKED_COUNT=$(grep -c "^| A-" "$DESIGN_LINKS" 2>/dev/null || echo "0")

    if [ "$ACTIVE_COUNT" -ne "$LINKED_COUNT" ]; then
      echo ""
      echo "WARNING: Design sync issue detected"
      echo "  Active designs: $ACTIVE_COUNT"
      echo "  Linked in DESIGN_LINKS: $LINKED_COUNT"
      echo ""
      echo "Run '/design:sync' to resolve."
    fi
  fi
fi
```

**Output Injection:** Yes

**Effect:** Design plane consistency is continuously monitored.

---

## Hook Execution Order

Hooks execute in defined order:

### Pre-command hooks (for `/loop:phase`)

1. `validate-governance` — Block if missing (can stop execution)
2. `inject-contract` — Inject A₀
3. `inject-playbook` — Inject B₀

### Command executes

### Post-command hooks (for `/loop:phase`)

1. `validate-phase-outcome` — Check results
2. `suggest-next-action` — Recommend next

### Pre-tool hooks (during execution)

- `boundary-guard` — Before any Edit/Write to src/**

---

## Hook Configuration Options

Each hook can have:

| Option | Type | Description |
|--------|------|-------------|
| `inject_output` | boolean | Inject script output into agent context |
| `block_on_failure` | boolean | Block command/tool if script exits non-zero |
| `timeout` | number | Max execution time in ms |
| `silent` | boolean | Don't show output to user |

---

## Writing New Hooks

### Hook Script Template

```bash
#!/bin/bash
# hooks/my-hook.sh

# Exit codes:
# 0 = success (continue)
# 1 = failure (block if block_on_failure)

# Output goes to agent context if inject_output=true
# Keep output concise and actionable

# Access environment:
# $COMMAND = the command being run (for pre/post_command)
# $TOOL = the tool being called (for pre_tool)
# $FILE_PATH = target file (for pre_tool on file operations)

# Example: simple check
if [ ! -f "some/required/file" ]; then
  echo "ERROR: Required file missing"
  exit 1
fi

# Example: inject context
echo "<system-reminder>"
echo "Remember: [important rule]"
echo "</system-reminder>"

exit 0
```

### Registration in hooks.json

```json
{
  "name": "my-hook",
  "type": "pre_command",
  "command_pattern": "^/my:command$",
  "script": "hooks/my-hook.sh",
  "inject_output": true,
  "block_on_failure": false,
  "timeout": 5000
}
```

---

## Why Hooks Matter

### Attention Re-Anchoring

From the context document: "Rules survive only if kept near the present."

Hooks automatically inject A₀/B₀ at the right moments, keeping critical rules "geometrically nearby" in the attention landscape.

Without hooks, agents would need to remember to restate rules — and they often forget.

### Mechanical Enforcement

The boundary-guard hook prevents resurrection at the mechanical level. The agent cannot accidentally violate boundaries because the write is blocked before it happens.

This is superior to "please remember not to" — it's impossible to forget.

### Consistent User Experience

Suggest-next-action ensures users always know what to do. No dead ends.

---

## Summary

Seven hooks providing automatic enforcement:

| Hook | Purpose | Critical Effect |
|------|---------|-----------------|
| inject-contract | Inject A₀ | Rules stay "near the present" |
| inject-playbook | Inject B₀ | Task-specific rules loaded |
| validate-governance | Pre-check | Can't run phase without governance |
| validate-phase-outcome | Post-check | Catch stagnation early |
| suggest-next-action | Guide user | No dead ends |
| boundary-guard | Block violations | Resurrection impossible |
| design-sync-check | Consistency | Drift detected early |

Hooks are the "always-on" layer. They don't rely on memory.
