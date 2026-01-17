# Implementation Context: roadmap-thin-wrapper

Sprint: roadmap-thin-wrapper
Generated: 2026-01-16

## Why This Refactor

The user wants to standardize skill naming with `do-*-skill` prefix to:
1. Avoid namespace conflicts with built-in commands (e.g., `plan`)
2. Make skill identity explicit
3. Future-proof as more skills are added

## Key Files

### Source (before)
```
plugins/do/
├── commands/roadmap.md          # 448 lines, full implementation
└── skills/roadmap/
    ├── SKILL.md                 # 738 lines, procedures
    └── SCHEMA.md                # 317 lines, format spec
```

### Target (after)
```
plugins/do/
├── commands/roadmap.md          # ~30 lines, thin wrapper
└── skills/do-roadmap-skill/
    ├── SKILL.md                 # ~750 lines, procedures + entry point
    └── SCHEMA.md                # 317 lines, unchanged
```

## Skill Invocation Pattern

From command:
```markdown
Skill("do:do-roadmap-skill") with:
  mode: "view" | "add"
  topic: "<topic-string>" | null
```

The skill handles:
- Argument validation
- Mode routing (view vs add)
- All user interactions (via do:prompt-questioning)
- File operations (parse, write ROADMAP.md)
- Beads integration

## Entry Point Procedure

Add to SKILL.md as "Procedure 0: Execute Command":

```python
def execute_command(mode: str, topic: str | None):
    """Entry point for /do:roadmap command"""

    if mode == "view":
        # Check if ROADMAP.md exists
        if not file_exists(".agent_planning/ROADMAP.md"):
            return "No roadmap yet.\n\nRun /do:roadmap <topic> to create..."

        roadmap = parse_roadmap(".agent_planning/ROADMAP.md")
        return format_tree_view(roadmap)

    elif mode == "add":
        # Full add flow:
        # 1. Check/create ROADMAP.md
        # 2. Parse existing
        # 3. Similarity check (LLM-based)
        # 4. Disambiguation if needed (prompt-questioning)
        # 5. Phase selection (prompt-questioning)
        # 6. Capture summary (prompt-questioning)
        # 7. Create beads epic
        # 8. Create topic directory
        # 9. Add to roadmap
        # 10. Write file
        # 11. Return confirmation
        ...
```

## Thin Wrapper Structure

```markdown
---
argument-hint: [topic to add to roadmap]
description: View roadmap tree or add topic. No args = show tree view. With args = add to roadmap.
---

# Roadmap Command

Hierarchical project planning with phases and topics.

## Usage

- `/do:roadmap` - Display roadmap tree view
- `/do:roadmap <topic>` - Add topic to roadmap

## Implementation

Determine mode and invoke skill:

Skill("do:do-roadmap-skill") with:
  mode: "view" if not ARGUMENTS.strip() else "add"
  topic: ARGUMENTS.strip() if ARGUMENTS.strip() else null
```

## Reference Updates Needed

| File | Line(s) | Change |
|------|---------|--------|
| SKILL.md | 58 | `do:roadmap` → `do:do-roadmap-skill` |
| SKILL.md | 737 | "See Also" section update |
| SCHEMA.md | - | Move to new directory |
| README.md | 87 | Keep as-is (documents command, not skill) |

## Testing

Manual verification:
1. `just validate` - plugin structure valid
2. `/do:roadmap` - view mode works
3. `/do:roadmap test-feature` - add mode works
4. Check `.agent_planning/ROADMAP.md` modified correctly after add

## Notes

- The skill is invoked as `do:do-roadmap-skill` (plugin:skill-name)
- Users can also invoke unprefixed `do-roadmap-skill` but this isn't recommended
- Git history preserved via `git mv`
