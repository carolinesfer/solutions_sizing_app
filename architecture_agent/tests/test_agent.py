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
Unit tests for Architecture Agent.

Tests validate agent functionality, RAG integration, and output schemas.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from scoper_shared.schemas import ArchitecturePlan, ArchitectureStep, QuestionnaireFinal

# Import after setting up path
import sys
from pathlib import Path

custom_model_path = Path(__file__).parent.parent / "custom_model"
sys.path.insert(0, str(custom_model_path))

from agent import ArchitectureAgent


class TestArchitectureAgent:
    """Test cases for ArchitectureAgent."""

    @pytest.fixture
    def sample_questionnaire(self) -> QuestionnaireFinal:
        """Create sample QuestionnaireFinal for testing."""
        return QuestionnaireFinal(
            qas=[
                {"id": "q1", "answer": "Database"},
                {"id": "q2", "answer": "Customer churn"},
            ],
            answered_pct=0.90,
            gaps=["q3"],
        )

    @pytest.fixture
    def sample_plan(self) -> ArchitecturePlan:
        """Create sample ArchitecturePlan for testing."""
        steps = [
            ArchitectureStep(
                id=i,
                name=f"Step {i}",
                purpose=f"Purpose {i}",
                inputs=[f"Input {i}"],
                outputs=[f"Output {i}"],
            )
            for i in range(1, 12)
        ]

        return ArchitecturePlan(
            steps=steps,
            assumptions=["Assumption 1", "Assumption 2"],
            risks=["Risk 1"],
            notes="Test notes",
        )

    @pytest.mark.asyncio
    async def test_run_with_valid_questionnaire(
        self, sample_questionnaire: QuestionnaireFinal
    ) -> None:
        """Test that agent.run() processes valid QuestionnaireFinal."""
        agent = ArchitectureAgent()

        # Mock the agent's run method to return structured output
        with patch.object(agent.agent, "run") as mock_run:
            mock_result = MagicMock()
            mock_result.data = ArchitecturePlan(
                steps=[
                    ArchitectureStep(
                        id=i,
                        name=f"Step {i}",
                        purpose=f"Purpose {i}",
                        inputs=[],
                        outputs=[],
                    )
                    for i in range(1, 11)
                ],
                assumptions=[],
                risks=[],
            )
            mock_result.usage = None
            mock_run.return_value = mock_result

            # Mock KB retriever
            with patch.object(agent.kb_retriever, "get_platform_guides") as mock_kb:
                mock_kb.return_value = {}

                plan, markdown = await agent.run(sample_questionnaire)

                assert isinstance(plan, ArchitecturePlan)
                assert 10 <= len(plan.steps) <= 16
                assert isinstance(markdown, str)
                assert len(markdown) > 0

    @pytest.mark.asyncio
    async def test_run_from_json(self) -> None:
        """Test that agent.run_from_json() processes JSON input."""
        agent = ArchitectureAgent()

        input_json = {
            "qas": [{"id": "q1", "answer": "value"}],
            "answered_pct": 1.0,
            "gaps": [],
        }

        with patch.object(agent, "run") as mock_run:
            mock_plan = ArchitecturePlan(
                steps=[
                    ArchitectureStep(
                        id=i, name=f"Step {i}", purpose=f"Purpose {i}", inputs=[], outputs=[]
                    )
                    for i in range(1, 11)
                ],
                assumptions=[],
                risks=[],
            )
            mock_run.return_value = (mock_plan, "# Test Markdown")

            plan, markdown = await agent.run_from_json(input_json)

            assert isinstance(plan, ArchitecturePlan)
            assert isinstance(markdown, str)

    def test_plan_to_markdown(self, sample_plan: ArchitecturePlan) -> None:
        """Test that _plan_to_markdown() generates valid markdown."""
        agent = ArchitectureAgent()

        markdown = agent._plan_to_markdown(sample_plan)

        assert isinstance(markdown, str)
        assert "# Solution Architecture Plan" in markdown
        assert "## Implementation Steps" in markdown
        assert "## Assumptions" in markdown
        assert "## Risks" in markdown

    def test_agent_initialization(self) -> None:
        """Test that agent initializes correctly."""
        agent = ArchitectureAgent()
        assert agent.agent is not None
        assert agent.model_name is not None
        assert agent.kb_retriever is not None

