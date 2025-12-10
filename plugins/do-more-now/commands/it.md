---
argument-hint: [refactor|debug|fix|test|tdd|iterate]
description: Implement something. Describe what you want, refer to a plan, or leave empty to default to most recently discussed work items
---

Implementation command. Detects intent and invokes the appropriate skill.

<user-input>$ARGUMENTS</user-input>
<current-command>it</current-command>

## Step 1: Route Subcommands (REQUIRED)

**Invoke `do:route-subcommands` skill FIRST.**

This skill will:
1. Analyze `$ARGUMENTS` for any `/do:*` commands
2. Execute pre-commands (commands that should run before main workflow)
3. Return `main_instructions` and `post_commands`

If no subcommands found, it returns immediately with `main_instructions = $ARGUMENTS`.

**Store the returned `post_commands` for Step 4.**

---

## Step 2: Intent Detection

Using `main_instructions` from Step 1, determine which skill to invoke:

| Intent signals | Skill to invoke |
|----------------|-----------------|
| "refactor", "restructure", "clean up code", "improve structure" | `do:refactor` |
| "debug", "investigate", "why is", "root cause", "troubleshoot" | `do:debug` |
| "fix", "bug", "issue", "broken", "not working" | `do:fix` |
| "review", "PR", "code review", "check this code" | `do:review` |
| "test", "add tests", "coverage", "write tests for" | `do:add-tests` |
| "setup testing", "configure tests", "add test framework", "init testing" | `do:setup-testing` |
| "tdd", "test first", "test-driven" | `do:tdd-workflow` |
| "iterate", "iterative", "build incrementally" | `do:iterative-workflow` |
| *(default - general implementation)* | Auto-select TDD or iterative below |

---

## Step 3: Execute Main Workflow

**Use the Skill tool** to invoke the detected skill. The skill will have access to conversation context.

**Default (no specialized skill matches)**: Auto-select based on context:
- Existing test framework + API/logic work → invoke `do:tdd-workflow`
- UI/visual work or no test framework → invoke `do:iterative-workflow`

---

## Step 4: Execute Post-Commands

If `post_commands` from Step 1 is non-empty, execute each one now using `SlashCommand` tool.

Pass `main_instructions` as arguments to each post-command.

---

## Step 5: Beads Sync (Optional)

If beads MCP tools available, update issue status after implementation completes.
