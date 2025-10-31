# /commit-tests - Test Commit Stage

## Purpose

Commit test files separately from implementation to prove tests were written first (TDD discipline).

## When to Use

After tests are written and verified to fail appropriately, before implementing any functionality.

## Workflow

1. **Review test changes**: Examine what's being committed
2. **Stage tests only**: Add only test files, no implementation
3. **Verify tests fail**: Run test suite to confirm appropriate failures
4. **Write commit message**: Document what behavior the tests define
5. **Commit**: Create first commit showing test-first approach
6. **Verify staging**: Confirm only tests were committed

## Key Principles

- **Tests first, always**: Separate commits prove TDD discipline
- **Only test files**: No implementation code in this commit
- **Tests must fail**: Passing tests prove nothing at this stage
- **Clear intent**: Commit message documents expected behavior
- **Executable specs**: Tests define the contract implementation must fulfill

## Commit Message Format

```
test(<scope>): add tests for <feature>

<Description of what functionality these tests define>

Test coverage includes:
- <Happy path scenario>
- <Edge case 1>
- <Edge case 2>
- <Error condition>

Tests currently fail (as expected) - implementation follows in next commit.

Tests: <test_name_1>, <test_name_2>, <test_name_3>
```

## Example (Python)

```bash
# Review test changes
git status
git diff tests/

# Stage only tests
git add tests/test_auth.py

# Verify what's staged
git diff --cached

# Verify tests fail
pytest -v
# FAILED tests/test_auth.py::test_registration
# FAILED tests/test_auth.py::test_validation
# (Expected - functions not implemented yet)

# Commit
git commit -m "test(auth): add tests for user registration

Define expected behavior for user registration including validation,
duplicate detection, and secure password handling.

Test coverage includes:
- Valid registration with all required fields
- Email format validation
- Password strength requirements
- Duplicate email detection
- Username constraints

Tests currently fail (as expected) - register_user() not implemented yet.

Tests: test_valid_registration, test_email_validation,
       test_password_strength, test_duplicate_email"

# Verify commit
git log -1 --stat
# test(auth): add tests for user registration
# tests/test_auth.py | 85 +++++++++++++++++++++++
```

## Anti-Patterns

❌ **Committing implementation with tests**:
```bash
git add tests/ src/  # Combined commit hides TDD
```

✅ **Tests first, implementation later**:
```bash
git add tests/
git commit -m "test(feature): add tests"
# (Implementation comes in next commit)
```

❌ **Committing passing tests**:
```bash
pytest -v  # All passing
git commit  # WRONG - tests should fail first
```

✅ **Verify tests fail before commit**:
```bash
pytest -v  # All failing (expected)
git commit  # Now shows TDD discipline
```

❌ **Accidentally staging implementation**:
```bash
git add .  # Stages everything including src/
```

✅ **Stage tests explicitly**:
```bash
git add tests/
git status  # Verify only tests staged
```

## Pre-Commit Verification

```bash
# Only tests staged
git diff --cached
# (Should show only test/ files)

# Tests still fail
pytest -v
# (All tests should fail - no implementation yet)

# No implementation accidentally included
git status
# (Should show implementation as untracked/unstaged)
```

## Common Issues

**Issue: Tests pass unexpectedly**

If tests pass, investigate:
- Are tests importing existing code?
- Are assertions meaningless (e.g., `assert True`)?
- Are tests actually calling the functions?

Fix tests to fail properly before committing.

**Issue: Implementation files staged**

```bash
# Unstage implementation
git reset HEAD src/
git status  # Verify only tests staged
```

## Transition

After committing tests:

1. Verify commit shows only test files: `git show HEAD --name-only`
2. Confirm tests fail appropriately: `pytest -v`
3. Type `/implement` to begin implementation phase

---

**Two commits tell the TDD story: (1) Tests that fail, (2) Implementation that passes. Keep them separate.**
