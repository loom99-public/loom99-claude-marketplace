---
argument-hint: [what to do]
description: [Optional: refactor|debug|fix|test|tdd|iterate] Implement or fix.  Describe what you want, refer to a plan, or let Claude figure it out
---

Implementation command. Detects intent and invokes the appropriate skill.

<user-input>
$ARGUMENTS
</user-input>

## Subcommand Detection (REQUIRED)

**STOP. Check $ARGUMENTS for any `/do:` command references.**

If $ARGUMENTS contains `/do:plan`, `/do:explore`, `/do:research`, `/do:chores`, `/do:docs`, or `/do:release`:
1. **IMMEDIATELY** use the SlashCommand tool to run that command first
2. Wait for it to complete
3. Then continue with this command's main workflow below

Example: "First run /do:plan, then implement the auth system"
→ Use SlashCommand with `/do:plan` first, THEN proceed to implementation.

**Do NOT skip this step. Do NOT proceed to implementation until subcommands complete.**

---

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
