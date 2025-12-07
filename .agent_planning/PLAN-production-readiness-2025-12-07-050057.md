# Production Readiness Plan
**Generated**: 2025-12-07-050057
**Source STATUS**: STATUS-symlink-removal-production-readiness-2025-12-07.md
**Spec Source**: CLAUDE.md (last modified 2025-12-07)
**Agent**: status-planner

---

## Executive Summary

**Current State**: 80% production-ready with 4 critical blockers (P0) and 5 high-priority issues (P1)
**Total Gap**: 21 issues across P0-P3 priorities
**Recommended Focus**: Fix all P0 issues before production release (est. complexity: Small)

**Critical Findings**:
1. **claude4claude plugin BROKEN** - references 5 non-existent command files, will fail to load
2. **dev-loop directory exists** - leftover from rename, causing confusion
3. **Documentation mismatch** - CLAUDE.md documents 4 plugins, marketplace has 6
4. **MCP config missing** - do-more-now plugin.json references .mcp.json that doesn't exist

**Symlink Decision**: Per user request, **KEEP SYMLINK** (evaluator recommendation) - zero changes needed

---

## Backlog by Priority

### P0 (Critical) - Production Blockers

#### P0-1: Fix claude4claude Broken Plugin Manifest

**Status**: Not Started
**Effort**: Small
**Dependencies**: None
**Spec Reference**: CLAUDE.md §Plugin Structure • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P0-2B (lines 177-220)

##### Description
The claude4claude plugin.json references 5 command files that DO NOT EXIST. The `commands` directory doesn't exist at all. This will cause plugin loading failure in strict mode. Analysis shows this is a skills-only plugin (provides mcp-builder and skill-creator skills), so commands array should be removed entirely.

**Referenced but missing files**:
- ./commands/agent-create.md
- ./commands/command-create.md
- ./commands/hook-create.md
- ./commands/mcp-create.md
- ./commands/skill-create.md

##### Acceptance Criteria
- [ ] Commands array removed from `plugins/claude4claude/.claude-plugin/plugin.json`
- [ ] Plugin.json contains only: name, version, description, author, license, keywords, skills
- [ ] Skills array remains intact (./skills/mcp-builder, ./skills/skill-creator)
- [ ] JSON validates successfully
- [ ] Plugin loads without errors in Claude Code strict mode (manual test)

##### Technical Notes
**File to modify**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/claude4claude/.claude-plugin/plugin.json`

**Change**: Remove lines 11-17 (entire commands array)

**Resulting structure**:
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

**Commit Message Template**:
```
fix(claude4claude): remove non-existent commands from plugin manifest

The claude4claude plugin is skills-only and does not provide slash
commands. Removed commands array that referenced 5 non-existent files
which would cause plugin loading failure in strict mode.

Fixes: P0-1
```

---

#### P0-2: Resolve do-more-now Missing .mcp.json

**Status**: Not Started
**Effort**: Small
**Dependencies**: None (requires user decision)
**Spec Reference**: CLAUDE.md §Plugin Structure §MCP Configurations • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P0-1 (lines 138-160)

##### Description
The do-more-now plugin.json references `.mcp.json` in the mcpServers field, but the file doesn't exist. Need to determine if chrome-devtools MCP integration is needed (used by work-evaluator agent for browser testing) or if the reference should be removed.

##### Acceptance Criteria
- [ ] User decision made: create .mcp.json OR remove mcpServers reference
- [ ] If creating: .mcp.json contains chrome-devtools configuration
- [ ] If removing: mcpServers field removed from plugin.json
- [ ] Plugin loads without errors
- [ ] work-evaluator agent functions correctly (manual test)

##### Technical Notes
**File to check**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/do-more-now/.claude-plugin/plugin.json`

**Decision Required**: Does work-evaluator agent need chrome-devtools MCP server?

**Option A - Create .mcp.json** (if MCP needed):
```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-chrome-devtools"],
    "env": {}
  }
}
```

**Option B - Remove mcpServers** (if MCP not needed):
Remove mcpServers field from plugin.json entirely.

**Commit Message Template (Option A)**:
```
feat(do-more-now): add chrome-devtools MCP configuration

Added .mcp.json with chrome-devtools server for work-evaluator
agent's browser testing capabilities.

Fixes: P0-2
```

**Commit Message Template (Option B)**:
```
fix(do-more-now): remove unused mcpServers reference

Plugin does not require MCP server integration. Removed mcpServers
field that referenced non-existent .mcp.json file.

Fixes: P0-2
```

---

