## **Unified Engineering Design Document: Agentic Professional Services Scoper (Hybrid MVP)**

| Field | Value |
| :---- | :---- |
| **Document Owner** | Engineering Lead / AI Architect |
| **Date** | November 2025 |
| **Related PRD** | Agentic Professional Services Scoper (MVP v1.0) |
| **Technology Stack** | Python, LLMs (Gemini), Pydantic, Agent Framework (e.g., Pydantic Agents) |
| **Target Architecture** | Hybrid State Machine/Pipeline |

### **1\. Goal and Technical Rationale 🎯**

#### **1.1 Goal Alignment**

The primary technical goal of this MVP is to replace the manual, inconsistent process of initial requirement analysis with a robust, automated pipeline that generates two standardized, high-quality artifacts:

1. **Tailored Deep-Dive Questionnaire** (Structured Pydantic JSON).  
2. **Preliminary Solution Design/Architecture Plan** (Structured Markdown Text).

#### **1.2 Rationale for Hybrid State Machine/Pipeline Pattern**

The task of converting unstructured text into highly structured outputs requires both strict validation and the ability for user interaction. This hybrid pattern is adopted to enforce structure while allowing for a bounded clarification loop.

* **Reliability & Validation:** The initial agent's output is strictly validated by the FactExtractionModel (Pydantic), ensuring clean, standardized data for all downstream agents.  
* **Specialization:** Each agent is given a specific, bounded task (e.g., extract facts, generate questions, draft architecture), optimizing prompt engineering and model behavior.  
* **Clarification:** The explicit Clarifier Agent and Q\_CLARIFY loop allows the system to fill high-impact informational gaps by engaging the user, a critical step for improving final architecture quality.

### **2\. Unified Agent Architecture** 

The system utilizes four distinct, specialized agents and two critical utilities, executed in a state-managed sequence.

#### **2.1 Unified Agent Architecture Breakdown** 🏗️ 

This table defines the agents. 

