---
name: test-execution
description: Test running and result analysis across multiple testing frameworks. Use to verify test failures, validate implementations, and interpret test output.
---

# Test Execution Skill

## Purpose

Execute tests systematically, interpret results accurately, and provide actionable feedback. Ensures tests run correctly, failures are understood, and progress toward passing tests is measurable.

## When to Use

- Verifying tests fail before implementation (Red phase)
- Checking tests pass after implementation (Green phase)
- Running tests during refactoring (Green → Green)
- Debugging test failures or errors

## Core Procedure

### Step 1: Detect Test Framework

Examine project indicators:

**Common indicators:**
- Config files: pytest.ini, jest.config.js, go.mod, pom.xml, .rspec
- Package manifests: package.json, requirements.txt, Gemfile, build.gradle
- Test file patterns: test_*.py, *.test.js, *_test.go, *Test.java, *_spec.rb

### Step 2: Execute Tests with Appropriate Flags

**Example execution patterns:**

```bash
# Python testing
pytest -vv                    # Very verbose output
pytest -x                     # Stop on first failure
pytest tests/test_auth.py     # Specific file

# JavaScript testing
npm test -- --verbose         # Verbose output
npm test auth.test.js         # Specific file
npm test -- --watch           # Watch mode

# Other common patterns
go test -v ./...              # Verbose all packages
mvn test                      # Maven projects
gradle test                   # Gradle projects
rspec --format documentation  # Ruby detailed output
```

### Step 3: Parse Test Results

Extract key information:

**Success Metrics:**
- Total tests run
- Pass count
- Fail count
- Skip count
- Execution time

**Failure Details:**
- Which tests failed
- Assertion errors
- Expected vs actual values
- Stack traces
- Error messages

### Step 4: Interpret Results

**All Tests Pass:**
```
✓ 45 passed in 2.3s
Status: GREEN - Implementation correct
Action: Proceed to refactoring or completion
```

**Some Tests Fail:**
```
✗ 3 failed, 42 passed in 2.5s

Failed tests:
- test_auth.py::test_invalid_password: AssertionError: False is not true
- test_auth.py::test_missing_user: AttributeError: 'NoneType' object has no attribute 'username'
- test_user.py::test_create_user: ValidationError: Email required

Status: RED - Implementation incomplete/incorrect
Action: Analyze failures and fix implementation
```

**Test Errors (Not Failures):**
```
✗ 5 errors

Errors:
- ImportError: No module named 'auth'
- SyntaxError: invalid syntax on line 23

Status: ERROR - Configuration or syntax issues
Action: Fix errors before implementing
```

### Step 5: Provide Actionable Feedback

For each failure, identify:

**Assertion Failures:**
- What was expected
- What was actual
- Why they differ

**Runtime Errors:**
- Error type (AttributeError, ValueError, etc.)
- Where error occurred
- Likely cause

**Next Steps:**
- Specific code changes needed
- Which function/method to fix
- What logic is missing or wrong

## Key Principles

**Framework Detection**: Automatically identify test framework from project structure. Don't assume or hardcode.

**Comprehensive Execution**: Run ALL tests, not just one. Capture full output including failures, errors, and warnings.

**Accurate Interpretation**: Distinguish between test failures (wrong behavior), errors (broken code), and skips (ignored tests).

**Actionable Feedback**: Parse failures to identify exactly what needs fixing. Provide specific guidance, not just "tests fail".

**Track Progress**: Count pass/fail ratios. Monitor progress toward all tests passing. Celebrate improvements.

## Example

### Test Execution and Interpretation

**Command:**
```bash
pytest -vv
```

**Output:**
```
============================= test session starts ==============================
tests/test_auth.py::test_valid_credentials PASSED                        [ 11%]
tests/test_auth.py::test_invalid_password FAILED                         [ 22%]
tests/test_auth.py::test_missing_user FAILED                             [ 33%]
tests/test_user.py::test_create_user PASSED                              [ 44%]
tests/test_user.py::test_update_user PASSED                              [ 55%]

=================================== FAILURES ===================================
_______________________ test_invalid_password ______________________

    def test_invalid_password():
        user = User("alice@example.com", "correct_password")
>       assert not user.authenticate("wrong_password")
E       AssertionError: assert not True
E        +  where True = <bound method User.authenticate of <User object>>('wrong_password')

tests/test_auth.py:15: AssertionError

_______________________ test_missing_user ______________________

    def test_missing_user():
        result = find_user("nonexistent@example.com")
>       assert result is None
E       AssertionError: assert {'email': 'nonexistent@example.com', 'error': 'not found'} is None

tests/test_auth.py:22: AssertionError

========================== short test summary info ==========================
FAILED tests/test_auth.py::test_invalid_password - AssertionError
FAILED tests/test_auth.py::test_missing_user - AssertionError
========================== 2 failed, 3 passed in 0.45s ==========================
```

