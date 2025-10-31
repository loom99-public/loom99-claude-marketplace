---
name: plan-generation
description: Structured implementation planning with task breakdown, dependency tracking, and success criteria. Use when starting complex features, coordinating multi-step work, or defining clear acceptance criteria.
---

# Plan Generation Skill

## Purpose

Generate detailed, actionable implementation plans that guide coding without ambiguity. Good plans save time by preventing false starts, reducing refactoring, and ensuring nothing is overlooked.

## When to Use

- After exploration complete and context understood
- Before writing production code
- When designing complex features or refactoring
- When multiple implementation approaches exist
- During `/plan` stage of workflow

## Core Procedure

### Step 1: Define Goals

Clarify what needs to be built:
- Feature description
- User impact
- Success criteria
- Constraints and requirements

### Step 2: Break Down Tasks

Decompose into concrete steps:

**Task Structure:**
- Task ID (T1, T2, T3)
- Description (what to do)
- Dependencies (must complete before this)
- Acceptance criteria (how to know it's done)
- Estimated complexity (S/M/L)

### Step 3: Identify Dependencies

Map task relationships:
- Which tasks must complete first
- Which can be done in parallel
- Critical path identification
- Risk areas

### Step 4: Define Implementation Strategy

Choose technical approach:
- Architecture decisions
- Technology choices
- Design patterns to use
- Known tradeoffs

### Step 5: Write Plan Document

Format plan clearly:

```markdown
# Implementation Plan: [Feature Name]

## Goal
[What we're building and why]

## Tasks

### T1: [Task Name] [S/M/L]
**Description:** [What to do]
**Dependencies:** None
**Acceptance:**
- Criterion 1
- Criterion 2

### T2: [Task Name] [S/M/L]
**Description:** [What to do]
**Dependencies:** T1
**Acceptance:**
- Criterion 1

## Implementation Strategy
[Technical approach, patterns, architecture]

## Risks
- Risk 1: [Description + mitigation]
- Risk 2: [Description + mitigation]
```

## Key Principles

**Think First, Code Later**: Time spent planning saves multiples during implementation. Good plan makes coding straightforward.

**Actionable Tasks**: Each task is concrete enough to start immediately. No vague "figure out X" tasks.

**Clear Dependencies**: Know what must be done first. Enables parallel work where possible.

**Measurable Success**: Acceptance criteria are testable. Know when task is done.

**Plans Are Flexible**: Blueprints, not straightjackets. Can adjust if better approach emerges. Document deviations.

**Right-Sized Scope**: Not too granular (50 microtasks), not too broad (2 huge tasks). Typically 5-10 tasks for a feature.

## Example

### Feature: User Authentication

**Plan:**

```markdown
# Implementation Plan: User Authentication

## Goal
Enable users to securely authenticate via email/password, receive JWT tokens, and access protected resources.

## Tasks

### T1: Database Schema [S]
**Description:** Create users table with email, password_hash, created_at
**Dependencies:** None
**Acceptance:**
- Migration file created
- Table exists with proper columns
- Unique constraint on email

### T2: Password Hashing [S]
**Description:** Implement secure password hashing using bcrypt
**Dependencies:** T1
**Acceptance:**
- hash_password(plain) returns bcrypt hash
- verify_password(plain, hash) validates correctly
- Min 12 rounds for bcrypt

### T3: JWT Token Generation [M]
**Description:** Create JWT tokens with user claims and expiration
**Dependencies:** None (parallel with T1/T2)
**Acceptance:**
- generate_token(user_id) returns valid JWT
- Token contains user_id claim
- Token expires in 24 hours
- Secret key from environment variable

### T4: Login Endpoint [M]
**Description:** POST /api/auth/login accepts credentials, returns token
**Dependencies:** T1, T2, T3
**Acceptance:**
- Endpoint accepts email + password
- Returns JWT token for valid credentials
- Returns 401 for invalid credentials
- Returns 404 for nonexistent user

### T5: Auth Middleware [M]
**Description:** Middleware to validate JWT on protected routes
**Dependencies:** T3
**Acceptance:**
- Extracts token from Authorization header
- Validates token signature
- Checks expiration
- Attaches user_id to request context
- Returns 401 for invalid/missing token

### T6: Protected Route Example [S]
**Description:** Create /api/user/profile endpoint requiring auth
**Dependencies:** T4, T5
**Acceptance:**
- Endpoint requires valid JWT
- Returns user profile data
- Returns 401 without valid token

## Implementation Strategy

**Architecture:**
- Token-based authentication (stateless)
- JWT with HMAC-SHA256 signing
- Middleware pattern for auth verification

**Libraries:**
- bcrypt for password hashing
- pyjwt for JWT operations
- SQLAlchemy for database

**Security:**
- Never store plain passwords
- Use environment variable for JWT secret
- Token expiration enforced
- Rate limiting on login endpoint (future)

## Risks

**Risk 1:** JWT secret leaked
**Mitigation:** Store in environment, never commit. Rotate periodically.

**Risk 2:** Brute force login attempts
**Mitigation:** Implement rate limiting (T7 future task)

**Risk 3:** Token expiration too long
**Mitigation:** 24-hour expiration, refresh tokens in future phase
```

### Execution Order

**Parallel Track 1:** T1 → T2 → T4
**Parallel Track 2:** T3 → T5
**Final:** T6 (requires both tracks)

**Total:** ~2-3 hours of work

## Anti-Patterns

❌ **Vague Tasks**: "Implement auth" (too broad)
✅ **Do**: "Create users table", "Implement password hashing" (specific)

❌ **No Dependencies**: All tasks marked "None"
✅ **Do**: Identify real dependencies, enable parallel work

❌ **No Acceptance Criteria**: "Task done when it works"
✅ **Do**: Specific, testable criteria

❌ **Over-Planning**: 50 tasks for simple feature
✅ **Do**: Right-size tasks (5-10 tasks typical)

❌ **Implementation-First**: Start coding before planning
✅ **Do**: Plan first, code later

❌ **Ignoring Plan**: Plan created but not followed
✅ **Do**: Refer to plan during implementation, update if needed

❌ **Analysis Paralysis**: Spending hours planning simple task
✅ **Do**: Time-box planning, iterate if needed

## Integration

**Agent Loop Context:**
- **Stage 2**: Planning happens after exploration
- **Input**: Context from code exploration
- **Output**: Structured implementation plan
- **Next**: Transition to coding stage

**Typical Flow:**
```
Explore (understand context) → Plan (this skill) → Code (implement plan) → Verify → Commit
```

**Works With:**
- code-exploration: Provides context for planning
- verification: Plan defines acceptance criteria to verify
- git-operations: Plan informs commit messages

## Plan Review Checklist

Before finalizing plan, verify:
- [ ] All tasks have clear descriptions
- [ ] Dependencies are explicitly stated
- [ ] Acceptance criteria are testable
