# Definition of Done: remove-vestigial-audit-skill

**Sprint**: remove-vestigial-audit-skill
**Generated**: 2026-01-18

## Acceptance Criteria

### Functional
- [ ] `plugins/do-more/skills/audit/` directory deleted
- [ ] `/do:audit` command still works (routes to audit-master)
- [ ] No broken skill references in documentation

### Quality
- [ ] `just validate` passes
- [ ] `just test` passes
- [ ] No regression in audit functionality

### Documentation
- [ ] CLAUDE.md skill reference updated
- [ ] docs/SKILLS.md references corrected

## Verification Commands

```bash
# Verify directory deleted
ls plugins/do-more/skills/audit/ 2>&1 | grep -q "No such file"

# Verify audit-master still exists
test -f plugins/do-more/skills/audit-master/SKILL.md

# Verify command still exists
test -f plugins/do-more/commands/audit.md

# Run validation
just validate

# Run tests
just test
```

## Not In Scope

- Renaming audit-master to audit
- Consolidating other audit-related skills (planning-audit, security-audit, etc.)
- Changing how the audit command works
