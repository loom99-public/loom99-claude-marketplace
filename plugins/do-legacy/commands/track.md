---
argument-hint: [priority] [type] description
description: Quick capture of backlog items to beads. Usage - /do:track fix the login bug OR /do:track 1 bug Cannot save settings
---

You are capturing a backlog item to beads for lightweight task tracking.

**User Input**: $ARGUMENTS

## Your Task

Parse the user input and create a beads issue for tracking. Handle this gracefully if beads is unavailable.

### Input Parsing

Extract from user input:
- **Priority**: Optional number (0-3) at start → 0=P0/Critical, 1=P1/High, 2=P2/Medium, 3=P3/Low
  - Default: 2 (Medium)
- **Type**: Optional keyword after priority → bug, feature, task, epic, chore
  - Default: task
- **Description**: Remainder of input (required)

### Examples

| Input | Priority | Type | Description |
|-------|----------|------|-------------|
| fix authentication timeout | 2 | task | fix authentication timeout |
| 1 bug Cannot save settings | 1 | bug | Cannot save settings |
| 0 feature Add export to CSV | 0 | feature | Add export to CSV |
| 2 chore Update dependencies | 2 | chore | Update dependencies |

### Beads Integration

**If beads MCP tools available**:
1. Detect workspace root from current directory
2. Call `mcp__plugin_beads_beads__set_context(workspace_root=<detected>)`
3. Call `mcp__plugin_beads_beads__create(title=<description>, issue_type=<type>, priority=<priority>)`
4. Confirm: "Created {type} {issue_id}: {title} (P{priority})"

**If beads unavailable**:
- Display: "Beads MCP not available. Add items to planning docs manually or use /do:plan to evaluate and create a backlog."

**If description empty**:
- Display usage: "Usage: /do:track [priority] [type] description\n\nExamples:\n  /do:track fix login bug\n  /do:track 1 bug Cannot save settings\n  /do:track 0 feature Add dark mode"

### Error Handling

- Beads not initialized → Let create tool return error, display to user with hint: "Run 'bd init' to initialize beads in this repository"
- Invalid priority → Default to 2
- Invalid type → Default to task
- Network/database errors → Display error message, suggest retrying

## Success Criteria

- Input parsed correctly (priority, type, description extracted)
- Beads issue created with correct fields
- User receives clear confirmation or actionable error message
- Workflow never crashes (graceful degradation)
