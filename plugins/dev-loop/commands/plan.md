---
argument-hint: [area of focus]
description: Evaluate the project and create a focused implementation plan for the scope of work. Evaluates first, then plans.
---

# Plan Command

Creates a focused, achievable plan. Automatically evaluates first if needed.

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
3. What needs changes (which files, components, architecture, etc)
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

### Step 3c: Ambiguity Resolution (if PAUSE)

Spend no more than 2-3 minutes on this. Then proceed to Step 4. If user stops you during this, pick up right where you left off.

For each ambiguity, do the minimal amount to achieve certainty:
1. **Ask user** - Quick clarifying questions. Allow user to provide suggestions such as "do research", etc. If user suggests research, ask user again with results of research.
2. **Research** - If critical and fast (`/lp:research`), do this before asking user. Always ask user again AFTER research, unless you are very certain.
3. **Defer** (last resort) - Note as out-of-scope, plan around it. This should be used as last resort. It's better to plan more work than less.

---

## Step 4: Generate Plan

**CRITICAL: After project-evaluator completes, you MUST continue to this step. Do not stop.**

**Plan at MINIMUM one sprint worth of work containing 2-3 significant deliverables.**

**Your GOAL is to plan as much work as you have CERTAINTY around: strategic value, architecture, dependency ordering, implementation details.**

**Prefer UPDATING an existing plan vs CREATING a new plan to previously planned work.**

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

Present Deliverable and Definition of Done summary for approval:

```
┌─ Please Review: Sprint Plan for $TOPIC ────────────┐
│ Task: [name]                                       │
│ Sprint Goal: [one sentence]                        │
│                                                    │
│ Deliverables (this sprint):                        │
│ 1. [Deliverable 1]                                 │
│ 2. [Deliverable 2]                                 │
│ 3. [Deliverable 3, if any]                         │
│                                                    │
│ Acceptance Criteria:                               │
│ - [ ] [Criterion 1]                                │
│ - [ ] [Criterion 2]                                │
│ - [ ] [Criterion 3]                                │
│                                                    │
│ Deferred to future sprints:                        │
│ - [List of out-of-scope items]                     │
│                                                    │
│ Options:                                           │
│ 1. Approve - looks good!                           │
│ 2. Revise - adjust, add context, give feedback     │
│ 3. Reject - start over with different approach     │
└────────────────────────────────────────────────────┘
```

- **Approve**: Proceed to completion
- **Adjust scope**: Modify and re-validate
- **Add context**: Ask questions, update plan
- **Reject**: Return to evaluation with new direction

**Tip:** Add to CLAUDE.md to customize: `dev-loop: auto-approve valid plans with clear acceptance criteria`

---

## Step 7: Completion and Auto-Chain

Once user approves:

1. Record user response to approval question in `.agent_planning/<topic>/USER-RESPONSE-<timestamp>.md`.  This should be either 'APPROVED', 'ADJUST', or 'REJECT' with appropriate context about the answer (why it was rejected or how it was adjusted, if it was).  This file is critical to proceeding and serves as a full user approval of the plan as written.  Include the specific filenames that are part of the plan that was approved.

2. Confirm files saved to topic directory:
   - `.agent_planning/<topic>/PLAN-<timestamp>.md`
   - `.agent_planning/<topic>/DOD-<timestamp>.md`
   - ...

3. Display summary:

```
═══════════════════════════════════════════════════════
Plan Complete
  Topic: [name]
  
  Directory structure:
   .agent_planning/
   ├── <topic>/
   │   ├── STATUS-<timestamp>.md          # Evaluation snapshots
   │   ├── EVAL-<timestamp>.md            # Gap analysis
   │   ├── PLAN-<timestamp>.md            # Full plan
   │   ├── USER-RESPONSE-<timestamp>.md   # User response to plan (Approved/Rejected)
   │   └── DOD-<timestamp>.md             # Definition of Done / Acceptance Criteria
   └── <topic>/
       └── ...

  Sprint Deliverables:
   - Item1
   - Item2
   - ...

Next: /lp:impl $TOPIC
═══════════════════════════════════════════════════════
```

4. **Auto-chain to implementation**:

Display to user:

**Tip:** You can specify the criteria under which we should automatically plan, such as the risk level, complexity, or uncertainty that is acceptable by adding a note to your CLAUDE.md file.  e.g., `dev-loop: auto-chain plan to implement for all low risk, low complexity plans with little uncertainty`.  By default it will ask you about every plan.

Perform this action:

**ONLY** when a user has requested auto-chain to implementation for some plans:
   Automatically execute command `/lp:impl $TOPIC`.  Do NOT ask for permission - immediately begin implementation using the approved plan.
   This ONLY takes effect for plans that match the users criteria for automatic implementation, e.g., the risk level, complexity, and uncertainty is within the user's acceptable range.

---


## Key principles:

1. Evaluate first - fresh context required
2. One sprint only - 2-3 deliverables max
3. All open questions must be resolved - don't plan around unclear requirements
4. DOD (Acceptance criteria) mandatory - plans without them are invalid
5. User approval required - plan & DOD must be accepted BEFORE WE EXIT PLANNING
