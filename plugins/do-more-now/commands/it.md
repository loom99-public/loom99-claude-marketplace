---
argument-hint: [refactor|debug|fix|test|tdd|iterate]
description: Implement something. Describe what you want, refer to a plan, or leave empty to default to most recently discussed work items
---

Implementation command. Detects intent and invokes the appropriate skill.

<user-input>$ARGUMENTS</user-input>
<current-command>it</current-command>

## Step 0: Load Gate Configuration

Gate config sources (highest precedence first):
1. Inline in `$ARGUMENTS` (e.g., "carefully", "ask about auth")
2. Session context (user said earlier "always verify")
3. CLAUDE.md (natural language gating preferences)
4. Prompt user if not configured

### Step 0a: Check for inline gate signals

| User Signals | Gate Config |
|--------------|-------------|
| "carefully", "approve each decision" | decision-gate: BLOCKING, checkpoint-gate: BLOCKING |
| "verify", "check my work", "review when done" | decision-gate: NONBLOCKING, checkpoint-gate: BLOCKING |
| "autonomous", "just do it", "trust your judgment" | All gates: NONBLOCKING |
| "ask about X" / "only stop for Y" | Both gates: CUSTOM with that prompt |

### Step 0b: Check CLAUDE.md for gate config

Look for gating preferences in natural language:

```markdown
## Gating Preferences

- Always verify my work before moving on
- Ask me about auth or security decisions
```

Or more structured:

```markdown
- decision-gate: Ask only if auth or security affected
- checkpoint-gate: Always verify
```

### Step 0c: Prompt if not configured

If no gate config found, display brief context then ask:

**Display first**:
```
This plugin can pause for your review at four points:
- **Agent gate**: Whether to execute tasks with autonomous agents (token-efficient) or interactively
- **Decision gate**: When making architecture/technology choices
- **Security gate**: When touching auth, credentials, external APIs, or adding dependencies
- **Checkpoint gate**: When a command finishes, before moving on

You can preconfigure these in CLAUDE.md with a "Gating" section, or choose now.
```

**Then AskUserQuestion**:
```json
{
  "questions": [
    {
      "question": "How should I handle execution mode for implementation tasks?",
      "header": "Execution",
      "options": [
        {"label": "Ask each time", "description": "Always ask whether to use agent or work interactively"},
        {"label": "Auto-decide", "description": "Choose automatically based on task clarity and scope"},
        {"label": "Always agent", "description": "Use autonomous agents for all concrete tasks"},
        {"label": "Always interactive", "description": "Work with you interactively for all tasks"}
      ],
      "multiSelect": false
    },
    {
      "question": "When should I stop for your review during implementation?",
      "header": "Review",
      "options": [
        {"label": "When done", "description": "Work through task, verify results before continuing"},
        {"label": "Each decision", "description": "Stop before each significant choice"},
        {"label": "Keep going", "description": "Work autonomously, review final result"},
        {"label": "Custom rule", "description": "Specify when to ask (e.g., 'only for auth changes')"}
      ],
      "multiSelect": false
    }
  ]
}
```

**Map responses**:

Execution mode (first question):
- "Ask each time" → agent-gate: BLOCKING
- "Auto-decide" → agent-gate: NONBLOCKING
- "Always agent" → agent-gate: NONBLOCKING (with auto-agent preference)
- "Always interactive" → agent-gate: NONBLOCKING (with auto-main preference)

Review gates (second question):
- "When done" → decision-gate: NONBLOCKING, checkpoint-gate: BLOCKING
- "Each decision" → decision-gate: BLOCKING, checkpoint-gate: BLOCKING
- "Keep going" → All gates: NONBLOCKING
- "Custom rule" → Prompt for rule, both gates: CUSTOM with that prompt

### Step 0d: Write gate config

Write to `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt`:

