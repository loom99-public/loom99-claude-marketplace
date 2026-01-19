# Sprint: fix-hooks

**Generated**: 2026-01-19
**Confidence**: HIGH
**Status**: READY FOR IMPLEMENTATION

## Sprint Goal

Remove false documentation about non-existent hook functionality from do-more plugin.

## Scope

**Deliverables:**
1. Update CLAUDE.md to remove false hook claims
2. Update README.md to remove execution log references
3. Update architecture docs to remove `bin/` references
4. Archive obsolete feature proposal file

## Work Items

### P0: Update do-more CLAUDE.md

**File:** `plugins/do-more/CLAUDE.md`

**Remove:**
- "Hooks (SessionStart/Stop)" architecture claim
- "Stop hook aggregates into final report" claim
- "Execution Tracking" section documenting non-existent files
- "Hooks" section documenting `bin/init.py` and `bin/aggregate-exec.py`

**Update:**
- `execution-summarizer` agent entry to note it's not yet connected

**Acceptance Criteria:**
- [ ] No references to `bin/init.py` or `bin/aggregate-exec.py`
- [ ] No false claims about execution logging
- [ ] execution-summarizer documented as "not yet wired"

### P1: Update do-more README.md

**File:** `plugins/do-more/README.md`

**Remove:**
- "Stop hook aggregates execution report" from How It Works
- "`.agent_logs/do/` has the receipts" claim
- Execution report file references

**Acceptance Criteria:**
- [ ] No false claims about execution logging
- [ ] How It Works section accurate

### P2: Update architecture docs

**Files:**
- `plugins/do-more/architecture/README.md`
- `plugins/do-more/architecture/EXECUTION-FLOW.md`

**Remove:**
- "Hook Integration" section
- `bin/` from plugin structure diagram
- "Hook Execution Flow" section entirely
- Runtime files section's execution log references

**Acceptance Criteria:**
- [ ] Architecture docs match actual implementation
- [ ] No references to non-existent `bin/` directory

### P3: Archive obsolete files

**File:** `plugins/do-more/FEATURE_PROPOSAL_subagent_execution_logging.md`

**Action:** Move to `.agent_planning/archive/`

**Acceptance Criteria:**
- [ ] Feature proposal archived, not in active plugin directory

### P4: Document empty hooks.json

**File:** `plugins/do-more/hooks/hooks.json`

**Option A:** Delete file entirely
**Option B:** Add comment explaining no hooks implemented

**Acceptance Criteria:**
- [ ] Empty hooks.json is either deleted or documented

## Dependencies

None - documentation cleanup only.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Miss a doc reference | Low | Low | Grep verification after changes |
