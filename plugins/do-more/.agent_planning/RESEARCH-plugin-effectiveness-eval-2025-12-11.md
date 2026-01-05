# Research: Testing do-more-now Plugin Effectiveness with DeepEval

**Date**: 2025-12-11
**Topic**: Establishing a quantitative baseline for measuring plugin effectiveness
**Goal**: Real metrics to know if changes improve or degrade the plugin
**Sources**: 20+ external sources

---

## Executive Summary

To measure the effectiveness of the `do-more-now` plugin, we need a **multi-layered evaluation framework** using DeepEval that measures:

1. **Task Completion** - Does the plugin accomplish what it's asked to do?
2. **Workflow Adherence** - Does it follow its defined processes correctly?
3. **Output Quality** - Are the deliverables (code, docs, plans) high quality?
4. **Efficiency** - Does it complete tasks without unnecessary steps?
5. **Regression Detection** - Can we detect when changes make things worse?

The framework should use **synthetic test scenarios** run through Claude in headless mode, scored by an **LLM-as-Judge** evaluator.

---

## What Others Are Doing

### Industry Standard Approaches

| Approach | Description | Relevance to Plugin |
|----------|-------------|---------------------|
| **DeepEval TaskCompletionMetric** | Measures if agent accomplishes task by analyzing execution trace | Directly applicable - can measure if `/do:it` completes work |
| **Trajectory Evaluation** | Analyzes reasoning/decision process, not just output | Critical for workflow adherence (TDD vs iterative) |
| **LLM-as-Judge with G-Eval** | Custom criteria evaluation with chain-of-thought | Perfect for subjective quality assessment |
| **A/B Testing** | Compare prompt versions under controlled conditions | Essential for measuring impact of changes |
| **Regression Testing** | Track metrics across versions, alert on degradation | Core requirement for your goal |

### Key Findings

1. **Start with ~50-100 test cases** covering common scenarios + edge cases
2. **Limit to 2-5 metrics** per evaluation to avoid noise
3. **Use binary scoring** for clear pass/fail criteria, Likert (1-5) for quality
4. **Automate in CI/CD** - run evals on every significant change
5. **Document baseline first** - you can't measure improvement without it

---

## Plugin Components to Evaluate

### Commands (7 total)
| Command | What to Measure |
|---------|-----------------|
| `/do:it` | Intent detection accuracy, workflow selection, task completion |
| `/do:plan` | Status accuracy, plan quality, backlog completeness |
| `/do:explore` | Answer relevance, file reference accuracy |
| `/do:research` | Source quality, synthesis coherence |
| `/do:chores` | Issue detection rate, fix correctness |
| `/do:docs` | Documentation accuracy, completeness |
| `/do:release` | (stub - skip for now) |

### Skills (20+ skills)
Focus on high-impact skills first:
- `do:tdd-workflow` - Does it write tests first?
- `do:iterative-workflow` - Does it validate with runtime?
- `do:fix` - Does it actually fix the bug?
- `do:debug` - Does it find root cause?
- `do:refactor` - Does it preserve behavior?

### Agents (9 total)
- `iterative-implementer` - Code quality, completion rate
- `test-driven-implementer` - TDD adherence, test quality
- `researcher` - Research thoroughness, accuracy
- `project-evaluator` - Gap detection accuracy
- `status-planner` - Plan actionability

---

## Proposed Evaluation Framework

### Architecture

```
do-more-now-eval/
├── pyproject.toml              # uv project
├── src/
│   └── do_eval/
│       ├── __init__.py
│       ├── runner.py           # Headless Claude execution
│       ├── metrics/
│       │   ├── task_completion.py
│       │   ├── workflow_adherence.py
│       │   ├── output_quality.py
│       │   └── intent_detection.py
│       └── scenarios/
│           ├── loader.py       # Load test scenarios
│           └── generator.py    # Generate synthetic scenarios
├── tests/
│   ├── test_commands/
│   │   ├── test_it.py
│   │   ├── test_plan.py
│   │   └── test_explore.py
│   ├── test_skills/
│   │   ├── test_tdd_workflow.py
│   │   └── test_iterative_workflow.py
│   └── conftest.py
├── scenarios/
│   ├── commands/
│   │   ├── it/
│   │   │   ├── fix_simple_bug.yaml
│   │   │   ├── implement_feature.yaml
│   │   │   └── refactor_code.yaml
│   │   └── plan/
│   │       ├── status_check.yaml
│   │       └── feature_proposal.yaml
│   └── skills/
│       └── tdd-workflow/
│           ├── basic_function.yaml
│           └── edge_cases.yaml
├── baselines/
│   └── baseline-2025-12-11.json   # Initial baseline scores
└── reports/
    └── EVAL-{timestamp}.md
```

