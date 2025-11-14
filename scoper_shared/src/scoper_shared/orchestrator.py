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
State machine orchestrator for the Agentic Professional Services Scoper system.

This module implements the orchestrator that manages the workflow state transitions
and coordinates calls between the four specialized agents.
"""

from enum import Enum
from typing import Any, Optional

from opentelemetry import trace

from scoper_shared.schemas import (
    ArchitecturePlan,
    FactExtractionModel,
    QuestionnaireDraft,
    QuestionnaireFinal,
    UseCaseInput,
)
from scoper_shared.utils import KBRetriever, domain_router

tracer = trace.get_tracer(__name__)


class WorkflowState(str, Enum):
    """Workflow state enumeration."""

    INGEST = "INGEST"
    ANALYZE = "ANALYZE"
    ROUTE = "ROUTE"
    KB_FETCH = "KB_FETCH"
    Q_DRAFT = "Q_DRAFT"
    Q_CLARIFY = "Q_CLARIFY"
    Q_FREEZE = "Q_FREEZE"
    PLAN_ARCH = "PLAN_ARCH"
    DONE = "DONE"


class OrchestratorError(Exception):
    """Base exception for orchestrator errors."""

    pass


class OrchestratorState:
    """
    Internal state container for the orchestrator.

    This class holds all intermediate data structures as the workflow progresses.
    """

    def __init__(self) -> None:
        """Initialize empty orchestrator state."""
        self.current_state: WorkflowState = WorkflowState.INGEST
        self.use_case_input: Optional[UseCaseInput] = None
        self.fact_extraction: Optional[FactExtractionModel] = None
        self.selected_tracks: list[str] = []
        self.master_questions: list[Any] = []
        self.platform_guides: dict[str, str] = {}
        self.questionnaire_draft: Optional[QuestionnaireDraft] = None
        self.questionnaire_final: Optional[QuestionnaireFinal] = None
        self.architecture_plan: Optional[ArchitecturePlan] = None
        self.architecture_markdown: str = ""
        self.clarification_answers: list[dict[str, Any]] = []
        self.clarification_question_num: int = 0
        self.error: Optional[str] = None


class Orchestrator:
    """
    State machine orchestrator for the Agentic Professional Services Scoper workflow.

    This orchestrator manages the sequential execution of the 4-agent pipeline:
    1. Requirement Analyzer Agent
    2. Questionnaire Agent
    3. Clarifier Agent
    4. Architecture Agent

    It also coordinates utility functions (Domain Router, KB Retriever) and
    manages state transitions with gating conditions.

    Attributes:
        state: Internal state container holding all workflow data.
        max_retries: Maximum number of retries for failed state transitions (default: 3).
        retry_delay: Delay in seconds between retries (default: 1.0).

    Example:
        ```python
        orchestrator = Orchestrator()
        
        # Start workflow
        await orchestrator.start(UseCaseInput(
            paragraph="We need to predict customer churn...",
            use_case_title="Customer Churn Prediction"
        ))
        
        # Process through states
        await orchestrator.run_until_clarification()
        
        # Handle clarification loop
        while orchestrator.state.current_state == WorkflowState.Q_CLARIFY:
            question, _ = await orchestrator.ask_next_question()
            if question:
                answer = input(f"{question.text}: ")
                await orchestrator.submit_clarification_answer(question.id, answer)
            else:
                await orchestrator.finalize_clarification()
        
        # Continue to completion
        await orchestrator.run_to_completion()
        
        # Get results
        results = orchestrator.get_results()
        ```
    """

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0) -> None:
        """
        Initialize the orchestrator.

        Args:
            max_retries: Maximum number of retries for failed state transitions.
            retry_delay: Delay in seconds between retries.
        """
        self.state = OrchestratorState()
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def start(self, use_case_input: UseCaseInput) -> None:
        """
        Start the workflow by ingesting and validating the input.

        Args:
            use_case_input: Initial user input containing paragraph, transcript, and title.

        Raises:
            OrchestratorError: If input validation fails.
        """
        with tracer.start_as_current_span("scoper_workflow") as workflow_span:
            workflow_span.set_attribute("workflow.start", True)
            try:
                await self._handle_ingest(use_case_input)
            except Exception as e:
                workflow_span.record_exception(e)
                workflow_span.set_attribute("workflow.error", str(e))
                raise OrchestratorError(f"Failed to start workflow: {e}") from e

    async def run_until_clarification(self) -> None:
        """
        Run the workflow from current state until Q_CLARIFY state.

        This method processes all states up to and including Q_DRAFT,
        then transitions to Q_CLARIFY where user interaction is required.
        """
        with tracer.start_as_current_span("scoper_workflow.run_until_clarification") as span:
            try:
                # Process states sequentially until Q_CLARIFY
                while self.state.current_state != WorkflowState.Q_CLARIFY:
                    if self.state.current_state == WorkflowState.INGEST:
                        # Already handled in start()
                        await self._transition_to(WorkflowState.ANALYZE)
                    elif self.state.current_state == WorkflowState.ANALYZE:
                        await self._handle_analyze()
                        await self._transition_to(WorkflowState.ROUTE)
                    elif self.state.current_state == WorkflowState.ROUTE:
                        await self._handle_route()
                        await self._transition_to(WorkflowState.KB_FETCH)
                    elif self.state.current_state == WorkflowState.KB_FETCH:
                        await self._handle_kb_fetch()
                        await self._transition_to(WorkflowState.Q_DRAFT)
                    elif self.state.current_state == WorkflowState.Q_DRAFT:
                        await self._handle_q_draft()
                        await self._transition_to(WorkflowState.Q_CLARIFY)
                    else:
                        break
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("error", str(e))
                raise OrchestratorError(f"Failed to run until clarification: {e}") from e

    async def ask_next_question(self) -> tuple[Optional[Any], str]:
        """
        Ask the next question in the clarification loop.

        Returns:
            Tuple of (Question object or None, status message).
            Returns (None, "") when no more questions are available.
        """
        if self.state.current_state != WorkflowState.Q_CLARIFY:
            raise OrchestratorError(
                f"Cannot ask question in state {self.state.current_state}"
            )

        if not self.state.questionnaire_draft:
            raise OrchestratorError("Questionnaire draft not available")

        # Import here to avoid circular dependencies
        from clarifier_agent.custom_model.agent import ClarifierAgent

        clarifier = ClarifierAgent()
        question, status = await clarifier.ask_question(
            self.state.questionnaire_draft,
            self.state.clarification_answers,
            self.state.clarification_question_num + 1,
        )

        if question:
            self.state.clarification_question_num += 1

        return question, status

    async def submit_clarification_answer(self, question_id: str, answer: Any) -> None:
        """
        Submit an answer to a clarification question.

        Args:
            question_id: ID of the question being answered.
            answer: Answer value.
        """
        if self.state.current_state != WorkflowState.Q_CLARIFY:
            raise OrchestratorError(
                f"Cannot submit answer in state {self.state.current_state}"
            )

        self.state.clarification_answers.append({"id": question_id, "answer": answer})

    async def finalize_clarification(self) -> None:
        """
        Finalize the clarification loop and compile QuestionnaireFinal.

        This method calls the Clarifier Agent's finalize() method to compile
        all Q&A pairs into QuestionnaireFinal.
        """
        if self.state.current_state != WorkflowState.Q_CLARIFY:
            raise OrchestratorError(
                f"Cannot finalize clarification in state {self.state.current_state}"
            )

        if not self.state.questionnaire_draft:
            raise OrchestratorError("Questionnaire draft not available")

        # Import here to avoid circular dependencies
        from clarifier_agent.custom_model.agent import ClarifierAgent

        clarifier = ClarifierAgent()
        questionnaire_final = await clarifier.finalize(
            self.state.questionnaire_draft, self.state.clarification_answers
        )

        self.state.questionnaire_final = questionnaire_final
        await self._transition_to(WorkflowState.Q_FREEZE)

    async def run_to_completion(self) -> None:
        """
        Run the workflow from current state to completion (DONE).

        This method processes Q_FREEZE gate, PLAN_ARCH, and DONE states.
        """
        with tracer.start_as_current_span("scoper_workflow.run_to_completion") as span:
            try:
                while self.state.current_state != WorkflowState.DONE:
                    if self.state.current_state == WorkflowState.Q_FREEZE:
                        can_proceed = await self._handle_q_freeze()
                        if can_proceed:
                            await self._transition_to(WorkflowState.PLAN_ARCH)
                        else:
                            # If gate fails, go back to clarification
                            await self._transition_to(WorkflowState.Q_CLARIFY)
                    elif self.state.current_state == WorkflowState.PLAN_ARCH:
                        await self._handle_plan_arch()
                        await self._transition_to(WorkflowState.DONE)
                    elif self.state.current_state == WorkflowState.DONE:
                        await self._handle_done()
                        break
                    else:
                        break
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("error", str(e))
                raise OrchestratorError(f"Failed to run to completion: {e}") from e

    def get_results(self) -> dict[str, Any]:
        """
        Get the final workflow results.

        Returns:
            Dictionary containing QuestionnaireFinal and ArchitecturePlan.

        Raises:
            OrchestratorError: If workflow is not in DONE state.
        """
        if self.state.current_state != WorkflowState.DONE:
            raise OrchestratorError(
                f"Cannot get results in state {self.state.current_state}"
            )

        if not self.state.questionnaire_final or not self.state.architecture_plan:
            raise OrchestratorError("Results not available")

        return {
            "questionnaire_final": self.state.questionnaire_final,
            "architecture_plan": self.state.architecture_plan,
            "architecture_markdown": self.state.architecture_markdown,
        }

    def get_current_state(self) -> WorkflowState:
        """
        Get the current workflow state.

        Returns:
            Current WorkflowState.
        """
        return self.state.current_state

    async def _transition_to(self, new_state: WorkflowState) -> None:
        """
        Transition to a new state with validation and tracing.

        Args:
            new_state: Target state to transition to.
        """
        with tracer.start_as_current_span("orchestrator.state_transition") as span:
            span.set_attribute("state.from", self.state.current_state.value)
            span.set_attribute("state.to", new_state.value)
            span.add_event("state_transition", {"from": self.state.current_state.value, "to": new_state.value})
            self.state.current_state = new_state

    async def _handle_ingest(self, use_case_input: UseCaseInput) -> None:
        """Handle INGEST state: validate UseCaseInput."""
        with tracer.start_as_current_span("orchestrator.ingest") as span:
            try:
                # Validate input schema
                with tracer.start_as_current_span("orchestrator.ingest.validation") as val_span:
                    validated_input = UseCaseInput.model_validate(use_case_input)
                    val_span.set_attribute("validation.success", True)
                    val_span.set_attribute("input.use_case_title", validated_input.use_case_title)
                    val_span.set_attribute("input.paragraph_length", len(validated_input.paragraph))
                    val_span.set_attribute(
                        "input.transcript_length",
                        len(validated_input.transcript) if validated_input.transcript else 0,
                    )

                self.state.use_case_input = validated_input
                span.set_attribute("ingest.success", True)
                span.add_event("ingest_completed", {"use_case_title": validated_input.use_case_title})
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("ingest.error", str(e))
                raise OrchestratorError(f"Input validation failed: {e}") from e

    async def _handle_analyze(self) -> None:
        """Handle ANALYZE state: call Requirement Analyzer Agent."""
        with tracer.start_as_current_span("orchestrator.analyze") as span:
            try:
                if not self.state.use_case_input:
                    raise OrchestratorError("UseCaseInput not available")

                # Import here to avoid circular dependencies
                from requirement_analyzer_agent.custom_model.agent import RequirementAnalyzerAgent

                agent = RequirementAnalyzerAgent()

                with tracer.start_as_current_span("orchestrator.analyze.agent_execution") as agent_span:
                    fact_extraction = await agent.run(self.state.use_case_input)
                    agent_span.set_attribute("agent.output.technical_confidence_score", fact_extraction.technical_confidence_score)
                    agent_span.set_attribute("agent.output.requirements_count", len(fact_extraction.key_extracted_requirements))
                    agent_span.set_attribute("agent.output.gaps_count", len(fact_extraction.identified_gaps))

                self.state.fact_extraction = fact_extraction
                span.set_attribute("analyze.success", True)
                span.add_event("analysis_completed", {"use_case_title": fact_extraction.use_case_title})
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("analyze.error", str(e))
                raise OrchestratorError(f"Analysis failed: {e}") from e

    async def _handle_route(self) -> None:
        """Handle ROUTE state: call Domain Router utility."""
        with tracer.start_as_current_span("orchestrator.route") as span:
            try:
                if not self.state.fact_extraction:
                    raise OrchestratorError("FactExtractionModel not available")

                selected_tracks = domain_router(self.state.fact_extraction)
                self.state.selected_tracks = selected_tracks

                span.set_attribute("route.selected_tracks", str(selected_tracks))
                span.set_attribute("route.track_count", len(selected_tracks))
                span.add_event("routing_completed", {"tracks": selected_tracks})
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("route.error", str(e))
                raise OrchestratorError(f"Routing failed: {e}") from e

    async def _handle_kb_fetch(self) -> None:
        """Handle KB_FETCH state: call KB Retriever utility."""
        with tracer.start_as_current_span("orchestrator.kb_fetch") as span:
            try:
                if not self.state.selected_tracks:
                    raise OrchestratorError("Selected tracks not available")

                kb_retriever = KBRetriever()

                with tracer.start_as_current_span("orchestrator.kb_fetch.master_questions") as mq_span:
                    master_questions = kb_retriever.get_master_questionnaire()
                    self.state.master_questions = master_questions
                    mq_span.set_attribute("kb.master_questions_count", len(master_questions))

                with tracer.start_as_current_span("orchestrator.kb_fetch.platform_guides") as pg_span:
                    platform_guides = kb_retriever.get_platform_guides(self.state.selected_tracks)
                    self.state.platform_guides = platform_guides
                    pg_span.set_attribute("kb.platform_guides_count", len(platform_guides))
                    pg_span.set_attribute("kb.platform_guides_tracks", str(list(platform_guides.keys())))

                span.set_attribute("kb_fetch.success", True)
                span.add_event("kb_fetch_completed", {
                    "master_questions_count": len(master_questions),
                    "platform_guides_count": len(platform_guides),
                })
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("kb_fetch.error", str(e))
                raise OrchestratorError(f"KB fetch failed: {e}") from e

    async def _handle_q_draft(self) -> None:
        """Handle Q_DRAFT state: call Questionnaire Agent."""
        with tracer.start_as_current_span("orchestrator.q_draft") as span:
            try:
                if not self.state.fact_extraction:
                    raise OrchestratorError("FactExtractionModel not available")
                if not self.state.master_questions:
                    raise OrchestratorError("Master questions not available")

                # Import here to avoid circular dependencies
                from questionnaire_agent.custom_model.agent import QuestionnaireAgent

                agent = QuestionnaireAgent()

                with tracer.start_as_current_span("orchestrator.q_draft.agent_execution") as agent_span:
                    questionnaire_draft = await agent.run(self.state.fact_extraction)
                    agent_span.set_attribute("agent.output.questions_count", len(questionnaire_draft.questions))
                    agent_span.set_attribute("agent.output.coverage_estimate", questionnaire_draft.coverage_estimate)
                    agent_span.set_attribute("agent.output.delta_questions_count", len(questionnaire_draft.delta_questions))

                self.state.questionnaire_draft = questionnaire_draft
                span.set_attribute("q_draft.success", True)
                span.add_event("questionnaire_draft_completed", {
                    "questions_count": len(questionnaire_draft.questions),
                    "coverage_estimate": questionnaire_draft.coverage_estimate,
                })
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("q_draft.error", str(e))
                raise OrchestratorError(f"Questionnaire draft failed: {e}") from e

    async def _handle_q_freeze(self) -> bool:
        """
        Handle Q_FREEZE gate: check if ≥80% answered OR coverage ≥0.8.

        Returns:
            True if gate passes (can proceed), False otherwise.
        """
        with tracer.start_as_current_span("orchestrator.q_freeze") as span:
            try:
                if not self.state.questionnaire_final:
                    raise OrchestratorError("QuestionnaireFinal not available")

                answered_pct = self.state.questionnaire_final.answered_pct
                coverage_estimate = (
                    self.state.questionnaire_draft.coverage_estimate
                    if self.state.questionnaire_draft
                    else 0.0
                )

                # Gate condition: ≥80% answered OR coverage ≥0.8
                can_proceed = answered_pct >= 0.8 or coverage_estimate >= 0.8

                span.set_attribute("q_freeze.answered_pct", answered_pct)
                span.set_attribute("q_freeze.coverage_estimate", coverage_estimate)
                span.set_attribute("q_freeze.gate_decision", can_proceed)
                span.add_event("gate_evaluation_completed", {
                    "answered_pct": answered_pct,
                    "coverage_estimate": coverage_estimate,
                    "can_proceed": can_proceed,
                })

                return can_proceed
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("q_freeze.error", str(e))
                raise OrchestratorError(f"Q_FREEZE gate evaluation failed: {e}") from e

    async def _handle_plan_arch(self) -> None:
        """Handle PLAN_ARCH state: call Architecture Agent with RAG context."""
        with tracer.start_as_current_span("orchestrator.plan_arch") as span:
            try:
                if not self.state.questionnaire_final:
                    raise OrchestratorError("QuestionnaireFinal not available")

                # Prepare RAG context from platform guides
                rag_context = None
                if self.state.platform_guides:
                    rag_context = "\n\n".join(
                        [f"## {track}\n{content}" for track, content in self.state.platform_guides.items()]
                    )

                # Import here to avoid circular dependencies
                from architecture_agent.custom_model.agent import ArchitectureAgent

                agent = ArchitectureAgent()

                with tracer.start_as_current_span("orchestrator.plan_arch.agent_execution") as agent_span:
                    architecture_plan, architecture_markdown = await agent.run(
                        self.state.questionnaire_final, rag_context
                    )
                    agent_span.set_attribute("agent.output.steps_count", len(architecture_plan.steps))
                    agent_span.set_attribute("agent.output.assumptions_count", len(architecture_plan.assumptions))
                    agent_span.set_attribute("agent.output.risks_count", len(architecture_plan.risks))
                    agent_span.set_attribute("rag.context_length", len(rag_context) if rag_context else 0)

                self.state.architecture_plan = architecture_plan
                self.state.architecture_markdown = architecture_markdown

                span.set_attribute("plan_arch.success", True)
                span.add_event("architecture_generation_completed", {
                    "steps_count": len(architecture_plan.steps),
                    "rag_context_length": len(rag_context) if rag_context else 0,
                })
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("plan_arch.error", str(e))
                raise OrchestratorError(f"Architecture planning failed: {e}") from e

    async def _handle_done(self) -> None:
        """Handle DONE state: finalize workflow and prepare results."""
        with tracer.start_as_current_span("orchestrator.done") as span:
            try:
                if not self.state.questionnaire_final or not self.state.architecture_plan:
                    raise OrchestratorError("Final artifacts not available")

                span.set_attribute("done.questionnaire_final.answered_pct", self.state.questionnaire_final.answered_pct)
                span.set_attribute("done.architecture_plan.steps_count", len(self.state.architecture_plan.steps))
                span.add_event("workflow_completed", {
                    "questionnaire_answered_pct": self.state.questionnaire_final.answered_pct,
                    "architecture_steps_count": len(self.state.architecture_plan.steps),
                })
            except Exception as e:
                span.record_exception(e)
                span.set_attribute("done.error", str(e))
                raise OrchestratorError(f"Done state handling failed: {e}") from e

