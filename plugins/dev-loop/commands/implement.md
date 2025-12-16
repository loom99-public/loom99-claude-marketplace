---
argument-hint: [feature or task to implement]
description: Implement a feature with automatic planning, human-in-the-loop verification, and feedback cycles. Chains to /plan if no plan exists.
---

# Implement Command

Iterative implementation workflow: resolve topic, get plan, approve DoD, spawn agent to build functionality, validate through runtime evaluation.

## Step 1: Determine What to Work On

<task-focus>
$ARGUMENTS
</task-focus>


**Resolution order:**

1. **User specified a task** → Use `$ARGUMENTS` as the topic
2. **Recent conversation context** → If we were just discussing something specific (e.g., user said "yes" or "make it so" after a proposal), use that as the topic
3. **Nothing clear** → Ask the user with concrete options:

```
┌─ What should I implement? ─────────────────────────┐
│ 1. [Most recent topic from .agent_planning/]       │
│ 2. [Highest priority incomplete work item]         │
│ 3. Something else (describe it)                    │
└────────────────────────────────────────────────────┘
```

**Output:** A topic string (e.g., "user authentication", "payment flow").

---

## Step 2: Resolve Topic Directory

All planning files for a topic live in `.agent_planning/<topic-slug>/`.

**Process:**

1. Generate a slug from the topic (lowercase, hyphenated, short)
   - "user authentication" → `auth` or `user-auth`
   - "payment processing" → `payments`

2. List existing topic directories:
   ```bash
   ls -d .agent_planning/*/
   ```

3. Check for matches:

   **Exact match exists** → Use it, proceed to Step 3

   **Similar directories found** → Ask user:
   ```
   ┌─ Topic: "user authentication" ─────────────────────┐
   │                                                    │
   │ Similar existing topics found:                     │
   │ 1. auth/ (3 files, last modified: 2024-12-12)     │
   │ 2. login/ (1 file, last modified: 2024-12-10)     │
   │ 3. Create new: user-auth/                          │
   │                                                    │
   └────────────────────────────────────────────────────┘
   ```

   **No similar directories**
      1. First, check .agent_planning/ for a plan on this topic (legacy plans are here)
      2. → Create new directory for topic and move existing plan to new directory
         - if no legacy plan found, continue with new directory

**Output:** Topic directory path (e.g., `.agent_planning/auth/`)

---

## Step 3: Find or Create a Plan

Check topic directory for a plan.

**Search:**
1. List files in topic directory: `ls .agent_planning/<topic>/`
2. Look for `PLAN-*.md` (newest by timestamp)
3. Look for `DOD-*.md` (must exist alongside plan)
   - DOD = Definition of Done.  If it does not exist, we must generate one

**Decision:**

- **Plan + DoD exist** → Note filepaths, proceed to Step 4
- **No plan** → Run `/dev-loop:plan $TOPIC`, then proceed with new plan
- **Plan exists, No DOD** → Run `/dev-loop:plan Please created a Definition of Done for this plan: $PLAN_PATH`, then proceed

**Output:** Plan filepath AND DoD filepath.

---

## Step 4: Definition of Done (Main Context Approval)

Before spawning the agent, get user approval on completion criteria.

