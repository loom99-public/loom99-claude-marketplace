---
name: setup-testing
description: Set up a testing framework for a project that doesn't have one. Use when user wants to add testing infrastructure before writing tests.
---

# Setup Testing Framework

Configure testing infrastructure for a project that lacks it.

## When to Use

- Project has no test framework configured
- User wants to establish testing before TDD workflow
- Migrating to a new test framework

## Process

**Step 1**: Detect project type and existing setup

Examine:
- `package.json` (Node/JS/TS)
- `pyproject.toml`, `setup.py`, `requirements.txt` (Python)
- `go.mod` (Go)
- `Cargo.toml` (Rust)
- `pom.xml`, `build.gradle` (Java)
- `Gemfile` (Ruby)

**Step 2**: Recommend framework based on ecosystem

| Language | Default Framework | Alternatives |
|----------|-------------------|--------------|
| JavaScript/TypeScript | Vitest | Jest, Mocha |
| Python | pytest | unittest |
| Go | go test (built-in) | testify |
| Rust | cargo test (built-in) | - |
| Java | JUnit 5 | TestNG |
| Ruby | RSpec | Minitest |

**Step 3**: Ask user to confirm using the AskUserQuestion tool

Example for a Node.js project:
```
AskUserQuestion with questions:
[
  {
    "question": "Which testing framework should we use?",
    "header": "Framework",
    "options": [
      {"label": "Vitest (Recommended)", "description": "Fast, Vite-native, Jest-compatible API"},
      {"label": "Jest", "description": "Popular, well-documented, large ecosystem"},
      {"label": "Mocha + Chai", "description": "Flexible, minimal, modular"}
    ],
    "multiSelect": false
  },
  {
    "question": "Where should tests live?",
    "header": "Test location",
    "options": [
      {"label": "tests/ directory (Recommended)", "description": "Separate from source, clear organization"},
      {"label": "__tests__/ directories", "description": "Co-located with source files"},
      {"label": "*.test.ts alongside source", "description": "Tests next to implementation files"}
    ],
    "multiSelect": false
  },
  {
    "question": "Which additional tooling do you want?",
    "header": "Extras",
    "options": [
      {"label": "Coverage reporting", "description": "Track test coverage with c8 or istanbul"},
      {"label": "Watch mode", "description": "Re-run tests on file changes"},
      {"label": "UI mode", "description": "Visual test runner interface"}
    ],
    "multiSelect": true
  }
]
```

Wait for user response before proceeding to Step 4.

**Step 4**: Install and configure

1. Add dependencies (dev dependencies)
2. Create test directory structure
3. Add test script to package manager config
4. Create example test file demonstrating patterns
5. Add to `.gitignore` if needed (coverage reports, etc.)

**Step 5**: Verify setup works

Run the example test to confirm framework is properly configured.

## Framework-Specific Setup

### JavaScript/TypeScript (Vitest)

```bash
pnpm add -D vitest
```

Add to `package.json`:
```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

Create `vitest.config.ts` if needed.

### Python (pytest)

```bash
uv add --dev pytest pytest-cov
```

Create `pyproject.toml` section:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

### Go

No installation needed. Create `*_test.go` files.

### Rust

No installation needed. Add `#[cfg(test)]` module or `tests/` directory.

## Output

```
═══════════════════════════════════════
Testing Framework Configured
  Framework: [name] [version]
  Test dir: [path]
  Run tests: [command]
  Example: [example test file]
Next: /do:it test [target] to add tests
      /do:it tdd [feature] to start TDD
═══════════════════════════════════════
```