#### P0-3: Delete Leftover dev-loop Directory

**Status**: Not Started
**Effort**: Small
**Dependencies**: None
**Spec Reference**: CLAUDE.md §Repository Structure • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P0-3 (lines 221-232)

##### Description
The `plugins/dev-loop/` directory exists on filesystem and is untracked in git. This is leftover from the dev-loop → do-more-now rename operation. It causes confusion and should be deleted to prevent users from finding outdated code.

##### Acceptance Criteria
- [ ] `plugins/dev-loop/` directory completely removed from filesystem
- [ ] Git status shows no untracked dev-loop directory
- [ ] Marketplace.json continues to reference only "do" plugin at "./plugins/do-more-now"
- [ ] No references to dev-loop remain in active documentation

##### Technical Notes
**Command**:
```bash
rm -rf "/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop"
```

**Verification**:
```bash
ls "/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/" | grep dev-loop
# Should return nothing
```

**Commit Message Template**:
```
chore: remove leftover dev-loop directory

Cleanup of old dev-loop plugin directory after rename to do-more-now.
Directory was untracked and contained outdated code.

Fixes: P0-3
```

---

#### P0-4: Update CLAUDE.md Plugin Inventory

**Status**: Not Started
**Effort**: Medium
**Dependencies**: None
**Spec Reference**: CLAUDE.md §Current Plugins • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P0-4 (lines 234-245)

##### Description
CLAUDE.md documents 4 plugins (agent-loop, epti, visual-iteration, promptctl) but the marketplace contains 6 plugins (also includes do-more-now and claude4claude). This creates misleading documentation for users and incorrect line count statistics.

**Affected sections**:
- Line 9: "approximately 24,400 lines of plugin implementation code across 4 plugins"
- Line 274: "**Plugins**: 4 total (agent-loop, epti, visual-iteration, promptctl)"
- Missing: Complete do-more-now plugin documentation
- Missing: Complete claude4claude plugin documentation

##### Acceptance Criteria
- [ ] CLAUDE.md §Current Plugins includes all 6 plugins with full descriptions
- [ ] Plugin count updated to 6 in all locations (line 9, line 274)
- [ ] do-more-now plugin documented with: purpose, status, implementation details, commands, agents, skills
- [ ] claude4claude plugin documented with: purpose, status, implementation details, skills
- [ ] Line count statistics updated or marked as "approximate"
- [ ] Component counts table updated with all 6 plugins

##### Technical Notes
**File to modify**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/CLAUDE.md`

**Required changes**:

1. **Update line 9** (§Project Overview):
```markdown
**Current State**: Implementation 95% complete. The marketplace contains approximately
30,000+ lines of plugin implementation code across 6 plugins: agent-loop, epti,
visual-iteration, promptctl, do-more-now, and claude4claude.
```

2. **Update line 274** (§Component Counts):
```markdown
- **Plugins**: 6 total (agent-loop, epti, visual-iteration, promptctl, do-more-now, claude4claude)
```

3. **Add section after visual-iteration** (around line 150):
```markdown
#### 4. promptctl (v0.1.0)
[existing content - verify completeness]

#### 5. do-more-now (v0.1.0)

**Purpose**: Do-More-Now workflow providing integrated TDD and iterative development workflows

**Status**: Implementation complete. Awaiting manual testing.

**Implementation Details**:
- **Agents**: 9 specialized workflow agents (project-evaluator, work-evaluator, project-architect, etc.)
- **Commands**: 5 workflow commands
  - `/do:plan` - Evaluate and create implementation plan
  - `/do:it` - Implement with auto-selected mode (TDD or iterative)
  - `/do:learn` - Research problem through iterative exploration
  - `/do:feature-proposal` - Generate user-focused feature proposals
  - `/do:init-project` - Initialize new project with guided setup
- **Skills**: 0 (uses agent-driven workflows)
- **Hooks**: Configured for pre-commit, post-code, commit-msg validation

**Total Lines**: ~8,000+ lines of implementation (9 agents + 5 commands)

**Testing Status**: Ready for manual testing. No execution data yet.

**Key Features**:
- Auto-selects TDD or iterative mode based on context
- Integrated planning and evaluation workflows
- Research loop for problem exploration
- Project initialization with adaptive questioning

#### 6. claude4claude (v0.1.0)

**Purpose**: Developer tools for creating Claude artifacts (MCP servers, skills, plugins, agents, commands)

**Status**: Implementation complete. Skills-only plugin.

