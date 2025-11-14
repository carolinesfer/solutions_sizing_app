# Testing and Evaluation Plan

This document outlines the comprehensive testing and evaluation strategy for the Agentic Professional Services Scoper system.

## Overview

The codebase includes:
- **Unit Tests**: Traditional pytest-based tests for individual components
- **Pydantic Evals**: Systematic evaluation framework for agent performance
- **Integration Tests**: End-to-end tests for the web API and workflow orchestration

## Prerequisites

### 1. Environment Setup

Ensure all dependencies are installed:

```bash
# Install all agent dependencies
task requirement_analyzer_agent:install
task questionnaire_agent:install
task clarifier_agent:install
task architecture_agent:install

# Install web dependencies
task web:install

# Install shared component dependencies
cd scoper_shared && uv sync
```

### 2. Environment Variables

For tests that require LLM access, ensure the following are set:
- `OPENAI_API_KEY` (or DataRobot LLM Gateway configuration)
- `LLM_DEFAULT_MODEL` (defaults to "gpt-4o-mini" if not set)

**Note**: Some tests use mocks and may not require actual LLM access.

### 3. Database Setup (for integration tests)

Integration tests may require a test database. Ensure database migrations are run:

```bash
cd web
alembic upgrade head
```

## Test Execution Plan

### Phase 1: Shared Component Tests

**Location**: `scoper_shared/tests/`

These tests validate core data models and utilities used by all agents.

#### 1.1 Schema Validation Tests
```bash
cd scoper_shared
pytest tests/test_schemas.py -v
```

**Expected**: All schema validation tests pass, including:
- UseCaseInput validation
- FactExtractionModel constraints (technical_confidence_score 0.0-1.0)
- Question type validation
- ArchitecturePlan step count (10-16)
- QuestionnaireDraft and QuestionnaireFinal validation

#### 1.2 Utility Function Tests
```bash
cd scoper_shared
pytest tests/test_utils.py -v
```

**Expected**: Tests for:
- Domain Router: Correct track selection based on keywords
- KB Retriever: Master questionnaire loading and platform guide filtering

#### 1.3 Orchestrator Tests
```bash
cd scoper_shared
pytest tests/test_orchestrator.py -v
```

**Expected**: Tests for:
- State machine transitions
- Agent coordination
- Gate condition evaluation
- State persistence

**Success Criteria**: All shared component tests pass (100% pass rate)

---

### Phase 2: Agent Unit Tests

**Location**: `{agent_name}/tests/test_agent.py`

These tests validate individual agent functionality using mocks.

#### 2.1 Requirement Analyzer Agent
```bash
cd requirement_analyzer_agent
pytest tests/test_agent.py -v
```

**Tests**:
- Agent initialization
- `run()` method with valid input
- `run_from_json()` method
- Output schema validation

#### 2.2 Questionnaire Agent
```bash
cd questionnaire_agent
pytest tests/test_agent.py -v
```

**Tests**:
- Agent initialization
- KB integration
- Questionnaire generation
- Delta question creation

#### 2.3 Clarifier Agent
```bash
cd clarifier_agent
pytest tests/test_agent.py -v
```

**Tests**:
- Question asking logic
- Answer collection
- Finalization with Q&A pairs
- Gap identification

#### 2.4 Architecture Agent
```bash
cd architecture_agent
pytest tests/test_agent.py -v
```

**Tests**:
- Architecture plan generation
- Step count validation (10-16)
- Markdown generation
- RAG context integration

**Success Criteria**: All unit tests pass (100% pass rate)

---

### Phase 3: Pydantic Evals (Agent Evaluations)

**Location**: `{agent_name}/tests/test_evals.py`

These evaluations systematically test agent performance against real LLM calls.

#### 3.1 Requirement Analyzer Agent Evaluation
```bash
cd requirement_analyzer_agent
python tests/test_evals.py
```

**Evaluators**:
- `IsInstance`: Validates FactExtractionModel output
- `TechnicalConfidenceEvaluator`: Scores confidence (0.0-1.0)
- `RequirementsExtractionEvaluator`: Checks requirement extraction quality
- `DomainKeywordEvaluator`: Validates domain keyword identification

**Test Cases**:
- Churn prediction (basic)
- Time series forecast
- NLP sentiment analysis
- Incomplete requirements (gap identification)

**Success Criteria**: 
- All evaluators return scores >= 0.5
- Average score >= 0.7

#### 3.2 Questionnaire Agent Evaluation
```bash
cd questionnaire_agent
python tests/test_evals.py
```

**Evaluators**:
- `IsInstance`: Validates QuestionnaireDraft output
- `CoverageEvaluator`: Scores coverage estimate
- `DeltaQuestionsEvaluator`: Checks delta question generation
- `QuestionQualityEvaluator`: Validates question structure

**Test Cases**:
- Churn prediction questionnaire
- Time series questionnaire

**Success Criteria**:
- All evaluators return scores >= 0.5
- Average score >= 0.7

#### 3.3 Clarifier Agent Evaluation
```bash
cd clarifier_agent
python tests/test_evals.py
```

