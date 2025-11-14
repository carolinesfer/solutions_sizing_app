<p align="center">
  <a href="https://github.com/carolinesfer/solutions_sizing_app">
    <img src="./.github/datarobot_logo.avif" width="600px" alt="DataRobot Logo"/>
  </a>
</p>
<p align="center">
    <span style="font-size: 1.5em; font-weight: bold; display: block;">Agentic Professional Services Scoper</span>
</p>

<p align="center">
  <a href="https://datarobot.com">Homepage</a>
  ·
  <a href="https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/index.html">Documentation</a>
  ·
  <a href="https://docs.datarobot.com/en/docs/get-started/troubleshooting/general-help.html">Support</a>
</p>

<p align="center">
  <a href="https://github.com/carolinesfer/solutions_sizing_app">
    <img src="https://img.shields.io/github/v/tag/carolinesfer/solutions_sizing_app?label=version" alt="Latest Release">
  </a>
  <a href="/LICENSE.txt">
    <img src="https://img.shields.io/github/license/carolinesfer/solutions_sizing_app" alt="License">
  </a>
</p>

## 📖 Overview

The **Agentic Professional Services Scoper** is an AI-powered system that standardizes and accelerates the Professional Services scoping process. It consumes initial customer requirements and rapidly generates high-quality, DataRobot-contextualized solution designs and questionnaires.

