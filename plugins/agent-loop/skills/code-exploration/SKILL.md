---
name: code-exploration
description: Systematic codebase investigation to understand architecture, patterns, dependencies, and integration points. Use when starting work on unfamiliar code, understanding change impact, or researching existing patterns to follow.
---

# Code Exploration Skill

A reusable skill for investigating codebases systematically using subagents when needed.

## Purpose

Guide thorough codebase exploration to understand architecture, patterns, dependencies, and context before making changes. This skill helps prevent premature decisions and ensures comprehensive understanding.

## When to Use

- Starting work on unfamiliar codebase
- Understanding impact of proposed changes
- Identifying integration points for new features
- Researching existing patterns to follow
- Finding affected components in large refactoring

## Exploration Strategy

### 1. Start with High-Level Structure

**What to examine:**
- Project directory structure (use tree or ls)
- README and documentation files
- Configuration files (package.json, Cargo.toml, go.mod, setup.py, etc.)
- Build and test configurations

**Key questions:**
- What is the overall architecture?
- What frameworks/libraries are used?
- How is the project organized?
- What are the main modules/packages?

### 2. Identify Entry Points

**What to find:**
- Main entry point (main.py, index.js, main.go, etc.)
- API routes or command handlers
- Public interfaces and exports
- Key classes or functions mentioned in requirements

**Exploration approach:**
- Read entry point to understand flow
- Trace execution paths relevant to your task
- Identify which modules will be affected

### 3. Understand Existing Patterns

**What to analyze:**
- Code style and conventions
- Design patterns in use (dependency injection, factories, etc.)
- Error handling approaches
- Testing patterns
- Naming conventions

**Why it matters:**
- New code should match existing patterns
- Understanding patterns prevents conflicts
- Consistency improves maintainability

### 4. Find Dependencies and Integration Points

**What to map:**
- Modules that depend on code you'll modify
- External services or APIs being called
- Database schemas and models
- Shared utilities and libraries

**Analysis approach:**
- Search for imports/requires of relevant modules
- Check for interface definitions
- Review test files for usage examples
- Look for integration tests

### 5. Review Related Tests

**What to examine:**
- Test files for modules you'll modify
- Test structure and frameworks used
- Coverage of edge cases
- Mocking patterns

**Benefits:**
- Tests document expected behavior
- Understanding tests prevents breaking changes
- Test patterns guide new test writing

## Using Subagents for Complex Investigation

For large or complex codebases, invoke subagents to parallelize exploration:

### Subagent Pattern

```markdown
I need to explore this codebase systematically. Can you help investigate:

**Subagent 1 - Architecture Overview:**
- Examine project structure
- Identify main modules and their purposes
- Map dependencies between modules
- Document architectural patterns

**Subagent 2 - Relevant Code Analysis:**
- Find code related to [specific feature/area]
- Trace execution flow
- Identify integration points
- Document current behavior

**Subagent 3 - Test Coverage Review:**
- Locate test files for affected modules
- Analyze test patterns and frameworks
- Identify gaps in test coverage
- Document edge cases being tested

Report findings in a structured format for synthesis.
```

### Synthesis After Subagent Reports

When subagents complete their investigation:

1. **Consolidate findings** into coherent understanding
2. **Identify conflicts** or ambiguities in reports
3. **Fill gaps** with targeted additional investigation
4. **Document architecture** before moving to planning

## Exploration Checklist

Before transitioning to `/plan`, ensure:

- [ ] Overall architecture understood
- [ ] Relevant code files identified and read
- [ ] Existing patterns and conventions documented
- [ ] Dependencies and integration points mapped
- [ ] Related tests reviewed
- [ ] All ambiguities resolved through questions
- [ ] No assumptions made about unknown areas

## Anti-Patterns to Avoid

**Shallow Exploration**
- Symptom: Only reading file names without reading contents
- Fix: Actually read the code, understand what it does

**Confirmation Bias**
- Symptom: Only looking for evidence supporting your initial idea
- Fix: Actively seek information that challenges assumptions

**Scope Creep During Exploration**
- Symptom: Getting lost in tangentially related code
- Fix: Stay focused on areas relevant to current task

**Skipping Tests**
- Symptom: Only reading production code
- Fix: Tests document behavior and provide usage examples

**Analysis Paralysis**
- Symptom: Exploring forever without moving forward
- Fix: Set time limit, document unknowns, ask questions

**Premature Implementation**
- Symptom: Starting to code while still confused about architecture
- Fix: Complete exploration first, then transition to planning phase

## Documentation Template

After exploration, document findings:

```markdown
## Exploration Summary

### Architecture Overview
- [High-level structure]
- [Key modules and purposes]
- [Architectural patterns]

### Relevant Code Locations
- [File paths and descriptions]
- [Integration points]
- [Current behavior]

### Existing Patterns
- [Coding conventions]
- [Design patterns]
- [Error handling approach]

### Dependencies
- [Internal module dependencies]
- [External libraries/APIs]
- [Database schemas]

### Test Coverage
- [Test file locations]
- [Test frameworks used]
- [Edge cases covered]

### Open Questions
- [Unresolved ambiguities]
- [Areas needing clarification]
```

## Example Usage

**Scenario**: Add user authentication to API

**Exploration steps:**
1. Read API entry point to understand request flow
2. Find existing authentication middleware (if any)
3. Review user model and database schema
4. Check how other protected endpoints work
5. Review authentication tests
6. Identify configuration for auth secrets
7. Document current auth approach

**Output**: Understanding of where auth hooks in, what patterns exist, which files need modification

## Integration with Workflow

This skill supports the **Explore** stage of the workflow agent:

- Use this skill when starting `/explore` command
- Reference findings when transitioning to `/plan`
- Subagent reports inform architectural decisions
- Documentation prevents revisiting same code

## Tips for Effective Exploration

1. **Start broad, then narrow**: Understand whole system before diving deep
2. **Follow the data**: Trace how data flows through the system
3. **Read tests like documentation**: They show intended usage
4. **Look for TODOs and comments**: Previous developers left breadcrumbs
5. **Check git history**: Recent changes show active development areas
6. **Ask questions early**: Don't waste time exploring if you can just ask
7. **Document as you explore**: Memory is unreliable, write it down
8. **Use search tools effectively**: grep/ripgrep for finding patterns
9. **Don't guess**: If code is unclear, investigate further or ask
10. **Know when to stop**: Perfect understanding isn't required, sufficient understanding is

## Success Criteria

Exploration is complete when you can:

- Explain the system architecture to someone else
- Identify all files that need modification
- Describe how your changes will integrate
- List potential side effects of your changes
- Confidently transition to planning stage