```
EXEC_ID: <uuid>
COMMAND: /do:it
CREATED: <timestamp>
SOURCE: command | session | claude-md | prompted

DECISION_GATE: BLOCKING | NONBLOCKING | CUSTOM
DECISION_PROMPT: <if CUSTOM>

SECURITY_GATE: BLOCKING | NONBLOCKING | CUSTOM
SECURITY_PROMPT: <if CUSTOM>

CHECKPOINT_GATE: BLOCKING | NONBLOCKING | CUSTOM
CHECKPOINT_PROMPT: <if CUSTOM>

AGENT_GATE: BLOCKING | NONBLOCKING | CUSTOM
AGENT_PROMPT: <if CUSTOM>
```

---

## Step 1: Topic Resolution

Determine what to work on:

1. **If `$ARGUMENTS` provided** → Use `$ARGUMENTS` as the topic
2. **If no arguments, check conversation context** → If we were just discussing a subject (a bug, feature, file, error, task, etc.), that subject is the topic
3. **If no obvious subject in conversation** → Look for the most recent planning doc in `.agent_planning/` (PLAN-*.md, SPRINT-*.md, or TODO-*.md) and use its next uncompleted item

Set `main_instructions` to the resolved topic.

---

## Step 1.1: Resolve Topic Directory

All planning files for a topic live in `.agent_planning/<topic-slug>/`.

**Process:**

1. Generate a slug from the topic (lowercase, hyphenated, short)
   - "user authentication" → `auth` or `user-auth`
   - "payment processing" → `payments`
   - "fix login bug" → `login-bug`

2. List existing topic directories:
   ```bash
   ls -d .agent_planning/*/
   ```

3. Check for matches:

   **Exact match exists** → Use it, proceed to next step

   **Similar directories found** → Ask user:
   ```
   ┌─ Topic: "fix login bug" ────────────────────────┐
   │                                                  │
   │ Similar existing topics found:                   │
   │ 1. auth/ (5 files, last modified: 2024-12-12)   │
   │ 2. login/ (2 files, last modified: 2024-12-10)  │
   │ 3. Create new: login-bug/                        │
   │                                                  │
   └──────────────────────────────────────────────────┘
   ```

   **No similar directories** → Create new directory:
   ```bash
   mkdir -p .agent_planning/<topic-slug>
   ```

**Output:** Topic directory path (e.g., `.agent_planning/auth/`)

**Store for later use**: Set `topic_directory` variable to the resolved path.

---

## Step 1.5: Check for Solid Plan

**Critical**: We ALWAYS need a solid plan before implementation. Never code without clear direction.

### What Makes a Solid Plan?

A plan is solid if it has ALL of these:
1. **Clear objective**: What needs to be accomplished
2. **Acceptance criteria**: How we know it's done (testable conditions)
3. **Defined scope**: Which files/components/areas will be modified
4. **Approach/constraints**: How to do it, what patterns/tech to use
5. **Current state context**: Understanding of what exists now (from STATUS or evaluation)

### Check Existing Planning Artifacts

Look for a solid plan in the **topic directory** (in order):

**1. Beads issue** (if user referenced issue ID in `main_instructions`):
```bash
bd show <id> --json
```
Check if description contains:
- Clear objective
- Acceptance criteria (or link to PLAN doc)
- Scope definition

**2. Recent PLAN-*.md** in topic directory:
```bash
ls -t <topic-directory>/PLAN-*.md | head -1
```
Check if plan contains:
- Related to current topic (keyword match with `main_instructions`)
- Has acceptance criteria section
- Has scope section
- Has approach/constraints section

**3. Recent STATUS-*.md** in topic directory (provides current state context):
```bash
ls -t <topic-directory>/STATUS-*.md | head -1
```
Provides understanding of current implementation state.

### Evaluate Plan Completeness

Score the plan on completeness (0-5 points):
- +1: Has clear objective
- +1: Has acceptance criteria (3+ testable criteria)
- +1: Has scope (specific files/components listed)
- +1: Has approach/constraints documented
- +1: Has current state context (from STATUS or recent evaluation)

**Plan Assessment**:
- Score **5**: Plan is solid → Skip to Step 1.6 (agent-gate)
- Score **3-4**: Plan exists but has gaps → Proceed to Step 1.5a (fill gaps)
- Score **0-2**: No plan or very incomplete → Proceed to Step 1.5a (fill gaps)

