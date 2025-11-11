# agent-loop Workflow Test Scenarios

Complete end-to-end workflow scenarios for the agent-loop plugin testing the 4-stage process: Explore → Plan → Code → Commit.

## Workflow 1: Simple Feature Addition


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 15-20 minutes

### Setup
- Clone a test repository or use existing codebase
- Initialize git if not already initialized
- Have a simple feature to add (e.g., "add email validation function")

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- Exploration Phase - Use `/explore` command
   - Investigate existing code structure
   - Find where new function should be added
   - Check for existing validation patterns
   - Document findings

- Planning Phase - Use `/plan` command
   - Create implementation plan for email validation
   - Define function signature
   - List test cases needed
   - Identify dependencies

- Implementation Phase - Use `/code` command
   - Implement email validation function
   - Follow plan structure
   - Add unit tests
   - Verify function works correctly

- Commit Phase - Use `/commit` command
   - Run git status to see changes
   - Stage new files with git add
   - Create descriptive commit message
   - Push changes

### Expected Deliverables
- Email validation function implemented and tested
- Unit tests passing
- Clean git commit with descriptive message
- Code follows project conventions

### Verification
- Verify function exists and is exported
- Verify tests pass: `pytest tests/` or equivalent
- Verify git commit exists: `git log -1`
- Verify code quality meets standards

## Workflow 2: Bug Fix


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 20 minutes

### Setup
- Have a known bug in codebase or create one
- Bug should be reproducible (e.g., "division by zero error in calculate function")

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- Exploration - Use `/explore`
   - Locate buggy function in codebase
   - Understand current implementation
   - Reproduce the bug
   - Document bug behavior

- Planning - Use `/plan`
   - Plan bug fix approach
   - Define test case that reproduces bug
   - Plan fix implementation
   - Consider edge cases

- Implementation - Use `/code`
   - Write failing test that reproduces bug
   - Implement fix
   - Verify test now passes
   - Check for similar bugs elsewhere

- Commit - Use `/commit`
   - Stage bug fix and test
   - Write commit message explaining fix
   - Push changes

### Expected Deliverables
- Bug fixed and no longer reproducible
- Test case added that would catch regression
- Git commit documenting the fix

### Verification
- Verify bug no longer occurs
- Verify new test passes
- Verify no regression in other tests

## Workflow 3: Refactoring Task


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 25 minutes

### Setup
- Identify code that needs refactoring (long function, duplicate code, etc.)
- Example: "Extract duplicate validation logic into utility function"

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- Exploration - Use `/explore`
   - Find duplicate or complex code
   - Understand current behavior
   - Identify refactoring opportunity
   - Check test coverage

- Planning - Use `/plan`
   - Plan refactoring approach
   - Define new structure
   - Ensure behavior preservation
   - Plan incremental steps

- Implementation - Use `/code`
   - Refactor code incrementally
   - Run tests after each step
   - Ensure no behavior changes
   - Update documentation

- Commit - Use `/commit`
   - Stage refactored code
   - Write commit explaining refactoring
   - Push changes

### Expected Deliverables
- Code is cleaner and more maintainable
- All existing tests still pass
- No behavior changes
- Clear commit message

### Verification
- Verify all tests pass
- Verify behavior unchanged
- Verify code quality improved (fewer lines, clearer logic)

## Workflow 4: New Module Creation


This workflow requires initial setup of test environment and project prerequisites. Execute the steps sequentially to complete the workflow. Verify all deliverables and expected outputs are produced correctly.

**Estimated Time:** 30 minutes

### Setup
- Plan to create new module/component
- Example: "Create user authentication module"

### Execution Steps

- Execute the first phase following guidance from the corresponding command
- Complete the second phase following workflow progression
- Verify each step completes successfully before proceeding to next phase

**Detailed Steps:**


- Exploration - Use `/explore`
   - Review project structure
   - Understand module conventions
   - Check for related modules
   - Document integration points

- Planning - Use `/plan`
   - Design module structure
   - Define API/interface
   - Plan tests
   - Identify dependencies

- Implementation - Use `/code`
   - Create module files
   - Implement core functionality
   - Add comprehensive tests
   - Document public API

- Commit - Use `/commit`
   - Stage new module files
   - Write detailed commit message
   - Push changes

### Expected Deliverables
- New module created and functional
- Comprehensive test coverage
- Documentation for public API
- Integrated with existing codebase

### Verification
- Verify module can be imported/used
- Verify all tests pass
- Verify documentation is clear

## Stage Transition Testing

### Verify Smooth Transitions

For each workflow, observe and verify:

- **Explore → Plan**: Agent suggests planning after exploration completes
- **Plan → Code**: Agent reminds to follow plan during implementation
- **Code → Commit**: Agent suggests committing when implementation complete

### Verify Anti-Pattern Detection

Test that agent blocks these anti-patterns:

- Attempting to code without planning first
- Skipping exploration for unfamiliar code
- Committing without testing
- Making large changes without a plan

## Success Criteria

Workflow testing is successful when:

- All 4 workflows complete from start to finish without blocking issues
- Each stage (explore, plan, code, commit) provides appropriate guidance
- Stage transitions are clear and logical
- Deliverables match expectations for each workflow
- All verification steps pass
- Time estimates are accurate within 25%
- Agent detects and warns about anti-patterns
