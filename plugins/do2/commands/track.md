---
argument-hint: [priority 0-3] [bug|feature|task|chore] description
description: Quick backlog capture to beads. Examples: "fix login", "1 bug auth fails", "0 feature export CSV"
---

Quick capture of backlog items. Minimal friction.

<input>
$ARGUMENTS
</input>

## Parse Input

Parse user input to extract:
- **Priority** (optional): 0, 1, 2, or 3 (defaults to 2/Medium)
- **Type** (optional): bug, feature, task, chore (defaults to task)
- **Description** (required): everything else

**Parsing rules**:
1. If first word is a single digit 0-3, it's priority
2. If next word is bug/feature/task/chore, it's type
3. Everything remaining is the description

**Examples**:
| Input | Priority | Type | Description |
|-------|----------|------|-------------|
| `fix login bug` | 2 | task | fix login bug |
| `1 bug auth fails` | 1 | bug | auth fails |
| `0 feature export CSV` | 0 | feature | export CSV |
| `chore update deps` | 2 | chore | update deps |
| `3 low priority thing` | 3 | task | low priority thing |

## Check Beads Availability

Check if `mcp__plugin_beads_beads__create` tool is available.

**If not available**:
```
Beads not available. Install the beads plugin to use /do2:track.

Alternative: Add to your planning docs manually, or use /do2:plan to capture in PLAN file.
```
Exit.

## Create Issue

Use `mcp__plugin_beads_beads__create` with:
- `title`: The description
- `issue_type`: The parsed type
- `priority`: The parsed priority (0=Critical, 1=High, 2=Medium, 3=Low)

## Confirm

Display confirmation:
```
Tracked: [description]
  Type: [type] | Priority: P[n]
  Issue: [beads issue ID]
```

## Error Handling

If beads create fails:
- Check if beads is initialized (`mcp__plugin_beads_beads__init` may be needed)
- Display helpful error message
- Suggest `/beads:init` if not initialized
