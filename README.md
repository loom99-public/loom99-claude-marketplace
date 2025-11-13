# dev-loop Plugin for Claude Code

**Structured development workflows with evaluation-driven iteration**

A production-ready Claude Code plugin that provides two complementary development workflows: Test-Driven Development (TDD) and Iterative Implementation. Both workflows share a common foundation of rigorous evaluation and planning, ensuring you understand the problem before solving it.

---

## 🎯 What is dev-loop?

dev-loop transforms Claude Code into a systematic development environment by enforcing a structured workflow:

1. **Evaluate** → Ruthless gap analysis of current state vs. requirements
2. **Plan** → Convert gaps into prioritized, actionable backlog
3. **Implement** → Build with either TDD or iterative validation
4. **Verify** → Runtime evidence (tests, logs, screenshots) confirms completion

**The Result**: Fewer bugs, better code, faster iteration, cleaner commits, higher quality.

---

## 🚀 Installation

### Step 1: Install the Plugin Marketplace

```bash
# Clone the marketplace repository
git clone https://github.com/loom99/loom99-claude-marketplace.git
cd loom99-claude-marketplace

# Add marketplace to Claude Code
# (In Claude Code)
/plugin marketplace add .
```

### Step 2: Install dev-loop Plugin

```bash
# In Claude Code
/plugin install dev-loop
```

### Step 3: Verify Installation

```bash
# Check available commands (should show /evaluate-and-plan, etc.)
/help
```

---

## 🔄 Two Workflows, One Foundation

### Workflow 1: TDD (Test-Driven Development)

**Best for**: Features with clear requirements, API development, critical systems, refactoring

**Process**:
```
User Request
     ↓
/evaluate-and-plan          → STATUS + PLAN generated
     ↓
/test-and-implement         → Two loops:
     ├─ TestLoop:           functional-tester writes tests
     │                      project-evaluator validates tests
     └─ ImplementLoop:      test-driven-implementer implements
                            project-evaluator validates implementation
```

**Key Principle**: Tests define the contract. Implementation must pass tests through real functionality, never shortcuts.

### Workflow 2: Iterative Implementation (Non-TDD)

**Best for**: UI/visual features, exploratory work, prototyping, when tests are impractical upfront

**Process**:
```
User Request
     ↓
/evaluate-and-plan          → STATUS + PLAN generated
     ↓
/implement-and-iterate      → Loop until complete:
     ├─ iterative-implementer builds incrementally
     └─ work-evaluator validates with runtime evidence
                            (screenshots, logs, execution)
```

**Key Principle**: Validation through manual testing and runtime evaluation. Visual proof for web UIs via chrome-devtools MCP.

---

## 📋 Commands Reference

### Core Workflow Commands

#### `/evaluate-and-plan [area of focus]`
Generates comprehensive status report and prioritized implementation plan.

**What it does**:
1. Runs `project-evaluator` agent → creates `STATUS-*.md`
2. Runs `status-planner` agent → creates `PLAN-*.md`

**When to use**: Start of any workflow, or after major changes to re-sync planning docs.

**Example**:
```
/evaluate-and-plan user authentication feature
```

---

#### `/test-and-implement [area of focus | "plan-first"]`
**TDD workflow** - Write tests first, then implement.

**What it does**:
1. Optional: Runs `/evaluate-and-plan` if "plan-first" or no STATUS/PLAN exists
2. **TestLoop**:
   - `functional-tester` writes comprehensive tests
   - `project-evaluator` validates tests meet criteria
   - Repeat until tests are production-quality
3. **ImplementLoop**:
   - `test-driven-implementer` implements functionality
   - `project-evaluator` validates implementation
   - Repeat until all tests pass with real functionality
4. Final: Re-runs `/evaluate-and-plan` to update status

**Exit Conditions**:
- TestLoop: Tests meet all TestCriteria (useful, complete, flexible, automated)
- ImplementLoop: No outstanding issues with well-defined solutions

**Example**:
```
# Start fresh with evaluation
/test-and-implement plan-first

# Use existing STATUS/PLAN
/test-and-implement API endpoints
```

---

#### `/implement-and-iterate [area of focus | "plan-first"]`
**Non-TDD workflow** - Implement and validate through runtime evidence.

**What it does**:
1. Optional: Runs `/evaluate-and-plan` if "plan-first" or no STATUS/PLAN exists
2. **Implementation Loop**:
   - `iterative-implementer` builds functionality incrementally
   - `work-evaluator` runs software and gathers evidence (screenshots, logs, output)
   - Compares against acceptance criteria from PLAN
   - Repeats until goals achieved
3. Final: Re-runs `/evaluate-and-plan` to update status

**Exit Conditions**:
- COMPLETE: work-evaluator confirms all goals achieved
- INCOMPLETE: Clear path forward exists, continue loop
- BLOCKED: No clear path, pause and request user guidance

**Example**:
```
# Start with fresh evaluation
/implement-and-iterate plan-first

# Use existing STATUS/PLAN
/implement-and-iterate dashboard UI
```

---

#### `/feature-proposal [feature description]`
Generates visionary, pragmatic feature designs.

**What it does**: Runs `product-visionary` agent to create forward-thinking feature proposals.

**Example**:
```
/feature-proposal real-time collaboration for documents
```

---

## 🎓 Getting Started

### Example 1: Building a New Feature (TDD)

