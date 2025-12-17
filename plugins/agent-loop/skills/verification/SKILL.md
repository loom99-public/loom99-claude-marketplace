---
name: verification
description: Code and test verification including running test suites, checking builds, and validating implementations. Use after code changes to ensure correctness, catch regressions, and verify acceptance criteria.
---

# Implementation Verification Skill

## Purpose

Systematically verify that implementation matches the plan, handles edge cases, meets quality standards, and is ready for commit. Prevents premature commits and catches issues before code review.

## When to Use

- Before transitioning from `/code` to `/commit`
- After completing feature implementation
- Before creating pull request
- When unsure if implementation complete
- As part of pre-commit automation

## Core Procedure

### Step 1: Verify Plan Alignment

Check implementation matches plan:
- All planned files created/modified
- Architecture follows design
- All planned steps completed
- Deviations documented with rationale

### Step 2: Run Tests

Execute test suite:
```bash
# Python
pytest -v

# JavaScript
npm test

# Go
go test ./...

# Java
mvn test  # or gradle test

# Ruby
rspec spec/
```

**Verify:**
- All tests pass (0 failures)
- No test errors
- Expected tests executed (count matches)
- Coverage adequate (if tracked)

### Step 3: Check Code Quality

Run linting and formatting:
```bash
# Python
pylint src/
black --check src/

# JavaScript
eslint src/
prettier --check src/

# Go
go vet ./...
gofmt -l .
```

**Verify:**
- No linting errors
- Formatting consistent
- No warnings (or documented)
- Type checks pass (if typed language)

### Step 4: Build Verification

Ensure project builds:
```bash
# Varies by project
make build
# or
npm run build
# or
go build
```

**Verify:**
- Build succeeds with no errors
- No compilation warnings
- Dependencies resolved
- Artifacts generated correctly

### Step 5: Edge Case Check

Review implementation for common issues:

**Checklist:**
- [ ] Null/None/undefined handling
- [ ] Empty collection handling
- [ ] Boundary values (0, negative, max)
- [ ] Error conditions caught
- [ ] Required fields validated
- [ ] Resource cleanup (files, connections)

### Step 6: Acceptance Criteria

Verify plan acceptance criteria met:

**For each criterion:**
1. Locate in plan
2. Test manually or automated
3. Confirm satisfied
4. Document result

**Example:**
```
Criterion: "API returns 401 for invalid token"
Test: curl with bad token
Result: ✓ Returns 401 Unauthorized
```

### Step 7: Final Checklist

Pre-commit checklist:
- [ ] All tests pass
- [ ] Code quality checks pass
- [ ] Build succeeds
- [ ] Edge cases handled
- [ ] Acceptance criteria met
- [ ] Documentation updated (if needed)
- [ ] No debug code left (console.log, print statements)
- [ ] No commented-out code blocks

## Key Principles

**Test Before Commit**: Never commit without running tests. Failing tests block commits.

**Comprehensive Verification**: Check tests, quality, build, edge cases. One dimension isn't enough.

**Plan as Contract**: Acceptance criteria from plan are the definition of "done".

**Fail Fast**: Stop at first verification failure. Fix before proceeding.

**Document Deviations**: If implementation differs from plan, document why. Don't silently diverge.

## Example

### Authentication Feature Verification

**Plan Acceptance Criteria:**
1. POST /api/auth/login accepts email + password
2. Returns JWT token for valid credentials
3. Returns 401 for invalid credentials
4. Token valid for 24 hours
5. Token can access protected routes

**Verification Process:**

**Step 1: Plan Alignment**
```
✓ Created src/auth.py (planned)
✓ Created tests/test_auth.py (planned)
✓ Modified src/api/routes.py (planned)
✓ Used JWT library as specified
✓ No unplanned deviations
```

**Step 2: Run Tests**
```bash
$ pytest -v tests/test_auth.py

tests/test_auth.py::test_valid_login PASSED       [20%]
tests/test_auth.py::test_invalid_password PASSED  [40%]
tests/test_auth.py::test_nonexistent_user PASSED  [60%]
tests/test_auth.py::test_token_expiration PASSED  [80%]
tests/test_auth.py::test_protected_route PASSED   [100%]

5 passed in 0.42s

✓ All tests pass
✓ Expected 5 tests, ran 5
```

**Step 3: Code Quality**
```bash
$ pylint src/auth.py
Your code has been rated at 10.00/10

$ black --check src/
All done! ✨ 🍰 ✨
1 file would be left unchanged.

✓ Linting clean
✓ Formatting consistent
```

**Step 4: Build Verification**
```bash
$ python -m py_compile src/auth.py
# No output = successful compilation

✓ No syntax errors
✓ Imports resolve
```

**Step 5: Edge Cases**
```
✓ Empty email handled → ValidationError
✓ Empty password handled → ValidationError
✓ Very long password (1000 chars) → Works correctly
✓ Special chars in email → Works correctly
✓ Database connection failure → Error caught and logged
```

**Step 6: Acceptance Criteria**
```
Criterion 1: Login endpoint accepts email + password
Manual test: curl -X POST /api/auth/login -d '{"email":"test@example.com","password":"pass123"}'
Result: ✓ Endpoint works

Criterion 2: Returns JWT for valid credentials
Result: ✓ Token returned in response.token

Criterion 3: Returns 401 for invalid credentials
Manual test: curl with wrong password
Result: ✓ Returns 401 Unauthorized

Criterion 4: Token valid for 24 hours
Result: ✓ Token expiration set to now + 24h

Criterion 5: Token can access protected routes
Manual test: curl /api/user/profile with token
Result: ✓ Access granted
```

**Step 7: Final Checklist**
```
✓ All tests pass (5/5)
✓ Code quality checks pass
✓ Build succeeds
✓ Edge cases handled (5 scenarios)
✓ Acceptance criteria met (5/5)
✓ README updated with new endpoint
✓ No print() statements left
✓ No commented code

VERIFICATION COMPLETE ✓
Ready to commit
```

## Anti-Patterns

❌ **Skip Tests**: "I'll run tests later"
✅ **Do**: Run tests before every commit

❌ **Ignore Failures**: "One failing test is fine"
✅ **Do**: Fix all failures before committing

❌ **Manual-Only Testing**: No automated tests
✅ **Do**: Automated tests for regressions

❌ **No Edge Case Check**: Only test happy path
✅ **Do**: Verify error conditions, boundaries, edge cases

❌ **Build Later**: Commit without checking build
✅ **Do**: Ensure project builds before commit

❌ **Partial Verification**: Only check one dimension
✅ **Do**: Comprehensive verification (tests + quality + build + criteria)

## Integration

**Agent Loop Context:**
- **Stage 3**: Verification after coding, before committing
- **Input**: Completed implementation + plan
- **Output**: Verified implementation or list of issues
- **Next**: If pass → commit, if fail → back to coding

**Typical Flow:**
```
Explore → Plan → Code → Verify (this skill) → If ✓ Commit, If ✗ Fix & Verify
```

**Works With:**
- plan-generation: Defines acceptance criteria to verify
- git-operations: Verified code is ready for commit
- code-exploration: Failed verification may need more exploration
