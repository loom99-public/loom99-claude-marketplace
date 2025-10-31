# Next Steps - Claude Marketplace Fixes

**Date**: 2025-10-29
**Status**: Critical fixes required before marketplace is functional
**Priority**: HIGH - Skills will not load without these changes

---

## Executive Summary

The loom99 Claude marketplace **passes validation** but has **critical structural issues** that prevent plugins from functioning. All 13 skills across 3 plugins use incorrect file structure (flat markdown files instead of subdirectories with SKILL.md). This is a **blocking issue** that must be fixed before any plugin can be used.

**Estimated Time to Fix**: 30-45 minutes
**Complexity**: Low (mechanical file restructuring)
**Risk**: Low (no code changes, only file organization)

---

## Critical Issues (MUST FIX)

### Issue #1: Skills Directory Structure (BLOCKING)

**Current State**: ❌ BROKEN
```
plugins/agent-loop/skills/
├── code-exploration.md          ❌ Flat file (incorrect)
├── git-operations.md            ❌ Flat file (incorrect)
├── plan-generation.md           ❌ Flat file (incorrect)
└── verification.md              ❌ Flat file (incorrect)
```

**Required State**: ✅ CORRECT
```
plugins/agent-loop/skills/
├── code-exploration/
│   └── SKILL.md                 ✅ Subdirectory with SKILL.md
├── git-operations/
│   └── SKILL.md                 ✅ Subdirectory with SKILL.md
├── plan-generation/
│   └── SKILL.md                 ✅ Subdirectory with SKILL.md
└── verification/
    └── SKILL.md                 ✅ Subdirectory with SKILL.md
```

**Reference**: [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)

**Impact**: Skills will not be recognized or loaded by Claude Code. This affects **100% of plugin functionality** since all three plugins rely heavily on skills.

**Affected Files**: 13 total skills
- agent-loop: 4 skills
- epti: 5 skills
- visual-iteration: 4 skills

---

### Issue #2: Missing YAML Frontmatter in Skills (BLOCKING)

**Current State**: Skills have markdown headers but no YAML frontmatter

**Required Format**:
```yaml
---
name: skill-identifier
description: What the skill does and when Claude should use it (max 1024 chars)
---

# Skill Title

[Rest of skill content...]
```

**Example**:
```yaml
---
name: code-exploration
description: Systematic codebase investigation to understand architecture, patterns, dependencies, and context before making changes. Use when starting work on unfamiliar code, identifying integration points, or researching existing patterns.
---

# Code Exploration Skill

[Current content follows...]
```

**Impact**: Even after fixing directory structure, skills won't register without proper frontmatter.

---

## Detailed Fix Plan

### Step 1: Restructure agent-loop Skills

**Skills to fix** (4 total):
1. `code-exploration.md` → `code-exploration/SKILL.md`
2. `git-operations.md` → `git-operations/SKILL.md`
3. `plan-generation.md` → `plan-generation/SKILL.md`
4. `verification.md` → `verification/SKILL.md`

**Commands**:
```bash
cd plugins/agent-loop/skills

# code-exploration
mkdir code-exploration
mv code-exploration.md code-exploration/SKILL.md

# git-operations
mkdir git-operations
mv git-operations.md git-operations/SKILL.md

# plan-generation
mkdir plan-generation
mv plan-generation.md plan-generation/SKILL.md

# verification
mkdir verification
mv verification.md verification/SKILL.md
```

**Add frontmatter to each SKILL.md**:

`code-exploration/SKILL.md`:
```yaml
---
name: code-exploration
description: Systematic codebase investigation to understand architecture, patterns, dependencies, and integration points. Use when starting work on unfamiliar code, understanding change impact, or researching existing patterns to follow.
---
```

`git-operations/SKILL.md`:
```yaml
---
name: git-operations
description: Git workflow automation including commits, branches, and repository management. Use when finalizing changes, creating feature branches, or managing git history following conventional commit standards.
---
```

`plan-generation/SKILL.md`:
```yaml
---
name: plan-generation
description: Structured implementation planning with task breakdown, dependency tracking, and success criteria. Use when starting complex features, coordinating multi-step work, or defining clear acceptance criteria.
---
```

`verification/SKILL.md`:
```yaml
---
name: verification
description: Code and test verification including running test suites, checking builds, and validating implementations. Use after code changes to ensure correctness, catch regressions, and verify acceptance criteria.
---
```

---

### Step 2: Restructure epti Skills

**Skills to fix** (5 total):
1. `implementation-with-protection.md` → `implementation-with-protection/SKILL.md`
2. `overfitting-detection.md` → `overfitting-detection/SKILL.md`
3. `refactoring.md` → `refactoring/SKILL.md`
4. `test-execution.md` → `test-execution/SKILL.md`
5. `test-generation.md` → `test-generation/SKILL.md`