**Implementation Details**:
- **Agents**: 0 (skills provide standalone functionality)
- **Commands**: 0 (skills-only plugin)
- **Skills**: 2 comprehensive builder skills
  - mcp-builder - Guide for creating high-quality MCP servers (Python FastMCP / Node MCP SDK)
  - skill-creator - Guide for creating effective Claude skills
- **Hooks**: N/A (no hooks needed)

**Total Lines**: ~2,000+ lines of implementation (2 skills with scaffolding)

**Testing Status**: Ready for manual testing.

**Framework Support**: FastMCP (Python), MCP SDK (Node/TypeScript), Claude plugin system
```

4. **Update Component Counts table** (line ~274):
```markdown
### Component Counts

- **Plugins**: 6 total (agent-loop, epti, visual-iteration, promptctl, do-more-now, claude4claude)
- **Agents**: 3 command-based + 9 do-more-now agents (12 total)
- **Commands**: 21 total commands implemented (4+6+6+0+5+0)
- **Skills**: 15 total skills implemented (4+5+4+0+0+2)
- **Hooks**: Multiple hook configurations across plugins
- **MCP Configurations**: browser-tools (visual-iteration), promptctl MCP server, chrome-devtools (do-more-now, if configured)
```

**Commit Message Template**:
```
docs(CLAUDE.md): update plugin inventory to reflect all 6 plugins

Added comprehensive documentation for do-more-now and claude4claude
plugins. Updated plugin count from 4 to 6 and revised component
statistics to match actual implementation.

Changes:
- Documented do-more-now (9 agents, 5 commands)
- Documented claude4claude (2 skills)
- Updated total counts and metrics
- Marked line counts as approximate

Fixes: P0-4
```

---

### P1 (High Priority) - Quality Issues

#### P1-1: Create Missing Plugin READMEs

**Status**: Not Started
**Effort**: Large (2-4 hours per README)
**Dependencies**: None
**Spec Reference**: CLAUDE.md §Development Workflow • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P1-1 (lines 249-264)

##### Description
Four plugins lack README.md files, reducing discoverability and usability. Only agent-loop and promptctl have comprehensive READMEs. Users need quick-start guides, command references, and example workflows for each plugin.

**Missing READMEs**:
1. `plugins/epti/README.md`
2. `plugins/visual-iteration/README.md`
3. `plugins/do-more-now/README.md`
4. `plugins/claude4claude/README.md`

##### Acceptance Criteria
- [ ] Each plugin has README.md with consistent structure
- [ ] Quick start section with installation and first use
- [ ] Command reference (if applicable) with usage examples
- [ ] Workflow examples showing real-world usage
- [ ] Use cases section explaining when to use the plugin
- [ ] Links to related plugins or skills
- [ ] Follows agent-loop README.md structure as template

##### Technical Notes
**Template structure** (from agent-loop/README.md):
1. Overview and purpose
2. Installation
3. Quick start
4. Commands (if applicable) or Skills (if applicable)
5. Workflow examples
6. Use cases
7. Configuration (if applicable)
8. Tips and best practices

**Recommended approach**: Create READMEs in this order:
1. epti (similar to agent-loop, TDD focus)
2. visual-iteration (unique workflow, needs browser setup)
3. do-more-now (complex, 9 agents, auto-mode selection)
4. claude4claude (skills-only, builder focus)

**Commit Message Template** (per plugin):
```
docs(epti): add comprehensive README with quick start and workflows

Created user-facing documentation including:
- Installation and setup
- Command reference with examples
- TDD workflow walkthrough
- Use cases and best practices

Fixes: P1-1 (epti portion)
```

---

#### P1-2: Fix Promptctl Author URL Typo

**Status**: Not Started
**Effort**: Small
**Dependencies**: None
**Spec Reference**: CLAUDE.md §Plugin Structure • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P1-2 (lines 266-271)

##### Description
The promptctl plugin.json author URL contains a backtick character that breaks the URL formatting.

##### Acceptance Criteria
- [ ] Backtick removed from line 8 of promptctl plugin.json
- [ ] URL is valid: `https://github.com/brandon-fryslie`
- [ ] JSON validates successfully

##### Technical Notes
**File to modify**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/promptctl/.claude-plugin/plugin.json`

**Line 8 current**: `https://gith`ub.com/brandon-fryslie`
**Line 8 fixed**: `https://github.com/brandon-fryslie`

**Commit Message Template**:
```
fix(promptctl): correct author URL typo in plugin manifest

Removed stray backtick from GitHub URL that broke link formatting.

Fixes: P1-2
```

---

#### P1-3: Add or Remove Marketplace Owner Email