**Evaluators**:
- `IsInstance`: Validates QuestionnaireFinal output
- `AnsweredPercentageEvaluator`: Validates answered_pct calculation
- `GapIdentificationEvaluator`: Checks gap identification
- `QACountEvaluator`: Validates Q&A pair count

**Test Cases**:
- Basic clarification loop
- Partial answers

**Success Criteria**:
- All evaluators return scores >= 0.5
- Average score >= 0.7

#### 3.4 Architecture Agent Evaluation
```bash
cd architecture_agent
python tests/test_evals.py
```

**Evaluators**:
- `IsInstance`: Validates ArchitecturePlan output
- `StepCountEvaluator`: Validates step count (10-16)
- `StepCompletenessEvaluator`: Checks step completeness
- `AssumptionsRisksEvaluator`: Validates assumptions/risks identification

**Test Cases**:
- Churn prediction architecture
- Time series architecture

**Success Criteria**:
- All evaluators return scores >= 0.5
- Average score >= 0.7

**Note**: Pydantic evals require actual LLM calls and may take longer. Ensure `OPENAI_API_KEY` is set.

---

### Phase 4: Integration Tests

**Location**: `web/tests/integration/test_scoper.py`

These tests validate the complete workflow through the FastAPI endpoints.

#### 4.1 Scoper API Integration Tests
```bash
cd web
pytest tests/integration/test_scoper.py -v
```

**Tests**:
- `test_start_scoper_workflow`: Workflow creation
- `test_get_scoper_workflow_state`: State retrieval
- `test_submit_clarification_answer`: Clarification submission
- `test_get_scoper_workflow_results`: Results retrieval
- Error handling (404, 400, 500)

**Success Criteria**: All integration tests pass (100% pass rate)

**Note**: These tests may require:
- Database setup (SQLite for testing)
- Mocked agent endpoints (or actual agent instances)

---

### Phase 5: Full Test Suite Execution

Run all tests in sequence:

```bash
# 1. Shared components
cd scoper_shared && pytest -v

# 2. All agent unit tests
cd ../requirement_analyzer_agent && pytest tests/test_agent.py -v
cd ../questionnaire_agent && pytest tests/test_agent.py -v
cd ../clarifier_agent && pytest tests/test_agent.py -v
cd ../architecture_agent && pytest tests/test_agent.py -v

# 3. All agent evaluations (requires LLM)
cd ../requirement_analyzer_agent && python tests/test_evals.py
cd ../questionnaire_agent && python tests/test_evals.py
cd ../clarifier_agent && python tests/test_evals.py
cd ../architecture_agent && python tests/test_evals.py

# 4. Integration tests
cd ../web && pytest tests/integration/test_scoper.py -v
```

---

## Expected Results Summary

### Unit Tests
- **Shared Components**: ~20-30 tests, 100% pass rate
- **Requirement Analyzer Agent**: ~5-10 tests, 100% pass rate
- **Questionnaire Agent**: ~5-10 tests, 100% pass rate
- **Clarifier Agent**: ~8-12 tests, 100% pass rate
- **Architecture Agent**: ~5-10 tests, 100% pass rate

### Pydantic Evals
- **Requirement Analyzer Agent**: 4 test cases, average score >= 0.7
- **Questionnaire Agent**: 2 test cases, average score >= 0.7
- **Clarifier Agent**: 2 test cases, average score >= 0.7
- **Architecture Agent**: 2 test cases, average score >= 0.7

### Integration Tests
- **Scoper API**: ~5-10 tests, 100% pass rate

---

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Symptom**: `ModuleNotFoundError` or `ImportError`
**Solution**: 
- Ensure all dependencies are installed: `task <agent>:install`
- Check Python path: `cd <agent> && python -c "import sys; print(sys.path)"`
- Verify workspace dependencies: `uv sync`

#### 2. LLM API Errors (Pydantic Evals)
**Symptom**: `OpenAI API error` or `Authentication failed`
**Solution**:
- Verify `OPENAI_API_KEY` is set: `echo $OPENAI_API_KEY`
- Check API key validity
- Consider using mocks for unit tests (evals require real LLM)

#### 3. Database Errors (Integration Tests)
**Symptom**: `Database connection error` or `Table not found`
**Solution**:
- Run migrations: `cd web && alembic upgrade head`
- Check database URL in test configuration
- Ensure test database is created

#### 4. Agent Endpoint Errors
**Symptom**: `Connection refused` or `Agent not available`
**Solution**:
- For integration tests, ensure agents are mocked or running
- Check agent endpoints in test configuration
- Verify agent ports are not in use

#### 5. Pydantic Validation Errors
**Symptom**: `ValidationError` in tests
**Solution**:
- Check schema definitions in `scoper_shared/schemas.py`
- Verify test data matches schema constraints
- Review field types and validators

---

## Continuous Integration

For CI/CD pipelines, consider:

1. **Unit Tests**: Run in parallel, fast execution
2. **Pydantic Evals**: Run sequentially (LLM rate limits), may be optional
3. **Integration Tests**: Require database setup, run after unit tests

