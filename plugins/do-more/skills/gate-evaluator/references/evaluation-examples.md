# Evaluation Examples

Common gate evaluation scenarios with expected outcomes.

## Decision Gate Examples

### Example 1: Auth-focused rule

**User prompt**: "Ask me if auth or security is touched"
**Context**: "Decision: Add index on users.email for query performance"
**Result**: SKIP
**Rationale**: Database indexing for performance doesn't touch auth/security logic

---

**User prompt**: "Ask me if auth or security is touched"
**Context**: "Decision: Use JWT with 24h expiry for session tokens"
**Result**: TRIGGER
**Rationale**: JWT token configuration is auth-related

---

**User prompt**: "Ask me if auth or security is touched"
**Context**: "Decision: Add bcrypt for password hashing"
**Result**: TRIGGER
**Rationale**: Password hashing is security-critical

### Example 2: Scope-based rule

**User prompt**: "Only ask about architecture decisions"
**Context**: "Decision: Use factory pattern for service instantiation"
**Result**: TRIGGER
**Rationale**: Design patterns are architectural decisions

---

**User prompt**: "Only ask about architecture decisions"
**Context**: "Decision: Name variable 'userCount' vs 'numUsers'"
**Result**: SKIP
**Rationale**: Naming is not an architectural decision

### Example 3: File-count rule

**User prompt**: "Ask if changing more than 3 files"
**Context**: "Decision: Refactor error handling across 7 files"
**Result**: TRIGGER
**Rationale**: 7 files exceeds the 3-file threshold

---

**User prompt**: "Ask if changing more than 3 files"
**Context**: "Decision: Add validation to UserService"
**Result**: SKIP
**Rationale**: Single file change, under threshold

### Example 4: External dependency rule

**User prompt**: "Stop if adding new dependencies"
**Context**: "Decision: Add lodash for utility functions"
**Result**: TRIGGER
**Rationale**: Adding new external dependency

---

**User prompt**: "Stop if adding new dependencies"
**Context**: "Decision: Use existing dayjs (already in package.json)"
**Result**: SKIP
**Rationale**: Using existing dependency, not adding new

## Checkpoint Gate Examples

### Example 5: Test-focused rule

**User prompt**: "Verify when tests are written or modified"
**Context**: "Completed: Added 5 unit tests for AuthService"
**Result**: TRIGGER
**Rationale**: Tests were written

---

**User prompt**: "Verify when tests are written or modified"
**Context**: "Completed: Fixed typo in README"
**Result**: SKIP
**Rationale**: No tests involved

### Example 6: API-focused rule

**User prompt**: "Review any API changes"
**Context**: "Completed: Added new POST /users endpoint"
**Result**: TRIGGER
**Rationale**: New API endpoint added

---

**User prompt**: "Review any API changes"
**Context**: "Completed: Refactored internal helper functions"
**Result**: SKIP
**Rationale**: Internal changes, no API impact

## Ambiguous Cases

When context is unclear, default to TRIGGER:

**User prompt**: "Ask about important decisions"
**Context**: "Decision: Change default timeout from 30s to 60s"
**Result**: TRIGGER
**Rationale**: "Important" is subjective; timeout changes could affect user experience. Err on side of asking.

## Parsing Complex Rules

**User prompt**: "Ask me about auth OR if touching the database schema, but not for test files"

Break down:
1. Auth-related? → Check
2. Database schema? → Check
3. Test files only? → Exclude

**Context**: "Decision: Add migration for users table"
**Result**: TRIGGER (database schema)

**Context**: "Decision: Add test fixture for auth"
**Result**: SKIP (test file, even though auth-related)
