# Requirement Analyzer Agent

The Requirement Analyzer Agent (Agent 1) is part of the Agentic Professional Services Scoper system. This agent extracts facts, requirements, and identifies gaps from raw user input (use case descriptions and transcripts).

## Overview

The Requirement Analyzer Agent is responsible for:
- Reading user queries and transcripts
- Extracting key technical requirements
- Identifying domain keywords (e.g., 'time series', 'nlp', 'images', 'agentic')
- Identifying informational gaps
- Outputting a validated `FactExtractionModel` (Pydantic schema)

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
task requirement_analyzer_agent:install

# Run development server
task requirement_analyzer_agent:dev

# Test agent locally
task requirement_analyzer_agent:cli -- execute --user_prompt "Sample use case description"
```

### Build and Deploy

```bash
# Build for LLM Playground testing
task requirement_analyzer_agent:build

# Deploy for production
task requirement_analyzer_agent:deploy

# Test deployed agent
task requirement_analyzer_agent:cli -- execute-deployment --user_prompt "..."
```

## Input/Output

**Input:** `UseCaseInput` schema containing:
- `paragraph`: Raw text description
- `transcript`: Optional call transcript
- `use_case_title`: Title of the use case

**Output:** `FactExtractionModel` schema containing:
- `use_case_title`: Title
- `technical_confidence_score`: Confidence score (0.0-1.0)
- `key_extracted_requirements`: List of technical/business needs
- `domain_keywords`: Keywords for domain routing
- `identified_gaps`: List of missing information

## System Prompt

The agent uses the following system prompt:
"You are a senior solutions architect. Your sole task is to read the following user query and transcript and extract key information. Identify the core goal, all technical requirements, any mentioned data sources, and any clear informational gaps. You must output *only* the Pydantic FactExtractionModel JSON. Do not add conversational text. Pay special attention to keywords that suggest the project domain (e.g., 'forecast', 'time series', 'NLP', 'images', 'agentic')."

## OpenTelemetry Tracing

The agent includes OpenTelemetry tracing to monitor:
- Agent execution flow
- LLM API calls
- Input/output attributes
- Intermediate outputs

## Related Documentation

- [DataRobot Agent Development Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-development.html)
- [DataRobot OpenTelemetry Tracing Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-tracing.html)
- [Agentic Professional Services Scoper PRD](../tasks/Solutions-Agent-PRD.md)
- [Agentic Professional Services Scoper EDD](../tasks/Solutions-Agent-Unified-EDD.md)

