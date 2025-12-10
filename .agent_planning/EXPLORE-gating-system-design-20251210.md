# Gating System Design Exploration

**Generated**: 2025-12-10
**Updated**: 2025-12-10 (corrected architecture understanding)
**Purpose**: Design a comprehensive gating system that works across all agents

---

## Problem Statement

Subagents cannot use `AskUserQuestion` directly. When agents encounter decision points, they need a mechanism to:
1. **BLOCKING mode**: Always get user approval
2. **HYBRID mode**: Get user approval for high-risk decisions, auto-approve low-risk
3. **NONBLOCKING mode**: Auto-approve everything but document all decisions

All decisions (user-approved or auto-approved) must be documented in a comprehensive report.

---

## Critical Architecture Understanding

### Commands, Skills, and Agents are DIFFERENT

| Component | Runs In | Can Ask User? | Can Read Files? | Invoked By |
|-----------|---------|---------------|-----------------|------------|
| **Commands** | Main context | YES | YES | `/do:*` slash command |
| **Skills** | Main context | YES | YES | `Skill` tool from command |
| **Agents** | Subagent (Task tool) | NO | YES | `Task` tool from skill |

**Key insight**: Skills run in the **main Claude context**, NOT as subagents. This means:
- Skills CAN use `AskUserQuestion`
- Skills CAN use `Read`, `Write`, `Glob`, `Grep`
- Skills CAN do everything the main Claude can do

**Agents are the constraint**: They run as subagents via the Task tool with restricted tool access.

### Implication for Gating

**Gating checkpoints belong in SKILLS, not agents.**

Flow:
1. Command detects gate mode, writes gate config to state file
2. Command invokes skill (e.g., `tdd-workflow`)
3. Skill invokes agent (e.g., `test-driven-implementer`)
4. Agent writes decision files (cannot ask user)
5. Agent returns to skill
6. **Skill reads decision files, uses AskUserQuestion if needed**
7. Skill continues or pauses based on user input

---

## State Management (NOT in logs directory)

The `do-command-logs/` directory is for LOGGING, not state passing.

Create new directory for state:
```
.agent_planning/do-command-state/
  └── <EXEC_ID>/
      ├── GATE_CONFIG.txt        # Gate mode for this execution
      ├── DECISIONS/             # Decision files from agents
      │   ├── 001-<agent>-<decision>.txt
      │   ├── 002-<agent>-<decision>.txt
      │   └── ...
      └── GATE_REPORT.md         # Final decision audit report
```

### Intent Detection (Not Flags)
Commands detect intent via LLM, not `--flag` syntax:

| Intent signals | Gate mode |
|----------------|-----------|
| "carefully", "review each step", "approve everything", "manual" | BLOCKING |
| "guided", "help with major decisions", "review risks" | HYBRID |
| "autonomous", "auto-approve", "just do it", "move fast" | NONBLOCKING |
| *(no gate signals)* | **Prompt user to choose** |

### Execution Summarizer Pattern
The `execution-summarizer` agent aggregates partial files into final reports. We can:
- Extend partial format to include `## Decisions Made` section
- Have summarizer include decisions in final EXEC report
- Reference GATE_REPORT.md for decision audit

---

## Design: Gating Architecture

### Component 1: Gate Config File

**Created by**: Command (after intent detection or user prompt)
**Location**: `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt`
**Format**:
```
GATE_MODE: BLOCKING | HYBRID | NONBLOCKING
EXEC_ID: <uuid>
CREATED: <timestamp>
COMMAND: /do:<command>
```

### Component 2: Decision Event Files

**Created by**: Agents at decision points
**Location**: `.agent_planning/do-command-state/<EXEC_ID>/DECISIONS/<SEQ>-<agent>-<decision-id>.txt`
**Format**:
```
DECISION_ID: <uuid>
EXEC_ID: <exec_id>
SEQUENCE: <n>
AGENT: <agent-name>
TIMESTAMP: <iso-timestamp>
RISK_LEVEL: HIGH | MEDIUM | LOW
CATEGORY: architecture | technology | implementation | testing | documentation

## Decision
<What was decided>

## Options Considered
- A: <option> - <tradeoffs>
- B: <option> - <tradeoffs>
- C: <option> - <tradeoffs>

## Chosen
<Which option and why>

## Impact If Wrong
<Consequences of wrong choice>

## Auto-Approve Rationale (if HYBRID/NONBLOCKING)
<Why this can be auto-approved in non-BLOCKING mode>
```

### Component 3: Gating Controller Skill

**File**: `plugins/do-more-now/skills/gating-controller.md`
**Purpose**: Process decisions and determine what needs user approval
**Invoked by**: Workflow skills (tdd-workflow, iterative-workflow) after each agent returns

**Key insight**: Since skills run in main context, this skill CAN use `AskUserQuestion` directly!

