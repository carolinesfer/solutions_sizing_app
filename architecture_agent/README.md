# Architecture Agent

The Architecture Agent (Agent 4) is part of the Agentic Professional Services Scoper system. This agent generates solution architecture plans using validated requirements and RAG context from internal platform guides.

## Overview

The Architecture Agent is responsible for:
- Receiving `QuestionnaireFinal` from Clarifier Agent
- Retrieving relevant context from Internal Platform Guides using RAG system
- Generating a step-by-step implementation plan (10-16 steps)
- Populating inputs and outputs fields for each step
- Identifying key assumptions and risks
- Outputting a validated `ArchitecturePlan` (Pydantic schema) and Markdown string

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
- `scoper_shared` - Shared schemas, utilities, and RAG system
- `opentelemetry-*` - Tracing and observability
- `datarobot-genai` - DataRobot GenAI integration

## Usage

### Local Development

```bash
# Install dependencies
task architecture_agent:install

# Run development server
task architecture_agent:dev

# Test agent locally
task architecture_agent:cli -- execute --user_prompt "Sample questionnaire final"
```

### Build and Deploy

```bash
# Build for LLM Playground testing
task architecture_agent:build

# Deploy for production
task architecture_agent:deploy

# Test deployed agent
task architecture_agent:cli -- execute-deployment --user_prompt "..."
```

## Input/Output

**Input:** `QuestionnaireFinal` schema containing:
- `qas`: List of Q&A pairs (e.g., `{'id': 'q1', 'answer': 'value'}`)
- `answered_pct`: Percentage of questions answered (0.0-1.0)
- `gaps`: List of question IDs that remain unanswered

**Output:** `ArchitecturePlan` schema containing:
- `steps`: List of 10-16 architecture steps, each with:
  - `id`: Step identifier
  - `name`: Name of the step (e.g., 'Data Ingestion')
  - `purpose`: Purpose of this step
  - `inputs`: List of inputs to this step
  - `outputs`: List of outputs from this step
- `assumptions`: List of key assumptions
- `risks`: List of identified risks
- `notes`: Optional notes

Also outputs a Markdown string representation of the architecture plan.

## System Prompt

The agent uses the following system prompt:
"You are a master solutions architect. You will be given a QuestionnaireFinal with validated user requirements and RAG context from our Internal Platform Guides. Your task is to generate a step-by-step implementation plan.
1. The plan must have between 10-16 steps covering data ingest, preprocessing, modeling, evaluation, deployment, and monitoring.
2. Ground your recommendations in the provided RAG context.
3. Identify key assumptions and risks.
4. For each step, you *must* populate the `inputs` and `outputs` fields with brief, clear descriptions (e.g., 'Inputs: Raw customer data', 'Outputs: Cleansed data frame')
5. You must output *only* the Pydantic ArchitecturePlan JSON."

## RAG Integration

The agent uses `scoper_shared.utils.rag_system` to:
- Search Internal Platform Guides for relevant context
- Retrieve top N relevant chunks based on the QuestionnaireFinal
- Provide grounded recommendations based on DataRobot best practices

## OpenTelemetry Tracing

The agent includes OpenTelemetry tracing to monitor:
- Agent execution flow
- RAG context retrieval (query, number of chunks retrieved)
- Architecture generation (number of steps, assumptions, risks)
- LLM API calls
- Input/output attributes

## Related Documentation

- [DataRobot Agent Development Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-development.html)
- [DataRobot OpenTelemetry Tracing Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-tracing.html)
- [Agentic Professional Services Scoper PRD](../tasks/Solutions-Agent-PRD.md)
- [Agentic Professional Services Scoper EDD](../tasks/Solutions-Agent-Unified-EDD.md)

