# **Product Requirements Document (PRD): Agentic Professional Services Scoper (MVP)**

| Product Name | Agentic Professional Services Scoper |
| :---- | :---- |
| **Product Manager** | $$Name/Team$$ |
| **Stakeholders** | Professional Services Leadership, Sales Leadership, Field Engineers |
| **Release Version** | MVP (v1.0) |
| **Target Date** | $$Date$$ |

## **1\. Goal & Rationale**

### **1.1 Problem Statement**

The current process for scoping, sizing, and pricing Professional Services (ProServ) engagements across global regions is **highly inconsistent** and **over-reliant on a small group of key Subject Matter Experts (SMEs)**. This dependency creates significant bottlenecks, slows down the sales cycle, and introduces delivery risk due to non-standardized estimation artifacts.

### **1.2 Vision**

To standardize and accelerate the ProServ scoping process using an AI agent that consumes initial customer requirements and rapidly generates high-quality, DataRobot-contextualized solution designs and hours estimations.

### **1.3 Success Metric (North Star)**

The primary success metric is the **reduction in variance (standard deviation) of actual project hours vs. estimated project hours for ProServ engagements** where the Agentic Scoper was used, compared to the current manual process.

* **KPIs:**  
  * **Adoption Rate:** Percentage of new ProServ scoping requests utilizing the agent.  
  * **SME Time Reduction:** Average time saved by SMEs in drafting initial scoping documents.  
  * **Artifact Quality:** Average quality score (1-5 grade) from manual review of agent-generated artifacts.

## **2\. MVP Definition & Scope**

The MVP is focused on generating the foundational documentation needed for an SME to validate and finalize a proposal, significantly speeding up the initial discovery and design phases.

### **2.1 Core User Story (Job-to-be-Done)**

**"As a Data Scientist or Sales Lead, I want to input an initial customer use case description and/or call recording transcript, so that the Agentic Scoper can immediately provide a tailored questionnaire and a preliminary Solution Architecture with DataRobot context, allowing me to move rapidly toward a finalized proposal."**

### **2.2 MVP Inputs**

The agent must be able to process the following inputs:

1. **Use Case Description (Mandatory):** A text paragraph or document describing the customer's problem, goals, and high-level requirements. This description could be either based on internal DataRobot professional services staff’s own notes after a customer call and/or the customers’ raw text (e.g. from an email or a meeting transcript). It is out of scope for any external customers to interact with the tool.  
2. **Call Recording Transcript (Preferred/Optional):** Text transcript of a discovery call (if available).  
3. **DataRobot Context (Implicit):** The agent must be pre-loaded with or have access to foundational DataRobot-specific knowledge (Documentation, common RFPs, previous solution designs) to ground its responses.

### **2.3 MVP Deliverables (Outputs)**

The Agent must generate two essential artifacts:

1. **Tailored Deep-Dive Questionnaire (Pydantic Schema):** A list of specific, clarifying questions to be asked of the customer to refine requirements (e.g., data source specifics, deployment environment, success criteria).  
2. **Preliminary Solution Design / Architecture Outline (Markdown):** A high-level description of the proposed DataRobot solution, including key components, architecture context, and implementation phases (without specific hours).

### **2.4 Agent Architecture**

The system uses a **4-agent pipeline architecture** with a state machine orchestrator to ensure structured, validated outputs:

1. **Requirement Analyzer Agent:** Extracts facts, requirements, and identifies gaps from raw user input
2. **Questionnaire Agent:** Generates a tailored questionnaire by selecting relevant questions from a Master KB and creating new questions for identified gaps
3. **Clarifier Agent:** Conducts a bounded clarification loop (up to K questions, e.g., K=5) to fill high-impact gaps through user interaction
4. **Architecture Agent:** Generates the final solution architecture plan using validated requirements and RAG context from internal platform guides

The system also includes two utility functions:
- **Domain Router:** Selects appropriate domain tracks (e.g., time_series, NLP, CV, genai_rag) based on extracted requirements
- **KB Retriever:** Fetches relevant Master Questionnaires and Platform Guides based on selected tracks

All agent outputs must conform to **Pydantic models** to ensure strict structural consistency and data validation.

### **2.5 System Workflow**

The system must execute the following workflow states in sequence:

1. **INGEST:** Receive UseCaseInput (paragraph/transcript and use case title)
2. **ANALYZE:** Requirement Analyzer extracts facts and gaps into FactExtractionModel
3. **ROUTE:** Domain Router selects appropriate domain track(s) based on extracted requirements
4. **KB_FETCH:** KB Retriever fetches relevant Master Questionnaire and Platform Guides based on selected tracks
5. **Q_DRAFT:** Questionnaire Agent creates initial QuestionnaireDraft using fetched Master Questions
6. **Q_CLARIFY:** Clarifier Agent runs bounded interview loop (≤K questions) to collect user answers
7. **Q_FREEZE:** Gate condition - proceeds only if ≥80% of required questions are answered OR coverage ≥0.8
8. **PLAN_ARCH:** Architecture Agent generates final ArchitecturePlan and Markdown artifact using RAG/KB content
9. **DONE:** System delivers both artifacts to the user

