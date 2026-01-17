# Definition of Done: roadmap-thin-wrapper

Sprint: roadmap-thin-wrapper
Generated: 2026-01-16

## Acceptance Criteria

### Structure
- [ ] Skill directory is `plugins/do/skills/do-roadmap-skill/`
- [ ] Skill contains `SKILL.md` and `SCHEMA.md`
- [ ] Command file is `plugins/do/commands/roadmap.md`
- [ ] Command is ≤50 lines (target ~30)

### Skill (do-roadmap-skill)
- [ ] Frontmatter has `name: do-roadmap-skill`
- [ ] Has entry point procedure that accepts mode/topic
- [ ] All 9 original procedures preserved and functional
- [ ] SCHEMA.md unchanged except for reference updates

### Command (roadmap.md)
- [ ] Preserves frontmatter: `argument-hint`, `description`
- [ ] Invokes skill via `Skill("do:do-roadmap-skill")`
- [ ] Parses arguments to determine mode
- [ ] No implementation logic (pure delegation)

### Behavior (unchanged)
- [ ] `/do:roadmap` (no args): displays tree view or "no roadmap" message
- [ ] `/do:roadmap topic` (with args): triggers add flow with disambiguation
- [ ] All user interactions preserved (phase selection, similarity check, etc.)

### Documentation
- [ ] All references updated to new skill name
- [ ] README.md still documents `/do:roadmap` command
- [ ] Internal cross-references consistent

### Validation
- [ ] `just validate` passes
- [ ] `just test` passes
- [ ] No broken references or dangling paths