**Status**: Not Started
**Effort**: Small
**Dependencies**: User decision (add email or remove field)
**Spec Reference**: CLAUDE.md §Licensing and Ownership • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P1-3 (lines 273-280)

##### Description
The marketplace.json owner field has an empty email string. Should either add a contact email or remove the field entirely for consistency.

##### Acceptance Criteria
- [ ] User decision made: add email OR remove field
- [ ] If adding: valid email address provided
- [ ] If removing: email field removed, only name remains
- [ ] JSON validates successfully

##### Technical Notes
**File to modify**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/.claude-plugin/marketplace.json`

**Line 5 current**: `"email": ""`

**Option A - Add email**:
```json
"owner": {
  "name": "Brandon Fryslie",
  "email": "brandon.fryslie.public@gmail.com"
}
```

**Option B - Remove field**:
```json
"owner": {
  "name": "Brandon Fryslie"
}
```

**Commit Message Template (Option A)**:
```
fix(marketplace): add owner contact email

Added contact email to marketplace owner information for user support.

Fixes: P1-3
```

**Commit Message Template (Option B)**:
```
fix(marketplace): remove empty email field from owner

Removed unused email field from marketplace owner metadata.

Fixes: P1-3
```

---

#### P1-4: Standardize Plugin Author Emails

**Status**: Not Started
**Effort**: Small
**Dependencies**: P1-3 decision (consistency with marketplace)
**Spec Reference**: CLAUDE.md §Plugin Structure • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P1-4 (lines 282-294)

##### Description
Multiple plugin.json files have empty author email fields, creating inconsistent attribution. Should match decision from P1-3 (either add emails consistently or remove field).

**Affected files**:
- `plugins/agent-loop/.claude-plugin/plugin.json` line 7
- `plugins/epti/.claude-plugin/plugin.json` line 7
- `plugins/visual-iteration/.claude-plugin/plugin.json` line 7
- `plugins/do-more-now/.claude-plugin/plugin.json` line 7
- `plugins/promptctl/.claude-plugin/plugin.json` line 7

Note: claude4claude already has email populated

##### Acceptance Criteria
- [ ] All plugin.json author fields match marketplace owner format
- [ ] Either all have email OR none have email (consistency)
- [ ] All JSON files validate successfully

##### Technical Notes
**Approach**: Apply same decision from P1-3 to all 5 plugins

**Option A - Add email to all**:
```json
"author": {
  "name": "Brandon Fryslie",
  "email": "brandon.fryslie.public@gmail.com"
}
```

**Option B - Remove email from all** (including claude4claude):
```json
"author": {
  "name": "Brandon Fryslie"
}
```

**Commit Message Template**:
```
fix(plugins): standardize author email across all plugins

Applied consistent author metadata format across all 6 plugins
to match marketplace owner configuration.

Fixes: P1-4
```

---

### P2 (Medium Priority) - Improvements

#### P2-1: Document "do" vs "do-more-now" Naming

**Status**: Not Started
**Effort**: Small
**Dependencies**: None
**Spec Reference**: CLAUDE.md §Repository Structure • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P2-4 (lines 351-363)

##### Description
The plugin name in marketplace is "do" but the source directory is "do-more-now", which can confuse users during installation and troubleshooting.

##### Acceptance Criteria
- [ ] CLAUDE.md documents naming clearly in §Current Plugins
- [ ] do-more-now README (when created) explains naming in installation section
- [ ] Marketplace.json includes note in plugin description (optional)

##### Technical Notes
**Add to CLAUDE.md** in do-more-now section:
```markdown
**Installation Name**: "do" (directory: do-more-now)
**Command Prefix**: All commands use `/do:` prefix
```

**Add to do-more-now README** in installation section:
```markdown
## Installation

Install the plugin using the short name "do":
```
/plugin marketplace add <marketplace-path>
/plugin install do
```

Note: The plugin is installed as "do" but stored in the `do-more-now` directory.
```

**Commit Message Template**:
```
docs: clarify "do" plugin naming convention

Documented that plugin installs as "do" but resides in "do-more-now"
directory to prevent user confusion.

