# Status Report - /do:peek Command Design

## Executive Summary

**Gap Identified**: The do-more-now plugin lacks a lightweight, instant-answer command for common codebase navigation questions. Users currently must choose between expensive full evaluations or asking Claude directly (which lacks structured navigation).

**Design Status**: COMPLETE - `/do:peek` design ready for implementation
**Ambiguities**: 0 - Design is clear and fits existing architecture
**Recommendation**: PROCEED with implementation

---

## Current Command Landscape Analysis

### Existing Commands (6)

**1. `/do:init-project`** - Project initialization
- **Scope**: Entire new project or major architectural change
- **Time**: 5-15 minutes (adaptive interview, research, scaffolding)
- **Output**: PROJECT_SPEC.md, ARCHITECTURE.md, scaffolding
- **Use when**: Starting from scratch or major restructuring

**2. `/do:feature-proposal`** - Product ideation
- **Scope**: Feature brainstorming and user value exploration
- **Time**: 3-8 minutes (ideation, refinement)
- **Output**: PROPOSAL.md with ideas and success criteria
- **Use when**: Need to explore "what" and "why" before "how"

**3. `/do:plan`** - Full evaluation + planning
- **Scope**: Comprehensive project assessment with auto-research
- **Time**: 5-15 minutes (evaluate → research → plan)
- **Output**: STATUS.md, PLAN.md, research decisions
- **Use when**: Need complete understanding before implementation

**4. `/do:status`** - Diagnostic check
- **Scope**: Read-only status assessment (project-wide or focused)
- **Time**: 2-5 minutes (surface-level, no research)
- **Output**: STATUS.md or WORK-EVALUATION.md
- **Use when**: Need quick health check without resolution

**5. `/do:learn`** - Deep research
- **Scope**: Iterative research on specific question (3 iteration max)
- **Time**: 5-20 minutes (research → evaluate → decide loop)
- **Output**: RESEARCH.md with decision and rationale
- **Use when**: Ambiguous question requiring external research

**6. `/do:it`** - Implementation
- **Scope**: TDD or iterative implementation workflow
- **Time**: 10-60+ minutes (depends on scope)
- **Output**: Code, tests, commits, updated STATUS/PLAN
- **Use when**: Ready to implement with clear plan

---

## Gap Analysis

### What's Missing?

**Scenario**: Developer needs quick, specific answer about codebase navigation or implementation detail.

**Examples of questions that don't fit existing commands**:

1. **"Where is user authentication implemented?"**
   - Too specific for `/do:plan` (overkill - would evaluate entire project)
   - Not a health check for `/do:status` (asking "where", not "is it working")
   - Not research-worthy for `/do:learn` (answer is in codebase, not web)
   - Just asking Claude: Lacks structured search, may miss files

2. **"How does the payment flow work?"**
   - Too narrow for `/do:plan` (would research entire project context)
   - Not a diagnostic for `/do:status` (asking "how", not "what's broken")
   - Not external research for `/do:learn` (implementation detail, not decision)
   - Just asking Claude: No guarantee of comprehensive tracing

3. **"What files are involved in the database migration system?"**
   - `/do:plan` would evaluate whole migration strategy (too broad)
   - `/do:status` would check if migrations work (different question)
   - `/do:learn` is for unknown decisions (this is known, just hard to find)
   - Just asking Claude: Might miss related files in different directories

4. **"Is there a pattern for handling async errors?"**
   - `/do:plan` would plan error handling across entire project
   - `/do:status` would diagnose current error handling health
   - `/do:learn` would research error handling strategies (external)
   - Just asking Claude: No codebase search, just generic advice

5. **"Show me how the config system is structured"**
   - Too specific for full planning workflows
   - Not a health check
   - Not a research question (answer exists in code)
   - Just asking: No structured exploration

### The Pattern

**Common thread**: Questions asking **"where/how/what files"** for **specific implementation details** that:
- Don't require evaluation (not checking if it works)
- Don't require planning (not deciding what to build)
- Don't require research (answer is in codebase)
- Benefit from structured search (not just grepping)

