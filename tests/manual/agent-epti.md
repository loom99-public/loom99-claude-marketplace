# epti Agent Observation Checklist

Qualitative assessment checklist for observing the tdd-agent behavior during epti plugin usage.

## Agent Identity and Purpose

**Agent Name:** tdd-agent
**Plugin:** epti
**Purpose:** Enforce test-driven development discipline through 6-stage workflow (Write Tests → Verify Fail → Commit Tests → Implement → Iterate → Commit Code)

## Observable Behaviors Checklist

### TDD Discipline Enforcement

- [ ] Does agent require tests before implementation?
- [ ] Does agent verify tests fail before implementation begins?
- [ ] Does agent block implementation without tests?
- [ ] Does agent require tests to pass before final commit?
- [ ] Is TDD discipline consistently enforced?

### Stage Guidance Quality

- [ ] Does agent provide clear test writing guidance?
- [ ] Does agent explain how to verify test failures?
- [ ] Does agent guide proper test-only commits?
- [ ] Does agent provide implementation guidance that passes tests?
- [ ] Does agent guide refinement while maintaining tests?
- [ ] Does agent ensure final commit has passing tests?

### Anti-Pattern Detection and Blocking

Test these TDD violations and verify agent blocks them:

- [ ] **Implementation before tests**: Does agent detect and prevent implementing before writing tests?
- [ ] **Skipping test failure verification**: Does agent require confirming tests fail first?
- [ ] **Committing with failing tests**: Does agent block commits when tests fail?
- [ ] **Test-specific hacks**: Does agent detect hardcoded values or shortcuts?
- [ ] **Modifying tests to pass**: Does agent detect when tests are being gamed?

**For each blocked anti-pattern, does agent:**
- Explain why it violates TDD discipline?
- Suggest correct TDD workflow step?
- Provide specific guidance to fix the violation?

### Overfitting Detection

- [ ] Does agent detect when implementation includes test-specific code?
- [ ] Does agent warn about hardcoded test values in implementation?
- [ ] Does agent identify when code is "too perfectly" matching tests?

## Qualitative Assessment Questions

**TDD Discipline:** Does agent successfully enforce test-first development?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

**Guidance Quality:** Is test writing and implementation guidance helpful?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

**Anti-Pattern Detection:** Does agent catch TDD violations reliably?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

**Overfitting Prevention:** Does agent prevent test-specific implementation hacks?
**Rating:** Excellent / Good / Fair / Poor
**Notes:**

## TDD Workflow Scenarios to Test

Test at least 3 TDD workflows observing:

1. **New Feature with TDD**
   - Does agent require tests first?
   - Does agent verify tests fail initially?
   - Does agent guide to implementation after tests ready?
   - Does agent verify tests pass before commit?

2. **Bug Fix with TDD**
   - Does agent require reproducing test first?
   - Does agent verify test fails with bug present?
   - Does agent guide to fix after test exists?
   - Does agent verify fix makes test pass?

3. **Refactoring with Tests**
   - Does agent ensure test coverage before refactoring?
   - Does agent verify tests pass throughout refactoring?
   - Does agent catch if tests modified during refactoring?

## Overall Assessment

**Does agent successfully enforce TDD discipline?** Yes / No / Partially
**Why or why not?**

**Most valuable TDD enforcement:**

**Gaps in TDD enforcement:**

**Suggestions for improvement:**

**Overall TDD agent effectiveness:** Excellent / Good / Fair / Poor / Unusable
