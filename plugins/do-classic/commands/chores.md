---
argument-hint: [quick|thorough] [specific chore]
description: Maintenance tasks - planning file cleanup, git hygiene, debt inventory. Quick or thorough mode.
---

Repository maintenance and housekeeping. The software equivalent of taking out the trash, doing the dishes, and paying the bills.

<chore-args>
$ARGUMENTS
</chore-args>

## Purpose

Tasks we don't want to run every session but need to run regularly. Keeps the repository healthy and prevents entropy accumulation.

**Quick mode**: 5-10 minutes, essential hygiene
**Thorough mode**: 20-40 minutes, deep cleaning + inventory

## Mode Selection

**Auto-select** (recommended):
- If git status is dirty → Quick mode (focus on cleanup first)
- If many stale planning files → Quick mode
- If last thorough chores was recent → Quick mode
- Otherwise → Thorough mode

**Manual override**:
- `quick` or `fast` in args → Quick mode
- `thorough`, `full`, or `deep` in args → Thorough mode

**Specific chore**:
- Pass specific chore name to run just that one

## Quick Chores Checklist

Essential hygiene that should run every 1-2 sessions:

### 1. Git Hygiene
- [ ] Check git status is clean (no uncommitted changes)
- [ ] Review any untracked files - should they be committed or gitignored?
- [ ] Check for merge conflicts
- [ ] Verify on expected branch

### 2. Planning File Cleanup
- [ ] Archive old STATUS-*.md files (keep latest 4)
- [ ] Archive old PLAN-*.md files (keep latest 4)
- [ ] Remove stale PEEK-*.md files (older than 24h)
- [ ] Remove stale WORK-EVALUATION-*.md files (older than 48h)
- [ ] Check for contradictory planning docs

### 3. Quick Code Scan
- [ ] Grep for TODO/FIXME added this session
- [ ] Check for debug code left behind (console.log, print, debugger)
- [ ] Verify no secrets/credentials in recent commits

### 4. Dependency Quick Check
- [ ] Any security warnings from package manager?
- [ ] Lock file in sync with manifest?

**Output**: Summary to console (no file created for quick mode)

```
═══════════════════════════════════════
Quick Chores Complete

  Git: [clean | n issues]
  Planning files: [cleaned up | n archived]
  Code scan: [clean | n items found]
  Dependencies: [ok | warnings]

  Time: [duration]
═══════════════════════════════════════
```

## Thorough Chores Checklist

Deep cleaning that should run every 3-5 sessions or weekly:

### Phase 1: Everything from Quick Chores
Run all quick chores first.

### Phase 2: Commit Quality Review
- [ ] Review last 10-20 commits for quality
- [ ] Check commit message consistency
- [ ] Identify any commits that should be squashed/amended
- [ ] Look for accidental commits (wrong files, secrets)

### Phase 3: Dead Code Detection
- [ ] Find unused imports
- [ ] Find unused functions/classes
- [ ] Find commented-out code blocks
- [ ] Find unreachable code

### Phase 4: Documentation Sync
- [ ] README accuracy check
- [ ] CLAUDE.md accuracy check
- [ ] API documentation currency
- [ ] Remove outdated comments

### Phase 5: Dependency Deep Dive
- [ ] Check for outdated dependencies
- [ ] Review unused dependencies
- [ ] License compatibility check
- [ ] Security vulnerability scan

### Phase 6: Technical Debt Inventory

Create comprehensive problem list:

**Immediate** (should fix this session):
- Broken tests
- Security issues
- Blocking bugs

**Short-term** (fix within 1-2 sessions):
- Code smells
- Missing tests
- Documentation gaps

**Medium-term** (plan for next sprint):
- Refactoring candidates
- Performance issues
- Outdated patterns

**Long-term** (backlog items):
- Architectural improvements
- Major upgrades
- Nice-to-haves

### Phase 7: Cleanup Actions

Actually fix simple issues found:
- Delete dead code
- Remove unused imports
- Archive stale files
- Fix obvious typos
- Commit housekeeping changes

**Output**: `CHORES-<timestamp>.md` in `.agent_planning/`:

```markdown
# Chores Report: [date]

**Mode**: Thorough
**Duration**: [time]

## Summary
- Issues found: [count]
- Issues fixed: [count]
- Items for backlog: [count]

## Git Status
[findings]

## Planning Files
[cleanup actions taken]

## Code Quality
### Dead Code Removed
[list]

### TODOs/FIXMEs Found
[list with locations]

## Dependencies
[status and recommendations]

## Technical Debt Inventory

### Immediate
| Issue | Location | Effort |
|-------|----------|--------|
| ... | ... | ... |

### Short-term
[same format]

### Medium-term
[same format]

### Long-term
[same format]

## Actions Taken
[list of cleanup commits made]

## Recommendations
[what to tackle next]
```

## Display Summary (Thorough)

```
═══════════════════════════════════════
Thorough Chores Complete

  Issues found: [n] | Fixed: [n] | Backlogged: [n]
  Dead code removed: [n items]
  Files archived: [n]
  Commits made: [n housekeeping]

  Report: .agent_planning/CHORES-<ts>.md

Next: Review debt inventory, /do:plan for priorities
═══════════════════════════════════════
```

## Specific Chores

Run individual chores by name:
- `/do:chores git` - Git hygiene only
- `/do:chores planning` - Planning file cleanup only
- `/do:chores dead-code` - Dead code detection only
- `/do:chores deps` - Dependency check only
- `/do:chores debt` - Technical debt inventory only

## Agent Usage

This command orchestrates multiple capabilities:

1. **Git operations**: Direct bash commands (git status, log, diff)
2. **File cleanup**: Direct file operations (archive, delete)
3. **Code analysis**: Grep/Glob for patterns
4. **Debt inventory**: do:project-evaluator in inventory mode
5. **Recommendations**: do:status-planner for prioritization

**Note**: No new agents needed - this orchestrates existing tools and agents.

## Frequency Recommendations

| Chore Type | Frequency |
|------------|-----------|
| Quick | Every 1-2 sessions |
| Thorough | Weekly or every 3-5 sessions |
| Before major release | Always thorough |
| After large merge | Quick at minimum |
