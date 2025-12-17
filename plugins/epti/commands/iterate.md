# /iterate - Test Iteration Stage

Activates the ITERATE stage of tdd-agent.md: Run tests, analyze failures, refine implementation until all pass.

## Purpose

Fix implementation (NOT tests) to satisfy test requirements through iterative refinement. Maintain test integrity while improving code.

## Workflow

```
1. Run tests → 2. Analyze failures → 3. Fix implementation → 4. Repeat until green
```

Key rule: Fix implementation to pass tests, never modify tests to pass implementation.

## Process

### 1. Run Test Suite

```bash
# Adapt to your framework:
pytest -v              # Python
npm test               # JavaScript
go test ./... -v       # Go
mvn test               # Java
bundle exec rspec      # Ruby
```

### 2. Analyze Results

**Focus on**:
- Failed test count
- Failure messages
- Expected vs actual values
- Stack traces pointing to issues

### 3. Fix Implementation

Apply fixes systematically:

**Priority**:
1. Logic errors (wrong algorithm)
2. Missing functionality (not implemented)
3. Edge case handling (boundary conditions)
4. Error handling (exceptions, validation)

**Example Fix**:
```python
# Test expects: validate_email("invalid") -> False

# Before (fails):
def validate_email(email):
    return True  # Always returns True

# After (passes):
def validate_email(email):
    return "@" in email and "." in email.split("@")[1]
```

### 4. Re-Run Tests

After each fix, run tests again to verify improvement.

### 5. Iterate Until Green

Typical iteration count: 2-5 cycles
- Cycle 1: 10 failing → 6 failing
- Cycle 2: 6 failing → 2 failing
- Cycle 3: 2 failing → 0 failing (all pass)

## Key Principles

1. **Fix Implementation**: Never modify tests to make them easier
2. **One Issue at a Time**: Address one failure, re-run, repeat
3. **Understand Failures**: Read error messages carefully
4. **Maintain Quality**: Don't work around tests with special cases
5. **Track Progress**: Document what changed and why

## Anti-Patterns

❌ **Modifying Tests**: Changing test expectations to match broken code
✅ **Fixing Code**: Adjusting implementation to meet test requirements

❌ **Hardcoding Test Data**: `if input == "test@example.com": return True`
✅ **Real Logic**: Implement actual validation logic

❌ **Skipping Tests**: Commenting out failing tests
✅ **Fixing Issues**: Address root cause of failures

❌ **Rushing**: Making random changes hoping something works
✅ **Systematic**: Understand failure, apply targeted fix, verify

## Troubleshooting

**Many failures**: Start with simplest/first failure, work systematically

**Flaky tests**: Ensure tests are deterministic, fix test environment issues

**Unclear failures**: Add debugging output, use debugger, inspect values

**One test breaks another**: Check for shared state, ensure test isolation

## Success Criteria

- ✅ All tests passing
- ✅ No tests modified (except legitimate bugs)
- ✅ Implementation satisfies requirements
- ✅ No hardcoded test-specific values
- ✅ Code quality maintained
- ✅ Ready for `/commit-code`

## Transition

**Next**: `/commit-code` (finalize implementation with passing tests)

See tdd-agent.md ITERATE stage for full guidance.
