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
Unit tests for Clarifier Agent.

Tests validate agent functionality, question asking, and finalization.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from scoper_shared.schemas import QuestionnaireDraft, QuestionnaireFinal, Question

# Import after setting up path
import sys
from pathlib import Path

custom_model_path = Path(__file__).parent.parent / "custom_model"
sys.path.insert(0, str(custom_model_path))

from agent import ClarifierAgent


class TestClarifierAgent:
    """Test cases for ClarifierAgent."""

    @pytest.fixture
    def sample_draft(self) -> QuestionnaireDraft:
        """Create sample QuestionnaireDraft for testing."""
        question1 = Question(
            id="q1",
            text="What is your data source?",
            type="single_select",
            options=["Database", "API"],
            required=True,
        )
        question2 = Question(
            id="q2", text="Is this urgent?", type="bool", required=True
        )

        return QuestionnaireDraft(
            questions=[question1, question2],
            selected_from_master_ids=["q1", "q2"],
            delta_questions=[],
            coverage_estimate=0.75,
        )

    @pytest.mark.asyncio
    async def test_ask_question(self, sample_draft: QuestionnaireDraft) -> None:
        """Test that ask_question() returns a question and answer."""
        agent = ClarifierAgent(max_questions=5)

        question, answer = await agent.ask_question(sample_draft, [], 1)

        assert question is not None
        assert isinstance(question, Question)
        assert question.id in ["q1", "q2"]

    @pytest.mark.asyncio
    async def test_ask_question_prefers_single_select_bool(
        self, sample_draft: QuestionnaireDraft
    ) -> None:
        """Test that ask_question prefers single-select or boolean questions."""
        agent = ClarifierAgent(max_questions=5)

        question, _ = await agent.ask_question(sample_draft, [], 1)

        assert question is not None
        assert question.type in ["single_select", "bool"]

    @pytest.mark.asyncio
    async def test_ask_question_returns_none_when_no_more_questions(
        self, sample_draft: QuestionnaireDraft
    ) -> None:
        """Test that ask_question returns None when no more questions."""
        agent = ClarifierAgent(max_questions=5)

        # Answer all questions
        current_answers = [{"id": "q1", "answer": "Database"}, {"id": "q2", "answer": "Yes"}]

        question, answer = await agent.ask_question(sample_draft, current_answers, 1)

        assert question is None

    @pytest.mark.asyncio
    async def test_finalize(self, sample_draft: QuestionnaireDraft) -> None:
        """Test that finalize() compiles Q&A pairs correctly."""
        agent = ClarifierAgent()

        all_answers = [{"id": "q1", "answer": "Database"}, {"id": "q2", "answer": "Yes"}]

        result = await agent.finalize(sample_draft, all_answers)

        assert isinstance(result, QuestionnaireFinal)
        assert len(result.qas) == 2
        assert result.answered_pct == 1.0
        assert result.gaps == []

    @pytest.mark.asyncio
    async def test_finalize_with_gaps(self, sample_draft: QuestionnaireDraft) -> None:
        """Test that finalize() correctly identifies gaps."""
        agent = ClarifierAgent()

        all_answers = [{"id": "q1", "answer": "Database"}]

        result = await agent.finalize(sample_draft, all_answers)

        assert isinstance(result, QuestionnaireFinal)
        assert result.answered_pct == 0.5
        assert "q2" in result.gaps

    @pytest.mark.asyncio
    async def test_run_full_loop(self, sample_draft: QuestionnaireDraft) -> None:
        """Test that run() executes full clarification loop."""
        agent = ClarifierAgent(max_questions=2)

        result = await agent.run(sample_draft)

        assert isinstance(result, QuestionnaireFinal)
        assert 0.0 <= result.answered_pct <= 1.0

    def test_agent_initialization(self) -> None:
        """Test that agent initializes correctly."""
        agent = ClarifierAgent()
        assert agent.agent is not None
        assert agent.model_name is not None
        assert agent.max_questions == 5

    def test_agent_initialization_with_custom_max_questions(self) -> None:
        """Test that agent initializes with custom max_questions."""
        agent = ClarifierAgent(max_questions=10)
        assert agent.max_questions == 10