**Commands**:
```bash
cd plugins/epti/skills

mkdir implementation-with-protection
mv implementation-with-protection.md implementation-with-protection/SKILL.md

mkdir overfitting-detection
mv overfitting-detection.md overfitting-detection/SKILL.md

mkdir refactoring
mv refactoring.md refactoring/SKILL.md

mkdir test-execution
mv test-execution.md test-execution/SKILL.md

mkdir test-generation
mv test-generation.md test-generation/SKILL.md
```

**Add frontmatter to each SKILL.md**:

`implementation-with-protection/SKILL.md`:
```yaml
---
name: implementation-with-protection
description: Safe code implementation following TDD principles with safeguards against overfitting. Use when implementing code to pass existing tests while maintaining clean, general-purpose solutions.
---
```

`overfitting-detection/SKILL.md`:
```yaml
---
name: overfitting-detection
description: Identify test-specific hacks and implementation shortcuts that compromise code quality. Use during code review or when implementation seems too tightly coupled to specific test cases.
---
```

`refactoring/SKILL.md`:
```yaml
---
name: refactoring
description: Post-implementation code refinement to improve structure, readability, and maintainability while preserving behavior. Use after tests pass to clean up implementation and reduce technical debt.
---
```

`test-execution/SKILL.md`:
```yaml
---
name: test-execution
description: Test running and result analysis across multiple frameworks (pytest, jest, go test, JUnit, RSpec). Use to verify test failures, validate implementations, and interpret test output.
---
```

`test-generation/SKILL.md`:
```yaml
---
name: test-generation
description: Comprehensive test writing from requirements without implementation code. Use at start of TDD cycle to define expected behavior, edge cases, and acceptance criteria through tests.
---
```

---

### Step 3: Restructure visual-iteration Skills

**Skills to fix** (4 total):
1. `design-implementation.md` → `design-implementation/SKILL.md`
2. `screenshot-capture.md` → `screenshot-capture/SKILL.md`
3. `visual-comparison.md` → `visual-comparison/SKILL.md`
4. `visual-refinement.md` → `visual-refinement/SKILL.md`

**Commands**:
```bash
cd plugins/visual-iteration/skills

mkdir design-implementation
mv design-implementation.md design-implementation/SKILL.md

mkdir screenshot-capture
mv screenshot-capture.md screenshot-capture/SKILL.md

mkdir visual-comparison
mv visual-comparison.md visual-comparison/SKILL.md

mkdir visual-refinement
mv visual-refinement.md visual-refinement/SKILL.md
```

**Add frontmatter to each SKILL.md**:

`design-implementation/SKILL.md`:
```yaml
---
name: design-implementation
description: Pixel-perfect UI implementation from design mockups or specifications. Use when building new UI components, implementing design systems, or translating visual designs into code.
---
```

`screenshot-capture/SKILL.md`:
```yaml
---
name: screenshot-capture
description: Automated and manual screenshot capture of UI implementations using MCP browser tools or manual workflows. Use to document current state, create visual baselines, or capture specific viewport sizes.
---
```

`visual-comparison/SKILL.md`:
```yaml
---
name: visual-comparison
description: Side-by-side visual comparison analysis identifying specific differences and generating actionable feedback. Use when comparing implementations to designs, before/after states, or cross-browser rendering.
---
```

`visual-refinement/SKILL.md`:
```yaml
---
name: visual-refinement
description: Iterative visual improvement through specific CSS and DOM refinements based on screenshot feedback. Use to achieve pixel-perfect results, fix visual bugs, or polish UI implementations.
---
```

---

### Step 4: Update plugin.json References (If Needed)

**Current configuration** in each plugin.json:
```json
"skills": "./skills/"
```

This should **automatically work** with the new directory structure since it points to the parent directory. The Claude Code runtime will discover subdirectories and look for SKILL.md files.

**Verification**: After restructuring, confirm the path is still `"skills": "./skills/"` in:
- `plugins/agent-loop/.claude-plugin/plugin.json`
- `plugins/epti/.claude-plugin/plugin.json`
- `plugins/visual-iteration/.claude-plugin/plugin.json`

---

### Step 5: Validate Changes

After restructuring, run validation:

```bash
cd /Users/bmf/Library/Mobile\ Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace
claude plugin validate .
```

**Expected output**:
```
✔ Validation passed
```

---

## Secondary Issues (Should Fix)

### Issue #3: visual-iteration Empty Hooks Array

**File**: `plugins/visual-iteration/hooks/hooks.json`

**Current State**: `[]` (empty array)

