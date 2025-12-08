---
argument-hint: [what to do]
description: Implementation & action. Routes to specialized skills based on intent.
---

Implementation command. Detects intent and invokes the appropriate skill.

<user-input>
$ARGUMENTS
</user-input>

## Intent Detection

Analyze the user's input to determine which skill to invoke:

| Intent signals | Skill to invoke |
|----------------|-----------------|
| "refactor", "restructure", "clean up code", "improve structure" | `do3:refactor` |
| "debug", "investigate", "why is", "root cause", "troubleshoot" | `do3:debug` |
| "fix", "bug", "issue", "broken", "not working" | `do3:fix` |
| "review", "PR", "code review", "check this code" | `do3:review` |
| "test", "add tests", "coverage", "write tests for" | `do3:add-tests` |
| "chores", "cleanup", "maintenance", "housekeeping" | `do3:chores` |
| "tdd", "test first", "test-driven" | `do3:tdd-workflow` |
| "iterate", "iterative", "build incrementally" | `do3:iterative-workflow` |
| *(default - general implementation)* | Auto-select TDD or iterative below |

**Use the Skill tool** to invoke the detected skill. The skill will have access to conversation context.

---

## Default: Auto-Select Workflow

If no specialized skill matches, auto-select based on context:
- Existing test framework + API/logic work → invoke `do3:tdd-workflow`
- UI/visual work or no test framework → invoke `do3:iterative-workflow`

---

## Beads Sync (Optional)

If beads MCP tools available, update issue status after implementation completes.
