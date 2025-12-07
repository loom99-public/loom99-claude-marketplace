# Implementation Plan: /do:peek Command

**Generated**: 2025-12-07-161712
**Source STATUS**: STATUS-do-peek-command-2025-12-07.md
**Spec**: plugins/do-more-now/CLAUDE.md
**Target Plugin**: do-more-now v0.1.0

---

## Executive Summary

**What**: Add `/do:peek` command for fast codebase navigation answering "where/how/what files" questions without evaluation overhead.

**Why**: Gap exists between instant Claude answers (0 min, unstructured) and full status evaluation (2-5 min, comprehensive). Need 30s-2min focused search for specific implementation questions.

**Impact**: Provides developers with quick, structured codebase exploration for navigation questions that don't require evaluation, planning, or external research.

**Scope**: 3 work items (P0), estimated 60-90 minutes total implementation time.

**Status**: Ready to implement. Design complete, no blockers, clear acceptance criteria.

---

## Current State (from STATUS-do-peek-command-2025-12-07.md)

### Existing Commands (6)
1. `/do:init-project` - Project initialization (5-15 min)
2. `/do:feature-proposal` - Product ideation (3-8 min)
3. `/do:plan` - Full evaluation + planning (5-15 min)
4. `/do:status` - Diagnostic check (2-5 min)
5. `/do:learn` - Deep research (5-20 min)
6. `/do:it` - Implementation (10-60+ min)

### Gap Identified
**Missing**: Fast codebase navigation (30s-2min) for specific "where/how/what files" questions that:
- Don't require evaluation (not checking if it works)
- Don't require planning (not deciding what to build)
- Don't require research (answer is in codebase)
- Benefit from structured search (not just grepping)

**Examples**:
- "Where is user authentication implemented?"
- "How does the payment flow work?"
- "What files are involved in database migrations?"
- "Is there a pattern for handling async errors?"
- "Show me how the config system is structured"

---

## Design Specification

### Command: `/do:peek`

**Arguments**: `[specific question about codebase]`
**Description**: Quick codebase navigation and implementation detail lookup. Answers "where/how/what files" questions with structured search.

**Target Time**: 30 seconds - 2 minutes
**Target Scope**: Single implementation detail or component
**Output**: Inline response + optional PEEK-<topic>-<timestamp>.md if complex

### Agent Selection

**Reuse existing**: `researcher` agent in "peek mode"

**Why researcher fits**:
- Already has tools: Read, Glob, Grep, WebSearch, WebFetch
- Designed for focused exploration
- No expensive evaluation overhead
- Can search codebase systematically

**Key difference from `/do:learn`**:
- `/do:learn`: Iterative research with evaluation loop (3 iterations max)
- `/do:peek`: Single-pass codebase search with immediate answer

### Workflow

```
Step 1: Parse Question
  ↓
  Classify type: Location | Mechanism | Inventory | Pattern | Structure

Step 2: Execute Search (single pass, codebase-only)
  ↓
  1. Identify search strategy based on question type
  2. Execute search (Glob, Grep, Read - NO WebSearch/WebFetch)
  3. Synthesize answer

Step 3: Output Decision
  ↓
  Simple (1-3 files) → Inline response
  Complex (4+ files) → PEEK-<topic>-<timestamp>.md + summary

Step 4: Display Summary
  ↓
  ═══════════════════════════════════════
  Peek: [question summary]
    Found: n files | Time: Xs
    [inline answer OR Details in PEEK.md]
  ═══════════════════════════════════════
```

### Constraints

**NO evaluation**: Don't assess if code works, just locate and explain
**NO planning**: Don't recommend changes, just describe what exists
**NO external research**: Codebase-only, no web searches
**NO iteration**: Single pass, immediate answer (not a loop)

### Fast Exit Conditions

- Can't find relevant code → "Not found in codebase. Try /do:learn if researching external solutions."
- Question too broad → "Question too broad for peek. Try /do:status [area] for evaluation."
- Question requires evaluation → "This needs testing. Try /do:status [area] to evaluate."

### Integration with Existing Commands

**Progression path**:
1. `/do:peek "Where is auth?"` → Quick location answer
2. `/do:status auth` → Evaluate if auth works properly
3. `/do:plan` → Plan auth improvements if needed
4. `/do:it` → Implement auth changes

---

## Prioritized Backlog

### P0-1: Create peek.md Command File

**Status**: Not Started
**Effort**: Small (15-20 minutes)
**Dependencies**: None
**Spec Reference**: STATUS-do-peek-command-2025-12-07.md § Implementation Specification

#### Description

Create `plugins/do-more-now/commands/peek.md` implementing the `/do:peek` command with proper argument handling, researcher agent invocation in "peek mode", and output formatting.

