# Evaluation: Roadmap Command → Skill Refactor

Topic: Moving roadmap command logic into skill
Generated: 2026-01-16

## Summary

The user wants to:
1. Move logic from `/do:roadmap` command into the `roadmap` skill
2. Rename the skill to `do-roadmap-skill`
3. Keep the slash command as a thin wrapper

## Analysis

### Current State

**Command (`plugins/do/commands/roadmap.md`):**
- 448 lines of implementation logic
- Handles two modes: view (no args) and add (with args)
- Contains step-by-step procedures for parsing, similarity checking, phase selection, etc.
- References skill procedures like `parse_roadmap()`, `format_tree_view()`, etc.

**Skill (`plugins/do/skills/roadmap/SKILL.md`):**
- 738 lines of procedural documentation
- Defines 9 procedures (parse, find, add, write, get_status, format_tree, format_status, create_epic, initialize)
- Contains the actual algorithms
- Already has comprehensive procedure definitions

**Schema (`plugins/do/skills/roadmap/SCHEMA.md`):**
- 317 lines of format specification
- Data model definitions

### Question Answers

#### 1. Are there references to the roadmap slash command elsewhere in the repo?

**YES.** Found 18 references across:

| File | Type |
|------|------|
| `README.md` | Documentation (describes `/do:roadmap`) |
| `plugins/do/commands/roadmap.md` | Self-references (usage examples) |
| `plugins/do/skills/roadmap/SKILL.md` | Cross-references to command |
| `plugins/do/skills/roadmap/SCHEMA.md` | Usage guidance |

**Impact:** Documentation updates needed in 4 files.

#### 2. What impact might this have on other things that use or depend on roadmap?

**LOW IMPACT.** Analysis:

- **No other commands** directly call the roadmap command
- **No agents** invoke roadmap as a dependency
- **The skill** is already the "source of truth" for algorithms
- **The command** is user-facing entry point only

The only dependencies are:
1. User invocations via `/do:roadmap`
2. Documentation references
3. The skill itself (which won't change functionally)

#### 3. Does this change the functionality in any way?

**NO.** This is a pure refactoring:

- Same input (command + args)
- Same output (tree view or add confirmation)
- Same procedures
- Same user experience

The change is structural, not behavioral.

#### 4. Can I call a skill from a slash command?

**YES.** This is the primary pattern. Examples:

```markdown
# From /do:test command
| `setup` | Set up test framework → `Skill("do:setup-testing")` |

# From /do:audit command
**Use the Skill tool** to invoke `do:audit-master` skill
```

Syntax:
```
Skill("skill-name")
Skill("skill-name") with:
  parameter: value
```

#### 5. Can I call a skill from another skill?

**YES.** Skills compose other skills. Examples:

```markdown
# From audit-master skill
Skill("do:deferred-work-capture") with:
  title: "Audit finding"
  description: "..."

# Architecture shows:
do:audit → do:deep-audit
        → do:security-audit
        → do:planning-audit
```

This is extensively used for:
- `do:deferred-work-capture` (called by many skills/agents)
- Audit skill composition
- Test workflow composition

### Recommended Approach

**Option A: Standard Wrapper Pattern** (Recommended)

1. Keep command as thin wrapper (~30 lines)
2. Move all logic to skill
3. Command invokes skill, skill returns result
4. Minimal code duplication

```markdown
# roadmap.md (thin wrapper)
---
argument-hint: [topic to add to roadmap]
description: View roadmap tree or add topic.
---

# Roadmap Command

Invoke the `do-roadmap-skill` to handle roadmap operations.

## Implementation

Skill("do:do-roadmap-skill") with:
  mode: "view" if not ARGUMENTS else "add"
  topic: ARGUMENTS.strip() or null
```

**Option B: Direct Skill Invocation**

Remove command entirely, rely on skill auto-discovery.

- Pros: Less code
- Cons: Loses explicit `/do:roadmap` entry point, harder to discover

### Naming Considerations

Current: `roadmap` skill
Proposed: `do-roadmap-skill`

**Observation:** The `do-` prefix is redundant since skill is in `do` plugin. Standard pattern uses just the skill name (`roadmap`, `beads`, `deferred-work-capture`).

Suggested alternatives:
1. Keep `roadmap` (current, conventional)
2. Use `do-roadmap` (matches command namespace)
3. Use `do-roadmap-skill` (explicit but verbose)

## Verdict

**CONTINUE** - Clear path forward with no blockers.

## Files to Modify

1. `plugins/do/commands/roadmap.md` - Thin wrapper (reduce from 448 lines to ~30)
2. `plugins/do/skills/roadmap/SKILL.md` - Add entry point procedure
3. `README.md` - Update if skill name changes
4. Optionally rename skill directory if changing name

## Risks

| Risk | Mitigation |
|------|------------|
| Documentation drift | Update all refs in same PR |
| Skill name confusion | Discuss naming before implementing |
| Regression in behavior | Test both modes (view/add) after |
