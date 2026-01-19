# Definition of Done: rename-research

**Sprint**: rename-research
**Generated**: 2026-01-19

## Acceptance Criteria

### Functional
- [ ] `/do:external-research` command works
- [ ] `/do:research` in do plugin (internal) still works unchanged
- [ ] Old `/do:research` command file removed from do-more
- [ ] `research-external-skill` skill unchanged (name stays same)

### Quality
- [ ] `just validate` passes
- [ ] `python scripts/generate_commands.py` runs successfully

### Documentation
- [ ] All do-more documentation references updated
- [ ] No `/do:research` references remain in do-more plugin (verify with grep)
- [ ] ROADMAP.md updated to reflect completion

## Verification Commands

```bash
# Verify new command exists
test -f plugins/do-more/commands/external-research.md && echo "OK: New command exists"

# Verify old command removed
test ! -f plugins/do-more/commands/research.md && echo "OK: Old command removed"

# Verify no orphaned references in do-more
if grep -r "/do:research" plugins/do-more/ | grep -v "external-research" | grep -v ".md:.*do:researcher" | grep -q .; then
  echo "FAIL: Orphaned /do:research references found"
else
  echo "OK: No orphaned references"
fi

# Verify do plugin research unchanged
test -f plugins/do/commands/research.md && echo "OK: do plugin research intact"

# Run validation suite
just validate
```

## Not In Scope

- Renaming `research-external-skill` (skill name stays the same)
- Changing the skill behavior
- Modifying the do plugin's `/do:research` command
