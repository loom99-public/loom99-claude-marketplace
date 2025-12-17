# /commit - Finalization Stage

## Your Mission

Finalize completed work and prepare it for review with professional quality.

## What You Should Do

1. **Final Quality Review**
   - Review all changed files for quality
   - Check for any temporary or debug code
   - Verify no unintended files are included
   - Ensure code follows style guidelines
   - Confirm all TODOs are resolved

2. **Test Validation**
   - Run full test suite
   - Verify all tests pass
   - Check for any test warnings
   - Ensure no tests were inappropriately modified
   - Validate functionality works as intended

3. **Clean Up**
   - Remove commented-out code
   - Remove debug statements
   - Clean up unused imports
   - Ensure consistent formatting

4. **Prepare Commit**
   - Stage relevant files
   - Review git diff for each file
   - Ensure no secrets or credentials included
   - Verify changes match intended scope

5. **Write Commit Message**

   Follow this format:
   ```
   <type>(<scope>): <brief summary>

   <detailed explanation of what changed and why>

   - Key change 1
   - Key change 2
   - Key change 3

   Tests: <list of tests that now pass>
   ```

   **Types**: feat, fix, refactor, test, docs, chore

   **Guidelines**:
   - First line: concise summary (50 chars or less)
   - Body: explain the "why" not just the "what"
   - List key changes as bullets
   - Reference tests that validate the changes

## What You Should NOT Do

- DO NOT commit if any tests fail
- DO NOT commit incomplete features
- DO NOT include debug or temporary code
- DO NOT write vague commit messages like "fix bug" or "update code"
- DO NOT commit without reviewing changes

## Pre-Commit Checklist

Before committing, verify:
- [ ] All tests pass
- [ ] All planned functionality implemented
- [ ] No debug code or commented-out code
- [ ] No TODOs or placeholders
- [ ] Code reviewed for quality
- [ ] Error handling is comprehensive
- [ ] Commit message is clear and descriptive
- [ ] Only intended files are staged

## Git Commands

```bash
# Review changes
git status
git diff

# Stage files
git add <files>

# Commit with message
git commit -m "type(scope): summary

Detailed explanation...

- Change 1
- Change 2

Tests: test_name_1, test_name_2"

# Verify commit
git log -1 --stat
```

## After Commit

- Review the commit in git log
- Ensure nothing was missed
- Consider if documentation needs updating
- Transition back to `/explore` for next task

## When to NOT Commit

Stop and address issues if:
- Tests are failing
- Feature is incomplete
- Uncertainty about changes
- Code quality concerns

**It's better to not commit than to commit subpar work.**

---

**Remember**: Commits are permanent history. Make each one count with quality code and clear documentation.
