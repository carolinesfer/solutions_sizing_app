# Agent Evaluation with Pydantic Evals

This project uses [Pydantic Evals](https://ai.pydantic.dev/evals/) to systematically test and evaluate all four agents in the Agentic Professional Services Scoper system.

## Overview

Pydantic Evals provides a code-first evaluation framework for testing AI systems. Each agent has a dedicated evaluation file (`tests/test_evals.py`) that defines:

- **Datasets**: Collections of test cases with inputs and expected outputs
- **Evaluators**: Scoring functions that assess agent performance
- **Experiments**: Execution of evaluations against the agent

## Evaluation Files

### Requirement Analyzer Agent (`requirement_analyzer_agent/tests/test_evals.py`)

**Test Cases:**
- `churn_prediction_basic`: Basic churn prediction use case
- `time_series_forecast`: Time series forecasting scenario
- `nlp_sentiment_analysis`: NLP sentiment analysis with transcript
- `incomplete_requirements`: Tests gap identification for incomplete inputs

**Evaluators:**
- `IsInstance`: Validates output is a `FactExtractionModel`
- `TechnicalConfidenceEvaluator`: Scores technical confidence (0.0-1.0)
- `RequirementsExtractionEvaluator`: Checks if key requirements were extracted
- `DomainKeywordEvaluator`: Validates domain keyword identification

### Questionnaire Agent (`questionnaire_agent/tests/test_evals.py`)

**Test Cases:**
- `churn_prediction_questionnaire`: Generates questionnaire for churn prediction
- `time_series_questionnaire`: Generates questionnaire for time series use case

**Evaluators:**
- `IsInstance`: Validates output is a `QuestionnaireDraft`
- `CoverageEvaluator`: Scores coverage estimate (should be >= 0.7)
- `DeltaQuestionsEvaluator`: Checks if delta questions were generated for gaps
- `QuestionQualityEvaluator`: Validates question structure and completeness

### Clarifier Agent (`clarifier_agent/tests/test_evals.py`)

**Test Cases:**
- `basic_clarification_loop`: Full clarification loop with all questions answered
- `partial_answers`: Partial answers with remaining gaps

**Evaluators:**
- `IsInstance`: Validates output is a `QuestionnaireFinal`
- `AnsweredPercentageEvaluator`: Validates answered_pct calculation
- `GapIdentificationEvaluator`: Checks if gaps are correctly identified
- `QACountEvaluator`: Validates Q&A pair count matches expectations

### Architecture Agent (`architecture_agent/tests/test_evals.py`)

**Test Cases:**
- `churn_prediction_architecture`: Generates architecture for churn prediction
- `time_series_architecture`: Generates architecture for time series use case

**Evaluators:**
- `IsInstance`: Validates output is an `ArchitecturePlan`
- `StepCountEvaluator`: Validates step count (10-16 steps required)
- `StepCompletenessEvaluator`: Checks if all steps have required fields
- `AssumptionsRisksEvaluator`: Validates assumptions and risks identification

## Running Evaluations

### Individual Agent Evaluation

Run evaluations for a specific agent:

```bash
# Requirement Analyzer Agent
cd requirement_analyzer_agent
python tests/test_evals.py

# Questionnaire Agent
cd questionnaire_agent
python tests/test_evals.py

# Clarifier Agent
cd clarifier_agent
python tests/test_evals.py

# Architecture Agent
cd architecture_agent
python tests/test_evals.py
```

### Programmatic Evaluation

You can also run evaluations programmatically:

```python
from requirement_analyzer_agent.tests.test_evals import (
    requirement_analyzer_dataset,
    run_requirement_analyzer,
)

# Run evaluation
report = requirement_analyzer_dataset.evaluate_sync(run_requirement_analyzer)

# Print results
report.print(include_input=True, include_output=True, include_durations=False)

# Access results programmatically
for case_result in report.case_results:
    print(f"Case: {case_result.case.name}")
    print(f"Scores: {case_result.scores}")
    print(f"Output: {case_result.output}")
```

### Integration with Logfire

If you have [Pydantic Logfire](https://logfire.pydantic.dev/) configured, evaluation results will automatically appear in the Logfire web UI for visualization and analysis.

Install Logfire integration:

```bash
pip install 'pydantic-evals[logfire]'
```

## Evaluation Metrics

Each evaluator returns a score between 0.0 and 1.0:

- **1.0**: Perfect match or optimal performance
- **0.8**: Good performance with minor issues
- **0.5-0.6**: Acceptable performance with notable issues
- **0.0-0.4**: Poor performance or failure

## Custom Evaluators

You can create custom evaluators by extending the `Evaluator` class:

```python
from pydantic_evals.evaluators import Evaluator, EvaluatorContext

class MyCustomEvaluator(Evaluator[InputType, OutputType]):
    def evaluate(self, ctx: EvaluatorContext[InputType, OutputType]) -> float:
        # Your evaluation logic here
        # Return a score between 0.0 and 1.0
        return 1.0
```

## Span-Based Evaluation

The agents use OpenTelemetry for tracing. You can use [span-based evaluation](https://ai.pydantic.dev/evals/evaluators/span-based/) to evaluate internal agent behavior (tool calls, execution flow) using OpenTelemetry traces. This is particularly useful for complex agents where correctness depends on *how* the answer was reached, not just the final output.

Example:

```python
from pydantic_evals.evaluators.span_based import SpanBasedEvaluator

class TracingEvaluator(SpanBasedEvaluator):
    def evaluate_span(self, span, ctx):
        # Evaluate based on OpenTelemetry span attributes
        if "requirement_analyzer.run" in span.name:
            return 1.0
        return 0.5
```

## Best Practices

1. **Add test cases regularly**: As you discover edge cases or new use cases, add them to the evaluation datasets.

2. **Update evaluators**: Refine evaluators based on production feedback and observed agent behavior.

3. **Track evaluation history**: Use Logfire or save evaluation reports to track agent performance over time.

4. **Combine with unit tests**: Pydantic Evals complement unit tests (`test_agent.py`) - use both for comprehensive testing.

5. **Use span-based evaluation**: For complex agents, evaluate not just outputs but also execution traces to ensure correct internal behavior.

## References

- [Pydantic Evals Documentation](https://ai.pydantic.dev/evals/)
- [Pydantic Evals Quick Start](https://ai.pydantic.dev/evals/quick-start/)
- [Evaluators Overview](https://ai.pydantic.dev/evals/evaluators/overview/)
- [Span-Based Evaluation](https://ai.pydantic.dev/evals/evaluators/span-based/)

