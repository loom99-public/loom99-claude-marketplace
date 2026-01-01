# Evaluation Cache Skill

Share evaluation findings between evaluators to avoid redundant work across context clears and different evaluation scopes.

## Cache Location

```
.agent_planning/eval-cache/
├── INDEX.md                      # Topic index with timestamps
├── project-structure.md          # Project layout, key files, entry points
├── test-infrastructure.md        # Test framework, patterns, coverage
├── architecture.md               # Key patterns, data flow, dependencies
├── runtime-<scope>.md            # Runtime behavior findings per scope
└── findings-<topic>.md           # Other reusable findings
```

## REQUIRED: Check Cache Before Evaluating

**This is mandatory. Do not skip.**

1. **Check INDEX.md exists**
   ```bash
   cat .agent_planning/eval-cache/INDEX.md 2>/dev/null
   ```

2. **Assess freshness of relevant entries**
   - FRESH (< 1 hour): Use directly, no re-validation needed
   - RECENT (< 24 hours): Use with light validation (spot-check key claims)
   - STALE (> 24 hours): Re-validate critical findings, reuse stable facts
   - ANCIENT (> 7 days): Treat as hints only, verify before using

3. **Grep for related topics if index miss**
   ```bash
   grep -r "<your-topic>" .agent_planning/eval-cache/ 2>/dev/null
   ```

4. **Cross-read other evaluator outputs**
   - Read latest `EVAL-*.md`, `STATUS-*.md`, `RELEVANT-FILES-*.md`

5. **Document what you reused**
   In your output, include:
   ```
   ## Reused From Cache
   - project-structure.md (FRESH, 23 min ago)
   - test-infrastructure.md (RECENT, 4 hours ago, spot-checked)
   ```

## REQUIRED: Write to Cache After Evaluating

**Factor out reusable findings. Do not skip.**

1. **Identify reusable knowledge**
   - Project structure (rarely changes)
   - Test infrastructure setup
   - Architecture patterns
   - Discovered conventions
   - Runtime behavior per scope

2. **Write cache entries** using this format:
   ```markdown
   # <Topic>

   **Cached**: <timestamp>
   **Source**: <agent-name>
   **Confidence**: HIGH | MEDIUM | LOW
   **Scope**: <what this covers>

   ## Findings

   <reusable findings here>

   ## Validation Commands

   <commands to verify these findings still hold>
   ```

3. **Update INDEX.md**
   ```markdown
   # Evaluation Cache Index

   | Topic | File | Cached | Source | Confidence |
   |-------|------|--------|--------|------------|
   | Project Structure | project-structure.md | 2025-12-14 10:30 | project-evaluator | HIGH |
   | Test Infrastructure | test-infrastructure.md | 2025-12-14 10:30 | project-evaluator | HIGH |
   ```

## What to Cache vs. What Not to Cache

### Cache These (Stable Knowledge)
- Project structure, directory layout, key files
- Test framework, test patterns, how to run tests
- Build system, how to build/run
- Architecture patterns, data flow
- Code conventions discovered
- Dependency analysis

### Don't Cache (Ephemeral)
- Specific bug findings (put in WORK-EVALUATION)
- Current implementation status (put in STATUS)
- Verdicts (COMPLETE/INCOMPLETE) - these are point-in-time
- Specific test pass/fail results (re-run to verify)

## Cross-Evaluator Protocol

### project-evaluator reads from work-evaluator:
- Runtime test results (what was actually tested)
- Break-it test findings (vulnerabilities found)
- Data flow verification results

### work-evaluator reads from project-evaluator:
- Project structure (don't re-analyze)
- Test infrastructure (don't re-discover)
- Architecture understanding (don't re-derive)
- Previous STATUS findings for context

## Cache Invalidation (CRITICAL)

**Implementers MUST invalidate cache entries when they modify files.**

This is how the cache stays valid:
1. Evaluator writes knowledge to cache
2. Implementer modifies files
3. **Implementer removes cache entries covering those files** (REQUIRED)
4. Next evaluator finds cache miss → does fresh evaluation → writes new cache

**Two-layer validation:**
1. **Primary**: Implementers invalidate on every change
2. **Safety net**: Timestamps catch interrupted implementers

If implementer was interrupted (crash, context limit, user stop), it may not have invalidated. Evaluators MUST still check timestamps as backup.

### Invalidation Rules (for implementers)

| Files Modified | Remove These Cache Entries |
|----------------|---------------------------|
| `src/auth/*` | Any entry with "auth" in filename or content |
| `tests/*` | `test-infrastructure.md` |
| `package.json`, `pyproject.toml`, etc. | `project-structure.md` |
| New modules, architectural changes | `architecture.md` |
| Any file in a scope | `runtime-<scope>.md`, `findings-*-<scope>.md` |

**Rule of thumb**: If in doubt, remove more rather than less. Stale cache causes wrong evaluations.

### Implementer Commands

```bash
# 1. Check what exists
cat .agent_planning/eval-cache/INDEX.md

# 2. Find entries covering modified files
grep -l "<component>\|<module>" .agent_planning/eval-cache/*.md

# 3. Remove stale entries
rm .agent_planning/eval-cache/<matched>.md

# 4. Update INDEX.md - remove deleted entries from table
```

## Cache Maintenance

- **Max age**: Archive entries older than 30 days
- **Max entries**: Keep latest 3 versions of each topic
- **Cleanup command**:
  ```bash
  # Move old cache entries to archive
  find .agent_planning/eval-cache -mtime +30 -exec mv {} .agent_planning/archive/ \;
  ```

## Example: Checking Cache Before Project Evaluation

```markdown
## Cache Check (REQUIRED)

Checking eval-cache/INDEX.md...

Found cached entries:
- project-structure.md: FRESH (15 min ago) - will reuse
- test-infrastructure.md: RECENT (3 hours ago) - will spot-check
- architecture.md: STALE (2 days ago) - will re-validate key points

Cross-reading work-evaluator outputs...
- WORK-EVALUATION-2025-12-14-093000.md exists
  - Runtime tests: auth flow verified working
  - Break-it: No vulnerabilities found in auth
  - Will carry forward these findings

Proceeding with evaluation, reusing cached knowledge where applicable.
```

## Example: Writing to Cache After Evaluation

```markdown
## Updating Eval Cache (REQUIRED)

Writing to eval-cache/:
- project-structure.md (updated - found new entry point)
- test-infrastructure.md (unchanged - still valid)
- runtime-auth.md (new - captured auth flow testing)

Updated INDEX.md with timestamps.
```
