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
Architecture Agent implementation using pydantic-ai.

This agent generates solution architecture plans using validated requirements
and RAG context from internal platform guides.
"""

from typing import Any

import datarobot as dr
from opentelemetry import trace
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from config import Config
from scoper_shared.schemas import ArchitecturePlan, QuestionnaireFinal
from scoper_shared.utils import KBRetriever

# Note: RAG system (scoper_shared.utils.rag_system) will be implemented in task 6.0.
# For MVP, using KBRetriever.get_platform_guides() as a placeholder.

config = Config()
tracer = trace.get_tracer(__name__)

# System prompt for Architecture Agent
SYSTEM_PROMPT = """You are a master solutions architect. You will be given a QuestionnaireFinal with validated user requirements and RAG context from our Internal Platform Guides. Your task is to generate a step-by-step implementation plan.
1. The plan must have between 10-16 steps covering data ingest, preprocessing, modeling, evaluation, deployment, and monitoring.
2. Ground your recommendations in the provided RAG context.
3. Identify key assumptions and risks.
4. For each step, you *must* populate the `inputs` and `outputs` fields with brief, clear descriptions (e.g., 'Inputs: Raw customer data', 'Outputs: Cleansed data frame')
5. You must output *only* the Pydantic ArchitecturePlan JSON."""


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
    architecture_agent = Agent(
        model=_create_model("gpt-4o-mini"),
        system_prompt=SYSTEM_PROMPT,
        output_type=ArchitecturePlan,
    )
else:
    # For LLM Gateway, create agent lazily in __init__ to avoid auth at import time
    architecture_agent = None


class ArchitectureAgent:
    """
    Architecture Agent (Agent 4).

    This agent generates solution architecture plans using validated requirements
    and RAG context from internal platform guides. It ensures the plan has 10-16
    steps with inputs/outputs populated.
    """

    def __init__(
        self, model_name: str | None = None, api_key: str | None = None
    ) -> None:
        """
        Initialize the Architecture Agent.

        Args:
            model_name: Optional model name to use. If None, uses config default.
            api_key: Optional API key for LLM. If None, uses environment/config.
                      Ignored when using DataRobot LLM Gateway (uses DataRobot API token).
        """
        self.model_name = model_name or config.llm_default_model
        self.api_key = api_key
        self.kb_retriever = KBRetriever()
        # Create model with appropriate configuration
        model = _create_model(self.model_name)
        # Override api_key if provided and not using LLM Gateway
        if api_key and not config.use_datarobot_llm_gateway:
            provider = OpenAIProvider(api_key=api_key)
            model = OpenAIModel(self.model_name, provider=provider)
        # Use global agent if available and not using LLM Gateway, and no custom model_name or api_key
        # (if api_key is provided, we must use the newly created model with that api_key)
        if (
            architecture_agent is not None
            and not config.use_datarobot_llm_gateway
            and not model_name
            and not api_key
        ):
            self.agent = architecture_agent
        else:
            self.agent = Agent(
                model=model,
                system_prompt=SYSTEM_PROMPT,
                output_type=ArchitecturePlan,
            )

    async def run(
        self, questionnaire_final: QuestionnaireFinal, rag_context: str | None = None
    ) -> tuple[ArchitecturePlan, str]:
        """
        Run the architecture agent on the final questionnaire.

        This method retrieves RAG context from Platform Guides and generates
        a step-by-step architecture plan with 10-16 steps.

        Args:
            questionnaire_final: QuestionnaireFinal with validated requirements.
            rag_context: Optional pre-retrieved RAG context. If None, will retrieve from KB.

        Returns:
            Tuple of (ArchitecturePlan, Markdown string representation).

        Example:
            ```python
            agent = ArchitectureAgent()
            questionnaire = QuestionnaireFinal(...)
            plan, markdown = await agent.run(questionnaire)
            ```
        """
        with tracer.start_as_current_span("architecture_agent.run") as span:
            # Set input attributes
            span.set_attribute("input.answered_pct", questionnaire_final.answered_pct)
            span.set_attribute("input.qas_count", len(questionnaire_final.qas))
            span.set_attribute("input.gaps_count", len(questionnaire_final.gaps))

            # Retrieve RAG context from Platform Guides
            with tracer.start_as_current_span("rag_context_retrieval") as rag_span:
                try:
                    # Extract domain tracks from questionnaire (if available)
                    # For MVP, we'll use a simple approach: get all platform guides
                    # In full implementation, this would use the RAG system (task 6.0)
                    # For now, we'll use KBRetriever to get platform guides
                    # and combine them as context

                    # Get all tracks (we'll use a default set for now)
                    tracks = ["classic_ml", "time_series", "nlp", "cv", "genai_rag"]
                    guides = self.kb_retriever.get_platform_guides(tracks)

                    # Combine guides into context string
                    if guides:
                        rag_context = "\n\n".join(
                            [
                                f"## {track}\n{content}"
                                for track, content in guides.items()
                            ]
                        )
                    else:
                        rag_context = "No platform guides available. Use DataRobot best practices."

                    rag_span.set_attribute("query", "platform_guides")
                    rag_span.set_attribute("chunks_retrieved", len(guides))
                    rag_span.set_attribute("guide_tracks", str(list(guides.keys())))

                except Exception as e:
                    rag_span.record_exception(e)
                    # Fallback: use default context
                    rag_context = (
                        "Use DataRobot best practices for ML/AI solution architecture."
                    )

            # Prepare prompt with questionnaire and RAG context
            questionnaire_json = questionnaire_final.model_dump_json(indent=2)

            prompt = f"""QuestionnaireFinal:
{questionnaire_json}

