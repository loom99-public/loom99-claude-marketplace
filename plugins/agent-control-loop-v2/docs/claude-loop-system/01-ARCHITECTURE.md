# Architecture: Claude Code Implementation

This document describes how the minimal control loop system maps to Claude Code's capabilities: commands, agents, skills, hooks, and scripts.

---

## Component Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SLASH COMMANDS                                 │
│   (Entry points - invoke agents, trigger hooks)                          │
│                                                                          │
│   /loop:init    /loop:phase    /loop:status    /loop:escalate           │
│   /design:propose   /design:accept   /design:ship   /design:sync        │
│   /intake:create    /intake:compile                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              HOOKS                                       │
│   (Automatic injection - no manual invocation)                           │
│                                                                          │
│   Pre-command: Inject compressed artifacts into context                  │
│   Post-command: Consistency checks, artifact validation                  │
│   Pre-tool: Boundary violation detection                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              AGENTS                                      │
│   (Focused, single-purpose - zero conditionals)                          │
│                                                                          │
│   Governor          - Owns execution plane, drives phase ritual          │
│   Design-Curator    - Owns design plane, manages proposals               │
│   Intake-Compiler   - Transforms intake into design proposals            │
│   Escalation-Handler - Presents decision gates via AskUserQuestion       │
│   Artifact-Validator - Validates artifact structure and consistency      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              SKILLS                                      │
│   (Shared behaviors - called by agents)                                  │
│                                                                          │
│   phase-ritual      - 5-step ritual procedure                            │
│   artifact-io       - Read/write/validate artifacts                      │
│   blocker-scoring   - Score and rank blockers                            │
│   metric-measurement - Measure and track metrics                         │
│   decision-gate     - Present AskUserQuestion for human decisions        │
│   design-lifecycle  - State machine for proposals                        │
│   compressed-artifacts - Generate A₀/B₀ compressed forms                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              SCRIPTS                                     │
│   (Deterministic operations - called by skills)                          │
│                                                                          │
│   init-governance.sh    - Create governance/ directory structure         │
│   measure-metrics.sh    - Run metric measurement commands                │
│   validate-boundary.sh  - Check imports against boundary law             │
│   scan-boundaries.sh    - Detect legacy/new code boundaries              │
│   archive-slice.sh      - Archive completed work                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Flow: How Components Interact

### Flow 1: /loop:phase (Normal Phase Execution)

```
User invokes: /loop:phase
         │
         ▼
┌─────────────────────────────────────────┐
│ HOOK: pre-command                        │
│ - Check governance/ exists               │
│ - Inject compressed A₀ (always-on)       │
│ - Inject relevant B₀ (playbooks)         │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ COMMAND: /loop:phase                     │
│ - Spawn Governor agent                   │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ AGENT: Governor                          │
│ - Use phase-ritual skill                 │
│   - Step 1: artifact-io skill (read)     │
│   - Step 2: blocker-scoring skill        │
│   - Step 3: Plan generation              │
│   - Step 4: Delegate/execute             │
│   - Step 5: artifact-io skill (write)    │
│ - If escalation needed:                  │
│   - Use decision-gate skill              │
│   - Present AskUserQuestion              │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ HOOK: post-command                       │
│ - Validate artifacts updated             │
│ - Check metrics moved monotonically      │
│ - Suggest next action                    │
└─────────────────────────────────────────┘
```

### Flow 2: /loop:init (Initialization)

```
User invokes: /loop:init [goal]
         │
         ▼
┌─────────────────────────────────────────┐
│ COMMAND: /loop:init                      │
│ - Prompt for goal (if not provided)      │
│ - Spawn Governor agent for init          │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ AGENT: Governor (init mode)              │
│ - Use artifact-io skill                  │
│   - SCRIPT: scan-boundaries.sh           │
│   - Present boundary options             │
│   - SCRIPT: init-governance.sh           │
│ - Use decision-gate skill                │
│   - Prompt for non-goals, DoD, metrics   │
│ - Use metric-measurement skill           │
│   - SCRIPT: measure-metrics.sh           │
│   - Capture baseline values              │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ SKILL: compressed-artifacts              │
│ - Generate A₀ from TARGET + BOUNDARY     │
│ - Generate B₀ playbooks from goal type   │
│ - Write to governance/compressed/        │
└─────────────────────────────────────────┘
```

