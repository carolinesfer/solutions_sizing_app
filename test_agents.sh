#!/bin/bash
# Unified test script for all 4 agents
# Tests each agent via CLI with sample inputs

set -e

echo "🧪 Testing All 4 Agents"
echo "======================"
echo ""

# Check if DataRobot credentials are set
if [ -z "$DATAROBOT_API_TOKEN" ] || [ -z "$DATAROBOT_ENDPOINT" ]; then
    echo "⚠️  WARNING: DATAROBOT_API_TOKEN or DATAROBOT_ENDPOINT not set"
    echo "   The agents will try to use DataRobot LLM Gateway if INFRA_ENABLE_LLM=gateway_direct.py"
    echo "   Make sure your credentials are configured in .env or environment"
    echo ""
fi

# Test 1: Requirement Analyzer Agent
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Requirement Analyzer Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cd requirement_analyzer_agent
task cli START_DEV=1 -- execute --user_prompt '{"paragraph": "We need to build a predictive maintenance system for industrial equipment. The system should analyze sensor data from machines to predict failures before they occur.", "use_case_title": "Predictive Maintenance System"}' --show_output 2>&1 | tail -50 || echo "⚠️  Test 1 had issues"
cd ..
echo ""

# Test 2: Questionnaire Agent  
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: Questionnaire Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cd questionnaire_agent
task cli START_DEV=1 -- execute --user_prompt '{"use_case_title": "Predictive Maintenance", "technical_confidence_score": 0.85, "key_extracted_requirements": ["Predict failures", "Analyze sensor data"], "domain_keywords": ["time_series"], "identified_gaps": ["Data source"]}' --show_output 2>&1 | tail -50 || echo "⚠️  Test 2 had issues"
cd ..
echo ""

# Test 3: Clarifier Agent
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: Clarifier Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cd clarifier_agent
task cli START_DEV=1 -- execute --user_prompt '{"questions": [{"id": "q1", "text": "Where is your data?", "type": "single_choice", "options": ["Database", "Cloud"], "required": true, "rationale": "Need data location", "tracks": ["classic_ml"]}], "selected_from_master_ids": ["q1"], "delta_questions": [], "coverage_estimate": 0.75}' --show_output 2>&1 | tail -50 || echo "⚠️  Test 3 had issues"
cd ..
echo ""

# Test 4: Architecture Agent
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: Architecture Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cd architecture_agent
task cli START_DEV=1 -- execute --user_prompt '{"qas": [{"id": "q1", "answer": "Database"}], "answered_pct": 0.9, "gaps": []}' --show_output 2>&1 | tail -50 || echo "⚠️  Test 4 had issues"
cd ..
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All tests completed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Tip: For more detailed testing with validation, use:"
echo "   cd requirement_analyzer_agent && PYTHONPATH=.. uv run python ../test_all_agents.py"

