# Development Guide

**Local development and testing guide for loom99 Claude Marketplace**

---

## Local Installation for Development

This guide covers installing the marketplace locally in Claude Code for development and testing.

### Prerequisites

1. **Claude Code** installed and running
2. **Repository cloned** to your local machine
3. **Python 3.8+** (for running tests)
4. **just** task runner (optional but recommended): `brew install just`

### Installation Steps

#### 1. Navigate to Repository

```bash
# Use the symlink path for convenience
cd ~/icode/loom99-claude-marketplace

# Or use the full iCloud path
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace
```

#### 2. Validate Structure (Optional but Recommended)

```bash
# Validate marketplace manifest and plugin configurations
just validate

# Or use Claude CLI directly
claude plugin validate .
```

**Expected output**:
```
Validating marketplace manifest: .claude-plugin/marketplace.json
✔ Validation passed
```

#### 3. Install Test Dependencies (Optional)

```bash
# Install Python test dependencies
just install-deps

# Or manually
uv pip install --system pytest PyYAML
```

#### 4. Run Tests (Optional)

```bash
# Run full test suite
just test

# Or run specific test categories
just test-structure
```

**Expected output**:
```
60+ tests should pass
```

#### 5. Add Marketplace to Claude Code

**In Claude Code**, run:

```
/plugin marketplace add ~/icode/loom99-claude-marketplace
```

Or with full path:

```
/plugin marketplace add ~/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace
```

**Expected response**:
```
✓ Marketplace 'loom99' added successfully
```

#### 6. Verify Marketplace Installation

```
/plugin marketplace list
```

**Expected output**:
```
Installed marketplaces:
- loom99 (local: ~/icode/loom99-claude-marketplace)
  - agent-loop (v0.1.0)
  - epti (v0.1.0)
  - visual-iteration (v0.1.0)
```

#### 7. Install Individual Plugins

```
/plugin install agent-loop
```

**Expected response**:
```
✓ Plugin 'agent-loop' installed successfully
  - Loaded 4 commands: /explore, /plan, /code, /commit
  - Loaded 4 skills: code-exploration, git-operations, plan-generation, verification
  - Registered 3 hooks: pre-commit, post-code, commit-msg
```

Repeat for other plugins:
```
/plugin install epti
/plugin install visual-iteration
```

#### 8. Verify Plugin Installation

```
/plugin list
```

**Expected output**:
```
Installed plugins:
- agent-loop (v0.1.0) - Agentic Software Engineering Loop
- epti (v0.1.0) - Evaluate-Plan-Test-Implement TDD Workflow
- visual-iteration (v0.1.0) - Screenshot-Driven UI Development
```

---

## Development Workflow

### Making Changes to Plugins

#### 1. Edit Plugin Files

Make changes to any component:
- **Agents**: `plugins/*/agents/*.md`
- **Commands**: `plugins/*/commands/*.md`
- **Skills**: `plugins/*/skills/*/SKILL.md`
- **Hooks**: `plugins/*/hooks/hooks.json`
- **Manifests**: `plugins/*/.claude-plugin/plugin.json`

#### 2. Validate Changes

```bash
# Validate marketplace structure
just validate

# Run tests to verify structure
just test
```

#### 3. Reload Plugin in Claude Code

After making changes, reload the plugin:

```
/plugin reload agent-loop
```

Or reload all plugins:

```
/plugin reload --all
```

#### 4. Test Changes Interactively

Test your changes by using the commands:

```
/explore
/plan
/code
/commit
```