### Flow 3: /design:propose → /design:accept (Design Lifecycle)

```
User invokes: /design:propose [description]
         │
         ▼
┌─────────────────────────────────────────┐
│ COMMAND: /design:propose                 │
│ - Spawn Design-Curator agent             │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ AGENT: Design-Curator                    │
│ - Use design-lifecycle skill             │
│   - Create /design/proposals/P-####/     │
│   - Generate PROPOSAL.md, STATUS.md      │
│ - Use decision-gate skill                │
│   - Prompt for goals, constraints        │
└─────────────────────────────────────────┘
         │
         │  (Later, user reviews and decides)
         ▼
User invokes: /design:accept P-0001
         │
         ▼
┌─────────────────────────────────────────┐
│ AGENT: Design-Curator                    │
│ - Use design-lifecycle skill             │
│   - Transition: Proposed → Accepted      │
│   - Create /design/active/A-####/        │
│   - Generate GOVERNANCE-DELTA.md         │
│ - Use decision-gate skill (Gate #1)      │
│   - AskUserQuestion: Confirm acceptance  │
│   - Present governance deltas            │
│   - Present risks                        │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ SKILL: artifact-io                       │
│ - Apply GOVERNANCE-DELTA to live/*       │
│ - Update DESIGN_LINKS.md                 │
│ - Regenerate compressed artifacts        │
└─────────────────────────────────────────┘
```

---

## Directory Structure

### Plugin Directory

```
plugins/agent-control-loop/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── agents/
│   ├── governor.md           # Execution plane owner
│   ├── design-curator.md     # Design plane owner
│   ├── intake-compiler.md    # Intake → Design
│   ├── escalation-handler.md # Human decision gates
│   └── artifact-validator.md # Artifact validation
├── commands/
│   ├── init.md               # /loop:init
│   ├── phase.md              # /loop:phase
│   ├── status.md             # /loop:status
│   ├── escalate.md           # /loop:escalate
│   ├── design-propose.md     # /design:propose
│   ├── design-accept.md      # /design:accept
│   ├── design-ship.md        # /design:ship
│   ├── design-sync.md        # /design:sync
│   ├── intake-create.md      # /intake:create
│   └── intake-compile.md     # /intake:compile
├── skills/
│   ├── phase-ritual/
│   │   └── SKILL.md
│   ├── artifact-io/
│   │   └── SKILL.md
│   ├── blocker-scoring/
│   │   └── SKILL.md
│   ├── metric-measurement/
│   │   └── SKILL.md
│   ├── decision-gate/
│   │   └── SKILL.md
│   ├── design-lifecycle/
│   │   └── SKILL.md
│   └── compressed-artifacts/
│       └── SKILL.md
├── hooks/
│   └── hooks.json            # Hook definitions
├── scripts/
│   ├── init-governance.sh
│   ├── measure-metrics.sh
│   ├── validate-boundary.sh
│   ├── scan-boundaries.sh
│   └── archive-slice.sh
└── docs/
    └── _now/
        └── claude-loop-system/  # These spec docs
```

### Project Directory (created by /loop:init)

