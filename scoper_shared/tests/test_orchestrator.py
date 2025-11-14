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
Unit tests for the orchestrator state machine.

Tests validate state transitions, error handling, and workflow execution.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from scoper_shared.orchestrator import (
    Orchestrator,
    OrchestratorError,
    OrchestratorState,
    WorkflowState,
)
from scoper_shared.schemas import (
    ArchitecturePlan,
    ArchitectureStep,
    FactExtractionModel,
    QuestionnaireDraft,
    QuestionnaireFinal,
    Question,
    UseCaseInput,
)


@pytest.fixture
def sample_use_case_input() -> UseCaseInput:
    """Create a sample UseCaseInput for testing."""
    return UseCaseInput(
        paragraph="We need to predict customer churn using historical data",
        use_case_title="Customer Churn Prediction",
    )


@pytest.fixture
def sample_fact_extraction() -> FactExtractionModel:
    """Create a sample FactExtractionModel for testing."""
    return FactExtractionModel(
        use_case_title="Customer Churn Prediction",
        technical_confidence_score=0.85,
        key_extracted_requirements=["Predict churn", "Use historical data"],
        domain_keywords=["classic_ml"],
        identified_gaps=["Data source details"],
    )


@pytest.fixture
def sample_questionnaire_draft() -> QuestionnaireDraft:
    """Create a sample QuestionnaireDraft for testing."""
    return QuestionnaireDraft(
        questions=[
            Question(
                id="q1",
                text="What is the primary data source?",
                type="single_select",
                options=["Database", "API"],
                required=True,
                rationale="Need to understand data source",
                tracks=["classic_ml"],
            )
        ],
        selected_from_master_ids=["q1"],
        delta_questions=[],
        coverage_estimate=0.75,
    )


@pytest.fixture
def sample_questionnaire_final() -> QuestionnaireFinal:
    """Create a sample QuestionnaireFinal for testing."""
    return QuestionnaireFinal(
        qas=[{"id": "q1", "answer": "Database"}],
        answered_pct=0.9,
        gaps=[],
    )


@pytest.fixture
def sample_architecture_plan() -> ArchitecturePlan:
    """Create a sample ArchitecturePlan for testing."""
    return ArchitecturePlan(
        steps=[
            ArchitectureStep(
                id="step1",
                name="Data Ingestion",
                purpose="Load customer data",
                inputs="Raw customer data",
                outputs="Cleansed data frame",
            )
        ]
        * 12,  # Ensure 12 steps (within 10-16 range)
        assumptions=["Data is available"],
        risks=["Data quality issues"],
        notes="Test architecture plan",
    )


@pytest.fixture
def orchestrator() -> Orchestrator:
    """Create an orchestrator instance for testing."""
    return Orchestrator(max_retries=1, retry_delay=0.1)


class TestOrchestratorState:
    """Test OrchestratorState class."""

    def test_initial_state(self) -> None:
        """Test that initial state is correctly set."""
        state = OrchestratorState()
        assert state.current_state == WorkflowState.INGEST
        assert state.use_case_input is None
        assert state.fact_extraction is None
        assert state.selected_tracks == []
        assert state.clarification_answers == []


class TestOrchestratorInitialization:
    """Test Orchestrator initialization."""

    def test_init_defaults(self) -> None:
        """Test orchestrator initialization with default parameters."""
        orch = Orchestrator()
        assert orch.max_retries == 3
        assert orch.retry_delay == 1.0
        assert orch.state.current_state == WorkflowState.INGEST

    def test_init_custom_params(self) -> None:
        """Test orchestrator initialization with custom parameters."""
        orch = Orchestrator(max_retries=5, retry_delay=2.0)
        assert orch.max_retries == 5
        assert orch.retry_delay == 2.0


class TestOrchestratorIngest:
    """Test INGEST state handling."""

    @pytest.mark.asyncio
    async def test_start_validates_input(
        self, orchestrator: Orchestrator, sample_use_case_input: UseCaseInput
    ) -> None:
        """Test that start() validates UseCaseInput."""
        await orchestrator.start(sample_use_case_input)
        assert orchestrator.state.current_state == WorkflowState.INGEST
        assert orchestrator.state.use_case_input == sample_use_case_input

    @pytest.mark.asyncio
    async def test_start_invalid_input(self, orchestrator: Orchestrator) -> None:
        """Test that start() raises error for invalid input."""
        invalid_input = {"invalid": "data"}  # type: ignore
        with pytest.raises(OrchestratorError):
            await orchestrator.start(invalid_input)  # type: ignore

    @pytest.mark.asyncio
    async def test_get_current_state(self, orchestrator: Orchestrator) -> None:
        """Test get_current_state() method."""
        assert orchestrator.get_current_state() == WorkflowState.INGEST


