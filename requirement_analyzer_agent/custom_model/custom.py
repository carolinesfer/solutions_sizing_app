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
# ------------------------------------------------------------------------------
# THIS SECTION OF CODE IS REQUIRED TO SETUP TRACING AND TELEMETRY FOR THE AGENTS.
# REMOVING THIS CODE WILL DISABLE ALL MONITORING, TRACING AND TELEMETRY.
# isort: off
import logging

# Suppress the "Attempting to instrument while already instrumented" warning
logging.getLogger("opentelemetry.instrumentation.instrumentor").setLevel(logging.ERROR)

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

instrument_requests = RequestsInstrumentor().instrument()
instrument_aiohttp = AioHttpClientInstrumentor().instrument()
instrument_httpx = HTTPXClientInstrumentor().instrument()
instrument_openai = OpenAIInstrumentor().instrument()

import os

# Some libraries collect telemetry data by default. Let's disable that.
os.environ["RAGAS_DO_NOT_TRACK"] = "true"
os.environ["DEEPEVAL_TELEMETRY_OPT_OUT"] = "YES"
# isort: on
# ------------------------------------------------------------------------------

from typing import Any, Iterator, Union

from datarobot_drum import RuntimeParameters
from datarobot_genai.core.chat import (
    CustomModelChatResponse,
    CustomModelStreamingResponse,
    initialize_authorization_context,
    to_custom_model_chat_response,
)
from openai.types.chat import CompletionCreateParams
from openai.types.chat.completion_create_params import (
    CompletionCreateParamsNonStreaming,
    CompletionCreateParamsStreaming,
)

# ruff: noqa: E402
from agent import RequirementAnalyzerAgent
from scoper_shared.schemas import UseCaseInput


def maybe_set_env_from_runtime_parameters(key: str) -> None:
    """
    Set an environment variable from a runtime parameter if it exists.

    In local development, the runtime parameters are not available, and environment variable
    is set from the .env file, so it's safe to ignore the exception.
    """
    RUNTIME_PARAMETER_PLACEHOLDER_VALUE = "SET_VIA_PULUMI_OR_MANUALLY"
    try:
        runtime_parameter_value = RuntimeParameters.get(key)
        if (
            runtime_parameter_value
            and len(runtime_parameter_value) > 0
            and runtime_parameter_value != RUNTIME_PARAMETER_PLACEHOLDER_VALUE
        ):
            os.environ[key] = runtime_parameter_value
    except ValueError:
        pass


def load_model(code_dir: str) -> tuple[ThreadPoolExecutor, asyncio.AbstractEventLoop]:
    """The agent is instantiated in this function and returned."""
    thread_pool_executor = ThreadPoolExecutor(1)
    event_loop = asyncio.new_event_loop()
    thread_pool_executor.submit(asyncio.set_event_loop, event_loop).result()
    return (thread_pool_executor, event_loop)


def _extract_user_prompt_from_messages(
    messages: list[dict[str, Any]] | None,
) -> str:
    """
    Extract user prompt from OpenAI messages format.

    Args:
        messages: List of message dicts with 'role' and 'content' keys.

    Returns:
        User prompt string, or empty string if not found.
    """
    if not messages:
        return ""

    # Find the last user message
    for message in reversed(messages):
        if message.get("role") == "user":
            content = message.get("content", "")
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                # Handle multimodal content
                text_parts = [
                    item.get("text", "") for item in content if item.get("type") == "text"
                ]
                return " ".join(text_parts)

    return ""


def chat(
    completion_create_params: CompletionCreateParams
    | CompletionCreateParamsNonStreaming
    | CompletionCreateParamsStreaming,
    load_model_result: tuple[ThreadPoolExecutor, asyncio.AbstractEventLoop],
    **kwargs: Any,
) -> Union[CustomModelChatResponse, Iterator[CustomModelStreamingResponse]]:
    """When using the chat endpoint, this function is called.

    Agent inputs are in OpenAI message format and defined as the 'user' portion
    of the input prompt. The user message should contain a JSON string with
    UseCaseInput data.

    Example:
        client = OpenAI(...)
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": '{"paragraph": "We need to predict churn...", "use_case_title": "Churn Prediction"}'},
            ],
            ...
        )
    """
    thread_pool_executor, event_loop = load_model_result

    # Change working directory to the directory containing this file.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Load MCP runtime parameters and session secret if configured
    maybe_set_env_from_runtime_parameters("EXTERNAL_MCP_URL")
    maybe_set_env_from_runtime_parameters("MCP_DEPLOYMENT_ID")
    maybe_set_env_from_runtime_parameters("SESSION_SECRET_KEY")

    # Initialize the authorization context
    initialize_authorization_context(completion_create_params)

    # Extract user prompt from messages
    messages = completion_create_params.get("messages", [])
    user_prompt = _extract_user_prompt_from_messages(messages)

    if not user_prompt:
        raise ValueError("No user message found in completion_create_params")

    # Parse user prompt as UseCaseInput JSON
    try:
        if user_prompt.strip().startswith("{"):
            input_data = UseCaseInput.model_validate_json(user_prompt)
        else:
            # If not JSON, treat as paragraph and create UseCaseInput
            input_data = UseCaseInput(
                paragraph=user_prompt,
                use_case_title="Untitled Use Case",
                transcript=None,
            )
    except Exception as e:
        # Fallback: create UseCaseInput from plain text
        input_data = UseCaseInput(
            paragraph=user_prompt,
            use_case_title="Untitled Use Case",
            transcript=None,
        )

    # Get model name from params or use default
    model_name = completion_create_params.get("model")

    # Instantiate the agent
    agent = RequirementAnalyzerAgent(model_name=model_name)

    # Run the agent
    def run_agent() -> tuple[str, list, dict[str, int]]:
        """Run agent in event loop and return formatted result."""
        result = event_loop.run_until_complete(agent.run(input_data))

        # Convert FactExtractionModel to JSON string for response
        response_text = result.model_dump_json(indent=2)

        # Extract usage metrics if available (pydantic-ai doesn't provide this directly)
        usage_metrics = {
            "completion_tokens": 0,
            "prompt_tokens": 0,
            "total_tokens": 0,
        }

        # Return in format expected by DataRobot
        return (response_text, [], usage_metrics)

    result = thread_pool_executor.submit(run_agent).result()
    response_text, pipeline_interactions, usage_metrics = result

    # Return non-streaming response
    return to_custom_model_chat_response(
        response_text,
        pipeline_interactions,
        usage_metrics,
        model=completion_create_params.get("model"),
    )