```bash
# 1. Start with evaluation and planning
/evaluate-and-plan user registration system

# 2. Read the generated plan
# (Claude will create .agent_planning/STATUS-*.md and PLAN-*.md)

# 3. Implement with TDD
/test-and-implement

# Claude will:
# - Write comprehensive tests first
# - Validate tests are production-quality
# - Implement functionality to pass tests
# - Re-evaluate and update status
```

### Example 2: Building UI Features (Non-TDD)

```bash
# 1. Start with evaluation and planning
/evaluate-and-plan responsive navigation menu

# 2. Implement with runtime validation
/implement-and-iterate

# Claude will:
# - Build functionality incrementally
# - Use chrome-devtools to capture screenshots (for web UIs)
# - Validate against acceptance criteria
# - Iterate until goals achieved
# - Re-evaluate and update status
```

### Example 3: Quick Feature Proposal

```bash
# Get visionary feature design
/feature-proposal AI-powered code suggestions

# Review proposal, then proceed with evaluate-and-plan + implement
```

---

## 🧩 Architecture

### Planning Document System

All workflow state lives in `.agent_planning/` directory:

**Authoritative Sources** (READ-ONLY):
- `PROJECT_SPEC.md` / `PROJECT.md` - Project requirements
- `STATUS-<timestamp>.md` - Current state (project-evaluator output)
- `PLAN-<timestamp>.md` - Work backlog (status-planner output)

**Working Documents** (READ-WRITE):
- `BACKLOG*.md`, `SPRINT*.md`, `TODO*.md` - Tracked during implementation
- `WORK-EVALUATION-<timestamp>.md` - Runtime validation results

**File Retention**: Max 4 timestamped files per prefix. Oldest automatically deleted.

### Agent Coordination

Commands orchestrate specialized agents:

| Agent | Role | Output |
|-------|------|--------|
| **project-evaluator** | Ruthless gap analysis | STATUS-*.md |
| **status-planner** | Backlog generation | PLAN-*.md |
| **functional-tester** | Test design (TDD) | Test files |
| **test-driven-implementer** | TDD implementation | Code + commits |
| **iterative-implementer** | Incremental implementation | Code + commits |
| **work-evaluator** | Runtime validation | WORK-EVALUATION-*.md |
| **product-visionary** | Feature proposals | Proposal docs |

---

## 🌐 MCP Integration

### chrome-devtools

**Purpose**: Browser automation with screenshots and DevTools metadata for web application testing.

**Used by**: `work-evaluator` agent during `/implement-and-iterate` workflow

**Capabilities**:
- Navigate web applications
- Capture screenshots
- Extract console logs
- Monitor network errors
- Inspect DOM state

**When it activates**: Automatically during runtime validation for browser-based features.

**Configuration**: Pre-configured in `.mcp.json` - no setup required.

---

## 🎯 Critical Rules

### For All Workflows

1. **File Management**: All planning work in `.agent_planning/`. Never modify completed work files.
2. **Honesty**: No optimism, no shortcuts, no placeholders in production code.
3. **Evidence**: Always cite file paths, line numbers, metrics.
4. **Timestamping**: Use `YYYY-MM-DD-HHmmss` format consistently.

### For Test Writing (TDD)

1. **Never use MagicMock()** for external systems - use real objects with selective patching.
2. **Never invent attributes/methods** that don't exist in real APIs.
3. **Tests must fail with stubs** - un-gameable by design.
4. **Validate real user workflows** - end-to-end, not implementation details.

### For Implementation (Both Workflows)

1. **No hardcoded test values** or test-specific branches.
2. **No TODO comments** in completed code.
3. **Explicit error handling** - no silent failures.
4. **Real functionality** - no shortcuts to pass tests/validation.

---

## 📚 Documentation

- **[CLAUDE.md](./plugins/dev-loop/CLAUDE.md)** - Comprehensive plugin guide for Claude Code
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Technical architecture and design decisions

---

## 🔧 Technical Requirements

- **Claude Code** (latest version)
- **git** (recommended for commit workflows)
- **Node.js** (for chrome-devtools MCP server, auto-installed via npx)

---

## 📊 What You Get

- **2 production-ready workflows** (TDD + Iterative)
- **7 specialized agents** with distinct responsibilities
- **4 slash commands** for workflow orchestration
- **1 MCP server integration** (chrome-devtools for web UI testing)
- **Zero-optimism evaluation** - brutal honesty that saves projects
- **Evidence-based validation** - runtime proof, not assumptions

---

## 💡 Philosophy

**Brutal honesty saves projects.** The workflows enforce reality-based development:

- **TDD**: Tests fail if functionality is faked → forces real implementation
- **Non-TDD**: Runtime evaluation fails if goals unmet → forces working software
- **Evaluation**: Zero-optimism gap analysis → exposes actual state
- **Planning**: Evidence-based backlog → tracks what remains

No shortcuts. No optimism. Just working software.

---

## 🤝 Contributing

This is currently a personal marketplace by Brandon Fryslie. Feedback and suggestions welcome via issues.

---

## 📝 License

MIT License

---

## 👤 Author

**Brandon Fryslie**
- Email: 
- Marketplace: loom99

---

## 🔗 Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Plugin Marketplaces Guide](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [Writing Plugins](https://docs.claude.com/en/docs/claude-code/plugins)

---

**Ready to build better software? Install dev-loop and start with `/evaluate-and-plan`!**
