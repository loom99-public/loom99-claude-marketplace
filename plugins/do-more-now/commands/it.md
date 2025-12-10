---
argument-hint: [what to do]
description: [Optional: refactor|debug|fix|test|tdd|iterate] Implement or fix.  Describe what you want, refer to a plan, or let Claude figure it out 
---

Implementation command. Detects intent and invokes the appropriate skill.

<user-input>
$ARGUMENTS
</user-input>

## Intent Detection

Analyze the user's input to determine which skill to invoke:

| Intent signals | Skill to invoke |
|----------------|-----------------|
| "refactor", "restructure", "clean up code", "improve structure" | `do:refactor` |
| "debug", "investigate", "why is", "root cause", "troubleshoot" | `do:debug` |
| "fix", "bug", "issue", "broken", "not working" | `do:fix` |
| "review", "PR", "code review", "check this code" | `do:review` |
| "test", "add tests", "coverage", "write tests for" | `do:add-tests` |
| "chores", "cleanup", "maintenance", "housekeeping" | `do:chores` |
| "tdd", "test first", "test-driven" | `do:tdd-workflow` |
| "iterate", "iterative", "build incrementally" | `do:iterative-workflow` |
| *(default - general implementation)* | Auto-select TDD or iterative below |

**Use the Skill tool** to invoke the detected skill. The skill will have access to conversation context.

---

## Default: Auto-Select Workflow

If no specialized skill matches, auto-select based on context:
- Existing test framework + API/logic work → invoke `do:tdd-workflow`
- UI/visual work or no test framework → invoke `do:iterative-workflow`

---

## Beads Sync (Optional)

If beads MCP tools available, update issue status after implementation completes.
