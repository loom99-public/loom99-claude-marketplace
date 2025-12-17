# agent-loop Plugin

Structured Agentic Software Engineering Loop: **Explore → Plan → Code → Commit**

**Version**: 0.1.0 | **Status**: Production Ready | **License**: MIT

## Quick Start

```bash
# Install from marketplace
/marketplace install agent-loop

# Use in workflow
/explore    # Understand context
/plan       # Design solution
/code       # Implement
/commit     # Finalize with git
```

## Four-Stage Workflow

### 1. Explore 🔍
**Purpose**: Understand before deciding

**Command**: `/explore [what to investigate]`

**Activities**:
- Read code and documentation
- Understand architecture
- Identify dependencies
- Clarify requirements

**Exit**: Can explain system, know what to change

---

### 2. Plan 📋
**Purpose**: Design before implementing

**Command**: `/plan [feature to design]`

**Activities**:
- Break down into tasks
- Define acceptance criteria
- Identify dependencies
- Choose technical approach

**Exit**: Clear implementation roadmap exists

---

### 3. Code 💻
**Purpose**: Implement with quality

**Command**: `/code [what to build]`

**Activities**:
- Write production code
- Follow plan structure
- Add tests
- Verify functionality

**Exit**: Tests pass, plan completed

---

### 4. Commit 📦
**Purpose**: Finalize professionally

**Command**: `/commit [what changed]`

**Activities**:
- Run verification checks
- Write conventional commit message
- Create git commit
- Update documentation

**Exit**: Clean commit in history

## Core Principles

**Quality over Speed**: Do it right the first time. Rushing creates rework.

**No Stage Skipping**: Each stage has purpose. Skipping creates technical debt.

**Discipline Wins**: Structured workflow prevents premature optimization and false starts.

**Plan as Contract**: Implementation follows plan. Deviations documented.

## Commands Reference

| Command | Stage | Purpose |
|---------|-------|---------|
| `/explore` | 1 | Investigate and understand |
| `/plan` | 2 | Design and break down |
| `/code` | 3 | Implement with tests |
| `/commit` | 4 | Finalize with git |

## Skills

- **code-exploration**: Systematic codebase investigation
- **plan-generation**: Structured planning with dependencies
- **verification**: Code and test verification
- **git-operations**: Git workflow automation

## Hooks

- **pre-commit**: Blocks commits without plan
- **post-code**: Reminds to run tests
- **commit-msg**: Enforces conventional commit format

## Example Workflow

```bash
# Starting new feature: User authentication
/explore user authentication in codebase

# After understanding context
/plan add JWT authentication to API endpoints

# After plan complete
/code implement JWT auth following plan

# After tests pass
/commit feat(auth): add JWT authentication
```

## Configuration

No configuration required. Works out of the box.

## Integration

Works with:
- Git repositories
- Any programming language
- Test-driven development
- Agile workflows

## Best Practices

1. **Always Explore First**: Even if familiar, explore refreshes context
2. **Plan Before Coding**: 10 minutes planning saves hours of refactoring
3. **Verify Before Commit**: Run tests, check quality, validate plan
4. **Clear Commits**: Conventional format, clear message, tests noted

## When to Use

**Use agent-loop when**:
- Working on complex features
- Unfamiliar codebase
- Need structured approach
- Quality critical

**Skip for**:
- Trivial fixes (typos, formatting)
- Emergency hotfixes
- Experimental prototypes

## Anti-Patterns

❌ Jumping straight to coding
❌ Skipping plan stage
❌ Committing without tests
❌ Vague commit messages
❌ Ignoring pre-commit hooks

✅ Follow Explore → Plan → Code → Commit
✅ Each stage complete before next
✅ Tests pass before commit
✅ Conventional commit format
✅ Respect workflow discipline

## Support

- **Documentation**: See `skills/` directory for detailed guides
- **Issues**: GitHub repository
- **Author**: Brandon Fryslie
- **License**: MIT

## Version History

- **0.1.0** (Current): Initial release with full workflow