**Interpretation:**
```markdown
TEST EXECUTION RESULTS:

Status: RED (2 failures, 3 passed)
Success rate: 60% (3 of 5)

FAILURES ANALYSIS:

1. test_invalid_password (Line 15)
   - Issue: authenticate() returns True for wrong password
   - Expected: False (authentication should fail)
   - Actual: True (authentication succeeded)
   - Root cause: Password validation logic missing or incorrect
   - Fix needed: Implement proper password comparison in User.authenticate()

2. test_missing_user (Line 22)
   - Issue: find_user() returns dict instead of None for nonexistent user
   - Expected: None
   - Actual: {'email': 'nonexistent@example.com', 'error': 'not found'}
   - Root cause: Function returns error dict instead of None
   - Fix needed: Return None when user not found, not error dict

PASSING TESTS:
✓ test_valid_credentials
✓ test_create_user
✓ test_update_user

NEXT STEPS:
1. Fix User.authenticate() to properly validate passwords
2. Fix find_user() to return None (not error dict) for missing users
3. Re-run tests to verify fixes
```

### Alternative Framework Example

**Command:**
```bash
npm test -- --verbose
```

**Output:**
```
 PASS  tests/auth.test.js
  ✓ authenticates valid credentials (12 ms)
  ✓ rejects invalid password (8 ms)

 FAIL  tests/user.test.js
  ✓ creates new user (15 ms)
  ✗ validates required email (3 ms)

  ● validates required email

    expect(received).toThrow()

    Received function did not throw

      10 |   test('validates required email', () => {
      11 |     expect(() => {
    > 12 |       createUser({ name: 'Alice' });
         |       ^
      13 |     }).toThrow('Email required');
      14 |   });

Tests: 1 failed, 3 passed, 4 total
```

**Interpretation:**
```markdown
TEST EXECUTION RESULTS:

Status: RED (1 failure, 3 passed)
Success rate: 75% (3 of 4)

FAILURE ANALYSIS:

1. validates required email (Line 12)
   - Issue: createUser() doesn't throw error when email missing
   - Expected: Function throws 'Email required' error
   - Actual: Function completes without throwing
   - Root cause: Missing validation logic for required email
   - Fix needed: Add email validation that throws error if email absent

NEXT STEPS:
1. Add validation to createUser() function
2. Check for email presence
3. Throw error with message 'Email required' if missing
4. Re-run tests
```

## Anti-Patterns

❌ **Running Single Test**: Only testing one function, missing integration failures
✅ **Do**: Run full test suite to catch all issues

❌ **Ignoring Errors**: "It's just an import error, I'll fix later"
✅ **Do**: Fix errors immediately, they block testing

❌ **No Interpretation**: Just showing raw test output without explanation
✅ **Do**: Parse results and provide actionable analysis

❌ **Vague Feedback**: "Tests fail, fix your code"
✅ **Do**: "test_auth line 15: authenticate() returns True for wrong password, should return False"

❌ **Not Tracking Progress**: Losing sight of how many tests remain
✅ **Do**: Monitor pass/fail count, celebrate progress (3→4→5 passing)

## Integration

**EPTI Workflow Context:**
- **Stage 2**: Verify tests fail (Red phase)
- **Stage 4**: Check tests pass (Green phase)
- **Stage 6**: Verify tests still pass during refactoring

**Typical Usage:**
```
Write tests → Execute (verify RED) → Implement → Execute (achieve GREEN) → Refactor → Execute (maintain GREEN)
```

**Works With:**
- test-generation: Executes generated tests
- implementation-with-protection: Verifies implementation passes tests
- overfitting-detection: Identifies suspicious test passes
- refactoring: Ensures refactoring doesn't break tests
