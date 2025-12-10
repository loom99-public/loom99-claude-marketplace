---
argument-hint: [refactor|debug|fix|test|tdd|iterate]
description: Implement something. Describe what you want, refer to a plan, or leave empty to default to most recently discussed work items
---

Implementation command. Detects intent and invokes the appropriate skill.

<user-input>$ARGUMENTS</user-input>
<current-command>it</current-command>

## Step 0: Detect Gate Mode

Analyze `$ARGUMENTS` for gate intent signals using LLM (NOT flag parsing):

**Intent Detection Table**:

| User Signals | Gate Mode |
|--------------|-----------|
| "carefully", "approve each", "manual", "review everything", "ask me about", "check with me" | BLOCKING |
| "guided", "review major", "help with risks", "important decisions only", "significant choices" | HYBRID |
| "autonomous", "auto", "just do it", "move fast", "trust your judgment", "auto-approve" | NONBLOCKING |

**If multiple signals or ambiguous**: Prefer more conservative (BLOCKING > HYBRID > NONBLOCKING)

**If no gate signals detected**:
Use AskUserQuestion to prompt:
```
How should I handle decisions during this work?

Options:
1. BLOCKING - Ask you to approve every significant choice
2. HYBRID - Ask about major/risky decisions, auto-approve obvious ones (Recommended)
3. NONBLOCKING - Make all decisions autonomously and document them for review
```

## Step 0b: Initialize Gate State (If Gate Mode Selected)

If a gate mode was detected or selected:

1. Read EXEC_ID from `.agent_planning/do-command-logs/CURRENT_EXECUTION_ID.txt`
   - If file doesn't exist, generate a new UUID

2. Create state directory structure:
   ```
   .agent_planning/do-command-state/<EXEC_ID>/
   .agent_planning/do-command-state/<EXEC_ID>/DECISIONS/
   ```

3. Write GATE_CONFIG.txt:
   ```
   GATE_MODE: <detected-or-selected-mode>
   EXEC_ID: <exec-id>
   CREATED: <iso-timestamp>
   COMMAND: /do:it
   USER_ARGS: $ARGUMENTS
   ```

**Continue to Step 1...**

---

## Subcommand Detection

**Quick check**: Does `$ARGUMENTS` contain `/do:` patterns (other than `/do:it`)?

- **If NO** → `main_instructions = $ARGUMENTS`, proceed to Intent Detection
- **If YES** → Invoke `do:route-subcommands` skill, then proceed with returned `main_instructions`

---

## Intent Detection

Analyze `main_instructions` to determine which skill to invoke:

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

## Post-Commands

If subcommands were detected and `post_commands` is non-empty, execute them now.

---

## Beads Sync (Optional)

If beads MCP tools available, update issue status after implementation completes.
