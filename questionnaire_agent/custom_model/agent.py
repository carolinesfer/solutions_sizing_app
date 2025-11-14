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
Questionnaire Agent implementation using pydantic-ai.

This agent generates tailored questionnaires by selecting relevant questions
from a Master Knowledge Base and creating new questions for identified gaps.
"""

import json
from typing import Any

from opentelemetry import trace
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from config import Config
from scoper_shared.schemas import FactExtractionModel, QuestionnaireDraft
from scoper_shared.utils import KBRetriever, domain_router

config = Config()
tracer = trace.get_tracer(__name__)

# System prompt for Questionnaire Agent
SYSTEM_PROMPT = """You are a scoping specialist. You will be given a FactExtractionModel containing facts and gaps from a user's request, and a list of Master Questions from a Knowledge Base. Your task is to:
1. Select *only* the relevant questions from the Master List based on the facts provided.
2. Use the identified_gaps from the FactExtractionModel to generate new, critical 'delta_questions'.
3. Populate the rationale field for any delta questions you create.
4. You must output *only* the Pydantic QuestionnaireDraft JSON."""

# Create the agent with structured output
questionnaire_agent = Agent(
    model=OpenAIModel("gpt-4o-mini"),
    system_prompt=SYSTEM_PROMPT,
    result_type=QuestionnaireDraft,
)


class QuestionnaireAgent:
    """
    Questionnaire Agent (Agent 2).

    This agent generates tailored questionnaires by selecting relevant questions
    from the Master KB and creating new questions for identified gaps.
    It uses pydantic-ai to ensure structured output conforming to QuestionnaireDraft.
    """

    def __init__(self, model_name: str | None = None, api_key: str | None = None) -> None:
        """
        Initialize the Questionnaire Agent.

        Args:
            model_name: Optional model name to use. If None, uses config default.
            api_key: Optional API key for LLM. If None, uses environment/config.
        """
        self.model_name = model_name or config.llm_default_model
        self.api_key = api_key
        self.kb_retriever = KBRetriever()
        # Update agent model if custom model provided
        if model_name:
            self.agent = Agent(
                model=OpenAIModel(model_name),
                system_prompt=SYSTEM_PROMPT,
                result_type=QuestionnaireDraft,
            )
        else:
            self.agent = questionnaire_agent

    async def run(self, facts: FactExtractionModel) -> QuestionnaireDraft:
        """
        Run the questionnaire agent on the extracted facts.

        This method selects relevant questions from the Master KB and generates
        delta questions for identified gaps, returning a validated QuestionnaireDraft.

        Args:
            facts: FactExtractionModel containing extracted requirements and gaps.

        Returns:
            QuestionnaireDraft with selected questions and generated delta questions.

        Example:
            ```python
            agent = QuestionnaireAgent()
            facts = FactExtractionModel(...)
            draft = await agent.run(facts)
            ```
        """
        with tracer.start_as_current_span("questionnaire_agent.run") as span:
            # Set input attributes
            span.set_attribute("input.use_case_title", facts.use_case_title)
            span.set_attribute(
                "input.technical_confidence_score", facts.technical_confidence_score
            )
            span.set_attribute(
                "input.requirements_count", len(facts.key_extracted_requirements)
            )
            span.set_attribute("input.gaps_count", len(facts.identified_gaps))
            span.set_attribute("input.domain_keywords", str(facts.domain_keywords))

            # Route to get domain tracks
            tracks = domain_router(facts)
            span.set_attribute("input.selected_tracks", str(tracks))

            # Retrieve Master Questionnaire
            with tracer.start_as_current_span("question_selection") as kb_span:
                try:
                    master_questions = self.kb_retriever.get_master_questionnaire()
                    kb_span.set_attribute("master_questions_count", len(master_questions))

                    # Filter questions by tracks
                    relevant_questions = [
                        q
                        for q in master_questions
                        if not q.tracks or any(track in q.tracks for track in tracks)
                    ]
                    kb_span.set_attribute("filtered_questions_count", len(relevant_questions))

                except Exception as e:
                    kb_span.record_exception(e)
                    # Fallback: use empty list if KB retrieval fails
                    master_questions = []
                    relevant_questions = []

            # Prepare prompt with facts and master questions
            master_questions_json = json.dumps(
                [q.model_dump() for q in relevant_questions], indent=2
            )
            facts_json = facts.model_dump_json(indent=2)

            prompt = f"""FactExtractionModel:
{facts_json}

Master Questions (filtered by domain tracks):
{master_questions_json}

Please:
1. Select only the relevant questions from the Master List based on the facts provided.
2. Generate new delta_questions for the identified_gaps: {facts.identified_gaps}
3. Populate the rationale field for any delta questions you create.
4. Calculate a coverage_estimate (0.0-1.0) based on how well the selected questions cover the requirements.
5. Output *only* the Pydantic QuestionnaireDraft JSON."""

            # Generate delta questions with nested span
            with tracer.start_as_current_span("delta_question_generation") as delta_span:
                delta_span.set_attribute("gaps_count", len(facts.identified_gaps))

                # Create nested span for LLM call
                with tracer.start_as_current_span("questionnaire_agent.llm_call") as llm_span:
                    try:
                        # Run the agent
                        result = await self.agent.run(prompt)
                        draft = result.data

                        # Set LLM call attributes
                        llm_span.set_attribute("model", self.model_name)
                        if result.usage:
                            llm_span.set_attribute(
                                "usage.prompt_tokens", result.usage.prompt_tokens or 0
                            )
                            llm_span.set_attribute(
                                "usage.completion_tokens", result.usage.completion_tokens or 0
                            )
                            llm_span.set_attribute(
                                "usage.total_tokens", result.usage.total_tokens or 0
                            )

                    except Exception as e:
                        llm_span.record_exception(e)
                        raise

                # Set delta question generation attributes
                delta_span.set_attribute(
                    "delta_questions_generated", len(draft.delta_questions)
                )

            # Set output attributes
            span.set_attribute("output.selected_from_master_count", len(draft.selected_from_master_ids))
            span.set_attribute("output.delta_questions_count", len(draft.delta_questions))
            span.set_attribute("output.total_questions_count", len(draft.questions))
            span.set_attribute("output.coverage_estimate", draft.coverage_estimate)

            # Add event when questionnaire draft completes
            span.add_event(
                "questionnaire_draft_completed",
                {
                    "selected_count": len(draft.selected_from_master_ids),
                    "delta_count": len(draft.delta_questions),
                    "coverage": draft.coverage_estimate,
                },
            )

            return draft

    async def run_from_json(self, input_json: str | dict[str, Any]) -> QuestionnaireDraft:
        """
        Run the agent from JSON input.

        Args:
            input_json: JSON string or dict containing FactExtractionModel data.

        Returns:
            QuestionnaireDraft with selected and generated questions.
        """
        if isinstance(input_json, str):
            facts = FactExtractionModel.model_validate_json(input_json)
        else:
            facts = FactExtractionModel.model_validate(input_json)
        return await self.run(facts)


# For backward compatibility with DataRobot template
MyAgent = QuestionnaireAgent
