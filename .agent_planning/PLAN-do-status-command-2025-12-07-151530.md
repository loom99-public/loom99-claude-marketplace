# Implementation Plan: `/do:status` Command

**Generated**: 2025-12-07 15:15:30
**Source**: User requirements + do-more-now plugin architecture analysis
**Spec Reference**: plugins/do-more-now/CLAUDE.md (workflow patterns)

---

## Executive Summary

Implement `/do:status` command to provide quick project status checks without modifying planning documents. The command routes to either full project evaluation (no args) or focused work evaluation (with args), surfaces major issues, and recommends context-appropriate next actions.

**Total Work Items**: 3 (P0: 2, P1: 1)
**Estimated Effort**: Small (1-2 days total)
**Dependencies**: None (all required agents already exist)
**Risk Level**: Low (read-only operation, proven agent patterns)

---

## Backlog by Priority

### P0 (Critical) - Core Functionality

#### P0-1: Create `status.md` Command File

**Status**: Not Started
**Effort**: Small (2-3 hours)
**Dependencies**: None
**Spec Reference**: plugins/do-more-now/CLAUDE.md § Command Structure

**Description**

Create the `/do:status` command file that routes to appropriate evaluator based on arguments. The command is strictly read-only - it invokes existing evaluators to assess current state but never modifies planning documents.

**Key Design Decisions** (from research):
1. **Missing PLAN Handling**: Fail with clear error message directing user to run `/do:plan` first. No auto-creation (preserves read-only semantics).
2. **Auto-Research on PAUSE**: NO. Surface ambiguities but don't resolve them. This is a status check, not a planning operation. Keep it fast.
3. **Next Action Recommendations**: Context-dependent messages (6-8 variants) based on evaluation outcome.

**Acceptance Criteria**

- [ ] Command file exists at `plugins/do-more-now/commands/status.md`
- [ ] Frontmatter includes:
  - `argument-hint: [area of focus]`
  - `description: Check project status using evaluators (read-only)`
- [ ] No arguments → invokes `do:project-evaluator` for full project assessment
- [ ] With arguments → invokes `do:work-evaluator` for focused assessment
- [ ] Missing PLAN/STATUS files → clear error message with guidance to run `/do:plan`
- [ ] PAUSE conditions → surfaces issues to user WITHOUT auto-research
- [ ] Context-appropriate "Next:" recommendations (6+ variants)
- [ ] Displays formatted summary box with key metrics
- [ ] NO file creation (STATUS, PLAN, or otherwise)
- [ ] Follows established command pattern (see `plan.md`, `it.md`)

**Context-Dependent Recommendations**

The command should recommend different next actions based on evaluation outcome:

1. **Missing Planning Docs**: "Next: Run /do:plan to evaluate and create backlog"
2. **Clean State (All Complete)**: "Next: /do:feature-proposal for next feature OR /do:plan [focus] for new area"
3. **Partial Work**: "Next: /do:it to continue implementation OR /do:plan to re-evaluate"
4. **Ambiguities Found**: "Next: /do:learn [question] to research OR /do:plan with research enabled"
5. **Blocked State**: "Next: Review blockers in STATUS file, resolve dependencies"
6. **Test Failures**: "Next: /do:it tdd to fix tests OR review test output in STATUS"
7. **Implementation Complete, Tests Needed**: "Next: /do:it tdd to add test coverage"
8. **Recent Changes**: "Next: /do:plan to update STATUS with latest changes"

**Technical Notes**

**Routing Logic**:
```
if ARGUMENTS empty:
    invoke do:project-evaluator (full project scan)
else:
    invoke do:work-evaluator with focus area
```

**Error Handling**:
- Check for `.agent_planning/` directory existence
- Check for latest PLAN-*.md file (required for work-evaluator)
- Check for PROJECT_SPEC.md or PROJECT.md (required for project-evaluator)
- Graceful failure with actionable error messages

**Agent Behavior**:
- project-evaluator: Runs full gap analysis, creates STATUS file, may return PAUSE
- work-evaluator: Evaluates recent work against PLAN acceptance criteria, runtime validation

**PAUSE Handling** (critical difference from `/do:plan`):
- Display PAUSE message and ambiguities to user
- DO NOT invoke do:researcher
- DO NOT create resolution loop
- Recommend `/do:learn` or `/do:plan` (which has auto-research)

**Output Format**:
```
═══════════════════════════════════════
Status Check Complete
  Evaluator: [project|work]
  Focus: [area OR "full project"]
  State: [COMPLETE|PARTIAL|BLOCKED|PAUSE]
  Issues: [count] | Gaps: [count]
Next: [context-specific recommendation]
═══════════════════════════════════════
```

