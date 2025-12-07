# Status Report - Symlink Removal & Production Readiness
**Date**: 2025-12-07
**Agent**: project-evaluator
**Focus**: Symlink dependency removal and production readiness assessment

## Executive Summary

**Overall Status**: 80% production-ready | **Critical Issues**: 4 P0, 5 P1, 8 P2, 4 P3
**Symlink Impact**: MODERATE - affects 8 documentation files, no code dependencies
**Production Blockers**: 4 (missing .mcp.json, dev-loop directory, plugin count mismatch, claude4claude broken)

**Recommendation**: FIX P0 issues before production release. Symlink removal is LOW RISK.

**CRITICAL**: claude4claude plugin is BROKEN - references 5 non-existent command files. Plugin will fail to load.

---

## Symlink Analysis

### Current Symlink
- **Location**: `~/icode` → `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode`
- **Status**: ACTIVE and functioning
- **Purpose**: Shorter path alias for iCloud Documents location

### Symlink Usage Assessment

**Files referencing symlink paths** (8 total):
1. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/CLAUDE.md` (line 321)
2. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/DEVELOPMENT.md` (lines 24, 76, 333, 637, 695)
3. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/NEXT_STEPS.md` (lines 310, 371)
4. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/tests/README.md` (line 122)
5. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/TEST_SUMMARY.md` (line 172)
6. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/do-more-now/RESTART_INSTRUCTIONS.md` (lines 122, 138, 150)

**Impact**: ALL DOCUMENTATION ONLY. No code files reference symlink.

**Full iCloud path references** (38 occurrences in `.agent_planning/STATUS-2025-12-03-000000.md`):
- All in old status file for dev-loop rename operation
- Not production-critical, can be archived

### Symlink Removal Plan

**Risk Assessment**: LOW RISK
- No production code depends on symlink
- Only documentation references exist
- Users can use either path format

**Options**:

#### Option A: KEEP SYMLINK (Recommended)
**Rationale**:
- Symlink provides user convenience (shorter paths)
- No production code dependencies exist
- iCloud Documents path is unwieldy (`/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode`)
- Documentation can reference both paths

**Changes needed**: NONE

**Pros**:
- Zero migration effort
- Users can use shorter path
- No risk of breaking workflows

**Cons**:
- Adds system dependency
- Non-portable to other systems

#### Option B: REMOVE SYMLINK AND UPDATE DOCS
**Rationale**:
- Eliminate external dependency
- Make paths explicit and portable

**Changes needed**: 8 files
1. CLAUDE.md - Remove line 320-322 (symlink instruction)
2. DEVELOPMENT.md - Replace 6 references with full path
3. NEXT_STEPS.md - Replace 2 references with full path
4. tests/README.md - Replace 1 reference with full path
5. TEST_SUMMARY.md - Replace 1 reference with full path
6. plugins/do-more-now/RESTART_INSTRUCTIONS.md - Replace 3 references with full path
7. Update global CLAUDE.md in `~/.claude/` to remove symlink instruction
8. Archive `.agent_planning/STATUS-2025-12-03-000000.md` (38 references, but old status file)

**Pros**:
- No external dependencies
- Explicit, portable paths

**Cons**:
- Longer, harder-to-read paths in docs
- Breaking change for existing users who use symlink

#### Option C: SUPPORT BOTH (Best for public marketplace)
**Rationale**:
- Document both path formats
- Users choose convenience vs. portability

**Changes needed**: 1 file
- Update CLAUDE.md and README.md to document both path options:
  ```markdown
  ## Installation Paths

  You can reference this repository using either:
  - Short path (requires symlink): `~/icode/loom99-claude-marketplace`
  - Full path (no dependencies): `/Users/YOUR_USERNAME/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace`

  ### Setting up the symlink (optional)
  `ln -s "/Users/$USER/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode" ~/icode`
  ```

**Pros**:
- User choice
- Accommodates both use cases
- Minimal changes

**Cons**:
- Two ways to do same thing (documentation burden)