```
project-root/
├── governance/
│   ├── live/                    # Binding execution plane
│   │   ├── TARGET.md
│   │   ├── BOUNDARY.md
│   │   ├── BLOCKERS.md
│   │   ├── METRICS.md
│   │   └── DESIGN_LINKS.md
│   ├── compressed/              # Pre-generated compressed artifacts
│   │   ├── A0-contract.md       # Always-on contract
│   │   └── B0-playbooks/        # Task-type playbooks
│   │       ├── migration.md
│   │       ├── refactor.md
│   │       └── feature.md
│   ├── roadmap/                 # Future work (non-binding)
│   │   ├── index.md
│   │   └── slices/
│   │       └── S-####-slug/
│   ├── completed/               # Historical record (immutable)
│   │   ├── index.md
│   │   └── slices/
│   │       └── S-####-slug__YYYY-MM-DD/
│   ├── PHASE-LOG.md             # Append-only phase history
│   └── HISTORY.md               # Append-only decision ledger
└── design/
    ├── README.md                # Taxonomy, state machine, rules
    ├── index.md                 # Curated entrypoints
    ├── current/                 # Authoritative big picture
    │   └── north-star/
    │       ├── OVERVIEW.md
    │       ├── ARCHITECTURE.md
    │       ├── CONSTRAINTS.md
    │       └── adr/
    ├── proposals/               # Candidate futures
    │   └── P-####-slug/
    │       ├── PROPOSAL.md
    │       ├── STATUS.md
    │       └── EVIDENCE/
    ├── active/                  # Under execution
    │   └── A-####-slug/
    │       ├── SPEC.md
    │       ├── STATUS.md
    │       ├── GOVERNANCE-DELTA.md
    │       └── LINKS.md
    ├── intake/                  # Human intent injection
    │   └── I-####-slug/
    │       ├── INTAKE.md
    │       ├── STATUS.md
    │       └── NOTES.md
    └── archive/                 # Immutable history
        ├── YYYY/
        └── rejected/
```

---

## Design Principles

### 1. Agents Are Focused and Single-Purpose

Each agent has ONE job. Zero conditionals in flow logic.

**Good:**
```
Governor agent → always runs phase ritual
Design-Curator agent → always manages design lifecycle
```

**Bad:**
```
General agent → if (init) do X, else if (phase) do Y, else if (design) do Z
```

Agents call skills for shared behavior. Skills never make routing decisions.

### 2. Skills Contain Shared Behaviors

Skills are reusable procedures called by multiple agents.

| Skill | Used By |
|-------|---------|
| `artifact-io` | Governor, Design-Curator, Artifact-Validator |
| `decision-gate` | Governor, Design-Curator, Escalation-Handler |
| `blocker-scoring` | Governor |
| `metric-measurement` | Governor |
| `design-lifecycle` | Design-Curator |

### 3. Scripts Handle Deterministic Operations

Scripts are bash files for operations that must be reliable and repeatable:
- File creation with exact structure
- Running measurement commands
- Scanning for patterns (grep, find)
- Archiving/moving files

Agents use skills, skills call scripts.

```
Agent → Skill → Script
  │        │        │
  │        │        └─ Deterministic (bash)
  │        └─ Procedural (agent prompt)
  └─ Goal-driven (focused agent)
```

### 4. Hooks Inject Context Automatically

Hooks ensure critical context is always present without manual invocation:

- **Pre-command hooks:** Inject compressed A₀/B₀ before any `/loop:` command
- **Post-command hooks:** Validate artifacts, suggest next action
- **Pre-tool hooks:** Detect boundary violations before writes

Hooks are the "always-on" enforcement layer.

### 5. Human Gates Use AskUserQuestion

All mandatory human decision points use `AskUserQuestion` with structured options.

**Never:** Free-form "edit this file and re-run"
**Always:** Structured options with clear consequences

### 6. Compressed Artifacts Are Pre-Generated

A₀ (always-on contract) and B₀ (playbooks) are generated at init time and on artifact changes. They are committed to `governance/compressed/`.

Hooks inject them; they are not regenerated on-the-fly.

---

## Command Namespace

| Namespace | Purpose |
|-----------|---------|
| `/loop:*` | Execution plane (phase ritual, governance) |
| `/design:*` | Design plane (proposals, lifecycle) |
| `/intake:*` | Intent injection (human → design) |

### Core Commands

| Command | Agent | Purpose |
|---------|-------|---------|
| `/loop:init` | Governor | Bootstrap governance/ |
| `/loop:phase` | Governor | Execute one phase |
| `/loop:status` | Governor | Quick governance snapshot |
| `/loop:escalate` | Escalation-Handler | Present pending escalations |
| `/design:propose` | Design-Curator | Create new proposal |
| `/design:accept` | Design-Curator | Accept proposal → active |
| `/design:ship` | Design-Curator | Mark active → shipped |
| `/design:sync` | Design-Curator | Check consistency |
| `/intake:create` | Intake-Compiler | Create new intake |
| `/intake:compile` | Intake-Compiler | Compile intake → proposal |