**File Structure** (60-80 lines estimated):
- Frontmatter: 3 lines
- Introduction/routing logic: 10 lines
- Error handling section: 15 lines
- project-evaluator path: 15 lines
- work-evaluator path: 15 lines
- PAUSE handling: 10 lines
- Output formatting: 12 lines

---

#### P0-2: Update `plugin.json` Command Registration

**Status**: Not Started
**Effort**: Small (15 minutes)
**Dependencies**: P0-1 (status.md must exist)
**Spec Reference**: plugins/do-more-now/.claude-plugin/plugin.json § commands array

**Description**

Add `./commands/status.md` to the commands array in plugin.json so Claude Code recognizes and loads the command.

**Acceptance Criteria**

- [ ] File `plugins/do-more-now/.claude-plugin/plugin.json` updated
- [ ] Entry `"./commands/status.md"` added to `commands` array
- [ ] JSON remains valid (no syntax errors)
- [ ] Alphabetical ordering maintained if applicable
- [ ] File can be parsed by Claude Code plugin loader

**Technical Notes**

Current commands array:
```json
"commands": [
  "./commands/plan.md",
  "./commands/feature-proposal.md",
  "./commands/init-project.md",
  "./commands/learn.md",
  "./commands/it.md"
]
```

Add as 6th entry (likely after `it.md` or in alphabetical position).

---

### P1 (High) - Documentation

#### P1-1: Update CLAUDE.md Command Reference

**Status**: Not Started
**Effort**: Small (1 hour)
**Dependencies**: P0-1, P0-2 (command must be implemented)
**Spec Reference**: plugins/do-more-now/CLAUDE.md § Command Reference

**Description**

Document the `/do:status` command in the plugin's CLAUDE.md file under the "Command Reference" section. Provide usage examples and clarify when to use vs. `/do:plan`.

**Acceptance Criteria**

