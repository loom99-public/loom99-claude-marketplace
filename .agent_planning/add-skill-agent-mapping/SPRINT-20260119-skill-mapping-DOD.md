# Definition of Done: skill-mapping

**Sprint**: skill-mapping
**Generated**: 2026-01-19

## Acceptance Criteria

### Content
- [ ] CLAUDE.md contains "Skill-Agent Invocations" section with accurate mappings
- [ ] CLAUDE.md contains "Skill Dependencies" section showing pipeline flows
- [ ] CLAUDE.md contains "Workflow Decision Trees" for /do:it and /do:test
- [ ] All agent names match actual agent file names in `agents/`
- [ ] All skill names match actual skill names in `skills/*/SKILL.md`

### Quality
- [ ] Formatting matches existing CLAUDE.md style
- [ ] Diagrams render correctly in markdown viewers
- [ ] No broken internal references
- [ ] `just validate` passes

### Integration
- [ ] Existing CLAUDE.md content preserved
- [ ] New sections logically placed (after Agent Mapping section)
- [ ] Table of contents updated if one exists

## Verification Commands

```bash
# Verify new sections exist
grep -q "Skill-Agent Invocations" plugins/do-more/CLAUDE.md && echo "OK: Invocations table exists"
grep -q "Skill Dependencies" plugins/do-more/CLAUDE.md && echo "OK: Dependencies section exists"
grep -q "Workflow Decision Trees" plugins/do-more/CLAUDE.md && echo "OK: Decision trees exist"

# Run validation
just validate
```

## Not In Scope

- Modifying actual skills or agents
- Creating new workflow diagrams outside CLAUDE.md
- Updating other documentation files
