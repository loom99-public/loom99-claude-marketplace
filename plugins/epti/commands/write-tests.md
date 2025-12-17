# /write-tests - Test Writing Stage

## Purpose

Write comprehensive tests that define expected behavior BEFORE implementing any code. Tests are executable specifications.

## When to Use

At the start of any new feature or functionality, before writing any implementation.

## Workflow

1. **Understand requirements**: Read requirements, ask questions about unclear aspects
2. **Choose framework**: Detect or confirm test framework (pytest/jest/go test)
3. **Write test cases**: Cover happy path, edge cases, boundaries, errors
4. **Structure tests**: Use AAA pattern (Arrange, Act, Assert)
5. **Ensure independence**: Each test runs standalone
6. **Verify completeness**: All requirements have test coverage

## Key Principles

- **ABSOLUTELY NO IMPLEMENTATION**: Write ONLY test code in this stage
- **Tests first, always**: Define behavior before implementation
- **Comprehensive coverage**: Happy path + edge cases + errors
- **Clear test names**: Describe exactly what they verify
- **Independent tests**: No test depends on another

## Critical Rules

**You are writing TESTS ONLY**. Do not:
- Write any implementation code
- Create stub functions or classes
- Modify existing implementation
- Write mock implementations

**ONLY write test code** that will fail until real implementation exists.

## Test Framework Examples

**Python (pytest)**:
```python
import pytest
from myapp.auth import register_user, validate_email

def test_valid_registration():
    """User can register with valid data"""
    user = register_user("test@example.com", "Pass123!", "testuser")
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.is_active == True

def test_empty_email_raises_error():
    """Registration fails with empty email"""
    with pytest.raises(ValueError, match="Email cannot be empty"):
        register_user("", "Pass123!", "testuser")

def test_duplicate_email():
    """Registration fails if email exists"""
    register_user("test@example.com", "Pass123!", "user1")
    with pytest.raises(ValueError, match="Email already registered"):
        register_user("test@example.com", "Pass123!", "user2")
```

**JavaScript (jest)**:
```javascript
const { registerUser } = require('./auth');

describe('User Registration', () => {
  test('registers user with valid data', () => {
    const user = registerUser('test@example.com', 'Pass123!', 'testuser');
    expect(user.email).toBe('test@example.com');
    expect(user.username).toBe('testuser');
  });

  test('throws error for empty email', () => {
    expect(() => {
      registerUser('', 'Pass123!', 'testuser');
    }).toThrow('Email cannot be empty');
  });
});
```

**Go**:
```go
func TestValidRegistration(t *testing.T) {
    user := RegisterUser("test@example.com", "Pass123!", "testuser")
    if user.Email != "test@example.com" {
        t.Errorf("expected email %v, got %v", "test@example.com", user.Email)
    }
}

func TestEmptyEmail(t *testing.T) {
    _, err := RegisterUser("", "Pass123!", "testuser")
    if err == nil {
        t.Error("expected error for empty email")
    }
}
```

## Test Coverage Types

**Happy Path**:
```python
def test_valid_user_registration():
    user = register_user("test@example.com", "SecurePass123!", "testuser")
    assert user.email == "test@example.com"
```

**Edge Cases**:
```python
def test_password_minimum_length():
    with pytest.raises(ValueError, match="Password must be at least 8 characters"):
        register_user("test@example.com", "short", "testuser")
```

**Boundaries**:
```python
def test_username_exactly_min_length():
    user = register_user("test@example.com", "Pass123!", "abc")
    assert user.username == "abc"

def test_username_exactly_max_length():
    username = "a" * 20
    user = register_user("test@example.com", "Pass123!", username)
    assert user.username == username
```

**Error Conditions**:
```python
def test_invalid_email_format():
    with pytest.raises(ValueError, match="Invalid email format"):
        register_user("notanemail", "Pass123!", "testuser")
```

## Test Structure (AAA Pattern)

```python
def test_feature():
    # Arrange - Set up test data
    input_data = {"name": "test", "value": 42}
    expected = "processed: test=42"

    # Act - Execute the code being tested
    result = process_data(input_data)

    # Assert - Verify the result
    assert result == expected
```

## Test Naming

✅ **Good** (clear and descriptive):
- `test_user_registration_with_valid_data`
- `test_empty_password_raises_validation_error`
- `test_calculate_discount_returns_correct_percentage`
- `test_api_returns_404_for_nonexistent_resource`

❌ **Bad** (vague):
- `test_user`
- `test1`
- `test_it_works`
- `test_stuff`

## Test Independence

```python
# Good - independent tests
def test_create_user():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"

def test_delete_user():
    user = create_user("delete@example.com")
    delete_user(user.id)
    assert get_user(user.id) is None

# Bad - tests depend on each other (DON'T DO THIS)
# global user
# def test_create():
#     user = create_user("test@example.com")
# def test_delete():
#     delete_user(user.id)  # Depends on previous test!
```

## Setup and Teardown

**pytest fixtures**:
```python
@pytest.fixture
def sample_user():
    """Create test user for each test"""
    user = create_user("test@example.com", "password123")
    yield user
    delete_user(user.id)  # Cleanup

def test_user_login(sample_user):
    result = login(sample_user.email, "password123")
    assert result.success == True
```

**jest hooks**:
```javascript
describe('User tests', () => {
  let testUser;

  beforeEach(() => {
    testUser = createUser('test@example.com', 'password123');
  });

  afterEach(() => {
    deleteUser(testUser.id);
  });

  test('user can login', () => {
    const result = login(testUser.email, 'password123');
    expect(result.success).toBe(true);
  });
});
```

## Anti-Patterns

❌ **Writing implementation**:
```python
# WRONG - implementation code!
def register_user(email, password, username):
    return User(email=email, password=password, username=username)
```

❌ **Creating stubs**:
```python
# WRONG - stub implementation
def register_user(email, password, username):
    pass  # Incomplete stub
```

❌ **Tests that pass immediately**:
```python
# WRONG - meaningless test
def test_always_passes():
    assert True
```

## Pre-Transition Checklist

- [ ] All requirements have test coverage
- [ ] Happy path tested
- [ ] Edge cases tested
- [ ] Error conditions tested
- [ ] Boundary values tested
- [ ] Test names descriptive
- [ ] Tests independent
- [ ] AAA pattern followed
- [ ] NO implementation code written
- [ ] NO stub functions created

## Transition

Once tests are comprehensive:

1. Review all test cases
2. Ensure NO implementation written
3. Verify tests clear and maintainable
4. Type `/verify-fail` to run tests and confirm failures

---

**The quality of your tests determines the quality of your implementation. Invest time in writing thorough tests.**
