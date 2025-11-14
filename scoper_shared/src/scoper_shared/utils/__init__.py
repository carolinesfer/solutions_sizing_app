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
Utility functions for the Agentic Professional Services Scoper system.

This module provides:
- Domain Router: Routes use cases to appropriate domain tracks
- KB Retriever: Fetches Master Questionnaires and Platform Guides
"""

from scoper_shared.utils.domain_router import domain_router
from scoper_shared.utils.kb_retriever import KBRetriever

__all__ = ["domain_router", "KBRetriever"]