Fixes: P2-1
```

---

#### P2-2: Remove or Populate Empty .mcp.json Files

**Status**: Not Started
**Effort**: Small
**Dependencies**: None
**Spec Reference**: CLAUDE.md §MCP Configurations • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P2-2 (lines 329-341)

##### Description
agent-loop and epti plugins have empty .mcp.json files (`{}`), suggesting they don't actually need MCP server integration. These files should be removed unless future integration is planned.

**Affected files**:
- `plugins/agent-loop/.mcp.json` - empty `{}`
- `plugins/epti/.mcp.json` - empty `{}`

##### Acceptance Criteria
- [ ] Decision made: remove files OR keep for future use
- [ ] If removing: .mcp.json files deleted from both plugins
- [ ] If removing: plugin.json mcpServers references removed (if present)
- [ ] Plugins load successfully without errors

##### Technical Notes
**Recommendation**: Remove empty files (plugins don't use MCP)

**Files to delete**:
```bash
rm "/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/agent-loop/.mcp.json"
rm "/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/epti/.mcp.json"
```

**Verify plugin.json**: Check if mcpServers field exists and remove if present

**Commit Message Template**:
```
chore: remove empty MCP configuration files

Removed unused .mcp.json files from agent-loop and epti plugins.
These plugins do not require MCP server integration.

Fixes: P2-2
```

---

#### P2-3: Update Line Count Metrics or Mark Approximate

**Status**: Not Started
**Effort**: Small
**Dependencies**: P0-4 (CLAUDE.md update)
**Spec Reference**: CLAUDE.md §Implementation Metrics • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P2-5 (lines 365-372)

##### Description
CLAUDE.md contains specific line counts (e.g., "206 lines", "342 lines") that become outdated with code changes. These should either be verified/updated or qualified as "approximate" to prevent misleading metrics.

**Affected locations**:
- Lines 100, 130, 163 (plugin implementation details)
- Lines 259-264 (implementation metrics)

##### Acceptance Criteria
- [ ] All line counts marked as "approximate" OR verified accurate
- [ ] Metrics include date of last verification
- [ ] Future updates can easily identify which metrics need refreshing

##### Technical Notes
**Option A - Add "approximate" qualifier**:
```markdown
- **Agent**: workflow-agent.md (~206 lines)
- **Commands**: 4 slash commands (~342 lines total)
```

**Option B - Add metadata**:
```markdown
## Implementation Metrics
*(Metrics approximate as of 2025-12-07)*

- **Total Plugin Implementation Lines**: ~30,000+ lines
```

**Option C - Remove specific counts**:
```markdown
- **Agent**: workflow-agent.md - Comprehensive 4-stage workflow
- **Commands**: 4 slash commands - Explore, Plan, Code, Commit
```

**Recommendation**: Option A (add ~ prefix) - preserves metrics while indicating approximation

**Commit Message Template**:
```
docs(CLAUDE.md): mark line counts as approximate

Added ~ prefix to line count metrics to indicate approximation
and prevent outdated documentation issues.

Fixes: P2-3
```

---

#### P2-4: Remove .DS_Store from Git History

**Status**: Not Started
**Effort**: Small
**Dependencies**: None
**Spec Reference**: CLAUDE.md §Repository Structure • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P2-6 (lines 374-387)

##### Description
.DS_Store files exist in git history despite being in .gitignore, polluting repository with macOS metadata.

**Affected files**:
- `.DS_Store` (root)
- `plugins/dev-loop/.DS_Store` (will be removed with P0-3)

##### Acceptance Criteria
- [ ] .DS_Store files removed from git index
- [ ] Files remain in .gitignore
- [ ] Git history cleaned (optional - requires force push)

##### Technical Notes
**Commands**:
```bash
cd "/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace"
git rm --cached .DS_Store 2>/dev/null || true
git rm --cached plugins/dev-loop/.DS_Store 2>/dev/null || true
```

**Note**: plugins/dev-loop/.DS_Store will be removed automatically when P0-3 deletes the directory

**Commit Message Template**:
```
chore: remove .DS_Store files from git index

Removed macOS metadata files from version control. Files remain
in .gitignore to prevent future commits.

Fixes: P2-4
```

---

#### P2-5: Fix Hardcoded Paths in Test Files

**Status**: Not Started
**Effort**: Medium
**Dependencies**: None
**Spec Reference**: tests/e2e/design/ARCHITECTURE.md • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P2-8 (lines 398-405)

##### Description
Test architecture file contains hardcoded absolute paths referencing specific user directory, making tests non-portable to other systems.

**Affected file**: `tests/e2e/design/ARCHITECTURE.md`
**Lines**: 244, 430, 495

##### Acceptance Criteria
- [ ] Hardcoded paths replaced with relative paths or environment variables
- [ ] Test documentation portable to other systems
- [ ] Examples use `${REPO_ROOT}` or similar variable

##### Technical Notes
**Current**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/...`

