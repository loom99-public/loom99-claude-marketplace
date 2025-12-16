---
argument-hint: [area of focus]
description: Evaluate the project and create a focused implementation plan for ONE sprint. Evaluates first, then plans.
---

# Plan Command

Creates a focused, sprint-sized plan. Automatically evaluates first if needed.

## Step 1: Determine Topic

<task-focus>
$ARGUMENTS
</task-focus>

If task-focus is empty, evaluate the project holistically using PROJECT_SPEC.md.

**Output:** A topic string.

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

   **No similar directories** → Create new directory:
   ```bash
   mkdir -p .agent_planning/<topic-slug>
   ```

**Tip:** Add to CLAUDE.md to customize: `dev-loop: auto-select directories without asking`

**Output:** Topic directory path (e.g., `.agent_planning/auth/`)

---

## Step 3: Evaluation

**Every plan requires fresh evaluation context.**

### Step 3a: Run Evaluation

**CRITICAL: You MUST spawn the evaluator AND continue to Step 4 after it completes.**

Use the Task tool with `subagent_type: "dev-loop:project-evaluator"` to evaluate the current state:

```
Topic: $TOPIC
Topic Directory: .agent_planning/<topic>/

Evaluate the current state of this topic area.
Write STATUS-<timestamp>.md to the topic directory.

Focus on:
1. What exists
2. What's missing
3. What needs changes
4. Dependencies and risks
5. Ambiguities
```

This produces evaluation files in the topic directory:
- `STATUS-<timestamp>.md` - Current state snapshot

### Step 3b: Handle Evaluation Results

**DEFAULT: Always proceed to Step 4 unless explicitly BLOCKED.**

| Result | Action |
|--------|--------|
| **CONTINUE** | Proceed to Step 4 immediately |
| **PAUSE** | Attempt quick resolution (Step 3c), then proceed to Step 4 |
| **BLOCKED** | Surface to user, ask how to proceed |
| **No verdict** | Treat as CONTINUE - proceed to Step 4 |

**IMPORTANT**: Do not stop after evaluation. The plan command must always attempt to generate a plan.

### Step 3c: Quick Ambiguity Resolution (if PAUSE)

Spend no more than 2-3 minutes on this. Then proceed to Step 4.

For each ambiguity:
1. **Defer** (preferred) - Note as out-of-scope, plan around it
2. **Ask user** - Quick clarifying question
3. **Research** - Only if critical and fast (`/dev-loop:research`)

After attempting resolution, **proceed to Step 4 regardless**. Planning can happen with noted ambiguities.

---

## Step 4: Generate Plan

**CRITICAL: After project-evaluator completes, you MUST continue to this step. Do not stop.**

**Plan ONLY what can be accomplished in ONE sprint (2-3 significant deliverables).**

Use the Task tool with `subagent_type: "dev-loop:status-planner"` agent with:

```
Topic: $TOPIC
Topic Directory: .agent_planning/<topic>/

Read the evaluation files in the topic directory.
Generate:
1. PLAN-<timestamp>.md - Full sprint plan
2. DOD-<timestamp>.md - Acceptance criteria only (separate file)

Both files go in the topic directory.
```

**Plan template:**
```markdown
# Sprint Plan: [Task Name]
Generated: <timestamp>

## Sprint Goal
[One sentence describing what this sprint delivers]

## Scope
**In scope (this sprint):**
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3, if applicable]

**Explicitly out of scope (future sprints):**
- [Item deferred]

## Work Items

### P0: [First deliverable]
**Acceptance Criteria (REQUIRED):**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Technical Notes:**
- [Implementation guidance]

### P1: [Second deliverable]
...

## Dependencies
- [Prerequisites]

## Risks
- [Potential issues]
```

**CRITICAL**: The planner MUST limit scope to 2-3 deliverables.

---

## Step 5: Validate Plan

Use dev-loop:work-evaluator agent to check:

| Check | Pass | Fail |
|-------|------|------|
| Every deliverable has acceptance criteria? | ✓ | INVALID |
| Acceptance criteria testable (2-5 per item)? | ✓ | Too vague |
| Scope reasonable for one sprint? | ✓ | Too large |
| Dependencies identified? | ✓ | Missing |

**Plans without acceptance criteria are INVALID.** Re-run planner.

---

## Step 6: User Approval

Present plan summary for approval:

```
┌─ Sprint Plan Ready for Review ─────────────────────┐
│ Task: [name]                                       │
│ Sprint Goal: [one sentence]                        │
│                                                    │
│ Deliverables (this sprint):                        │
│ 1. [Deliverable 1]                                 │
│ 2. [Deliverable 2]                                 │
│ 3. [Deliverable 3, if any]                         │
│                                                    │
│ Deferred to future sprints:                        │
│ - [List of out-of-scope items]                     │
│                                                    │
│ Options:                                           │
│ 1. Approve - plan looks good                       │
│ 2. Adjust scope - change what's included           │
│ 3. Add context - more info needed                  │
│ 4. Reject - start over with different approach     │
└────────────────────────────────────────────────────┘
```

- **Approve**: Proceed to completion
- **Adjust scope**: Modify and re-validate
- **Add context**: Ask questions, update plan
- **Reject**: Return to evaluation with new direction

**Tip:** Add to CLAUDE.md to customize: `dev-loop: auto-approve valid plans with clear acceptance criteria`

---

## Step 7: Completion

Once user approves:

1. Confirm files saved to topic directory:
   - `.agent_planning/<topic>/PLAN-<timestamp>.md`
   - `.agent_planning/<topic>/DOD-<timestamp>.md`

2. Archive old plans (keep max 4 per type)

3. Display summary:

```
═══════════════════════════════════════════════════════
Plan Complete
  Topic: [name]
  Directory: .agent_planning/<topic>/

  Files:
  - PLAN-<timestamp>.md
  - DOD-<timestamp>.md

  Sprint Scope: [n] deliverables

Next: /dev-loop:implement $TOPIC
═══════════════════════════════════════════════════════
```

---

## Summary

**Directory structure:**
```
.agent_planning/
├── auth/
│   ├── STATUS-<timestamp>.md   # Evaluation snapshots
│   ├── EVAL-<timestamp>.md     # Gap analysis
│   ├── PLAN-<timestamp>.md     # Full plan
│   └── DOD-<timestamp>.md      # Acceptance criteria only
├── payments/
│   └── ...
└── do-command-logs/            # Execution tracking (unchanged)
```

**Key principles:**
1. Evaluate first - fresh context required
2. One sprint only - 2-3 deliverables max
3. Resolve ambiguity - don't plan around unclear requirements
4. Acceptance criteria mandatory - plans without them are invalid
5. User approval required - plan must be accepted before implementation