---

## Step 1.5a: Fill Knowledge Gaps (if needed)

**Only execute if plan score < 5**

Detect what's missing and spawn agents to fill gaps. Can run multiple agents in parallel.

### Gap Detection & Agent Assignment

| Missing Component | Spawn Agent | Purpose |
|-------------------|-------------|---------|
| Current state context (no STATUS) | `project-evaluator` | Analyze current implementation, identify gaps |
| Implementation plan (no PLAN or incomplete) | `status-planner` | Create detailed implementation plan with acceptance criteria |
| Technical details / unknowns | `researcher` (external) | Research APIs, libraries, patterns, best practices |
| Codebase understanding | `researcher` (codebase) | Explore code structure, existing patterns, related components |
| Requirements unclear | AskUserQuestion OR `product-visionary` | Clarify what user actually wants |

### Spawn Gap-Filling Agents

**ALL agents must receive the topic directory path.**

**Spawn in parallel when possible** (multiple independent gaps):

```
// Example: Missing both STATUS and technical details
Task(subagent_type="project-evaluator", prompt="Topic: <topic>
Topic Directory: <topic-directory>

Analyze current auth system implementation...")

Task(subagent_type="researcher", prompt="Topic: <topic>
Topic Directory: <topic-directory>

Research OAuth 2.0 best practices for Node.js...")
```

**Sequential when dependent**:
```
// Example: Need STATUS before creating PLAN
Task(subagent_type="project-evaluator", prompt="Topic: <topic>
Topic Directory: <topic-directory>

Evaluate the current state...")

// Wait for result

Task(subagent_type="status-planner", prompt="Topic: <topic>
Topic Directory: <topic-directory>

Create implementation plan based on STATUS-<timestamp>.md in the topic directory...")
```

### Wait for Agents to Complete

All gap-filling agents must complete before proceeding.

Agents will create files in the topic directory:
- `<topic-directory>/STATUS-<timestamp>.md` (from project-evaluator)
- `<topic-directory>/PLAN-<timestamp>.md` (from status-planner)
- `<topic-directory>/RESEARCH-<topic>-<timestamp>.md` (from researcher)

---

## Step 1.5b: Validate Plan is Now Solid

After gap-filling agents complete, re-check plan completeness:

1. **Re-score** the plan (same 0-5 scoring as Step 1.5)
2. **If score >= 4**: Plan is now solid → Proceed to Step 1.6
3. **If score < 4**:
   - Surface to user: "I've gathered context but still have questions..."
   - Use AskUserQuestion to clarify remaining gaps
   - Update planning docs with user's answers
   - Proceed to Step 1.6

---

## Step 1.6: Agent-Gate (Execution Mode Decision)

**At this point, we have a solid plan.** Now decide HOW to implement it.

### Analyze Implementation Complexity

**Simple implementation signals** (likely agent mode):
- Single file or component
- Clear algorithmic change
- Well-defined scope (< 5 files)
- No UI/visual work
- Existing test framework

**Complex implementation signals** (likely main context):
- Multiple interconnected changes
- UI/visual work needing iteration
- Exploratory refactoring
- Complex debugging scenarios
- User wants to see progress

### Trigger Agent-Gate

1. **Check gate configuration** from `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt`
2. **Get AGENT_GATE mode**:
   - `BLOCKING`: Always ask user
   - `NONBLOCKING`: Auto-decide based on complexity signals
   - `CUSTOM`: Use custom rule to evaluate

3. **If BLOCKING or (CUSTOM and rule triggers)**:

Use AskUserQuestion:
```json
{
  "questions": [{
    "question": "We have a solid plan. How should I execute the implementation?",
    "header": "Execution",
    "options": [
      {
        "label": "Use agent",
        "description": "Token-efficient, autonomous. Less visible. Best for well-defined implementation."
      },
      {
        "label": "Work with me",
        "description": "Interactive, visible progress. Easier to redirect. Best for complex/visual work."
      }
    ],
    "multiSelect": false
  }]
}
```

