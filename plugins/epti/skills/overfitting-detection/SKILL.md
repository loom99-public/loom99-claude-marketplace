---
name: overfitting-detection
description: Identify test-specific hacks and implementation shortcuts that compromise code quality. Use during code review or when implementation seems too tightly coupled to specific test cases.
---

# Overfitting Detection Skill

## Purpose

Identify when code merely passes tests through shortcuts, hardcoding, or test-specific logic rather than implementing real functionality. Ensures implementations solve actual problems, not just satisfy test assertions.

## When to Use

- After implementation passes tests (code review)
- When tests pass suspiciously quickly
- During Green phase verification
- Before committing implementation

## Core Procedure

### Step 1: Understand Overfitting

**Overfitting in TDD:** Code passes tests without implementing real behavior

**Example:**
```python
# OVERFITTED (Bad)
def calculate_tax(amount):
    if amount == 100: return 10
    if amount == 200: return 20
    if amount == 500: return 50
    return 0  # Fails for untested values!

# Tests pass but real usage fails:
calculate_tax(150)  # Returns 0 (wrong!)

# PROPER (Good)
def calculate_tax(amount):
    TAX_RATE = 0.10
    return amount * TAX_RATE

# Tests pass AND real usage works:
calculate_tax(150)  # Returns 15 (correct!)
```

### Step 2: Analyze Test Values

Extract values used in test assertions:

**From Tests:**
```python
# test_tax.py
assert calculate_tax(100) == 10
assert calculate_tax(200) == 20
assert calculate_tax(500) == 50

# Test values: [100, 200, 500, 10, 20, 50]
```

**Check Implementation:**
```python
# implementation.py contains: if amount == 100: return 10
# ⚠️ SUSPICIOUS: Exact test values hardcoded
```

### Step 3: Inspect Logic Patterns

Look for overfitting indicators:

**Hardcoded Test Values:**
- Implementation contains exact values from test assertions
- Conditional branches matching test cases

**Test-Specific Branches:**
- `if` statements for each test scenario
- No general algorithm, only case-by-case handling

**Empty/Stub Logic:**
- Functions that return None or empty for untested cases
- Placeholder implementations

**Magic Numbers:**
- Unexplained constants matching test outputs
- No business logic, just return values

### Step 4: Test with Untested Values

Verify implementation handles values not in tests:

**Technique:**
```python
# Tests use: 100, 200, 500
# Try nearby values: 150, 250, 450

result = calculate_tax(150)
# If result is wrong → overfitted
# If result is correct → likely genuine
```

**Create Verification Tests:**
```python
# Add tests with different values
def test_tax_with_untested_value():
    # Not 100, 200, or 500
    result = calculate_tax(123)
    expected = 123 * 0.10  # 12.3
    assert result == expected
```

### Step 5: Spawn Review Subagent

Use subagent for thorough analysis:

**Subagent Prompt:**
```markdown
You are a code quality reviewer specializing in TDD overfitting detection.

TASK: Analyze this implementation for overfitting to tests.

TESTS: [paste test code]
IMPLEMENTATION: [paste implementation code]

CHECK FOR:
1. Hardcoded test values in implementation
2. Conditional branches matching test cases
3. Logic that only works for tested inputs
4. Missing general algorithm/formula

REPORT:
- Overfitting indicators found
- Specific lines of concern
- Suggested fixes
- Confidence level (Low/Medium/High overfitting risk)
```

## Key Principles

**Real Logic vs Shortcuts**: Implementation should contain business logic/algorithms, not hardcoded case statements.

**Generalization**: Code should handle untested values correctly, not just pass existing tests.

**Algorithm-Driven**: Implementations use formulas, patterns, algorithms. Not case-by-case conditionals.

**Test Independence**: Implementation written without looking at test values. Tests verify behavior, not drive hardcoding.

## Example

### Detecting Overfitting

**Tests:**
```python
def test_discount():
    assert calculate_discount(100) == 5
    assert calculate_discount(500) == 50
    assert calculate_discount(1000) == 150
```

**Overfitted Implementation (BAD):**
```python
def calculate_discount(amount):
    # Hardcoded for each test case
    if amount == 100:
        return 5
    elif amount == 500:
        return 50
    elif amount == 1000:
        return 150
    else:
        return 0  # Untested values fail!
```

**Indicators:**
- ❌ Contains exact test values (100, 500, 1000, 5, 50, 150)
- ❌ Conditional for each test case
- ❌ No discount logic, just returns
- ❌ Fails for 250: `calculate_discount(250)` returns 0

**Proper Implementation (GOOD):**
```python
def calculate_discount(amount):
    # Business logic: tiered discount
    if amount >= 1000:
        return amount * 0.15  # 15% for >= 1000
    elif amount >= 500:
        return amount * 0.10  # 10% for >= 500
    elif amount >= 100:
        return amount * 0.05  # 5% for >= 100
    else:
        return 0
```

**Why It's Proper:**
- ✓ Uses percentages (business logic)
- ✓ Works for untested values: `calculate_discount(250)` returns 12.5 (correct!)
- ✓ No hardcoded test outputs
- ✓ Clear tiered structure

**Verification:**
```python
# Add test for untested value
def test_discount_for_mid_tier():
    result = calculate_discount(250)
    assert result == 12.5  # 5% of 250
    # Passes with proper implementation
    # Fails with overfitted version
```

### Common Overfitting Patterns

**Pattern 1: Direct Return**
```python
# BAD
def get_user_name(user_id):
    if user_id == 1: return "Alice"
    if user_id == 2: return "Bob"
    return None

# GOOD
def get_user_name(user_id):
    user = database.get_user(user_id)
    return user.name if user else None
```

**Pattern 2: Test-Driven Conditionals**
```python
# BAD
def validate_email(email):
    # Only checks test emails!
    if email == "valid@test.com": return True
    if email == "invalid@": return False
    return True  # Default wrong!

# GOOD
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

## Anti-Patterns

❌ **Hardcoding Test Values**: Implementation contains exact values from assertions
✅ **Do**: Use algorithms, calculations, business logic

❌ **Case-by-Case Conditionals**: `if test_value_1: return output_1`
✅ **Do**: General logic that derives outputs from inputs

❌ **Ignoring Overfitting**: "Tests pass, ship it!"
✅ **Do**: Review implementation, test with untested values

❌ **Test-Specific Branches**: `if os.getenv("TESTING"): return fake_data()`
✅ **Do**: Same code path for tests and production

❌ **Incomplete Logic**: Only handles tested scenarios
✅ **Do**: Handle full range of valid inputs

## Integration

**EPTI Workflow Context:**
- **Stage 4**: After implementation passes tests (Green phase)
- **Input**: Passing implementation + test suite
- **Output**: Overfitting risk assessment
- **Next**: Fix overfitting or proceed to refactoring

**Typical Flow:**
```
Tests pass (GREEN) → Detect overfitting → Fix if found → Re-test → Refactor
```

**Works With:**
- implementation-with-protection: Verifies genuine implementation
- test-execution: Re-runs tests after fixing overfitting
- refactoring: Clean up after removing overfitting
