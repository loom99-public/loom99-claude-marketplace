---
name: "do:plan"
description: "Create comprehensive, confidence-rated implementation plans. Always use while planning.  Always use when the user mentions do:plan"
hooks:
   PreToolUse:
      - matcher: "*"
        hooks:
          - type: command
            command: "cat > /tmp/do-plan-pretooluse-$$.log"
   PostToolUse:
      - matcher: "*"
        hooks:
          - type: command
            command: "cat > /tmp/do-plan-posttooluse-$$.log"
   Stop:
      - matcher: "*"
        hooks:
          - type: command
            command: "cat > /tmp/do-plan-stop-$$.log"
---

# Plan Skill

Creates comprehensive, confidence-rated plans. Plans ALL work to some level of certainty.

## Core Concepts

**Sprint**: A coherent unit of related work (features, fixes, implementations). NOT time-based.

**Confidence Level**:
- **HIGH**: We know the work and how to do it. Ready for implementation.
- **MEDIUM**: General approach clear, but details need research. Primary goal: raise to HIGH.
- **LOW**: Significant unknowns. Primary goal: research and clarify before implementation.

**Principle**: Plan ALL work to some confidence level. Better to have 4 low-confidence sprints than 1 high-confidence sprint that ignores remaining work.

---

### Execute Command (Entry Point)

**Input**:
- `topic`: Area of focus (from $ARGUMENTS)

If `topic` is empty, search recent conversational context for the topic, or pick the next item from the 'bd ready' queue.

**Flow**:

```python
def execute_command(topic: str | None) -> str:
    """Entry point for /do:plan command"""

    # Step 1: Determine topic
    if not topic:
        # Evaluate project holistically using PROJECT_SPEC.md
        topic = evaluate_project_holistically()

    # Step 2: Resolve topic directory
    topic_dir = resolve_topic_directory(topic)

    # Step 3: Run evaluation
    evaluation = run_evaluation(topic, topic_dir)

    # Step 4: Handle evaluation results
    if evaluation.verdict == "BLOCKED":
        return surface_blockers_to_user(evaluation)
    elif evaluation.verdict == "PAUSE":
        resolve_ambiguities(evaluation)

    # Step 5: Generate sprint plans
    sprints = generate_sprint_plans(topic, topic_dir, evaluation)

    # Step 6: Validate plans
    validate_plans(sprints)

    # Step 7: Get user approval
    approval = present_for_approval(sprints)

    # Step 8: Complete
    return finalize_planning(topic, topic_dir, sprints, approval)
```

---

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

**Output:** Topic directory path (e.g., `.agent_planning/auth/`)

---

## Step 3: Evaluation

**Every plan requires fresh evaluation context.**

### Step 3a: Run Evaluation

Use the /Explore agent to evaluate the current state:

```
Topic: $TOPIC
Topic Directory: .agent_planning/<topic>/

Evaluate the current state of this topic area.
Write EVALUATION-<timestamp>.md to the topic directory.

Focus on:
1. What exists
2. What's missing
3. What needs changes (which files, components, architecture, etc)
4. Dependencies and risks
5. Ambiguities and unknowns (CRITICAL - list ALL uncertainties)
```

This produces: `EVALUATION-<timestamp>.md`

### Step 3b: Handle Evaluation Results

| Result | Action |
|--------|--------|
| **CONTINUE** | Proceed to Step 4 |
| **PAUSE** | Attempt resolution (Step 3c), then proceed |
| **BLOCKED** | Surface to user, ask how to proceed |
| **No verdict** | Treat as CONTINUE |

### Step 3c: Ambiguity Resolution (if PAUSE)

For each ambiguity, ask user with prepared options:

