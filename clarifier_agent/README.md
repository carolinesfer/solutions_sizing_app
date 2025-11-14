# Clarifier Agent

The Clarifier Agent (Agent 3) is part of the Agentic Professional Services Scoper system. This agent conducts a bounded clarification loop (up to K questions, e.g., K=5) to fill high-impact gaps through user interaction.

## Overview

The Clarifier Agent is responsible for:
- Receiving `QuestionnaireDraft` from Questionnaire Agent
- Asking questions one at a time (up to K=5) to the user
- Preferring single-choice or boolean questions for efficiency
- Tracking Q&A pairs during the clarification loop
- Compiling all Q&A pairs into `QuestionnaireFinal` when complete
- Outputting a validated `QuestionnaireFinal` (Pydantic schema)

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
- `scoper_shared` - Shared schemas and utilities
- `opentelemetry-*` - Tracing and observability
- `datarobot-genai` - DataRobot GenAI integration

## Usage

### Local Development

```bash
# Install dependencies
task clarifier_agent:install

# Run development server
task clarifier_agent:dev

# Test agent locally
task clarifier_agent:cli -- execute --user_prompt "Sample questionnaire draft"
```

### Build and Deploy

```bash
# Build for LLM Playground testing
task clarifier_agent:build

# Deploy for production
task clarifier_agent:deploy

# Test deployed agent
task clarifier_agent:cli -- execute-deployment --user_prompt "..."
```

## Input/Output

**Input:** `QuestionnaireDraft` schema containing:
- `questions`: List of selected and generated questions
- `selected_from_master_ids`: IDs of questions from Master KB
- `delta_questions`: New questions generated for gaps
- `coverage_estimate`: Agent's estimate of requirement coverage (0.0-1.0)

**Output:** `QuestionnaireFinal` schema containing:
- `qas`: List of Q&A pairs (e.g., `{'id': 'q1', 'answer': 'value'}`)
- `answered_pct`: Percentage of questions answered (0.0-1.0)
- `gaps`: List of question IDs that remain unanswered

## System Prompt

The agent uses the following system prompt:
"You are an interviewer. You will be given a QuestionnaireDraft and a list of current answers. Your goal is to fill the remaining high-impact gaps. Ask up to K (e.g., K=5) high-value follow-up questions to the user, one at a time. Prefer single-choice or boolean questions. Once the loop is complete, compile all Q&A pairs and output *only* the Pydantic QuestionnaireFinal JSON."

## Key Methods

- `ask_question()`: Asks one question at a time (up to K=5), preferring single-choice or boolean questions
- `finalize()`: Compiles all Q&A pairs into `QuestionnaireFinal`

## OpenTelemetry Tracing

The agent includes OpenTelemetry tracing to monitor:
- Agent execution flow
- Question asking iterations (question number, question ID, question type)
- Answer receiving events
- Finalization process (total questions asked, answered count, unanswered count)
- LLM API calls
- Input/output attributes

## Related Documentation

- [DataRobot Agent Development Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-development.html)
- [DataRobot OpenTelemetry Tracing Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-tracing.html)
- [Agentic Professional Services Scoper PRD](../tasks/Solutions-Agent-PRD.md)
- [Agentic Professional Services Scoper EDD](../tasks/Solutions-Agent-Unified-EDD.md)