### **2.6 User Interface & Delivery**

1. The system must present both final output artifacts to the user in a clean, read-only web interface
2. The Questionnaire data must be viewable as a structured list of Q&As
3. The Solution Design must be rendered as clean, readable Markdown in the UI
4. The UI must provide buttons for the user to download both the Questionnaire (as JSON) and the ArchitecturePlan (as Markdown)
5. During the Q_CLARIFY state, the UI must allow users to answer clarification questions one at a time
6. The UI must display progress indicators showing which workflow state is currently active

## **3\. Future Scope (Beyond MVP)**

The following components are **explicitly out of scope** for the MVP but are planned for subsequent phases:

* **Detailed Hours Estimation:** Generating the final hours and FTE required (Phase 2). This requires the integration of historical project data and workforce rate information.  
* **Full Project Plan / SOW Generation:** Creating the final, legally binding Statements of Work (SOWs) or detailed project plans (Phase 2/3).  
* **Workflow Integration:** Integration into Salesforce (SF) or other internal tooling pages for seamless access.  
* **Automated Feedback Loop Implementation:** The formal mechanism to feed manual review grades back to the agent for reinforcement learning (MVP evaluation will be manual).  
* **Handling of Non-Execution Projects:** Initially limited to standard execution/implementation projects; not applicable to exploratory or advisory services.

## **4\. Evaluation and Feedback Loop**

### **4.1 Evaluation Method (MVP)**

The goodness of the generated artifacts will be assessed via **Manual Review** by a rotating pool of ProServ SMEs using a **1-5 grade scale** (1=Poor, 5=Excellent) based on three criteria:

1. **Completeness:** Did the questionnaire cover all major gaps identified in the input data?  
2. **Accuracy:** Was the solution design technically sound and correctly contextualized to DataRobot capabilities?  
3. **Clarity:** Were the outputs (Questionnaire and Architecture) easy to understand and use by a Field Engineer?

### **4.2 Blockers/Risks**

* **Access to DataRobot Context:** Ensuring the agent has reliable, up-to-date access to internal documentation and successful project examples is critical. A strategy for sanitizing and loading this proprietary knowledge must be developed
* **Call Recording Quality:** Dependence on the quality and format of call recording transcripts could limit the agent's effectiveness. Input data standardization will be necessary
* **RAG System Implementation:** The MVP requires a functional RAG system to query Internal Platform Guides. This must be implemented using **DataRobot's managed Vector Database** to provide relevant context to the Architecture Agent. The RAG system will be integrated via DataRobot's GenAI capabilities and Python SDK.
* **Knowledge Base Content:** The Master Questionnaire and Platform Guides must be properly structured and maintained. Initial content must be extracted from referenced Google Docs/Sheets and converted to the required formats (JSON for questionnaires, Markdown for guides)

## **5\. Functional Requirements**

The system must implement the following functional requirements:

1. **Input Validation:** The system must validate that UseCaseInput contains at minimum a `paragraph` and `use_case_title` field
2. **Fact Extraction:** Agent 1 must output a FactExtractionModel with technical_confidence_score (0.0-1.0), key_extracted_requirements (list), domain_keywords (list), and identified_gaps (list)
3. **Domain Routing:** The Domain Router must select at least one track (time_series, nlp, cv, genai_rag, or classic_ml as default) based on keyword matching in requirements and title
4. **Question Selection:** Agent 2 must select relevant questions from the Master Questionnaire based on the FactExtractionModel and generate new delta_questions for identified gaps
5. **Clarification Loop:** Agent 3 must ask up to K questions (default K=5) to the user, one at a time, preferring single-choice or boolean questions
6. **Coverage Gate:** The system must enforce the Q_FREEZE gate condition (≥80% answered OR coverage ≥0.8) before proceeding to architecture generation
7. **Architecture Generation:** Agent 4 must generate an ArchitecturePlan with 10-16 steps, each including inputs and outputs fields, plus assumptions and risks lists
8. **RAG Context:** Agent 4 must receive relevant context from Internal Platform Guides via the RAG system before generating the architecture. The RAG system must use DataRobot's managed Vector Database for storing and querying embeddings.
9. **Schema Validation:** All agent outputs must be validated against their respective Pydantic schemas before state transitions
10. **Error Handling:** The system must handle and report errors at each state, allowing for retry or manual intervention

## **6\. Technical Considerations (DataRobot Platform)**

This section specifies how the feature will be built, deployed, and managed on the DataRobot platform.

### **6.1 Deployment**

* **Deployment Target:** This feature will be deployed as a **DataRobot Custom Application** for unified governance, monitoring, and security. The FastAPI backend (`web/`) will be deployed as the main Custom Application, and all four agents will be deployed as separate DataRobot Agentic Workflow deployments.
* **Model Registry:** All four agents (Requirement Analyzer, Questionnaire, Clarifier, Architecture) must be registered in the **DataRobot Model Registry** and available as scalable DataRobot Deployments.
* **Infrastructure as Code:** Deployment will be managed using **Pulumi** with the DataRobot Pulumi provider (`@pulumi/datarobot`) to automate agent deployment, execution environment configuration, and runtime parameter management.

