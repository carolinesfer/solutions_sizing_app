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

"""create_workflow_table

Creates the workflow table for storing Agentic Professional Services Scoper workflow state.

Revision ID: a1b2c3d4e5f6
Revises: 4d5262be920d
Create Date: 2025-01-15 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "4d5262be920d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema"""
    op.create_table(
        "workflow",
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("workflow_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("user", sa.Uuid(), nullable=True),
        sa.Column("current_state", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "orchestrator_state_json", sa.Text(), nullable=False, server_default="{}"
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user"], ["user.uuid"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("uuid"),
        sa.UniqueConstraint("workflow_id"),
    )
    op.create_index(
        op.f("ix_workflow_workflow_id"), "workflow", ["workflow_id"], unique=True
    )
    op.create_index(op.f("ix_workflow_id_user"), "workflow", ["workflow_id", "user"], unique=False)
    op.create_index(op.f("ix_workflow_user"), "workflow", ["user"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_workflow_user"), table_name="workflow")
    op.drop_index(op.f("ix_workflow_id_user"), table_name="workflow")
    op.drop_index(op.f("ix_workflow_workflow_id"), table_name="workflow")
    op.drop_table("workflow")

