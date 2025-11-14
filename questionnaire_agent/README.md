# Questionnaire Agent

The Questionnaire Agent (Agent 2) is part of the Agentic Professional Services Scoper system. This agent generates tailored questionnaires by selecting relevant questions from a Master Knowledge Base and creating new questions for identified gaps.

## Overview

The Questionnaire Agent is responsible for:
- Receiving `FactExtractionModel` from Requirement Analyzer Agent
- Selecting relevant questions from the Master Questionnaire KB based on extracted facts
- Generating new "delta questions" for identified gaps
- Calculating coverage estimate
- Outputting a validated `QuestionnaireDraft` (Pydantic schema)

## Architecture

This agent uses **pydantic-ai** as the agent framework and follows the DataRobot Agentic Workflow Application template structure.

## Key Components

- `custom_model/agent.py` - Main agent implementation using pydantic-ai
- `custom_model/custom.py` - DataRobot integration hooks (`load_model`, `chat`)
- `custom_model/config.py` - Agent configuration and environment variables
- `custom_model/helpers.py` - Utility functions, response formatting, and tool client
- `custom_model/model-metadata.yaml` - Agent metadata and runtime parameters

## Dependencies

- `pydantic-ai` - Agent framework
- `scoper_shared` - Shared schemas, utilities, and KB Retriever
- `opentelemetry-*` - Tracing and observability
- `datarobot-genai` - DataRobot GenAI integration

## Usage

### Local Development

```bash
# Install dependencies
task questionnaire_agent:install

# Run development server
task questionnaire_agent:dev

# Test agent locally
task questionnaire_agent:cli -- execute --user_prompt "Sample fact extraction model"
```

### Build and Deploy

```bash
# Build for LLM Playground testing
task questionnaire_agent:build

# Deploy for production
task questionnaire_agent:deploy

# Test deployed agent
task questionnaire_agent:cli -- execute-deployment --user_prompt "..."
```

## Input/Output

**Input:** `FactExtractionModel` schema containing:
- `use_case_title`: Title
- `technical_confidence_score`: Confidence score (0.0-1.0)
- `key_extracted_requirements`: List of technical/business needs
- `domain_keywords`: Keywords for domain routing
- `identified_gaps`: List of missing information

**Output:** `QuestionnaireDraft` schema containing:
- `questions`: List of selected and generated questions
- `selected_from_master_ids`: IDs of questions from Master KB
- `delta_questions`: New questions generated for gaps
- `coverage_estimate`: Agent's estimate of requirement coverage (0.0-1.0)

## System Prompt

The agent uses the following system prompt:
"You are a scoping specialist. You will be given a FactExtractionModel containing facts and gaps from a user's request, and a list of Master Questions from a Knowledge Base. Your task is to:
1. Select *only* the relevant questions from the Master List based on the facts provided.
2. Use the identified_gaps from the FactExtractionModel to generate new, critical 'delta_questions'.
3. Populate the rationale field for any delta questions you create.
4. You must output *only* the Pydantic QuestionnaireDraft JSON."

## Knowledge Base Integration

The agent uses `scoper_shared.utils.kb_retriever` to:
- Fetch Master Questionnaire from `scoper_shared/src/scoper_shared/kb_content/master_questionnaire.json`
- Filter questions based on domain tracks and extracted facts

## OpenTelemetry Tracing

The agent includes OpenTelemetry tracing to monitor:
- Agent execution flow
- KB retrieval operations (question selection)
- Delta question generation
- LLM API calls
- Input/output attributes
- Coverage estimation

## Related Documentation

- [DataRobot Agent Development Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-development.html)
- [DataRobot OpenTelemetry Tracing Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-tracing.html)
- [Agentic Professional Services Scoper PRD](../tasks/Solutions-Agent-PRD.md)
- [Agentic Professional Services Scoper EDD](../tasks/Solutions-Agent-Unified-EDD.md)

