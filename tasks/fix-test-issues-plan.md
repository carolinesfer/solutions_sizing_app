# Plan to Fix Test Issues and Package Structure

Based on the test results in `test-and-eval.md`, this document outlines the plan to resolve the remaining issues.

## Issues Identified

### Issue 1: Orchestrator Test Mock Configuration
**Problem**: Tests are trying to mock `scoper_shared.orchestrator.RequirementAnalyzerAgent`, but the orchestrator imports agents inside methods using:
```python
from requirement_analyzer_agent.custom_model.agent import RequirementAnalyzerAgent
```

**Error**: `AttributeError: <module 'scoper_shared.orchestrator'> does not have the attribute 'RequirementAnalyzerAgent'`

**Solution**: Update test patches to use the actual import paths where agents are imported:
- `requirement_analyzer_agent.custom_model.agent.RequirementAnalyzerAgent`
- `questionnaire_agent.custom_model.agent.QuestionnaireAgent`
- `clarifier_agent.custom_model.agent.ClarifierAgent`
- `architecture_agent.custom_model.agent.ArchitectureAgent`

### Issue 2: scoper_shared Package Structure
**Problem**: `hatchling` cannot determine which files to ship in the wheel. The package structure may be incorrect.

**Current Structure**:
```
scoper_shared/
  - __init__.py
  - schemas.py
  - orchestrator.py
  - utils/
  - kb_content/
  - tests/
  - scoper_shared/  # Nested directory (incorrect)
```

**Solution**: 
1. Remove nested `scoper_shared/scoper_shared/` directory if it exists
2. Update `pyproject.toml` to use proper package structure with `packages = ["scoper_shared"]`
3. Ensure all package files are correctly included

## Implementation Steps

### Step 1: Fix Orchestrator Test Mocks ✅
- [x] Update `test_orchestrator.py` to patch correct import paths
- [x] Change all `@patch("scoper_shared.orchestrator.X")` to `@patch("requirement_analyzer_agent.custom_model.agent.X")` (and similar for other agents)
- [x] Updated patches for: RequirementAnalyzerAgent, QuestionnaireAgent, ClarifierAgent, ArchitectureAgent, KBRetriever

### Step 2: Fix scoper_shared Package Structure ✅
- [x] Removed nested `scoper_shared/scoper_shared/` directory
- [x] Restructured to use `src/` layout: `scoper_shared/src/scoper_shared/`
- [x] Updated `scoper_shared/pyproject.toml` to use `packages = ["src/scoper_shared"]`
- [x] Verified package builds successfully with `uv build`

### Step 3: Verify Package Build ✅
- [x] Run `cd scoper_shared && uv build` to verify package builds correctly
- [x] Package builds successfully: `Successfully built dist/scoper_shared-0.1.0-py3-none-any.whl`

### Step 4: Re-run Tests
- [ ] Run orchestrator tests: `cd scoper_shared && uv run pytest tests/test_orchestrator.py -v`
- [ ] Run agent unit tests: `task requirement_analyzer_agent:test` (and similar for others)
- [ ] Verify all tests pass

### Step 5: Update Test Plan Document
- [ ] Update `tasks/test-and-eval.md` with results after fixes
- [ ] Mark completed items and note any remaining issues

## Expected Outcomes

After implementing these fixes:
1. ⚠️ Orchestrator tests: 10 passed, 3 failed, 2 errors (mocks fixed, but tests need agents in PYTHONPATH)
2. ✅ Package builds successfully with `uv build`
3. ✅ All workspace dependencies resolve correctly
4. ⚠️ Agent unit tests: Need to run from repository root with proper environment

## Current Status

### ✅ Completed
- Fixed orchestrator test mock paths (all patches updated to use actual import paths)
- Fixed package structure (moved to `src/` layout)
- Package builds successfully
- Removed nested `scoper_shared/scoper_shared/` directory

### ⚠️ Remaining Issues
- Orchestrator tests fail when run from `scoper_shared/` directory because agent modules aren't in PYTHONPATH
- **Solution**: Run tests from repository root: `cd /path/to/repo && PYTHONPATH=. uv run pytest scoper_shared/tests/test_orchestrator.py -v`
- Agent unit tests need proper environment setup (pytest not found in some environments)

### Next Steps
1. Run orchestrator tests from repository root with proper PYTHONPATH
2. Fix agent test environments to ensure pytest is available
3. Update test-and-eval.md with final results

## Files to Modify

1. `scoper_shared/tests/test_orchestrator.py` - Fix mock patch paths
2. `scoper_shared/pyproject.toml` - Fix package structure configuration
3. `tasks/test-and-eval.md` - Update with results after fixes