### **6.2 Agentic AI Framework**

* **Agent Development:** All four agents must be developed, tested, and deployed using **DataRobot's Agentic AI framework** ([Agentic AI Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/index.html)). Each agent will be hosted as a DataRobot Application for testing, monitoring, and production use.
* **Agent Lifecycle:** DataRobot will manage the agent lifecycle, state, and interaction logging. Each agent's `custom_model/` directory must include the required DataRobot integration hooks (`load_model`, `chat`) as specified in the [Agent Development Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-development.html).
* **OpenTelemetry Tracing:** All agents and the orchestrator must utilize **OpenTelemetry** as documented in the [DataRobot Tracing Documentation](https://docs.datarobot.com/en/docs/agentic-ai/agentic-develop/agentic-tracing.html) to capture tool execution, intermediate outputs, and state transitions.

### **6.3 Generative AI & RAG**

* **Vector Database:** The RAG system for Platform Guides **must** utilize **DataRobot's managed Vector Database** for storing and querying embeddings. Do not use local or standalone vector stores like FAISS or Chroma. The Architecture Agent will use DataRobot's GenAI capabilities to retrieve relevant context from Platform Guides.
* **RAG Implementation:** Use DataRobot's pre-built RAG tools and prompt templates (available in the LLM Playground) as a starting point, and integrate them via the Python SDK. The RAG system will be implemented in `scoper_shared/utils/rag_system.py` and will leverage DataRobot's managed Vector Database APIs.
* **GenAI SDK:** All interactions with DataRobot's GenAI capabilities will use the `datarobot` Python package and DataRobot APIs as documented in the [GenAI Documentation](https://docs.datarobot.com/en/docs/gen-ai/genai-code/index.html).

### **6.4 Technology Stack**

* **Python Version:** Python 3.10+ (tested up to 3.12)
* **Agent Framework:** `pydantic-ai` for all four agents (as shown in the example agent implementation)
* **Data Contracts:** All data flow between agents must use strict Pydantic models (UseCaseInput, FactExtractionModel, QuestionnaireDraft, QuestionnaireFinal, ArchitecturePlan)
* **Backend Framework:** FastAPI for the web API server
* **Frontend Framework:** React with TypeScript
* **Database:** SQLite/PostgreSQL for workflow state persistence (via SQLModel)
* **Infrastructure:** Pulumi for Infrastructure as Code

### **6.5 DataRobot SDK & API Integration**

* **Primary SDK:** All programmatic interactions with the DataRobot platform must use the `datarobot` Python package, including:
  - Agent deployment and management
  - LLM Gateway configuration
  - Vector Database operations for RAG
  - Model Registry registration
  - Runtime parameter management
* **API Documentation:** Refer to the [DataRobot API Documentation](https://docs.datarobot.com/en/docs/api/index.html) for detailed usage patterns.

### **6.6 Architecture Pattern**

* **Hybrid State Machine/Pipeline:** The system uses a hybrid state machine/pipeline pattern to enforce structure while allowing bounded user interaction. The orchestrator (`scoper_shared/orchestrator.py`) manages state transitions and enforces gate conditions.
* **Knowledge Base Storage:** Master Questionnaires stored as JSON files, Platform Guides stored as Markdown files in a known directory structure (e.g., `scoper_shared/kb_content/`). These will be loaded into DataRobot's Vector Database for RAG operations.
* **State Management:** Orchestrator manages state transitions and enforces gate conditions, with all state persisted in the database for workflow resumption.

## **7\. Non-Goals (Out of Scope)**

* **Direct Client Interaction:** This tool will **not** be client-facing. It is for internal PS staff only
* **Web Search:** The system will **not** have the ability to search the public internet for information. It is restricted to its internal Knowledge Base
* **Accessing Prior Project Data:** The KB will **not** include or be trained on data from previous client projects. It is limited to official templates (Master Questionnaires) and guides (Internal Platform Guides)
* **Synchronous Chat:** The MVP will **not** be a real-time, single-session chatbot. The clarification loop is explicitly asynchronous (one question at a time)
* **In-App Editing:** The user will **not** be able to edit the generated artifacts within this tool. The tool's purpose is generation and export
* **UI for KB Management:** This PRD does **not** include requirements for a UI to manage the Knowledge Base (e.g., editing Master Questions or platform guides). KB management is expected to be done via file system updates

## **8\. Open Questions**

The following questions remain open and may need clarification during implementation:

1. **Vector Database Configuration:** What is the specific DataRobot Vector Database endpoint and authentication mechanism for RAG operations? How will embeddings be generated and stored?
2. **Agent Deployment Strategy:** Should all four agents be deployed to the same DataRobot environment, or can they be distributed across environments? What are the networking requirements between agents?
3. **Workflow State Persistence:** What is the expected retention period for workflow state in the database? Should completed workflows be archived or deleted after a certain period?
4. **LLM Model Selection:** Which specific LLM models should be used for each agent? Should all agents use the same model, or can different models be configured per agent based on task complexity?
5. **Error Recovery:** What is the expected behavior when an agent fails mid-workflow? Should the system support workflow resumption from the last successful state?