**Recommended replacement**:
```markdown
${REPO_ROOT}/plugins/...
# or
./plugins/...
# or
$(pwd)/plugins/...
```

**Commit Message Template**:
```
fix(tests): replace hardcoded paths with relative paths

Converted absolute user-specific paths to relative paths for
portability across development environments.

Fixes: P2-5
```

---

### P3 (Low Priority) - Polish

#### P3-1: Archive Old Status Files

**Status**: Not Started
**Effort**: Small
**Dependencies**: None
**Spec Reference**: .agent_planning/ structure • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P3-1 (lines 409-414)

##### Description
Old status file `.agent_planning/STATUS-2025-12-03-000000.md` contains 38 references to full iCloud paths from dev-loop rename operation. Should be archived to prevent confusion.

##### Acceptance Criteria
- [ ] `.agent_planning/archive/` directory created
- [ ] Old status file moved to archive with `.archived` suffix
- [ ] Only current/recent status files remain in .agent_planning root

##### Technical Notes
**Commands**:
```bash
mkdir -p "/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/.agent_planning/archive"
mv "/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/.agent_planning/STATUS-2025-12-03-000000.md" \
   "/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/.agent_planning/archive/STATUS-2025-12-03-000000.md.archived"
```

**Commit Message Template**:
```
chore(agent_planning): archive old dev-loop rename status file

Moved outdated status file to archive directory to reduce clutter
and prevent confusion with current planning documents.

Fixes: P3-1
```

---

#### P3-2: Add LICENSE Files to Plugin Directories

**Status**: Not Started
**Effort**: Small
**Dependencies**: None
**Spec Reference**: CLAUDE.md §Licensing and Ownership • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P3-4 (lines 431-436)

##### Description
All plugins declare MIT license in plugin.json but don't include LICENSE file in plugin directory. License text should be distributed with each plugin for legal clarity.

**Affected plugins**: All 6 plugins

##### Acceptance Criteria
- [ ] Each plugin directory contains LICENSE or LICENSE.txt file
- [ ] MIT license text is complete and accurate
- [ ] Copyright year and owner name correct

##### Technical Notes
**Create LICENSE file** in each plugin directory:
```
MIT License

Copyright (c) 2025 Brandon Fryslie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Files to create**:
- `plugins/agent-loop/LICENSE`
- `plugins/epti/LICENSE`
- `plugins/visual-iteration/LICENSE`
- `plugins/promptctl/LICENSE`
- `plugins/do-more-now/LICENSE`
- `plugins/claude4claude/LICENSE`

**Commit Message Template**:
```
chore(plugins): add MIT license files to all plugins

Included MIT license text in each plugin directory for proper
license distribution and legal compliance.

Fixes: P3-2
```

---

#### P3-3: Standardize Plugin Keywords

**Status**: Not Started
**Effort**: Small
**Dependencies**: None
**Spec Reference**: CLAUDE.md §Plugin Structure • **Status Reference**: STATUS-symlink-removal-production-readiness-2025-12-07.md §P3-3 (lines 424-429)

##### Description
Plugin keywords vary in quality and quantity across plugins, affecting search and discoverability in marketplace.

##### Acceptance Criteria
- [ ] All plugins have relevant, consistent keywords
- [ ] Keywords cover: workflow type, use case, technology focus
- [ ] Minimum 4-6 keywords per plugin
- [ ] No duplicate or redundant keywords

##### Technical Notes
**Recommended keyword categories**:
1. Workflow type (e.g., "tdd", "iteration", "automation")
2. Development phase (e.g., "planning", "testing", "implementation")
3. Technology (e.g., "visual", "browser", "git")
4. Purpose (e.g., "development", "workflow", "productivity")

**Example standardization**:
```json
"keywords": ["tdd", "testing", "development", "workflow", "implementation", "verification"]
```

**Commit Message Template**:
```
docs(plugins): standardize keywords for better discoverability

Reviewed and enhanced plugin keywords across all 6 plugins to
improve marketplace search and categorization.

Fixes: P3-3
```

---

## Dependency Graph

```
P0-1 (claude4claude fix) ──┐
P0-2 (do-more-now MCP)    ─┤
P0-3 (delete dev-loop)    ─┤──> P0-4 (CLAUDE.md update) ──> P2-3 (line counts)
                            │
                            └──> P1-1 (READMEs) ──> P2-1 (naming docs)

P1-3 (marketplace email) ──> P1-4 (plugin emails)

P1-2 (promptctl typo) ──> (independent)