---

## Hook Triggers

| Hook Type | Trigger | Action |
|-----------|---------|--------|
| Pre-command | Any `/loop:*` command | Inject A₀ contract |
| Pre-command | `/loop:phase` | Inject relevant B₀ playbook |
| Post-command | `/loop:phase` | Validate metrics moved |
| Pre-tool | Edit/Write to `src/**` | Check boundary violations |
| Post-command | Any `/design:*` command | Update DESIGN_LINKS |

---

## State Machine: Design Lifecycle

```
                    ┌──────────────┐
                    │   Drafted    │
                    └──────┬───────┘
                           │ submit
                           ▼
                    ┌──────────────┐
                    │   Proposed   │
                    └──────┬───────┘
                           │ review
                           ▼
┌───────────┐       ┌──────────────┐       ┌───────────┐
│   OnIce   │◄──────│   InReview   │──────►│  Rejected │
└───────────┘ defer └──────┬───────┘ reject└───────────┘
                           │ accept (Gate #1)
                           ▼
                    ┌──────────────┐
                    │   Accepted   │
                    └──────┬───────┘
                           │ promote
                           ▼
                    ┌──────────────┐
                    │    Active    │◄──┐
                    └──────┬───────┘   │ supersede (Gate #3)
                           │ complete  │
                           ▼           │
                    ┌──────────────┐   │
                    │   Shipped    │───┘
                    └──────┬───────┘
                           │ archive
                           ▼
                    ┌──────────────┐
                    │   Archived   │
                    └──────────────┘
```

Gates requiring human decision (via AskUserQuestion):
- **Gate #1:** InReview → Accepted
- **Gate #2:** Active → Shipped
- **Gate #3:** Any → Superseded
- **Gate #4:** → Rejected
- **Gate #5:** Change Boundary

---

## Artifact Authority Model

| Source | Binding? | Scope |
|--------|----------|-------|
| `governance/live/*` | YES | Execution (what must be true now) |
| `governance/compressed/*` | YES | Injected by hooks |
| `design/current/*` | YES (via DESIGN_LINKS) | Architecture intent |
| `design/active/*` | YES (via DESIGN_LINKS) | Active design specs |
| `design/proposals/*` | NO | Candidate futures |
| `design/archive/*` | NO | Historical record |
| `governance/roadmap/*` | NO | Future work |
| `governance/completed/*` | NO | Past work |

**Conflict Resolution:**
- If `governance/live` conflicts with `design/current`: governance wins, agent escalates
- If `design/active` conflicts with `design/current`: escalate (Gate #3)

---

## Error Handling

### Governance Directory Missing

```
/loop:phase called, governance/ doesn't exist
→ Hook blocks command
→ Display: "Run /loop:init first"
```

### Artifact Validation Fails

```
Governor reads BLOCKERS.md, format invalid
→ artifact-io skill detects error
→ Spawn Artifact-Validator agent
→ Fix or escalate
```

### Metric Measurement Fails

```
Script measure-metrics.sh returns non-zero
→ Governor escalates with fix suggestions
→ User updates measurement method
→ Resume phase
```

### Boundary Violation Detected

```
Pre-tool hook detects forbidden import
→ Block write operation
→ Display: violation + options (escalate, use bridge, fix import)
```

---

## Summary

The system maps to Claude Code as follows:

- **Commands:** Entry points that spawn agents
- **Hooks:** Automatic injection of compressed artifacts, validation, boundary enforcement
- **Agents:** Focused, single-purpose owners of specific domains (Governor, Design-Curator, etc.)
- **Skills:** Shared procedures called by agents (artifact-io, decision-gate, etc.)
- **Scripts:** Deterministic bash operations called by skills

Flow is always: Command → Hook → Agent → Skill → Script

Zero conditionals in agent routing. Agents are separate and focused.