### Test Scenario Format (YAML)

```yaml
# scenarios/commands/it/fix_simple_bug.yaml
name: "Fix Simple Bug"
command: "/do:it"
description: "Test that /do:it fix correctly identifies and fixes a simple bug"

setup:
  # Synthetic project setup
  files:
    - path: "src/utils.py"
      content: |
        def calculate_total(items):
            # Bug: doesn't handle empty list
            return sum(item['price'] for item in items)

    - path: "tests/test_utils.py"
      content: |
        from src.utils import calculate_total

        def test_calculate_total():
            items = [{'price': 10}, {'price': 20}]
            assert calculate_total(items) == 30

input: "fix calculate_total crashes on empty list"

expected_behavior:
  - "Identifies the bug in calculate_total"
  - "Adds handling for empty list case"
  - "Preserves existing functionality"
  - "Tests pass after fix"

metrics:
  - name: task_completion
    type: binary
    criteria: "The bug is fixed and tests pass"

  - name: fix_correctness
    type: g_eval
    criteria: "The fix correctly handles empty list without breaking existing behavior"
    threshold: 0.7

  - name: workflow_adherence
    type: binary
    criteria: "The skill invoked do:fix and followed the fix workflow"
```

### Core Metrics Implementation

```python
# src/do_eval/metrics/task_completion.py
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

class TaskCompletionMetric(BaseMetric):
    """Binary metric: did the plugin complete the task?"""

    def __init__(self, criteria: str, threshold: float = 0.5):
        self.criteria = criteria
        self.threshold = threshold
        self.score = None
        self.reason = None
        self.success = None

    def measure(self, test_case: LLMTestCase) -> float:
        # Use LLM-as-judge to evaluate
        prompt = f"""
        Evaluate whether this task was completed successfully.

        Task: {test_case.input}
        Criteria: {self.criteria}

        Execution output:
        {test_case.actual_output}

        Was the task completed? Answer only YES or NO, then explain briefly.
        """

        # Call evaluator LLM
        response = self._evaluate(prompt)

        self.score = 1.0 if response.startswith("YES") else 0.0
        self.reason = response
        self.success = self.score >= self.threshold

        return self.score

    @property
    def __name__(self):
        return "Task Completion"
```

```python
# src/do_eval/metrics/workflow_adherence.py
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

def create_workflow_adherence_metric(workflow_name: str, expected_steps: list[str]):
    """Create a G-Eval metric for workflow adherence"""

    steps_text = "\n".join(f"- {step}" for step in expected_steps)

    return GEval(
        name=f"Workflow Adherence ({workflow_name})",
        criteria=f"""
        Evaluate whether the execution followed the {workflow_name} workflow.

        Expected steps:
        {steps_text}

        Score based on:
        - Did it follow the expected order?
        - Did it skip any required steps?
        - Did it add unnecessary steps?
        """,
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT
        ],
        threshold=0.7
    )
```

```python
# src/do_eval/metrics/output_quality.py
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

def create_output_quality_metric(output_type: str):
    """Create quality metric for different output types"""

    criteria_map = {
        "code": """
        Evaluate the quality of the generated code:
        - Is it correct and functional?
        - Is it readable and maintainable?
        - Does it follow best practices?
        - Is it free of obvious bugs?
        """,
        "plan": """
        Evaluate the quality of the generated plan:
        - Are the steps actionable and specific?
        - Is the ordering logical?
        - Are dependencies identified?
        - Is the scope appropriate?
        """,
        "docs": """
        Evaluate the quality of the generated documentation:
        - Is it accurate to the code?
        - Is it clear and understandable?
        - Is it complete?
        - Does it follow conventions?
        """
    }

    return GEval(
        name=f"Output Quality ({output_type})",
        criteria=criteria_map.get(output_type, criteria_map["code"]),
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT
        ],
        threshold=0.6
    )
```

### Headless Runner

```python
# src/do_eval/runner.py
import subprocess
import json
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ExecutionResult:
    output: str
    exit_code: int
    files_changed: list[str]
    duration_seconds: float

class HeadlessRunner:
    """Run Claude Code commands in headless mode"""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def run_command(self, command: str, input_text: str) -> ExecutionResult:
        """Execute a /do: command in headless mode"""

        full_input = f"{command} {input_text}"

        result = subprocess.run(
            ["claude", "-p", full_input, "--print"],
            cwd=self.project_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        return ExecutionResult(
            output=result.stdout,
            exit_code=result.returncode,
            files_changed=self._detect_changed_files(),
            duration_seconds=0  # TODO: measure
        )

    def setup_scenario(self, scenario: dict):
        """Create synthetic project from scenario definition"""
        for file_spec in scenario.get("setup", {}).get("files", []):
            path = self.project_dir / file_spec["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(file_spec["content"])
```