- [ ] Entry added to "Command Reference" section in CLAUDE.md
- [ ] Documents both usage patterns: `/do:status` and `/do:status [focus]`
- [ ] Explains read-only semantics (doesn't create/modify PLAN files)
- [ ] Clarifies difference from `/do:plan` (status check vs. planning operation)
- [ ] Provides 3+ usage examples
- [ ] Notes PAUSE behavior (surfaces without resolving)
- [ ] Links to related commands (`/do:plan`, `/do:learn`)

**Technical Notes**

**Section Location**: After `/do:it` entry, before or alongside `/feature-proposal`

**Usage Examples to Include**:
1. Quick status check: `/do:status`
2. Focused check on recent feature: `/do:status user authentication`
3. After making manual changes: `/do:status`

**Key Clarifications**:
- Use `/do:status` for read-only status checks (fast, no file creation)
- Use `/do:plan` when you want updated STATUS/PLAN files and auto-research
- Use `/do:status [focus]` to evaluate recent work against acceptance criteria

---

## Dependency Graph

```
P0-1 (Create status.md)
  ↓
P0-2 (Update plugin.json) ──→ P1-1 (Update CLAUDE.md)
```

**Critical Path**: P0-1 → P0-2 (must be sequential)
**Parallelizable**: P1-1 can start after P0-1 completes (doesn't need P0-2)

---

## Recommended Sprint Planning

### Sprint 1: Core Implementation (Day 1)

**Morning**:
- P0-1: Create `status.md` command file
  - Start with command structure (frontmatter, argument handling)
  - Implement routing logic (no args → project-evaluator, with args → work-evaluator)
  - Add error handling for missing files
  - Implement PAUSE handling (surface without resolving)

**Afternoon**:
- P0-1 (continued): Context-dependent recommendations
  - Implement 6-8 recommendation variants
  - Add output formatting
  - Test with various scenarios (missing files, PAUSE, complete, partial)
- P0-2: Update plugin.json
- P1-1: Document in CLAUDE.md

**Validation**:
- Manual test: `/do:status` with no planning docs → expect clear error
- Manual test: `/do:status` with valid project → expect project-evaluator invocation
- Manual test: `/do:status authentication` → expect work-evaluator invocation
- Verify plugin.json is valid JSON
- Review CLAUDE.md documentation for clarity

---

## Risk Assessment

### Low Risk Items

- **P0-1**: Follows established command patterns (`plan.md`, `it.md` are proven templates). Low risk of structural issues.
- **P0-2**: Simple JSON array modification. Low risk if syntax validated.

### Medium Risk Items

- **P1-1**: Documentation clarity depends on user mental model. Medium risk of confusion about `/do:status` vs. `/do:plan` distinction.

### Mitigation Strategies

1. **Pattern Reuse**: Copy structure from `plan.md` as starting point for `status.md` to inherit proven patterns.
2. **JSON Validation**: Use `jq` or JSON linter to validate plugin.json after modification.
3. **Usage Examples**: Include concrete examples in CLAUDE.md to clarify status vs. plan distinction.
4. **Clear Error Messages**: Invest time in error message clarity for missing files (helps users self-correct).

---

## Implementation Notes

### Design Philosophy

The `/do:status` command is intentionally **read-only** and **fast**:

1. **Read-Only**: Never creates or modifies STATUS/PLAN files. Only invokes evaluators that may create their own output files.
2. **Fast**: No auto-research loops. Surfaces issues but doesn't resolve them.
3. **Informative**: Context-aware recommendations guide users to appropriate next command.

### Command vs. Planning Operation

**`/do:status`** (this command):
- Quick status check
- Read-only operation
- Surfaces issues without resolution
- Recommends next action

**`/do:plan`**:
- Creates/updates STATUS and PLAN files
- Auto-research on PAUSE (resolves ambiguities)
- Generates actionable backlog
- Longer operation

### Agent Invocation Patterns

**project-evaluator** (full project):
- Scans entire codebase against PROJECT_SPEC.md
- Creates STATUS-<timestamp>.md (this is the ONE exception to read-only - evaluator creates its own output)
- Returns COMPLETE, PARTIAL, or PAUSE
- May identify gaps, missing components, ambiguities

**work-evaluator** (focused area):
- Reads latest PLAN file
- Evaluates specific work against acceptance criteria
- Requires PLAN to exist (fails if missing)
- Returns COMPLETE, INCOMPLETE, PAUSE, or BLOCKED
- May use chrome-devtools for web UI validation

### Testing Strategy

**Manual Test Scenarios**:

1. **No Planning Docs**: Fresh project, no .agent_planning/ → expect clear error
2. **Full Project Status**: Call `/do:status` on project with PROJECT_SPEC → expect project-evaluator summary
3. **Focused Status**: Call `/do:status authentication` on project with PLAN → expect work-evaluator summary
4. **Missing PLAN**: Call `/do:status authentication` when no PLAN exists → expect error directing to `/do:plan`
5. **PAUSE Condition**: Trigger evaluator PAUSE (ambiguous requirements) → expect issues surfaced without auto-research
6. **Complete State**: Run on fully implemented feature → expect "all complete" message with next recommendations

**Validation Checklist**:
- [ ] Command loads in Claude Code (no plugin.json errors)
- [ ] Argument routing works correctly (no args vs. with args)
- [ ] Error messages are clear and actionable
- [ ] Output formatting is readable and consistent
- [ ] Recommendations make sense for each context
- [ ] No unintended file creation (except evaluator's own output)

---

## Success Criteria

**Implementation Complete When**:
1. `/do:status` command recognized by Claude Code
2. Routes correctly to project-evaluator (no args) or work-evaluator (with args)
3. Handles missing files with clear error messages
4. Surfaces PAUSE conditions without auto-research
5. Provides context-appropriate "Next:" recommendations
6. Documented in CLAUDE.md with examples
7. Manual testing confirms expected behavior in all scenarios

**Quality Standards**:
- Command structure matches existing patterns (plan.md, it.md)
- Error messages are user-friendly and actionable
- Output formatting is clean and scannable
- Documentation includes 3+ concrete usage examples
- PAUSE handling clearly distinguishes from `/do:plan` auto-research

---

## Open Questions

None. All design decisions resolved through research:
1. Missing PLAN handling → Fail with error ✓
2. Auto-research on PAUSE → No, surface only ✓
3. Next action recommendations → Context-dependent (6-8 variants) ✓

---

## References

**Existing Commands** (patterns to follow):
- `plugins/do-more-now/commands/plan.md` - Evaluate + plan workflow
- `plugins/do-more-now/commands/it.md` - Implementation workflows with loops

**Agents** (invoked by this command):
- `plugins/do-more-now/agents/project-evaluator.md` - Full project gap analysis
- `plugins/do-more-now/agents/work-evaluator.md` - Focused work validation

**Plugin Configuration**:
- `plugins/do-more-now/.claude-plugin/plugin.json` - Command registration
- `plugins/do-more-now/CLAUDE.md` - Plugin documentation
