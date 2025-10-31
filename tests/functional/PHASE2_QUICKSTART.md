# Phase 2 Tests: Quick Start Guide

## What Are These Tests?

Automated tests that validate Phase 2 verbosity reduction work:
- **Skills**: Must be 250-400 lines (currently 247-1,232)
- **READMEs**: Must be 200-550 lines (currently 715-2,320)

## Quick Commands

### Check Phase 2 Status

```bash
just test-phase2-quick
```

**Expected now**: `22 failed, 31 passed` (size validation fails, quality passes)
**After Phase 2**: `53 passed` (all tests pass)

### Show Current Metrics

```bash
just phase2-metrics
```

Shows current line counts vs. targets for all skills and READMEs.

### Run Full Test Suite

```bash
just test-phase2
```

Runs all 53 tests with detailed output and Phase 2 summary.

### Test One Plugin

```bash
just test-phase2-plugin visual-iteration
```

Focus on a specific plugin's tests.

## Understanding Test Results

### Before Phase 2 (Current State)

```
22 failed, 31 passed
```

**This is correct!** Tests are designed to fail until Phase 2 work is done.

**22 Failures** = Size validation (files too large)
**31 Passes** = Quality validation (content is good)

### After Phase 2 (Target State)

```
53 passed
```

**All tests pass** = Phase 2 targets achieved, quality preserved.

## What Tests Validate

### Size Tests (Currently FAIL)

- ❌ Skills within 250-450 lines
- ❌ READMEs within target ranges
- ❌ Total skills ~4,030 lines
- ❌ Total READMEs ~1,050 lines

### Quality Tests (Currently PASS)

- ✅ YAML frontmatter preserved
- ✅ Structured sections present
- ✅ Examples included
- ✅ Procedural content intact
- ✅ Plugin descriptions clear

## Key Targets

### Skills

| Plugin | Current Total | Target Total | Per-Skill Range |
|--------|--------------|--------------|-----------------|
| agent-loop | 1,783 lines | 900 lines | 250-400 lines |
| epti | 3,039 lines | 1,430 lines | 250-400 lines |
| visual-iteration | 4,173 lines | 1,700 lines | 250-400 lines |
| **TOTAL** | **8,999** | **4,030** | - |

### READMEs

| Plugin | Current | Target | Max |
|--------|---------|--------|-----|
| agent-loop | 716 lines | 200 lines | 250 lines |
| epti | 1,239 lines | 350 lines | 400 lines |
| visual-iteration | 2,320 lines | 500 lines | 550 lines |
| **TOTAL** | **4,275** | **1,050** | **1,200** |

## Phase 2 Workflow

### 1. Before Starting

```bash
# Check current state
just phase2-metrics

# Run baseline tests (expect failures)
just test-phase2-quick
```

### 2. During Work

After editing skills or READMEs:

```bash
# Quick check
just test-phase2-quick

# Or test specific plugin
just test-phase2-plugin agent-loop
```

### 3. Verify Completion

```bash
# Full test suite
just test-phase2

# Should see: 53 passed
```

## Common Issues

### "Still failing after reduction"

Check the test output for specific issues:
- File still too long? Check line count
- Missing structure? Verify YAML frontmatter and sections
- No examples? Add back 1-2 examples

### "Tests pass but content seems thin"

Good news! Quality tests ensure content is preserved. If tests pass, you've hit the optimal balance.

### "One plugin done, others not"

Use per-plugin tests to track progress:
```bash
just test-phase2-plugin visual-iteration  # Test one plugin
```

## Files

- **Tests**: `tests/functional/test_phase2_reductions.py`
- **Documentation**: `tests/functional/README_PHASE2_TESTS.md`
- **Summary**: `tests/functional/PHASE2_TEST_SUMMARY.md`

## Help

For detailed documentation:
```bash
cat tests/functional/README_PHASE2_TESTS.md
```

For implementation details:
```bash
cat tests/functional/test_phase2_reductions.py
```

---

**TL;DR**: Run `just test-phase2-quick`. Currently: 22 fail (size), 31 pass (quality). After Phase 2: 53 pass (all good).
