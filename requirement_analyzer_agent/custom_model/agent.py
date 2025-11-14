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

import json
from typing import Any

from opentelemetry import trace
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from config import Config
from scoper_shared.schemas import FactExtractionModel, UseCaseInput

config = Config()
tracer = trace.get_tracer(__name__)

# System prompt for Requirement Analyzer Agent
SYSTEM_PROMPT = """You are a senior solutions architect. Your sole task is to read the following user query and transcript and extract key information. Identify the core goal, all technical requirements, any mentioned data sources, and any clear informational gaps. You must output *only* the Pydantic FactExtractionModel JSON. Do not add conversational text. Pay special attention to keywords that suggest the project domain (e.g., 'forecast', 'time series', 'NLP', 'images', 'agentic')."""

# Create the agent with structured output
requirement_analyzer_agent = Agent(
    model=OpenAIModel("gpt-4o-mini"),
    system_prompt=SYSTEM_PROMPT,
    result_type=FactExtractionModel,
)


class RequirementAnalyzerAgent:
    """
    Requirement Analyzer Agent (Agent 1).

    This agent extracts facts, requirements, and identifies gaps from raw user input.
    It uses pydantic-ai to ensure structured output conforming to FactExtractionModel.
    """

    def __init__(self, model_name: str | None = None, api_key: str | None = None) -> None:
        """
        Initialize the Requirement Analyzer Agent.

        Args:
            model_name: Optional model name to use. If None, uses config default.
            api_key: Optional API key for LLM. If None, uses environment/config.
        """
        self.model_name = model_name or config.llm_default_model
        self.api_key = api_key
        # Update agent model if custom model provided
        if model_name:
            self.agent = Agent(
                model=OpenAIModel(model_name),
                system_prompt=SYSTEM_PROMPT,
                result_type=FactExtractionModel,
            )
        else:
            self.agent = requirement_analyzer_agent

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
                "input.transcript_length", len(input_data.transcript) if input_data.transcript else 0
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
            with tracer.start_as_current_span("requirement_analyzer.llm_call") as llm_span:
                try:
                    # Run the agent
                    result = await self.agent.run(prompt)
                    extracted_facts = result.data

                    # Set LLM call attributes
                    llm_span.set_attribute("model", self.model_name)
                    if result.usage:
                        llm_span.set_attribute("usage.prompt_tokens", result.usage.prompt_tokens or 0)
                        llm_span.set_attribute(
                            "usage.completion_tokens", result.usage.completion_tokens or 0
                        )
                        llm_span.set_attribute("usage.total_tokens", result.usage.total_tokens or 0)

                except Exception as e:
                    llm_span.record_exception(e)
                    raise

            # Set output attributes
            span.set_attribute(
                "output.technical_confidence_score", extracted_facts.technical_confidence_score
            )
            span.set_attribute(
                "output.requirements_count", len(extracted_facts.key_extracted_requirements)
            )
            span.set_attribute("output.gaps_count", len(extracted_facts.identified_gaps))
            span.set_attribute("output.domain_keywords", str(extracted_facts.domain_keywords))

            # Add event when extraction completes
            span.add_event(
                "requirement_extraction_completed",
                {
                    "confidence_score": extracted_facts.technical_confidence_score,
                    "requirements_count": len(extracted_facts.key_extracted_requirements),
                    "gaps_count": len(extracted_facts.identified_gaps),
                },
            )

            return extracted_facts

    async def run_from_json(self, input_json: str | dict[str, Any]) -> FactExtractionModel:
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
