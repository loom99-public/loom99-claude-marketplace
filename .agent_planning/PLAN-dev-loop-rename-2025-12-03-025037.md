# Rename Plan: dev-loop → do-more-now

**Generated**: 2025-12-03-025037
**Source STATUS**: STATUS-2025-12-03-000000.md
**Spec**: CLAUDE.md (loom99-claude-marketplace)
**Approach**: Minimal changes, systematic search/replace, no rewrites

## Scope

Rename plugin from `dev-loop` to `do-more-now` (manifest name: `do`) with command consolidation:
- Directory rename
- Command renames: evaluate-and-plan → plan, research → learn
- Command merge: test-and-implement + implement-and-iterate → it (automatic mode selection)
- Delete 12 duplicate ' 2.md' files
- Update ~120 cross-references
- Aggressively clean archived planning docs

## Execution Phases

### Phase 1: Delete Cruft

**Delete duplicate ' 2.md' files** (12 files):

Commands (5 files):
```
rm "plugins/dev-loop/commands/evaluate-and-plan 2.md"
rm "plugins/dev-loop/commands/feature-proposal 2.md"
rm "plugins/dev-loop/commands/implement-and-iterate 2.md"
rm "plugins/dev-loop/commands/research 2.md"
rm "plugins/dev-loop/commands/test-and-implement 2.md"
```

Agents (7 files):
```
rm "plugins/dev-loop/agents/functional-tester 2.md"
rm "plugins/dev-loop/agents/iterative-implementer 2.md"
rm "plugins/dev-loop/agents/product-visionary 2.md"
rm "plugins/dev-loop/agents/project-evaluator 2.md"
rm "plugins/dev-loop/agents/status-planner 2.md"
rm "plugins/dev-loop/agents/test-driven-implementer 2.md"
rm "plugins/dev-loop/agents/work-evaluator 2.md"
```

**Delete archived planning docs**:
```
rm -rf .agent_planning/archive/
```

### Phase 2: Directory Rename

```bash
mv "plugins/dev-loop" "plugins/do-more-now"
```

All subsequent operations use path: `plugins/do-more-now/`

### Phase 3: Command Operations

**Simple renames**:
```bash
cd plugins/do-more-now/commands/
mv evaluate-and-plan.md plan.md
mv research.md learn.md
```

**Create merged 'it' command**:
- Read test-and-implement.md (TDD workflow)
- Read implement-and-iterate.md (iterative workflow)
- Create it.md with:
  - Lightweight mode detection (~15 lines)
  - Preserve both workflows (no rewrites)
  - Automatic mode: check context → choose TDD or iterative
  - Explicit override: user passes 'tdd' or 'iterate' keyword

**Delete old commands**:
```bash
rm test-and-implement.md
rm implement-and-iterate.md
```

### Phase 4: Manifest Updates

**plugin.json** (plugins/do-more-now/.claude-plugin/plugin.json):
- Change: `"name": "dev-loop"` → `"name": "do"`
- Update commands array:
  - `evaluate-and-plan.md` → `plan.md`
  - `research.md` → `learn.md`
  - Remove: `test-and-implement.md`, `implement-and-iterate.md`
  - Add: `it.md`

**marketplace.json** (.claude-plugin/marketplace.json):
- Change: plugin name `"dev-loop"` → `"do"`
- Change: source path `"./plugins/dev-loop"` → `"./plugins/do-more-now"`

### Phase 5: Cross-Reference Updates

**Pattern replacements** (global search/replace):

Command references:
- `/dev-loop:evaluate-and-plan` → `/do:plan`
- `/dev-loop:test-and-implement` → `/do:it`
- `/dev-loop:implement-and-iterate` → `/do:it`
- `/dev-loop:research` → `/do:learn`
- `/dev-loop:init-project` → `/do:init-project`
- `/dev-loop:feature-proposal` → `/do:feature-proposal`

