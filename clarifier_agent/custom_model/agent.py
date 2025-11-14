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
Clarifier Agent implementation using pydantic-ai.

This agent conducts a bounded clarification loop (up to K questions, e.g., K=5)
to fill high-impact gaps through user interaction.
"""

from typing import Any, Optional

import datarobot as dr
from opentelemetry import trace
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from config import Config
from scoper_shared.schemas import QuestionnaireDraft, QuestionnaireFinal, Question

config = Config()
tracer = trace.get_tracer(__name__)

# System prompt for Clarifier Agent
SYSTEM_PROMPT = """You are an interviewer. You will be given a QuestionnaireDraft and a list of current answers. Your goal is to fill the remaining high-impact gaps. Ask up to K (e.g., K=5) high-value follow-up questions to the user, one at a time. Prefer single-choice or boolean questions. Once the loop is complete, compile all Q&A pairs and output *only* the Pydantic QuestionnaireFinal JSON."""


def _create_model(model_name: str) -> OpenAIModel:
    """
    Create an OpenAIModel configured for either DataRobot LLM Gateway or direct OpenAI.

    Args:
        model_name: Model identifier (e.g., "azure/gpt-4o-mini" for LLM Gateway or "gpt-4o-mini" for OpenAI).

    Returns:
        Configured OpenAIModel instance.
    """
    if config.use_datarobot_llm_gateway:
        # Use DataRobot LLM Gateway
        dr_client = dr.Client()
        base_url = f"{dr_client.endpoint.rstrip('/')}/genai/llmgw"
        api_key = dr_client.token
        # Create OpenAIProvider for DataRobot LLM Gateway
        provider = OpenAIProvider(
            base_url=base_url,
            api_key=api_key,
        )
        return OpenAIModel(
            model_name,
            provider=provider,
        )
    else:
        # Use direct OpenAI (requires OPENAI_API_KEY)
        return OpenAIModel(model_name)


# Create the agent with structured output (lazy initialization for LLM Gateway)
# Only create agent at module level if not using LLM Gateway (to avoid auth issues at import time)
if not config.use_datarobot_llm_gateway:
    clarifier_agent = Agent(
        model=_create_model("gpt-4o-mini"),
        system_prompt=SYSTEM_PROMPT,
        output_type=QuestionnaireFinal,
    )
else:
    # For LLM Gateway, create agent lazily in __init__ to avoid auth at import time
    clarifier_agent = None


class ClarifierAgent:
    """
    Clarifier Agent (Agent 3).

    This agent conducts a bounded clarification loop to fill high-impact gaps
    through user interaction. It asks questions one at a time (up to K=5)
    and compiles Q&A pairs into QuestionnaireFinal.
    """

    def __init__(
        self,
        model_name: str | None = None,
        api_key: str | None = None,
        max_questions: int = 5,
    ) -> None:
        """
        Initialize the Clarifier Agent.

        Args:
            model_name: Optional model name to use. If None, uses config default.
            api_key: Optional API key for LLM. If None, uses environment/config.
                      Ignored when using DataRobot LLM Gateway (uses DataRobot API token).
            max_questions: Maximum number of questions to ask (default: 5).
        """
        self.model_name = model_name or config.llm_default_model
        self.api_key = api_key
        self.max_questions = max_questions
        # Create model with appropriate configuration
        model = _create_model(self.model_name)
        # Override api_key if provided and not using LLM Gateway
        if api_key and not config.use_datarobot_llm_gateway:
            provider = OpenAIProvider(api_key=api_key)
            model = OpenAIModel(self.model_name, provider=provider)
        # Use global agent if available and not using LLM Gateway, and no custom model_name or api_key
        # (if api_key is provided, we must use the newly created model with that api_key)
        if (
            clarifier_agent is not None
            and not config.use_datarobot_llm_gateway
            and not model_name
            and not api_key
        ):
            self.agent = clarifier_agent
        else:
            self.agent = Agent(
                model=model,
                system_prompt=SYSTEM_PROMPT,
                output_type=QuestionnaireFinal,
            )

    async def ask_question(
        self,
        draft: QuestionnaireDraft,
        current_answers: list[dict[str, Any]],
        question_num: int,
    ) -> tuple[Optional[Question], str]:
        """
        Ask one question at a time (up to K=5), preferring single-choice or boolean.

        Args:
            draft: QuestionnaireDraft containing questions to ask.
            current_answers: List of current Q&A pairs (e.g., [{'id': 'q1', 'answer': 'value'}]).
            question_num: Current question number (1-indexed).

        Returns:
            Tuple of (Question object, answer string).

        Example:
            ```python
            agent = ClarifierAgent()
            draft = QuestionnaireDraft(...)
            question, answer = await agent.ask_question(draft, [], 1)
            ```
        """
        with tracer.start_as_current_span("clarifier_agent.ask_question") as span:
            span.set_attribute("question_number", question_num)
            span.set_attribute("max_questions", self.max_questions)
            span.set_attribute("current_answers_count", len(current_answers))

            # Find unanswered questions, preferring single-choice or boolean
            unanswered = [
                q
                for q in draft.questions
                if q.id not in [ans.get("id") for ans in current_answers]
            ]

            # Prefer single-choice or boolean questions
            preferred_questions = [
                q for q in unanswered if q.type in ["single_select", "bool"]
            ]
            questions_to_ask = (
                preferred_questions if preferred_questions else unanswered
            )

            if not questions_to_ask or question_num > self.max_questions:
                # No more questions or reached max
                span.add_event("no_more_questions")
                return (None, "")

            # Select the next question
            question = questions_to_ask[0]

            span.set_attribute("question_id", question.id)
            span.set_attribute("question_type", question.type)
            span.add_event(
                "question_asked",
                {"question_id": question.id, "question_text": question.text},
            )

            # Prepare prompt for asking the question
            prompt = f"""QuestionnaireDraft:
{draft.model_dump_json(indent=2)}