class TestOrchestratorWorkflow:
    """Test full workflow execution."""

    @pytest.mark.asyncio
    @patch("requirement_analyzer_agent.custom_model.agent.RequirementAnalyzerAgent")
    @patch("scoper_shared.orchestrator.domain_router")
    @patch("scoper_shared.utils.kb_retriever.KBRetriever")
    @patch("questionnaire_agent.custom_model.agent.QuestionnaireAgent")
    @patch("architecture_agent.custom_model.agent.ArchitectureAgent")
    async def test_run_until_clarification(
        self,
        mock_arch_agent: MagicMock,
        mock_q_agent: MagicMock,
        mock_kb: MagicMock,
        mock_router: MagicMock,
        mock_req_agent: MagicMock,
        orchestrator: Orchestrator,
        sample_use_case_input: UseCaseInput,
        sample_fact_extraction: FactExtractionModel,
        sample_questionnaire_draft: QuestionnaireDraft,
    ) -> None:
        """Test workflow execution until Q_CLARIFY state."""
        # Setup mocks
        mock_req_agent_instance = AsyncMock()
        mock_req_agent_instance.run = AsyncMock(return_value=sample_fact_extraction)
        mock_req_agent.return_value = mock_req_agent_instance

        mock_router.return_value = ["classic_ml"]

        mock_kb_instance = MagicMock()
        mock_kb_instance.get_master_questionnaire.return_value = []
        mock_kb_instance.get_platform_guides.return_value = {}
        mock_kb.return_value = mock_kb_instance

        mock_q_agent_instance = AsyncMock()
        mock_q_agent_instance.run = AsyncMock(return_value=sample_questionnaire_draft)
        mock_q_agent.return_value = mock_q_agent_instance

        # Run workflow
        await orchestrator.start(sample_use_case_input)
        await orchestrator.run_until_clarification()

        # Verify state
        assert orchestrator.state.current_state == WorkflowState.Q_CLARIFY
        assert orchestrator.state.fact_extraction == sample_fact_extraction
        assert orchestrator.state.selected_tracks == ["classic_ml"]
        assert orchestrator.state.questionnaire_draft == sample_questionnaire_draft

    @pytest.mark.asyncio
    @patch("clarifier_agent.custom_model.agent.ClarifierAgent")
    async def test_clarification_loop(
        self,
        mock_clarifier: MagicMock,
        orchestrator: Orchestrator,
        sample_questionnaire_draft: QuestionnaireDraft,
        sample_questionnaire_final: QuestionnaireFinal,
    ) -> None:
        """Test clarification loop handling."""
        # Setup state
        orchestrator.state.current_state = WorkflowState.Q_CLARIFY
        orchestrator.state.questionnaire_draft = sample_questionnaire_draft

        # Setup mock
        mock_clarifier_instance = AsyncMock()
        mock_clarifier_instance.ask_question = AsyncMock(
            return_value=(sample_questionnaire_draft.questions[0], "")
        )
        mock_clarifier_instance.finalize = AsyncMock(return_value=sample_questionnaire_final)
        mock_clarifier.return_value = mock_clarifier_instance

        # Test asking question
        question, status = await orchestrator.ask_next_question()
        assert question is not None
        assert orchestrator.state.clarification_question_num == 1

        # Test submitting answer
        await orchestrator.submit_clarification_answer("q1", "Database")
        assert len(orchestrator.state.clarification_answers) == 1

        # Test finalizing
        await orchestrator.finalize_clarification()
        assert orchestrator.state.current_state == WorkflowState.Q_FREEZE
        assert orchestrator.state.questionnaire_final == sample_questionnaire_final

    @pytest.mark.asyncio
    @patch("architecture_agent.custom_model.agent.ArchitectureAgent")
    async def test_q_freeze_gate_passes(
        self,
        mock_arch_agent: MagicMock,
        orchestrator: Orchestrator,
        sample_questionnaire_final: QuestionnaireFinal,
        sample_questionnaire_draft: QuestionnaireDraft,
        sample_architecture_plan: ArchitecturePlan,
    ) -> None:
        """Test Q_FREEZE gate when conditions are met."""
        # Setup state
        orchestrator.state.current_state = WorkflowState.Q_FREEZE
        orchestrator.state.questionnaire_final = sample_questionnaire_final
        orchestrator.state.questionnaire_draft = sample_questionnaire_draft

        # Setup mock
        mock_arch_agent_instance = AsyncMock()
        mock_arch_agent_instance.run = AsyncMock(
            return_value=(sample_architecture_plan, "# Architecture Plan\nTest")
        )
        mock_arch_agent.return_value = mock_arch_agent_instance

        # Test gate evaluation
        can_proceed = await orchestrator._handle_q_freeze()
        assert can_proceed is True  # answered_pct = 0.9 >= 0.8

        # Test running to completion
        await orchestrator.run_to_completion()
        assert orchestrator.state.current_state == WorkflowState.DONE

    @pytest.mark.asyncio
    async def test_q_freeze_gate_fails(
        self, orchestrator: Orchestrator, sample_questionnaire_draft: QuestionnaireDraft
    ) -> None:
        """Test Q_FREEZE gate when conditions are not met."""
        # Setup state with low answered_pct
        orchestrator.state.current_state = WorkflowState.Q_FREEZE
        orchestrator.state.questionnaire_final = QuestionnaireFinal(
            qas=[], answered_pct=0.5, gaps=["q1"]
        )
        orchestrator.state.questionnaire_draft = sample_questionnaire_draft

        # Test gate evaluation
        can_proceed = await orchestrator._handle_q_freeze()
        assert can_proceed is False  # answered_pct = 0.5 < 0.8 and coverage = 0.75 < 0.8

    @pytest.mark.asyncio
    async def test_get_results_success(
        self,
        orchestrator: Orchestrator,
        sample_questionnaire_final: QuestionnaireFinal,
        sample_architecture_plan: ArchitecturePlan,
    ) -> None:
        """Test getting results when workflow is complete."""
        # Setup state
        orchestrator.state.current_state = WorkflowState.DONE
        orchestrator.state.questionnaire_final = sample_questionnaire_final
        orchestrator.state.architecture_plan = sample_architecture_plan
        orchestrator.state.architecture_markdown = "# Architecture Plan\nTest"

        # Get results
        results = orchestrator.get_results()
        assert "questionnaire_final" in results
        assert "architecture_plan" in results
        assert "architecture_markdown" in results
        assert results["questionnaire_final"] == sample_questionnaire_final
        assert results["architecture_plan"] == sample_architecture_plan

    @pytest.mark.asyncio
    async def test_get_results_not_done(self, orchestrator: Orchestrator) -> None:
        """Test that get_results() raises error when not in DONE state."""
        orchestrator.state.current_state = WorkflowState.Q_CLARIFY
        with pytest.raises(OrchestratorError):
            orchestrator.get_results()


