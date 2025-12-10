# Status Report - 2025-12-10 02:23:57

## Executive Summary
Overall: 85% compliant | Critical issues: 3 large skills, 3 broken references | Progressive disclosure: partially implemented

**Profile**: agent-prompt (evaluating skill/agent definitions)

## Evaluation Context

This evaluation assesses the do-more-now plugin's skills for compliance with Claude Code's progressive disclosure pattern. The goal is to keep skill.md files under ~100 lines while moving detailed reference content into separate Level 3 files.

**Current State**:
- 16 skills total
- 3 skills exceed recommended size: gating-controller (214 lines), route-subcommands (162 lines), setup-testing (146 lines)
- 1 skill with proper progressive disclosure: evaluation-profiles (168 lines + 6 reference files)
- 3 broken command references in researcher.md agent

## File Structure Assessment

### Skills With Progressive Disclosure ✅

**evaluation-profiles** (168 lines + 6 references):
- Main skill.md: Overview, profile selection, integration guidance
- Reference files (66-129 lines each):
  - agent-prompt.md (103 lines)
  - api-service.md (121 lines)
  - cli-tool.md (66 lines)
  - config-infra.md (129 lines)
  - library.md (100 lines)
  - web-app.md (77 lines)

**Structure**: ✅ Excellent example of progressive disclosure
**Pattern**: Main file explains "what/when/why", references provide "how" details

### Skills Needing Progressive Disclosure ❌

#### 1. gating-controller (214 lines)

**Current structure**: Single monolithic file with:
- Process overview (lines 1-84)
- AskUserQuestion format template (lines 86-122)
- Error handling reference (lines 123-129)
- Example flows (lines 131-167)
- File format specifications (lines 169-214)

**Recommended split**:

**Keep in skill.md** (~80 lines):
- Core concept (what gating does)
- When to use this skill
- High-level process (5 steps)
- Integration points
- Error handling strategy (summary)
- Pointer to references

