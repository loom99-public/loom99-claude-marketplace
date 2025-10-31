# loom99 Claude Marketplace

**Professional-grade workflow plugins for Claude Code**

A curated collection of three production-ready plugins that transform Claude Code into a structured, disciplined development environment. Built for engineers who value systematic approaches over ad-hoc coding.

---

## 🎯 What's Inside

### [agent-loop](./plugins/agent-loop/) - Agentic Software Engineering Loop
**4-stage workflow: Explore → Plan → Code → Commit**

Stop jumping straight into code. This plugin enforces a structured engineering workflow that ensures you understand the problem before solving it.

- **Systematic exploration** of codebases before making changes
- **Structured planning** with task breakdown and dependencies
- **Verification-first coding** with automated test running
- **Conventional commits** with git workflow automation

**Best for**: Complex features, unfamiliar codebases, team collaboration

---

### [epti](./plugins/epti/) - Evaluate-Plan-Test-Implement
**6-stage TDD workflow with exceptional discipline**

True test-driven development with guardrails that prevent cheating. Write tests first, watch them fail, then implement. No shortcuts.

- **Test generation** from requirements (before any implementation)
- **Failure verification** (ensure tests actually fail first)
- **Protected implementation** (safeguards against overfitting)
- **Overfitting detection** (catch test-specific hacks)
- **Automated test running** with framework detection

**Best for**: Critical systems, API development, refactoring, TDD practitioners

---

### [visual-iteration](./plugins/visual-iteration/) - Screenshot-Driven UI Development
**Iterative refinement workflow for pixel-perfect UIs**

Build UIs through rapid iteration cycles with visual feedback. Capture screenshots, analyze differences, make specific improvements, repeat until perfect.

- **Automated screenshot capture** via MCP browser tools
- **Specific visual feedback** ("32px should be 24px, add 2px border-radius")
- **Before/after comparison** for tracking progress
- **Typical iteration cycles**: 2-3 rounds to pixel perfection

**Best for**: Frontend development, design system implementation, UI polish

---

## 🚀 Quickstart

### 1. Install the Marketplace

```bash
# Clone or navigate to the marketplace
cd ~/icode/loom99-claude-marketplace

# Validate structure (optional)
just validate

# Add marketplace to Claude Code
/plugin marketplace add .
```

### 2. Install a Plugin

```bash
# In Claude Code, install the plugin you want:
/plugin install agent-loop
# OR
/plugin install epti
# OR
/plugin install visual-iteration
```

### 3. Start Using It

Each plugin provides slash commands for its workflow:

**agent-loop**:
```
/explore   - Investigate codebase systematically
/plan      - Create structured implementation plan
/code      - Implement with verification
/commit    - Finalize with git operations
```

**epti**:
```
/write-tests     - Generate tests without implementation
/verify-fail     - Verify tests fail properly
/commit-tests    - Commit tests only
/implement       - Implement code to pass tests
/iterate         - Refine implementation
/commit-code     - Commit final implementation
```

**visual-iteration**:
```
/screenshot      - Capture current UI state
/feedback        - Analyze screenshot and suggest improvements
/refine          - Implement visual improvements
/iterate-loop    - Run full iteration cycle
/compare         - Side-by-side before/after comparison
/visual-commit   - Commit polished results
```

---

## 💡 Why Use These Plugins?

### The Problem

Claude Code is powerful but unstructured. Without discipline:
- You jump into coding before understanding the problem
- You skip writing tests or write them after implementation
- You commit without proper review or testing
- You iterate on UIs without systematic feedback

### The Solution

These plugins provide **structured workflows** that:
- ✅ Force understanding before implementation
- ✅ Enforce test-first development
- ✅ Automate verification and validation
- ✅ Guide systematic improvement
- ✅ Prevent common mistakes through hooks

### The Result

- **Fewer bugs** - Tests written first catch issues early
- **Better code** - Understanding comes before implementation
- **Faster iteration** - Structured workflows reduce back-and-forth
- **Cleaner commits** - Conventional commits with proper history
- **Higher quality** - Systematic refinement until requirements met

---

## 🛠️ Common Tasks

```bash
# Validate marketplace structure
just validate

# Run comprehensive tests
just test

# Run full verification (validate + test)
just verify

# Show marketplace info
just info

# Show detailed statistics
just stats

# Clean test artifacts
just clean

# Pre-commit checks
just pre-commit
```

See `Justfile` for all available commands.

---

## 📊 What You Get

- **3 production-ready plugins** (100% MVP complete)
- **13 skills** for specialized capabilities
- **16 slash commands** for workflow stages
- **3 custom agents** with specialized behaviors
- **9 lifecycle hooks** enforcing best practices
- **24,459 lines** of implementation
- **Comprehensive test suite** (60+ test cases, all passing)
- **Full documentation** for each plugin

---

## 📚 Documentation

- **[README.md](./README.md)** - This file (overview and quickstart)
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Technical architecture and design decisions
- **[NEXT_STEPS.md](./NEXT_STEPS.md)** - Resolved issues and future enhancements
- **[CLAUDE.md](./CLAUDE.md)** - Project guidance for Claude Code
- **[tests/README.md](./tests/README.md)** - Test suite documentation
- **Plugin READMEs**:
  - [agent-loop/README.md](./plugins/agent-loop/README.md)
  - [epti/README.md](./plugins/epti/README.md)
  - [visual-iteration/README.md](./plugins/visual-iteration/README.md)

---

## 🔧 Technical Details

### Requirements

- **Claude Code** (latest version)
- **Python 3.8+** (for tests)
- **just** (task runner) - `brew install just`
- **git** (recommended)

### Testing

```bash
# Install test dependencies
just install-deps

# Run all tests
just test

# Run specific test categories
just test-structure
```

All tests pass (60+ test cases) ✅

### Validation

```bash
# Validate marketplace
just validate

# Output: ✔ Validation passed
```

---

## 🎨 Plugin Architecture

Each plugin follows standard Claude Code structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── agents/                  # Custom agent definitions
├── commands/                # Slash commands
├── hooks/                   # Lifecycle hooks
├── skills/                  # Reusable skills (subdirectories with SKILL.md)
└── .mcp.json               # MCP server configuration
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed technical documentation.

---

## 📈 Status

- ✅ **100% MVP Complete** - All plugins fully implemented
- ✅ **Production Ready** - Validated and tested
- ✅ **Skills Structure Fixed** - All 13 skills properly restructured
- ✅ **All Tests Passing** - 60+ functional tests green
- ✅ **Actively Maintained** - By Brandon Fryslie

---

## 🤝 Contributing

This is currently a personal marketplace by Brandon Fryslie. Feedback and suggestions welcome via issues.

---

## 📝 License

MIT License - See individual plugin licenses for details.

---

## 👤 Author

**Brandon Fryslie**
- Email: 
- Marketplace: loom99

---

## 🔗 Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Plugin Marketplaces Guide](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [Writing Plugins](https://docs.claude.com/en/docs/claude-code/plugins)
- [Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)

---

**Ready to transform your Claude Code workflow? Start with `just validate` and install your first plugin!**