Current Answers:
{current_answers}

Ask question {question_num} of {self.max_questions}: {question.text}

Please provide a concise answer. If the question is single_select or bool, choose from the options: {question.options if question.options else "N/A"}"""

            # Create nested span for LLM call
            with tracer.start_as_current_span("clarifier_agent.llm_call") as llm_span:
                try:
                    # For now, we'll use a simple approach: return the question
                    # In a real implementation, this would interact with the user
                    # and get their answer. For MVP, we'll simulate this.
                    answer = "User answer pending"  # Placeholder

                    llm_span.set_attribute("model", self.model_name)

                except Exception as e:
                    llm_span.record_exception(e)
                    raise

            span.set_attribute("answer_value", answer)
            span.add_event(
                "answer_received", {"question_id": question.id, "answer": answer}
            )

            return (question, answer)

    async def finalize(
        self, draft: QuestionnaireDraft, all_answers: list[dict[str, Any]]
    ) -> QuestionnaireFinal:
        """
        Compile all Q&A pairs into QuestionnaireFinal.

        Args:
            draft: QuestionnaireDraft containing all questions.
            all_answers: List of all Q&A pairs collected during the clarification loop.

        Returns:
            QuestionnaireFinal with compiled Q&A pairs, answered percentage, and gaps.

        Example:
            ```python
            agent = ClarifierAgent()
            draft = QuestionnaireDraft(...)
            answers = [{'id': 'q1', 'answer': 'value1'}, {'id': 'q2', 'answer': 'value2'}]
            final = await agent.finalize(draft, answers)
            ```
        """
        with tracer.start_as_current_span("clarifier_agent.finalize") as span:
            # Calculate answered percentage
            total_questions = len(draft.questions)
            answered_count = len(all_answers)
            unanswered_count = total_questions - answered_count
            answered_pct = (
                answered_count / total_questions if total_questions > 0 else 0.0
            )

            # Find gaps (unanswered question IDs)
            answered_ids = {ans.get("id") for ans in all_answers}
            gaps = [q.id for q in draft.questions if q.id not in answered_ids]

            # Set attributes
            span.set_attribute("total_questions", total_questions)
            span.set_attribute("answered_count", answered_count)
            span.set_attribute("unanswered_count", unanswered_count)
            span.set_attribute("answered_pct", answered_pct)
            span.set_attribute("gaps", str(gaps))

            # Create QuestionnaireFinal
            final = QuestionnaireFinal(
                qas=all_answers,
                answered_pct=answered_pct,
                gaps=gaps,
            )

            span.add_event(
                "finalization_completed",
                {
                    "answered_count": answered_count,
                    "unanswered_count": unanswered_count,
                    "answered_pct": answered_pct,
                },
            )

            return final

    async def run(
        self,
        draft: QuestionnaireDraft,
        current_answers: list[dict[str, Any]] | None = None,
    ) -> QuestionnaireFinal:
        """
        Run the full clarification loop and finalize.

        This method asks questions one at a time (up to K) and then finalizes
        the questionnaire with all Q&A pairs.

        Args:
            draft: QuestionnaireDraft containing questions to ask.
            current_answers: Optional list of existing answers.

        Returns:
            QuestionnaireFinal with compiled Q&A pairs.
        """
        if current_answers is None:
            current_answers = []

        # Ask questions up to max_questions
        for i in range(1, self.max_questions + 1):
            question, answer = await self.ask_question(draft, current_answers, i)
            if question is None:
                break
            # Add answer to current_answers
            if question.id:  # Only add if question has valid ID
                current_answers.append({"id": question.id, "answer": answer})

        # Finalize
        return await self.finalize(draft, current_answers)

    async def run_from_json(
        self, input_json: str | dict[str, Any]
    ) -> QuestionnaireFinal:
        """
        Run the agent from JSON input.

        Args:
            input_json: JSON string or dict containing QuestionnaireDraft data.

        Returns:
            QuestionnaireFinal with compiled Q&A pairs.
        """
        if isinstance(input_json, str):
            draft = QuestionnaireDraft.model_validate_json(input_json)
        else:
            draft = QuestionnaireDraft.model_validate(input_json)
        return await self.run(draft)


# For backward compatibility with DataRobot template
MyAgent = ClarifierAgent