**Documentation Claims**: CLAUDE.md states "3 hooks configured" but file is empty

**Resolution Options**:

1. **If intentional**: Update CLAUDE.md to reflect reality
2. **If unintentional**: Add hooks based on workflow needs

**Suggested hooks** (if adding):
```json
[
  {
    "event": "post-code",
    "command": "echo '\n💡 Tip: Capture a screenshot with /screenshot to verify visual changes'",
    "description": "Suggest screenshot verification after code changes"
  },
  {
    "event": "pre-commit",
    "command": "echo '\n📸 Visual Commit Checklist:\n  1. Screenshot captured?\n  2. Visual feedback addressed?\n  3. Polish complete?\n\nUse /visual-commit for guided workflow.'",
    "description": "Remind about visual validation before commits"
  },
  {
    "event": "post-refine",
    "command": "echo '\n✓ Refinement complete. Next steps:\n  1. Capture new screenshot\n  2. Compare with previous version\n  3. Iterate if needed or commit'",
    "description": "Guide next steps after visual refinement"
  }
]
```

---

### Issue #4: Git Repository Not Initialized

**Current State**: Not a git repository

**Why This Matters**:
- Version control for development
- Required for GitHub distribution
- Enables team collaboration
- Marketplace best practice

**Commands**:
```bash
cd /Users/bmf/Library/Mobile\ Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace

git init
git add .
git commit -m "feat(marketplace): initial commit of loom99 marketplace

- Add agent-loop plugin with 4-stage workflow
- Add epti plugin with TDD workflow
- Add visual-iteration plugin with screenshot-driven development
- Include 24,459 lines of implementation across 3 plugins"
```

**Future**: Consider publishing to GitHub for distribution

---

### Issue #5: Add Repository Metadata (Optional)

**Enhancement**: Add `homepage` and `repository` fields to plugin manifests

**Benefits**:
- Better discoverability
- Link to documentation
- Enable GitHub integration
- Professional presentation

**Update each plugin.json** (`agent-loop`, `epti`, `visual-iteration`):
```json
{
  "name": "agent-loop",
  "version": "0.1.0",
  "description": "Agentic Software Engineering Loop - Explore, plan, code, commit workflow",
  "homepage": "https://github.com/brandonfryslie/loom99-claude-marketplace",
  "repository": {
    "type": "git",
    "url": "https://github.com/brandonfryslie/loom99-claude-marketplace"
  },
  "author": {
    "name": "Brandon Fryslie",
    "email": ""
  },
  "license": "MIT",
  "keywords": ["agent", "workflow", "engineering", "explore", "plan", "code", "commit"],
  "commands": "./commands/",
  "agents": "./agents/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Replace GitHub URLs** with actual repository location when available.

---

## Validation Checklist

After completing all fixes:

- [ ] All 13 skills restructured into subdirectories
- [ ] All 13 SKILL.md files have YAML frontmatter
- [ ] `claude plugin validate .` passes
- [ ] visual-iteration hooks resolved (added or docs updated)
- [ ] Git repository initialized
- [ ] Repository metadata added to plugin.json files
- [ ] CLAUDE.md updated to reflect actual state
- [ ] Manual testing in Claude Code environment

---

## Testing Plan

### Phase 1: Structure Validation
1. Run `claude plugin validate .`
2. Verify all skills have proper structure
3. Check YAML frontmatter syntax

### Phase 2: Plugin Loading
1. Add marketplace to Claude Code: `/plugin marketplace add .`
2. Install each plugin individually
3. Verify commands appear in autocomplete
4. Confirm agents load without errors
5. Test hooks trigger properly
6. Verify skills are discoverable

### Phase 3: Functional Testing

**agent-loop**:
- [ ] `/explore` command loads and provides guidance
- [ ] `/plan` command creates structured plans
- [ ] `/code` command enforces verification
- [ ] `/commit` command follows git workflow
- [ ] Skills invocable during workflow

**epti**:
- [ ] `/write-tests` generates tests first
- [ ] `/verify-fail` confirms proper TDD cycle
- [ ] `/commit-tests` allows test-only commits
- [ ] `/implement` enforces test-first discipline
- [ ] `/iterate` supports refinement
- [ ] `/commit-code` requires passing tests

**visual-iteration**:
- [ ] `/screenshot` captures UI state
- [ ] `/feedback` provides specific visual analysis
- [ ] `/refine` implements improvements
- [ ] `/iterate-loop` runs full cycle
- [ ] `/visual-commit` finalizes polished work
- [ ] `/compare` shows before/after differences

### Phase 4: Integration Testing
- [ ] Plugins work independently
- [ ] No conflicts between plugins
- [ ] MCP servers load correctly (browser-tools)
- [ ] Hooks don't conflict with each other

---

## Risk Assessment

### Low Risk
- ✅ Structural changes (directories, file moves)
- ✅ Adding YAML frontmatter (non-breaking)
- ✅ Git initialization (local only)

### Medium Risk
- ⚠️ Hook modifications (test in isolated environment first)
- ⚠️ Plugin.json changes (validate thoroughly)

### High Risk
- ❌ Content changes to skills (not recommended without testing)

---

## Success Criteria

### Minimum Viable Fix
- All skills in correct directory structure
- All skills have valid YAML frontmatter
- Marketplace passes validation
- Plugins load in Claude Code without errors

### Complete Fix
- All minimum criteria met
- Visual-iteration hooks resolved
- Git repository initialized
- Repository metadata added
- Documentation accurate
- All plugins manually tested

### Production Ready
- All complete criteria met
- Integration testing passed
- Real-world usage validated
- Performance verified
- Documentation complete

---

## Timeline Estimate

| Task | Time | Complexity |
|------|------|------------|
| Restructure skills (13 files) | 15 min | Low |
| Add YAML frontmatter (13 files) | 15 min | Low |
| Validate changes | 5 min | Low |
| Fix visual-iteration hooks | 10 min | Low |
| Initialize git + commit | 5 min | Low |
| Add repository metadata | 10 min | Low |
| Manual testing (all plugins) | 60 min | Medium |
| **Total** | **120 min** | **Low-Medium** |

**Critical Path**: Skills restructure (30 min) → Validation (5 min) → Testing (60 min)

---

## Automation Script (Optional)

Create `scripts/fix-skills-structure.sh`:

```bash
#!/bin/bash

