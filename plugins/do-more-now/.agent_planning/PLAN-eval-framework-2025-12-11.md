# Implementation Plan: do-more-now Plugin Evaluation Framework

**Date**: 2025-12-11
**Based on**: RESEARCH-plugin-effectiveness-eval-2025-12-11.md
**Goal**: Quantitative baseline for measuring plugin effectiveness with regression detection

---

## Overview

Build a DeepEval-based testing framework that:
1. Runs plugin commands/skills against synthetic scenarios
2. Scores results using LLM-as-Judge metrics
3. Establishes a baseline for comparison
4. Detects regressions when changes are made

---

## Phase 1: Foundation

**Deliverable**: Working eval measuring task completion for `/do:it fix`

### 1.1 Project Setup
- [ ] Create `do-more-now-eval/` directory structure
- [ ] Initialize uv project with `pyproject.toml`
- [ ] Add dependencies: `deepeval`, `pytest`, `pyyaml`, `anthropic`
- [ ] Create `src/do_eval/__init__.py` package structure

### 1.2 Headless Runner
- [ ] Implement `HeadlessRunner` class in `src/do_eval/runner.py`
  - `run_command(command, input_text)` → Execute via `claude -p`
  - `setup_scenario(scenario)` → Create synthetic project files
  - `cleanup()` → Remove test artifacts
- [ ] Add timing measurement
- [ ] Add file change detection

### 1.3 Scenario Loader
- [ ] Create YAML schema for test scenarios
- [ ] Implement `load_scenarios(path)` in `src/do_eval/scenarios/loader.py`
- [ ] Create 5 initial scenarios:
  - `scenarios/commands/it/fix_simple_bug.yaml`
  - `scenarios/commands/it/fix_empty_list.yaml`
  - `scenarios/commands/it/implement_function.yaml`
  - `scenarios/commands/it/refactor_rename.yaml`
  - `scenarios/commands/it/debug_error.yaml`

### 1.4 Task Completion Metric
- [ ] Implement `TaskCompletionMetric` extending `BaseMetric`
- [ ] Use Claude as LLM-as-Judge (via Anthropic API)
- [ ] Binary scoring (0 or 1) based on criteria
- [ ] Include reasoning in output

### 1.5 Initial Test Suite
- [ ] Create `tests/test_commands/test_it.py`
- [ ] Implement parametrized test using scenarios
- [ ] Create `conftest.py` with fixtures
- [ ] Run manually and verify results

### 1.6 Baseline Capture
- [ ] Run full suite 3x to check consistency
- [ ] Record scores in `baselines/baseline-initial.json`
- [ ] Document any flaky tests

**Exit Criteria**: Can run `uv run pytest tests/` and get scored results for 5 scenarios

---

## Phase 2: Metrics Expansion

**Deliverable**: Multi-metric evaluation covering major commands

### 2.1 G-Eval Workflow Adherence
- [ ] Implement `create_workflow_adherence_metric()` using DeepEval's GEval
- [ ] Define expected steps for each workflow:
  - `do:fix` → Identify bug → Create fix → Verify → Commit
  - `do:tdd-workflow` → Write test → Run (fail) → Implement → Run (pass)
  - `do:iterative-workflow` → Implement → Validate → Iterate
- [ ] Add to test suite

### 2.2 Output Quality Metric
- [ ] Implement `create_output_quality_metric(type)` for:
  - Code quality (correctness, readability, best practices)
  - Plan quality (actionable, logical, scoped)
  - Docs quality (accurate, clear, complete)
- [ ] Threshold: 0.6 (3/5 on quality scale)

### 2.3 Intent Detection Metric
- [ ] Create golden mapping: input pattern → expected skill
  - "fix" → `do:fix`
  - "refactor" → `do:refactor`
  - "debug" → `do:debug`
  - "tdd" → `do:tdd-workflow`
- [ ] Implement binary metric checking correct routing
- [ ] Track activation rate

### 2.4 Expand Scenarios to 20
- [ ] `/do:it` scenarios (8 total)
  - fix_simple_bug, fix_complex_bug, fix_edge_case
  - implement_function, implement_feature
  - refactor_code, debug_error, add_tests
- [ ] `/do:plan` scenarios (4 total)
  - status_check, feature_planning, audit_deep, track_issue
- [ ] `/do:explore` scenarios (4 total)
  - find_function, explain_code, compare_approaches, understand_flow
- [ ] Skill scenarios (4 total)
  - tdd_basic, tdd_complex, iterative_basic, iterative_ui

### 2.5 Test Coverage
- [ ] `test_commands/test_plan.py`
- [ ] `test_commands/test_explore.py`
- [ ] `test_skills/test_tdd_workflow.py`
- [ ] `test_skills/test_iterative_workflow.py`

### 2.6 Baseline Report Generator
- [ ] Create `scripts/generate_baseline.py`
- [ ] Output format: JSON with all scores
- [ ] Generate markdown summary

**Exit Criteria**: 20 scenarios across 3 commands + 2 skills, 3 metrics per scenario

---

## Phase 3: Automation

**Deliverable**: CI/CD integration with regression detection