```
┌─ Clarification Needed ────────────────────────────────┐
│                                                       │
│ Question: [specific question]                         │
│                                                       │
│ Options:                                              │
│                                                       │
│ | Option | Approach | Pros | Cons |                   │
│ |--------|----------|------|------|                   │
│ | A (Standard) | [well-trodden path] | ... | ... |   │
│ | B (Creative) | [optimal improvement] | ... | ... | │
│ | C | [alternative if applicable] | ... | ... |      │
│                                                       │
│ Recommendation: [your suggestion and why]             │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**ALWAYS** include:
1. A "standard/well-trodden" option
2. An "optimal/creative improvement" option
3. Optionally a third alternative

---

## Step 4: Generate Sprint Plans

**CRITICAL: Plan ALL identified work. Do not artificially limit to 1 sprint.**

### Step 4a: Assess Work and Assign Confidence

Review evaluation and categorize ALL work items by confidence:

| Confidence | Criteria | Sprint Focus |
|------------|----------|--------------|
| HIGH | Known approach, clear implementation path | Implementation |
| MEDIUM | General direction clear, details uncertain | Research → Implementation |
| LOW | Significant unknowns, multiple approaches possible | Research → Raise confidence |

### Step 4b: Group into Sprints

**Each sprint**:
- Contains ONE confidence level (homogeneous)
- Represents a coherent unit of related work
- Has its OWN planning documents (not shared)

**Sprint naming**: `SPRINT-<timestamp>-<slug>.md`
- Slug is 2-3 words describing the work
- Example: `SPRINT-2024-12-15-120000-auth-core.md`

### Step 4c: Generate Plans

**For each sprint**, use the /Plan subagent:

```
Topic: $TOPIC
Topic Directory: .agent_planning/<topic>/
Sprint: <sprint-slug>
Confidence: HIGH | MEDIUM | LOW

Generate:
1. SPRINT-<timestamp>-<slug>-PLAN.md - Sprint plan
2. SPRINT-<timestamp>-<slug>-DOD.md - Acceptance criteria
3. SPRINT-<timestamp>-<slug>-CONTEXT.md - Implementation context

All files go in the topic directory.
```

### Sprint Plan Templates

**HIGH Confidence Sprint:**
```markdown
# Sprint: [Slug] - [Name]
Generated: <timestamp>
Confidence: HIGH
Status: READY FOR IMPLEMENTATION

## Sprint Goal
[One sentence describing deliverables]

## Scope
**Deliverables:**
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3, if applicable]

## Work Items

### P0: [First deliverable]
**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Technical Notes:**
- [Implementation guidance]

## Dependencies
- [Prerequisites]

## Risks
- [Known risks with mitigations]
```

**MEDIUM Confidence Sprint:**
```markdown
# Sprint: [Slug] - [Name]
Generated: <timestamp>
Confidence: MEDIUM
Status: RESEARCH REQUIRED

## Sprint Goal
[Raise confidence to HIGH through targeted research]

## Known Elements
- [What we DO know]

## Unknowns to Resolve
1. [Unknown 1] - Research approach: [how to find out]
2. [Unknown 2] - Research approach: [how to find out]

## Tentative Deliverables
- [Likely deliverable 1 - pending research]
- [Likely deliverable 2 - pending research]

## Research Tasks
- [ ] [Research task 1]
- [ ] [Research task 2]

## Exit Criteria (to reach HIGH confidence)
- [ ] [What must be true to proceed]
```

**LOW Confidence Sprint:**
```markdown
# Sprint: [Slug] - [Name]
Generated: <timestamp>
Confidence: LOW
Status: EXPLORATION REQUIRED

## Sprint Goal
[Reduce uncertainty and define approach]

## Current Understanding
[What little we know]

## Major Unknowns
1. [Unknown 1] - Impact: [why it matters]
2. [Unknown 2] - Impact: [why it matters]

## Exploration Options

### Option A: [Standard Approach]
| Aspect | Assessment |
|--------|------------|
| Complexity | [Low/Medium/High] |
| Risk | [Low/Medium/High] |
| Pros | [benefits] |
| Cons | [drawbacks] |

### Option B: [Creative Approach]
| Aspect | Assessment |
|--------|------------|
| Complexity | [Low/Medium/High] |
| Risk | [Low/Medium/High] |
| Pros | [benefits] |
| Cons | [drawbacks] |

## Questions for User
1. [Question 1]
2. [Question 2]