**Current workaround**: Ask Claude directly, but this:
- Lacks systematic codebase exploration
- May miss related files
- Doesn't produce reusable artifacts
- No guarantee of completeness

**Time gap**: Need something between "instant Claude answer" (0 min) and "full status check" (2-5 min)

---

## Proposed Design: `/do:peek`

### Command Definition

**Name**: `/do:peek`
**Arguments**: `[specific question about codebase]`
**Description**: Quick codebase navigation and implementation detail lookup. Answers "where/how/what files" questions with structured search.

### What It Does

**Core behavior**: Fast, focused codebase exploration that answers specific navigation questions without evaluation or planning overhead.

**Target time**: 30 seconds - 2 minutes
**Target scope**: Single implementation detail or component
**Output**: Inline response + optional PEEK.md if complex

### Agent Selection

**Use existing agent**: `researcher` (modified invocation)

**Why researcher fits**:
- Already designed for focused exploration
- Has tools: Read, Glob, Grep, WebSearch, WebFetch
- No expensive evaluation overhead
- Can search codebase systematically

**Key difference from `/do:learn`**:
- `/do:learn`: Iterative research with evaluation loop (3 iterations max)
- `/do:peek`: Single-pass codebase search with immediate answer

### Workflow

```markdown
## Step 1: Parse Question

Classify the question type:
- **Location**: "Where is X implemented?"
- **Mechanism**: "How does Y work?"
- **Inventory**: "What files are involved in Z?"
- **Pattern**: "Is there a pattern for W?"
- **Structure**: "Show me the structure of Q"

## Step 2: Execute Search

Use researcher agent in "peek mode" (single pass, codebase-only):

1. **Identify search strategy** based on question type
   - Location: Glob + Grep for relevant files
   - Mechanism: Find entry points, trace execution
   - Inventory: Search for patterns, list related files
   - Pattern: Search for examples, extract commonalities
   - Structure: Map directory structure, identify key files

2. **Execute search** using available tools
   - Glob: Find files by pattern
   - Grep: Search for specific code patterns
   - Read: Examine relevant files
   - NO WebSearch/WebFetch (codebase-only)

3. **Synthesize answer**
   - List relevant files with paths
   - Show key code snippets
   - Explain relationships between components
   - Note any gaps or ambiguities

## Step 3: Output

**For simple questions** (1-3 files involved):
Display inline response:
```
Found in 2 files:
- /path/to/auth.py (lines 45-89) - Main authentication logic
- /path/to/middleware.py (lines 12-34) - Auth middleware wrapper

Key mechanism: Uses JWT tokens validated against Redis cache.
Entry point: authenticate() function in auth.py
```

**For complex questions** (4+ files, intricate relationships):
Write PEEK-<topic>-<timestamp>.md + inline summary:
```
Component spans 7 files across 3 directories.
Details: .agent_planning/PEEK-payment-flow-20251207.md

Summary: Payment flow uses Stripe API, queue-based processing.
Entry: /api/payment.py → /workers/process_payment.py → /models/transaction.py
```

## Step 4: Display Summary

```
═══════════════════════════════════════
Peek: [question summary]
  Found: n files | Time: Xs
  [Details in PEEK.md OR inline answer]
═══════════════════════════════════════
```
```

### Constraints

**NO evaluation**: Don't assess if code works, just locate and explain
**NO planning**: Don't recommend changes, just describe what exists
**NO external research**: Codebase-only, no web searches
**NO iteration**: Single pass, immediate answer (not a loop)

**Fast exit conditions**:
- Can't find relevant code → "Not found in codebase. Try /do:learn if researching external solutions."
- Question too broad → "Question too broad for peek. Try /do:status [area] for evaluation."
- Question requires evaluation → "This needs testing. Try /do:status [area] to evaluate."

### Integration with Existing Commands

**Progression path**:

1. `/do:peek "Where is auth?"` → Quick location answer
2. `/do:status auth` → Evaluate if auth works properly
3. `/do:plan` → Plan auth improvements if needed
4. `/do:it` → Implement auth changes

**When to use what**:

| Question Type | Command |
|---------------|---------|
| "Where is X?" | `/do:peek` |
| "Does X work?" | `/do:status` |
| "How should we implement X?" | `/do:learn` |
| "What needs fixing?" | `/do:plan` |
| "Build X" | `/do:it` |

---

## Example Usage Scenarios

### Example 1: Finding Authentication Code

**User**: `/do:peek Where is user authentication implemented?`

**Peek executes**:
1. Grep for "auth", "authenticate", "login" patterns
2. Find: auth.py, middleware/auth.py, models/user.py
3. Read key files to identify entry points
4. Trace auth flow: login → validate → session

**Output** (inline):
```
Authentication implemented across 3 files:

1. /api/auth.py (lines 23-156)
   - login() - Main entry point
   - validate_credentials() - Password check
   - create_session() - JWT generation

2. /middleware/auth.py (lines 8-45)
   - require_auth() - Decorator for protected routes
   - verify_token() - JWT validation

3. /models/user.py (lines 67-89)
   - User.check_password() - Hash comparison

Flow: POST /login → auth.login() → User.check_password() → create_session() → JWT returned
Middleware: @require_auth decorator checks JWT on protected routes
```

**Time**: ~45 seconds

---

### Example 2: Understanding Payment Flow

**User**: `/do:peek How does the payment processing flow work?`

**Peek executes**:
1. Grep for "payment", "stripe", "transaction"
2. Find 7 files across api/, workers/, models/
3. Trace flow from API endpoint through queue to completion
4. Too complex for inline → write PEEK.md

**Output** (inline summary + file):
```
Payment flow spans 7 files - see .agent_planning/PEEK-payment-flow-20251207-143022.md

Summary:
Entry: POST /api/payment → creates PaymentIntent with Stripe
Queue: Publishes to Redis queue for async processing
Worker: process_payment.py polls queue, confirms payment
Database: Updates Transaction model on success
Webhooks: Stripe webhook verifies payment status

Key files:
- /api/payment.py - Entry point, Stripe API calls
- /workers/process_payment.py - Async processing
- /models/transaction.py - Database persistence
```

**Time**: ~90 seconds

---

### Example 3: Pattern Lookup

**User**: `/do:peek Is there a pattern for handling database transactions?`

**Peek executes**:
1. Grep for "transaction", "commit", "rollback"
2. Find examples in models/, services/
3. Extract common pattern
4. Show representative example

**Output** (inline):
```
Database transaction pattern (used in 8 locations):

Standard pattern:
```python
from contextlib import contextmanager

@contextmanager
def transaction():
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise

# Usage:
with transaction():
    user.update(...)
    log.create(...)
```

Examples in:
- /services/user_service.py (lines 45-52)
- /services/order_service.py (lines 89-96)
- /api/admin.py (lines 123-130)

All follow same pattern: contextmanager with commit/rollback.
```

**Time**: ~60 seconds

---

## Implementation Specification

### Command File: `commands/peek.md`

```markdown
---
argument-hint: [specific question about codebase]
description: Quick codebase navigation. Answers "where/how/what files" questions without evaluation overhead.
---

Fast, focused codebase exploration for specific navigation questions.

<question>
$ARGUMENTS
</question>

## Execution

Use the do:researcher agent in "peek mode":

<mode>peek</mode>
<constraints>
- Single pass, no iteration
- Codebase-only, no external research
- No evaluation, no planning
- Target time: 30s - 2min
</constraints>

## Output Decision

**Simple answer** (1-3 files, straightforward):
- Display inline with file paths and key snippets

**Complex answer** (4+ files, intricate relationships):
- Write PEEK-<topic>-<timestamp>.md
- Display inline summary

## Display Summary

```
═══════════════════════════════════════
Peek: [question summary]
  Found: n files | Time: Xs
  [inline answer OR "Details in PEEK-<topic>.md"]
═══════════════════════════════════════
```

## Fast Exit Conditions

If question is:
- Not found → "Not found. Try /do:learn for external research."
- Too broad → "Too broad. Try /do:status [area] for evaluation."
- Needs testing → "Needs testing. Try /do:status [area]."
```

### Agent Modification: `agents/researcher.md`