### 3.1 Regression Comparison Script
- [ ] Create `scripts/compare_baseline.py`
- [ ] Load baseline JSON
- [ ] Compare current run results
- [ ] Calculate deltas per metric
- [ ] Flag degradations (>5% drop)

### 3.2 Report Generator
- [ ] Create `scripts/generate_report.py`
- [ ] Output: `reports/EVAL-{timestamp}.md`
- [ ] Include:
  - Summary table (metric, baseline, current, delta)
  - Pass/fail status per scenario
  - Flagged regressions
  - Full details expandable

### 3.3 CLI Interface
- [ ] Create `src/do_eval/cli.py`
- [ ] Commands:
  - `do-eval run` → Run full suite
  - `do-eval baseline` → Capture new baseline
  - `do-eval compare` → Compare to baseline
  - `do-eval report` → Generate report

### 3.4 GitHub Actions Workflow
- [ ] Create `.github/workflows/eval.yml`
- [ ] Trigger on push to `do-more-now/**`
- [ ] Steps: checkout, setup, install, run, compare, upload
- [ ] Add secrets for `ANTHROPIC_API_KEY`

### 3.5 Baseline Management
- [ ] Store baselines in `baselines/` with timestamps
- [ ] Keep last 5 baselines
- [ ] Script to promote current → baseline

### 3.6 Alert Configuration
- [ ] Define thresholds for alerts
- [ ] Task Completion: warn at -3%, fail at -5%
- [ ] Workflow Adherence: warn at -5%, fail at -10%
- [ ] Output summary in CI logs

**Exit Criteria**: Every push triggers eval, regressions block merge

---

## Phase 4: Advanced (Future)

**Deliverable**: Comprehensive evaluation suite

### 4.1 Synthetic Project Generator
- [ ] Simple projects (1 file, 1 issue)
- [ ] Medium projects (3-5 files, dependencies)
- [ ] Complex projects (full structure, multiple issues)
- [ ] Randomized generation for variety

### 4.2 Multi-Turn Evaluation
- [ ] Conversation trace capture
- [ ] Evaluate full conversation flow
- [ ] Score intermediate steps

### 4.3 Tool Call Validation
- [ ] Capture which tools were called
- [ ] Verify correct tools for task
- [ ] Flag unnecessary tool calls

### 4.4 Historical Trends
- [ ] Store all run results
- [ ] Trend analysis script
- [ ] Visualization (if needed)

### 4.5 Human Calibration
- [ ] Sample results periodically
- [ ] Manual review process
- [ ] Adjust rubrics based on drift

---

## File Structure

```
do-more-now-eval/
├── pyproject.toml
├── src/
│   └── do_eval/
│       ├── __init__.py
│       ├── cli.py
│       ├── runner.py
│       ├── metrics/
│       │   ├── __init__.py
│       │   ├── task_completion.py
│       │   ├── workflow_adherence.py
│       │   ├── output_quality.py
│       │   └── intent_detection.py
│       └── scenarios/
│           ├── __init__.py
│           └── loader.py
├── tests/
│   ├── conftest.py
│   ├── test_commands/
│   │   ├── test_it.py
│   │   ├── test_plan.py
│   │   └── test_explore.py
│   └── test_skills/
│       ├── test_tdd_workflow.py
│       └── test_iterative_workflow.py
├── scenarios/
│   ├── commands/
│   │   ├── it/
│   │   ├── plan/
│   │   └── explore/
│   └── skills/
│       ├── tdd-workflow/
│       └── iterative-workflow/
├── baselines/
│   └── baseline-initial.json
├── reports/
├── scripts/
│   ├── generate_baseline.py
│   ├── compare_baseline.py
│   └── generate_report.py
└── .github/
    └── workflows/
        └── eval.yml
```

---

## Dependencies

```toml
# pyproject.toml
[project]
name = "do-more-now-eval"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "deepeval>=2.0.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pyyaml>=6.0",
    "anthropic>=0.40.0",
    "click>=8.0.0",
]

[project.scripts]
do-eval = "do_eval.cli:main"
```

---

## Metrics Summary

| Metric | Type | Threshold | Used For |
|--------|------|-----------|----------|
| Task Completion | Binary (0/1) | 0.5 | Did it work? |
| Workflow Adherence | G-Eval (0-1) | 0.7 | Did it follow process? |
| Output Quality | G-Eval (0-1) | 0.6 | Is result good? |
| Intent Detection | Binary (0/1) | 1.0 | Right skill invoked? |

---

## Success Criteria

| Criteria | Target |
|----------|--------|
| Phase 1 completion | 5 scenarios passing |
| Phase 2 completion | 20 scenarios, 3+ metrics |
| Phase 3 completion | CI/CD running on every push |
| Baseline accuracy | >80% agreement with human judgment |
| Eval suite runtime | <10 minutes for full suite |
| Regression detection | 100% of degradations caught |

---

## Next Steps

1. Start with Phase 1.1 - Create project structure
2. Implement HeadlessRunner first (core dependency)
3. Create one scenario end-to-end before expanding
4. Run first baseline manually before automating

**Recommended**: `/do:it` to begin Phase 1 implementation