P2-2 (empty MCP files) ──> (independent)
P2-4 (.DS_Store) ──> (independent)
P2-5 (test paths) ──> (independent)

P3-1 (archive status) ──> (independent)
P3-2 (LICENSE files) ──> (independent)
P3-3 (keywords) ──> (independent)
```

**Critical Path**: P0-1 → P0-2 → P0-3 → P0-4 → P1-1

---

## Recommended Sprint Planning

### Sprint 1: Production Blockers (Complexity: Medium)
**Goal**: Fix all P0 issues to enable production release

**Tasks**:
1. P0-1: Fix claude4claude plugin.json (15 min)
2. P0-2: Resolve do-more-now MCP config (15 min + decision time)
3. P0-3: Delete dev-loop directory (5 min)
4. P0-4: Update CLAUDE.md plugin inventory (45 min)

**Total Effort**: Small-Medium (~90 min)
**Outcome**: Repository production-ready

**Commit sequence**:
```bash
# 1. Fix broken plugin
git add plugins/claude4claude/.claude-plugin/plugin.json
git commit -m "fix(claude4claude): remove non-existent commands from plugin manifest"

# 2. Clean up dev-loop
# (manual delete - no commit needed unless .DS_Store is tracked)

# 3. Resolve MCP config
git add plugins/do-more-now/.mcp.json  # OR plugins/do-more-now/.claude-plugin/plugin.json
git commit -m "fix(do-more-now): [add/remove] .mcp.json configuration"

# 4. Update documentation
git add CLAUDE.md
git commit -m "docs(CLAUDE.md): update plugin inventory to reflect all 6 plugins"
```

---

### Sprint 2: Quality Fixes (Complexity: Medium)
**Goal**: Address P1 high-priority issues

**Tasks**:
1. P1-2: Fix promptctl URL typo (5 min)
2. P1-3: Marketplace email decision (10 min)
3. P1-4: Standardize plugin emails (10 min)
4. P1-1: Create README for epti (60 min)
5. P1-1: Create README for visual-iteration (90 min)
6. P1-1: Create README for do-more-now (90 min)
7. P1-1: Create README for claude4claude (60 min)

**Total Effort**: Medium-Large (~5 hours)
**Outcome**: Professional user experience

**Commit sequence**:
```bash
# 1. Quick fixes
git add plugins/promptctl/.claude-plugin/plugin.json
git commit -m "fix(promptctl): correct author URL typo in plugin manifest"

# 2. Email standardization
git add .claude-plugin/marketplace.json plugins/*/. claude-plugin/plugin.json
git commit -m "fix: standardize author/owner email across all plugins and marketplace"

# 3. READMEs (one commit per plugin)
git add plugins/epti/README.md
git commit -m "docs(epti): add comprehensive README with quick start and workflows"

git add plugins/visual-iteration/README.md
git commit -m "docs(visual-iteration): add comprehensive README with browser setup guide"

git add plugins/do-more-now/README.md
git commit -m "docs(do-more-now): add comprehensive README with workflow modes"

git add plugins/claude4claude/README.md
git commit -m "docs(claude4claude): add comprehensive README for builder skills"
```

---

### Sprint 3: Cleanup & Polish (Complexity: Small)
**Goal**: Address P2 and P3 issues for repository cleanliness

**Tasks**:
1. P2-1: Document "do" naming (10 min)
2. P2-2: Remove empty MCP files (10 min)
3. P2-3: Update line counts (15 min)
4. P2-4: Remove .DS_Store (5 min)
5. P2-5: Fix test paths (20 min)
6. P3-1: Archive old status (5 min)
7. P3-2: Add LICENSE files (20 min)
8. P3-3: Standardize keywords (30 min)

**Total Effort**: Small (~2 hours)
**Outcome**: Clean, polished repository

**Commit sequence**:
```bash
# 1. Documentation polish
git add CLAUDE.md plugins/do-more-now/README.md
git commit -m "docs: clarify 'do' plugin naming convention"

git add CLAUDE.md
git commit -m "docs(CLAUDE.md): mark line counts as approximate"

# 2. Cleanup
git rm --cached .DS_Store
git commit -m "chore: remove .DS_Store files from git index"

rm -rf plugins/agent-loop/.mcp.json plugins/epti/.mcp.json
git commit -m "chore: remove empty MCP configuration files"

# 3. Test portability
git add tests/e2e/design/ARCHITECTURE.md
git commit -m "fix(tests): replace hardcoded paths with relative paths"

# 4. Licensing
git add plugins/*/LICENSE
git commit -m "chore(plugins): add MIT license files to all plugins"