### Test Structure

```python
# tests/test_commands/test_it.py
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from do_eval.runner import HeadlessRunner
from do_eval.metrics import TaskCompletionMetric, create_workflow_adherence_metric
from do_eval.scenarios import load_scenarios

@pytest.fixture
def runner(tmp_path):
    return HeadlessRunner(tmp_path)

@pytest.fixture
def scenarios():
    return load_scenarios("commands/it")

class TestDoIt:
    """Test suite for /do:it command"""

    @pytest.mark.parametrize("scenario", load_scenarios("commands/it"))
    def test_task_completion(self, runner, scenario):
        """Test that /do:it completes the given task"""

        # Setup
        runner.setup_scenario(scenario)

        # Execute
        result = runner.run_command("/do:it", scenario["input"])

        # Create test case
        test_case = LLMTestCase(
            input=scenario["input"],
            actual_output=result.output,
            expected_output=scenario.get("expected_output", "")
        )

        # Evaluate
        metric = TaskCompletionMetric(
            criteria=scenario["metrics"][0]["criteria"]
        )

        assert_test(test_case, [metric])

    def test_fix_intent_detection(self, runner):
        """Test that 'fix' in input triggers do:fix skill"""
        scenario = {
            "setup": {"files": [{"path": "bug.py", "content": "x = 1/0"}]},
            "input": "fix the division by zero bug"
        }

        runner.setup_scenario(scenario)
        result = runner.run_command("/do:it", scenario["input"])

        # Check that do:fix was invoked
        assert "do:fix" in result.output or "fix workflow" in result.output.lower()
```

### CI/CD Integration

```yaml
# .github/workflows/eval.yml
name: Plugin Evaluation

on:
  push:
    paths:
      - 'do-more-now/**'
  pull_request:
    paths:
      - 'do-more-now/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync
        working-directory: do-more-now-eval

      - name: Run evaluations
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: uv run deepeval test run tests/ -n 4
        working-directory: do-more-now-eval

      - name: Compare to baseline
        run: uv run python scripts/compare_baseline.py
        working-directory: do-more-now-eval

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: eval-results
          path: do-more-now-eval/reports/
```

---

## Brainstormed Ideas

### 1. **Synthetic Project Generator**
Create a tool that generates synthetic projects of varying complexity:
- Simple: Single file, one bug
- Medium: Multi-file, dependency between modules
- Complex: Full project structure, multiple issues

This ensures reproducible test scenarios across runs.

### 2. **Golden Output Comparison**
For deterministic tasks (like intent detection), store "golden" outputs and compare:
- `/do:it fix bug` should always invoke `do:fix`
- `/do:it refactor` should always invoke `do:refactor`

Any deviation triggers a regression alert.

### 3. **Skill Activation Rate Tracking**
Research shows skill activation is ~50% baseline. Track:
- How often does the right skill get invoked?
- What inputs cause mis-routing?
- What's the activation rate after changes?

### 4. **Workflow Trace Analysis**
Parse execution logs to verify workflow:
```python
def verify_tdd_workflow(trace):
    """Verify TDD workflow was followed"""
    steps = extract_steps(trace)

    # TDD requires: test first, then implement
    test_step = find_step(steps, "write test")
    impl_step = find_step(steps, "implement")

    return test_step.index < impl_step.index
```

### 5. **Human-in-the-Loop Calibration**
Periodically:
1. Run eval suite
2. Sample 10-20 results
3. Have human rate quality
4. Compare to LLM-as-judge scores
5. Adjust rubrics if drift detected

### 6. **Regression Dashboard**
Simple markdown report showing:
```
## Baseline vs Current

| Metric | Baseline | Current | Δ |
|--------|----------|---------|---|
| Task Completion | 85% | 82% | -3% ⚠️ |
| Workflow Adherence | 90% | 92% | +2% ✓ |
| Output Quality | 3.8 | 3.9 | +0.1 ✓ |
```

### 7. **Scenario Difficulty Levels**
Tag scenarios by difficulty:
- **Easy**: Clear intent, simple task, happy path
- **Medium**: Ambiguous phrasing, moderate complexity
- **Hard**: Edge cases, complex multi-step tasks

Track scores per difficulty level to understand where the plugin struggles.

### 8. **Version Tagging**
Every eval run should capture:
- Plugin version (git hash)
- Model used (claude-sonnet-4-5)
- Timestamp
- Full scenario inputs

This enables historical comparison and debugging.

---

## Recommended Test Scenarios (Initial Set)

