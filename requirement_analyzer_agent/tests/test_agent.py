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
Unit tests for Requirement Analyzer Agent.

Tests validate agent functionality, input/output schemas, and error handling.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from scoper_shared.schemas import FactExtractionModel, UseCaseInput

# Import after setting up path
import sys
from pathlib import Path

custom_model_path = Path(__file__).parent.parent / "custom_model"
sys.path.insert(0, str(custom_model_path))

from agent import RequirementAnalyzerAgent


class TestRequirementAnalyzerAgent:
    """Test cases for RequirementAnalyzerAgent."""

    @pytest.fixture
    def sample_input(self) -> UseCaseInput:
        """Create sample UseCaseInput for testing."""
        return UseCaseInput(
            paragraph="We need to predict customer churn using historical transaction data and customer demographics.",
            use_case_title="Customer Churn Prediction",
            transcript="Call transcript discussing churn prediction requirements...",
        )

    @pytest.fixture
    def sample_output(self) -> FactExtractionModel:
        """Create sample FactExtractionModel for testing."""
        return FactExtractionModel(
            use_case_title="Customer Churn Prediction",
            technical_confidence_score=0.85,
            key_extracted_requirements=[
                "Predict customer churn",
                "Use historical transaction data",
                "Use customer demographics",
            ],
            domain_keywords=["classic_ml", "binary_classification"],
            identified_gaps=["Data source location", "Deployment environment"],
        )

    @pytest.mark.asyncio
    async def test_run_with_valid_input(self, sample_input: UseCaseInput) -> None:
        """Test that agent.run() processes valid input."""
        agent = RequirementAnalyzerAgent()

        # Mock the agent's run method to return structured output
        with patch.object(agent.agent, "run") as mock_run:
            mock_result = MagicMock()
            mock_result.data = FactExtractionModel(
                use_case_title=sample_input.use_case_title,
                technical_confidence_score=0.85,
                key_extracted_requirements=["Predict churn"],
                domain_keywords=["classic_ml"],
                identified_gaps=["Data source"],
            )
            mock_result.usage = None
            mock_run.return_value = mock_result

            result = await agent.run(sample_input)

            assert isinstance(result, FactExtractionModel)
            assert result.use_case_title == sample_input.use_case_title
            assert 0.0 <= result.technical_confidence_score <= 1.0

    @pytest.mark.asyncio
    async def test_run_from_json(self) -> None:
        """Test that agent.run_from_json() processes JSON input."""
        agent = RequirementAnalyzerAgent()

        input_json = {
            "paragraph": "We need to forecast sales",
            "use_case_title": "Sales Forecast",
            "transcript": None,
        }

        with patch.object(agent, "run") as mock_run:
            mock_result = FactExtractionModel(
                use_case_title="Sales Forecast",
                technical_confidence_score=0.8,
                key_extracted_requirements=["Forecast sales"],
                domain_keywords=["time_series"],
                identified_gaps=[],
            )
            mock_run.return_value = mock_result

            result = await agent.run_from_json(input_json)

            assert isinstance(result, FactExtractionModel)
            assert result.use_case_title == "Sales Forecast"

    def test_agent_initialization(self) -> None:
        """Test that agent initializes correctly."""
        agent = RequirementAnalyzerAgent()
        assert agent.agent is not None
        assert agent.model_name is not None

    def test_agent_initialization_with_custom_model(self) -> None:
        """Test that agent initializes with custom model name."""
        agent = RequirementAnalyzerAgent(model_name="gpt-4")
        assert agent.model_name == "gpt-4"