RAG Context from Internal Platform Guides:
{rag_context}

Please generate a step-by-step implementation plan:
1. The plan must have between 10-16 steps covering data ingest, preprocessing, modeling, evaluation, deployment, and monitoring.
2. Ground your recommendations in the provided RAG context.
3. Identify key assumptions and risks.
4. For each step, you *must* populate the `inputs` and `outputs` fields with brief, clear descriptions.
5. Output *only* the Pydantic ArchitecturePlan JSON."""

            # Generate architecture plan with nested span
            with tracer.start_as_current_span("architecture_generation") as gen_span:
                # Create nested span for LLM call
                with tracer.start_as_current_span(
                    "architecture_agent.llm_call"
                ) as llm_span:
                    try:
                        # Run the agent
                        result = await self.agent.run(prompt)
                        plan = result.data

                        # Validate step count (10-16)
                        if len(plan.steps) < 10 or len(plan.steps) > 16:
                            # Log warning but don't fail
                            span.add_event(
                                "step_count_warning",
                                {
                                    "step_count": len(plan.steps),
                                    "expected_range": "10-16",
                                },
                            )

                        # Set LLM call attributes
                        llm_span.set_attribute("model", self.model_name)
                        if result.usage:
                            llm_span.set_attribute(
                                "usage.prompt_tokens", result.usage.prompt_tokens or 0
                            )
                            llm_span.set_attribute(
                                "usage.completion_tokens",
                                result.usage.completion_tokens or 0,
                            )
                            llm_span.set_attribute(
                                "usage.total_tokens", result.usage.total_tokens or 0
                            )

                    except Exception as e:
                        llm_span.record_exception(e)
                        raise

                # Set architecture generation attributes
                gen_span.set_attribute("steps_generated", len(plan.steps))
                gen_span.set_attribute("assumptions_count", len(plan.assumptions))
                gen_span.set_attribute("risks_count", len(plan.risks))

            # Generate Markdown representation
            markdown = self._plan_to_markdown(plan)

            # Set output attributes
            span.set_attribute("output.steps_count", len(plan.steps))
            span.set_attribute("output.assumptions_count", len(plan.assumptions))
            span.set_attribute("output.risks_count", len(plan.risks))
            span.set_attribute("output.markdown_length", len(markdown))

            # Add event when architecture plan completes
            span.add_event(
                "architecture_plan_completed",
                {
                    "steps_count": len(plan.steps),
                    "assumptions_count": len(plan.assumptions),
                    "risks_count": len(plan.risks),
                },
            )

            return (plan, markdown)

    def _plan_to_markdown(self, plan: ArchitecturePlan) -> str:
        """
        Convert ArchitecturePlan to Markdown string.

        Args:
            plan: ArchitecturePlan to convert.

        Returns:
            Markdown string representation of the plan.
        """
        lines = [
            "# Solution Architecture Plan",
            "",
            f"**Use Case:** Architecture Plan with {len(plan.steps)} steps",
            "",
            "## Implementation Steps",
            "",
        ]

        for step in plan.steps:
            lines.append(f"### Step {step.id}: {step.name}")
            lines.append("")
            lines.append(f"**Purpose:** {step.purpose}")
            lines.append("")
            if step.inputs:
                lines.append("**Inputs:**")
                for inp in step.inputs:
                    lines.append(f"- {inp}")
                lines.append("")
            if step.outputs:
                lines.append("**Outputs:**")
                for out in step.outputs:
                    lines.append(f"- {out}")
                lines.append("")

        if plan.assumptions:
            lines.append("## Assumptions")
            lines.append("")
            for assumption in plan.assumptions:
                lines.append(f"- {assumption}")
            lines.append("")

        if plan.risks:
            lines.append("## Risks")
            lines.append("")
            for risk in plan.risks:
                lines.append(f"- {risk}")
            lines.append("")

        if plan.notes:
            lines.append("## Notes")
            lines.append("")
            lines.append(plan.notes)
            lines.append("")

        return "\n".join(lines)

    async def run_from_json(
        self, input_json: str | dict[str, Any], rag_context: str | None = None
    ) -> tuple[ArchitecturePlan, str]:
        """
        Run the agent from JSON input.

        Args:
            input_json: JSON string or dict containing QuestionnaireFinal data.
            rag_context: Optional pre-retrieved RAG context.

        Returns:
            Tuple of (ArchitecturePlan, Markdown string).
        """
        if isinstance(input_json, str):
            questionnaire = QuestionnaireFinal.model_validate_json(input_json)
        else:
            questionnaire = QuestionnaireFinal.model_validate(input_json)
        return await self.run(questionnaire, rag_context)


# For backward compatibility with DataRobot template
MyAgent = ArchitectureAgent