4. **Handle response**:
   - "Use agent" → Set `execution_mode = AGENT`
   - "Work with me" → Set `execution_mode = MAIN`

5. **If NONBLOCKING**: Auto-decide based on complexity signals above

---

## Step 2: Subcommand Detection

**Quick check**: Does `main_instructions` contain `/do:` patterns (other than `/do:it`)?

- **If NO** → Proceed to Intent Detection
- **If YES** → Invoke `do:route-subcommands` skill, then proceed with returned `main_instructions`

---

## Step 3: Execute Implementation

**At this point**: We have a solid plan and have decided execution mode (agent or main context).

### Prepare Execution Context

#### Option A: Use Existing Handoff Document (Preferred)

Check if a recent handoff document exists in the topic directory:

```bash
# Find most recent handoff for this topic
ls -t <topic-directory>/HANDOFF-*.md | head -1
```

If handoff exists and is recent (< 1 hour old) and related to topic:
- **Use it directly** - no need to recreate context
- Skip to execution mode branching below

#### Option B: Create Execution Brief

If no handoff exists, gather context from planning artifacts **in the topic directory**:

1. **Read latest PLAN-*.md** (created by status-planner):
   ```bash
   ls -t <topic-directory>/PLAN-*.md | head -1
   ```

2. **Read latest STATUS-*.md** (created by project-evaluator):
   ```bash
   ls -t <topic-directory>/STATUS-*.md | head -1
   ```

3. **Read beads issue** (if applicable):
   ```bash
   bd show <id> --json
   ```

4. **Synthesize concise execution brief** (<500 tokens):
   ```
   OBJECTIVE: [From PLAN]

   ACCEPTANCE CRITERIA:
   - [From PLAN]

   SCOPE:
   - Files to modify: [From PLAN]
   - Components affected: [From PLAN]

   CURRENT STATE:
   - [Key points from STATUS]

   APPROACH:
   - [From PLAN - how to implement]

   CONSTRAINTS:
   - [From PLAN - what to avoid, patterns to use]

   REFERENCES:
   - Topic Directory: <topic-directory>
   - PLAN: <topic-directory>/PLAN-<timestamp>.md
   - STATUS: <topic-directory>/STATUS-<timestamp>.md
   - Beads: <issue IDs>
   ```

5. **Store brief** at `.agent_planning/do-command-state/<EXEC_ID>/EXECUTION_BRIEF.md`

**Note**: For complex work, consider running `/do:handoff` first to create a comprehensive context document.

### Execution Mode Branching

**If `execution_mode = AGENT`**:

1. **Determine which agent to spawn**:
   - User said "tdd" or "test first" → `test-driven-implementer`
   - Test framework exists + API/logic work → `test-driven-implementer`
   - Otherwise → `iterative-implementer`

2. **Spawn implementation agent WITH TOPIC DIRECTORY**:

   **If using HANDOFF document**:
   ```
   Task(
     subagent_type="test-driven-implementer" OR "iterative-implementer",
     description="Implement: <objective from handoff>",
     prompt="Topic Directory: <topic-directory>

Read and execute the handoff document at <topic-directory>/HANDOFF-<topic>-<timestamp>.md

This contains complete context including:
- Objective and acceptance criteria
- Current state and what's been done
- Implementation approach and constraints
- Reference materials (PLAN, DOD, STATUS, beads issues)
- Known gotchas and patterns to follow

All planning files (PLAN, DOD, STATUS) are in the topic directory.

Follow the recommended steps in the handoff. Update the beads issue as you progress.
"
   )
   ```

   **If using EXECUTION_BRIEF**:
   ```
   Task(
     subagent_type="test-driven-implementer" OR "iterative-implementer",
     description="Implement: <objective from plan>",
     prompt="Topic Directory: <topic-directory>

<contents of EXECUTION_BRIEF.md>

Please implement according to the plan above. Read the detailed PLAN and STATUS docs from the topic directory as needed.

Beads tracking: <if applicable, reference issue ID>
"
   )
   ```

