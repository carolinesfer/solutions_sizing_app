# Copyright 2025 DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pydantic data models for the Agentic Professional Services Scoper system.

This module defines all data contracts used for communication between agents
in the 4-agent pipeline workflow.
"""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


# --- INPUT SCHEMA ---


class UseCaseInput(BaseModel):
    """
    The initial user query. This is the input to Agent 1 (Requirement Analyzer).

    This schema represents the raw input from the user, which may include
    a paragraph description, an optional transcript from a discovery call,
    and a use case title.

    Attributes:
        paragraph: The user's raw text description of the use case.
        transcript: Optional call transcript text from discovery meetings.
        use_case_title: Title of the use case.

    Example:
        ```python
        input_data = UseCaseInput(
            paragraph="We need to predict customer churn using historical data...",
            transcript="Call transcript from meeting with customer...",
            use_case_title="Customer Churn Prediction"
        )
        ```
    """

    paragraph: str = Field(..., description="The user's raw text description.")
    transcript: Optional[str] = Field(None, description="Optional call transcript text.")
    use_case_title: str = Field(..., description="Title of the use case.")


# --- CONTRACT 1 (Output of Agent 1) ---


class FactExtractionModel(BaseModel):
    """
    Output of Agent 1 (Requirement Analyzer).

    This schema represents the extracted facts, requirements, and identified gaps
    from the raw user input. It serves as input for Agent 2 (Questionnaire Agent)
    and U1 (Domain Router).

    Attributes:
        use_case_title: Title of the use case.
        technical_confidence_score: LLM's confidence in the extracted facts (0.0-1.0).
        key_extracted_requirements: List of specific technical or business needs.
        domain_keywords: Keywords for domain routing (e.g., 'time series', 'nlp').
        identified_gaps: Information that is clearly missing from the input.

    Example:
        ```python
        facts = FactExtractionModel(
            use_case_title="Customer Churn Prediction",
            technical_confidence_score=0.85,
            key_extracted_requirements=["Predict churn", "Use historical data"],
            domain_keywords=["classic_ml", "binary_classification"],
            identified_gaps=["Data source location", "Deployment environment"]
        )
        ```
    """

    use_case_title: str = Field(..., description="Title of the use case.")
    technical_confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="LLM's confidence in the extracted facts.",
    )
    key_extracted_requirements: List[str] = Field(
        ...,
        description="List of specific technical or business needs.",
    )
    domain_keywords: List[str] = Field(
        default=[],
        description="Keywords for U1 Router (e.g., 'time series', 'nlp').",
    )
    identified_gaps: List[str] = Field(
        default=[],
        description="Information that is clearly missing.",
    )


# --- COMPONENT SCHEMAS (Used by Contracts 2, 3, 4) ---


class Question(BaseModel):
    """
    A single question object, used in the Master KB and Questionnaires.

    This schema represents a question that can be asked to the user during
    the scoping process. Questions can be of different types and may be
    associated with specific domain tracks.

    Attributes:
        id: Unique identifier for the question.
        text: The question text to be asked.
        type: Type of question (free_text, single_select, multi_select, bool).
        options: Optional list of options for single/multi-select questions.
        required: Whether this question is required to be answered.
        rationale: Rationale for why this question is being asked.
        tracks: Which domains this applies to (e.g., ['time_series']).

    Example:
        ```python
        question = Question(
            id="q1",
            text="What is the primary data source?",
            type="single_select",
            options=["Database", "API", "File upload"],
            required=True,
            rationale="Need to understand data ingestion requirements",
            tracks=["classic_ml", "time_series"]
        )
        ```
    """

    id: str = Field(..., description="Unique identifier for the question.")
    text: str = Field(..., description="The question text to be asked.")
    type: Literal["free_text", "single_select", "multi_select", "bool"] = Field(
        ...,
        description="Type of question.",
    )
    options: Optional[List[str]] = Field(
        None,
        description="Optional list of options for single/multi-select questions.",
    )
    required: bool = Field(
        False,
        description="Whether this question is required to be answered.",
    )
    rationale: Optional[str] = Field(
        None,
        description="Rationale for *why* this question is being asked.",
    )
    tracks: List[str] = Field(
        default=[],
        description="Which domains this applies to (e.g. ['time_series']).",
    )


class ArchitectureStep(BaseModel):
    """
    A single step in the final architecture plan.

    This schema represents one step in the solution architecture, including
    its purpose, inputs, and outputs.

    Attributes:
        id: Unique identifier for the step (typically sequential).
        name: Name of the step (e.g., 'Data Ingestion').
        purpose: Purpose of this step.
        inputs: List of inputs to this step.
        outputs: List of outputs from this step.

    Example:
        ```python
        step = ArchitectureStep(
            id=1,
            name="Data Ingestion",
            purpose="Extract data from source systems",
            inputs=["Raw customer data", "Database connection"],
            outputs=["Cleansed data frame", "Data quality report"]
        )
        ```
    """

    id: int = Field(..., description="Unique identifier for the step.")
    name: str = Field(..., description="Name of the step (e.g., 'Data Ingestion').")
    purpose: str = Field(..., description="Purpose of this step.")
    inputs: List[str] = Field(
        default=[],
        description="Inputs to this step.",
    )
    outputs: List[str] = Field(
        default=[],
        description="Outputs from this step.",
    )


# --- CONTRACT 2 (Output of Agent 2) ---


class QuestionnaireDraft(BaseModel):
    """
    Output of Agent 2 (Questionnaire Agent).

    This schema represents the initial questionnaire draft created by selecting
    relevant questions from the Master KB and generating new questions for
    identified gaps. It serves as input for Agent 3 (Clarifier Agent).

    Attributes:
        questions: List of all questions (selected + delta).
        selected_from_master_ids: IDs of questions pulled from the Master KB.
        delta_questions: New questions generated by the agent for gaps.
        coverage_estimate: Agent's estimate of requirement coverage (0.0-1.0).

    Example:
        ```python
        draft = QuestionnaireDraft(
            questions=[question1, question2, question3],
            selected_from_master_ids=["q1", "q2"],
            delta_questions=[question3],
            coverage_estimate=0.75
        )
        ```
    """

    questions: List[Question] = Field(
        ...,
        description="List of all questions (selected from master + delta questions).",
    )
    selected_from_master_ids: List[str] = Field(
        ...,
        description="IDs of questions pulled from the Master KB.",
    )
    delta_questions: List[Question] = Field(
        ...,
        description="New questions generated by the agent for gaps.",
    )
    coverage_estimate: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Agent's estimate of requirement coverage.",
    )


# --- CONTRACT 3 (Output of Agent 3) ---


class QuestionnaireFinal(BaseModel):
    """
    Output of Agent 3 (Clarifier Agent).

    This schema represents the final questionnaire with all Q&A pairs compiled
    after the clarification loop. This is the FIRST deliverable and serves as
    input for Agent 4 (Architecture Agent).

    Attributes:
        qas: List of Q&A pairs, e.g., {'id': 'q1', 'answer': 'value'}.
        answered_pct: Percentage of questions answered (0.0-1.0).
        gaps: List of question IDs that remain unanswered.

    Example:
        ```python
        final = QuestionnaireFinal(
            qas=[
                {"id": "q1", "answer": "Database"},
                {"id": "q2", "answer": "Yes"}
            ],
            answered_pct=0.90,
            gaps=["q3"]
        )
        ```
    """

    qas: List[dict] = Field(
        ...,
        description="List of Q&A pairs, e.g., {'id': 'q1', 'answer': 'value'}.",
    )
    answered_pct: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Percentage of questions answered.",
    )
    gaps: List[str] = Field(
        default=[],
        description="List of question IDs that remain unanswered.",
    )


# --- CONTRACT 4 (Output of Agent 4) ---


class ArchitecturePlan(BaseModel):
    """
    Output of Agent 4 (Architecture Agent).

    This schema represents the final solution architecture plan with step-by-step
    implementation details. This is the SECOND deliverable.

    Attributes:
        steps: List of 10-16 architecture steps.
        assumptions: List of key assumptions made in the plan.
        risks: List of identified risks.
        notes: Optional notes or additional context.

    Example:
        ```python
        plan = ArchitecturePlan(
            steps=[step1, step2, ..., step12],
            assumptions=["Data quality is acceptable", "API access available"],
            risks=["Data privacy concerns", "Latency requirements"],
            notes="Additional considerations..."
        )
        ```
    """

    steps: List[ArchitectureStep] = Field(
        ...,
        min_length=10,
        max_length=16,
        description="List of architecture steps (must be 10-16 steps).",
    )
    assumptions: List[str] = Field(
        default=[],
        description="List of key assumptions made in the plan.",
    )
    risks: List[str] = Field(
        default=[],
        description="List of identified risks.",
    )
    notes: Optional[str] = Field(
        None,
        description="Optional notes or additional context.",
    )

