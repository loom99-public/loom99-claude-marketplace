---
name: implementation-with-protection
description: Safe code implementation following TDD principles with safeguards against overfitting. Use when implementing code to pass existing tests while maintaining clean, general-purpose solutions.
---

# Implementation with Protection Skill

## Purpose

Guide implementation that satisfies test requirements without modifying tests or compromising TDD discipline. Ensures code is written to meet specifications, not to make tests easier to pass.

## When to Use

- Implementing code to pass failing tests (Red → Green)
- Green phase of TDD cycle
- When tests defined and verified as failing
- After test generation complete

## Core Procedure

### Step 1: Understand Test Requirements

Analyze failing tests to extract requirements:

**Read Test Code:**
```python
def test_authenticate_valid_credentials():
    result = authenticate("alice@example.com", "SecurePass123!")
    assert result.is_authenticated is True
    assert result.token is not None
    assert len(result.token) == 64
```

**Extract Requirements:**
1. Function: `authenticate(email, password)`
2. Returns object with `is_authenticated` property (bool)
3. Returns object with `token` property (string)
4. Token is 64 characters long
5. Valid credentials → authenticated + token present

**Understand Intent:**
Not just "make assertions pass". Understand business logic: Authentication needs secure token generation, likely SHA-256 or JWT.

### Step 2: Implement Incrementally

Make smallest change to progress toward passing tests:

**Start Simple:**
1. Create function signature
2. Add basic structure
3. Implement core logic
4. Handle edge cases
5. Add error handling

**Run Tests Frequently:**
After each small change, run tests to see progress.

### Step 3: Write Real Logic (No Shortcuts)

Implement genuine business logic:

**GOOD Implementation:**
```python
import hashlib
import secrets

class AuthResult:
    def __init__(self, is_authenticated, token=None):
        self.is_authenticated = is_authenticated
        self.token = token

def authenticate(email, password):
    # Real logic: Check credentials
    user = database.find_user_by_email(email)

    if not user:
        return AuthResult(is_authenticated=False)

    if not user.verify_password(password):
        return AuthResult(is_authenticated=False)

    # Generate secure token
    token = secrets.token_hex(32)  # 32 bytes = 64 hex chars

    return AuthResult(is_authenticated=True, token=token)
```

**BAD Implementation (Overfitted):**
```python
def authenticate(email, password):
    # Hardcoded for test!
    if email == "alice@example.com" and password == "SecurePass123!":
        return AuthResult(True, "x" * 64)
    return AuthResult(False)
```

### Step 4: Verify Tests Pass

Run test suite:
```bash
pytest -vv
# All tests should now pass
```

If tests still fail:
- Analyze failure messages
- Fix implementation (NOT tests)
- Re-run tests
- Repeat until green

### Step 5: Never Modify Tests

**Tests are sacred** - implementation adapts to tests, not vice versa.

**Don't:**
- ❌ Weaken assertions: `assert len(token) >= 60` (was == 64)
- ❌ Skip failing tests: `@pytest.skip("Too hard")`
- ❌ Change expected values: `assert result is False` (was True)
- ❌ Remove error checks: Delete test for edge case

**Do:**
- ✅ Implement code that satisfies ALL assertions
- ✅ Handle ALL test scenarios
- ✅ Fix implementation when tests fail
- ✅ Ask for clarification if test seems wrong

**Exception:** Test has genuine bug. Document issue, get approval, then fix test.

## Key Principles

**Tests Are Sacred**: Never modify tests during implementation. Implementation adapts to tests. Tests define requirements.

**Implement to Specification**: Solve actual problem, not just pass tests. Handle real-world scenarios, not just test cases.

**Red → Green → Refactor**: Tests fail (Red) → Implement (Green) → Clean up (Refactor). Never skip phases.

**No Overfitting**: Use algorithms and business logic. No hardcoded test values. Code works for untested inputs too.

**Incremental Progress**: Small steps. Run tests frequently. One failing test → partially passing → fully passing.

## Example

### Authentication Implementation

**Tests (Given):**
```python
def test_valid_credentials():
    result = authenticate("alice@example.com", "password123")
    assert result.is_authenticated is True
    assert result.token is not None

def test_invalid_password():
    result = authenticate("alice@example.com", "wrongpass")
    assert result.is_authenticated is False
    assert result.token is None

def test_nonexistent_user():
    result = authenticate("nobody@example.com", "anypass")
    assert result.is_authenticated is False
```

**Step-by-Step Implementation:**

**Iteration 1: Create structure**
```python
class AuthResult:
    def __init__(self, is_authenticated, token=None):
        self.is_authenticated = is_authenticated
        self.token = token

def authenticate(email, password):
    # Stub - all tests fail
    return AuthResult(False)
```
Run tests: 1 pass, 2 fail

**Iteration 2: Add user lookup**
```python
def authenticate(email, password):
    user = database.find_user_by_email(email)
    if not user:
        return AuthResult(False)
    # Not checking password yet
    return AuthResult(False)
```
Run tests: Still 1 pass, 2 fail

**Iteration 3: Check password**
```python
def authenticate(email, password):
    user = database.find_user_by_email(email)
    if not user:
        return AuthResult(False)

    if user.verify_password(password):
        token = generate_secure_token()
        return AuthResult(True, token)
    else:
        return AuthResult(False)
```
Run tests: All pass!

**What We Did Right:**
- ✓ Used real database lookup
- ✓ Used password verification method
- ✓ Generated secure token
- ✓ Handled all three scenarios
- ✓ Never modified tests

### Bad Example (What NOT to Do)

**Overfitted Implementation:**
```python
def authenticate(email, password):
    # Hardcoded for specific test!
    if email == "alice@example.com" and password == "password123":
        return AuthResult(True, "fake_token_" + "x" * 53)  # 64 chars

    return AuthResult(False)
```

**Problems:**
- ❌ Hardcoded test email
- ❌ Hardcoded test password
- ❌ Fake token, not secure
- ❌ Won't work for other valid users
- ❌ No database integration
- ❌ No password verification

## Anti-Patterns

❌ **Modifying Tests**: Changing assertions to match buggy implementation
✅ **Do**: Fix implementation to satisfy original tests

❌ **Hardcoding**: `if input == test_value: return test_output`
✅ **Do**: Implement algorithm that derives outputs from inputs

❌ **Skipping Tests**: `@pytest.skip` or `.skip()` on failing tests
✅ **Do**: Implement code that makes tests pass

❌ **Test-Specific Branches**: `if os.getenv("TEST"): return fake_data()`
✅ **Do**: Same code for test and production

❌ **Shortcuts**: Return None/empty to pass tests quickly
✅ **Do**: Implement proper logic even if more complex

❌ **Ignoring Intent**: Just make assertions pass, miss business logic
✅ **Do**: Understand requirements behind tests

## Integration

**EPTI Workflow Context:**
- **Stage 4**: Implementation phase (Red → Green)
- **Input**: Failing test suite (Red state)
- **Output**: Working implementation (Green state)
- **Next**: Overfitting detection, then refactoring

**Typical Flow:**
```
Tests fail (RED) → Implement with protection → Tests pass (GREEN) → Detect overfitting → Refactor
```

**Works With:**
- test-generation: Implements code to pass generated tests
- test-execution: Runs tests to verify implementation
- overfitting-detection: Ensures implementation is genuine
- refactoring: Cleans up after implementation passes
