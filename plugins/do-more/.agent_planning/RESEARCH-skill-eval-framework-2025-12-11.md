# Research: Quantitative Testing Framework for Claude Skills & Evals

**Date**: 2025-12-11
**Topic**: Evaluation frameworks for Claude Code skills and prompt-based workflows
**Sources**: 15+ external sources

---

## Executive Summary

There is **no existing framework specifically designed for evaluating Claude Code skills**. However, several general-purpose LLM evaluation frameworks exist that can be adapted. The best approach is to build a lightweight, custom framework that:

1. Uses **DeepEval** or **Promptfoo** as the evaluation engine
2. Applies **LLM-as-a-Judge** patterns from Claude's official guidance
3. Implements **skill-specific test case structures** tailored to the `do-more-now` plugin architecture

---

## Existing Frameworks Analysis

### 1. DeepEval (Recommended Base)

**What it is**: Open-source LLM evaluation framework with pytest integration

**Key strengths**:
- 50+ built-in metrics (G-Eval, Faithfulness, Answer Relevancy, Task Completion, Tool Correctness)
- Native LLM-as-a-Judge support
- Pytest integration for CI/CD
- Runs locally (no cloud dependency)
- Supports custom metric creation

**Installation**: `pip install -U deepeval`

**Basic structure**:
```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval

test_case = LLMTestCase(
    input="user prompt",
    actual_output="skill response",
    expected_output="ideal response"  # optional
)

metric = GEval(name="task_completion", threshold=0.7)
evaluate([test_case], [metric])
```

**Limitation**: Designed for LLM output evaluation, not specifically for multi-step skill workflows.

