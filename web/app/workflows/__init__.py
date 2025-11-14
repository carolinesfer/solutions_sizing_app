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
Workflow models and repository for the Agentic Professional Services Scoper.

This module defines database models for storing workflow state and orchestrator instances.
"""

import json
import logging
import uuid as uuidpkg
from datetime import datetime, timezone
from typing import Any, Sequence, cast

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlmodel import Field, Index, SQLModel, select

from app.db import DBCtx
from app.users.user import User

logger = logging.getLogger(__name__)


class WorkflowBase(SQLModel):
    """Base workflow model with common fields."""

    workflow_id: str = Field(unique=True, index=True)
    user_uuid: uuidpkg.UUID | None = Field(
        default=None,
        sa_column=Column(
            "user", ForeignKey("user.uuid", ondelete="CASCADE"), index=True
        ),
    )
    current_state: str = Field(default="INGEST")
    orchestrator_state_json: str = Field(
        sa_column=Column(Text), default="{}"
    )  # Serialized OrchestratorState

    # Don't want two users to step on each other's toes.
    __table_args__ = (
        Index("ix_workflow_id_user", "workflow_id", "user"),
    )

    def dump_json_compatible(self) -> dict[str, Any]:
        """Convert model to JSON-compatible dictionary."""
        return cast(dict[str, Any], json.loads(self.model_dump_json()))


class Workflow(WorkflowBase, table=True):
    """Workflow database model."""

    uuid: uuidpkg.UUID = Field(
        default_factory=uuidpkg.uuid4, primary_key=True, unique=True
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    def dump_json_compatible(self) -> dict[str, Any]:
        """Convert model to JSON-compatible dictionary."""
        return cast(dict[str, Any], json.loads(self.model_dump_json()))


class WorkflowCreate(WorkflowBase):
    """Schema for creating a new workflow."""


class WorkflowRepository:
    """
    Workflow repository class to handle workflow-related database operations.
    """

    def __init__(self, db: DBCtx):
        self._db = db

    async def create_workflow(self, workflow_data: WorkflowCreate) -> Workflow:
        """Create a new workflow."""
        workflow = Workflow(**workflow_data.model_dump())

        async with self._db.session(writable=True) as session:
            session.add(workflow)
            await session.commit()
            await session.refresh(workflow)
            return workflow

    async def get_workflow(self, uuid: uuidpkg.UUID) -> Workflow | None:
        """Get workflow by UUID."""
        async with self._db.session() as sess:
            response = await sess.exec(
                select(Workflow).where(Workflow.uuid == uuid).limit(1)
            )
            return response.one_or_none()

    async def get_workflow_by_id(
        self, user_uuid: uuidpkg.UUID, workflow_id: str
    ) -> Workflow | None:
        """Get workflow by workflow_id and user."""
        async with self._db.session() as sess:
            query = (
                select(Workflow)
                .where(
                    Workflow.workflow_id == workflow_id,
                    Workflow.user_uuid == user_uuid,
                )
                .limit(1)
            )
            response = await sess.exec(query)
            return response.one_or_none()

    async def get_all_workflows(self, user: User | None) -> Sequence[Workflow]:
        """Get all workflows for a user."""
        query = select(Workflow)
        if user:
            query = query.where(Workflow.user_uuid == user.uuid)
        async with self._db.session() as sess:
            response = await sess.exec(query)
            return response.all()

    async def update_workflow_state(
        self, uuid: uuidpkg.UUID, current_state: str, orchestrator_state_json: str
    ) -> Workflow | None:
        """Update workflow state and orchestrator state."""
        async with self._db.session(writable=True) as sess:
            response = await sess.exec(
                select(Workflow).where(Workflow.uuid == uuid).limit(1)
            )
            workflow = response.one_or_none()
            if not workflow:
                return None

            workflow.current_state = current_state
            workflow.orchestrator_state_json = orchestrator_state_json
            workflow.updated_at = datetime.now(timezone.utc)
            sess.add(workflow)
            await sess.commit()
            await sess.refresh(workflow)
            return workflow

    async def delete_workflow(self, uuid: uuidpkg.UUID) -> Workflow | None:
        """Delete a workflow by UUID."""
        async with self._db.session(writable=True) as sess:
            response = await sess.exec(
                select(Workflow).where(Workflow.uuid == uuid).limit(1)
            )
            workflow = response.first()
            if not workflow:
                return None

            await sess.delete(workflow)
            await sess.commit()
            return workflow