### Command: `/do:it`
1. **fix_simple_bug** - Fix obvious bug in single file
2. **fix_complex_bug** - Fix bug requiring understanding of multiple files
3. **implement_function** - Implement a clearly specified function
4. **implement_feature** - Implement multi-file feature
5. **refactor_code** - Refactor without changing behavior
6. **debug_error** - Investigate and explain an error
7. **add_tests** - Add tests to existing code
8. **ambiguous_request** - Handle unclear/ambiguous input gracefully

### Command: `/do:plan`
1. **status_check** - Evaluate current project status
2. **feature_planning** - Create plan for new feature
3. **audit_deep** - Comprehensive codebase audit
4. **track_issue** - Quick issue tracking

### Skill: `tdd-workflow`
1. **basic_tdd** - Simple function with clear requirements
2. **tdd_with_deps** - Function requiring mocks/stubs
3. **tdd_complex** - Multi-step TDD process

### Skill: `iterative-workflow`
1. **iterative_basic** - Simple implementation task
2. **iterative_with_validation** - Requires runtime validation
3. **iterative_ui** - UI component (can't run tests)

---

## Implementation Phases

### Phase 1: Foundation (Low Complexity)
1. Create project structure with uv
2. Implement HeadlessRunner
3. Create 5 basic test scenarios
4. Implement TaskCompletionMetric
5. Run manually, establish baseline

**Deliverable**: Working eval that can measure task completion for `/do:it fix`

### Phase 2: Metrics Expansion (Medium Complexity)
1. Add G-Eval workflow adherence metric
2. Add output quality metric
3. Expand to 20 scenarios
4. Add intent detection tests
5. Generate baseline report

**Deliverable**: Multi-metric evaluation covering all major commands

### Phase 3: Automation (Medium Complexity)
1. CI/CD integration
2. Regression comparison script
3. Baseline management
4. Dashboard generation
5. Alert on degradation

**Deliverable**: Automated evaluation running on every push

### Phase 4: Advanced (High Complexity)
1. Synthetic project generator
2. Multi-turn conversation evaluation
3. Tool call validation
4. Historical trend analysis
5. Human calibration workflow

**Deliverable**: Comprehensive evaluation suite with full observability

---

## Key Success Metrics

For the evaluation framework itself:

| Metric | Target | Purpose |
|--------|--------|---------|
| Scenario Coverage | 50+ scenarios | Cover major use cases |
| Eval Time | <10 min full suite | Fast feedback loop |
| LLM-Judge Agreement | >80% with human | Reliable automated scoring |
| Regression Detection | 100% | Never miss a degradation |
| False Positive Rate | <5% | Don't cry wolf |

---

## Sources

### DeepEval & LLM Evaluation
- [DeepEval GitHub](https://github.com/confident-ai/deepeval)
- [DeepEval Test Cases](https://deepeval.com/docs/evaluation-test-cases)
- [DeepEval G-Eval](https://deepeval.com/docs/metrics-llm-evals)
- [DeepEval Custom Metrics](https://deepeval.com/docs/metrics-custom)
- [DeepEval Task Completion](https://deepeval.com/docs/metrics-task-completion)
- [DataCamp DeepEval Tutorial](https://www.datacamp.com/tutorial/deepeval)
- [LLM Evaluation Playbook](https://www.confident-ai.com/blog/the-ultimate-llm-evaluation-playbook)

### AI Agent Evaluation
- [Confident AI - AI Agent Evaluation Guide](https://www.confident-ai.com/blog/definitive-ai-agent-evaluation-guide)
- [IBM - AI Agent Evaluation](https://www.ibm.com/think/topics/ai-agent-evaluation)
- [Fiddler AI - Agent Evaluation](https://www.fiddler.ai/articles/ai-agent-evaluation)
- [Galileo - AI Agent Metrics](https://galileo.ai/blog/ai-agent-metrics)
- [LXT - Agent Evaluation Framework](https://www.lxt.ai/blog/ai-agent-evaluation/)
- [METR - Measuring AI Task Length](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)

### Workflow & Testing
- [Confident AI - RAG Evaluation in CI/CD](https://www.confident-ai.com/blog/how-to-evaluate-rag-applications-in-ci-cd-pipelines-with-deepeval)
- [Braintrust - A/B Testing Prompts](https://www.braintrust.dev/articles/ab-testing-llm-prompts)
- [Helicone - Testing LLM Prompts](https://www.helicone.ai/blog/test-your-llm-prompts)
- [Datadog - LLM Evaluation Best Practices](https://www.datadoghq.com/blog/llm-evaluation-framework-best-practices/)

### Claude Code Specific
- [Anthropic - Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [SkyWork - Skills Testing Guide](https://skywork.ai/blog/how-to-use-skills-in-claude-code-install-path-project-scoping-testing/)
- [Playwright Skill](https://github.com/lackeyjb/playwright-skill)
- [Claude Plugins Dev](https://claude-plugins.dev/skills/)