```markdown
---
name: gating-controller
description: Process pending decisions, ask user for approvals if needed, document all decisions
---

# Gating Controller

## Step 1: Read Gate Config
Read `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt`
Extract: GATE_MODE

## Step 2: Collect Pending Decisions
Glob: `.agent_planning/do-command-state/<EXEC_ID>/DECISIONS/*.txt`
Read each decision file that hasn't been processed yet

## Step 3: Process Each Decision

For each unprocessed decision:

  **BLOCKING mode**:
    → Use AskUserQuestion to present decision to user
    → Wait for approval
    → Mark decision as USER_APPROVED or USER_REJECTED

  **HYBRID mode**:
    If RISK_LEVEL == HIGH:
      → Use AskUserQuestion to present decision to user
      → Mark as USER_APPROVED or USER_REJECTED
    Else:
      → Mark as AUTO_APPROVED
      → Document rationale

  **NONBLOCKING mode**:
    → Mark as AUTO_APPROVED
    → Document rationale

## Step 4: Update Decision Files

Write approval status back to decision file:
```
APPROVAL_STATUS: USER_APPROVED | AUTO_APPROVED | USER_REJECTED
APPROVED_AT: <timestamp>
APPROVAL_RATIONALE: <if auto-approved, why>
USER_FEEDBACK: <if user provided alternative, capture it>
```

## Step 5: Return Status

If any USER_REJECTED:
  Return: { continue: false, rejected: [...], reason: "..." }

Else:
  Return: { continue: true, decisions_processed: n }
```

### Component 4: Modified Workflow Skills

**Files**: `tdd-workflow.md`, `iterative-workflow.md`, etc.

Add gating checkpoints between agent invocations. Since skills run in main context, they can directly invoke the gating-controller skill which will handle user interaction:

```markdown
## Step 1b: Gating Checkpoint

After each agent completes, invoke `do:gating-controller` skill:

The gating-controller will:
1. Read pending decisions from state directory
2. If BLOCKING or HIGH_RISK in HYBRID: Use AskUserQuestion directly
3. If NONBLOCKING or LOW_RISK: Auto-approve and document
4. Return { continue: true/false }

If continue == false (user rejected):
  → Exit workflow with rejection details

If continue == true:
  → Continue to next step
```

**No "return to command" needed** - skills handle user interaction directly!

### Component 5: Modified Commands

**Files**: `it.md`, `plan.md`, etc.

Add gate mode detection and user prompting. Commands run in main context, so they CAN use AskUserQuestion:

```markdown
## Step 0: Detect Gate Mode

Analyze $ARGUMENTS for gate intent using LLM (NOT flags):

| Signals | Mode |
|---------|------|
| "carefully", "approve each", "manual", "review everything" | BLOCKING |
| "guided", "review major", "help with risks", "important decisions" | HYBRID |
| "autonomous", "auto", "just do it", "move fast", "trust your judgment" | NONBLOCKING |

If no signals detected:
  Use AskUserQuestion:
  "How should I handle decisions during this work?"
  - BLOCKING: "Ask me to approve every significant choice"
  - HYBRID: "Ask about major/risky decisions, auto-approve obvious ones" (Recommended)
  - NONBLOCKING: "Make all decisions autonomously and document them for review"

## Step 0b: Initialize State Directory

Create: `.agent_planning/do-command-state/<EXEC_ID>/`
Create: `.agent_planning/do-command-state/<EXEC_ID>/DECISIONS/`
Write: `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt`
```

### Component 6: Gate Report Generation

**Extended**: `execution-summarizer.md`

Add decision aggregation to the EXEC report:

```markdown
## Decisions Made

| # | Decision | Risk | Status | Agent |
|---|----------|------|--------|-------|
| 1 | Use class-based approach | LOW | AUTO_APPROVED | test-driven-implementer |
| 2 | JWT over sessions | HIGH | USER_APPROVED | researcher |
| 3 | PostgreSQL for storage | MEDIUM | AUTO_APPROVED | project-architect |

### Decision Details

#### Decision 1: Use class-based approach
- **Risk**: LOW
- **Options**: Class-based (chosen), Functional, Hybrid
- **Rationale**: Matches existing codebase patterns
- **Auto-approved because**: Low risk, clear precedent in codebase
```

---

## Flow Diagrams

### BLOCKING Mode Flow

```
User: /do:it implement auth carefully

Command (main context):
  1. Detect "carefully" → BLOCKING mode
  2. Create state dir, write GATE_CONFIG
  3. Invoke tdd-workflow skill

tdd-workflow skill (main context):
  4. Invoke functional-tester agent (Task tool → subagent)

  functional-tester agent (subagent - CANNOT ask user):
    5. Makes decision about test approach
    6. Writes DECISION file to state dir
    7. Returns to skill

  8. Invoke gating-controller skill (still main context!)

  gating-controller skill (main context - CAN ask user):
    9. Reads DECISION files
    10. Uses AskUserQuestion directly for each decision
    11. User approves/rejects
    12. Updates DECISION file with approval status
    13. Returns { continue: true/false }

  14. If continue, invoke next agent
  15. Repeat until workflow complete

Command:
  16. Invoke execution-summarizer
  17. Display GATE_REPORT with all decisions
```

### HYBRID Mode Flow

```
User: /do:it implement auth

Command (main context):
  1. No gate signals detected
  2. Use AskUserQuestion: "How should I handle decisions?"
  3. User selects HYBRID
  4. Create state dir, write GATE_CONFIG (HYBRID)
  5. Invoke iterative-workflow skill

iterative-workflow skill (main context):
  6. Invoke iterative-implementer agent (Task → subagent)

  iterative-implementer agent (subagent):
    7. Makes LOW risk decision (naming) → Writes DECISION file
    8. Makes HIGH risk decision (architecture) → Writes DECISION file
    9. Returns to skill

  10. Invoke gating-controller skill

  gating-controller skill (main context):
    11. Reads DECISION files
    12. LOW risk → AUTO_APPROVED (document rationale)
    13. HIGH risk → AskUserQuestion (user approval needed)
    14. User approves architecture decision
    15. Returns { continue: true }

  16. Continue workflow
```

### NONBLOCKING Mode Flow

```
User: /do:it implement auth, trust your judgment

Command (main context):
  1. Detect "trust your judgment" → NONBLOCKING mode
  2. Create state dir, write GATE_CONFIG (NONBLOCKING)
  3. Invoke tdd-workflow skill

tdd-workflow skill (main context):
  4. Invoke agents in sequence

  Each agent (subagent):
    5. Makes decisions → Writes DECISION files
    6. Returns to skill

  7. Invoke gating-controller skill after each agent

  gating-controller skill (main context):
    8. Reads DECISION files
    9. ALL decisions → AUTO_APPROVED (document rationale)
    10. NO AskUserQuestion calls (full autonomy)
    11. Returns { continue: true }

  12. Workflow completes without interruption

Command:
  13. Invoke execution-summarizer
  14. GATE_REPORT shows all decisions with rationale
  15. User can audit after the fact
```

---

## Risk Classification Criteria

### HIGH Risk (Always review in HYBRID)
- Architecture decisions (patterns, structure)
- Technology choices (frameworks, databases, services)
- API contract changes (breaking changes)
- Security-related decisions
- Performance tradeoffs with user-facing impact
- Decisions that are expensive to reverse

### MEDIUM Risk (Document well, may auto-approve)
- Implementation approach (TDD vs iterative)
- Test strategy within established framework
- Module organization within existing patterns
- Error handling approach
- Dependency choices within established categories

### LOW Risk (Auto-approve, document)
- Variable/function naming
- Code formatting within established style
- Documentation content
- Log level selections
- Internal optimization without behavioral change
- Refactoring within established patterns

---

## Files to Create/Modify

### New Files

1. **`skills/gating-controller.md`** - Gate processing skill (runs in main context, CAN use AskUserQuestion)

### Modified Files

**Commands** (add Step 0 gate detection + state directory init):
- `commands/it.md`
- `commands/plan.md`
- `commands/explore.md`
- `commands/research.md`
- `commands/chores.md`
- `commands/docs.md`
- `commands/release.md`

**Workflow Skills** (add gating checkpoints after agent invocations):
- `skills/tdd-workflow.md`
- `skills/iterative-workflow.md`
- `skills/refactor.md`
- `skills/debug.md`
- `skills/fix.md`
- `skills/review.md`
- `skills/add-tests.md`

**Agents** (add decision logging - write DECISION files):
- `agents/test-driven-implementer.md`
- `agents/iterative-implementer.md`
- `agents/functional-tester.md`
- `agents/project-architect.md`
- `agents/researcher.md`
- `agents/project-evaluator.md`
- `agents/work-evaluator.md`
- `agents/status-planner.md`
- `agents/product-visionary.md`

**Execution Tracking**:
- `agents/execution-summarizer.md` - Add GATE_REPORT generation

**Hooks** (optional):
- `bin/init.py` - Create state directory structure at session start

---

## Implementation Priority

### Phase 1: Foundation (Critical)
1. Create GATE_CONFIG file format and init hook integration
2. Create DECISION file format
3. Create `gating-controller.md` skill
4. Modify one command (`it.md`) as pilot

### Phase 2: Agent Integration
5. Add decision logging to key agents:
   - `test-driven-implementer.md`
   - `iterative-implementer.md`
   - `researcher.md`
   - `project-architect.md`

### Phase 3: Workflow Integration
6. Add gating checkpoints to workflow skills:
   - `tdd-workflow.md`
   - `iterative-workflow.md`

### Phase 4: Full Rollout
7. Add gate detection to all commands
8. Add decision logging to remaining agents
9. Enhance execution-summarizer with decision report

### Phase 5: Polish
10. Risk classification refinement
11. Report formatting improvements
12. User experience refinement

---

## Open Questions

1. **Checkpoint granularity**: Gate after every agent, or batch decisions?
   - Recommendation: Batch per workflow step (fewer interruptions)

2. **Decision persistence**: Keep decision files after execution or cleanup?
   - Recommendation: Cleanup partials, keep GATE report in EXEC file

3. **Risk override**: Can user pre-approve all decisions of certain types?
   - Future enhancement: Allow `HYBRID+TRUST_TECH_CHOICES`

4. **Resume support**: If user rejects a decision, can they provide alternative?
   - Yes, AskUserQuestion can include "Other" option for custom input