# Script to restructure all skills into proper directory format
# WARNING: Test in isolated environment first!

set -e

PLUGINS=("agent-loop" "epti" "visual-iteration")

for plugin in "${PLUGINS[@]}"; do
  echo "Processing plugin: $plugin"
  cd "plugins/$plugin/skills"

  # Find all .md files (except SKILL.md)
  for file in *.md; do
    if [ -f "$file" ]; then
      # Extract filename without extension
      name="${file%.md}"

      echo "  Restructuring: $name"

      # Create subdirectory
      mkdir -p "$name"

      # Move file to SKILL.md
      mv "$file" "$name/SKILL.md"

      echo "  ✓ Created $name/SKILL.md"
    fi
  done

  cd ../../..
done

echo ""
echo "✓ All skills restructured!"
echo ""
echo "Next steps:"
echo "1. Add YAML frontmatter to each SKILL.md"
echo "2. Run: claude plugin validate ."
echo "3. Test in Claude Code environment"
```

**Usage**:
```bash
chmod +x scripts/fix-skills-structure.sh
./scripts/fix-skills-structure.sh
```

**Note**: Frontmatter must still be added manually (skill-specific descriptions).

---

## References

### Documentation
- [Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [Skills Structure](https://docs.claude.com/en/docs/claude-code/skills)
- [Plugin Structure](https://docs.claude.com/en/docs/claude-code/plugins)
- [Slash Commands](https://docs.claude.com/en/docs/claude-code/slash-commands)

### Files to Update
- All 13 skill files (restructure + frontmatter)
- `plugins/visual-iteration/hooks/hooks.json` (if adding hooks)
- All 3 `plugin.json` files (if adding repository metadata)
- `CLAUDE.md` (update accuracy)

### Validation Commands
```bash
# Validate marketplace
claude plugin validate .

# Add marketplace locally for testing
/plugin marketplace add .

# List installed marketplaces
/plugin marketplace list

# Install specific plugin
/plugin install agent-loop
```

---

## Questions to Resolve

1. **visual-iteration hooks**: Should we add hooks or update docs to reflect empty state?
2. **GitHub repository**: Plan to publish marketplace publicly or keep private?
3. **Testing priority**: Which plugin should be tested first?
4. **Frontmatter descriptions**: Should descriptions match current markdown headers or be rewritten?
5. **Additional files**: Should skills include supporting files (examples, templates, etc.)?

---

## Conclusion

The marketplace has **excellent foundations** but cannot function until skills are restructured. This is a **mechanical fix** with low risk and clear steps. After restructuring, the marketplace will be fully functional and ready for comprehensive testing.

**Recommended Approach**:
1. Fix skills structure (Priority 1)
2. Validate changes
3. Resolve visual-iteration hooks (Priority 2)
4. Manual testing phase
5. Git + metadata (Priority 3)

**Estimated Time to Functional State**: 35 minutes (restructure + validate)
**Estimated Time to Production Ready**: 2 hours (including manual testing)

---

**Last Updated**: 2025-10-29
**Next Review**: After skills restructure completed