**RECOMMENDATION**: **Option A (KEEP SYMLINK)** - Zero risk, user convenience, no production impact.

---

## Production Readiness Assessment

### Plugin Inventory

**Marketplace declares 6 plugins**:
1. **agent-loop** (v0.1.0) - Explore→Plan→Code→Commit workflow
2. **epti** (v0.1.0) - Evaluate-Plan-Test-Implement (TDD)
3. **visual-iteration** (v0.1.0) - Screenshot-driven UI development
4. **promptctl** (v0.1.0) - Hook-based automation
5. **do** (v0.1.0) - Do-more-now (TDD + iterative workflows)
6. **claude4claude** (v0.1.0) - Plugin/skill/MCP builder tools

**Undocumented directory exists**:
- `plugins/dev-loop/` - UNTRACKED in git, appears to be old version of do-more-now

### Critical Issues (P0) - PRODUCTION BLOCKERS

#### P0-1: do-more-now plugin missing .mcp.json
**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/do-more-now/.mcp.json`
**Status**: MISSING
**Impact**: Plugin manifest references `.mcp.json` at line 15, but file doesn't exist
**Evidence**: `plugin.json` does not include mcpServers field, plugin has no MCP integration
**Root Cause**: do-more-now likely doesn't need MCP servers (uses chrome-devtools via work-evaluator coordination, not direct integration)

**Fix**: Either:
- Remove `mcpServers` reference from plugin.json (if no MCP needed)
- Create `.mcp.json` with chrome-devtools configuration (if MCP integration desired)

**Recommendation**: Check if work-evaluator agent needs chrome-devtools MCP. If yes, create `.mcp.json`:
```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-chrome-devtools"],
    "env": {}
  }
}
```

If no, remove mcpServers line from plugin.json.

#### P0-2: claude4claude plugin missing .mcp.json and hooks
**Files**:
- `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/claude4claude/.mcp.json` - MISSING
- `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/claude4claude/hooks/` - DIRECTORY DOESN'T EXIST

**Status**: Plugin manifest does NOT reference these files
**Impact**: INCONSISTENT configuration compared to other plugins
**Evidence**: `plugin.json` has no `mcpServers` or `hooks` fields - this is VALID

**Analysis**: claude4claude is a tools-only plugin (skills for creating other artifacts). It doesn't need hooks or MCP servers.

**Fix**: NONE NEEDED - plugin.json is correct. Remove from P0 list.

**Reclassification**: NOT AN ISSUE (design choice, not defect)

#### P0-2B: claude4claude plugin references non-existent command files (CRITICAL)
**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/claude4claude/.claude-plugin/plugin.json`
**Lines**: 11-17
**Status**: BROKEN PLUGIN - references 5 command files that DO NOT EXIST
**Evidence**:
- Plugin.json declares commands array with 5 files
- Directory `plugins/claude4claude/commands/` DOES NOT EXIST
- No command markdown files found anywhere in claude4claude plugin

**Referenced but missing files**:
1. ./commands/agent-create.md
2. ./commands/command-create.md
3. ./commands/hook-create.md
4. ./commands/mcp-create.md
5. ./commands/skill-create.md

**Impact**: PRODUCTION BLOCKER - plugin will fail to load in Claude Code with strict mode enabled

**Fix Options**:
1. **Remove commands field** from plugin.json (if skills-only plugin)
2. **Create command files** if commands are intended functionality
3. **Change to skills-only plugin** - this appears to be intended behavior (plugin provides skills, not commands)

**Recommendation**: REMOVE commands array from plugin.json - this is a skills-only plugin providing mcp-builder and skill-creator skills. The skills have their own initialization scripts.

**Updated plugin.json should be**:
```json
{
  "name": "claude4claude",
  "version": "0.1.0",
  "description": "Claude plugin for working with Claude artifacts (MCP, skills, plugins, agents, commands, etc)",
  "author": {
    "name": "Brandon Fryslie",
    "email": "brandon.fryslie.public@gmail.com"
  },
  "license": "MIT",
  "keywords": ["development", "workflow", "testing", "implementation", "planning", "tdd"],
  "skills": [
    "./skills/mcp-builder",
    "./skills/skill-creator"
  ]
}
```