**Move to references/**:
1. `gate-modes.md` (~40 lines):
   - BLOCKING mode details
   - HYBRID mode details
   - NONBLOCKING mode details
   - Mode selection guidance

2. `approval-formats.md` (~50 lines):
   - AskUserQuestion template
   - Decision file format (before approval)
   - Decision file format (after approval)
   - GATE_CONFIG.txt format

3. `gating-examples.md` (~40 lines):
   - Complete flow examples for each mode
   - Edge case handling
   - Integration patterns

**Rationale**: The main file should explain the concept. Implementation details (exact formats, templates, examples) belong in reference files.

#### 2. route-subcommands (162 lines)

**Current structure**: Single file with:
- Purpose and when to use (lines 1-20)
- 5-step process (lines 22-76)
- 4 detailed examples (lines 79-122)
- Edge cases (lines 124-143)
- Output format specification (lines 145-162)

**Recommended split**:

**Keep in skill.md** (~60 lines):
- Core concept (parse /do: subcommands)
- When to use
- High-level process overview
- Integration with parent command
- Output contract (brief)
- Pointer to references

**Move to references/**:
1. `command-parsing.md` (~50 lines):
   - Pre-command detection rules
   - Post-command detection rules
   - Main instruction extraction
   - Ambiguity resolution rules

2. `routing-examples.md` (~50 lines):
   - All 4 examples with detailed walkthroughs
   - Self-reference handling
   - Ambiguous ordering resolution
   - No clear main instructions case

**Rationale**: Parsing rules and examples are reference material. The skill should focus on "what it does" and "how to invoke it", not exhaustive parsing logic.

#### 3. setup-testing (146 lines)

**Current structure**: Single file with:
- Purpose (lines 1-14)
- 5-step process (lines 16-90)
- Framework-specific setup (lines 92-133)
- Output format (lines 135-146)

**Recommended split**:

**Keep in skill.md** (~50 lines):
- Purpose and when to use
- High-level process (5 steps as brief list)
- Framework selection strategy
- Example invocation flow
- Pointer to framework references

**Move to references/**:
1. `framework-matrix.md` (~30 lines):
   - Language/framework recommendation table
   - Framework comparison criteria
   - When to choose alternatives

2. `framework-setup.md` (~60 lines):
   - JavaScript/TypeScript (Vitest, Jest, Mocha)
   - Python (pytest)
   - Go (go test)
   - Rust (cargo test)
   - Java (JUnit)
   - Ruby (RSpec)
   - Config examples for each

**Rationale**: Framework-specific setup commands are reference material that will be consulted when needed, not every time the skill is invoked.

## Broken References Assessment

### Agent: researcher.md

**Line 185**: References `/do:peek` command
```markdown
When invoked by `/do:peek`, operate in **peek mode**
```

**Issue**: Command `/do:peek` does not exist
**Available commands**: chores, docs, explore, it, plan, release, research
**Fix needed**:
- Option A: Remove peek mode section entirely (if feature not implemented)
- Option B: Update to `/do:explore` (if that's the intended command)
- Option C: Create `/do:peek` command if peek mode is desired functionality

**Recommendation**: Remove peek mode section. "Peek" functionality seems to be a fast variant of exploration, which should just be `/do:explore` with guidance to be fast/minimal.

**Line 206**: References `/do:learn` command
```markdown
- Question needs external research (redirect to `/do:learn`)
```

**Issue**: Command `/do:learn` does not exist
**Available command**: `/do:research` (based on commands/research.md)
**Fix needed**: Change `/do:learn` → `/do:research`

**Evidence**: CLAUDE.md documents `/do:research` as the external research command:
```markdown
### `/do:research` - External Research
/do:research jwt best practices    # Industry patterns
/do:research competitors           # Market analysis
```

**Line 207**: References `/do:status` command
```markdown
- Question is about correctness (redirect to `/do:status`)
```

**Issue**: Command `/do:status` does not exist as standalone
**Available**: `/do:plan status` subcommand (documented in CLAUDE.md)
**Fix needed**: Change `/do:status` → `/do:plan status`

**Evidence**: CLAUDE.md shows:
```markdown
/do:plan status             # Quick status check
```

## Universal Checks (Agent/Prompt Profile)

### File Syntax ✅
- All skill.md files: Valid YAML frontmatter
- All skills have required fields: `name`, `description`

### File References (Spot Check)

**gating-controller** - References state files:
- `.agent_planning/do-command-logs/CURRENT_EXECUTION_ID.txt` ✅ (pattern used across agents)
- `.agent_planning/do-command-state/<EXEC_ID>/GATE_CONFIG.txt` ✅ (created by gating system)
- `.agent_planning/do-command-state/<EXEC_ID>/DECISIONS/*.txt` ✅ (created by agents)

**route-subcommands** - No file references ✅

**setup-testing** - No file references ✅

**researcher.md** - File references:
- `.agent_planning/do-command-logs/CURRENT_EXECUTION_ID.txt` ✅
- `.agent_planning/RESEARCH-*.md` ✅ (created by this agent)
- `.agent_planning/STATUS-*.md` ✅ (created by evaluators)
- `.agent_planning/PLAN-*.md` ✅ (created by planners)

### Tool References ✅

**researcher.md agent**:
- Declared tools: Read, Glob, Grep, WebSearch, WebFetch ✅ (all valid)
- Model: sonnet ✅ (valid)

### Spelling/Grammar ✅
- Spot-checked key sections: No egregious issues

## Skill Description Quality

Most skills have ~100-150 character descriptions within the 1024 character limit. While they could be expanded, current descriptions are adequate and follow a consistent pattern:

| Skill | Chars | Quality |
|-------|-------|---------|
| gating-controller | 180 | Good - explains purpose and key constraint |
| route-subcommands | 156 | Good - explains purpose and usage |
| setup-testing | 148 | Good - explains purpose and when to use |
| evaluation-profiles | 381 | Excellent - comprehensive overview |

**Recommendation**: Current descriptions are sufficient. Focus on progressive disclosure structure first.

## Ambiguity Detection

No significant ambiguities detected in the three large skills:

**gating-controller**:
- Clear decision points (BLOCKING vs HYBRID vs NONBLOCKING)
- Well-defined file formats
- Explicit error handling

**route-subcommands**:
- Clear parsing rules
- Documented edge cases
- Explicit handling of ambiguous ordering

**setup-testing**:
- Asks user for confirmation (uses AskUserQuestion) ✅
- Framework recommendations are documented
- No silent assumptions

## Implementation Red Flags

### Quick Grep Results

```bash
grep -r "TODO\|FIXME\|stub\|placeholder" skills/*/skill.md
```

**Results**: No matches ✅

### Reference File Orphaning Risk ⚠️

**evaluation-profiles**: Currently the ONLY skill with reference files
- 6 reference files exist and are properly referenced
- Other skills reference this skill (project-evaluator, work-evaluator)
- **Risk**: If skill is removed, reference files are orphaned

**Recommendation**: Add references/ README or document reference file lifecycle

## Recommendations

### Priority 1: Fix Broken References (5 minutes)

1. **researcher.md line 185-210**: Remove or update peek mode section
   - **Recommended**: Remove entire "Peek Mode" section (lines 183-210)
   - **Rationale**: Command doesn't exist, feature scope unclear

2. **researcher.md line 206**: Change `/do:learn` → `/do:research`
   - **Impact**: Enables correct command routing

3. **researcher.md line 207**: Change `/do:status` → `/do:plan status`
   - **Impact**: Enables correct command routing

### Priority 2: Apply Progressive Disclosure (2-3 hours)

**Order of implementation**:

1. **setup-testing** (easiest, clearest split)
   - Create `skills/setup-testing/references/` directory
   - Move framework-specific content → `framework-setup.md`
   - Move framework selection table → `framework-matrix.md`
   - Update main skill.md with pointers
   - **Expected time**: 30 minutes

2. **route-subcommands** (medium complexity)
   - Create `skills/route-subcommands/references/` directory
   - Move parsing rules → `command-parsing.md`
   - Move examples → `routing-examples.md`
   - Update main skill.md
   - **Expected time**: 45 minutes

3. **gating-controller** (most complex, newest feature)
   - Create `skills/gating-controller/references/` directory
   - Move mode details → `gate-modes.md`
   - Move format specs → `approval-formats.md`
   - Move examples → `gating-examples.md`
   - Update main skill.md
   - **Expected time**: 60 minutes

### Priority 3: Documentation

1. Add `skills/README.md` explaining progressive disclosure pattern
2. Document reference file lifecycle (when to create, when to remove)
3. Add "how to add a skill" guide showing reference file structure

## What Could Not Be Verified

| Item | Why | User Can Check |
|------|-----|----------------|
| Runtime effectiveness of gating | New feature, no usage history | Deploy gating system, test with BLOCKING/HYBRID/NONBLOCKING modes |
| Subcommand parsing edge cases | Requires diverse user inputs | Test `/do:it` with various pre/post command combinations |
| Framework setup completeness | Limited to listed languages | Attempt setup on unlisted languages (C#, PHP, etc.) |

## Workflow Recommendation

- [x] CONTINUE - Issues are clear, implementer can fix
- [ ] PAUSE - No ambiguities requiring user input

**Next Actions**:
1. Fix 3 broken references in researcher.md
2. Apply progressive disclosure to 3 large skills (setup-testing first)
3. Validate reference structure matches evaluation-profiles pattern

## Evidence Summary

**Line counts verified**:
```
gating-controller/skill.md: 214 lines ❌ (target: ~80)
route-subcommands/skill.md: 162 lines ❌ (target: ~60)
setup-testing/skill.md: 146 lines ❌ (target: ~50)
evaluation-profiles/skill.md: 168 lines ✅ (has references)
```

**Reference file counts**:
```
evaluation-profiles/references/: 6 files ✅
gating-controller/references/: 0 files ❌
route-subcommands/references/: 0 files ❌
setup-testing/references/: 0 files ❌
```

**Broken command references**:
```
researcher.md:185 → /do:peek (doesn't exist)
researcher.md:206 → /do:learn (should be /do:research)
researcher.md:207 → /do:status (should be /do:plan status)
```

**Available commands** (verified):
```
chores.md ✅
docs.md ✅
explore.md ✅
it.md ✅
plan.md ✅
release.md ✅
research.md ✅
```