## Exit Criteria (to reach MEDIUM confidence)
- [ ] [What must be true to proceed]
```

### Step 4d: Check for Existing Plans

**CRITICAL: ALWAYS update existing plans rather than creating duplicates.**

Before creating any sprint plan:
1. List existing `SPRINT-*-PLAN.md` files in topic directory
2. Check if any cover the same work
3. If yes: UPDATE the existing plan, don't create new
4. If no: Create new plan

---

## Step 5: Handle Low/Medium Confidence

**For LOW or MEDIUM confidence sprints, the primary goal is raising confidence.**

### Present Options to User

```
┌─ Research Required: [Sprint Name] ────────────────────┐
│ Confidence: LOW/MEDIUM                                │
│                                                       │
│ Unknowns:                                             │
│ 1. [Unknown 1]                                        │
│ 2. [Unknown 2]                                        │
│                                                       │
│ Research Options:                                     │
│                                                       │
│ | Option | Approach | Effort | Outcome |              │
│ |--------|----------|--------|---------|              │
│ | A | [standard research path] | [est] | [result] |  │
│ | B | [alternative approach] | [est] | [result] |    │
│                                                       │
│ Which approach should we take? (or suggest your own) │
└───────────────────────────────────────────────────────┘
```

**After user input**: Update sprint plan with findings, re-assess confidence.

---

## Step 6: Validate Plans

For each sprint plan, verify:

| Check | Pass | Fail |
|-------|------|------|
| Every deliverable has acceptance criteria? | ✓ | INVALID |
| Acceptance criteria testable (2-5 per item)? | ✓ | Too vague |
| Confidence level appropriate for content? | ✓ | Reassess |
| Dependencies identified? | ✓ | Missing |
| LOW/MEDIUM have exit criteria? | ✓ | INVALID |

**Plans without acceptance criteria are INVALID.**

---

## Step 7: User Approval

Present ALL sprints for approval:

```
┌─ Sprint Plan Summary: $TOPIC ─────────────────────────┐
│                                                       │
│ Total Sprints: N                                      │
│                                                       │
│ ┌─ Sprint 1: [slug] ─────────────────────────────┐   │
│ │ Confidence: HIGH                                │   │
│ │ Deliverables:                                   │   │
│ │ - [Deliverable 1]                               │   │
│ │ - [Deliverable 2]                               │   │
│ └─────────────────────────────────────────────────┘   │
│                                                       │
│ ┌─ Sprint 2: [slug] ─────────────────────────────┐   │
│ │ Confidence: MEDIUM                              │   │
│ │ Focus: Research [topic]                         │   │
│ │ Exit criteria: [what raises to HIGH]            │   │
│ └─────────────────────────────────────────────────┘   │
│                                                       │
│ Options:                                              │
│ 1. Approve all                                        │
│ 2. Approve HIGH confidence only, discuss others      │
│ 3. Revise specific sprint                             │
│ 4. Reject and restart                                 │
└───────────────────────────────────────────────────────┘
```

---

## Step 8: Completion

Once user approves:

1. Record approval in `.agent_planning/<topic>/USER-RESPONSE-<timestamp>.md`
   - Include: APPROVED/PARTIAL/REJECT
   - List which sprint files were approved
   - Note any adjustments made

2. Confirm files saved:
   ```
   .agent_planning/<topic>/
   ├── EVALUATION-<timestamp>.md
   ├── SPRINT-<ts>-<slug>-PLAN.md      # Per sprint
   ├── SPRINT-<ts>-<slug>-DOD.md       # Per sprint
   ├── SPRINT-<ts>-<slug>-CONTEXT.md   # Per sprint
   └── USER-RESPONSE-<timestamp>.md
   ```

3. Display summary:

```
═══════════════════════════════════════════════════════
Plan Complete: $TOPIC

Sprints planned: N
├─ HIGH confidence: X (ready for implementation)
├─ MEDIUM confidence: Y (research first)
└─ LOW confidence: Z (exploration needed)

Files:
  .agent_planning/<topic>/
  ├── SPRINT-<ts>-<slug1>-PLAN.md [HIGH]
  ├── SPRINT-<ts>-<slug2>-PLAN.md [MEDIUM]
  └── ...

Next steps:
  HIGH confidence: /do:it $TOPIC
  MEDIUM/LOW: Run research, then re-plan
═══════════════════════════════════════════════════════
```

---

## Key Principles

1. **Plan ALL work** - Don't artificially limit scope. Plan everything to some confidence level.
2. **Confidence drives approach** - HIGH = implement. MEDIUM/LOW = research first.
3. **Homogeneous sprints** - Each sprint has ONE confidence level.
4. **Separate documents per sprint** - Never reuse or combine sprint plans.
5. **Update over create** - Always update existing plans for unworked topics.
6. **Options with tradeoffs** - When asking users, provide standard + creative options with comparison.
7. **Acceptance criteria mandatory** - Plans without them are INVALID.
8. **User approval required** - All plans need explicit approval before implementation.