| \# | Component Name | Component Type | Primary Input | Primary Output Schema | Key Responsibility |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **0** | **Orchestrator** | Agent (State Machine) | State Transitions | N/A (Control) | Drives phases and manages gating. |
| **1** | **Requirement Analyzer** | Agent | Raw User Text/Transcript | **FactExtractionModel** | **Decomposition & Fact Extraction**. |
| **2** | **Questionnaire Agent** | Agent | FactExtractionModel \+ **KB (Master Q's)** | **QuestionnaireDraft** | **Structuring & Scoping**. |
| **3** | **Clarifier Agent** | Agent | QuestionnaireDraft \+ Current Answers | **QuestionnaireFinal** | **Gap Filling** (Bounded loop). |
| **4** | **Architecture Agent** | Agent | QuestionnaireFinal \+ **RAG Context** | **ArchitecturePlan** and Markdown String | **Generation & Grounding** in internal guides. |
| **U1** | **Domain Router** | Utility (Function) | FactExtractionModel | Selected Tracks (e.g., time\_series) | Simple rules/embedding match to choose the track(s). |
| **U2** | **KB Retriever** | Utility (Function) | Query | Retrieved KB content | Fetches templates, internal guides, and frames for agents. |

#### **2.2 Baseline Agent Prompts** 

This section provides the baseline system prompts and tasks for each agent in the chain.

**Agent 1: Requirement Analyzer**

* **Input:** Raw User Text/Transcript (as a UseCaseInput schema ).  
* **Output:** FactExtractionModel schema.  
* **System Prompt:** "You are a senior solutions architect. Your sole task is to read the following user query and transcript and extract key information. Identify the core goal, all technical requirements, any mentioned data sources, and any clear informational gaps. You must output *only* the Pydantic FactExtractionModel JSON. Do not add conversational text. Pay special attention to keywords that suggest the project domain (e.g., 'forecast', 'time series', 'NLP', 'images', 'agentic')."

**Agent 2: Questionnaire Agent**

* **Input:** FactExtractionModel (from Agent 1\) and KB (Master Q's).  
* **Output:** QuestionnaireDraft schema.  
* **System Prompt:** "You are a scoping specialist. You will be given a FactExtractionModel containing facts and gaps from a user's request, and a list of Master Questions from a Knowledge Base. Your task is to:  
  1. Select *only* the relevant questions from the Master List based on the facts provided.  
  2. Use the identified\_gaps from the FactExtractionModel to generate new, critical 'delta\_questions'.  
  3. Populate the rationale field for any delta questions you create.  
  4. You must output *only* the Pydantic QuestionnaireDraft JSON."

**Agent 3: Clarifier Agent**

* **Input:** QuestionnaireDraft \+ Current Answers.  
* **Output:** QuestionnaireFinal schema.  
* **System Prompt:** "You are an interviewer. You will be given a QuestionnaireDraft and a list of current answers. Your goal is to fill the remaining high-impact gaps. Ask up to K (e.g., K=5) high-value follow-up questions to the user, one at a time. Prefer single-choice or boolean questions. Once the loop is complete, compile all Q\&A pairs and output *only* the Pydantic QuestionnaireFinal JSON."

**Agent 4: Architecture Agent**

* **Input:** QuestionnaireFinal \+ RAG Context (from Internal Platform Guides).  
* **Output:** ArchitecturePlan schema and Markdown String.  
* **System Prompt:** "You are a master solutions architect. You will be given a QuestionnaireFinal with validated user requirements and RAG context from our Internal Platform Guides. Your task is to generate a step-by-step implementation plan.  
  1. The plan must have between 10-16 steps covering data ingest, preprocessing, modeling, evaluation, deployment, and monitoring.  
  2. Ground your recommendations in the provided RAG context.  
  3. Identify key assumptions and risks.  
  4. For each step, you *must* populate the `inputs` and `outputs` fields with brief, clear descriptions (e.g., 'Inputs: Raw customer data', 'Outputs: Cleansed data frame')  
  5. You must output *only* the Pydantic ArchitecturePlan JSON."

### **3\. Control Flow & Utilities**

The system's control flow is managed by the Orchestrator as a sequence of states with explicit gates.

####  **3.1 Unified Control Flow (State Machine)** ⚙️

| State Name | Component | Status | Description |
| :---- | :---- | :---- | :---- |
| **INGEST** | User/System Input | Input | Receives the UseCaseInput (paragraph/transcript). |
| **ANALYZE** | Requirement Analyzer (Agent 1\) | Agent | Extracts facts and gaps into the FactExtractionModel. |
| **ROUTE** | Domain Router (U1) | Function | **Chooses the track(s)** based on FactExtractionModel data. |
| **KB\_FETCH** | KB Retriever (U2) | Function | **Fetches the relevant Master Questionnaire** and Platform Guides based on the selected tracks. |
| **Q\_DRAFT** | Questionnaire Agent (Agent 2\) | Agent | Creates the initial **QuestionnaireDraft** using the fetched Master Q's. |
| **Q\_CLARIFY** | Clarifier Agent (Agent 3\) | Agent (Loop) | Runs the short interview loop ($\\leq K$ questions) to update to **QuestionnaireFinal**. |
| **Q\_FREEZE** | Orchestrator/Gate | Gate | **Gate Condition:** Proceeds only if $\\geq 80\\%$ of required questions are answered OR coverage $\\geq 0.8$. |
| **PLAN\_ARCH** | Architecture Agent (Agent 4\) | Agent | Generates the final **ArchitecturePlan** and Markdown artifact, using RAG/KB content. |
| **DONE** | System Output | Final | Delivers the two primary artifacts. |

### **3.2 Utility Implementation** 

This clarifies the implementation of the non-agent utilities.

**U1: Domain Router (Function)**

* Purpose: To select the 'track(s)' (e.g., time\_series, classic\_ml, genai\_rag, agentic) needed to fetch the correct KB documents.  
* Input: FactExtractionModel (specifically, a field like domain\_keywords or key\_extracted\_requirements).  
* Logic (Pseudo-code): This will be a simple, rule-based function, not an LLM.

```py
def domain_router(facts: FactExtractionModel) -> list[str]:
    tracks = set()
    # Combine requirements and title for keyword search
    search_text = " ".join(facts.key_extracted_requirements).lower()
    search_text += facts.use_case_title.lower()

    if "forecast" in search_text or "time series" in search_text:
        tracks.add("time_series")
    if "nlp" in search_text or "text" in search_text:
        tracks.add("nlp")
    if "image" in search_text or "cv" in search_text:
        tracks.add("cv")
    if "agent" in search_text or "rag" in search_text:
        tracks.add("genai_rag")

    if not tracks:
        tracks.add("classic_ml") # Default track

    return list(tracks)
```

**U2: KB Retriever (Function)**

* Purpose: To fetch KB content for agents.  
* Storage: Per, KB content (Master Questionnaire, Guides) is stored in Markdown and JSON/YAML files in a known directory (e.g., /kb\_content/).  
* Logic:  
  1. For Master Questionnaire : The function will read a file like /kb\_content/master\_questionnaire.json and parse it into a list of Question objects.  
  2. For RAG System (MVP): This utility will load all .md files from /kb\_content/platform\_guides/. It will use a simple vector search (e.g., based on FAISS or Chroma) to find and return the top N relevant chunks of text based on the QuestionnaireFinal data.

### **4\. Critical Data Contracts (Pydantic Schemas) 📝**

These models, adapted from , define the data contracts for the 4-agent workflow.

```py
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Literal

# --- INPUT SCHEMA ---

class UseCaseInput(BaseModel):
    """
    The initial user query. This is the input to Agent 1.
    [Source: 48-50]
    """
    paragraph: str = Field(..., description="The user's raw text description.")
    transcript: Optional[str] = Field(None, description="Optional call transcript text.")
    use_case_title: str

# --- CONTRACT 1 (Output of Agent 1) ---

class FactExtractionModel(BaseModel):
    """
    Output of Agent 1 (Requirement Analyzer). 
    Input for Agent 2 (Questionnaire Agent) and U1 (Domain Router).
    
    """
    use_case_title: str 
    technical_confidence_score: float = Field(..., ge=0.0, le=1.0, description="LLM's confidence in the extracted facts.") 
    key_extracted_requirements: List[str] = Field(..., description="List of specific technical or business needs.") 
    domain_keywords: List[str] = Field(default=[], description="Keywords for U1 Router (e.g., 'time series', 'nlp').")
    identified_gaps: List[str] = Field(default=[], description="Information that is clearly missing.")

# --- COMPONENT SCHEMAS (Used by Contracts 2, 3, 4) ---

class Question(BaseModel):
    """
    A single question object, used in the Master KB and Questionnaires.
    
    """
    id: str
    text: str
    type: Literal["free_text", "single_select", "multi_select", "bool"] 
    options: Optional[List[str]] = None 
    required: bool = False 
    rationale: Optional[str] = Field(None, description="Rationale for *why* this question is being asked.") 
    tracks: List[str] = Field(default=[], description="Which domains this applies to (e.g. ['time_series']).") 

class ArchitectureStep(BaseModel):
    """
    A single step in the final architecture plan.
    
    """
    id: int
    name: str = Field(..., description="Name of the step (e.g., 'Data Ingestion').")
    purpose: str = Field(..., description="Purpose of this step.")
    inputs: List[str] = Field(default=[], description="Inputs to this step.") 
    outputs: List[str] = Field(default=[], description="Outputs from this step.") 

# --- CONTRACT 2 (Output of Agent 2) ---

class QuestionnaireDraft(BaseModel):
    """
    Output of Agent 2 (Questionnaire Agent). 
    Input for Agent 3 (Clarifier Agent).
    
    """
    questions: List[Question] 
    selected_from_master_ids: List[str] = Field(..., description="IDs of questions pulled from the Master KB.") 
    delta_questions: List[Question] = Field(..., description="New questions generated by the agent for gaps.") 
    coverage_estimate: float = Field(..., ge=0.0, le=1.0, description="Agent's estimate of requirement coverage.") 

# --- CONTRACT 3 (Output of Agent 3) ---

class QuestionnaireFinal(BaseModel):
    """
    Output of Agent 3 (Clarifier Agent). 
    Input for Agent 4 (Architecture Agent). This is the FIRST deliverable.
    
    """
    qas: List[dict] = Field(..., description="List of Q&A pairs, e.g., {'id': 'q1', 'answer': 'value'}.") 
    answered_pct: float = Field(..., ge=0.0, le=1.0) 
    gaps: List[str] = Field(default=[], description="List of question IDs that remain unanswered.") 

# --- CONTRACT 4 (Output of Agent 4) ---

class ArchitecturePlan(BaseModel):
    """
    Output of Agent 4 (Architecture Agent). This is the SECOND deliverable.
  
    """
    steps: List[ArchitectureStep] = Field(..., min_items=10, max_items=16) 
    assumptions: List[str] = [] 
    risks: List[str] = [] 
    notes: Optional[str] = None 
```

### **5\. Knowledge Management and Grounding 🧠**

The system leverages specific Knowledge Base (KB) collections to ensure grounding and quality.

| KB Component | Agent Impacted | Description | Reference Documentation |
| :---- | :---- | :---- | :---- |
| **Master Questionnaire**  | Agent 2 | Canonical questions used to start the scoping process; filtered by Agent 2\. | [SCOPING MASTER SHEET](https://docs.google.com/spreadsheets/d/16p2Ul08dx1jcbD8ywnV0WS-crXm7O7fUAZ5dAt13nP0/edit?pli=1&gid=32304464#gid=32304464) [APP QUESTIONNAIRES](https://docs.google.com/spreadsheets/d/1TFIdjr9Ui1DlVs4mkJsrkdLquU5diVQQRQajDA4QVs0/edit?gid=1586512925#gid=1586512925) [Complexity Questionnaire for Predictive AI TEMPLATE](https://docs.google.com/spreadsheets/d/1aI_B0ncPtqoyZTAGBMSGI2PRrUO8z8JHyjYYPcds6s0/edit?usp=drive_link) [Catalyst Build Phase Scoping TEMPLATE](https://docs.google.com/spreadsheets/d/1S7XhxtgD695ayHfOjhCaQ0DfZtD1j7hwjvrN8vaMI_0/edit?usp=drive_link) [AI Analyst - Use Case Questionnaire TEMPLATE v02.docx](https://docs.google.com/document/d/1BSMKMeoYc7enuHuFuvvfCGwrogddLfgp/edit?usp=drive_link&ouid=107181442599516377731&rtpof=true&sd=true) [Custom Application - Use Case Questionnaire TEMPLATE v01.docx](https://docs.google.com/document/d/19hIAGRx8GGvgao4rKcrRYetfr0cwxqoQ/edit?usp=drive_link&ouid=107181442599516377731&rtpof=true&sd=true) [Execution Project Questions to Ask](https://docs.google.com/document/d/1XLTW-LubwAnem7tDRX9YLWX4VCMwDxEaAT4cGa2W9Z0/edit?usp=drive_link) [Use Case Deep Dive Workshop (Production)](https://docs.google.com/presentation/d/1YZImhG4QEh_Euea3d8qa2UGbfIQSxeK1dHWNdGarySg/edit?slide=id.g4e7e110c69_0_356#slide=id.g4e7e110c69_0_356) |
| **Internal Platform Guides**  | Agent 4 | Org-specific patterns, reference architectures, and preferred approaches used as context for the RAG system. | [https://docs.datarobot.com/en/docs/index.html](https://docs.datarobot.com/en/docs/index.html) [DataRobot Time Series II - Current](https://docs.google.com/presentation/d/1Q8cPXgUmkcB7VfbbRRxAuuntDyMn_qMtGbbNlxEwbTw/edit) [https://github.com/datarobot-community/ai-accelerators](https://github.com/datarobot-community/ai-accelerators) [https://github.com/datarobot-community/predictive-content-generator](https://github.com/datarobot-community/predictive-content-generator) [https://github.com/datarobot-community/talk-to-my-data-agent](https://github.com/datarobot-community/talk-to-my-data-agent) [https://github.com/datarobot-community/talk-to-my-docs-agents](https://github.com/datarobot-community/talk-to-my-docs-agents) |
| **Heuristics**  | Agent 1 & Agent 4 | Model family suggestions and constraints (latency, PII, etc.) used for initial recommendations and final plan checks. | Unknown \- to be determined |
| **RAG System (MVP)** | Agent 4 | Implemented to query the **Internal Platform Guides** and provide context *before* Agent 4 generates the architecture. |  |

### **6\. Scope Clarifications & Exclusions** 

This section addresses specific questions from the PRD to provide clarity for the MVP.

* **Web Search Tool:** A web search tool is **explicitly out of scope** for the MVP. The system will only use the internal Knowledge Base.  
* **Prior Client Data:** The Knowledge Base **does not** include previous project data or specific interactions with a client. The KB is limited to *templates* (Master Questionnaires) and *guides* (Internal Platform Guides).  
* **Agent 1 vs. MVP Pydantic:** This EDD explicitly uses the 4-agent architecture. The Requirement Analyzer (Agent 1\) is responsible for creating the FactExtractionModel, which is a distinct and required step *before* the Questionnaire Agent (Agent 2\) runs. This differs from the 3-agent flow proposed in MVP design Pydantic.md .

