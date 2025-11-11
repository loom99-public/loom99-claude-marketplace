# epti Workflow Test Scenarios

Complete TDD workflow scenarios for the epti plugin testing the 6-stage process: Write Tests → Verify Fail → Commit Tests → Implement → Iterate → Commit Code.

## Workflow 1: New Feature with TDD


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 25 minutes

### Setup
- Test project with testing framework (pytest, jest, etc.)
- Feature to build: "Add user registration validation"

### Prerequisites
- Testing framework installed and configured
- Git initialized

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- Write Tests - Use `/write-tests`
   - Write tests for registration validation before implementation
   - Cover valid/invalid email, password strength, etc.
   - Define expected behaviors

- Verify Failure - Use `/verify-fail`
   - Run tests and confirm they fail (no implementation yet)
   - Verify failures are for correct reasons (not found, not implemented)
   - Document failure messages

- Commit Tests - Use `/commit-tests`
   - Stage test files only
   - Commit with message "Add registration validation tests"
   - Push test-only commit

- Implement - Use `/implement`
   - Implement registration validation to make tests pass
   - Follow TDD red-green cycle
   - Verify tests now pass

- **Iterate** (if needed) - Use `/iterate`
   - Refine implementation for edge cases
   - Improve code quality
   - Maintain passing tests

- Commit Code - Use `/commit-code`
   - Stage implementation files
   - Commit with message "Implement registration validation"
   - Push final implementation

### Expected Deliverables
- Tests written before implementation
- Tests fail initially, then pass after implementation
- Clean separation of test and implementation commits
- All tests passing
- Code meets quality standards

### Verification
- Verify tests exist and are comprehensive
- Verify test-only commit in git history
- Verify implementation commit separate
- Verify all tests pass: `pytest` or equivalent

## Workflow 2: Bug Fix with TDD


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 20 minutes

### Setup
- Existing bug: "Password reset allows weak passwords"

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- Write Tests - Use `/write-tests`
   - Write test that reproduces the bug
   - Test should fail with current code
   - Document expected vs actual behavior

- Verify Failure - Use `/verify-fail`
   - Run test and confirm it fails
   - Verify failure demonstrates the bug

- Commit Tests - Use `/commit-tests`
   - Commit failing test
   - Message: "Add test for password reset validation bug"

- Implement - Use `/implement`
   - Fix bug to make test pass
   - Verify test now passes
   - Check for similar bugs

- Commit Code - Use `/commit-code`
   - Commit bug fix
   - Reference test in commit message

### Expected Deliverables
- Failing test that demonstrates bug
- Bug fix that makes test pass
- Separate test and fix commits

### Verification
- Verify test fails before fix
- Verify test passes after fix
- Verify no regression in other tests

## Workflow 3: Refactoring with Test Coverage


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 30 minutes

### Setup
- Code to refactor: "Extract duplicate input validation into utility"
- Existing tests cover functionality

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- **Write Tests** (if gaps exist) - Use `/write-tests`
   - Ensure comprehensive test coverage before refactoring
   - Add any missing tests
   - Verify 100% coverage of refactoring target

- Verify Tests Pass - Use `/verify-fail` (should pass, not fail)
   - Confirm all tests pass before refactoring
   - Establish baseline

- Implement Refactoring - Use `/implement`
   - Refactor incrementally
   - Run tests after each small change
   - Maintain green tests throughout

- Iterate - Use `/iterate`
   - Improve refactored code
   - Simplify logic
   - Maintain passing tests

- Commit Code - Use `/commit-code`
   - Commit refactored code
   - Note behavior preservation in message

### Expected Deliverables
- All tests pass before and after refactoring
- Code is cleaner and more maintainable
- No behavior changes
- Test coverage maintained or improved

### Verification
- Verify tests pass before refactoring
- Verify tests pass after refactoring
- Verify code quality improved

## TDD Discipline Testing

### Verify Test-First Enforcement

For each workflow, verify agent enforces:

- Tests must be written before implementation
- Tests must fail before implementation begins
- Tests must pass before final commit
- No test-specific hacks or hardcoded values

### Verify Anti-Pattern Detection

Test that agent blocks:

- Implementing before writing tests
- Skipping test failure verification
- Committing code with failing tests
- Hardcoding test values in implementation
- Modifying tests to make them easier to pass

## Success Criteria

TDD workflow testing is successful when:

- All 3 workflows complete following strict TDD discipline
- Tests are written before implementation in every case
- Tests fail initially, then pass after implementation
- Test and implementation commits are separate
- Agent enforces test-first discipline
- Agent detects and blocks anti-patterns
- Time estimates accurate within 25%