#### P0-3: dev-loop directory exists but not in marketplace
**Directory**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/`
**Status**: EXISTS on filesystem, UNTRACKED in git, NOT in marketplace.json
**Impact**: CONFUSION - appears to be old name for do-more-now plugin
**Evidence**:
- Git status shows `plugins/dev-loop` as untracked
- Marketplace has "do" plugin pointing to `plugins/do-more-now`
- `.agent_planning/STATUS-2025-12-03-000000.md` describes rename operation from dev-loop to do-more-now

**Fix**: DELETE plugins/dev-loop directory (cleanup leftover from rename)

**Command**: `rm -rf /Users/bmf/Library/Mobile\ Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop`

#### P0-4: CLAUDE.md documents 4 plugins, marketplace has 6
**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/CLAUDE.md`
**Lines**: 9, 274
**Status**: DOCUMENTATION MISMATCH
**Evidence**:
- Line 9: "approximately 24,400 lines of plugin implementation code across 4 plugins: agent-loop, epti, visual-iteration, and promptctl"
- Line 274: "**Plugins**: 4 total (agent-loop, epti, visual-iteration, promptctl)"
- Marketplace.json declares 6 plugins (includes do-more-now and claude4claude)

**Impact**: MISLEADING documentation for users

**Fix**: Update CLAUDE.md to reflect all 6 plugins with accurate descriptions

### High Priority Issues (P1)

#### P1-1: Missing plugin READMEs
**Files missing**:
- `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/epti/README.md`
- `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/visual-iteration/README.md`
- `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/do-more-now/README.md`
- `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/claude4claude/README.md`

**Status**: Only agent-loop and promptctl have README.md files
**Impact**: Poor user experience, no quick-start guides
**Severity**: High - reduces discoverability and usability

**Fix**: Create README.md for each plugin with:
- Quick start
- Command reference
- Example workflows
- Use cases

#### P1-2: Promptctl plugin.json has typo in author URL
**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/promptctl/.claude-plugin/plugin.json`
**Line**: 8
**Issue**: URL has backtick: `https://gith`ub.com/brandon-fryslie` (should be `https://github.com/brandon-fryslie`)

**Fix**: Remove backtick from line 8