Agent references:
- `dev-loop:project-evaluator` → `do:project-evaluator`
- `dev-loop:status-planner` → `do:status-planner`
- `dev-loop:functional-tester` → `do:functional-tester`
- `dev-loop:test-driven-implementer` → `do:test-driven-implementer`
- `dev-loop:iterative-implementer` → `do:iterative-implementer`
- `dev-loop:work-evaluator` → `do:work-evaluator`
- `dev-loop:researcher` → `do:researcher`
- `dev-loop:product-visionary` → `do:product-visionary`
- `dev-loop:project-architect` → `do:project-architect`

**Files to update** (~15 files):
1. plugins/do-more-now/CLAUDE.md (~30 refs)
2. plugins/do-more-now/commands/*.md (6 files, ~25 refs)
3. plugins/do-more-now/agents/*.md (9 files, ~15 refs)
4. .claude-plugin/marketplace.json (2 refs)
5. CLAUDE.md (root - document the rename)

### Phase 6: Cleanup Archived Planning Docs

**Delete stale planning files** in `.agent_planning/`:
- All BACKLOG-*.md files (historical, pre-rename)
- All SPRINT-*.md files (historical, pre-rename)
- All PLANNING-SUMMARY-*.md files (stale)
- All TODO-*.md files (stale)
- Keep only: Latest 4 STATUS files, Latest 4 PLAN files, SUMMARY files

**Retention rule**: Keep max 4 of each type (STATUS, PLAN), delete rest.

## 'it' Command Design

**File**: plugins/do-more-now/commands/it.md

**Structure**:
```markdown
---
argument-hint: [area of focus] [mode]
description: Implement functionality. Auto-selects TDD or iterative mode. Pass 'tdd' or 'iterate' to force.
---

# Mode Selection

Check $ARGUMENTS:
- Contains 'tdd' → TDD workflow
- Contains 'iterate' → Iterative workflow
- Otherwise → AUTO:
  - Has test framework → TDD
  - UI feature → Iterative
  - API/logic → TDD

# TDD Workflow
[Preserve content from test-and-implement.md]
- Uses: do:functional-tester, do:test-driven-implementer

# Iterative Workflow
[Preserve content from implement-and-iterate.md]
- Uses: do:iterative-implementer, do:work-evaluator
```

**Key**: Minimal decision logic, preserve all existing workflow content.

## Validation Checklist

- [ ] plugin.json is valid JSON
- [ ] marketplace.json is valid JSON
- [ ] All command files have frontmatter
- [ ] No references to `/dev-loop:` remain
- [ ] No references to `dev-loop:` (agents) remain
- [ ] it.md contains both workflows
- [ ] Duplicate ' 2.md' files deleted
- [ ] Archived planning docs cleaned up

## Risk Mitigation

**Git safety**: All operations traceable via git history (no explicit backup needed per user directive).

**Testing**: Manual spot-checks after cross-reference updates:
1. Verify command references in CLAUDE.md
2. Verify agent references in commands
3. Verify plugin loads in Claude Code

## Complexity Estimates

- Phase 1 (Delete cruft): TRIVIAL
- Phase 2 (Directory rename): SIMPLE
- Phase 3 (Command ops): MODERATE (merge requires reading both files)
- Phase 4 (Manifests): SIMPLE (2 files, JSON edits)
- Phase 5 (Cross-refs): MODERATE (~120 refs, systematic search/replace)
- Phase 6 (Cleanup): SIMPLE (delete old planning files)

**Overall**: MODERATE (mostly mechanical, careful execution required)

## File Inventory

**Critical files** (35 total):
- 1 directory (dev-loop → do-more-now)
- 2 manifests (plugin.json, marketplace.json)
- 6 commands (4 renamed/merged, 2 unchanged)
- 9 agents (agent references updated)
- 1 CLAUDE.md (plugin docs)
- 1 CLAUDE.md (root - document rename)
- 12 duplicates (deleted)
- ~50 archived planning docs (deleted)

**Cross-references**: ~120 updates across 15 files

## Next Steps

1. User approval
2. Execute phases 1-6 sequentially
3. Validate JSON and references
4. Manual testing if possible
5. Document completion

---

**End of Plan**
