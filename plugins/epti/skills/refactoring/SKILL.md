---
name: refactoring
description: Post-implementation code refinement to improve structure, readability, and maintainability while preserving behavior. Use after tests pass to clean up implementation and reduce technical debt.
---

# Refactoring Skill

## Purpose

Transform working code into cleaner, more maintainable code without changing behavior. Ensures refactoring is safe, incremental, and always maintains test coverage.

## When to Use

- After tests pass (Green → Green refactoring)
- When code smells detected (duplication, complexity)
- Before adding new features (clean foundation)
- During code review feedback

## Core Procedure

### Step 1: Verify Tests Pass

Before any refactoring:
```bash
pytest -v
# All tests must pass: ✓ 45 passed, 0 failed
```

If tests failing, fix them first. Never refactor with failing tests.

### Step 2: Identify Refactoring Opportunities

Look for code smells:

**Duplication**: Same code repeated
**Long Functions**: > 20-30 lines doing multiple things
**Complex Logic**: Nested conditionals, hard to understand
**Poor Names**: Unclear variable/function names
**Magic Numbers**: Hardcoded values with no context
**Large Classes**: Too many responsibilities

### Step 3: Choose Refactoring Pattern

Select appropriate refactoring:

**Extract Function**: Break long function into smaller pieces
**Rename**: Improve clarity of names
**Extract Variable**: Name intermediate values
**Simplify Conditional**: Reduce nesting, clarify logic
**Remove Duplication**: DRY principle
**Extract Class**: Split large class into focused classes

### Step 4: Apply Refactoring Incrementally

Small steps with verification:

1. Make ONE small change
2. Run tests immediately
3. Tests pass → Continue
4. Tests fail → Revert, try different approach
5. Commit after each successful refactoring

### Step 5: Final Verification

After all refactorings:
- Run full test suite
- Check code coverage unchanged
- Verify no new warnings/errors
- Review changes for clarity

## Key Principles

**Tests Must Stay Green**: Golden rule - tests pass before, tests pass after. If tests fail, refactoring changed behavior (revert!).

**Refactor in Small Steps**: One small change at a time. Run tests after each. Commit successful changes. Never refactor entire module at once.

**Preserve Behavior**: Internal structure can change. Public API, return values, side effects cannot change. Tests verify behavior unchanged.

**Clean Code Goals**: Single Responsibility Principle. Descriptive names. Low complexity. No duplication. Clear intent.

## Example

### Extract Function Refactoring

**Before:** Long function with multiple responsibilities

```python
def process_order(order):
    # Validation
    if not order.get("customer_id"):
        raise ValueError("Customer ID required")
    if not order.get("items") or len(order["items"]) == 0:
        raise ValueError("Order must have items")
    if order.get("total", 0) <= 0:
        raise ValueError("Order total must be positive")

    # Discount calculation
    total = order["total"]
    if total >= 500:
        discount = total * 0.15
    elif total >= 200:
        discount = total * 0.10
    elif total >= 100:
        discount = total * 0.05
    else:
        discount = 0

    # Save to database
    discounted_total = total - discount
    db.execute(
        "INSERT INTO orders (customer_id, total, discount) VALUES (?, ?, ?)",
        (order["customer_id"], discounted_total, discount)
    )

    return {"order_id": db.last_insert_id(), "total": discounted_total}
```

**After:** Extracted into focused functions

```python
def process_order(order):
    """Process and save order with appropriate discount."""
    _validate_order(order)
    discount = _calculate_discount(order["total"])
    discounted_total = order["total"] - discount
    order_id = _save_order(order["customer_id"], discounted_total, discount)
    return {"order_id": order_id, "total": discounted_total}


def _validate_order(order):
    """Validate order has required fields."""
    if not order.get("customer_id"):
        raise ValueError("Customer ID required")
    if not order.get("items") or len(order["items"]) == 0:
        raise ValueError("Order must have items")
    if order.get("total", 0) <= 0:
        raise ValueError("Order total must be positive")


def _calculate_discount(total):
    """Calculate discount based on order total."""
    if total >= 500:
        return total * 0.15
    elif total >= 200:
        return total * 0.10
    elif total >= 100:
        return total * 0.05
    return 0


def _save_order(customer_id, total, discount):
    """Save order to database and return order ID."""
    db.execute(
        "INSERT INTO orders (customer_id, total, discount) VALUES (?, ?, ?)",
        (customer_id, total, discount)
    )
    return db.last_insert_id()
```