**Read the DoD file** (it's small, just acceptance criteria).

**Present for approval:**

```
┌─ Definition of Done: $TOPIC ───────────────────────┐
│                                                    │
│ Acceptance Criteria:                               │
│ - [ ] [Criterion 1]                                │
│ - [ ] [Criterion 2]                                │
│ - [ ] [Criterion 3]                                │
│                                                    │
│ Sprint Scope: [2-3 deliverables max]               │
│                                                    │
│ 1. Approve - spawn agent to implement              │
│ 2. Revise - adjust criteria first                  │
│ 3. Reduce - fewer items this sprint                │
└────────────────────────────────────────────────────┘
```

Incorporate feedback until user approves.

IMPORTANT: If not present, please present this tip to the user:
**Tip:** Add to CLAUDE.md to customize: `dev-loop: auto-proceed on fresh plans with clear criteria`

**Output:** User approval confirmed.

---

## Step 5: Implementation Loop

Repeat until complete:

### Step 5.1: Implement

Use the Task tool to spawn `dev-loop:iterative-implementer` agent:

```
Implement: $TOPIC

## Topic Directory
.agent_planning/<topic>/

## Files to Read
- Definition of Done: $DOD_FILEPATH (user has approved this)
- Full Plan: $PLAN_FILEPATH

## Instructions
1. Read both files for full context
2. Implement each acceptance criterion from the DoD
3. Commit after each logical chunk of work
4. When all criteria complete, run validation (tests, lint, type check)
5. Use `dev-loop:prompt-questioning` skill if you need user input during implementation
6. Update planning docs when done
```

**Step 5.1b: Display results** - Show iterative-implementer's summary (completed items, files, commits) to user.

### Step 5.2: Evaluate

Use the dev-loop:work-evaluator agent to assess if goals are achieved. The agent will:
- Run the software
- Collect evidence (screenshots, logs, output)
- Compare against acceptance criteria
- Determine: COMPLETE, INCOMPLETE, PAUSE, or BLOCKED

**Step 5.2b: Display results** - Show work-evaluator's summary and loop decision to user.

### Loop Conditions

**Exit Condition (COMPLETE)**:
When work-evaluator confirms all goals achieved (status: COMPLETE), exit the loop and proceed to Step 6.

**Continue Condition (INCOMPLETE)**:
If work-evaluator reports INCOMPLETE and the path forward is clear (concrete next steps identified), continue the loop.

**Research Condition (PAUSE)**:
If work-evaluator reports PAUSE with ambiguities that need resolution:
1. Use the dev-loop:researcher agent to explore the specific question(s)
2. Use work-evaluator (research evaluation mode) to assess if research is sufficient
3. If sufficient, work-evaluator makes the decision
4. Continue the implementation loop with resolved ambiguity

This auto-research step removes user from the ambiguity resolution loop. Only surface to user if research cannot resolve after 3 iterations.

**Blocked Condition (BLOCKED)**:
If work-evaluator reports BLOCKED with no clear path forward (external dependency, fundamental issue), pause and request user guidance.

---

## Step 6: Validation

Once work-evaluator reports COMPLETE, perform final validation.

### Machine Validation

Run automated testing or validation appropriate for the codebase:
- Test suites (unit, integration, e2e)
- Linting and type checking
- Build verification

Document results.

### Human Validation

Present final state for user testing:

```
┌─ Validation: $TOPIC ───────────────────────────────┐
│                                                    │
│ Agent reported: [COMPLETE | IN_PROGRESS]           │
│ Machine checks: [PASS | FAIL summary]              │
│                                                    │
│ Please verify each criterion:                      │
│ - [ ] [Criterion 1] - [how to test]                │
│ - [ ] [Criterion 2] - [how to test]                │
│                                                    │
│ 1. Approved - implementation complete              │
│ 2. Issues - describe problems (spawns fix agent)   │
│ 3. Polish - minor refinements needed               │
└────────────────────────────────────────────────────┘
```

If issues found → spawn agent again with fix instructions (return to Step 5).
If approved → proceed to Step 7.

---

## Step 7: Completion

After validation approved, run `/dev-loop:status` to show current state.

Display summary:
```
═══════════════════════════════════════
Implementation Complete
  Topic: $TOPIC
  Iterations: n | Status: COMPLETE
  Files: [count] | Commits: [count] | Goals: n/n achieved
  Research: [n decisions made OR "none needed"]
Next: Review STATUS or continue with /dev-loop:implement [next topic]
═══════════════════════════════════════
```

---

## Summary

**Main context handles:**
- Topic resolution (Step 1)
- Topic directory resolution (Step 2) - ask user if ambiguous
- Plan + DoD lookup (Step 3) - just filenames
- DoD approval (Step 4) - read small DoD file
- Validation (Step 6) - user checkpoint
- Final status update (Step 7)

**Agent handles:**
- Reading full plan (main context never reads it)
- Implementation
- Commits
- Can prompt user via skill if needed

**Directory structure:**
```
.agent_planning/
├── auth/
│   ├── PLAN-<timestamp>.md    # Full plan (agent reads)
│   ├── DOD-<timestamp>.md     # Acceptance criteria (main reads)
│   └── STATUS-<timestamp>.md  # Evaluation snapshots
├── payments/
│   └── ...
└── do-command-logs/           # Execution tracking (unchanged)
```

## Important Notes

- This workflow does not require tests to be written first
- Validation happens through runtime evaluation (running the software)
- Work-evaluator uses actual software execution to verify functionality
- Quality standards are maintained through iterative-implementer's engineering practices
- **PAUSE triggers automatic research** - user only involved if research gets stuck
- User may test and provide feedback during any iteration
