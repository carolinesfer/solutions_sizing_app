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
Unit tests for Questionnaire Agent.

Tests validate agent functionality, KB integration, and output schemas.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from scoper_shared.schemas import FactExtractionModel, QuestionnaireDraft

# Import after setting up path
import sys
from pathlib import Path

custom_model_path = Path(__file__).parent.parent / "custom_model"
sys.path.insert(0, str(custom_model_path))

from agent import QuestionnaireAgent


class TestQuestionnaireAgent:
    """Test cases for QuestionnaireAgent."""

    @pytest.fixture
    def sample_facts(self) -> FactExtractionModel:
        """Create sample FactExtractionModel for testing."""
        return FactExtractionModel(
            use_case_title="Customer Churn Prediction",
            technical_confidence_score=0.85,
            key_extracted_requirements=["Predict churn", "Use historical data"],
            domain_keywords=["classic_ml"],
            identified_gaps=["Data source location"],
        )

    @pytest.fixture
    def sample_draft(self) -> QuestionnaireDraft:
        """Create sample QuestionnaireDraft for testing."""
        from scoper_shared.schemas import Question

        question1 = Question(
            id="q1", text="What is your data source?", type="single_select", required=True
        )
        question2 = Question(
            id="q2", text="What is the target variable?", type="free_text", required=True
        )

        return QuestionnaireDraft(
            questions=[question1, question2],
            selected_from_master_ids=["q1", "q2"],
            delta_questions=[],
            coverage_estimate=0.75,
        )

    @pytest.mark.asyncio
    async def test_run_with_valid_facts(self, sample_facts: FactExtractionModel) -> None:
        """Test that agent.run() processes valid FactExtractionModel."""
        agent = QuestionnaireAgent()

        # Mock the agent's run method to return structured output
        with patch.object(agent.agent, "run") as mock_run:
            mock_result = MagicMock()
            mock_result.data = QuestionnaireDraft(
                questions=[],
                selected_from_master_ids=[],
                delta_questions=[],
                coverage_estimate=0.8,
            )
            mock_result.usage = None
            mock_run.return_value = mock_result

            # Mock KB retriever
            with patch.object(agent.kb_retriever, "get_master_questionnaire") as mock_kb:
                mock_kb.return_value = []

                result = await agent.run(sample_facts)

                assert isinstance(result, QuestionnaireDraft)
                assert 0.0 <= result.coverage_estimate <= 1.0

    @pytest.mark.asyncio
    async def test_run_from_json(self) -> None:
        """Test that agent.run_from_json() processes JSON input."""
        agent = QuestionnaireAgent()

        input_json = {
            "use_case_title": "Sales Forecast",
            "technical_confidence_score": 0.8,
            "key_extracted_requirements": ["Forecast sales"],
            "domain_keywords": ["time_series"],
            "identified_gaps": [],
        }

        with patch.object(agent, "run") as mock_run:
            mock_result = QuestionnaireDraft(
                questions=[],
                selected_from_master_ids=[],
                delta_questions=[],
                coverage_estimate=0.8,
            )
            mock_run.return_value = mock_result

            result = await agent.run_from_json(input_json)

            assert isinstance(result, QuestionnaireDraft)

    def test_agent_initialization(self) -> None:
        """Test that agent initializes correctly."""
        agent = QuestionnaireAgent()
        assert agent.agent is not None
        assert agent.model_name is not None
        assert agent.kb_retriever is not None