**Benefits:**
- Single Responsibility: Each function has one job
- Testable: Can test discount calculation independently
- Readable: Intent clear from function names
- Maintainable: Easy to modify discount logic without touching validation

**Verification:**
```bash
pytest -v
# Output: ✓ 45 passed, 0 failed (same as before)
```

### Rename for Clarity

**Before:** Unclear names

```python
def calc(x, y):
    """Calculate something."""
    if x > 0 and y > 0:
        z = x * y * 0.1
        return z
    return 0
```

**After:** Descriptive names

```python
def calculate_commission(sales_amount, transaction_count):
    """Calculate 10% commission if both sales and transactions are positive."""
    if sales_amount > 0 and transaction_count > 0:
        commission = sales_amount * transaction_count * 0.1
        return commission
    return 0
```

**What Changed:**
- `calc` → `calculate_commission` (clear purpose)
- `x, y` → `sales_amount, transaction_count` (meaningful)
- `z` → `commission` (describes value)
- Magic number `0.1` now explained in docstring

### Remove Duplication

**Before:** Repeated logic

```python
def send_welcome_email(user):
    subject = f"Welcome, {user.name}!"
    body = f"Hello {user.name}, welcome to our service!"
    smtp.send(user.email, subject, body)
    log.info(f"Welcome email sent to {user.email}")


def send_reset_email(user, token):
    subject = f"Password Reset for {user.name}"
    body = f"Hello {user.name}, click here to reset: {token}"
    smtp.send(user.email, subject, body)
    log.info(f"Reset email sent to {user.email}")
```

**After:** Extracted common pattern

```python
def send_welcome_email(user):
    subject = f"Welcome, {user.name}!"
    body = f"Hello {user.name}, welcome to our service!"
    _send_email(user, subject, body, "Welcome")


def send_reset_email(user, token):
    subject = f"Password Reset for {user.name}"
    body = f"Hello {user.name}, click here to reset: {token}"
    _send_email(user, subject, body, "Reset")


def _send_email(user, subject, body, email_type):
    """Send email and log action."""
    smtp.send(user.email, subject, body)
    log.info(f"{email_type} email sent to {user.email}")
```

## Anti-Patterns

❌ **Refactor With Failing Tests**: Starting refactoring when tests are red
✅ **Do**: Fix tests first, then refactor from green state

❌ **Big Bang Refactoring**: Rewriting entire module at once
✅ **Do**: Small, incremental changes with test verification

❌ **Changing Behavior**: Fixing bugs during refactoring
✅ **Do**: Separate bug fixes from refactoring (different commits)

❌ **Skipping Tests**: "It's just a rename, don't need to test"
✅ **Do**: Run tests after EVERY change, no matter how small

❌ **Refactoring Without Tests**: No safety net to catch regressions
✅ **Do**: Write tests first if they don't exist, then refactor

❌ **Over-Engineering**: Creating abstractions for future use cases
✅ **Do**: Refactor for current needs, not hypothetical futures

## Integration

**EPTI Workflow Context:**
- **Stage 6**: Refactoring happens after implementation passes tests
- **Input**: Working code with passing tests
- **Output**: Cleaner code, same passing tests
- **Next**: Commit refined implementation

**Typical Flow:**
```
Tests pass (Green) → Identify smell → Refactor → Tests pass (Green) → Commit
```

**When to Skip:**
- Code already clean and simple
- No obvious improvements
- Time-boxed: Don't refactor for hours

**Works With:**
- test-execution: Verifies refactoring didn't break behavior
- implementation-with-protection: Provides working code to refactor
- overfitting-detection: Ensures refactoring doesn't introduce test-specific code
