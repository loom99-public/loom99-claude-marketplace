---
name: git-operations
description: Git workflow automation including commits, branches, and repository management. Use when finalizing changes, creating feature branches, or managing git history following conventional commit standards.
---

# Git Operations Skill

## Purpose

Provide structured guidance for git operations ensuring clear history, professional commit messages, and smooth collaboration. Maintains clean git history that serves as project documentation.

## When to Use

- After implementation verification passes
- When ready to commit code
- Creating pull requests
- Managing feature branches
- Updating documentation with code changes

## Core Procedure

### Step 1: Verify Ready to Commit

Check prerequisites:
- Tests pass (run test suite)
- Code verified (linting, formatting)
- Changes reviewed (self-review complete)
- Documentation updated if needed

### Step 2: Stage Changes

Add files to staging area:
```bash
git add <files>
# Or stage all changes
git add .
```

Check what's staged:
```bash
git status
git diff --cached
```

### Step 3: Write Commit Message

Use conventional commit format:

**Structure:**
```
<type>(<scope>): <summary>

<detailed explanation>

- Key change 1
- Key change 2

Tests: <tests that pass>
```

**Type Values:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `test`: Test changes
- `docs`: Documentation
- `style`: Formatting
- `chore`: Maintenance

**Example:**
```
feat(auth): add JWT token validation

Implement token validation middleware:
- Verify token signature
- Check expiration
- Extract user claims

Tests: test_valid_token, test_expired_token, test_invalid_signature
```

### Step 4: Commit Changes

Create commit:
```bash
git commit -m "type(scope): summary" -m "Details..."
# Or use editor for longer messages
git commit
```

Verify commit:
```bash
git log -1 --stat
```

### Step 5: Push (If Appropriate)

Push to remote:
```bash
# First time pushing branch
git push -u origin <branch-name>

# Subsequent pushes
git push
```

## Key Principles

**Commits Tell a Story**: Each commit should be understandable months later. Clear message, clear intent.

**Atomic Commits**: One logical change per commit. If using "and" in message, probably two commits.

**Tests in History**: Commit when tests pass. History shows working states.

**Clean History**: History is permanent. Make it professional. No "WIP" or "fix typo" commits.

**Conventional Commits**: Follow type(scope): summary format. Enables tooling, improves readability.

**Self-Contained**: Each commit should be reviewable independently. Include context in message.

## Example

### Feature Implementation Commit

**Context:** Added user authentication endpoint

**Check Status:**
```bash
git status
# Changes:
#   modified: src/auth.py
#   new file: tests/test_auth.py
```

**Stage Changes:**
```bash
git add src/auth.py tests/test_auth.py
```

**Write Commit:**
```
feat(auth): add user login endpoint

Implement POST /api/auth/login endpoint:
- Accept email and password
- Validate credentials against database
- Return JWT token on success
- Return 401 for invalid credentials

Tests: test_valid_login, test_invalid_password, test_nonexistent_user
```

**Commit:**
```bash
git commit -F commit_message.txt
```

**Verify:**
```bash
git log -1
# Shows clean, professional commit
```

### Bug Fix Commit

**Context:** Fixed validation bug

**Commit Message:**
```
fix(validation): handle empty email input

Email validator was crashing on empty string input.
Added check for empty/null values before regex validation.

Tests: test_empty_email_validation
```

### Refactoring Commit

**Context:** Extracted duplicate code

**Commit Message:**
```
refactor(api): extract query builder to util

Extracted duplicate SQL query building logic into reusable utility function.
No behavior change - same queries generated.

Tests: All existing tests still pass (42 tests)
```

### Documentation Commit

**Context:** Updated README with new API

**Commit Message:**
```
docs(api): document authentication endpoints

Add documentation for new auth endpoints:
- POST /api/auth/login
- GET /api/auth/verify
- POST /api/auth/logout

Include request/response examples and error codes.
```

## Branch Management

### Creating Feature Branches

**Pattern:**
```bash
# Create and switch to feature branch
git checkout -b feature/user-authentication

# Or separate commands
git branch feature/user-authentication
git checkout feature/user-authentication
```

**Naming Conventions:**
- `feature/` for new features
- `fix/` for bug fixes
- `refactor/` for refactoring
- `docs/` for documentation

### Merging Branches

**Update from main:**
```bash
# Fetch latest changes
git fetch origin

# Merge main into feature branch
git checkout feature/my-feature
git merge origin/main

# Or rebase (cleaner history)
git rebase origin/main
```

**Merge feature into main:**
```bash
# Switch to main
git checkout main

# Merge feature branch
git merge feature/my-feature

# Push to remote
git push origin main
```

## Anti-Patterns

❌ **Vague Messages**: "fix bug", "update code"
✅ **Do**: "fix(auth): handle empty password input"

❌ **WIP Commits**: "work in progress", "WIP"
✅ **Do**: Commit when logical change complete

❌ **Giant Commits**: 50 files changed, multiple features
✅ **Do**: Atomic commits, one logical change

❌ **Broken Commits**: Tests fail at this commit
✅ **Do**: Commit when tests pass

❌ **No Context**: "fix it"
✅ **Do**: Explain what changed and why

❌ **Emoji Pollution**: "✨ Added feature ✨"
✅ **Do**: Professional, searchable text

❌ **Committing Secrets**: API keys, passwords in commits
✅ **Do**: Use environment variables, .gitignore sensitive files

## Integration

**Agent Loop Context:**
- **Stage 4**: After verification passes, before moving to next feature
- **Input**: Verified implementation + passing tests
- **Output**: Clean commit in git history
- **Next**: Loop back to exploration or complete

**Typical Flow:**
```
Explore → Plan → Code → Verify → Commit (this skill) → Next iteration
```

**Works With:**
- verification: Confirms changes ready to commit
- plan-generation: Commit messages reference plan items
- code-exploration: New commits become exploration context
