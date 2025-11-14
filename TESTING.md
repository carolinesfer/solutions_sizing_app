# Testing Guide for Agentic Professional Services Scoper

This guide explains how to test all 4 agents in the Agentic Professional Services Scoper system.

## Quick Start

### Prerequisites

**Option 1: DataRobot LLM Gateway (Recommended)**

The agents automatically detect `INFRA_ENABLE_LLM=gateway_direct.py` and use DataRobot LLM Gateway. Set these in your `.env` file:

```bash
DATAROBOT_API_TOKEN=your-datarobot-api-token
DATAROBOT_ENDPOINT=https://app.datarobot.com/api/v2
INFRA_ENABLE_LLM=gateway_direct.py
```

**Option 2: Direct OpenAI (Fallback)**

If not using LLM Gateway, set:

```bash
OPENAI_API_KEY=your-openai-api-key
# Unset or remove INFRA_ENABLE_LLM
```

## Testing Methods

### Method 1: Automated Python Test Script (Recommended)

Tests all 4 agents in sequence with proper input/output validation:

```bash
cd requirement_analyzer_agent
PYTHONPATH=.. uv run python ../test_all_agents.py
```

**What it does:**
- Tests Requirement Analyzer → Questionnaire → Clarifier → Architecture
- Validates each agent's output schema
- Shows formatted results for each step
- Provides a summary at the end

### Method 2: Quick CLI Testing (Shell Script)

Tests each agent individually via their CLI interface:

```bash
./test_agents.sh
```

**What it does:**
- Runs each agent's CLI command with sample inputs
- Shows last 50 lines of output for each test
- Non-interactive (good for CI/CD)

### Method 3: Individual Agent Testing

Test each agent manually:

```bash
# Test Requirement Analyzer Agent
cd requirement_analyzer_agent
task cli START_DEV=1 -- execute --user_prompt '{"paragraph": "We need to build a predictive maintenance system.", "use_case_title": "Predictive Maintenance"}' --show_output

# Test Questionnaire Agent
cd ../questionnaire_agent
task cli START_DEV=1 -- execute --user_prompt '{"use_case_title": "Predictive Maintenance", "technical_confidence_score": 0.85, "key_extracted_requirements": ["Predict failures"], "domain_keywords": ["time_series"], "identified_gaps": ["Data source"]}' --show_output

# Test Clarifier Agent
cd ../clarifier_agent
task cli START_DEV=1 -- execute --user_prompt '{"questions": [{"id": "q1", "text": "Where is your data?", "type": "single_choice", "options": ["Database", "Cloud"], "required": true, "rationale": "Need data location", "tracks": ["classic_ml"]}], "selected_from_master_ids": ["q1"], "delta_questions": [], "coverage_estimate": 0.75}' --show_output

# Test Architecture Agent
cd ../architecture_agent
task cli START_DEV=1 -- execute --user_prompt '{"qas": [{"id": "q1", "answer": "Database"}], "answered_pct": 0.9, "gaps": []}' --show_output
```

### Method 4: Manual Testing via Dev Server

Start the dev server and test via HTTP:

```bash
# Terminal 1: Start dev server
cd requirement_analyzer_agent
task dev

# Terminal 2: Test via curl
curl -X POST http://localhost:8842/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DATAROBOT_API_TOKEN" \
  -d '{
    "model": "test",
    "messages": [{
      "role": "user",
      "content": "{\"paragraph\": \"We need to build a predictive maintenance system.\", \"use_case_title\": \"Predictive Maintenance\"}"
    }]
  }'
```

## Expected Outputs

### Requirement Analyzer Agent
**Input:** `UseCaseInput` (paragraph, use_case_title, optional transcript)  
**Output:** `FactExtractionModel` with:
- `use_case_title`
- `technical_confidence_score` (0.0-1.0)
- `key_extracted_requirements` (list)
- `domain_keywords` (list)
- `identified_gaps` (list)

### Questionnaire Agent
**Input:** `FactExtractionModel`  
**Output:** `QuestionnaireDraft` with:
- `questions` (list of Question objects)
- `selected_from_master_ids` (list)
- `delta_questions` (list)
- `coverage_estimate` (float)

**Note:** Requires `scoper_shared/src/scoper_shared/kb_content/master_questionnaire.json` to exist.

### Clarifier Agent
**Input:** `QuestionnaireDraft`  
**Output:** `QuestionnaireFinal` with:
- `qas` (list of Q&A pairs)
- `answered_pct` (float)
- `gaps` (list of unanswered question IDs)

### Architecture Agent
**Input:** `QuestionnaireFinal`  
**Output:** `ArchitecturePlan` with:
- `steps` (10-16 ArchitectureStep objects)
- `assumptions` (list)
- `risks` (list)
- `notes` (list)
- Plus markdown string representation

## Troubleshooting

### Authentication Errors

**Error:** `Unable to authenticate to the server`

**Solutions:**
1. Verify `DATAROBOT_API_TOKEN` and `DATAROBOT_ENDPOINT` are set correctly
2. Check that your token hasn't expired
3. Ensure `INFRA_ENABLE_LLM=gateway_direct.py` is set if using LLM Gateway

### Import Errors

**Error:** `No module named 'scoper_shared'` or `No module named 'config'`

**Solutions:**
1. Run from the correct directory (agent directory for CLI, root for Python script)
2. Ensure dependencies are installed: `task <agent>:install`
3. Set `PYTHONPATH=..` when running from agent directory

### LLM Gateway Not Working

**Error:** Agents not using DataRobot LLM Gateway

**Solutions:**
1. Verify `INFRA_ENABLE_LLM=gateway_direct.py` is in your `.env` file
2. The config validator should auto-enable `USE_DATAROBOT_LLM_GATEWAY`
3. Check that `DATAROBOT_API_TOKEN` and `DATAROBOT_ENDPOINT` are set
4. As fallback, explicitly set `USE_DATAROBOT_LLM_GATEWAY=1`

### Missing Master Questionnaire

**Error:** `FileNotFoundError: master_questionnaire.json`

**Solution:** Create a placeholder file at `scoper_shared/src/scoper_shared/kb_content/master_questionnaire.json`:
```json
[]
```

Or complete task 7.2-7.4 to extract questions from reference documents.

### Port Already in Use

**Error:** `Dev server failed to start` or port conflicts

**Solution:**
```bash
# Check what's using the port
lsof -i :8842

# Kill existing processes
pkill -f 'uv run python dev.py'
```

## Next Steps

After successful local testing:

1. **Build for LLM Playground:**
   ```bash
   task <agent>:build
   ```

2. **Deploy for Production:**
   ```bash
   task <agent>:deploy
   ```

3. **Test Deployed Agent:**
   ```bash
   task <agent>:cli -- execute-deployment --user_prompt "..." --deployment_id <id>
   ```

## File Structure

- `test_all_agents.py` - Main Python test script (tests all agents in sequence)
- `test_agents.sh` - Quick shell script for CLI testing
- `TESTING.md` - This file (consolidated testing documentation)

