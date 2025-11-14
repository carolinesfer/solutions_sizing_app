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
Domain Router utility for selecting appropriate domain tracks.

This module provides a rule-based function to route use cases to appropriate
domain tracks (e.g., time_series, nlp, cv, genai_rag, classic_ml) based on
extracted facts and requirements.
"""

from opentelemetry import trace

from scoper_shared.schemas import FactExtractionModel

tracer = trace.get_tracer(__name__)


def domain_router(facts: FactExtractionModel) -> list[str]:
    """
    Route a use case to appropriate domain tracks based on extracted facts.

    This function uses keyword matching to identify which domain tracks
    (time_series, nlp, cv, genai_rag) are relevant. If no tracks are
    identified, it defaults to classic_ml.

    Args:
        facts: FactExtractionModel containing extracted requirements and keywords.

    Returns:
        List of track strings (e.g., ['time_series', 'classic_ml']).

    Example:
        ```python
        facts = FactExtractionModel(
            use_case_title="Customer Churn Prediction",
            technical_confidence_score=0.85,
            key_extracted_requirements=["Predict churn", "Use historical data"],
            domain_keywords=["forecast"],
            identified_gaps=[]
        )
        tracks = domain_router(facts)
        # Returns: ['time_series', 'classic_ml']
        ```
    """
    with tracer.start_as_current_span("domain_router") as span:
        # Set input attributes
        span.set_attribute("input.use_case_title", facts.use_case_title)
        span.set_attribute(
            "input.technical_confidence_score", facts.technical_confidence_score
        )
        span.set_attribute(
            "input.key_extracted_requirements_count",
            len(facts.key_extracted_requirements),
        )
        span.set_attribute("input.domain_keywords", str(facts.domain_keywords))
        span.set_attribute("input.identified_gaps_count", len(facts.identified_gaps))

        tracks = set()

        # Combine requirements and title for keyword search
        search_text = " ".join(facts.key_extracted_requirements).lower()
        search_text += " " + facts.use_case_title.lower()
        # Also include domain_keywords in search
        search_text += " " + " ".join(facts.domain_keywords).lower()

        # Keyword matching for tracks
        if "forecast" in search_text or "time series" in search_text or "timeseries" in search_text:
            tracks.add("time_series")
        if "nlp" in search_text or "text" in search_text or "natural language" in search_text:
            tracks.add("nlp")
        if "image" in search_text or "cv" in search_text or "computer vision" in search_text or "vision" in search_text:
            tracks.add("cv")
        if "agent" in search_text or "rag" in search_text or "retrieval" in search_text or "generative" in search_text:
            tracks.add("genai_rag")

        # Default track if no matches
        if not tracks:
            tracks.add("classic_ml")

        result = list(tracks)

        # Set output attributes
        span.set_attribute("output.selected_tracks", str(result))
        span.set_attribute("output.track_count", len(result))

        # Add event when routing completes
        span.add_event("domain_routing_completed", {"tracks": result})

        return result

