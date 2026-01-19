# Definition of Done: remove-gabe-dup

**Sprint**: remove-gabe-dup
**Generated**: 2026-01-19

## Acceptance Criteria

### Functional
- [ ] `plugins/do-extra/agents/gabe.md` deleted
- [ ] `plugins/do-more/agents/gabe.md` unchanged and exists
- [ ] gabe agent remains discoverable via do-more plugin

### Quality
- [ ] `just validate` passes
- [ ] No broken references in codebase

### Documentation
- [ ] `plugins/do-extra/README.md` updated - no gabe references
- [ ] README.md structure preserved

## Verification Commands

```bash
# Verify do-extra gabe deleted
test ! -f plugins/do-extra/agents/gabe.md && echo "PASS: do-extra gabe deleted"

# Verify do-more gabe exists
test -f plugins/do-more/agents/gabe.md && echo "PASS: do-more gabe exists"

# Verify no gabe references in do-extra README
! grep -q "gabe" plugins/do-extra/README.md && echo "PASS: README clean"

# Run validation
just validate
```

## Not In Scope

- Creating command to invoke gabe (separate roadmap item: connect-orphaned-agents)
- Modifying gabe agent content
- Moving gabe to different plugin
