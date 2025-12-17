# /commit-code - Implementation Commit Stage

## Purpose

Commit the implementation separately from tests, completing the TDD cycle with clear git history.

## When to Use

After all tests pass and implementation is complete, to document the test-driven development workflow.

## Workflow

1. **Final test verification**: Run full test suite, confirm 100% pass
2. **Review implementation**: Check for debug code, TODOs, test modifications
3. **Stage implementation**: Add only implementation files (tests already committed)
4. **Write commit message**: Document what was implemented and how it passes tests
5. **Commit**: Create clean git history showing TDD discipline
6. **Verify history**: Confirm two-commit pattern (tests → implementation)

## Key Principles

- **Git history proves TDD**: Two commits show (1) tests first, (2) implementation passes
- **Implementation only**: Tests were committed separately in previous commit
- **All tests must pass**: Never commit failing implementation
- **Clear documentation**: Commit message links implementation to test requirements
- **No test modifications**: Implementation adapts to tests, not vice versa

## Prerequisites

Before committing:

```bash
# All tests must pass
pytest -v  # or npm test, go test

# Tests were not modified
git diff tests/  # Should show no changes

# Implementation is complete
# - No TODOs or placeholders
# - No debug code
# - All edge cases handled
```

## Commit Message Format

```
<type>(<scope>): implement <feature>

<Description of implementation>

Implementation passes all tests from previous commit:
- <test scenario 1>
- <test scenario 2>
- <edge case>
- <error handling>

Key implementation details:
- <detail 1>
- <detail 2>

Tests: <test_name_1>, <test_name_2> (all passing)
```

## Example (Python)

```bash
# Final test run
pytest -v
# ========================= 8 passed in 0.45s =========================

# Review changes
git status
git diff src/

# Stage implementation only
git add src/auth/

# Verify tests not staged
git diff --cached tests/  # (no changes)

# Commit
git commit -m "feat(auth): implement user validation

Complete email, password, and username validation following TDD.

Implementation passes all tests from previous commit:
- Valid formats accepted
- Invalid formats rejected with clear errors
- Duplicate detection working
- Edge cases handled

Key details:
- Email validation uses RFC-compliant regex
- Password hashing with bcrypt (cost factor 12)
- Clear error messages for all failures

Tests: test_valid_email, test_password_strength,
       test_duplicate_email (all passing)"

# Verify TDD history
git log --oneline -2
# abc123 feat(auth): implement user validation
# def456 test(auth): add tests for user validation
```

## Anti-Patterns

❌ **Committing with failing tests**:
```bash
pytest -v  # 6 passed, 2 failed
git commit  # WRONG - fix implementation first
```

✅ **Fix implementation until all pass**:
```bash
# Use /iterate until 100% passing
pytest -v  # 8 passed, 0 failed
git commit  # Now ready
```

❌ **Committing tests with implementation**:
```bash
git add tests/ src/  # Combined commit hides TDD
```

✅ **Separate commits maintain TDD history**:
```bash
# Tests already committed separately
git add src/
git commit
```

❌ **Committing modified tests**:
```bash
git diff tests/  # Shows test changes
git commit  # WRONG - tests shouldn't change during implementation
```

✅ **Tests unchanged, implementation adapts**:
```bash
git diff tests/  # No changes
git add src/
git commit  # Clean TDD cycle
```

## Transition

After committing implementation:

- **Next feature**: Type `/write-tests` to begin new TDD cycle
- **Code review**: Create pull request referencing both commits
- **Production**: Merge with confidence (tests prove it works)

---

**Two commits tell the complete TDD story. Tests define the contract, implementation fulfills it.**