Example CI configuration:
```yaml
test:
  - name: Unit Tests
    run: |
      pytest scoper_shared/tests/ -v
      pytest requirement_analyzer_agent/tests/test_agent.py -v
      pytest questionnaire_agent/tests/test_agent.py -v
      pytest clarifier_agent/tests/test_agent.py -v
      pytest architecture_agent/tests/test_agent.py -v
  
  - name: Integration Tests
    run: |
      cd web && pytest tests/integration/test_scoper.py -v
  
  - name: Pydantic Evals (Optional)
    run: |
      cd requirement_analyzer_agent && python tests/test_evals.py
      cd ../questionnaire_agent && python tests/test_evals.py
      cd ../clarifier_agent && python tests/test_evals.py
      cd ../architecture_agent && python tests/test_evals.py
    if: env.OPENAI_API_KEY != ''
```

---

## Next Steps

After executing this plan:

1. **Review Results**: Check all test outputs and evaluation scores
2. **Fix Failures**: Address any failing tests or low evaluation scores
3. **Update Documentation**: Document any issues or improvements needed
4. **Iterate**: Re-run tests after fixes to ensure stability

---

## Execution Log

### Execution Date: 2025-01-14

#### Phase 1: Shared Component Tests
- [x] Schema tests: **PASS** (23 tests, 0.64s)
- [x] Utility tests: **PASS** (15 tests, 0.11s)
- [x] Orchestrator tests: **IMPROVED** (10 passed, 3 failed, 2 errors) - Mock paths fixed

**Orchestrator Test Fixes Applied**:
- ✅ Fixed test mock paths to use actual import paths:
  - `requirement_analyzer_agent.custom_model.agent.RequirementAnalyzerAgent`
  - `questionnaire_agent.custom_model.agent.QuestionnaireAgent`
  - `clarifier_agent.custom_model.agent.ClarifierAgent`
  - `architecture_agent.custom_model.agent.ArchitectureAgent`
  - `scoper_shared.utils.kb_retriever.KBRetriever`
- ⚠️ Remaining issue: Tests need agents in PYTHONPATH when run from `scoper_shared/` directory
- **Solution**: Run tests from repository root with `PYTHONPATH=.` or ensure agents are installed

#### Phase 2: Agent Unit Tests
- [x] Package structure: **FIXED** (scoper_shared now uses src/ layout and builds successfully)
- [ ] Requirement Analyzer: **NEEDS TESTING** (package structure fixed, ready for testing)
- [ ] Questionnaire Agent: **NEEDS TESTING** (package structure fixed, ready for testing)
- [ ] Clarifier Agent: **NEEDS TESTING** (package structure fixed, ready for testing)
- [ ] Architecture Agent: **NEEDS TESTING** (package structure fixed, ready for testing)

**Package Structure Fixes Applied**:
- ✅ Removed nested `scoper_shared/scoper_shared/` directory
- ✅ Restructured to use `src/` layout: `scoper_shared/src/scoper_shared/`
- ✅ Updated `scoper_shared/pyproject.toml` to use `packages = ["src/scoper_shared"]`
- ✅ Package builds successfully: `Successfully built dist/scoper_shared-0.1.0-py3-none-any.whl`
- ✅ Workspace dependencies now resolve correctly

#### Phase 3: Pydantic Evals
- [ ] Requirement Analyzer: **NOT RUN** (blocked by dependency issues)
- [ ] Questionnaire Agent: **NOT RUN** (blocked by dependency issues)
- [ ] Clarifier Agent: **NOT RUN** (blocked by dependency issues)
- [ ] Architecture Agent: **NOT RUN** (blocked by dependency issues)

#### Phase 4: Integration Tests
- [ ] Scoper API tests: **NOT RUN**

#### Overall Status: **IN PROGRESS**

**Notes**:
- ✅ Schema tests: **PASS** (23 tests, 0.64s)
- ✅ Utility tests: **PASS** (15 tests, 0.11s)
- ✅ Orchestrator tests: **IMPROVED** (10 passed, 3 failed, 2 errors) - Mock paths fixed, remaining issues are PYTHONPATH related
- ✅ Package structure: **FIXED** - scoper_shared now uses src/ layout and builds successfully
- **Fixes Applied**:
  - ✅ Fixed orchestrator test mock paths to use actual import paths
  - ✅ Restructured scoper_shared to use `src/` layout
  - ✅ Updated `scoper_shared/pyproject.toml` to use `packages = ["src/scoper_shared"]`
  - ✅ Package builds successfully with `uv build`
  - ✅ Removed nested `scoper_shared/scoper_shared/` directory
- **Remaining Issues**:
  - Orchestrator tests need agents in PYTHONPATH (run from repo root with `PYTHONPATH=.`)
  - Agent unit tests need proper environment setup (pytest availability)

**Recommendation**: 
1. ✅ **COMPLETED**: Fixed scoper_shared package structure (using src/ layout)
2. ✅ **COMPLETED**: Fixed orchestrator test mocks
3. ⚠️ **IN PROGRESS**: Re-run all tests from repository root with proper PYTHONPATH
4. ⚠️ **PENDING**: Proceed with Pydantic evals once unit tests pass

**See**: `tasks/fix-test-issues-plan.md` for detailed implementation plan and status