This application is built on the [DataRobot Agentic Workflow Application template](https://github.com/datarobot-community/datarobot-agent-application) and implements a **4-agent pipeline** using **pydantic-ai** to extract requirements, generate tailored questionnaires, conduct clarification loops, and produce solution architecture plans.

### ✨ Key Features

- **Multi-Agent Architecture**: Four specialized agents working in sequence to scope Professional Services engagements
- **Structured Data Contracts**: Pydantic schemas ensure type safety and validation throughout the workflow
- **Knowledge Base Integration**: Master Questionnaires and Platform Guides provide domain-specific context
- **OpenTelemetry Tracing**: Comprehensive observability for debugging and monitoring
- **DataRobot Platform Integration**: Built for deployment and management within DataRobot's ecosystem
- **FastAPI Backend**: RESTful API for workflow orchestration
- **React Frontend**: Modern TypeScript UI for user interaction

---

## 🗂️ Repository Structure

```
solutions_sizing_app/
├── requirement_analyzer_agent/    # Agent 1: Extracts facts and gaps from user input
├── questionnaire_agent/           # Agent 2: Generates tailored questionnaires
├── clarifier_agent/               # Agent 3: Conducts clarification loop (up to K=5 questions)
├── architecture_agent/            # Agent 4: Generates solution architecture plans
├── scoper_shared/                 # Shared components (schemas, utilities, KB content)
│   ├── src/scoper_shared/        # Package source code (src/ layout)
│   │   ├── schemas.py            # Pydantic data models
│   │   ├── orchestrator.py       # State machine orchestrator managing workflow execution
│   │   ├── utils/                # Domain Router, KB Retriever, RAG System (to be implemented)
│   │   │   ├── domain_router.py  # Routes use cases to domain tracks
│   │   │   └── kb_retriever.py   # Fetches Master Questionnaires and Platform Guides
│   │   └── kb_content/           # Master Questionnaires and Platform Guides
│   │       └── master_questionnaire.json
│   └── tests/                     # Unit tests for shared components
├── writer_agent/                  # Example agent template (LangGraph-based)
├── web/                           # FastAPI backend server
├── frontend_web/                  # React frontend with TypeScript
├── mcp_server/                     # MCP server for tool integration
├── infra/                         # Pulumi Infrastructure as Code
├── tasks/                         # Project documentation (PRD, EDD, task list)
├── tests/                         # Testing files and documentation
│   ├── test_agents.sh            # Quick CLI test script for all agents
│   ├── test_all_agents.py        # Comprehensive Python test script for full workflow
│   ├── TESTING.md                # Complete testing guide and documentation
│   └── TEST_FILES_EXPLANATION.md # Explanation of testing file consolidation
```

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following tools installed:

| Tool         | Version    | Description                     | Installation guide            |
|--------------|------------|---------------------------------|-------------------------------|
| **dr-cli**   | >= 0.1.8   | The DataRobot CLI.              | [dr-cli installation guide](https://github.com/datarobot-oss/cli?tab=readme-ov-file#installation) |
| **git**      | >= 2.30.0  | A version control system.       | [git installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) |
| **uv**       | >= 0.7.0   | A Python package manager.       | [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)     |
| **Pulumi**   | >= 3.163.0 | An Infrastructure as Code tool. | [Pulumi installation guide](https://www.pulumi.com/docs/iac/download-install/)        |
| **Taskfile** | >= 3.43.3  | A task runner.                  | [Taskfile installation guide](https://taskfile.dev/docs/installation)                 |
| **NodeJS**   | >= 24      | JavaScript runtime for frontend development. | [NodeJS installation guide](https://nodejs.org/en/download/)                |

> **IMPORTANT**: This repository is only compatible with macOS and Linux operating systems. For Windows, consider using a [DataRobot codespace](https://docs.datarobot.com/en/docs/workbench/wb-notebook/codespaces/index.html), Windows Subsystem for Linux (WSL), or a virtual machine.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/carolinesfer/solutions_sizing_app.git
   cd solutions_sizing_app
   ```

2. **Prepare the application:**
   ```bash
   task start
   ```
   This interactive wizard will guide you through configuration options.

3. **Install dependencies for all agents:**
   ```bash
   task requirement_analyzer_agent:install
   task questionnaire_agent:install
   task clarifier_agent:install
   task architecture_agent:install
   ```

---

## 🏗️ Architecture

### Agent Pipeline

The system implements a **4-agent sequential pipeline**:

1. **Requirement Analyzer Agent** (`requirement_analyzer_agent/`)
   - **Input**: `UseCaseInput` (paragraph, transcript, use_case_title)
   - **Output**: `FactExtractionModel` (requirements, gaps, domain keywords)
   - **Purpose**: Extracts facts and identifies informational gaps from raw user input

2. **Questionnaire Agent** (`questionnaire_agent/`)
   - **Input**: `FactExtractionModel` + Master Questions (from KB)
   - **Output**: `QuestionnaireDraft` (selected questions + delta questions for gaps)
   - **Purpose**: Generates tailored questionnaires by selecting relevant questions and creating new ones for gaps

3. **Clarifier Agent** (`clarifier_agent/`)
   - **Input**: `QuestionnaireDraft` + Current Answers
   - **Output**: `QuestionnaireFinal` (compiled Q&A pairs)
   - **Purpose**: Conducts bounded clarification loop (up to K=5 questions) to fill high-impact gaps

4. **Architecture Agent** (`architecture_agent/`)
   - **Input**: `QuestionnaireFinal` + RAG Context (Platform Guides)
   - **Output**: `ArchitecturePlan` (10-16 steps) + Markdown string
   - **Purpose**: Generates step-by-step solution architecture plans grounded in DataRobot best practices

### Shared Components (`scoper_shared/`)

The `scoper_shared` package uses a `src/` layout for proper Python packaging:

- **Schemas** (`src/scoper_shared/schemas.py`): Pydantic data models for all agent inputs/outputs
- **Domain Router** (`src/scoper_shared/utils/domain_router.py`): Routes use cases to domain tracks (time_series, nlp, cv, genai_rag, classic_ml)
- **KB Retriever** (`src/scoper_shared/utils/kb_retriever.py`): Fetches Master Questionnaires and Platform Guides
- **RAG System** (`src/scoper_shared/utils/rag_system.py`): Vector search for Platform Guides using DataRobot's managed Vector Database (to be implemented in task 6.0)
- **Orchestrator** (`src/scoper_shared/orchestrator.py`): State machine managing workflow execution with 9 states (INGEST → ANALYZE → ROUTE → KB_FETCH → Q_DRAFT → Q_CLARIFY → Q_FREEZE → PLAN_ARCH → DONE)
- **Knowledge Base** (`src/scoper_shared/kb_content/`): Master Questionnaires (JSON) and Platform Guides (Markdown)

### Technology Stack

- **Agent Framework**: `pydantic-ai` (all 4 agents)
- **Evaluation Framework**: `pydantic-evals` for systematic agent testing
- **Backend**: FastAPI with AG-UI protocol support, SQLModel for database persistence
- **Frontend**: React with TypeScript
- **Infrastructure**: Pulumi for DataRobot deployment (all 4 agents + FastAPI Custom Application)
- **Observability**: OpenTelemetry for distributed tracing
- **Data Validation**: Pydantic v2 with strict type checking
- **Database**: SQLite (development) / PostgreSQL (production) with Alembic migrations

---

## 🛠️ Usage

### Local Development

#### Option 1: Full Application (Backend + Frontend + Agents)

Start all services together:
```bash
task dev
```

This will start:
- MCP server (port 9000)
- FastAPI backend (port 8080)
- All 4 agents (ports 8842, 8843, 8844, 8845)
- React frontend (port 5173)

Access the application at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080
- **Scoper Page**: http://localhost:5173/scoper

#### Option 2: Individual Services

Build the frontend:
```bash
task frontend_web:build
```

Start the backend:
```bash
task web:dev
```

Start all agents (in separate terminals):
```bash
task requirement_analyzer_agent:dev
task questionnaire_agent:dev
task clarifier_agent:dev
task architecture_agent:dev
```

#### Option 3: Individual Agent Testing

**Quick Test All Agents (Recommended):**
```bash
# Automated Python script - tests all 4 agents in sequence
cd tests
PYTHONPATH=.. python test_all_agents.py

# Or use the shell script for quick CLI tests
./tests/test_agents.sh
```

**Test Individual Agents via CLI:**

**Requirement Analyzer Agent:**
```bash
task requirement_analyzer_agent:cli -- execute --user_prompt '{"paragraph": "We need to predict customer churn using historical data", "use_case_title": "Customer Churn Prediction"}'
```

**Questionnaire Agent:**
```bash
task questionnaire_agent:cli -- execute --user_prompt '{"use_case_title": "Customer Churn", "technical_confidence_score": 0.85, "key_extracted_requirements": ["Predict churn"], "domain_keywords": ["classic_ml"], "identified_gaps": []}'
```

**Clarifier Agent:**
```bash
task clarifier_agent:cli -- execute --user_prompt '{"questions": [...], "selected_from_master_ids": [...], "delta_questions": [], "coverage_estimate": 0.75}'
```

**Architecture Agent:**
```bash
task architecture_agent:cli -- execute --user_prompt '{"qas": [{"id": "q1", "answer": "Database"}], "answered_pct": 0.9, "gaps": []}'
```

See [tests/TESTING.md](./tests/TESTING.md) for comprehensive testing documentation.

#### Option 4: Agent Playground (Chainlit)

For interactive testing of individual agents:

```bash
task requirement_analyzer_agent:dev
task requirement_analyzer_agent:chainlit
```

Access at http://localhost:8083/

### Web API Usage

The FastAPI backend provides RESTful endpoints for the scoper workflow:

**Start a new workflow:**
```bash
POST /api/v1/scoper/start
{
  "paragraph": "We need to build a predictive maintenance system",
  "use_case_title": "Predictive Maintenance",
  "transcript": "Optional transcript from customer meeting"
}
```

**Get workflow state:**
```bash
GET /api/v1/scoper/{workflow_id}/state
```

**Submit clarification answer:**
```bash
POST /api/v1/scoper/{workflow_id}/clarify
{
  "question_id": "q1",
  "answer": "Database"
}
```

**Get final results:**
```bash
GET /api/v1/scoper/{workflow_id}/results
```

### Build and Deploy

**Build agents for LLM Playground testing:**
```bash
task requirement_analyzer_agent:build
task questionnaire_agent:build
task clarifier_agent:build
task architecture_agent:build
```

**Deploy all agents to DataRobot:**
```bash
# Deploy all agents and FastAPI backend
task deploy

# Or deploy individually
task requirement_analyzer_agent:deploy
task questionnaire_agent:deploy
task clarifier_agent:deploy
task architecture_agent:deploy
```

**Deploy FastAPI backend as Custom Application:**
```bash
cd infra
pulumi up
```

**Test deployed agents:**
```bash
task requirement_analyzer_agent:cli -- execute-deployment --user_prompt "..." --deployment_id <deployment_id>
```

---

## 📦 Key Components

### Agents

Each agent follows the DataRobot Agentic Workflow Application template structure:

- `custom_model/agent.py` - Main agent implementation using pydantic-ai
- `custom_model/custom.py` - DataRobot integration hooks (`load_model`, `chat`)
- `custom_model/config.py` - Agent configuration and environment variables
- `custom_model/helpers.py` - Utility functions and response formatting
- `custom_model/model-metadata.yaml` - Agent metadata and runtime parameters
- `cli.py` - Command-line interface for testing
- `dev.py` - Development server entry point
- `README.md` - Agent-specific documentation

### Shared Components

The `scoper_shared` package uses a `src/` layout for proper Python packaging:

- **`scoper_shared/src/scoper_shared/schemas.py`**: All Pydantic data models
  - `UseCaseInput`, `FactExtractionModel`, `Question`, `QuestionnaireDraft`, `QuestionnaireFinal`, `ArchitectureStep`, `ArchitecturePlan`

- **`scoper_shared/src/scoper_shared/orchestrator.py`**: State machine orchestrator managing the complete workflow
  - 9 workflow states: INGEST → ANALYZE → ROUTE → KB_FETCH → Q_DRAFT → Q_CLARIFY → Q_FREEZE → PLAN_ARCH → DONE
  - State persistence and recovery
  - Gate conditions (e.g., ≥80% answered or coverage ≥0.8)

- **`scoper_shared/src/scoper_shared/utils/domain_router.py`**: Routes use cases to domain tracks based on keywords

- **`scoper_shared/src/scoper_shared/utils/kb_retriever.py`**: Fetches Master Questionnaires and Platform Guides

- **`scoper_shared/src/scoper_shared/kb_content/`**: Knowledge Base content
  - `master_questionnaire.json`: Canonical questions organized by domain tracks
  - `platform_guides/`: Internal DataRobot documentation (Markdown) - organized by track subdirectories

### Web API

- **`web/app/api/v1/scoper.py`**: FastAPI router for scoper endpoints
  - `POST /api/v1/scoper/start` - Start new workflow
  - `GET /api/v1/scoper/{workflow_id}/state` - Get current state
  - `POST /api/v1/scoper/{workflow_id}/clarify` - Submit clarification answer
  - `GET /api/v1/scoper/{workflow_id}/results` - Get final results

- **`web/app/workflows/__init__.py`**: Database models and repository for workflow persistence
  - `Workflow` SQLModel for state storage
  - `WorkflowRepository` for database operations

### Frontend

- **`frontend_web/src/pages/Scoper.tsx`**: Main scoper page component
- **`frontend_web/src/components/ScoperWorkflow.tsx`**: Workflow progress visualization
- **`frontend_web/src/components/ClarificationQuestion.tsx`**: Interactive question/answer component
- **`frontend_web/src/components/QuestionnaireView.tsx`**: Final questionnaire display with JSON download
- **`frontend_web/src/components/ArchitecturePlanView.tsx`**: Architecture plan display with Markdown download
- **`frontend_web/src/api/scoper/`**: API client functions for backend communication

---

## 🔧 Configuration

### LLM Configuration

The application supports multiple LLM configuration options with **automatic detection**:

**Option 1: DataRobot LLM Gateway (Recommended - Auto-detected)**
```bash
# Set in .env file
DATAROBOT_API_TOKEN=your-datarobot-api-token
DATAROBOT_ENDPOINT=https://app.datarobot.com/api/v2
INFRA_ENABLE_LLM=gateway_direct.py
```

When `INFRA_ENABLE_LLM=gateway_direct.py` is set, agents automatically use DataRobot LLM Gateway. No need to explicitly set `USE_DATAROBOT_LLM_GATEWAY=1`.

**Option 2: Direct OpenAI**
```bash
# Set in .env file
OPENAI_API_KEY=your-openai-api-key
# Unset or remove INFRA_ENABLE_LLM
```

**Option 3: Already Deployed Text Generation model in DataRobot**
```bash
LLM_DEPLOYMENT_ID=your-deployment-id
```

### Environment Variables

Each agent can be configured via environment variables or `.env` file:

- `LLM_DEFAULT_MODEL`: Default model to use (e.g., `"azure/gpt-4o-mini"` for LLM Gateway)
- `LLM_DEPLOYMENT_ID`: DataRobot deployment ID (if using deployed model)
- `USE_DATAROBOT_LLM_GATEWAY`: Explicitly enable DataRobot LLM Gateway (auto-detected from `INFRA_ENABLE_LLM`)
- `INFRA_ENABLE_LLM`: Infrastructure LLM configuration (set to `gateway_direct.py` for auto-detection)
- `DATAROBOT_API_TOKEN`: DataRobot API token (required for LLM Gateway)
- `DATAROBOT_ENDPOINT`: DataRobot API endpoint (required for LLM Gateway)
- `<AGENT>_AGENT_ENDPOINT`: Agent endpoint URL (e.g., `REQUIREMENT_ANALYZER_AGENT_ENDPOINT`)

---

## 🎯 DataRobot Platform Integration

### Use Case

The application is deployed under a DataRobot **Use Case** that groups all related resources:

- **Use Case Name**: `Agentic Professional Services Scoper [<PROJECT_NAME>]` (default) or uses existing use case if `DATAROBOT_DEFAULT_USE_CASE` environment variable is set
  - If `DATAROBOT_DEFAULT_USE_CASE` is set to a Use Case ID (24+ character alphanumeric), it will use that existing Use Case
  - If `DATAROBOT_DEFAULT_USE_CASE` is set to a name (not an ID), it will create a new Use Case with that name
- **Use Case Description**: "Agentic Professional Services Scoper - AI-powered system for standardizing and accelerating Professional Services scoping process"
- **Location**: Defined in `infra/infra/__init__.py`

The Use Case serves as the organizational container for:
- All 4 agent Custom Models
- Agent Deployments
- Registered Models
- FastAPI Custom Application
- Agentic Playgrounds
- LLM Blueprints

### Registry Items

When deployed, the following items are registered in the DataRobot Model Registry:

#### Custom Models

Each of the 4 agents is registered as a **Custom Model** in the Model Registry:

1. **Requirement Analyzer Agent Custom Model**
   - Target Type: `AgenticWorkflow`
   - Language: `python`
   - Base Environment: Python 3.12 execution environment
   - Use Case: Associated with the project Use Case

2. **Questionnaire Agent Custom Model**
   - Target Type: `AgenticWorkflow`
   - Language: `python`
   - Base Environment: Python 3.12 execution environment
   - Use Case: Associated with the project Use Case

3. **Clarifier Agent Custom Model**
   - Target Type: `AgenticWorkflow`
   - Language: `python`
   - Base Environment: Python 3.12 execution environment
   - Use Case: Associated with the project Use Case

4. **Architecture Agent Custom Model**
   - Target Type: `AgenticWorkflow`
   - Language: `python`
   - Base Environment: Python 3.12 execution environment
   - Use Case: Associated with the project Use Case

#### Registered Models

Each Custom Model is registered as a **Registered Model** in the Model Registry, enabling:
- Version tracking
- Deployment management
- Model lineage
- Governance and compliance

#### Custom Application

The FastAPI backend is registered as a **Custom Application**:
- Application Source: Contains all web application files
- Runtime Parameters: Configured for agent endpoints, LLM settings, OAuth providers
- Resources: CPU XL resource bundle (configurable)
- Use Case: Associated with the project Use Case

### Deployed Models

When `AGENT_DEPLOY` environment variable is not set to `"0"`, the following deployments are created:

#### Agent Deployments

Each agent is deployed as a **DataRobot Deployment**:

1. **Requirement Analyzer Agent Deployment**
   - Platform: `DATAROBOT_SERVERLESS`
   - Prediction Environment: Serverless prediction environment
   - Association ID Settings: Configured for workflow tracking
   - Predictions Data Collection: Enabled for monitoring
   - Predictions Settings: Min computes: 0, Max computes: 2

2. **Questionnaire Agent Deployment**
   - Platform: `DATAROBOT_SERVERLESS`
   - Prediction Environment: Serverless prediction environment
   - Association ID Settings: Configured for workflow tracking
   - Predictions Data Collection: Enabled for monitoring
   - Predictions Settings: Min computes: 0, Max computes: 2

3. **Clarifier Agent Deployment**
   - Platform: `DATAROBOT_SERVERLESS`
   - Prediction Environment: Serverless prediction environment
   - Association ID Settings: Configured for workflow tracking
   - Predictions Data Collection: Enabled for monitoring
   - Predictions Settings: Min computes: 0, Max computes: 2

4. **Architecture Agent Deployment**
   - Platform: `DATAROBOT_SERVERLESS`
   - Prediction Environment: Serverless prediction environment
   - Association ID Settings: Configured for workflow tracking
   - Predictions Data Collection: Enabled for monitoring
   - Predictions Settings: Min computes: 0, Max computes: 2

#### Deployment Endpoints

Each agent deployment provides:
- **Direct Access Endpoint**: `{DATAROBOT_ENDPOINT}/deployments/{deployment_id}/directAccess/`
- **Chat Endpoint**: `{DATAROBOT_ENDPOINT}/genai/agents/fromCustomModel/{custom_model_id}/chat/`
- **MCP Endpoint** (if applicable): `{DATAROBOT_ENDPOINT}/deployments/{deployment_id}/directAccess/mcp`

#### Agentic Playgrounds

Each agent has an associated **Agentic Playground** for interactive testing:
- Playground Type: `agentic`
- Use Case: Associated with the project Use Case
- Access URL: `{DATAROBOT_URL}/usecases/{use_case_id}/agentic-playgrounds/{playground_id}/comparison/chats`

#### LLM Blueprints

Each agent has an associated **LLM Blueprint**:
- Playground ID: Linked to the agent's Agentic Playground
- LLM ID: `chat-interface-custom-model`
- Custom Model ID: References the agent's Custom Model
- Prompt Type: `ONE_TIME_PROMPT`

### Accessing Deployed Resources

After deployment, Pulumi exports the following information:

- **Custom Model IDs**: For each agent
- **Deployment IDs**: For each agent deployment
- **Deployment Endpoints**: Direct access URLs for each agent
- **Playground URLs**: Links to agentic playgrounds for testing
- **Custom Application ID**: FastAPI backend application ID
- **Custom Application URL**: Production URL for the web application

View these exports by running:
```bash
cd infra
pulumi stack output
```

---

## 📊 Current Development Progress

### ✅ Completed Components

#### Core Infrastructure (100% Complete)
- ✅ All 4 agents implemented and tested locally
- ✅ Shared components (schemas, orchestrator, domain router, KB retriever)
- ✅ State machine orchestrator with 9 workflow states
- ✅ FastAPI backend with scoper endpoints
- ✅ React frontend with workflow UI
- ✅ Database persistence for workflow state
- ✅ OpenTelemetry tracing throughout
- ✅ Pulumi infrastructure code for all agents

#### Knowledge Base (100% Complete)
- ✅ 43 questions extracted and structured in `master_questionnaire.json`
- ✅ 184 platform guide markdown files organized by track:
  - `time_series/`: Time series forecasting guides
  - `nlp/`: Natural language processing guides
  - `cv/`: Computer vision guides
  - `genai_rag/`: Generative AI and RAG guides
  - `classic_ml/`: Traditional machine learning guides
  - `infrastructure/`: Infrastructure and deployment guides (80 Pulumi docs)
  - `general/`: General DataRobot documentation (13 files)

#### Testing Infrastructure (100% Complete)
- ✅ Unit tests for all agents
- ✅ Unit tests for shared components
- ✅ Integration tests for web API
- ✅ End-to-end test script (`tests/test_all_agents.py`)
- ✅ Quick CLI test script (`tests/test_agents.sh`)
- ✅ All testing files consolidated in `tests/` directory
- ✅ Pydantic Evals evaluation framework setup
- ✅ Comprehensive testing documentation (`tests/TESTING.md`)

#### Documentation (100% Complete)
- ✅ Product Requirements Document (PRD)
- ✅ Engineering Design Document (EDD)
- ✅ Task list with progress tracking
- ✅ Testing guide
- ✅ Agent development guidelines
- ✅ Evaluation guide

### 🚧 In Progress / Pending

#### RAG System Implementation (Task 6.0 - 0% Complete)
- ❌ **Critical Gap**: RAG system using DataRobot's managed Vector Database not yet implemented
- ❌ Architecture Agent currently uses simple file-based KB retriever (loads all platform guides)
- ❌ No semantic search or relevance ranking
- ❌ Missing vector database integration
- **Impact**: Architecture Agent receives all platform guides instead of semantically relevant context

**Required Implementation:**
- Create `scoper_shared/src/scoper_shared/utils/rag_system.py`
- Integrate DataRobot Vector Database APIs
- Implement document chunking and embedding generation
- Implement vector search functionality
- Update Architecture Agent to use RAG system
- Update Orchestrator PLAN_ARCH state to use RAG system

#### Deployment Tasks (Tasks 5.28-5.34 - Pending)
- ⏳ Build agents for LLM Playground testing (requires Pulumi deployment)
- ⏳ Deploy agents to DataRobot production (requires Pulumi deployment)
- ⏳ Test deployed agents via deployment endpoints
- ⏳ Configure Custom Application deployment settings
- ⏳ Deploy FastAPI backend as Custom Application
- ⏳ Verify end-to-end workflow with deployed agents

**Note**: These tasks require actual DataRobot environment access and cannot be completed with test files alone.

#### Minor Tasks
- ⏳ PDF extraction for some reference documents (non-critical, can be done manually)
- ⏳ PDF to Markdown conversion for one time series document

#### Recent Improvements
- ✅ **Test File Consolidation**: All testing files have been consolidated into the `tests/` directory at the repository root for better organization
  - `test_all_agents.py` - Comprehensive Python test script
  - `test_agents.sh` - Quick CLI test script
  - `TESTING.md` - Complete testing documentation
  - `TEST_FILES_EXPLANATION.md` - Explanation of test file structure

---

## 🎯 Planned Next Steps

### Immediate Priorities

1. **Implement RAG System (Task 6.0)** - **HIGH PRIORITY**
   - This is the most critical missing component
   - Will significantly improve Architecture Agent output quality
   - Required for production readiness
   - Estimated effort: 2-3 days

2. **Complete Deployment Pipeline (Tasks 5.28-5.34)**
   - Build and deploy all 4 agents to DataRobot
   - Deploy FastAPI backend as Custom Application
   - Verify end-to-end workflow with deployed agents
   - Estimated effort: 1-2 days

3. **Production Testing and Validation**
   - Test complete workflow with real use cases
   - Validate output quality with SMEs
   - Performance testing and optimization
   - Estimated effort: 2-3 days

### Short-Term Goals (Next 2-4 Weeks)

1. **RAG System Integration**
   - Complete DataRobot Vector Database integration
   - Implement semantic search for Platform Guides
   - Update Architecture Agent to use RAG context
   - Test and validate RAG retrieval quality

2. **Production Deployment**
   - Deploy all components to DataRobot production environment
   - Configure monitoring and alerting
   - Set up CI/CD pipeline for automated deployments
   - Document deployment procedures

3. **Quality Assurance**
   - Comprehensive end-to-end testing
   - SME review and feedback collection
   - Performance benchmarking
   - Bug fixes and improvements

### Medium-Term Goals (Next 1-2 Months)

1. **Enhancement and Optimization**
   - Optimize agent prompts based on feedback
   - Improve question selection algorithms
   - Enhance architecture plan generation quality
   - Add more domain-specific knowledge

2. **Feature Additions**
   - Support for additional domain tracks
   - Enhanced clarification question generation
   - Multi-language support (if needed)
   - Export formats (PDF, Word, etc.)

3. **Integration and Automation**
   - Integration with Salesforce or other internal tools
   - Automated feedback loop implementation
   - Historical project data integration (for Phase 2)
   - Hours estimation functionality (Phase 2)

### Long-Term Vision (Phase 2+)

1. **Hours Estimation**
   - Generate detailed hours and FTE requirements
   - Integrate historical project data
   - Workforce rate information integration

2. **SOW Generation**
   - Full Project Plan generation
   - Statements of Work (SOW) creation
   - Legal and compliance considerations

3. **Advanced Features**
   - Multi-project scoping
   - Template customization
   - Advanced analytics and reporting
   - Machine learning model for estimation accuracy

---

## ✅ Requirements

- Python 3.10+ (tested up to 3.12)
- Node.js 24+
- DataRobot account with appropriate permissions
- OpenAI API key (or DataRobot LLM Gateway configuration)

---

## 📄 Documentation

- **[Product Requirements Document (PRD)](./tasks/Solutions-Agent-PRD.md)**: Business requirements and success metrics
- **[Engineering Design Document (EDD)](./tasks/Solutions-Agent-Unified-EDD.md)**: Technical architecture and implementation details
- **[Task List](./tasks/tasks-agentic-professional-services-scoper.md)**: Detailed implementation checklist and progress tracking
- **[Testing Guide](./tests/TESTING.md)**: Comprehensive testing documentation and methods
- **[Agent Development Guidelines](./AGENTS.md)**: Coding standards and best practices
- **[Evaluation Guide](./EVALUATION.md)**: Pydantic Evals evaluation framework usage
- **[DataRobot Agent Development Docs](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-development.html)**: Official DataRobot documentation
- **[DataRobot LLM Gateway Docs](https://docs.datarobot.com/en/docs/gen-ai/genai-code/dr-llm-gateway.html)**: LLM Gateway usage and configuration
- **[OpenTelemetry Tracing Docs](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-tracing.html)**: Observability and tracing
- **[Pydantic Evals Docs](https://ai.pydantic.dev/evals/)**: Evaluation framework documentation

### Agent-Specific Documentation

- [Requirement Analyzer Agent](./requirement_analyzer_agent/README.md)
- [Questionnaire Agent](./questionnaire_agent/README.md)
- [Clarifier Agent](./clarifier_agent/README.md)
- [Architecture Agent](./architecture_agent/README.md)

---

## 🧪 Testing

See **[tests/TESTING.md](./tests/TESTING.md)** for comprehensive testing documentation and guides.

### Quick Start Testing

**Test all 4 agents in sequence:**
```bash
# Automated Python script (recommended)
cd tests
PYTHONPATH=.. python test_all_agents.py

# Or quick CLI tests
./tests/test_agents.sh
```

### Unit Tests

Run unit tests for each component:

```bash
# Test shared components (from repository root)
cd scoper_shared && PYTHONPATH=.. uv run pytest tests/

# Test individual agents
task requirement_analyzer_agent:test
task questionnaire_agent:test
task clarifier_agent:test
task architecture_agent:test

# Test web API integration
cd web && pytest tests/integration/test_scoper.py
```

### Pydantic Evals

All agents use [Pydantic Evals](https://ai.pydantic.dev/evals/) for systematic evaluation. Run evaluations:

```bash
# Requirement Analyzer Agent
cd requirement_analyzer_agent && uv run python tests/test_evals.py

# Questionnaire Agent
cd questionnaire_agent && uv run python tests/test_evals.py

# Clarifier Agent
cd clarifier_agent && uv run python tests/test_evals.py

# Architecture Agent
cd architecture_agent && uv run python tests/test_evals.py
```

See [EVALUATION.md](./EVALUATION.md) for detailed evaluation documentation.

### Test Coverage

- **Shared Components**: Unit tests for schemas, orchestrator, domain router, and KB retriever
- **Agents**: Unit tests for each agent's core logic and output validation
- **Pydantic Evals**: Systematic evaluation datasets with custom evaluators for each agent
- **Web API**: Integration tests for all scoper endpoints (workflow creation, state management, clarification, results)
- **End-to-End Testing**: `tests/test_all_agents.py` tests the complete workflow from Requirement Analyzer → Questionnaire → Clarifier → Architecture

---

## 🚢 Deployment

Deploy all components to DataRobot:

```bash
# Deploy all agents and FastAPI backend
task deploy

# Or deploy individually
task requirement_analyzer_agent:deploy
task questionnaire_agent:deploy
task clarifier_agent:deploy
task architecture_agent:deploy
```

The deployment process uses Pulumi to:
- Create DataRobot Custom Model deployments for all 4 agents
- Deploy FastAPI backend as DataRobot Custom Application
- Configure execution environments
- Set up runtime parameters (including agent deployment IDs and endpoints)
- Register agents in the Model Registry
- Create feature flag configurations for each agent

### Infrastructure Files

- `infra/infra/requirement_analyzer_agent.py` - Pulumi infrastructure for Agent 1
- `infra/infra/questionnaire_agent.py` - Pulumi infrastructure for Agent 2
- `infra/infra/clarifier_agent.py` - Pulumi infrastructure for Agent 3
- `infra/infra/architecture_agent.py` - Pulumi infrastructure for Agent 4
- `infra/infra/web.py` - Pulumi infrastructure for FastAPI Custom Application
- `infra/feature_flags/*.yaml` - Feature flag configurations for each agent

---

## 🔍 Observability

All components include **OpenTelemetry tracing** for comprehensive observability:

**Agents:**
- Agent execution flow with nested spans
- LLM API calls with token usage
- Input/output attributes (confidence scores, question counts, etc.)
- Error tracking and retry logic

**Utilities:**
- Domain Router: Track selected domain tracks
- KB Retriever: Monitor file loading and question retrieval
- RAG System: Vector search operations (when implemented)

**Orchestrator:**
- State transitions with timing information
- Agent coordination spans
- Gate condition evaluations
- Workflow-level span encompassing entire execution

**Web API:**
- Request/response tracing
- Database operations
- Agent invocation tracking

Traces can be viewed in DataRobot's monitoring dashboard or exported to external observability platforms.

---

## 🤝 Contributing

This project follows DataRobot's coding standards and best practices. See [AGENTS.md](./AGENTS.md) for detailed guidelines.

Key principles:
- **Type Safety**: All functions must have type annotations
- **Documentation**: Google-style docstrings for all public APIs
- **Testing**: Aim for 90%+ test coverage
- **Code Quality**: Ruff for linting and formatting
- **DataRobot Integration**: All components designed for DataRobot platform deployment

---

## 📝 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and changes.

---

## ❤️ Acknowledgements

- Built on the [DataRobot Agentic Workflow Application template](https://github.com/datarobot-community/datarobot-agent-application)
- Uses [pydantic-ai](https://github.com/pydantic/pydantic-ai) for agent framework
- Powered by [DataRobot](https://datarobot.com) platform

---

## 📞 Get Help

If you encounter issues or have questions:

- [Contact DataRobot Support](https://docs.datarobot.com/en/docs/get-started/troubleshooting/general-help.html)
- Open an issue on the [GitHub repository](https://github.com/carolinesfer/solutions_sizing_app)
- Review the [task list](./tasks/tasks-agentic-professional-services-scoper.md) for implementation status

---

## 📜 License

This project is licensed under the Apache License 2.0 - see [LICENSE.txt](./LICENSE.txt) for details.
