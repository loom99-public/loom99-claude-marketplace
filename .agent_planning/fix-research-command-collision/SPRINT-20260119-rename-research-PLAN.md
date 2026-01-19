# Sprint: rename-research

**Generated**: 2026-01-19
**Confidence**: HIGH
**Status**: READY FOR IMPLEMENTATION

## Sprint Goal

Rename do-more's `/do:research` command to `/do:external-research` to eliminate namespace collision.

## Scope

**Deliverables:**
1. Rename command file from `research.md` to `external-research.md`
2. Update `commands.yaml` configuration
3. Update all documentation references

## Work Items

### P0: Rename command file and update configuration

**Files to change:**
1. `plugins/do-more/commands/research.md` → `plugins/do-more/commands/external-research.md`
2. `commands.yaml` line 104-108: Change `name: research` to `name: external-research`

**Acceptance Criteria:**
- [ ] Old file `plugins/do-more/commands/research.md` deleted
- [ ] New file `plugins/do-more/commands/external-research.md` exists
- [ ] `commands.yaml` has `name: external-research`
- [ ] `python scripts/generate_commands.py` runs without errors

### P1: Update do-more CLAUDE.md

**File:** `plugins/do-more/CLAUDE.md`

Changes needed at command table and agent mapping sections.

**Acceptance Criteria:**
- [ ] Command table updated
- [ ] All `/do:research` references changed to `/do:external-research`

### P2: Update do-more README.md

**File:** `plugins/do-more/README.md`

Command section needs renaming.

**Acceptance Criteria:**
- [ ] Command section header updated
- [ ] All examples use `/do:external-research`

### P3: Update docs directory

**Files in `plugins/do-more/docs/`:**
- COMMANDS.md (many references)
- AGENTS.md
- EXAMPLES.md
- GETTING-STARTED.md
- GATING.md
- README.md
- SKILLS.md
- WORKFLOWS.md

**Acceptance Criteria:**
- [ ] All `/do:research` references in do-more/docs/ updated
- [ ] No orphaned references remain

### P4: Update architecture docs

**File:** `plugins/do-more/architecture/README.md`

**Acceptance Criteria:**
- [ ] Architecture docs updated

## Dependencies

None - this is a rename operation.

## Verification

```bash
# Verify no remaining /do:research in do-more (should only find /do:external-research)
grep -r "/do:research" plugins/do-more/ | grep -v external

# Verify new command exists
test -f plugins/do-more/commands/external-research.md

# Verify old command gone
test ! -f plugins/do-more/commands/research.md

# Run validation
just validate
```
