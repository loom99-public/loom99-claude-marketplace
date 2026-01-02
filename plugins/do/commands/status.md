---
argument-hint: [topic]
description: Quick status check - WIP, uncommitted changes, in-progress work, recent plans, and next queued work.
---

# Status Command

Fast, lightweight status check. No deep evaluation - just surface the current state.

## Output

Run these checks quickly and display results:

### 1. Git Status (WIP / Uncommitted Changes)

```bash
git status --short
git stash list
```

Display:
```
┌─ Working Directory ────────────────────────────────┐
│ Uncommitted changes: [n files]                     │
│ Staged: [list or "none"]                           │
│ Unstaged: [list or "none"]                         │
│ Stashes: [n stashes or "none"]                     │
└────────────────────────────────────────────────────┘
```

### 2. In-Progress Work

Check for active work in `.agent_planning/`:

```bash
ls -t .agent_planning/*/SPRINT-*.md 2>/dev/null | head -3
ls -t .agent_planning/*/TODO-*.md 2>/dev/null | head -3
```

For each found, extract:
- Topic name (from directory)
- Status (from file content - look for checked/unchecked items)
- Last modified

Display:
```
┌─ In-Progress Work ─────────────────────────────────┐
│ 1. auth/ - 2/5 items complete (modified: 2h ago)   │
│ 2. payments/ - 0/3 items (modified: 1d ago)        │
│ [or "No active sprints found"]                     │
└────────────────────────────────────────────────────┘
```

### 3. Recent Plans

```bash
ls -t .agent_planning/*/PLAN-*.md 2>/dev/null | head -3
```

Display:
```
┌─ Recent Plans ─────────────────────────────────────┐
│ 1. auth/PLAN-2024-12-13-143022.md (today)          │
│    Sprint: "Implement login flow"                  │
│ 2. payments/PLAN-2024-12-12-091500.md (yesterday)  │
│    Sprint: "Add Stripe integration"                │
└────────────────────────────────────────────────────┘
```

### 4. Next Queued Work

Look for incomplete items in most recent plans:

```bash
# Find highest priority incomplete item from latest PLAN
```

Display:
```
┌─ Next Up ──────────────────────────────────────────┐
│ From: auth/PLAN-2024-12-13-143022.md               │
│ P0: Implement password validation                  │
│ Status: Not started                                │
│                                                    │
│ Run: /do:it auth                      │
└────────────────────────────────────────────────────┘
```

---

## Full Output Example

```
═══════════════════════════════════════════════════════
Status Check
═══════════════════════════════════════════════════════

Working Directory:
  Uncommitted: 3 files (2 staged, 1 unstaged)
  Stashes: none

In-Progress:
  auth/ - 2/5 complete (2h ago)

Recent Plans:
  1. auth/PLAN-2024-12-13.md - "Implement login flow"
  2. payments/PLAN-2024-12-12.md - "Add Stripe"

Next Up:
  P0: Implement password validation (auth/)
  → /do:it auth

═══════════════════════════════════════════════════════
```

---

## Important Notes

- This is a **quick check** - no deep evaluation or agent spawning
- Does NOT run tests or validate implementation
- For deep evaluation, use `/do:plan` which evaluates before planning
- Use this for "where am I?" orientation at start of session
