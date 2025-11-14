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
Requirement Analyzer Agent implementation using pydantic-ai.

This agent extracts facts, requirements, and identifies gaps from raw user input.
"""

from typing import Any

import datarobot as dr
from opentelemetry import trace
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from config import Config
from scoper_shared.schemas import FactExtractionModel, UseCaseInput

config = Config()
tracer = trace.get_tracer(__name__)

# System prompt for Requirement Analyzer Agent
SYSTEM_PROMPT = """You are a senior solutions architect. Your sole task is to read the following user query and transcript and extract key information. Identify the core goal, all technical requirements, any mentioned data sources, and any clear informational gaps. You must output *only* the Pydantic FactExtractionModel JSON. Do not add conversational text. Pay special attention to keywords that suggest the project domain (e.g., 'forecast', 'time series', 'NLP', 'images', 'agentic')."""


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
    requirement_analyzer_agent = Agent(
        model=_create_model("gpt-4o-mini"),
        system_prompt=SYSTEM_PROMPT,
        output_type=FactExtractionModel,
    )
else:
    # For LLM Gateway, create agent lazily in __init__ to avoid auth at import time
    requirement_analyzer_agent = None


class RequirementAnalyzerAgent:
    """
    Requirement Analyzer Agent (Agent 1).

    This agent extracts facts, requirements, and identifies gaps from raw user input.
    It uses pydantic-ai to ensure structured output conforming to FactExtractionModel.
    """

    def __init__(
        self, model_name: str | None = None, api_key: str | None = None
    ) -> None:
        """
        Initialize the Requirement Analyzer Agent.

        Args:
            model_name: Optional model name to use. If None, uses config default.
            api_key: Optional API key for LLM. If None, uses environment/config.
                      Ignored when using DataRobot LLM Gateway (uses DataRobot API token).
        """
        self.model_name = model_name or config.llm_default_model
        self.api_key = api_key
        # Create model with appropriate configuration
        model = _create_model(self.model_name)
        # Override api_key if provided and not using LLM Gateway
        if api_key and not config.use_datarobot_llm_gateway:
            provider = OpenAIProvider(api_key=api_key)
            model = OpenAIModel(self.model_name, provider=provider)
        # Use global agent if available and not using LLM Gateway, and no custom model_name or api_key
        # (if api_key is provided, we must use the newly created model with that api_key)
        if (
            requirement_analyzer_agent is not None
            and not config.use_datarobot_llm_gateway
            and not model_name
            and not api_key
        ):
            self.agent = requirement_analyzer_agent
        else:
            self.agent = Agent(
                model=model,
                system_prompt=SYSTEM_PROMPT,
                output_type=FactExtractionModel,
            )

    async def run(self, input_data: UseCaseInput) -> FactExtractionModel:
        """
        Run the requirement analyzer agent on the input data.

        This method extracts facts, requirements, and gaps from the user input
        and returns a validated FactExtractionModel.

        Args:
            input_data: UseCaseInput containing paragraph, transcript, and use_case_title.

        Returns:
            FactExtractionModel with extracted facts, requirements, and gaps.

        Example:
            ```python
            agent = RequirementAnalyzerAgent()
            input_data = UseCaseInput(
                paragraph="We need to predict customer churn...",
                use_case_title="Customer Churn Prediction"
            )
            facts = await agent.run(input_data)
            ```
        """
        with tracer.start_as_current_span("requirement_analyzer.run") as span:
            # Set input attributes
            span.set_attribute("input.use_case_title", input_data.use_case_title)
            span.set_attribute("input.paragraph_length", len(input_data.paragraph))
            span.set_attribute(
                "input.transcript_length",
                len(input_data.transcript) if input_data.transcript else 0,
            )

            # Prepare prompt for the agent
            prompt_parts = [
                f"Use Case Title: {input_data.use_case_title}",
                f"\nUser Description:\n{input_data.paragraph}",
            ]
            if input_data.transcript:
                prompt_parts.append(f"\nCall Transcript:\n{input_data.transcript}")

            prompt = "\n".join(prompt_parts)

            # Create nested span for LLM call
            with tracer.start_as_current_span(
                "requirement_analyzer.llm_call"
            ) as llm_span:
                try:
                    # Run the agent
                    result = await self.agent.run(prompt)
                    extracted_facts = result.data

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

            # Set output attributes
            span.set_attribute(
                "output.technical_confidence_score",
                extracted_facts.technical_confidence_score,
            )
            span.set_attribute(
                "output.requirements_count",
                len(extracted_facts.key_extracted_requirements),
            )
            span.set_attribute(
                "output.gaps_count", len(extracted_facts.identified_gaps)
            )
            span.set_attribute(
                "output.domain_keywords", str(extracted_facts.domain_keywords)
            )

            # Add event when extraction completes
            span.add_event(
                "requirement_extraction_completed",
                {
                    "confidence_score": extracted_facts.technical_confidence_score,
                    "requirements_count": len(
                        extracted_facts.key_extracted_requirements
                    ),
                    "gaps_count": len(extracted_facts.identified_gaps),
                },
            )

            return extracted_facts

    async def run_from_json(
        self, input_json: str | dict[str, Any]
    ) -> FactExtractionModel:
        """
        Run the agent from JSON input.

        Args:
            input_json: JSON string or dict containing UseCaseInput data.

        Returns:
            FactExtractionModel with extracted facts.
        """
        if isinstance(input_json, str):
            input_data = UseCaseInput.model_validate_json(input_json)
        else:
            input_data = UseCaseInput.model_validate(input_json)
        return await self.run(input_data)


# For backward compatibility with DataRobot template
MyAgent = RequirementAnalyzerAgent
