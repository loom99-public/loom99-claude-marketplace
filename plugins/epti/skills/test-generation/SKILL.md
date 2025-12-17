---
name: test-generation
description: Comprehensive test writing from requirements without implementation code. Use at start of TDD cycle to define expected behavior, edge cases, and acceptance criteria through tests.
---

# Test Generation Skill

## Purpose

Guide test-first development by creating thorough test cases that specify behavior before any implementation exists. Ensures tests are designed independently of implementation details, preventing overfitting and maintaining true TDD discipline.

## When to Use

- Starting TDD cycle (Red phase)
- Defining requirements for new features
- Documenting expected behavior
- Creating regression test suites

## Core Procedure

### Step 1: Understand Requirements

Clarify what needs testing:
- Feature description
- Expected inputs and outputs
- Edge cases and error conditions
- Performance requirements
- Integration points

### Step 2: Structure Tests (Given-When-Then)

Use behavior-driven format:

**Given:** Initial context/setup
**When:** Action performed
**Then:** Expected outcome

Example:
```
Given: User exists with email "alice@example.com"
When: User logs in with correct password
Then: Authentication succeeds, session token returned
```

### Step 3: Identify Test Scenarios

Cover main categories:

**Happy Path:** Normal, successful operation
**Edge Cases:** Boundaries, empty inputs, special characters
**Error Cases:** Invalid inputs, missing data, violations
**Integration:** Dependencies, external services

### Step 4: Write Test Code

Implement tests using Arrange-Act-Assert:

1. **Arrange:** Setup fixtures and test data
2. **Act:** Execute function/method under test
3. **Assert:** Verify expected outcomes
4. Clean up resources if needed

### Step 5: Verify Tests Fail (Red)

Run tests to confirm they fail:
```bash
pytest -v
# All new tests should FAIL (no implementation yet)
```

This confirms tests are valid and actually testing something.

## Key Principles

**Test Behavior, Not Implementation**: Focus on WHAT function does, not HOW. Tests should remain valid even if internal implementation changes.

**One Assert Per Test**: Each test verifies one specific behavior. Makes failures clear and tests maintainable.

**Independent Tests**: Tests don't depend on each other. Can run in any order. No shared state.

**Clear Test Names**: Test name describes scenario. `test_authentication_fails_with_wrong_password` not `test_auth_1`.

**Specification-Driven**: Tests generated from requirements, NOT implementation. Never peek at implementation code when writing tests.

## Example

### pytest (Python) - Authentication System

```python
import pytest
from auth import User, AuthenticationError


class TestUserAuthentication:
    """Test user authentication behavior."""

    def test_authentication_succeeds_with_correct_credentials(self):
        """Given valid credentials, authentication should succeed."""
        # Arrange
        user = User(email="alice@example.com", password="secure123")

        # Act
        result = user.authenticate("secure123")

        # Assert
        assert result is True


    def test_authentication_fails_with_wrong_password(self):
        """Given wrong password, authentication should fail."""
        # Arrange
        user = User(email="alice@example.com", password="secure123")

        # Act
        result = user.authenticate("wrongpass")

        # Assert
        assert result is False


    def test_authentication_raises_error_for_nonexistent_user(self):
        """Given nonexistent user, should raise AuthenticationError."""
        # Arrange / Act / Assert
        with pytest.raises(AuthenticationError, match="User not found"):
            User.authenticate_by_email("nobody@example.com", "anypass")


    def test_user_creation_requires_email(self):
        """Given missing email, user creation should fail."""
        # Arrange / Act / Assert
        with pytest.raises(ValueError, match="Email required"):
            User(email="", password="secure123")


    def test_user_creation_requires_strong_password(self):
        """Given weak password, user creation should fail."""
        # Arrange / Act / Assert
        with pytest.raises(ValueError, match="Password must be at least 8 characters"):
            User(email="alice@example.com", password="weak")
```

### jest (JavaScript) - Order Processing

```javascript
import { processOrder, calculateDiscount } from './orders';

describe('Order Processing', () => {
  test('processes valid order successfully', () => {
    // Arrange
    const order = {
      customerId: 123,
      items: [{ id: 1, price: 50 }],
      total: 50
    };

    // Act
    const result = processOrder(order);

    // Assert
    expect(result.status).toBe('success');
    expect(result.orderId).toBeDefined();
  });

  test('applies 10% discount for orders over $100', () => {
    // Arrange
    const orderTotal = 150;

    // Act
    const discount = calculateDiscount(orderTotal);

    // Assert
    expect(discount).toBe(15); // 10% of 150
  });

  test('throws error when customer ID missing', () => {
    // Arrange
    const invalidOrder = {
      items: [{ id: 1, price: 50 }],
      total: 50
    };

    // Act / Assert
    expect(() => processOrder(invalidOrder)).toThrow('Customer ID required');
  });

  test('throws error when order has no items', () => {
    // Arrange
    const emptyOrder = {
      customerId: 123,
      items: [],
      total: 0
    };

    // Act / Assert
    expect(() => processOrder(emptyOrder)).toThrow('Order must have items');
  });
});
```

### go test (Go) - Email Validator

```go
package validator

import "testing"

func TestValidEmail(t *testing.T) {
    // Arrange
    email := "alice@example.com"

    // Act
    result := IsValidEmail(email)

    // Assert
    if !result {
        t.Errorf("Expected valid email %s to return true", email)
    }
}

func TestInvalidEmailWithoutAtSign(t *testing.T) {
    // Arrange
    email := "aliceexample.com"

    // Act
    result := IsValidEmail(email)

    // Assert
    if result {
        t.Errorf("Expected invalid email %s to return false", email)
    }
}

func TestEmptyEmailIsInvalid(t *testing.T) {
    // Arrange
    email := ""

    // Act
    result := IsValidEmail(email)

    // Assert
    if result {
        t.Error("Expected empty email to return false")
    }
}
```

## Anti-Patterns

❌ **Testing Implementation Details**: `assert user._password_hash == "abc123"`
✅ **Do**: `assert user.authenticate("correct_password") is True`

❌ **Multiple Asserts Testing Different Things**: One test checking email, password, AND creation date
✅ **Do**: Separate tests for each behavior

❌ **Test Dependencies**: test_2 assumes test_1 ran first
✅ **Do**: Each test fully independent with its own setup

❌ **Vague Test Names**: `test_user_1`, `test_case_a`
✅ **Do**: `test_authentication_fails_with_wrong_password`

❌ **Peeking at Implementation**: Writing tests after seeing code
✅ **Do**: Write tests from requirements alone, before implementation

❌ **Hardcoded Test Data**: Magic numbers without context
✅ **Do**: Named constants or fixtures with clear meaning

## Integration

**EPTI Workflow Context:**
- **Stage 1**: This skill generates tests defining requirements
- **Input**: Feature requirements, specifications
- **Output**: Test suite that fails (RED state)
- **Next**: Verify tests fail, then implement

**Typical Flow:**
```
Requirements → Generate tests → Verify RED → Implement → Achieve GREEN
```

**Works With:**
- test-execution: Runs generated tests to verify RED/GREEN states
- implementation-with-protection: Implements code to pass these tests
- overfitting-detection: Ensures tests are valid, not overfitted
