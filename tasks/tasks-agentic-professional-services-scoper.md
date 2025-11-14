# Task List: Agentic Professional Services Scoper (MVP)

**Repository:** [solutions_sizing_app](https://github.com/carolinesfer/solutions_sizing_app)  
**Base Template:** Forked from [datarobot-agent-application](https://github.com/datarobot-community/datarobot-agent-application)  
**Related Documents:** 
- [PRD: Solutions-Agent-PRD-gdrive.md](./Solutions-Agent-PRD-gdrive.md)
- [EDD: Solutions-Agent-Unified-EDD-gdrive.md](./Solutions-Agent-Unified-EDD-gdrive.md)
- [DataRobot Agent Development Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-development.html)
- [DataRobot OpenTelemetry Tracing Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-tracing.html)

## Repository Context

This implementation is based on the DataRobot Agentic Workflow Application template, which provides:
- FastAPI backend (`web/`) with AG-UI protocol support
- React frontend (`frontend_web/`) with TypeScript
- Agent framework (`writer_agent/`) supporting multiple agent frameworks (LangGraph, pydantic-ai, etc.)
- MCP server (`mcp_server/`) for tool integration
- Infrastructure as Code (`infra/`) using Pulumi for DataRobot deployment

The agent implementation will use **pydantic-ai** (as shown in the example `agent.py`) rather than LangGraph, following the pattern from the provided example agent.

**Note:** The `writer_agent/` folder is an example/template for a single agent. This implementation will create **4 separate agent folders** at the repository root level, each following the `writer_agent/` structure:
- `requirement_analyzer_agent/` - Agent 1: Requirement Analyzer
- `questionnaire_agent/` - Agent 2: Questionnaire Agent  
- `clarifier_agent/` - Agent 3: Clarifier Agent
- `architecture_agent/` - Agent 4: Architecture Agent

Each agent folder will have its main agent code in `custom_model/agent.py`. Shared code (schemas, orchestrator, utils, KB content) will be in a `scoper_shared/` folder that all agents can import from.

**DataRobot Agent Development Requirements:**
According to the [DataRobot documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-development.html), each agent's `custom_model/` directory must include:
- `__init__.py` - Package initialization
- `agent.py` - Main agent implementation (MyAgent class with core workflow logic)
- `custom.py` - DataRobot integration hooks (`load_model`, `chat`) for agent execution
- `helpers.py` - Utility functions, response formatting, and tool client
- `model-metadata.yaml` - Agent configuration, runtime parameters, and deployment settings

**Testing and Deployment:**
- Local testing: `task <agent>:cli -- execute --user_prompt "..."` 
- Build for LLM Playground: `task <agent>:build`
- Deploy for production: `task <agent>:deploy`
- Test deployed agent: `task <agent>:cli -- execute-deployment --user_prompt "..."`

**OpenTelemetry Tracing:**
According to the [DataRobot tracing documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-tracing.html), OpenTelemetry instrumentation is automatically included in agent templates. Custom tracing should be added to:
- Utility functions (Domain Router, KB Retriever, RAG System) to capture execution details
- Each agent's execution flow to track intermediate outputs and tool invocations
- Orchestrator state transitions to monitor workflow execution
- Use nested spans for complex operations and events to mark important moments

## Relevant Files

### Shared Components (scoper_shared/)
- `scoper_shared/schemas.py` - All Pydantic data models (UseCaseInput, FactExtractionModel, QuestionnaireDraft, QuestionnaireFinal, ArchitecturePlan, Question, ArchitectureStep)
- `scoper_shared/orchestrator.py` - State machine orchestrator managing workflow states
- `scoper_shared/utils/domain_router.py` - Domain Router utility (U1)
- `scoper_shared/utils/kb_retriever.py` - KB Retriever utility (U2)
- `scoper_shared/utils/rag_system.py` - RAG system for Platform Guides vector search
- `scoper_shared/kb_content/master_questionnaire.json` - Master Questionnaire KB content
- `scoper_shared/kb_content/platform_guides/` - Directory for Platform Guides Markdown files
- `scoper_shared/pyproject.toml` - Shared dependencies
- `scoper_shared/tests/test_schemas.py` - Unit tests for Pydantic schemas
- `scoper_shared/tests/test_orchestrator.py` - Unit tests for state machine orchestrator
- `scoper_shared/tests/test_utils.py` - Unit tests for Domain Router and KB Retriever
- `scoper_shared/tests/test_rag.py` - Unit tests for RAG system

### Requirement Analyzer Agent (requirement_analyzer_agent/)
- `requirement_analyzer_agent/custom_model/__init__.py` - Package initialization
- `requirement_analyzer_agent/custom_model/agent.py` - RequirementAnalyzerAgent class (main MyAgent class with core workflow logic)
- `requirement_analyzer_agent/custom_model/custom.py` - DataRobot integration hooks (`load_model`, `chat`) for agent execution
- `requirement_analyzer_agent/custom_model/helpers.py` - Utility functions, response formatting, and tool client
- `requirement_analyzer_agent/custom_model/config.py` - Agent configuration
- `requirement_analyzer_agent/custom_model/model-metadata.yaml` - Agent configuration, runtime parameters, and deployment settings
- `requirement_analyzer_agent/custom_model/pyproject.toml` - Agent dependencies
- `requirement_analyzer_agent/cli.py` - CLI for agent interaction
- `requirement_analyzer_agent/dev.py` - Development server entry point
- `requirement_analyzer_agent/pyproject.toml` - Root dependencies
- `requirement_analyzer_agent/Taskfile.yml` - Agent-specific tasks
- `requirement_analyzer_agent/README.md` - Agent documentation
- `requirement_analyzer_agent/tests/test_agent.py` - Unit tests for RequirementAnalyzerAgent

### Questionnaire Agent (questionnaire_agent/)
- `questionnaire_agent/custom_model/__init__.py` - Package initialization
- `questionnaire_agent/custom_model/agent.py` - QuestionnaireAgent class (main MyAgent class with core workflow logic)
- `questionnaire_agent/custom_model/custom.py` - DataRobot integration hooks (`load_model`, `chat`) for agent execution
- `questionnaire_agent/custom_model/helpers.py` - Utility functions, response formatting, and tool client
- `questionnaire_agent/custom_model/config.py` - Agent configuration
- `questionnaire_agent/custom_model/model-metadata.yaml` - Agent configuration, runtime parameters, and deployment settings
- `questionnaire_agent/custom_model/pyproject.toml` - Agent dependencies
- `questionnaire_agent/cli.py` - CLI for agent interaction
- `questionnaire_agent/dev.py` - Development server entry point
- `questionnaire_agent/pyproject.toml` - Root dependencies
- `questionnaire_agent/Taskfile.yml` - Agent-specific tasks
- `questionnaire_agent/README.md` - Agent documentation
- `questionnaire_agent/tests/test_agent.py` - Unit tests for QuestionnaireAgent

### Clarifier Agent (clarifier_agent/)
- `clarifier_agent/custom_model/__init__.py` - Package initialization
- `clarifier_agent/custom_model/agent.py` - ClarifierAgent class (main MyAgent class with core workflow logic)
- `clarifier_agent/custom_model/custom.py` - DataRobot integration hooks (`load_model`, `chat`) for agent execution
- `clarifier_agent/custom_model/helpers.py` - Utility functions, response formatting, and tool client
- `clarifier_agent/custom_model/config.py` - Agent configuration
- `clarifier_agent/custom_model/model-metadata.yaml` - Agent configuration, runtime parameters, and deployment settings
- `clarifier_agent/custom_model/pyproject.toml` - Agent dependencies
- `clarifier_agent/cli.py` - CLI for agent interaction
- `clarifier_agent/dev.py` - Development server entry point
- `clarifier_agent/pyproject.toml` - Root dependencies
- `clarifier_agent/Taskfile.yml` - Agent-specific tasks
- `clarifier_agent/README.md` - Agent documentation
- `clarifier_agent/tests/test_agent.py` - Unit tests for ClarifierAgent

### Architecture Agent (architecture_agent/)
- `architecture_agent/custom_model/__init__.py` - Package initialization
- `architecture_agent/custom_model/agent.py` - ArchitectureAgent class (main MyAgent class with core workflow logic)
- `architecture_agent/custom_model/custom.py` - DataRobot integration hooks (`load_model`, `chat`) for agent execution
- `architecture_agent/custom_model/helpers.py` - Utility functions, response formatting, and tool client
- `architecture_agent/custom_model/config.py` - Agent configuration
- `architecture_agent/custom_model/model-metadata.yaml` - Agent configuration, runtime parameters, and deployment settings
- `architecture_agent/custom_model/pyproject.toml` - Agent dependencies
- `architecture_agent/cli.py` - CLI for agent interaction
- `architecture_agent/dev.py` - Development server entry point
- `architecture_agent/pyproject.toml` - Root dependencies
- `architecture_agent/Taskfile.yml` - Agent-specific tasks
- `architecture_agent/README.md` - Agent documentation
- `architecture_agent/tests/test_agent.py` - Unit tests for ArchitectureAgent
### Web API and Frontend
- `web/app/api/v1/scoper.py` - FastAPI router for scoper endpoints (workflow state management, clarification answers)
- `frontend_web/src/pages/Scoper.tsx` - Main scoper page component
- `frontend_web/src/components/ScoperWorkflow.tsx` - Workflow state display and progress indicator
- `frontend_web/src/components/ClarificationQuestion.tsx` - Component for displaying and answering clarification questions
- `frontend_web/src/components/QuestionnaireView.tsx` - Component for displaying final questionnaire
- `frontend_web/src/components/ArchitecturePlanView.tsx` - Component for displaying architecture plan markdown
- `frontend_web/src/api/scoper/` - API client functions for scoper endpoints

### Infrastructure
- `infra/infra/requirement_analyzer_agent.py` - Pulumi infrastructure for requirement analyzer agent
- `infra/infra/questionnaire_agent.py` - Pulumi infrastructure for questionnaire agent
- `infra/infra/clarifier_agent.py` - Pulumi infrastructure for clarifier agent
- `infra/infra/architecture_agent.py` - Pulumi infrastructure for architecture agent
- `infra/feature_flags/requirement_analyzer_agent.yaml` - Feature flag configuration
- `infra/feature_flags/questionnaire_agent.yaml` - Feature flag configuration
- `infra/feature_flags/clarifier_agent.yaml` - Feature flag configuration
- `infra/feature_flags/architecture_agent.yaml` - Feature flag configuration

## Instructions for Completing Tasks

**IMPORTANT:** As you complete each task, you must check it off in this markdown file by changing `- [ ]` to `- [x]`. This helps track progress and ensures you don't skip any steps.

Example:
- `- [ ] 1.1 Read file` → `- [x] 1.1 Read file` (after completing)

Update the file after completing each sub-task, not just after completing an entire parent task.

## Tasks

- [x] 0.0 Create feature branch
  - [x] 0.1 Create and checkout a new branch for this feature (e.g., `git checkout -b feature/agentic-professional-services-scoper`)

- [x] 0.5 Set up scoper_shared folder structure
  - [x] 0.5.1 Create `scoper_shared/` directory at repository root
  - [x] 0.5.2 Create `scoper_shared/pyproject.toml` for shared dependencies
  - [x] 0.5.3 Create `scoper_shared/utils/` directory
  - [x] 0.5.4 Create `scoper_shared/kb_content/` directory
  - [x] 0.5.5 Create `scoper_shared/tests/` directory

- [x] 0.6 Set up requirement_analyzer_agent folder structure (based on writer_agent template)
  - [x] 0.6.1 Create `requirement_analyzer_agent/` directory at repository root
  - [x] 0.6.2 Copy `writer_agent/pyproject.toml` to `requirement_analyzer_agent/pyproject.toml` and update name/description
  - [x] 0.6.3 Copy `writer_agent/Taskfile.yml` to `requirement_analyzer_agent/Taskfile.yml` and update agent-specific tasks
  - [x] 0.6.4 Copy `writer_agent/custom_model/` structure to `requirement_analyzer_agent/custom_model/` (including `__init__.py`, `helpers.py`, `config.py`)
  - [x] 0.6.5 Update `requirement_analyzer_agent/custom_model/__init__.py` (package initialization)
  - [x] 0.6.6 Update `requirement_analyzer_agent/custom_model/config.py` for requirement analyzer agent
  - [x] 0.6.7 Update `requirement_analyzer_agent/custom_model/helpers.py` if needed for utility functions, response formatting, and tool client
  - [x] 0.6.8 Update `requirement_analyzer_agent/custom_model/model-metadata.yaml` for requirement analyzer agent (agent configuration, runtime parameters, deployment settings)
  - [x] 0.6.9 Copy `writer_agent/cli.py` to `requirement_analyzer_agent/cli.py` and update
  - [x] 0.6.10 Copy `writer_agent/dev.py` to `requirement_analyzer_agent/dev.py` and update
  - [x] 0.6.11 Create `requirement_analyzer_agent/tests/` directory and copy `writer_agent/tests/conftest.py` if needed
  - [x] 0.6.12 Create `requirement_analyzer_agent/README.md` with agent documentation
  - [x] 0.6.13 Update `requirement_analyzer_agent/custom_model/pyproject.toml` with required dependencies (pydantic-ai, scoper_shared, etc.)

- [x] 0.7 Set up questionnaire_agent folder structure (based on writer_agent template)
  - [x] 0.7.1 Create `questionnaire_agent/` directory at repository root
  - [x] 0.7.2 Copy `writer_agent/pyproject.toml` to `questionnaire_agent/pyproject.toml` and update name/description
  - [x] 0.7.3 Copy `writer_agent/Taskfile.yml` to `questionnaire_agent/Taskfile.yml` and update agent-specific tasks
  - [x] 0.7.4 Copy `writer_agent/custom_model/` structure to `questionnaire_agent/custom_model/` (including `__init__.py`, `helpers.py`, `config.py`)
  - [x] 0.7.5 Update `questionnaire_agent/custom_model/__init__.py` (package initialization)
  - [x] 0.7.6 Update `questionnaire_agent/custom_model/config.py` for questionnaire agent
  - [x] 0.7.7 Update `questionnaire_agent/custom_model/helpers.py` if needed for utility functions, response formatting, and tool client
  - [x] 0.7.8 Update `questionnaire_agent/custom_model/model-metadata.yaml` for questionnaire agent (agent configuration, runtime parameters, deployment settings)
  - [x] 0.7.9 Copy `writer_agent/cli.py` to `questionnaire_agent/cli.py` and update
  - [x] 0.7.10 Copy `writer_agent/dev.py` to `questionnaire_agent/dev.py` and update
  - [x] 0.7.11 Create `questionnaire_agent/tests/` directory and copy `writer_agent/tests/conftest.py` if needed
  - [x] 0.7.12 Create `questionnaire_agent/README.md` with agent documentation
  - [x] 0.7.13 Update `questionnaire_agent/custom_model/pyproject.toml` with required dependencies (pydantic-ai, scoper_shared, etc.)

- [x] 0.8 Set up clarifier_agent folder structure (based on writer_agent template)
  - [x] 0.8.1 Create `clarifier_agent/` directory at repository root
  - [x] 0.8.2 Copy `writer_agent/pyproject.toml` to `clarifier_agent/pyproject.toml` and update name/description
  - [x] 0.8.3 Copy `writer_agent/Taskfile.yml` to `clarifier_agent/Taskfile.yml` and update agent-specific tasks
  - [x] 0.8.4 Copy `writer_agent/custom_model/` structure to `clarifier_agent/custom_model/` (including `__init__.py`, `helpers.py`, `config.py`)
  - [x] 0.8.5 Update `clarifier_agent/custom_model/__init__.py` (package initialization)
  - [x] 0.8.6 Update `clarifier_agent/custom_model/config.py` for clarifier agent
  - [x] 0.8.7 Update `clarifier_agent/custom_model/helpers.py` if needed for utility functions, response formatting, and tool client
  - [x] 0.8.8 Update `clarifier_agent/custom_model/model-metadata.yaml` for clarifier agent (agent configuration, runtime parameters, deployment settings)
  - [x] 0.8.9 Copy `writer_agent/cli.py` to `clarifier_agent/cli.py` and update
  - [x] 0.8.10 Copy `writer_agent/dev.py` to `clarifier_agent/dev.py` and update
  - [x] 0.8.11 Create `clarifier_agent/tests/` directory and copy `writer_agent/tests/conftest.py` if needed
  - [x] 0.8.12 Create `clarifier_agent/README.md` with agent documentation
  - [x] 0.8.13 Update `clarifier_agent/custom_model/pyproject.toml` with required dependencies (pydantic-ai, scoper_shared, etc.)

- [x] 0.9 Set up architecture_agent folder structure (based on writer_agent template)
  - [x] 0.9.1 Create `architecture_agent/` directory at repository root
  - [x] 0.9.2 Copy `writer_agent/pyproject.toml` to `architecture_agent/pyproject.toml` and update name/description
  - [x] 0.9.3 Copy `writer_agent/Taskfile.yml` to `architecture_agent/Taskfile.yml` and update agent-specific tasks
  - [x] 0.9.4 Copy `writer_agent/custom_model/` structure to `architecture_agent/custom_model/` (including `__init__.py`, `helpers.py`, `config.py`)
  - [x] 0.9.5 Update `architecture_agent/custom_model/__init__.py` (package initialization)
  - [x] 0.9.6 Update `architecture_agent/custom_model/config.py` for architecture agent
  - [x] 0.9.7 Update `architecture_agent/custom_model/helpers.py` if needed for utility functions, response formatting, and tool client
  - [x] 0.9.8 Update `architecture_agent/custom_model/model-metadata.yaml` for architecture agent (agent configuration, runtime parameters, deployment settings)
  - [x] 0.9.9 Copy `writer_agent/cli.py` to `architecture_agent/cli.py` and update
  - [x] 0.9.10 Copy `writer_agent/dev.py` to `architecture_agent/dev.py` and update
  - [x] 0.9.11 Create `architecture_agent/tests/` directory and copy `writer_agent/tests/conftest.py` if needed
  - [x] 0.9.12 Create `architecture_agent/README.md` with agent documentation
  - [x] 0.9.13 Update `architecture_agent/custom_model/pyproject.toml` with required dependencies (pydantic-ai, scoper_shared, etc.)

- [x] 1.0 Set up Pydantic data models and schemas (in scoper_shared)
  - [x] 1.1 Create `scoper_shared/schemas.py` file
  - [x] 1.2 Implement `UseCaseInput` schema with `paragraph`, `transcript` (optional), and `use_case_title` fields
  - [x] 1.3 Implement `FactExtractionModel` schema with `use_case_title`, `technical_confidence_score`, `key_extracted_requirements`, `domain_keywords`, and `identified_gaps` fields
  - [x] 1.4 Implement `Question` schema with `id`, `text`, `type` (Literal), `options`, `required`, `rationale`, and `tracks` fields
  - [x] 1.5 Implement `ArchitectureStep` schema with `id`, `name`, `purpose`, `inputs`, and `outputs` fields
  - [x] 1.6 Implement `QuestionnaireDraft` schema with `questions`, `selected_from_master_ids`, `delta_questions`, and `coverage_estimate` fields
  - [x] 1.7 Implement `QuestionnaireFinal` schema with `qas`, `answered_pct`, and `gaps` fields
  - [x] 1.8 Implement `ArchitecturePlan` schema with `steps` (10-16 items), `assumptions`, `risks`, and `notes` fields
  - [x] 1.9 Add Google-style docstrings to all schemas explaining their purpose and usage
  - [x] 1.10 Create unit tests for schema validation in `scoper_shared/tests/test_schemas.py`

- [x] 2.0 Implement Knowledge Base infrastructure (KB Retriever and Domain Router in scoper_shared)
  - [x] 2.1 Create `scoper_shared/utils/__init__.py` file
  - [x] 2.2 Implement `scoper_shared/utils/domain_router.py` with `domain_router()` function that takes `FactExtractionModel` and returns list of track strings
  - [x] 2.3 Add keyword matching logic for tracks: `time_series`, `nlp`, `cv`, `genai_rag`, and default `classic_ml`
  - [x] 2.4 Add OpenTelemetry tracing to `domain_router()` function: create span "domain_router", set attributes for input FactExtractionModel fields, selected tracks, add event when routing completes
  - [x] 2.5 Create `scoper_shared/utils/kb_retriever.py` with `KBRetriever` class
  - [x] 2.6 Implement `get_master_questionnaire()` method that reads JSON file from `scoper_shared/kb_content/master_questionnaire.json` and parses into list of `Question` objects
  - [x] 2.7 Add OpenTelemetry tracing to `get_master_questionnaire()`: create span "kb_retriever.get_master_questionnaire", set attributes for file path, question count, add event when parsing completes
  - [x] 2.8 Implement `get_platform_guides()` method that loads Markdown files from `scoper_shared/kb_content/platform_guides/` directory
  - [x] 2.9 Add filtering logic to return guides based on selected tracks
  - [x] 2.10 Add OpenTelemetry tracing to `get_platform_guides()`: create span "kb_retriever.get_platform_guides", set attributes for selected tracks, number of guides found, file paths, add event when filtering completes
  - [x] 2.11 Create unit tests for `domain_router()` function in `scoper_shared/tests/test_utils.py`
  - [x] 2.12 Create unit tests for `KBRetriever` class in `scoper_shared/tests/test_utils.py`

- [x] 3.0 Implement Requirement Analyzer Agent
  - [x] 3.1 Implement `requirement_analyzer_agent/custom_model/agent.py` with `RequirementAnalyzerAgent` class using pydantic-ai (main MyAgent class with core workflow logic)
  - [x] 3.2 Configure Agent 1 system prompt in `agent.py`: "You are a senior solutions architect. Your sole task is to read the following user query and transcript and extract key information..."
  - [x] 3.3 Implement `run()` method that takes `UseCaseInput` and returns `FactExtractionModel` (validated Pydantic JSON)
  - [x] 3.4 Add OpenTelemetry tracing to `run()` method: create span "requirement_analyzer.run", set attributes for input use_case_title, paragraph length, transcript length, add nested span for LLM call, set attributes for output technical_confidence_score, number of requirements extracted, number of gaps identified, add event when extraction completes
  - [x] 3.5 Import schemas from `scoper_shared.schemas`
  - [x] 3.6 Update `requirement_analyzer_agent/custom_model/custom.py` to implement DataRobot integration hooks (`load_model`, `chat`) for agent execution (OpenTelemetry instrumentation is already included in template)
  - [x] 3.7 Update `requirement_analyzer_agent/custom_model/helpers.py` if needed for utility functions, response formatting, and tool client
  - [ ] 3.8 Test agent locally using `task requirement_analyzer_agent:cli -- execute --user_prompt "Sample use case description"`
  - [x] 3.9 Create unit tests in `requirement_analyzer_agent/tests/test_agent.py`

- [x] 3.2 Implement Questionnaire Agent
  - [x] 3.2.1 Implement `questionnaire_agent/custom_model/agent.py` with `QuestionnaireAgent` class using pydantic-ai (main MyAgent class with core workflow logic)
  - [x] 3.2.2 Configure Agent 2 system prompt in `agent.py`: "You are a scoping specialist. You will be given a FactExtractionModel..."
  - [x] 3.2.3 Implement `run()` method that takes `FactExtractionModel` and Master Questions, returns `QuestionnaireDraft`
  - [x] 3.2.4 Add logic to select relevant questions from Master KB (via scoper_shared.utils.kb_retriever) and generate delta_questions for gaps
  - [x] 3.2.5 Add OpenTelemetry tracing to `run()` method: create span "questionnaire_agent.run", set attributes for input FactExtractionModel fields, create nested span "question_selection" for KB retrieval, set attributes for number of master questions available, number selected, create nested span "delta_question_generation" for gap questions, set attributes for number of gaps, delta questions generated, coverage_estimate, add event when questionnaire draft completes
  - [x] 3.2.6 Import schemas from `scoper_shared.schemas` and utils from `scoper_shared.utils`
  - [x] 3.2.7 Update `questionnaire_agent/custom_model/custom.py` to implement DataRobot integration hooks (`load_model`, `chat`) for agent execution (OpenTelemetry instrumentation is already included in template)
  - [x] 3.2.8 Update `questionnaire_agent/custom_model/helpers.py` if needed for utility functions, response formatting, and tool client
  - [ ] 3.2.9 Test agent locally using `task questionnaire_agent:cli -- execute --user_prompt "Sample fact extraction model"`
  - [x] 3.2.10 Create unit tests in `questionnaire_agent/tests/test_agent.py`

- [x] 3.3 Implement Clarifier Agent
  - [x] 3.3.1 Implement `clarifier_agent/custom_model/agent.py` with `ClarifierAgent` class using pydantic-ai (main MyAgent class with core workflow logic)
  - [x] 3.3.2 Configure Agent 3 system prompt in `agent.py`: "You are an interviewer. You will be given a QuestionnaireDraft..."
  - [x] 3.3.3 Implement `ask_question()` method that asks one question at a time (up to K=5), preferring single-choice or boolean
  - [x] 3.3.4 Add OpenTelemetry tracing to `ask_question()` method: create span "clarifier_agent.ask_question", set attributes for question number, question ID, question type, add event when question is asked, add event when answer is received, set attributes for answer value
  - [x] 3.3.5 Implement `finalize()` method that compiles all Q&A pairs into `QuestionnaireFinal`
  - [x] 3.3.6 Add OpenTelemetry tracing to `finalize()` method: create span "clarifier_agent.finalize", set attributes for total questions asked, answered count, unanswered count, answered_pct, gaps list, add event when finalization completes
  - [x] 3.3.7 Import schemas from `scoper_shared.schemas`
  - [x] 3.3.8 Update `clarifier_agent/custom_model/custom.py` to implement DataRobot integration hooks (`load_model`, `chat`) for agent execution (OpenTelemetry instrumentation is already included in template)
  - [x] 3.3.9 Update `clarifier_agent/custom_model/helpers.py` if needed for utility functions, response formatting, and tool client
  - [ ] 3.3.10 Test agent locally using `task clarifier_agent:cli -- execute --user_prompt "Sample questionnaire draft"`
  - [x] 3.3.11 Create unit tests in `clarifier_agent/tests/test_agent.py`

- [x] 3.4 Implement Architecture Agent
  - [x] 3.4.1 Implement `architecture_agent/custom_model/agent.py` with `ArchitectureAgent` class using pydantic-ai (main MyAgent class with core workflow logic)
  - [x] 3.4.2 Configure Agent 4 system prompt in `agent.py`: "You are a master solutions architect. You will be given a QuestionnaireFinal..."
  - [x] 3.4.3 Implement `run()` method that takes `QuestionnaireFinal` and RAG context, returns `ArchitecturePlan` and Markdown string
  - [x] 3.4.4 Ensure Agent 4 generates 10-16 steps with inputs/outputs fields populated
  - [x] 3.4.5 Add OpenTelemetry tracing to `run()` method: create span "architecture_agent.run", set attributes for input QuestionnaireFinal fields, create nested span "rag_context_retrieval" for RAG search, set attributes for query, number of chunks retrieved, create nested span "architecture_generation" for LLM call, set attributes for number of steps generated, number of assumptions, number of risks, add event when architecture plan completes
  - [x] 3.4.6 Import schemas from `scoper_shared.schemas` and RAG system from `scoper_shared.utils.rag_system`
  - [x] 3.4.7 Update `architecture_agent/custom_model/custom.py` to implement DataRobot integration hooks (`load_model`, `chat`) for agent execution (OpenTelemetry instrumentation is already included in template)
  - [x] 3.4.8 Update `architecture_agent/custom_model/helpers.py` if needed for utility functions, response formatting, and tool client
  - [ ] 3.4.9 Test agent locally using `task architecture_agent:cli -- execute --user_prompt "Sample questionnaire final"`
  - [x] 3.4.10 Create unit tests in `architecture_agent/tests/test_agent.py`

- [x] 4.0 Implement state machine orchestrator (in scoper_shared)
  - [x] 4.1 Create `scoper_shared/orchestrator.py` file
  - [x] 4.2 Define state enum: `INGEST`, `ANALYZE`, `ROUTE`, `KB_FETCH`, `Q_DRAFT`, `Q_CLARIFY`, `Q_FREEZE`, `PLAN_ARCH`, `DONE`
  - [x] 4.3 Implement `Orchestrator` class with state management
  - [x] 4.4 Add OpenTelemetry tracing setup: import `opentelemetry.trace`, create tracer, ensure OpenTelemetry instrumentation is available
  - [x] 4.5 Implement `INGEST` state handler that receives and validates `UseCaseInput` with tracing: create span "orchestrator.ingest", set attributes for input validation, add event when validation completes
  - [x] 4.6 Implement `ANALYZE` state handler that calls Requirement Analyzer Agent (import from requirement_analyzer_agent) with tracing: create span "orchestrator.analyze", set attributes for agent call, add nested span for agent execution, add event when analysis completes
  - [x] 4.7 Implement `ROUTE` state handler that calls Domain Router utility (from scoper_shared.utils) with tracing: create span "orchestrator.route", set attributes for selected tracks, add event when routing completes
  - [x] 4.8 Implement `KB_FETCH` state handler that calls KB Retriever utility (from scoper_shared.utils) with tracing: create span "orchestrator.kb_fetch", set attributes for KB retrieval, add nested span for KB operations, add event when KB fetch completes
  - [x] 4.9 Implement `Q_DRAFT` state handler that calls Questionnaire Agent (import from questionnaire_agent) with tracing: create span "orchestrator.q_draft", set attributes for agent call, add nested span for agent execution, add event when draft completes
  - [x] 4.10 Implement `Q_CLARIFY` state handler that manages bounded loop with Clarifier Agent (≤K questions, import from clarifier_agent) with tracing: create span "orchestrator.q_clarify", set attributes for clarification loop, add nested spans for each question iteration, set attributes for questions asked, answers received, add event when clarification loop completes
  - [x] 4.11 Implement `Q_FREEZE` gate condition: proceed only if ≥80% answered OR coverage ≥0.8 with tracing: create span "orchestrator.q_freeze", set attributes for answered_pct, coverage_estimate, gate decision, add event when gate evaluation completes
  - [x] 4.12 Implement `PLAN_ARCH` state handler that calls Architecture Agent with RAG context (import from architecture_agent) with tracing: create span "orchestrator.plan_arch", set attributes for agent call, RAG context size, add nested span for agent execution, add event when architecture generation completes
  - [x] 4.13 Implement `DONE` state handler that returns both artifacts (QuestionnaireFinal and ArchitecturePlan) with tracing: create span "orchestrator.done", set attributes for final artifacts, add event when workflow completes
  - [x] 4.14 Add top-level workflow tracing: create main span "scoper_workflow" that encompasses entire workflow, with nested spans for each state transition
  - [x] 4.15 Add error handling and retry logic for each state transition with tracing: set error attributes on spans, add error events
  - [x] 4.16 Add schema validation before each state transition (import from scoper_shared.schemas) with tracing: add validation spans with attributes for validation results
  - [x] 4.17 Create unit tests for orchestrator state transitions in `scoper_shared/tests/test_orchestrator.py`

- [x] 5.0 Integrate agent with web API and frontend
  - [x] 5.1 Create a main orchestrator entry point (could be in scoper_shared or a separate orchestrator service)
  - [x] 5.2 The orchestrator will coordinate calls to all 4 agents (requirement_analyzer_agent, questionnaire_agent, clarifier_agent, architecture_agent)
  - [x] 5.3 Create `web/app/api/v1/scoper.py` FastAPI router
  - [x] 5.4 Implement `POST /api/v1/scoper/start` endpoint that accepts `UseCaseInput` and initiates workflow
  - [x] 5.5 Implement `GET /api/v1/scoper/{workflow_id}/state` endpoint to get current workflow state
  - [x] 5.6 Implement `POST /api/v1/scoper/{workflow_id}/clarify` endpoint to submit clarification answers
  - [x] 5.7 Implement `GET /api/v1/scoper/{workflow_id}/results` endpoint to retrieve final artifacts
  - [x] 5.8 Add workflow state persistence (store in database or session)
  - [x] 5.9 Create `frontend_web/src/api/scoper/` directory and API client functions
  - [x] 5.10 Implement `startScoping()`, `getWorkflowState()`, `submitClarification()`, `getResults()` API functions
  - [x] 5.11 Create `frontend_web/src/pages/Scoper.tsx` main page component
  - [x] 5.12 Create `frontend_web/src/components/ScoperWorkflow.tsx` to display workflow state and progress
  - [x] 5.13 Create `frontend_web/src/components/ClarificationQuestion.tsx` for displaying and answering questions one at a time
  - [x] 5.14 Create `frontend_web/src/components/QuestionnaireView.tsx` to display final questionnaire as structured Q&As
  - [x] 5.15 Create `frontend_web/src/components/ArchitecturePlanView.tsx` to render architecture plan markdown
  - [x] 5.16 Add download buttons for Questionnaire (JSON) and ArchitecturePlan (Markdown)
  - [x] 5.17 Add route configuration in `frontend_web/src/routesConfig.tsx` for `/scoper` path
  - [ ] 5.18 Create integration tests for API endpoints in `web/tests/integration/test_scoper.py`
  - [ ] 5.19 Create `infra/infra/requirement_analyzer_agent.py` for Pulumi deployment (based on `infra/infra/writer_agent.py`)
  - [ ] 5.20 Create `infra/infra/questionnaire_agent.py` for Pulumi deployment
  - [ ] 5.21 Create `infra/infra/clarifier_agent.py` for Pulumi deployment
  - [ ] 5.22 Create `infra/infra/architecture_agent.py` for Pulumi deployment
  - [ ] 5.23 Create `infra/feature_flags/requirement_analyzer_agent.yaml` for feature flag configuration
  - [ ] 5.24 Create `infra/feature_flags/questionnaire_agent.yaml` for feature flag configuration
  - [ ] 5.25 Create `infra/feature_flags/clarifier_agent.yaml` for feature flag configuration
  - [ ] 5.26 Create `infra/feature_flags/architecture_agent.yaml` for feature flag configuration
  - [ ] 5.27 Update root `Taskfile.yml` to include all agent tasks if needed
  - [ ] 5.28 Build each agent for testing in DataRobot LLM Playground using `task requirement_analyzer_agent:build`, `task questionnaire_agent:build`, `task clarifier_agent:build`, `task architecture_agent:build`
  - [ ] 5.29 Deploy each agent for production use using `task requirement_analyzer_agent:deploy`, `task questionnaire_agent:deploy`, `task clarifier_agent:deploy`, `task architecture_agent:deploy`
  - [ ] 5.30 Test deployed agents using `task requirement_analyzer_agent:cli -- execute-deployment --user_prompt "..."` (and similar for other agents)

- [ ] 6.0 Set up RAG system for Platform Guides (in scoper_shared)
  - [ ] 6.1 Create `scoper_shared/utils/rag_system.py` file
  - [ ] 6.2 Install and configure FAISS or Chroma library in `scoper_shared/pyproject.toml`
  - [ ] 6.3 Implement `RAGSystem` class with vector store initialization
  - [ ] 6.4 Implement `load_documents()` method that reads Markdown files from `scoper_shared/kb_content/platform_guides/` and chunks them
  - [ ] 6.5 Add OpenTelemetry tracing to `load_documents()`: create span "rag_system.load_documents", set attributes for number of files loaded, total chunks created, add nested spans for file reading and chunking operations, add event when loading completes
  - [ ] 6.6 Implement `embed_documents()` method that creates embeddings for document chunks
  - [ ] 6.7 Add OpenTelemetry tracing to `embed_documents()`: create span "rag_system.embed_documents", set attributes for number of chunks embedded, embedding model used, add nested span for embedding API calls, add event when embedding completes
  - [ ] 6.8 Implement `search()` method that takes query (from QuestionnaireFinal) and returns top N relevant chunks
  - [ ] 6.9 Add OpenTelemetry tracing to `search()`: create span "rag_system.search", set attributes for query text, query length, top N requested, create nested span "vector_search" for similarity search, set attributes for number of results returned, similarity scores, add event when search completes
  - [ ] 6.10 Architecture Agent will import and use RAG system from `scoper_shared.utils.rag_system` to provide context before generation
  - [ ] 6.11 Add configuration for embedding model (use DataRobot LLM Gateway or external provider)
  - [ ] 6.12 Create unit tests for RAG system in `scoper_shared/tests/test_rag.py`
  - [ ] 6.13 Test RAG retrieval with sample queries and verify relevant context is returned

- [ ] 7.0 Create initial Knowledge Base content (Master Questionnaires and Platform Guides in scoper_shared)
  - [ ] 7.1 Create `scoper_shared/kb_content/platform_guides/` directory
  - [ ] 7.2 Extract questions from referenced Google Sheets/Docs (SCOPING MASTER SHEET, APP QUESTIONNAIRES, etc.)
  - [ ] 7.3 Convert extracted questions to JSON format matching `Question` schema
  - [ ] 7.4 Create `scoper_shared/kb_content/master_questionnaire.json` file with all questions, including `tracks` field for domain filtering
  - [ ] 7.5 Extract content from Internal Platform Guides (DataRobot docs, GitHub repos, presentations)
  - [ ] 7.6 Convert platform guide content to Markdown format
  - [ ] 7.7 Organize platform guides by domain/track (time_series.md, nlp.md, cv.md, genai_rag.md, classic_ml.md) in `scoper_shared/kb_content/platform_guides/`
  - [ ] 7.8 Create placeholder/example content if source documents are not immediately available
  - [ ] 7.9 Document the KB content structure and update process in `scoper_shared/kb_content/README.md`