#### Acceptance Criteria

- [ ] File created at `plugins/do-more-now/commands/peek.md`
- [ ] Front matter includes:
  - `argument-hint: [specific question about codebase]`
  - `description: Quick codebase navigation. Answers "where/how/what files" questions without evaluation overhead.`
- [ ] Command expands to prompt that:
  - Passes user question to researcher agent
  - Specifies `<mode>peek</mode>` to enable peek mode
  - Includes constraints: single pass, codebase-only, no evaluation/planning, 30s-2min target
  - Defines output decision logic (inline vs PEEK.md)
  - Includes fast exit conditions
  - Displays formatted summary at end
- [ ] Follows existing command pattern from `plan.md`, `status.md`, `learn.md`
- [ ] Properly handles `$ARGUMENTS` variable for user question

#### Technical Notes

**Command file structure** (reference existing commands):
```markdown
---
argument-hint: [hint text]
description: [short description]
---

[Command prompt that expands when /do:peek is invoked]

<question>
$ARGUMENTS
</question>

## Execution
[Instructions for researcher agent in peek mode]

## Output Decision
[Inline vs PEEK.md logic]

## Display Summary
[Formatted output box]

## Fast Exit Conditions
[When to suggest other commands]
```

**Example from STATUS file** (lines 360-408):
- Use `<mode>peek</mode>` to signal peek mode to researcher
- Include `<constraints>` block with 4 constraints
- Define output decision: simple (1-3 files inline) vs complex (4+ files PEEK.md)
- Include formatted summary box with `═══` borders
- List fast exits with specific suggestions

**File to reference**: `plugins/do-more-now/commands/learn.md` (similar researcher invocation)

---

### P0-2: Update researcher.md with Peek Mode

**Status**: Not Started
**Effort**: Small (15-20 minutes)
**Dependencies**: None (can work in parallel with P0-1)
**Spec Reference**: STATUS-do-peek-command-2025-12-07.md § Agent Modification

#### Description

Add "Peek Mode" section to `plugins/do-more-now/agents/researcher.md` specifying behavior modifications when invoked with `<mode>peek</mode>`.

#### Acceptance Criteria

- [ ] New section added to `researcher.md` titled "## Peek Mode (Optional)"
- [ ] Section placed after main research process, before "Quality Standards" section
- [ ] Documents peek mode constraints:
  - Single pass, no iteration
  - Codebase-only (NO WebSearch/WebFetch)
  - No evaluation or planning
  - Target completion: 30s-2min
- [ ] Defines peek mode focus:
  - Answer specific navigation question
  - List relevant files with paths
  - Show key code snippets
  - Explain relationships
- [ ] Specifies output format:
  - Inline if simple (1-3 files)
  - PEEK-<topic>-<timestamp>.md if complex (4+ files)
- [ ] Lists fast exit conditions with suggestions
- [ ] Does NOT break existing researcher behavior (peek mode is optional)

#### Technical Notes

**Integration approach**: Add new optional mode section that researcher checks for when invoked. When `<mode>peek</mode>` is present, researcher follows modified workflow. When absent, researcher follows existing workflow.

**Peek mode differences from normal research**:
- Normal: Iterative (evaluate → research → decide loop)
- Peek: Single-pass (search → answer immediately)
- Normal: External research allowed (WebSearch/WebFetch)
- Peek: Codebase-only (NO web tools)
- Normal: Produces RESEARCH-*.md with options/tradeoffs
- Peek: Produces inline answer OR PEEK-*.md with findings
- Normal: Decision-oriented (recommend option)
- Peek: Fact-oriented (describe what exists)

**File management consistency**:
- Use `.agent_planning/` directory for PEEK-*.md files
- Follow timestamp format: `PEEK-<topic>-<YYYY-MM-DD-HHmmss>.md`
- No file retention policy needed (not authoritative like STATUS/PLAN)

**Example section structure** (from STATUS lines 414-439):
```markdown
## Peek Mode (Optional)

When invoked with `<mode>peek</mode>`:

**Constraints**:
[4 constraints listed]

**Focus**:
[4 focus items listed]

**Output**:
[Inline vs file decision]

**Fast exits**:
[3 exit conditions with suggestions]
```

---

### P0-3: Update plugin.json to Register Command

**Status**: Not Started
**Effort**: Small (5-10 minutes)
**Dependencies**: P0-1 complete (peek.md exists)
**Spec Reference**: STATUS-do-peek-command-2025-12-07.md § Plugin Integration

#### Description

Update `plugins/do-more-now/.claude-plugin/plugin.json` to register the new `/do:peek` command in the commands array.

#### Acceptance Criteria

