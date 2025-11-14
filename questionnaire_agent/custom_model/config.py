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
# ------------------------------------------------------------------------------
"""
All configuration for the agent application. The config class handles
loading variables from environment, .env files, Pulumi outputs, and
DataRobot credentials automatically.
"""

from typing import Any
from urllib.parse import urlparse

from datarobot.core.config import DataRobotAppFrameworkBaseSettings
from pydantic import Field, model_validator


class Config(DataRobotAppFrameworkBaseSettings):
    """
    This class finds variables in the priority order of: env
    variables (including Runtime Parameters), .env, file_secrets, then
    Pulumi output variables.
    """

    llm_deployment_id: str | None = None
    llm_default_model: str = "azure/gpt-4o-mini"  # Model ID for DataRobot LLM Gateway (without 'datarobot/' prefix)
    use_datarobot_llm_gateway: bool = Field(
        default=False, validation_alias="USE_DATAROBOT_LLM_GATEWAY"
    )
    mcp_deployment_id: str | None = None
    external_mcp_url: str | None = None

    agent_endpoint: str = Field(
        default="http://localhost:8842", validation_alias="QUESTIONNAIRE_AGENT_ENDPOINT"
    )

    @property
    def local_dev_port(self) -> int:
        parsed_url = urlparse(self.agent_endpoint)
        if parsed_url.port:
            return parsed_url.port
        raise ValueError(f"No port in {self.agent_endpoint}")

    @model_validator(mode="after")
    def auto_enable_llm_gateway_from_infra(self) -> "Config":
        """Automatically enable LLM Gateway if INFRA_ENABLE_LLM=gateway_direct.py is set."""
        import os
        infra_enable_llm = os.getenv("INFRA_ENABLE_LLM", "")
        if infra_enable_llm == "gateway_direct.py" and not self.use_datarobot_llm_gateway:
            # If INFRA_ENABLE_LLM=gateway_direct.py is set, automatically enable LLM Gateway
            self.use_datarobot_llm_gateway = True
        return self

    @model_validator(mode="before")
    @classmethod
    def replace_placeholder_values(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for field_name, field_info in cls.model_fields.items():
                if data.get(field_name) == "SET_VIA_PULUMI_OR_MANUALLY":
                    data[field_name] = field_info.default
        return data