3. **Agent will**:
   - Read full PLAN/DOD/STATUS from topic directory
   - Implement according to acceptance criteria
   - Run tests/validation
   - Invalidate eval-cache for modified files
   - Update beads issue with progress
   - Return summary of what was implemented

**If `execution_mode = MAIN`** (work interactively):

1. **Determine workflow approach**:
   - User said "tdd" or "test first" → `do:tdd-workflow`
   - Test framework exists + API/logic work → `do:tdd-workflow`
   - Otherwise → `do:iterative-workflow`

2. **Invoke workflow skill** with plan context:
   ```
   Skill("do:tdd-workflow" OR "do:iterative-workflow")
   ```

3. **Skill will**:
   - Guide you through implementation
   - Reference EXECUTION_BRIEF.md for plan
   - Check acceptance criteria as you go
   - Update beads issue with progress

---

## Step 3b: Process Decision and Security Gates

After agent/skill returns, process any logged gates:

**Check for pending decisions**:
- Glob: `.agent_planning/do-command-state/<EXEC_ID>/DECISIONS/*.txt`
- If files exist without `APPROVAL_STATUS:` → invoke `do:gating-controller` for `decision-gate`

**Check for pending security events**:
- Glob: `.agent_planning/do-command-state/<EXEC_ID>/SECURITY/*.txt`
- If files exist without `APPROVAL_STATUS:` → invoke `do:gating-controller` for `security-gate`

**Handle results**:
- If gating-controller returns `STOP` → Stop command, show user feedback
- If gating-controller returns `CONTINUE` → Proceed

---

## Post-Commands

If `route-subcommands` returned `post_commands`, execute each one now:

**For each command in post_commands**:
- Use the `SlashCommand` tool
- Format: `<command> <main_instructions>`
- Example: If post_commands = `["/do:chores"]` and main_instructions = `"fix the bug"`, execute:
  ```
  SlashCommand("/do:chores fix the bug")
  ```

**Important**: Append main_instructions to preserve context for downstream commands.

---

## Step 4: Checkpoint Gate

After workflow completes, invoke `do:gating-controller` for `checkpoint-gate`:

**Read config** from `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.yaml`

| checkpoint-gate mode | Action |
|----------------------|--------|
| BLOCKING | Invoke `do:work-checkpoint` skill |
| NONBLOCKING | Skip checkpoint |
| CUSTOM | Invoke `do:gating-controller` to evaluate, then checkpoint if triggered |

**If checkpoint invoked**, handle the result:

| Checkpoint Result | Next Action |
|-------------------|-------------|
| `ACTION: FIX_FEEDBACK` | Re-invoke workflow skill with feedback as context |
| `ACTION: CONTINUE` | Proceed to next planned work (or prompt for next command) |
| `ACTION: STOP` | End command, wait for user |
| `ACTION: CUSTOM` | Execute user's custom instruction |

---

## Beads Integration

### At Command Start

Check if working on a specific beads issue:
```bash
# If user references an issue ID (e.g., "fix bd-xxx")
bd show <id> --json

# Or check for ready work
bd ready --json
```

If issue identified, claim it:
```bash
bd update <id> --status in_progress --json
```

### After Workflow Completes

Update beads with results:
```bash
# If implementation succeeded
bd update <id> --notes "COMPLETED: <summary of work done>"
bd close <id> --reason "Implemented in commit <hash>" --json

# If partially complete
bd update <id> --notes "IN PROGRESS: <what was done>. NEXT: <remaining work>"

# If blocked
bd update <id> --notes "BLOCKER: <what's blocking>"
```

### Discovered Issues

If the workflow created new issues (check agent output for `discovered_issues`):
```bash
# These are already created by the agent with discovered-from links
# Just verify they exist
bd show <discovered-id> --json
```

### Session End Sync

```bash
bd sync  # Force immediate export/commit/push - NEVER skip at session end
```

**Graceful Degradation**: If beads unavailable, skip all beads steps silently. Workflow continues normally.