**Add "peek mode" section**:

```markdown
## Peek Mode (Optional)

When invoked with `<mode>peek</mode>`:

**Constraints**:
- Single pass, no iteration
- Codebase-only (NO WebSearch/WebFetch)
- No evaluation or planning
- Target completion: 30s - 2min

**Focus**:
- Answer specific navigation question
- List relevant files with paths
- Show key code snippets
- Explain relationships

**Output**:
- Inline if simple (1-3 files)
- PEEK-<topic>.md if complex (4+ files)

**Fast exits**:
- Not found → Suggest /do:learn
- Too broad → Suggest /do:status
- Needs testing → Suggest /do:status
```

### Plugin Integration

**Update `plugin.json`**:
```json
"commands": [
  "./commands/plan.md",
  "./commands/status.md",
  "./commands/peek.md",    // <-- ADD THIS
  "./commands/feature-proposal.md",
  "./commands/init-project.md",
  "./commands/learn.md",
  "./commands/it.md"
]
```

---

## Design Validation

### Gap Filled?

**✓** Provides fast codebase navigation without evaluation overhead
**✓** Answers "where/how/what files" questions systematically
**✓** Fills time gap between "instant answer" and "full evaluation"
**✓** Produces artifacts for complex answers (PEEK.md)
**✓** Distinct from existing commands (doesn't overlap)

### Fits Existing Architecture?

**✓** Reuses existing `researcher` agent (no new agent needed)
**✓** Follows command pattern (markdown file with arguments)
**✓** Uses same file management (`.agent_planning/` directory)
**✓** Follows same output format (summary box at end)
**✓** Integrates with workflow progression (/peek → /status → /plan → /it)

### Ambiguities Resolved?

**✓** Clear scope: Codebase navigation only, no evaluation
**✓** Clear time target: 30s - 2min (fast)
**✓** Clear output format: Inline or PEEK.md based on complexity
**✓** Clear exit conditions: Not found, too broad, needs testing
**✓** Clear agent reuse: researcher in "peek mode"

---

## Recommendations

### Implementation Priority

**P0 - Core Command**: Create `commands/peek.md` with workflow as specified
**P0 - Agent Mode**: Add "peek mode" section to `agents/researcher.md`
**P0 - Plugin Config**: Update `plugin.json` to include peek command

**P1 - Testing**: Test with example scenarios (auth, payment, pattern lookup)
**P1 - Documentation**: Update plugin README with `/do:peek` examples

### Estimated Complexity

**Low** - Reuses existing agent, simple workflow, clear constraints

**Implementation time**: 30-60 minutes
- 15min: Create peek.md command file
- 15min: Update researcher.md with peek mode
- 10min: Update plugin.json
- 20min: Test with real examples

### Success Criteria

**Command works if**:
1. Returns relevant files in under 2 minutes for typical questions
2. Produces inline answers for simple queries (1-3 files)
3. Writes PEEK.md for complex queries (4+ files)
4. Fast-exits gracefully when question doesn't fit scope
5. Provides clear next-step suggestions (when to use /status, /learn, etc.)

**Quality indicators**:
- Users stop asking "where is X" directly to Claude
- Peek answers are comprehensive (finds all relevant files)
- Peek is faster than running multiple grep/glob commands manually
- Peek output feeds naturally into /status or /plan workflows

---

## Ambiguities

**NONE** - Design is clear and ready for implementation.

All design decisions have clear rationale:
- **Why peek vs. extending status?** Different intent (navigation vs. evaluation)
- **Why reuse researcher?** Already has search tools, no need for new agent
- **Why inline + file options?** Balance speed (inline) vs. completeness (file)
- **Why codebase-only?** External research already covered by /do:learn
- **Why single-pass?** Keep it fast, iteration covered by /do:learn

---

## Workflow Recommendation

**✓ CONTINUE** - Design complete, ready for implementation

**Next steps**:
1. Create `commands/peek.md` per specification above
2. Update `agents/researcher.md` with peek mode section
3. Update `plugin.json` to register peek command
4. Test with example scenarios
5. Update plugin documentation

**No blockers identified.**