- [ ] `plugin.json` updated with new command entry
- [ ] Command path added: `"./commands/peek.md"`
- [ ] Command inserted in logical position (suggest between `status.md` and `feature-proposal.md`)
- [ ] JSON remains valid after edit (no syntax errors)
- [ ] All existing commands remain registered
- [ ] File follows existing formatting/indentation

#### Technical Notes

**Current commands array** (from plugin.json lines 11-18):
```json
"commands": [
  "./commands/plan.md",
  "./commands/status.md",
  "./commands/feature-proposal.md",
  "./commands/init-project.md",
  "./commands/learn.md",
  "./commands/it.md"
]
```

**Suggested new order** (logical grouping):
```json
"commands": [
  "./commands/plan.md",       // Full evaluation + planning
  "./commands/status.md",     // Quick diagnostic
  "./commands/peek.md",       // <-- ADD: Quick navigation
  "./commands/feature-proposal.md",  // Feature design
  "./commands/init-project.md",     // Project initialization
  "./commands/learn.md",      // Deep research
  "./commands/it.md"          // Implementation
]
```

**Rationale for placement**: Group navigation/diagnostic commands together (plan → status → peek), separate from creative/implementation commands.

**Validation**: After editing, verify JSON syntax with `cat plugin.json | python -m json.tool` or similar.

---

## Dependency Graph

```
P0-1: Create peek.md
  ↓ (P0-3 depends on this)

P0-2: Update researcher.md
  (Independent - can work in parallel)

P0-3: Update plugin.json
  ↑ (Requires P0-1 complete)
```

**Critical path**: P0-1 → P0-3 (20-30 min)
**Parallel work**: P0-2 can execute during or after (15-20 min)
**Total time**: 50-70 minutes if sequential, 30-35 minutes if P0-2 done in parallel

---

## Recommended Sprint Planning

### Sprint 1: Core Implementation (Single Session)

**Goal**: Complete `/do:peek` command implementation and registration

**Tasks** (execute in this order):
1. **P0-1 + P0-2 (parallel)**: Create peek.md + Update researcher.md (20-25 min)
   - Start with peek.md (read learn.md for reference)
   - While that's fresh, update researcher.md
2. **P0-3**: Update plugin.json (5-10 min)
   - Add command entry
   - Validate JSON syntax

**Deliverable**: Working `/do:peek` command registered and ready for testing

**Testing approach** (manual):
- Invoke `/do:peek Where is authentication implemented?` in a test project
- Verify researcher agent activates in peek mode
- Verify output format (inline or PEEK.md based on complexity)
- Verify fast exits work (e.g., `/do:peek How do I build a web server?` → suggests /do:learn)
- Verify time constraint (completes in under 2 minutes)

---

## Risk Assessment

### Low Risk Items

**P0-1 (peek.md)**: Straightforward command file creation following existing pattern. Reference `learn.md` for researcher invocation structure.

**P0-2 (researcher.md)**: Additive change (new optional section). Does not modify existing workflow. Low risk of breaking current functionality.

**P0-3 (plugin.json)**: Simple JSON array update. Easy to validate syntax.

### Medium Risk Items

**None identified**

### High Risk Items

**None identified**

### Mitigation Strategies

