---
argument-hint: [priority 0-3] [type] description
description: Quick backlog capture to beads.
---

Quick capture. No skills needed - direct execution.

<input>
$ARGUMENTS
</input>

## Parse Input

- **Priority** (optional): 0-3 (defaults to 2)
- **Type** (optional): bug/feature/task/chore (defaults to task)
- **Description**: everything else

## Check Beads

If `mcp__plugin_beads_beads__create` unavailable:
```
Beads not available. Install beads plugin for /do3:track.
```

## Create Issue

Use `mcp__plugin_beads_beads__create`:
- title: description
- issue_type: parsed type
- priority: parsed priority

## Confirm

```
Tracked: [description]
  Type: [type] | Priority: P[n]
```
