# Definition of Done: fix-hooks

**Sprint**: fix-hooks
**Generated**: 2026-01-19

## Acceptance Criteria

### Functional
- [ ] No documentation claims hook functionality that doesn't exist
- [ ] No references to `bin/init.py` or `bin/aggregate-exec.py`
- [ ] No false claims about execution logging in `.agent_logs/do/`
- [ ] Feature proposal archived to `.agent_planning/archive/`

### Quality
- [ ] `just validate` passes
- [ ] Documentation is internally consistent
- [ ] grep for `bin/init.py` returns no results in do-more

### Documentation
- [ ] CLAUDE.md accurate
- [ ] README.md accurate
- [ ] architecture/*.md accurate
- [ ] execution-summarizer noted as "not yet wired"

## Verification Commands

```bash
# Verify no bin/ references
grep -r "bin/init.py\|bin/aggregate-exec.py" plugins/do-more/ && echo "FAIL: bin references found" || echo "PASS: no bin references"

# Verify no .agent_logs claims
grep -r "\.agent_logs/do/" plugins/do-more/ && echo "FAIL: agent_logs claims found" || echo "PASS: no agent_logs claims"

# Verify feature proposal archived
test ! -f plugins/do-more/FEATURE_PROPOSAL_subagent_execution_logging.md && echo "PASS: proposal archived"

# Run validation
just validate
```

## Not In Scope

- Implementing hooks (future work if needed)
- Wiring execution-summarizer (separate roadmap item: connect-orphaned-agents)
- Creating execution logging infrastructure
