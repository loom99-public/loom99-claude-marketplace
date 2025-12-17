# /verify-fail - Test Failure Verification Stage

## Purpose

Run tests and verify they fail appropriately, proving tests actually test something real.

## When to Use

After writing tests but before committing them, to ensure tests are meaningful.

## Workflow

1. **Run test suite**: Execute tests with appropriate runner
2. **Verify failures**: Confirm all tests fail as expected
3. **Analyze failure reasons**: Check error messages show missing implementation
4. **Document failures**: Record what's failing and why
5. **Investigate passes**: If tests pass, stop and fix tests

## Key Principles

- **Tests must fail first**: Passing tests without implementation prove nothing
- **Failure proves value**: Tests that fail will catch bugs when implemented
- **Expected failures only**: Functions not defined, modules not found
- **No test errors**: Failures should be implementation gaps, not test bugs

## Running Tests

Detect framework and run appropriately:

**Python (pytest)**:
```bash
pytest -v  # Verbose output
pytest tests/test_feature.py  # Specific file
```

**JavaScript (jest)**:
```bash
npm test  # Run all
npm test feature.test.js  # Specific file
```

**Go**:
```bash
go test -v ./...  # All tests
go test -v ./pkg/feature  # Specific package
```

## Expected Output

**Good failures** (implementation missing):
```
FAILED tests/test_auth.py::test_registration
AttributeError: module 'auth' has no attribute 'register_user'

FAILED tests/test_auth.py::test_validation
NameError: name 'validate_email' is not defined
```

These show implementation doesn't exist yet - perfect!

**Bad failures** (investigate):
```
ERROR tests/test_auth.py - ModuleNotFoundError
SyntaxError in test file
ImportError: cannot find module
```

These are test setup issues, not expected TDD failures.

## What If Tests Pass?

**RED FLAG: Tests should NOT pass yet!**

If tests pass unexpectedly, investigate:

### Scenario 1: Testing Existing Code
Tests import and use code that already exists.

**Fix**: Verify test scope, check imports

### Scenario 2: Meaningless Assertions
```python
# Bad - always passes
def test_feature():
    result = some_function()
    assert True  # Always true!
```

**Fix**: Test actual result values

### Scenario 3: Not Calling Code
```python
# Bad - doesn't call function
test('registration', () => {
  // registerUser('test@example.com', 'pass');  // Commented!
  expect(true).toBe(true);  // Meaningless
});
```

**Fix**: Actually call the functions being tested

### Scenario 4: Testing Mocks
Test uses mocks that return fake data instead of real implementation.

**Fix**: Ensure tests call real code, not mocks

## Failure Analysis Example

```markdown
## Test Failure Analysis

**Total tests**: 8
**Failed**: 8 (expected)
**Passed**: 0

**Failure Summary**:
- test_user_registration: register_user() not defined ✓
- test_email_validation: validate_email() not defined ✓
- test_password_validation: validate_password() not defined ✓
- test_duplicate_email: register_user() not defined ✓

**Conclusion**: All failures expected (functions don't exist).
Ready for implementation phase.
```

## Verification Checklist

Before moving forward:
- [ ] Test suite executed successfully
- [ ] All tests failed (as expected)
- [ ] Failure messages show missing implementation
- [ ] No unexpected passes
- [ ] No test setup errors
- [ ] No syntax errors in tests
- [ ] Failure reasons appropriate
- [ ] Test output documented

## Common Issues

**Import Errors**:
```
ModuleNotFoundError: No module named 'myapp.feature'
```

**Fix**: Check module paths, create `__init__.py` (Python), verify package structure

**Test Discovery**:
```
No tests found / 0 tests collected
```

**Fix**: Verify naming (test_*.py, *.test.js, *_test.go), check directory structure

**Syntax Errors**:
```
SyntaxError: invalid syntax
```

**Fix**: Review test code, check indentation, verify brackets/parens

## Transition

Once tests fail appropriately:

1. Document failure analysis
2. Confirm all fail for right reasons
3. Note expected behavior from errors
4. Type `/commit-tests` to commit tests separately

---

**Failing tests are the foundation of TDD. They prove your tests work and will catch bugs. Embrace the failures!**
