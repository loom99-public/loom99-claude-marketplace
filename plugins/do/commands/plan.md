---
argument-hint: [focus area]
description: Planning & evaluation. Routes to specialized skills based on intent.
---

Planning command. Detects intent and invokes the appropriate skill.

<user-input>
$ARGUMENTS
</user-input>

## Intent Detection

Analyze the user's input to determine which skill to invoke:

| Intent signals | Skill to invoke |
|----------------|-----------------|
| "init", "new project", "start", "create project" | `do3:init-project` |
| "audit", "deep dive", "forensic", "comprehensive" | `do3:audit` |
| "status", "check", "how's it going", "progress" | `do3:status-check` |
| "feature", "proposal", "new feature", "design" | `do3:feature-proposal` |
| *(default - any other planning request)* | Default evaluate+plan workflow below |

**Use the Skill tool** to invoke the detected skill with the user's arguments.

---

## Default: Evaluate + Plan Workflow

If no specialized skill matches, run the standard planning cycle:

**Step 1: Evaluate**
Use do3:project-evaluator to assess current state → STATUS-*.md

If evaluator returns PAUSE with ambiguities, use do3:researcher to resolve, then re-evaluate.

**Step 1b**: Display evaluator's summary.

**Step 2: Plan**
Use do3:status-planner to create implementation plan → PLAN-*.md

**Step 2b**: Display planner's summary.

**Output**:
```
═══════════════════════════════════════
Plan Complete
  STATUS: .agent_planning/STATUS-<ts>.md
  PLAN: .agent_planning/PLAN-<ts>.md
Next: /do3:it to implement
═══════════════════════════════════════
```

---

## Beads Sync (Optional)

If beads MCP tools available, sync P0/P1 items after planning.
