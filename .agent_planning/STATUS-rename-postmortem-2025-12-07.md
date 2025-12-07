# Rename Postmortem: dev-loop → do-more-now

**Date**: 2025-12-07
**Operation**: Plugin rename and command consolidation

---

## What We Missed

### 1. Claude Code Plugin Path Caching (CRITICAL)

**Issue**: Claude Code caches the plugin path at session start. Renaming the plugin directory broke the stop hook because Claude was still looking for `plugins/dev-loop/bin/hello.py`.

**Impact**: Stop hook error on every stop attempt until Claude is restarted.

**Root Cause**: We didn't account for runtime caching. The `${CLAUDE_PLUGIN_ROOT}` variable resolves at plugin load time, not at hook execution time.

**Lesson**: Plugin renames require Claude restart. Consider adding to rename checklist: "User must restart Claude Code after plugin directory renames."

---

### 2. Cross-Reference Depth

**Issue**: Initial search/replace missed references in:
- Agent files (`project-evaluator.md`, `researcher.md`)
- Documentation files (`RESTART_INSTRUCTIONS.md`, `FUTURE_IMPROVEMENTS.md`)
- Root docs (`README.md`, `COMING_SOON.md`)
- CLAUDE.md section headers (not just content)

**Impact**: Multiple passes required to find all references.

**Lesson**: Use broader grep patterns FIRST, then filter. Pattern `dev-loop|evaluate-and-plan|test-and-implement` would have caught everything in one pass.

---

### 3. Orphaned Plugin Discovery

**Issue**: `plugins/dev-loop-web` was an orphaned directory (not in marketplace.json) that we discovered late.

**Impact**: Left cruft in the repo until final cleanup.

**Lesson**: Run `find plugins -name "plugin.json"` and compare against marketplace.json BEFORE starting a rename operation.

---

### 4. Command Name Patterns Without Prefix

**Issue**: Some references used the command name without the `/dev-loop:` prefix (e.g., just `evaluate-and-plan` in prose). These weren't caught by initial patterns.

**Impact**: Required additional search patterns.

**Lesson**: Search for bare command names too, not just prefixed versions.

---

### 5. CLAUDE.md File Structure Section

**Issue**: The file tree listing in CLAUDE.md had hardcoded filenames that didn't get updated by search/replace.

**Impact**: File structure docs showed old filenames.

**Lesson**: File structure sections need manual review - they're not caught by content patterns.

---

## What Worked Well

1. **Phased approach**: Delete cruft → Rename dir → Rename files → Update manifests → Cross-refs → Cleanup
2. **JSON validation**: Verified plugin.json and marketplace.json after changes
3. **Merged command design**: The `it.md` command with auto mode selection is cleaner than two separate commands
4. **Aggressive cleanup**: Deleting stale planning docs reduced noise

---

## Production Readiness Gaps

### Must Fix Before Release

1. **Stop hook still uses test script**: `hello.py` just logs to `/tmp`. Real stop logic needed or remove hook entirely.

2. **CLAUDE.md needs coherence review**: After all the search/replace, the docs may have awkward phrasing (e.g., "Use `/do:it` (continued)" as a section header).

3. **No .mcp.json in do-more-now**: The plugin doesn't have an MCP configuration file. If chrome-devtools integration is needed, add it.

### Nice to Have

1. **Update root CLAUDE.md**: The main project CLAUDE.md still documents the old plugin structure.

2. **Test the commands**: Actually run `/do:plan`, `/do:it`, `/do:learn` to verify they work.

3. **Consider removing hooks entirely**: The stop hook is a debugging artifact, not core functionality.

---

## Checklist for Future Renames

```
[ ] Grep for ALL variations of old name (prefixed, bare, in prose)
[ ] Check all plugins directories against marketplace.json
[ ] Review file structure sections in docs
[ ] Validate JSON files
[ ] Check for cached paths (warn user to restart Claude)
[ ] Run commands to verify functionality
[ ] Review doc coherence after bulk edits
```

---

## Files Changed

- **91 files** in commit
- **~43k lines deleted** (mostly old planning docs)
- **~1k lines added** (new it.md, planning docs)

---

## Remaining Work

1. Restart Claude Code to pick up new plugin path
2. Test all commands
3. Review CLAUDE.md for awkward phrasing
4. Decide fate of stop hook (keep, fix, or remove)