Or test skills by invoking them in conversation (they're auto-discovered).

---

## Testing

### Run All Tests

```bash
just test
```

### Run Specific Test Categories

```bash
# Structure validation only
just test-structure

# Run with verbose output
pytest tests/functional/test_skills_structure.py -v

# Run specific test
pytest tests/functional/test_skills_structure.py::TestSkillsDirectoryStructure::test_all_skills_use_subdirectories -v
```

### Test Coverage

The test suite validates:
- ✅ All skills in correct subdirectory structure
- ✅ All SKILL.md files have valid YAML frontmatter
- ✅ Plugin configurations reference correct paths
- ✅ Content preserved during migrations
- ✅ All 13 skills accounted for

### Adding New Tests

Create new test functions in `tests/functional/test_skills_structure.py`:

```python
def test_new_requirement():
    """Test description"""
    # Your test logic
    assert condition
```

---

## Common Development Tasks

### Add a New Command

1. Create markdown file in `plugins/PLUGIN/commands/`:
   ```bash
   touch plugins/agent-loop/commands/new-command.md
   ```

2. Write command content:
   ```markdown
   # /new-command - Description

   Your command guidance here...
   ```

3. Reload plugin:
   ```
   /plugin reload agent-loop
   ```

4. Test command:
   ```
   /new-command
   ```

### Add a New Skill

1. Create subdirectory:
   ```bash
   mkdir plugins/agent-loop/skills/new-skill
   ```

2. Create SKILL.md with frontmatter:
   ```yaml
   ---
   name: new-skill
   description: What this skill does and when to use it
   ---

   # Skill content...
   ```

3. Reload plugin:
   ```
   /plugin reload agent-loop
   ```

4. Skill is now auto-discoverable by Claude

### Add a New Hook

1. Edit `plugins/PLUGIN/hooks/hooks.json`:
   ```json
   [
     {
       "event": "pre-commit",
       "command": "echo 'Hook message' && exit 0",
       "description": "What this hook does"
     }
   ]
   ```

2. Reload plugin:
   ```
   /plugin reload agent-loop
   ```

3. Test hook by triggering the event (e.g., git commit)

### Modify Plugin Manifest

1. Edit `plugins/PLUGIN/.claude-plugin/plugin.json`

2. Update version, description, or component paths

3. Validate:
   ```bash
   just validate
   ```

4. Reload plugin:
   ```
   /plugin reload PLUGIN
   ```

---

## Troubleshooting

### Marketplace Not Loading

**Symptom**: `/plugin marketplace list` doesn't show loom99

**Solutions**:
1. Verify path is correct:
   ```bash
   ls ~/icode/loom99-claude-marketplace/.claude-plugin/marketplace.json
   ```

2. Check marketplace.json is valid:
   ```bash
   jq empty .claude-plugin/marketplace.json
   ```

3. Try absolute path instead of relative:
   ```
   /plugin marketplace add /Users/YOUR_USERNAME/icode/loom99-claude-marketplace
   ```

4. Restart Claude Code

### Plugin Not Installing

**Symptom**: `/plugin install agent-loop` fails

**Solutions**:
1. Verify plugin.json exists:
   ```bash
   ls plugins/agent-loop/.claude-plugin/plugin.json
   ```

2. Validate plugin.json:
   ```bash
   jq empty plugins/agent-loop/.claude-plugin/plugin.json
   ```

3. Check component paths exist:
   ```bash
   ls plugins/agent-loop/commands/
   ls plugins/agent-loop/skills/
   ```

4. Reload marketplace:
   ```
   /plugin marketplace reload loom99
   ```

### Commands Not Found

**Symptom**: `/explore` not recognized after installing agent-loop

**Solutions**:
1. Verify plugin installed:
   ```
   /plugin list
   ```

2. Check command files exist:
   ```bash
   ls plugins/agent-loop/commands/
   ```

3. Reload plugin:
   ```
   /plugin reload agent-loop
   ```

4. Restart Claude Code

### Skills Not Working

**Symptom**: Skills not being invoked automatically

**Solutions**:
1. Verify directory structure:
   ```bash
   ls plugins/agent-loop/skills/code-exploration/SKILL.md
   ```

2. Check YAML frontmatter:
   ```bash
   head -10 plugins/agent-loop/skills/code-exploration/SKILL.md
   ```

3. Verify skills path in plugin.json:
   ```bash
   jq .skills plugins/agent-loop/.claude-plugin/plugin.json
   ```

4. Reload plugin:
   ```
   /plugin reload agent-loop
   ```

### Hooks Not Triggering

**Symptom**: Git hooks don't execute

**Solutions**:
1. Verify hooks.json exists and is valid:
   ```bash
   jq empty plugins/agent-loop/hooks/hooks.json
   ```

2. Check hook commands are valid bash:
   ```bash
   # Test hook command manually
   bash -c "YOUR_HOOK_COMMAND"
   ```

3. Verify hooks path in plugin.json:
   ```bash
   jq .hooks plugins/agent-loop/.claude-plugin/plugin.json
   ```

4. Reload plugin:
   ```
   /plugin reload agent-loop
   ```

### Tests Failing

**Symptom**: `just test` shows failures

**Solutions**:
1. Read test output to identify issue

2. Common issues:
   - Missing YAML frontmatter
   - Incorrect directory structure
   - Invalid JSON configuration

3. Fix the issue and re-run:
   ```bash
   just test
   ```

4. Run specific test for debugging:
   ```bash
   pytest tests/functional/test_skills_structure.py::test_name -v
   ```

---

## Development Best Practices

### Before Making Changes

1. ✅ Pull latest changes (if collaborating)
2. ✅ Run `just validate` to verify current state
3. ✅ Run `just test` to ensure tests pass
4. ✅ Create a branch (if using git)

### While Making Changes

1. ✅ Follow existing patterns and conventions
2. ✅ Update documentation if changing behavior
3. ✅ Test incrementally (reload plugin after each change)
4. ✅ Keep changes focused (one feature/fix per branch)

### After Making Changes

1. ✅ Run `just validate` to verify structure
2. ✅ Run `just test` to ensure tests still pass
3. ✅ Test interactively in Claude Code
4. ✅ Update relevant documentation
5. ✅ Commit with descriptive message

### Git Workflow (If Using)

```bash
# Create feature branch
git checkout -b feature/add-new-command

# Make changes, test, validate
just verify

# Commit changes
git add .
git commit -m "feat(agent-loop): add new command for X"

# Push to remote (if applicable)
git push origin feature/add-new-command
```

---

## Advanced Development

### Testing with Multiple Claude Code Instances

You can test with multiple Claude Code instances:

1. **Production instance**: Stable marketplace version
2. **Development instance**: Testing changes

Use different marketplace paths or names to keep separate.

### Debugging Plugin Issues

Enable verbose logging in Claude Code (if available):

```
/debug enable
```

Then test your plugin and review logs.

### Performance Testing

For large repositories, test plugin performance:

1. Clone large repository
2. Install plugins
3. Run commands and measure time
4. Profile if needed

### Integration Testing

Test multiple plugins together:

```
/plugin install agent-loop
/plugin install epti

# Use both workflows
/explore
/plan
/write-tests
/implement
```

Verify no conflicts between plugins.

---

## File Watching and Auto-Reload (Future)

Currently, you must manually reload plugins after changes. Future enhancement:

```bash
# Watch for changes and auto-reload (not yet implemented)
just watch
```

For now, use manual reload:
```
/plugin reload agent-loop
```

---

## Development Environment Setup

### Recommended Tools

1. **Editor**: VS Code, Cursor, or any editor with markdown support
2. **Terminal**: iTerm2 or native Terminal
3. **Git**: For version control
4. **just**: Task runner (`brew install just`)
5. **jq**: JSON validation (`brew install jq`)
6. **Python**: For running tests (`brew install python3`)

### VS Code Configuration (Optional)

Create `.vscode/settings.json`:

```json
{
  "files.associations": {
    "*.md": "markdown"
  },
  "markdown.preview.breaks": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests"
  ]
}
```

---

## Quick Reference

### Essential Commands

```bash
# Validate marketplace
just validate

# Run tests
just test

# Full verification
just verify

# Show info
just info

# Clean artifacts
just clean

# Pre-commit checks
just pre-commit
```

### Claude Code Commands

```
# Marketplace management
/plugin marketplace add ~/icode/loom99-claude-marketplace
/plugin marketplace list
/plugin marketplace reload loom99

# Plugin management
/plugin install agent-loop
/plugin list
/plugin reload agent-loop
/plugin uninstall agent-loop

# Using plugins
/explore
/plan
/code
/commit
```

### File Paths

- **Marketplace manifest**: `.claude-plugin/marketplace.json`
- **Plugin manifests**: `plugins/*/.claude-plugin/plugin.json`
- **Commands**: `plugins/*/commands/*.md`
- **Skills**: `plugins/*/skills/*/SKILL.md`
- **Hooks**: `plugins/*/hooks/hooks.json`
- **Tests**: `tests/functional/test_skills_structure.py`

---

## Getting Help

### Documentation

- **README.md**: User guide
- **ARCHITECTURE.md**: Technical details
- **DEVELOPMENT.md**: This file
- **tests/README.md**: Test documentation

### Debugging Steps

1. Check file exists
2. Validate JSON syntax
3. Verify path references
4. Reload plugin
5. Restart Claude Code
6. Check Claude Code logs

### Support

- **Issues**: Open GitHub issue (if repository public)
- **Email**: 
- **Documentation**: Review architecture docs

---

## Summary

**Quick Setup**:
```bash
cd ~/icode/loom99-claude-marketplace
just validate
just test
```

**In Claude Code**:
```
/plugin marketplace add ~/icode/loom99-claude-marketplace
/plugin install agent-loop
/explore
```

**Development Cycle**:
1. Edit files
2. `just validate`
3. `/plugin reload agent-loop`
4. Test interactively
5. Commit changes

---

**Last Updated**: 2025-10-29
**Maintainer**: Brandon Fryslie
