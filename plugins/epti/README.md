# epti Plugin

Evaluate-Plan-Test-Implement: **Strict TDD Discipline Enforced**

**Version**: 0.1.0 | **Status**: Production Ready | **License**: MIT

## Quick Start

```bash
# Install
/marketplace install epti

# TDD workflow
/write-tests      # Write tests first (Red)
/verify-fail      # Confirm tests fail
/commit-tests     # Commit test-only
/implement        # Make tests pass (Green)
/iterate          # Refine if needed
/commit-code      # Commit implementation
```

## Six-Stage TDD Workflow

### 1. Write Tests 📝
**Command**: `/write-tests [feature to test]`

Write comprehensive tests WITHOUT implementation. Define behavior through tests.

**Activities**: Create test files, write assertions, cover edge cases
**Exit**: Test suite written, no implementation code exists

---

### 2. Verify Fail ❌
**Command**: `/verify-fail`

Run tests to confirm they fail properly. Ensures tests are valid.

**Activities**: Execute test suite, confirm RED state, analyze failures
**Exit**: All new tests fail as expected

---

### 3. Commit Tests ✅
**Command**: `/commit-tests`

Commit test-only changes. Separate test commit from implementation.

**Activities**: Stage test files only, write test commit message, push
**Exit**: Tests in git history, implementation not started

---

### 4. Implement 💻
**Command**: `/implement [following tests]`

Write minimal code to pass tests. No shortcuts, no overfitting.

**Activities**: Implement real logic, pass tests, handle edge cases
**Exit**: All tests pass (GREEN state)

---

### 5. Iterate 🔄
**Command**: `/iterate [refine implementation]`

Refactor and polish while maintaining green tests.

**Activities**: Clean code, improve structure, optimize, verify tests still pass
**Exit**: Code clean, tests still passing

---

### 6. Commit Code 📦
**Command**: `/commit-code`

Finalize implementation with proper commit.

**Activities**: Final verification, conventional commit, update docs
**Exit**: Implementation committed, cycle complete

## Core Principles

**Tests First, Always**: No implementation before tests. Tests define requirements.

**Red → Green → Refactor**: Fail tests (Red) → Pass tests (Green) → Clean code (Refactor). Never skip phases.

**No Overfitting**: Implement real logic, not hardcoded test values. Code works for untested inputs too.

**Test Independence**: Each test runs in isolation. No shared state, no test dependencies.

**Protect Test Integrity**: Never modify tests to pass. Implementation adapts to tests.

## Commands Reference

| Command | Stage | Purpose |
|---------|-------|---------|
| `/write-tests` | 1 | Write tests without implementation |
| `/verify-fail` | 2 | Confirm tests fail properly |
| `/commit-tests` | 3 | Commit test-only changes |
| `/implement` | 4 | Make tests pass |
| `/iterate` | 5 | Refactor while green |
| `/commit-code` | 6 | Finalize implementation |

## Skills

- **test-generation**: Behavior-driven test writing
- **test-execution**: Test running and result analysis
- **implementation-with-protection**: Safe TDD implementation
- **overfitting-detection**: Identify test-specific hacks
- **refactoring**: Post-implementation code refinement

## Hooks

- **pre-implementation**: Verify tests defined before coding
- **post-code**: Run test suite after changes
- **pre-commit**: Gate on all tests passing

## Example Workflow

```bash
# Feature: User authentication

/write-tests user can authenticate with valid credentials
# Creates test_auth.py with failing tests

/verify-fail
# Confirms: 5 tests fail as expected

/commit-tests
# test(auth): add authentication test suite

/implement JWT-based authentication following tests
# Implements auth.py to pass tests

/iterate refactor auth code for clarity
# Cleans up while tests stay green

/commit-code
# feat(auth): implement JWT authentication
```

## Framework Support

- **Python**: pytest, unittest
- **JavaScript**: jest, mocha
- **Go**: go test
- **Java**: JUnit
- **Ruby**: RSpec

## TDD Anti-Patterns Prevented

❌ Implementation before tests
❌ Modifying tests to pass
❌ Hardcoding test values
❌ Skipping failing test verification
❌ Overfitting to test cases
❌ Ignoring red phase

✅ Tests first, always
✅ Tests stay sacred
✅ Real logic, not shortcuts
✅ Verify RED before implementing
✅ General solutions
✅ Respect TDD phases

## Integration

Works with:
- Any test framework
- Git workflows
- CI/CD pipelines
- Code review processes
- Pair programming
- TDD training

## Best Practices

1. **Write Tests First**: No exceptions. Define behavior through tests.
2. **Verify Fail**: Always confirm RED state before implementing.
3. **Separate Commits**: Test commit, then implementation commit.
4. **Real Logic**: No hardcoded test values. Solve actual problem.
5. **Refactor Fearlessly**: Tests provide safety net for refactoring.

## When to Use

**Use epti when**:
- Building new features
- Learning TDD discipline
- Ensuring test coverage
- Team enforcing TDD
- Quality-critical code

**Not suitable for**:
- Exploratory prototypes
- Spike solutions
- Legacy code (no tests yet)
- Simple scripts

## Overfitting Detection

Plugin automatically detects:
- Hardcoded test values in implementation
- Conditional branches matching test cases
- Test-specific logic branches
- Implementations that only work for tested inputs

Ensures genuine solutions, not test-passing hacks.

## Configuration

No configuration required. Works out of the box with auto-detected test framework.

## Support

- **Documentation**: See `skills/` directory
- **Issues**: GitHub repository
- **Author**: Brandon Fryslie
- **License**: MIT

## Version History

- **0.1.0** (Current): Initial release with full TDD workflow
