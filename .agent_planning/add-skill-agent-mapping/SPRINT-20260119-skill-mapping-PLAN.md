# Sprint: skill-mapping

**Generated**: 2026-01-19
**Confidence**: HIGH
**Status**: READY FOR IMPLEMENTATION

## Sprint Goal

Add skill-to-agent mapping documentation to do-more CLAUDE.md.

## Scope

**Deliverables:**
1. Add Skill-Agent Invocations table
2. Add Skill Dependencies graph
3. Add Workflow Decision Trees

## Work Items

### P0: Add Skill-Agent Invocations table

**File:** `plugins/do-more/CLAUDE.md`

**Location:** After existing Agent Mapping section (around line 88)

**Content:**
```markdown
## Skill-Agent Invocations

| Skill | Agents Invoked | Sequence |
|-------|----------------|----------|
| `do:tdd-workflow` | functional-tester → project-evaluator → test-driven-implementer → work-evaluator | TestLoop then ImplementLoop |
| `do:iterative-workflow` | iterative-implementer → work-evaluator | Loop until COMPLETE |
| `do:fix` | researcher → iterative-implementer → work-evaluator | Investigate → Fix → Verify |
| `do:debug` | researcher → work-evaluator | Investigate → Report (no fix) |
| `do:refactor` | project-evaluator → iterative-implementer → work-evaluator | Analyze → Restructure → Verify |
| `do:review` | project-evaluator | Single-pass review |
| `do:add-tests` | project-evaluator → functional-tester → work-evaluator | Find gaps → Write tests → Verify |
| `do:competitive-audit` | researcher | External research |
| `do:explore-skill` | researcher (explore mode) | Codebase search |
| `do:stuff-skill` | project-evaluator, status-planner, researcher, (tdd or iterative) | Full orchestration |
```

**Acceptance Criteria:**
- [ ] Table added with accurate mappings
- [ ] All agent names match actual agent files
- [ ] All skill names match actual skill files

### P1: Add Skill Dependencies graph

**Location:** After Skill-Agent Invocations table

**Content:**
```markdown
## Skill Dependencies

### Audit Pipeline
​```
/do:audit
    └── audit-master
        ├── [code] → deep-audit
        ├── [planning] → planning-audit
        ├── [security] → security-audit
        ├── [competitive] → competitive-audit → researcher
        └── [testing] → test-coverage-audit
​```

### Testing Pipeline
​```
/do:test
    └── testing-master
        ├── setup → setup-testing
        ├── audit → test-coverage-audit
        ├── recommend → test-recommendations
        └── plan → test-implementation-plan
​```

### Implementation Pipeline
​```
/do:it OR /do:stuff
    └── stuff-skill
        ├── [no plan] → project-evaluator → status-planner
        ├── [unknowns] → researcher
        └── [implement] → tdd-workflow OR iterative-workflow
​```
```

**Acceptance Criteria:**
- [ ] Diagrams accurately reflect skill dependencies
- [ ] Formatting renders correctly in markdown

### P2: Add Workflow Decision Trees

**Location:** After Skill Dependencies section

**Content:**
```markdown
## Workflow Decision Trees

### /do:it Intent Detection
​```
User says...
├── "tdd", "test first" → tdd-workflow
├── "refactor", "restructure" → refactor skill
├── "debug", "investigate" → debug skill
├── "fix", "bug", "broken" → fix skill
├── "review", "PR" → review skill
├── "test", "add tests" → add-tests skill
├── "iterate", "build" → iterative-workflow
└── (default) → auto-select based on:
    ├── test framework exists + API/logic → tdd-workflow
    └── otherwise → iterative-workflow
​```
```

**Acceptance Criteria:**
- [ ] Decision trees match actual intent detection logic
- [ ] Clear and readable format

## Dependencies

None - documentation addition only.

## Verification

- [ ] CLAUDE.md renders correctly
- [ ] All references valid
- [ ] `just validate` passes