**General**:
- Reference existing commands (learn.md, status.md) for consistent patterns
- Test manually after implementation (5 example questions from STATUS file)
- Validate researcher agent still works for `/do:learn` (ensure peek mode doesn't break normal research)

**Quality checks**:
- Does peek complete in under 2 minutes for typical questions?
- Does output clearly distinguish inline vs PEEK.md cases?
- Are fast exits helpful and accurate?
- Does peek integrate naturally with `/do:status` and `/do:plan` progression?

---

## Success Criteria

### Implementation Success

**Command works if**:
1. ✓ Returns relevant files in under 2 minutes for typical questions
2. ✓ Produces inline answers for simple queries (1-3 files)
3. ✓ Writes PEEK-<topic>-<timestamp>.md for complex queries (4+ files)
4. ✓ Fast-exits gracefully when question doesn't fit scope
5. ✓ Provides clear next-step suggestions (when to use /status, /learn, etc.)

### Quality Indicators

**User experience**:
- Users stop asking "where is X" directly to Claude (use `/do:peek` instead)
- Peek answers are comprehensive (finds all relevant files)
- Peek is faster than running multiple grep/glob commands manually
- Peek output feeds naturally into `/do:status` or `/do:plan` workflows

**Technical**:
- Peek mode doesn't break existing researcher agent behavior
- Command registration works (appears in Claude Code command list)
- Output format is consistent with other do-more-now commands
- File management follows `.agent_planning/` conventions

---

## Next Steps After Implementation

### P1: Manual Testing (15-20 minutes)

Test with example scenarios from STATUS file:
1. **Example 1**: `/do:peek Where is user authentication implemented?`
   - Expect: Inline answer with 2-3 files (auth.py, middleware, models)
   - Time: ~45 seconds
2. **Example 2**: `/do:peek How does the payment processing flow work?`
   - Expect: PEEK.md file with 7+ files spanning api/workers/models
   - Time: ~90 seconds
3. **Example 3**: `/do:peek Is there a pattern for handling database transactions?`
   - Expect: Inline answer with pattern example + 3-4 file locations
   - Time: ~60 seconds
4. **Fast exit test**: `/do:peek How should I architect a payment system?`
   - Expect: "Question too broad for peek. Try /do:status [area] or /do:learn"
5. **Not found test**: `/do:peek Where is the quantum entanglement module?`
   - Expect: "Not found in codebase. Try /do:learn if researching external solutions."

### P1: Documentation Update (10-15 minutes)

Update `plugins/do-more-now/CLAUDE.md`:
- Add `/do:peek` to command reference section (after `/do:status`)
- Document when to use peek vs status vs learn
- Add progression path examples (peek → status → plan → it)
- Update command count (6 → 7 commands)

### P2: Root CLAUDE.md Update (5-10 minutes)

Update repository root `CLAUDE.md`:
- Increment do-more-now command count (6 → 7)
- Add brief mention of `/do:peek` in do-more-now plugin description
- Update line counts if significantly changed

---

## File Change Summary

**Files to CREATE**:
- `plugins/do-more-now/commands/peek.md` (new command file, ~80-120 lines estimated)

**Files to MODIFY**:
- `plugins/do-more-now/agents/researcher.md` (add peek mode section, +30-40 lines)
- `plugins/do-more-now/.claude-plugin/plugin.json` (add 1 line to commands array)

**Files to UPDATE (post-implementation)**:
- `plugins/do-more-now/CLAUDE.md` (documentation)
- `CLAUDE.md` (root documentation)

**Files GENERATED at runtime**:
- `.agent_planning/PEEK-<topic>-<timestamp>.md` (when complex queries are answered)

---

## Estimated Effort

### By Priority

**P0 Items**: 50-70 minutes
- P0-1: 15-20 minutes (peek.md creation)
- P0-2: 15-20 minutes (researcher.md update)
- P0-3: 5-10 minutes (plugin.json update)
- Buffer: 15-20 minutes (testing, validation, iteration)

**P1 Items**: 25-35 minutes
- Manual testing: 15-20 minutes
- Documentation: 10-15 minutes

**P2 Items**: 5-10 minutes
- Root CLAUDE.md update: 5-10 minutes

### Total Effort

**Core implementation (P0)**: 50-70 minutes
**Full completion (P0+P1+P2)**: 80-115 minutes (~1.5-2 hours)

**Realistic estimate**: 90 minutes for complete implementation, testing, and documentation.

---

## Ambiguities

**NONE** - Design is clear and ready for implementation.

All design decisions documented in STATUS file with clear rationale:
- ✓ Why peek vs. extending status? Different intent (navigation vs. evaluation)
- ✓ Why reuse researcher? Already has search tools, no need for new agent
- ✓ Why inline + file options? Balance speed (inline) vs. completeness (file)
- ✓ Why codebase-only? External research already covered by /do:learn
- ✓ Why single-pass? Keep it fast, iteration covered by /do:learn

---

## Blockers and Questions

**NONE** - No blockers identified. Ready to proceed.

---

## Implementation Checklist

**Core Implementation**:
- [ ] P0-1: Create `commands/peek.md`
- [ ] P0-2: Update `agents/researcher.md` with peek mode
- [ ] P0-3: Update `plugin.json` to register command
- [ ] Validate JSON syntax
- [ ] Test researcher agent still works for `/do:learn`

**Testing**:
- [ ] Test Example 1 (simple inline answer)
- [ ] Test Example 2 (complex PEEK.md output)
- [ ] Test Example 3 (pattern lookup)
- [ ] Test fast exit (too broad)
- [ ] Test fast exit (not found)
- [ ] Verify time constraint (<2 min)

**Documentation**:
- [ ] Update `plugins/do-more-now/CLAUDE.md`
- [ ] Update root `CLAUDE.md`

**Completion**:
- [ ] All tests pass
- [ ] Documentation current
- [ ] Ready for real-world usage

---

## Workflow Recommendation

**✓ PROCEED** - Implementation ready to begin.

**Suggested execution**:
1. Start with P0-1 and P0-2 in parallel (create peek.md + update researcher.md)
2. Complete P0-3 (update plugin.json)
3. Manual testing with 5 example scenarios
4. Documentation updates (P1, P2)
5. Final validation

**Estimated completion**: 90 minutes total for fully tested, documented implementation.

**Next command to run**: Begin implementation of P0-1 (create peek.md)
