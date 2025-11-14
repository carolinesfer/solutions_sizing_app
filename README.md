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
│   ├── schemas.py                 # Pydantic data models
│   ├── orchestrator.py            # State machine orchestrator (to be implemented)
│   ├── utils/                     # Domain Router, KB Retriever, RAG System
│   ├── kb_content/                # Master Questionnaires and Platform Guides
│   └── tests/                     # Unit tests for shared components
├── writer_agent/                  # Example agent template (LangGraph-based)
├── web/                           # FastAPI backend server
├── frontend_web/                  # React frontend with TypeScript
├── mcp_server/                     # MCP server for tool integration
├── infra/                         # Pulumi Infrastructure as Code
└── tasks/                         # Project documentation (PRD, EDD, task list)
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

- **Schemas** (`schemas.py`): Pydantic data models for all agent inputs/outputs
- **Domain Router** (`utils/domain_router.py`): Routes use cases to domain tracks (time_series, nlp, cv, genai_rag, classic_ml)
- **KB Retriever** (`utils/kb_retriever.py`): Fetches Master Questionnaires and Platform Guides
- **RAG System** (`utils/rag_system.py`): Vector search for Platform Guides (to be implemented in task 6.0)
- **Orchestrator** (`orchestrator.py`): State machine managing workflow execution (to be implemented in task 4.0)
- **Knowledge Base** (`kb_content/`): Master Questionnaires (JSON) and Platform Guides (Markdown)

### Technology Stack

- **Agent Framework**: `pydantic-ai` (all 4 agents)
- **Backend**: FastAPI with AG-UI protocol support
- **Frontend**: React with TypeScript
- **Infrastructure**: Pulumi for DataRobot deployment
- **Observability**: OpenTelemetry for distributed tracing
- **Data Validation**: Pydantic v2 with strict type checking

---

## 🛠️ Usage

### Local Development

#### Option 1: Full Application (Backend + Frontend + Agents)

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

Access the application at http://localhost:8080

#### Option 2: Individual Agent Testing

Test each agent independently using the CLI:

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

#### Option 3: Agent Playground (Chainlit)

For interactive testing of individual agents:

```bash
task requirement_analyzer_agent:dev
task requirement_analyzer_agent:chainlit
```

Access at http://localhost:8083/

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
task requirement_analyzer_agent:deploy
task questionnaire_agent:deploy
task clarifier_agent:deploy
task architecture_agent:deploy
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

- **`scoper_shared/schemas.py`**: All Pydantic data models
  - `UseCaseInput`, `FactExtractionModel`, `Question`, `QuestionnaireDraft`, `QuestionnaireFinal`, `ArchitectureStep`, `ArchitecturePlan`

- **`scoper_shared/utils/domain_router.py`**: Routes use cases to domain tracks based on keywords

- **`scoper_shared/utils/kb_retriever.py`**: Fetches Master Questionnaires and Platform Guides

- **`scoper_shared/kb_content/`**: Knowledge Base content
  - `master_questionnaire.json`: Canonical questions organized by domain tracks
  - `platform_guides/`: Internal DataRobot documentation (Markdown)

---

## 🔧 Configuration

### LLM Configuration

The application supports multiple LLM configuration options. See the [original template documentation](#prepare-application) for details on:
- LLM Blueprint with LLM Gateway (default)
- LLM Blueprint with External LLM
- Already Deployed Text Generation model in DataRobot

### Environment Variables

Each agent can be configured via environment variables or `.env` file:

- `LLM_DEFAULT_MODEL`: Default model to use (e.g., `"datarobot/azure/gpt-4o-mini"`)
- `LLM_DEPLOYMENT_ID`: DataRobot deployment ID (if using deployed model)
- `USE_DATAROBOT_LLM_GATEWAY`: Enable DataRobot LLM Gateway
- `<AGENT>_AGENT_ENDPOINT`: Agent endpoint URL (e.g., `REQUIREMENT_ANALYZER_AGENT_ENDPOINT`)

---

## ✅ Requirements

- Python 3.10+ (tested up to 3.12)
- Node.js 24+
- DataRobot account with appropriate permissions
- OpenAI API key (or DataRobot LLM Gateway configuration)

---

## 📄 Documentation

- **[Product Requirements Document (PRD)](./tasks/Solutions-Agent-PRD-gdrive.md)**: Business requirements and success metrics
- **[Engineering Design Document (EDD)](./tasks/Solutions-Agent-Unified-EDD-gdrive.md)**: Technical architecture and implementation details
- **[Task List](./tasks/tasks-agentic-professional-services-scoper.md)**: Detailed implementation checklist
- **[Agent Development Guidelines](./AGENTS.md)**: Coding standards and best practices
- **[DataRobot Agent Development Docs](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-development.html)**: Official DataRobot documentation
- **[OpenTelemetry Tracing Docs](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-tracing.html)**: Observability and tracing

### Agent-Specific Documentation

- [Requirement Analyzer Agent](./requirement_analyzer_agent/README.md)
- [Questionnaire Agent](./questionnaire_agent/README.md)
- [Clarifier Agent](./clarifier_agent/README.md)
- [Architecture Agent](./architecture_agent/README.md)

---

## 🧪 Testing

Run unit tests for each component:

```bash
# Test shared components
cd scoper_shared && pytest

# Test individual agents
task requirement_analyzer_agent:test
task questionnaire_agent:test
task clarifier_agent:test
task architecture_agent:test
```

---

## 🚢 Deployment

Deploy all components to DataRobot:

```bash
# Deploy all agents
task deploy

# Or deploy individually
task requirement_analyzer_agent:deploy
task questionnaire_agent:deploy
task clarifier_agent:deploy
task architecture_agent:deploy
```

The deployment process uses Pulumi to:
- Create DataRobot Custom Model deployments
- Configure execution environments
- Set up runtime parameters
- Register agents in the Model Registry

---

## 🔍 Observability

All agents include **OpenTelemetry tracing** for:
- Agent execution flow
- LLM API calls
- Utility function execution (Domain Router, KB Retriever)
- State transitions (when orchestrator is implemented)
- Input/output attributes
- Error tracking

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