**Source**: [DeepEval GitHub](https://github.com/confident-ai/deepeval)

---

### 2. Promptfoo

**What it is**: CLI-based prompt testing framework with YAML configuration

**Key strengths**:
- Matrix testing: prompt × model × test case
- 25+ LLM provider support (including Claude)
- Built-in red teaming and security testing
- 100% open source, free to use
- CI/CD integration

**Basic structure**:
```yaml
prompts:
  - "Skill prompt v1"
  - "Skill prompt v2"

providers:
  - anthropic:messages:claude-sonnet-4-20250514

tests:
  - vars:
      input: "test scenario"
    assert:
      - type: llm-rubric
        value: "Response correctly identifies the task"
```

**Limitation**: More suited for prompt comparison than skill workflow validation.

**Source**: [Promptfoo GitHub](https://github.com/promptfoo/promptfoo)

---

### 3. Claude's Official Evaluation Guidance

Anthropic's documentation provides patterns for evaluating Claude outputs:

**Grading hierarchy** (fastest → slowest):
1. **Code-based grading**: Exact match, string match
2. **LLM-based grading**: G-Eval, Likert scales, binary classification
3. **Human grading**: Manual review (avoid if possible)

**LLM-as-Judge best practices**:
- Use detailed, clear rubrics with score definitions
- Use low-precision scales (1-5 or binary)
- Include few-shot examples
- Ask for reasoning before score (chain-of-thought)
- Use a different model as judge than the one being evaluated

**Example grading pattern**:
```python
def evaluate_likert(model_output, criteria):
    prompt = f"""Rate this response on a scale of 1-5 for {criteria}:
    <response>{model_output}</response>
    1: Not at all {criteria}
    5: Perfectly {criteria}
    Output only the number."""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )
    return int(response.content[0].text.strip())
```

**Source**: [Claude Docs - Create Strong Empirical Evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

---

### 4. Agent-Specific Evaluation (τ-bench, AgentBench)

For agentic workflows (like `do-more-now`), specialized benchmarks exist:

**τ-bench (Tau-Bench)**:
- Measures agent ability to interact with users and APIs
- Includes realistic databases, tool APIs, policy documents
- Uses LLM-based user simulator

**AgentBench**:
- Comprehensive benchmark for LLMs as agents
- Function-calling evaluation
- Multi-turn conversation support

**Key insight**: Agent evaluation requires testing both **final outputs** AND **reasoning processes**, since agents can follow different paths to correct answers.

**Sources**:
- [τ-bench](https://sierra.ai/blog/benchmarking-ai-agents)
- [AgentBench GitHub](https://github.com/THUDM/AgentBench)

---

## Recommended Framework Design

Based on research, here's a proposed framework for evaluating Claude skills:

### Architecture

```
skill-eval/
├── test_cases/
│   ├── skill_name/
│   │   ├── test_basic.yaml       # Basic functionality
│   │   ├── test_edge_cases.yaml  # Edge cases
│   │   └── golden_outputs/       # Reference outputs
├── metrics/
│   ├── task_completion.py        # Did it complete the task?
│   ├── instruction_following.py  # Did it follow skill instructions?
│   ├── tool_correctness.py       # Did it use tools correctly?
│   └── output_quality.py         # Is output high quality?
├── runners/
│   ├── headless_runner.py        # Run skills without UI
│   └── ci_runner.py              # CI/CD integration
├── reports/
│   └── EVAL-{skill}-{timestamp}.md
└── config.yaml
```

### Test Case Structure

```yaml
# test_cases/tdd-workflow/test_basic.yaml
name: TDD Workflow - Basic Function
skill: do:tdd-workflow
description: Test TDD workflow with simple function implementation

input:
  task: "Implement a function that checks if a number is prime"
  context:
    has_test_framework: true
    language: python

assertions:
  - type: file_created
    pattern: "test_*.py"
    description: "Test file must be created first"

  - type: llm_rubric
    criteria: "Tests are written BEFORE implementation"
    scale: binary

  - type: llm_rubric
    criteria: "Implementation passes all tests"
    scale: binary

  - type: code_execution
    command: "pytest"
    expected_exit_code: 0

golden_reference: |
  # Expected workflow:
  # 1. Create test_prime.py with failing tests
  # 2. Run tests, confirm failure
  # 3. Implement is_prime() function
  # 4. Run tests, confirm pass
```

### Core Metrics

| Metric | Type | Description |
|--------|------|-------------|
| **Task Completion** | Binary | Did the skill complete its stated objective? |
| **Instruction Following** | 1-5 Likert | How closely did it follow skill instructions? |
| **Tool Correctness** | % | Percentage of tool calls that were correct |
| **Output Quality** | 1-5 Likert | Quality of final deliverable |
| **Workflow Adherence** | Binary | Did it follow the expected workflow order? |
| **No Regressions** | Binary | Did it avoid introducing errors? |

### Evaluation Rubric Template

```python
SKILL_EVAL_RUBRIC = """
You are evaluating a Claude skill execution. Score each criterion.

## Skill: {skill_name}
## Task: {task_description}
## Skill Instructions Summary: {skill_instructions}

## Actual Execution:
<execution>
{execution_trace}
</execution>

## Scoring Criteria:

### 1. Task Completion (0 or 1)
Did the skill accomplish its stated objective?
- 0: Task not completed or fundamentally wrong
- 1: Task completed successfully

### 2. Instruction Following (1-5)
How closely did the execution follow the skill's defined workflow?
- 1: Completely ignored instructions
- 3: Followed some instructions, deviated on others
- 5: Followed instructions precisely

### 3. Output Quality (1-5)
How high-quality is the final deliverable?
- 1: Unusable or severely flawed
- 3: Functional but with issues
- 5: Production-ready, well-crafted

Think through your reasoning first, then provide scores in this format:
<scores>
task_completion: [0 or 1]
instruction_following: [1-5]
output_quality: [1-5]
</scores>
"""
```

### Headless Runner Concept

Since there's no official headless skill runner, we'd need to simulate skill execution:

```python
import anthropic
from pathlib import Path

class SkillEvaluator:
    def __init__(self, skill_path: Path):
        self.skill = self._load_skill(skill_path)
        self.client = anthropic.Anthropic()

    def _load_skill(self, path: Path) -> dict:
        """Load skill definition from SKILL.md"""
        # Parse frontmatter + content
        pass

    def run_test_case(self, test_case: dict) -> dict:
        """Execute skill against test case, capture execution trace"""
        prompt = self._build_execution_prompt(test_case)

        # Run skill (simulated)
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=8192,
            system=self.skill['content'],
            messages=[{"role": "user", "content": test_case['input']['task']}]
        )

        return {
            "execution_trace": response.content[0].text,
            "test_case": test_case
        }

    def evaluate(self, execution: dict) -> dict:
        """Score execution using LLM-as-judge"""
        rubric_prompt = SKILL_EVAL_RUBRIC.format(
            skill_name=self.skill['name'],
            task_description=execution['test_case']['input']['task'],
            skill_instructions=self.skill['summary'],
            execution_trace=execution['execution_trace']
        )

        # Use different model as judge
        judge_response = self.client.messages.create(
            model="claude-sonnet-4-5",  # or use haiku for cost
            max_tokens=2048,
            messages=[{"role": "user", "content": rubric_prompt}]
        )

        return self._parse_scores(judge_response.content[0].text)
```

---

## Implementation Recommendations

### Phase 1: Foundation (Complexity: Low)
1. Create test case YAML schema for skills
2. Build basic LLM-as-judge evaluator using Claude's patterns
3. Implement 3-5 test cases per major skill
4. Generate markdown reports

### Phase 2: Automation (Complexity: Medium)
1. Add pytest integration for CI/CD
2. Implement headless skill execution (simulated)
3. Add regression detection (compare against golden outputs)
4. Build metrics aggregation dashboard

### Phase 3: Advanced (Complexity: High)
1. Multi-turn conversation evaluation (for chat-based skills)
2. Tool call validation (verify correct tool usage)
3. Workflow graph analysis (verify step ordering)
4. A/B testing support for skill variants

---

## Key Insights

1. **No existing framework fits perfectly** - All frameworks are designed for general LLM output evaluation, not skill workflow validation.

2. **LLM-as-a-Judge is essential** - For skill evaluation, automated rubric-based scoring is the only scalable approach. Use Claude Sonnet as judge.

3. **Binary + Likert hybrid works best** - Use binary for pass/fail criteria (task completion), Likert for quality assessments.

4. **Test the workflow, not just output** - Skills define multi-step processes. Evaluation must verify steps were followed in order.

5. **Skill activation is a known problem** - Research shows only 50% baseline activation. Consider including activation reliability in eval metrics.

6. **Build incrementally** - Start with simple test cases and LLM-as-judge, then add complexity as needed.

---

## Sources

- [Claude Docs - Create Strong Empirical Evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
- [DeepEval GitHub](https://github.com/confident-ai/deepeval)
- [DeepEval Tutorial - DataCamp](https://www.datacamp.com/tutorial/deepeval)
- [Promptfoo GitHub](https://github.com/promptfoo/promptfoo)
- [Promptfoo Docs](https://www.promptfoo.dev/docs/intro/)
- [LLM-as-a-Judge Guide - Confident AI](https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method)
- [LLM-as-a-Judge - Towards Data Science](https://towardsdatascience.com/llm-as-a-judge-a-practical-guide/)
- [LLM-as-a-Judge Best Practices - Monte Carlo](https://www.montecarlodata.com/blog-llm-as-judge/)
- [τ-bench - Sierra AI](https://sierra.ai/blog/benchmarking-ai-agents)
- [AgentBench GitHub](https://github.com/THUDM/AgentBench)
- [AI Agent Evaluation - LXT](https://www.lxt.ai/blog/ai-agent-evaluation/)
- [Evidently AI - AI Agent Benchmarks](https://www.evidentlyai.com/blog/ai-agent-benchmarks)
- [Prompt Evaluation Metrics - Portkey](https://portkey.ai/blog/evaluating-prompt-effectiveness-key-metrics-and-tools/)
- [Claude Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [Skill Activation Testing - Scott Spence](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably)
