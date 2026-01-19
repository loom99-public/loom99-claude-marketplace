# Evaluation: Fix Empty Hooks

**Generated**: 2026-01-19
**Topic**: Empty hooks.json vs documented hook functionality

## Current State

### The Problem

`plugins/do-more/hooks/hooks.json` contains only `{"hooks": {}}` - empty.

However, documentation claims:
1. **SessionStart hook** (`bin/init.py`) - Creates directories, initializes tracking
2. **Stop hook** (`bin/aggregate-exec.py`) - Aggregates partial logs
3. **execution-summarizer agent** - Runs on "All commands"

**None of this functionality exists.** The `bin/` directory doesn't exist in do-more.

### Documentation vs Reality

| Feature | Documented In | Actual State |
|---------|---------------|--------------|
| `bin/init.py` | CLAUDE.md, README.md, architecture/*.md | Does not exist |
| `bin/aggregate-exec.py` | CLAUDE.md, README.md, architecture/*.md | Does not exist |
| SessionStart hook | hooks.json schema | Empty |
| Stop hook | hooks.json schema | Empty |
| Execution tracking dirs | `.agent_logs/do/` | No hook creates them |
| `execution-summarizer` | `agents/execution-summarizer.md` | Agent exists but not invoked |

## Options Analysis

### Option A: Implement the Hooks
- Create `bin/init.py` and `bin/aggregate-exec.py`
- Populate `hooks.json` with SessionStart and Stop hooks
- Wire up execution-summarizer agent

**Pros:** Makes documented features work, provides execution tracking
**Cons:** Medium effort, adds complexity, hooks need careful error handling

### Option B: Remove False Documentation
- Delete claims about hooks from all documentation
- Note `execution-summarizer` as "future work"
- Clean up orphaned FEATURE_PROPOSAL file

**Pros:** Low effort, aligns documentation with reality
**Cons:** Loses planned functionality

## Recommendation: **Option B - Remove False Documentation**

**Rationale:**

1. **One Source of Truth violated**: Documentation claims features that don't exist - actively misleading
2. **Complexity cost**: do plugin already has hooks; adding more creates conflicts
3. **Feature value unclear**: Execution logging was never validated for actual need
4. **Immediate debt vs aspirational**: Fix misleading docs first, implement later when needed

## Verdict

**CONTINUE** with Option B (remove false documentation).