class TestOrchestratorErrorHandling:
    """Test error handling in orchestrator."""

    @pytest.mark.asyncio
    @patch("requirement_analyzer_agent.custom_model.agent.RequirementAnalyzerAgent")
    async def test_analyze_state_error(
        self,
        mock_req_agent: MagicMock,
        orchestrator: Orchestrator,
        sample_use_case_input: UseCaseInput,
    ) -> None:
        """Test error handling in ANALYZE state."""
        await orchestrator.start(sample_use_case_input)

        # Setup mock to raise error
        mock_req_agent_instance = AsyncMock()
        mock_req_agent_instance.run = AsyncMock(side_effect=Exception("Agent error"))
        mock_req_agent.return_value = mock_req_agent_instance

        # Test that error is raised
        with pytest.raises(OrchestratorError):
            await orchestrator.run_until_clarification()

    @pytest.mark.asyncio
    async def test_ask_question_wrong_state(self, orchestrator: Orchestrator) -> None:
        """Test that ask_question() raises error in wrong state."""
        orchestrator.state.current_state = WorkflowState.ANALYZE
        with pytest.raises(OrchestratorError):
            await orchestrator.ask_next_question()

    @pytest.mark.asyncio
    async def test_submit_answer_wrong_state(self, orchestrator: Orchestrator) -> None:
        """Test that submit_clarification_answer() raises error in wrong state."""
        orchestrator.state.current_state = WorkflowState.ANALYZE
        with pytest.raises(OrchestratorError):
            await orchestrator.submit_clarification_answer("q1", "answer")

