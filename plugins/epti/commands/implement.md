# /implement - Implementation Stage

## Purpose

Write the simplest code that makes all tests pass without modifying test assertions.

## When to Use

After tests are written, verified to fail, and committed separately.

## Workflow

1. **Review test requirements**: Understand what tests expect
2. **Implement signatures**: Create function/class skeletons
3. **Implement happy path**: Start with main success scenario
4. **Handle edge cases**: Add logic for boundary conditions
5. **Handle errors**: Implement proper error handling
6. **Run tests continuously**: Verify progress after each change

## Key Principles

- **Tests define the contract**: NEVER modify test assertions
- **Simplest solution wins**: Implement only what tests require (KISS, YAGNI)
- **No untested features**: Don't add functionality beyond tests
- **Quality matters**: Clean, readable, maintainable code
- **Tests are truth**: If tests fail, fix implementation (not tests)

## Critical Rules

During implementation:
- ❌ **NEVER** modify test assertions
- ❌ **NEVER** comment out failing tests
- ❌ **NEVER** skip or weaken tests
- ❌ **NEVER** add untested features
- ✅ **ALWAYS** fix implementation to pass tests
- ✅ **ONLY** implement what tests require

## Implementation Approach

### 1. Understand Test Requirements

```python
# Analyze each test to extract requirements
def test_valid_email():
    assert validate_email("user@example.com") == True

# Requirements:
# - Function: validate_email()
# - Parameter: email (string)
# - Returns: boolean
# - Behavior: Accept valid email format
```

### 2. Start Simple (Happy Path)

```python
def validate_email(email):
    """Validate email format"""
    if "@" in email and "." in email:
        return True
    raise ValueError("Invalid email format")
```

### 3. Add Edge Cases

```python
def validate_email(email):
    """Validate email format"""
    if not email:
        raise ValueError("Email cannot be empty")
    if " " in email:
        raise ValueError("Invalid email format")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Invalid email format")
    return True
```

### 4. Handle Errors Properly

```python
def register_user(email, password, username):
    """Register new user with validation"""
    # Validate inputs (tests require this)
    validate_email(email)
    validate_password(password)
    validate_username(username)

    # Check duplicates (tests require this)
    if user_exists(email):
        raise ValueError("Email already registered")

    # Create user
    user = User(
        email=email,
        password=hash_password(password),
        username=username
    )
    save_user(user)
    return user
```

## Code Quality Standards

**Clear naming**:
```python
# Good
def calculate_order_total(items, tax_rate, discount):
    subtotal = sum(item.price for item in items)
    discounted = subtotal - discount
    return discounted + (discounted * tax_rate)

# Bad
def calc(i, t, d):
    s = sum(x.p for x in i)
    return (s - d) * (1 + t)
```

**Small, focused functions**:
```python
# Good - single responsibility
def validate_email_format(email):
    return "@" in email and "." in email.split("@")[-1]

def email_exists(email):
    return db.query(User).filter_by(email=email).first() is not None

def validate_email(email):
    if not email:
        raise ValueError("Email cannot be empty")
    if not validate_email_format(email):
        raise ValueError("Invalid email format")
    if email_exists(email):
        raise ValueError("Email already registered")
```

**Clear error messages**:
```python
# Good
if len(password) < 8:
    raise ValueError("Password must be at least 8 characters")
if not any(c.isdigit() for c in password):
    raise ValueError("Password must contain at least one number")

# Bad
if len(password) < 8 or not any(c.isdigit() for c in password):
    raise ValueError("Invalid password")  # Vague!
```

## Anti-Patterns

❌ **Hardcoding test values**:
```python
def calculate_discount(price):
    if price == 100:  # Hardcoded test value!
        return 10
```

✅ **Generic implementation**:
```python
def calculate_discount(price, percentage):
    return price * (percentage / 100)
```

❌ **Adding untested features**:
```python
def register_user(email, password, username):
    user = create_user(email, password, username)
    send_welcome_email(user)  # Not tested!
    create_preferences(user)  # Not tested!
```

✅ **Only what tests require**:
```python
def register_user(email, password, username):
    validate_inputs(email, password, username)
    user = create_user(email, password, username)
    save_user(user)
    return user
```

❌ **Modifying tests to pass**:
```python
# In test file - NEVER DO THIS
def test_validation():
    # assert validate_email("user@example.com") == True
    assert True  # Cheating!
```

## Example (Complete Feature)

**Tests require** (from test file):
```python
def test_valid_registration():
    user = register_user("test@example.com", "Pass123!", "testuser")
    assert user.email == "test@example.com"
    assert user.username == "testuser"

def test_duplicate_email():
    register_user("test@example.com", "Pass123!", "user1")
    with pytest.raises(ValueError, match="Email already registered"):
        register_user("test@example.com", "Pass123!", "user2")
```

**Implementation**:
```python
def register_user(email, password, username):
    """Register new user with validation"""
    validate_email(email)
    validate_password(password)
    validate_username(username)

    if user_exists(email):
        raise ValueError("Email already registered")

    hashed = hash_password(password)
    user = User(email=email, password=hashed, username=username)
    save_user(user)
    return user
```

## Transition

Once implementation is complete:

1. Ensure no tests were modified: `git diff tests/`
2. Verify no untested features added
3. Check code quality and readability
4. Type `/iterate` to run tests and refine

---

**The goal is green tests with simple, clean code. Nothing more, nothing less.**
