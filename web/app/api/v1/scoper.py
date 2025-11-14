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
FastAPI router for the Agentic Professional Services Scoper endpoints.

This module provides REST API endpoints for managing the scoping workflow:
- Start a new workflow
- Get workflow state
- Submit clarification answers
- Get final results
"""

import json
import logging
import uuid as uuidpkg
from typing import Any

from datarobot.auth.session import AuthCtx
from datarobot.auth.typing import Metadata
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from app.auth.ctx import must_get_auth_ctx
from app.deps import Deps
from app.users.user import User, UserRepository
from app.workflows import WorkflowCreate, WorkflowRepository

logger = logging.getLogger(__name__)

try:
    from scoper_shared.orchestrator import Orchestrator, OrchestratorState, WorkflowState
    from scoper_shared.schemas import UseCaseInput
except ImportError:
    # Fallback for when scoper_shared is not available
    logger.warning("scoper_shared not available, scoper endpoints will not work")
    Orchestrator = None  # type: ignore
    OrchestratorState = None  # type: ignore
    WorkflowState = None  # type: ignore
    UseCaseInput = None  # type: ignore

scoper_router = APIRouter(tags=["Scoper"])


async def _get_current_user(user_repo: UserRepository, user_id: int) -> User:
    """Get current user from repository."""
    current_user = await user_repo.get_user(user_id=user_id)
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    return current_user


# Request/Response schemas
class StartWorkflowRequest(BaseModel):
    """Request schema for starting a workflow."""

    paragraph: str
    transcript: str | None = None
    use_case_title: str


class StartWorkflowResponse(BaseModel):
    """Response schema for starting a workflow."""

    workflow_id: str
    state: str


class WorkflowStateResponse(BaseModel):
    """Response schema for workflow state."""

    workflow_id: str
    state: str
    current_question: dict[str, Any] | None = None
    progress: dict[str, Any] | None = None


class ClarificationAnswerRequest(BaseModel):
    """Request schema for submitting clarification answer."""

    question_id: str
    answer: Any


class ClarificationAnswerResponse(BaseModel):
    """Response schema for clarification answer."""

    workflow_id: str
    state: str
    next_question: dict[str, Any] | None = None
    completed: bool = False


class WorkflowResultsResponse(BaseModel):
    """Response schema for workflow results."""

    workflow_id: str
    questionnaire_final: dict[str, Any]
    architecture_plan: dict[str, Any]
    architecture_markdown: str


def _serialize_orchestrator_state(state: OrchestratorState) -> str:
    """Serialize OrchestratorState to JSON string."""
    state_dict = {
        "current_state": state.current_state.value,
        "use_case_input": (
            state.use_case_input.model_dump() if state.use_case_input else None
        ),
        "fact_extraction": (
            state.fact_extraction.model_dump() if state.fact_extraction else None
        ),
        "selected_tracks": state.selected_tracks,
        "questionnaire_draft": (
            state.questionnaire_draft.model_dump()
            if state.questionnaire_draft
            else None
        ),
        "questionnaire_final": (
            state.questionnaire_final.model_dump()
            if state.questionnaire_final
            else None
        ),
        "architecture_plan": (
            state.architecture_plan.model_dump()
            if state.architecture_plan
            else None
        ),
        "architecture_markdown": state.architecture_markdown,
        "clarification_answers": state.clarification_answers,
        "clarification_question_num": state.clarification_question_num,
    }
    return json.dumps(state_dict)


def _deserialize_orchestrator_state(state_json: str) -> OrchestratorState:
    """Deserialize JSON string to OrchestratorState."""
    state_dict = json.loads(state_json)
    state = OrchestratorState()
    state.current_state = WorkflowState(state_dict.get("current_state", "INGEST"))
    # Note: We don't fully reconstruct all objects, just the state
    # Full reconstruction would require importing all schemas
    state.clarification_answers = state_dict.get("clarification_answers", [])
    state.clarification_question_num = state_dict.get("clarification_question_num", 0)
    return state


@scoper_router.post("/scoper/start", response_model=StartWorkflowResponse)
async def start_workflow(
    request: Request,
    workflow_request: StartWorkflowRequest,
    auth_ctx: AuthCtx[Metadata] = Depends(must_get_auth_ctx),
) -> StartWorkflowResponse:
    """
    Start a new scoping workflow.

    This endpoint accepts a use case description and initiates the workflow
    by creating an orchestrator instance and running it until clarification.
    """
    current_user = await _get_current_user(
        request.app.state.deps.user_repo, int(auth_ctx.user.id)
    )

    workflow_repo: WorkflowRepository = request.app.state.deps.workflow_repo

    # Create UseCaseInput
    use_case_input = UseCaseInput(
        paragraph=workflow_request.paragraph,
        transcript=workflow_request.transcript,
        use_case_title=workflow_request.use_case_title,
    )

    # Create orchestrator and start workflow
    orchestrator = Orchestrator()
    try:
        await orchestrator.start(use_case_input)
        await orchestrator.run_until_clarification()
    except Exception as e:
        logger.error(f"Failed to start workflow: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start workflow: {str(e)}",
        ) from e

    # Generate workflow ID
    workflow_id = str(uuidpkg.uuid4())

    # Save workflow state to database
    workflow_data = WorkflowCreate(
        workflow_id=workflow_id,
        user_uuid=current_user.uuid,
        current_state=orchestrator.state.current_state.value,
        orchestrator_state_json=_serialize_orchestrator_state(orchestrator.state),
    )
    workflow = await workflow_repo.create_workflow(workflow_data)

    logger.info(f"Created workflow {workflow_id} for user {current_user.uuid}")

    return StartWorkflowResponse(
        workflow_id=workflow_id, state=orchestrator.state.current_state.value
    )


@scoper_router.get("/scoper/{workflow_id}/state", response_model=WorkflowStateResponse)
async def get_workflow_state(
    request: Request,
    workflow_id: str,
    auth_ctx: AuthCtx[Metadata] = Depends(must_get_auth_ctx),
) -> WorkflowStateResponse:
    """
    Get the current state of a workflow.

    Returns the workflow state, current question (if in clarification),
    and progress information.
    """
    current_user = await _get_current_user(
        request.app.state.deps.user_repo, int(auth_ctx.user.id)
    )

    workflow_repo: WorkflowRepository = request.app.state.deps.workflow_repo

    workflow = await workflow_repo.get_workflow_by_id(current_user.uuid, workflow_id)
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )

    # Deserialize orchestrator state
    orchestrator_state = _deserialize_orchestrator_state(
        workflow.orchestrator_state_json
    )

    # Get current question if in clarification state
    current_question = None
    if orchestrator_state.current_state == WorkflowState.Q_CLARIFY:
        # Reconstruct orchestrator to get question
        orchestrator = Orchestrator()
        orchestrator.state = orchestrator_state
        try:
            question, _ = await orchestrator.ask_next_question()
            if question:
                current_question = question.model_dump()
        except Exception as e:
            logger.warning(f"Failed to get current question: {e}")

    return WorkflowStateResponse(
        workflow_id=workflow_id,
        state=workflow.current_state,
        current_question=current_question,
        progress={"state": workflow.current_state},
    )


@scoper_router.post(
    "/scoper/{workflow_id}/clarify", response_model=ClarificationAnswerResponse
)
async def submit_clarification(
    request: Request,
    workflow_id: str,
    answer_request: ClarificationAnswerRequest,
    auth_ctx: AuthCtx[Metadata] = Depends(must_get_auth_ctx),
) -> ClarificationAnswerResponse:
    """
    Submit a clarification answer and get the next question.

    This endpoint handles the clarification loop by submitting an answer
    and either returning the next question or finalizing the questionnaire.
    """
    current_user = await _get_current_user(
        request.app.state.deps.user_repo, int(auth_ctx.user.id)
    )

    workflow_repo: WorkflowRepository = request.app.state.deps.workflow_repo

    workflow = await workflow_repo.get_workflow_by_id(current_user.uuid, workflow_id)
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )

    # Deserialize orchestrator state
    orchestrator_state = _deserialize_orchestrator_state(
        workflow.orchestrator_state_json
    )

    # Reconstruct orchestrator
    orchestrator = Orchestrator()
    orchestrator.state = orchestrator_state

    try:
        # Submit answer
        await orchestrator.submit_clarification_answer(
            answer_request.question_id, answer_request.answer
        )

        # Get next question or finalize
        question, status_msg = await orchestrator.ask_next_question()
        completed = False

        if not question:
            # No more questions, finalize
            await orchestrator.finalize_clarification()
            completed = True
            # Continue to completion
            await orchestrator.run_to_completion()

        # Update workflow state
        await workflow_repo.update_workflow_state(
            workflow.uuid,
            orchestrator.state.current_state.value,
            _serialize_orchestrator_state(orchestrator.state),
        )

        next_question = question.model_dump() if question else None

        return ClarificationAnswerResponse(
            workflow_id=workflow_id,
            state=orchestrator.state.current_state.value,
            next_question=next_question,
            completed=completed,
        )
    except Exception as e:
        logger.error(f"Failed to submit clarification: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit clarification: {str(e)}",
        ) from e


@scoper_router.get("/scoper/{workflow_id}/results", response_model=WorkflowResultsResponse)
async def get_workflow_results(
    request: Request,
    workflow_id: str,
    auth_ctx: AuthCtx[Metadata] = Depends(must_get_auth_ctx),
) -> WorkflowResultsResponse:
    """
    Get the final results of a completed workflow.

    Returns both the QuestionnaireFinal and ArchitecturePlan artifacts.
    """
    current_user = await _get_current_user(
        request.app.state.deps.user_repo, int(auth_ctx.user.id)
    )

    workflow_repo: WorkflowRepository = request.app.state.deps.workflow_repo

    workflow = await workflow_repo.get_workflow_by_id(current_user.uuid, workflow_id)
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )

    if workflow.current_state != "DONE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Workflow is not complete. Current state: {workflow.current_state}",
        )

    # Deserialize orchestrator state
    orchestrator_state = _deserialize_orchestrator_state(
        workflow.orchestrator_state_json
    )

    if not orchestrator_state.questionnaire_final or not orchestrator_state.architecture_plan:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Workflow results not available",
        )

    return WorkflowResultsResponse(
        workflow_id=workflow_id,
        questionnaire_final=orchestrator_state.questionnaire_final.model_dump(),
        architecture_plan=orchestrator_state.architecture_plan.model_dump(),
        architecture_markdown=orchestrator_state.architecture_markdown,
    )

