# Definition of Done: connect-agents

**Sprint**: connect-agents
**Generated**: 2026-01-19

## Acceptance Criteria

### Functional

- [ ] execution-summarizer is invoked via Stop hook
- [ ] execution-summarizer produces EXEC-*.md reports when partial logs exist
- [ ] test-auditor is spawned during `/do:test audit` workflow
- [ ] test-auditor produces TEST-AUDIT-*.md output
- [ ] `/do:rigidity` command exists and is discoverable
- [ ] gabe agent produces expected artifacts (SYSTEM_MAP.md, NUCLEATION_SITES.md, etc.)

### Quality

- [ ] `just validate` passes
- [ ] No broken references in codebase
- [ ] hooks.json is valid JSON

### Documentation

- [ ] CLAUDE.md accurately reflects implemented functionality
- [ ] Agent descriptions note they are now connected

## Verification Commands

```bash
# Verify hooks.json is valid and has content
python -c "import json; d=json.load(open('plugins/do-more/hooks/hooks.json')); print('OK' if d.get('hooks') else 'EMPTY')"

# Verify rigidity command exists
test -f plugins/do-more/commands/rigidity.md && echo "OK: rigidity command exists"

# Verify rigidity skill exists
test -f plugins/do-more/skills/rigidity-skill/SKILL.md && echo "OK: rigidity skill exists"

# Run validation
just validate
```

## Not In Scope

- Removing duplicate gabe from do-extra (separate roadmap item)
- Implementing the hooks that were falsely documented (separate roadmap item)
- Major refactoring of existing skills
