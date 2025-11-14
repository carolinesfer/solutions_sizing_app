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
Integration tests for the Scoper API endpoints.

These tests verify the complete workflow of the professional services scoper,
including workflow creation, state management, clarification questions, and results retrieval.
"""
import json
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.workflows import Workflow, WorkflowRepository
from tests.conftest import authenticated_client, make_authenticated_client


@pytest.mark.asyncio
async def test_start_scoper_workflow(make_authenticated_client):
    """Test starting a new scoper workflow."""
    client = await make_authenticated_client()

    use_case_input = {
        "paragraph": "We need to build a predictive maintenance system for industrial equipment.",
        "use_case_title": "Predictive Maintenance System",
    }

    with patch("app.api.v1.scoper.Orchestrator") as mock_orchestrator_class:
        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        # Mock the orchestrator's start method
        from scoper_shared.orchestrator import OrchestratorState, WorkflowState
        from scoper_shared.schemas import Question

        mock_state = OrchestratorState(
            workflow_id=uuid4(),
            current_state=WorkflowState.Q_CLARIFY,
            use_case_input=use_case_input,
        )
        mock_question = Question(
            id="q1",
            text="What is the primary data source?",
            type="single_select",
            options=["Database", "API", "File"],
            required=True,
        )

        mock_orchestrator.start = AsyncMock(return_value=(mock_state, mock_question))

        response = client.post("/api/v1/scoper/start", json=use_case_input)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "workflow_id" in data
        assert data["current_state"] == "Q_CLARIFY"
        assert data["next_question"] is not None
        assert data["next_question"]["id"] == "q1"


@pytest.mark.asyncio
async def test_get_workflow_state(make_authenticated_client):
    """Test retrieving the current state of a workflow."""
    client = await make_authenticated_client()
    workflow_id = uuid4()

    # Create a workflow in the database
    workflow_repo: WorkflowRepository = client.app.state.deps.workflow_repo  # type: ignore[attr-defined]
    from scoper_shared.orchestrator import OrchestratorState, WorkflowState

    state_data = OrchestratorState(
        workflow_id=workflow_id,
        current_state=WorkflowState.Q_CLARIFY,
        use_case_input={"paragraph": "Test", "use_case_title": "Test"},
    )
    workflow = await workflow_repo.create_workflow(
        type("WorkflowCreate", (), {
            "user_uuid": client.app_user.uuid,  # type: ignore[attr-defined]
            "current_state": "Q_CLARIFY",
            "state_data": json.dumps(state_data.model_dump()),
        })()
    )

    with patch("app.api.v1.scoper.Orchestrator") as mock_orchestrator_class:
        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        from scoper_shared.schemas import Question

        mock_question = Question(
            id="q1",
            text="What is the primary data source?",
            type="single_select",
            options=["Database", "API"],
            required=True,
        )
        mock_orchestrator.set_state = MagicMock()
        mock_orchestrator.ask_next_question = AsyncMock(return_value=(mock_question, ""))

        response = client.get(f"/api/v1/scoper/{workflow_id}/state")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["workflow_id"] == str(workflow_id)
        assert data["current_state"] == "Q_CLARIFY"
        assert data["next_question"] is not None


@pytest.mark.asyncio
async def test_submit_clarification_answer(make_authenticated_client):
    """Test submitting a clarification answer."""
    client = await make_authenticated_client()
    workflow_id = uuid4()

    # Create a workflow in the database
    workflow_repo: WorkflowRepository = client.app.state.deps.workflow_repo  # type: ignore[attr-defined]
    from scoper_shared.orchestrator import OrchestratorState, WorkflowState

    state_data = OrchestratorState(
        workflow_id=workflow_id,
        current_state=WorkflowState.Q_CLARIFY,
        use_case_input={"paragraph": "Test", "use_case_title": "Test"},
    )
    workflow = await workflow_repo.create_workflow(
        type("WorkflowCreate", (), {
            "user_uuid": client.app_user.uuid,  # type: ignore[attr-defined]
            "current_state": "Q_CLARIFY",
            "state_data": json.dumps(state_data.model_dump()),
        })()
    )

    with patch("app.api.v1.scoper.Orchestrator") as mock_orchestrator_class:
        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        from scoper_shared.schemas import Question

        mock_question = Question(
            id="q2",
            text="What is the target variable?",
            type="free_text",
            required=True,
        )
        mock_new_state = OrchestratorState(
            workflow_id=workflow_id,
            current_state=WorkflowState.Q_CLARIFY,
            use_case_input={"paragraph": "Test", "use_case_title": "Test"},
        )

        mock_orchestrator.set_state = MagicMock()
        mock_orchestrator.submit_clarification_answer = AsyncMock(
            return_value=(mock_new_state, mock_question)
        )

        clarify_request = {
            "question_id": "q1",
            "answer": "Database",
        }

        response = client.post(f"/api/v1/scoper/{workflow_id}/clarify", json=clarify_request)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["workflow_id"] == str(workflow_id)
        assert data["next_question"] is not None
        assert data["next_question"]["id"] == "q2"


@pytest.mark.asyncio
async def test_get_workflow_results(make_authenticated_client):
    """Test retrieving final workflow results."""
    client = await make_authenticated_client()
    workflow_id = uuid4()

    # Create a completed workflow in the database
    workflow_repo: WorkflowRepository = client.app.state.deps.workflow_repo  # type: ignore[attr-defined]
    from scoper_shared.orchestrator import OrchestratorState, WorkflowState
    from scoper_shared.schemas import ArchitecturePlan, QuestionnaireFinal

    questionnaire_final = QuestionnaireFinal(
        qas=[{"id": "q1", "answer": "Database"}],
        answered_pct=0.9,
        gaps=[],
    )
    architecture_plan = ArchitecturePlan(
        steps=[
            {
                "id": "step1",
                "name": "Data Ingestion",
                "purpose": "Ingest data from database",
                "inputs": "Database connection",
                "outputs": "Raw data",
            }
        ],
        assumptions=["Database is accessible"],
        risks=["Network latency"],
    )

    state_data = OrchestratorState(
        workflow_id=workflow_id,
        current_state=WorkflowState.DONE,
        use_case_input={"paragraph": "Test", "use_case_title": "Test"},
        questionnaire_final=questionnaire_final,
        architecture_plan=architecture_plan,
        architecture_markdown="# Architecture Plan\n\n## Step 1: Data Ingestion",
    )
    workflow = await workflow_repo.create_workflow(
        type("WorkflowCreate", (), {
            "user_uuid": client.app_user.uuid,  # type: ignore[attr-defined]
            "current_state": "DONE",
            "state_data": json.dumps(state_data.model_dump()),
        })()
    )

    with patch("app.api.v1.scoper.Orchestrator") as mock_orchestrator_class:
        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        mock_orchestrator.set_state = MagicMock()
        mock_orchestrator.get_results = MagicMock(
            return_value=(questionnaire_final, architecture_plan, "# Architecture Plan\n\n## Step 1: Data Ingestion")
        )

        response = client.get(f"/api/v1/scoper/{workflow_id}/results")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["workflow_id"] == str(workflow_id)
        assert "questionnaire_final" in data
        assert "architecture_plan" in data
        assert "architecture_markdown" in data
        assert data["questionnaire_final"]["answered_pct"] == 0.9


@pytest.mark.asyncio
async def test_get_workflow_state_not_found(make_authenticated_client):
    """Test retrieving state for a non-existent workflow."""
    client = await make_authenticated_client()
    workflow_id = uuid4()

    response = client.get(f"/api/v1/scoper/{workflow_id}/state")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_submit_clarification_wrong_state(make_authenticated_client):
    """Test submitting clarification when workflow is not in clarification state."""
    client = await make_authenticated_client()
    workflow_id = uuid4()

    # Create a workflow in DONE state
    workflow_repo: WorkflowRepository = client.app.state.deps.workflow_repo  # type: ignore[attr-defined]
    from scoper_shared.orchestrator import OrchestratorState, WorkflowState

    state_data = OrchestratorState(
        workflow_id=workflow_id,
        current_state=WorkflowState.DONE,
        use_case_input={"paragraph": "Test", "use_case_title": "Test"},
    )
    workflow = await workflow_repo.create_workflow(
        type("WorkflowCreate", (), {
            "user_uuid": client.app_user.uuid,  # type: ignore[attr-defined]
            "current_state": "DONE",
            "state_data": json.dumps(state_data.model_dump()),
        })()
    )

    clarify_request = {
        "question_id": "q1",
        "answer": "Database",
    }

    response = client.post(f"/api/v1/scoper/{workflow_id}/clarify", json=clarify_request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not in clarification state" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_results_not_complete(make_authenticated_client):
    """Test retrieving results for a workflow that is not yet complete."""
    client = await make_authenticated_client()
    workflow_id = uuid4()

    # Create a workflow in Q_CLARIFY state
    workflow_repo: WorkflowRepository = client.app.state.deps.workflow_repo  # type: ignore[attr-defined]
    from scoper_shared.orchestrator import OrchestratorState, WorkflowState

    state_data = OrchestratorState(
        workflow_id=workflow_id,
        current_state=WorkflowState.Q_CLARIFY,
        use_case_input={"paragraph": "Test", "use_case_title": "Test"},
    )
    workflow = await workflow_repo.create_workflow(
        type("WorkflowCreate", (), {
            "user_uuid": client.app_user.uuid,  # type: ignore[attr-defined]
            "current_state": "Q_CLARIFY",
            "state_data": json.dumps(state_data.model_dump()),
        })()
    )

    with patch("app.api.v1.scoper.Orchestrator") as mock_orchestrator_class:
        mock_orchestrator = MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator
        mock_orchestrator.set_state = MagicMock()

        response = client.get(f"/api/v1/scoper/{workflow_id}/results")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "not yet complete" in response.json()["detail"].lower()