# 5. Metadata
git add plugins/*/.claude-plugin/plugin.json
git commit -m "docs(plugins): standardize keywords for better discoverability"

# 6. Archive
mkdir -p .agent_planning/archive
mv .agent_planning/STATUS-2025-12-03-000000.md .agent_planning/archive/
git commit -m "chore(agent_planning): archive old dev-loop rename status file"
```

---

## Risk Assessment

### Production Release Readiness

**Current Risk**: MEDIUM-HIGH (P0 blockers prevent release)
**Post-Sprint-1 Risk**: LOW (production-ready)
**Post-Sprint-2 Risk**: VERY LOW (professional quality)

**Blocking Issues**: 4 P0 items (all fixable in ~90 minutes)
**Critical Path**: P0 fixes must be completed before release
**Non-Blocking**: All P1-P3 items can be addressed post-release

### High-Risk Items

1. **claude4claude broken plugin** (P0-1): CRITICAL - plugin will not load
2. **do-more-now MCP decision** (P0-2): Requires user input on chrome-devtools needs
3. **CLAUDE.md accuracy** (P0-4): Misleading documentation impacts user trust

### Low-Risk Items

- P1-4: Email standardization (cosmetic)
- P2-2: Empty MCP files (cleanup)
- P3-*: All polish items (zero functional impact)

---

## Gaps and Missing Considerations

### Identified During Planning

1. **No testing validation**: Status report notes 0 manual tests executed. Production readiness assumes plugins work but haven't been validated in Claude Code environment.

2. **MCP server compatibility**: chrome-devtools MCP server for do-more-now not verified to work with work-evaluator agent's browser testing features.

3. **Plugin loading order**: No documentation of whether plugins have interdependencies or recommended loading order.

4. **Version management**: All plugins are v0.1.0 with no versioning strategy documented for future updates.

5. **Migration path**: No upgrade guide for users who might have installed plugins before these fixes.

6. **Performance benchmarks**: No metrics on plugin load time, agent execution time, or resource usage.

7. **Cross-plugin compatibility**: No documentation of which plugins work well together or conflict.

8. **Error handling**: No documented error recovery strategies if plugin loading fails.

### Recommendations for Future Sprints

1. **Create manual test suite** (Sprint 4):
   - Load each plugin in Claude Code
   - Execute representative commands
   - Verify hooks trigger correctly
   - Test MCP integrations

2. **Version management strategy** (Sprint 5):
   - Document semver approach
   - Create CHANGELOG.md per plugin
   - Define breaking change policy

3. **Plugin compatibility matrix** (Sprint 5):
   - Document which plugins complement each other
   - Identify conflicts or redundancies
   - Create recommended plugin bundles

4. **Performance profiling** (Sprint 6):
   - Measure plugin load times
   - Profile agent execution
   - Optimize MCP server connections

5. **User migration guide** (Post-release):
   - Document upgrade process
   - Provide rollback instructions
   - Create troubleshooting guide

---

## Symlink Decision

**User Request**: Keep symlink (evaluator recommendation)
**Changes Required**: NONE
**Risk**: ZERO

The symlink at `~/icode` provides user convenience with no production code dependencies. All references are in documentation only (8 files, 14 occurrences). Keeping the symlink requires no changes to the repository.

---

## Next Steps

### Immediate (This Session)
1. Execute Sprint 1 (P0 fixes)
2. Commit each fix separately with detailed messages
3. Verify plugins load without errors

### Short-Term (Next Session)
1. Make P1-3 and P1-4 email decisions
2. Execute Sprint 2 (README creation)
3. Begin manual testing

### Medium-Term (Next Week)
1. Execute Sprint 3 (cleanup)
2. Complete manual testing
3. Document test results

### Long-Term (Next Month)
1. Address identified gaps
2. Create versioning strategy
3. Build plugin compatibility matrix

---

## Summary Statistics

**Total Issues**: 21 (4 P0, 5 P1, 6 P2, 4 P3)
**Total Estimated Effort**: Medium (~8-10 hours across all sprints)
**Critical Path Items**: 4 (P0-1 through P0-4)
**User Decisions Required**: 2 (P0-2 MCP, P1-3 email)
**Documentation Updates**: 5 files (CLAUDE.md, 4 READMEs)
**Code Fixes**: 3 plugin.json files
**Deletions**: 1 directory, 2-3 files

**Production Readiness**: 95% after Sprint 1 completion
**Professional Quality**: 100% after Sprint 2 completion
**Repository Polish**: 100% after Sprint 3 completion
