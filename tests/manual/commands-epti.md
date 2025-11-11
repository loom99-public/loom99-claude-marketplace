# epti Command Test Scenarios

Test scenarios for all 6 TDD workflow commands in the epti plugin.

## Command Test Matrix

| Command | Purpose | Expected Content |
|---------|---------|------------------|
| /write-tests | Generate tests before implementation | Test writing strategies, coverage, examples |
| /verify-fail | Confirm tests fail properly | Verification steps, expected failures |
| /commit-tests | Commit tests separately | Test-only commit workflow |
| /implement | Implement code to pass tests | Implementation with test validation |
| /iterate | Refine implementation | Refinement guidance, optimization |
| /commit-code | Commit final implementation | Code commit workflow |

## Test Scenario: /write-tests

**Purpose:** Verify test writing guidance appears

**Steps:**
- Type `/write-tests` and press Enter
- Observe prompt expansion

**Expected:**
- Comprehensive test writing guidance (400+ lines)
- Test-first discipline emphasized
- Framework-specific examples (pytest, jest, etc.)
- No errors

**Error Scenarios:**

| Scenario | Expected Behavior |
|----------|-------------------|
| /write-tests without requirements | Should guide on defining requirements first |
| Typo: /write-test | Command not found |

## Test Scenario: /verify-fail

**Purpose:** Verify test failure verification guidance

**Steps:**
- Type `/verify-fail` and press Enter
- Observe prompt expansion

**Expected:**
- Guidance on running tests and confirming they fail
- Explanation of why tests should fail first
- Examples of proper test failures
- No errors

## Test Scenario: /commit-tests

**Purpose:** Verify test commit guidance

**Steps:**
- Type `/commit-tests` and press Enter
- Observe prompt expansion

**Expected:**
- Guidance on committing tests separately from implementation
- Git workflow for test-only commits
- Commit message format for tests
- No errors

## Test Scenario: /implement

**Purpose:** Verify implementation guidance with test protection

**Steps:**
- Type `/implement` and press Enter
- Observe prompt expansion

**Expected:**
- Implementation guidance emphasizing passing tests
- Warnings against test-specific hacks
- Code quality standards
- Verification steps
- No errors

**Error Scenarios:**

| Scenario | Expected Behavior |
|----------|-------------------|
| /implement without tests | Agent should block and require tests first |
| /implement with passing tests | Agent may question if implementation already exists |

## Test Scenario: /iterate

**Purpose:** Verify refinement guidance

**Steps:**
- Type `/iterate` and press Enter
- Observe prompt expansion

**Expected:**
- Refinement and optimization guidance
- Emphasis on maintaining passing tests
- Refactoring strategies
- No errors

## Test Scenario: /commit-code

**Purpose:** Verify code commit guidance

**Steps:**
- Type `/commit-code` and press Enter
- Observe prompt expansion

**Expected:**
- Final commit workflow guidance
- Verification that all tests pass
- Code review preparation
- No errors

**Error Scenarios:**

| Scenario | Expected Behavior |
|----------|-------------------|
| /commit-code with failing tests | Agent should block commit |
| /commit-code without implementation | Agent should indicate nothing to commit |

## Complete TDD Workflow Test

**Execute full TDD cycle:**

- Use `/write-tests` to create tests
- Use `/verify-fail` to confirm tests fail
- Use `/commit-tests` to commit tests
- Use `/implement` to create passing implementation
- Use `/iterate` if refinement needed
- Use `/commit-code` to finalize

**Expected:**
- All 6 commands work in sequence
- Agent enforces test-first discipline
- Tests must fail before implementation
- Tests must pass before final commit
- Workflow prevents anti-patterns

## Negative Test Scenarios

### TDD Discipline Violations

| Violation | Expected Agent Behavior |
|-----------|------------------------|
| Skip /write-tests, go to /implement | Agent blocks and requires tests first |
| Skip /verify-fail | Agent warns about importance of failing tests |
| Use /commit-code with failing tests | Agent blocks commit |
| Implement before writing tests | Agent detects and blocks anti-pattern |

### Invalid Commands

| Invalid Command | Expected |
|----------------|----------|
| /write-test | Not found error |
| /verify | Not found error |
| /commit | Ambiguous (conflicts with agent-loop?) |

## Success Criteria

- All 6 commands accessible via autocomplete
- Each command provides comprehensive TDD guidance
- Agent enforces test-first discipline
- Anti-patterns are detected and blocked
- Complete TDD workflow (write-tests→verify-fail→commit-tests→implement→commit-code) executes successfully
- Negative tests handle errors appropriately