#### P1-3: Marketplace owner email is empty
**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/.claude-plugin/marketplace.json`
**Line**: 5
**Issue**: `"email": ""` - empty email for marketplace owner

**Impact**: No contact information for marketplace

**Fix**: Add email or remove field if not needed

#### P1-4: Multiple plugin.json files have empty author email
**Files**:
- agent-loop/plugin.json line 7
- epti/plugin.json line 7
- visual-iteration/plugin.json line 7
- do-more-now/plugin.json line 7
- promptctl/plugin.json line 7

**Impact**: Inconsistent author attribution, no contact info

**Fix**: Either:
- Add email to all plugins
- Remove email field (keep just name)

#### P1-5: TODO/FIXME comments in plugin production code
**Files with TODO in production content**:
- `plugins/claude4claude/skills/skill-creator/scripts/init_skill.py` - Lines 20, 27, 31, 57, 59, 119, 266
  - **Context**: This is a TEMPLATE GENERATOR - TODOs are INTENTIONAL placeholders for generated files
  - **Reclassification**: NOT A DEFECT - working as designed

**Files with TODO in documentation/examples**:
- `plugins/epti/commands/commit-code.md` - Lines 14, 40 (examples of what to check)
- `plugins/agent-loop/commands/commit.md` - Lines 14, 72 (examples of what to check)
- `plugins/agent-loop/skills/code-exploration/SKILL.md` - Line 235 (guidance: "look for TODOs")
- `plugins/do-more-now/agents/*` - Multiple files (guidance about TODO files and avoiding TODOs)

**Analysis**: All TODO references are in:
1. Documentation explaining what to check
2. Template generators (intentional placeholders)
3. Guidance about avoiding TODOs

**Reclassification**: P3 (documentation clarity) - not production code issue

### Medium Priority Issues (P2)

#### P2-1: Inconsistent plugin.json structure
**Issue**: Some plugins use arrays, some use directory paths
- agent-loop: Explicit command array, agents array, skills directory
- epti: All directories
- visual-iteration: All directories
- do-more-now: Command array, agent array (no skills/hooks/mcpServers fields)
- claude4claude: Command array, skills array

**Impact**: Inconsistent but VALID per Claude plugin spec (supports both)

**Fix**: Not required, but could standardize for consistency

#### P2-2: MCP server configuration inconsistencies
**Files**:
- visual-iteration/.mcp.json - uses "browser-tools" (correct package name)
- agent-loop/.mcp.json - empty `{}`
- epti/.mcp.json - empty `{}`
- promptctl/.mcp.json - has nested "mcpServers" wrapper (unusual structure)

**Impact**: Empty MCP configs suggest unused files

**Fix**:
- Remove empty .mcp.json files from agent-loop and epti if not needed
- Verify promptctl MCP config format (nested structure unusual)

#### P2-3: Global CLAUDE.md symlink instruction
**File**: `~/.claude/CLAUDE.md` (user's global config)
**Line**: Unknown (needs verification)
**Issue**: Global instructions mention using symlink for this project

**Impact**: User-specific configuration, not repository issue

**Fix**: Update user's global CLAUDE.md if symlink removal chosen

#### P2-4: Plugin "do" vs "do-more-now" naming inconsistency
**Marketplace**: Plugin name is "do", source is "./plugins/do-more-now"
**Directory**: Plugin directory is "do-more-now"
**Commands**: Commands use "/do:" prefix

**Impact**: User confusion (install "do" but directory is "do-more-now")

**Fix**: Either:
- Rename directory to "do" (breaking change)
- Change plugin name to "do-more-now" in marketplace (more descriptive)
- Document the naming clearly in README

**Recommendation**: Keep as-is but document clearly: "Install as 'do', stored in 'do-more-now' directory"

#### P2-5: Line count metrics in CLAUDE.md outdated
**File**: CLAUDE.md
**Lines**: 100, 130, 163, 259-264
**Issue**: Documents specific line counts that may be outdated

**Impact**: Misleading metrics

**Fix**: Remove specific line counts or add "approximate" qualifier

#### P2-6: .DS_Store files in repository
**Files**:
- `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/.DS_Store`
- `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/.DS_Store`

**Status**: .DS_Store is in .gitignore but files exist in git history

**Impact**: Pollutes repository with macOS metadata

**Fix**: Remove from git history:
```bash
git rm --cached .DS_Store plugins/dev-loop/.DS_Store
git commit -m "chore: remove .DS_Store files"
```

#### P2-7: .venv directories exist in plugin directories
**Location**: `plugins/promptctl/.venv/`

**Status**: .venv is in .gitignore, not tracked

**Impact**: Takes up disk space, not in git

**Fix**: Run `rm -rf plugins/*/.venv` to clean up local environments

#### P2-8: Absolute paths in test files reference iCloud full path
**File**: `tests/e2e/design/ARCHITECTURE.md`
**Lines**: 244, 430, 495
**Issue**: Hardcoded absolute paths to specific user directory

**Impact**: Tests won't work on other systems

**Fix**: Use relative paths or environment variables

### Low Priority Issues (P3)

#### P3-1: Stale agent_planning status file
**File**: `.agent_planning/STATUS-2025-12-03-000000.md`
**Issue**: Contains 38 references to full iCloud path from dev-loop rename operation

**Impact**: Confusing if users read old status files

**Fix**: Archive to `.agent_planning/archive/` directory

#### P3-2: Empty env objects in .mcp.json
**Files**: All .mcp.json files have `"env": {}`

**Impact**: None (valid but unnecessary)

**Fix**: Remove empty env objects or keep for future use

#### P3-3: Missing keywords in some plugin.json files
**Issue**: Keywords vary widely in quality/quantity

**Impact**: Search/discovery in marketplace

**Fix**: Review and standardize keyword sets

#### P3-4: No LICENSE files in plugin directories
**Status**: All plugins declare MIT license in plugin.json, but no LICENSE file in plugin directories

**Impact**: License text not distributed with plugins

**Fix**: Add LICENSE or LICENSE.txt to each plugin directory

---

## File Structure Validation

### Validated Components

**Marketplace manifest**: ✅ VALID JSON, all 6 plugins properly declared
**Plugin manifests**: ✅ ALL VALID JSON (6 of 6)
**MCP configs**: ✅ ALL VALID JSON (4 of 4 that exist)
**Hook configs**: ✅ ALL VALID JSON (5 of 5)

### Component Inventory

| Plugin | Commands | Agents | Skills | Hooks | MCP | README |
|--------|----------|--------|--------|-------|-----|--------|
| agent-loop | 4 | 1 | 4 dirs | ✅ | ✅ (empty) | ✅ |
| epti | 6 | 1 | 5 dirs | ✅ | ✅ (empty) | ❌ |
| visual-iteration | 6 | 1 | 4 dirs | ✅ | ✅ | ❌ |
| promptctl | 0 | 0 | 0 | ✅ | ✅ | ✅ |
| do-more-now | 5 | 9 | 0 | ✅ | ❌ | ❌ |
| claude4claude | 0 (5 broken*) | 0 | 2 dirs | N/A | N/A | ❌ |

*claude4claude plugin.json references 5 command files that DO NOT EXIST - P0 BLOCKER

### Missing Components Check

**claude4claude commands referenced but DO NOT EXIST**:
- ./commands/agent-create.md - MISSING
- ./commands/command-create.md - MISSING
- ./commands/hook-create.md - MISSING
- ./commands/mcp-create.md - MISSING
- ./commands/skill-create.md - MISSING

**Status**: VERIFIED - commands directory does not exist, plugin.json is INCORRECT
**Severity**: P0 - Plugin will fail to load with strict mode
**Fix**: Remove commands field from plugin.json (this is a skills-only plugin)

---

## Production Readiness Checklist

### MUST FIX (P0) - PRODUCTION BLOCKERS
- [ ] P0-1: Resolve do-more-now .mcp.json (add file or remove reference)
- [ ] P0-2B: Fix claude4claude plugin.json - remove non-existent commands array (CRITICAL)
- [ ] P0-3: Delete plugins/dev-loop directory (cleanup)
- [ ] P0-4: Update CLAUDE.md to document all 6 plugins accurately

### SHOULD FIX (P1)
- [ ] P1-1: Create README.md for epti, visual-iteration, do-more-now, claude4claude
- [ ] P1-2: Fix typo in promptctl plugin.json author URL
- [ ] P1-3: Add or remove marketplace owner email
- [ ] P1-4: Standardize plugin author emails (add or remove)
- [ ] P0-2B: Fix claude4claude plugin.json - remove non-existent commands field (CRITICAL)

### NICE TO FIX (P2)
- [ ] P2-1: Consider standardizing plugin.json structure
- [ ] P2-2: Remove empty .mcp.json files or populate them
- [ ] P2-4: Document "do" vs "do-more-now" naming
- [ ] P2-5: Update or remove line count metrics
- [ ] P2-6: Remove .DS_Store from git
- [ ] P2-8: Fix hardcoded paths in test files

### POLISH (P3)
- [ ] P3-1: Archive old status files
- [ ] P3-2: Clean up empty env objects
- [ ] P3-3: Standardize keywords
- [ ] P3-4: Add LICENSE files to plugin directories

---

## Recommendations

### Immediate Actions (Before Production Release)

1. **Fix P0 issues** (est. 45 minutes):
   ```bash
   # 1. Delete dev-loop directory
   rm -rf plugins/dev-loop

   # 2. Fix claude4claude plugin.json - remove commands field
   # Edit plugins/claude4claude/.claude-plugin/plugin.json
   # Remove lines 11-17 (commands array)

   # 3. Update CLAUDE.md with all 6 plugins
   # (manual edit required)

   # 4. Resolve do-more-now MCP config
   # Option A: Remove mcpServers reference if not needed
   # Option B: Create .mcp.json with chrome-devtools if needed
   # (decision needed: check if work-evaluator needs chrome-devtools)
   ```

3. **Create missing READMEs** (est. 2-4 hours):
   - Copy agent-loop README.md structure
   - Customize for each plugin
   - Include quick start, commands, examples

### Symlink Decision

**Recommendation**: **KEEP SYMLINK** (Option A)
- Zero risk
- User convenience
- No production code impact
- No migration needed

If removing symlink is required for portability:
- Update 8 documentation files
- Provide migration guide for users
- Consider Option C (support both) for flexibility

### Post-Release Improvements

1. **Standardize structure** (P2 issues):
   - Create plugin development guide
   - Document MCP integration patterns
   - Standardize plugin.json format

2. **Improve discoverability** (P3 issues):
   - Add LICENSE files
   - Improve keywords
   - Create marketplace landing page

3. **Clean up technical debt**:
   - Archive old status files
   - Remove .DS_Store from history
   - Fix test absolute paths

---

## Risk Assessment

### Production Release Risk: MEDIUM-LOW

**Blockers**: 3 P0 issues (fixable in under 1 hour)
**Quality**: High (all JSON valid, comprehensive implementation)
**Documentation**: Good (needs README additions)
**Testing**: Untested in production Claude Code environment

**Safe to release after**: P0 fixes + claude4claude verification

### Symlink Removal Risk: LOW

**Code impact**: ZERO (no code references symlink)
**User impact**: DOCUMENTATION ONLY
**Migration effort**: 8 files or zero files (if keeping symlink)

---

## Evidence Summary

**Files analyzed**: 2,876 plugin files, 8 documentation files, 6 plugin manifests, 1 marketplace manifest
**Lines of code**: ~50,000+ across all plugins and documentation
**JSON validation**: 11/11 files valid
**Git status**: 18 commits ahead of origin, 1 untracked directory (dev-loop)

**Assessment date**: 2025-12-07
**Working directory**: `/Users/bmf/icode/loom99-claude-marketplace`
**Symlink**: `~/icode` → `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode` (ACTIVE)

---

## Appendix: File References

### Symlink References by File

**CLAUDE.md** (1 reference):
- Line 320-322: Documents symlink usage for shorter paths

**DEVELOPMENT.md** (6 references):
- Line 24: cd ~/icode/loom99-claude-marketplace
- Line 76: /plugin marketplace add ~/icode/loom99-claude-marketplace
- Line 333: ls ~/icode/loom99-claude-marketplace/.claude-plugin/marketplace.json
- Line 637: /plugin marketplace add ~/icode/loom99-claude-marketplace
- Line 695: cd ~/icode/loom99-claude-marketplace

**NEXT_STEPS.md** (2 references):
- Lines 310, 371: Full iCloud path usage in examples

**tests/README.md** (1 reference):
- Line 122: cd ~/icode/loom99-claude-marketplace

**TEST_SUMMARY.md** (1 reference):
- Line 172: cd ~/icode/loom99-claude-marketplace

**plugins/do-more-now/RESTART_INSTRUCTIONS.md** (3 references):
- Lines 122, 138: cd ~/icode/loom99-claude-marketplace
- Line 150: Source files path reference

Total: 14 user-facing references across 6 files

### Full iCloud Path References

**tests/e2e/design/ARCHITECTURE.md** (3 references):
- Lines 244, 430, 495: Hardcoded absolute paths in test architecture

**.agent_planning/STATUS-2025-12-03-000000.md** (38 references):
- All references related to dev-loop rename operation
- File should be archived

Total: 41 references (38 archivable, 3 requiring fix for test portability)
