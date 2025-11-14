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
Knowledge Base Retriever utility for fetching Master Questionnaires and Platform Guides.

This module provides functionality to:
- Load Master Questionnaire from JSON file
- Load Platform Guides from Markdown files
- Filter content based on domain tracks
"""

import json
import os
from pathlib import Path
from typing import List

from opentelemetry import trace

from scoper_shared.schemas import Question

tracer = trace.get_tracer(__name__)

# Get the directory containing this file
_UTILS_DIR = Path(__file__).parent
_SCOPER_SHARED_DIR = _UTILS_DIR.parent
_KB_CONTENT_DIR = _SCOPER_SHARED_DIR / "kb_content"
_MASTER_QUESTIONNAIRE_PATH = _KB_CONTENT_DIR / "master_questionnaire.json"
_PLATFORM_GUIDES_DIR = _KB_CONTENT_DIR / "platform_guides"


class KBRetriever:
    """
    Knowledge Base Retriever for fetching Master Questionnaires and Platform Guides.

    This class provides methods to:
    - Load and parse Master Questionnaire JSON into Question objects
    - Load Platform Guides from Markdown files
    - Filter content based on domain tracks

    Example:
        ```python
        retriever = KBRetriever()
        questions = retriever.get_master_questionnaire()
        guides = retriever.get_platform_guides(["time_series", "classic_ml"])
        ```
    """

    def __init__(self, kb_content_dir: Path | None = None) -> None:
        """
        Initialize the KB Retriever.

        Args:
            kb_content_dir: Optional custom path to KB content directory.
                If None, uses default path relative to this module.
        """
        if kb_content_dir is None:
            self.kb_content_dir = _KB_CONTENT_DIR
            self.master_questionnaire_path = _MASTER_QUESTIONNAIRE_PATH
            self.platform_guides_dir = _PLATFORM_GUIDES_DIR
        else:
            self.kb_content_dir = Path(kb_content_dir)
            self.master_questionnaire_path = (
                self.kb_content_dir / "master_questionnaire.json"
            )
            self.platform_guides_dir = self.kb_content_dir / "platform_guides"

    def get_master_questionnaire(self) -> List[Question]:
        """
        Load and parse the Master Questionnaire from JSON file.

        Returns:
            List of Question objects parsed from the Master Questionnaire JSON.

        Raises:
            FileNotFoundError: If the master_questionnaire.json file does not exist.
            ValueError: If the JSON file cannot be parsed or is invalid.

        Example:
            ```python
            retriever = KBRetriever()
            questions = retriever.get_master_questionnaire()
            ```
        """
        with tracer.start_as_current_span(
            "kb_retriever.get_master_questionnaire"
        ) as span:
            span.set_attribute("file.path", str(self.master_questionnaire_path))

            if not self.master_questionnaire_path.exists():
                raise FileNotFoundError(
                    f"Master questionnaire file not found: {self.master_questionnaire_path}"
                )

            try:
                with open(self.master_questionnaire_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Parse JSON into Question objects
                # Handle both list of questions and dict with "questions" key
                if isinstance(data, list):
                    questions_data = data
                elif isinstance(data, dict) and "questions" in data:
                    questions_data = data["questions"]
                else:
                    raise ValueError(
                        "Invalid JSON structure: expected list of questions or dict with 'questions' key"
                    )

                questions = [Question(**q) for q in questions_data]

                span.set_attribute("question_count", len(questions))
                span.add_event("master_questionnaire_parsed", {"count": len(questions)})

                return questions

            except json.JSONDecodeError as e:
                span.record_exception(e)
                raise ValueError(
                    f"Invalid JSON in master questionnaire file: {e}"
                ) from e
            except Exception as e:
                span.record_exception(e)
                raise

    def get_platform_guides(self, selected_tracks: List[str]) -> dict[str, str]:
        """
        Load Platform Guides from Markdown files based on selected tracks.

        This method supports two directory structures:
        1. Subdirectory structure (preferred): `platform_guides/{track}/*.md` - loads all .md files from track subdirectories
        2. Flat structure (backward compatible): `platform_guides/{track}.md` - loads single file per track

        Files are organized by track name (e.g., `time_series/`, `nlp/`, `classic_ml/`, etc.).
        Multiple files in a track subdirectory are concatenated with separators.

        Args:
            selected_tracks: List of track strings to filter guides (e.g., ['time_series', 'nlp']).

        Returns:
            Dictionary mapping track names to guide content (concatenated markdown text).

        Example:
            ```python
            retriever = KBRetriever()
            guides = retriever.get_platform_guides(["time_series", "classic_ml"])
            # Returns: {'time_series': '...', 'classic_ml': '...'}
            ```
        """
        with tracer.start_as_current_span("kb_retriever.get_platform_guides") as span:
            span.set_attribute("selected_tracks", str(selected_tracks))
            span.set_attribute("platform_guides_dir", str(self.platform_guides_dir))

            guides: dict[str, str] = {}

            if not self.platform_guides_dir.exists():
                span.add_event("platform_guides_directory_not_found")
                return guides

            # Load guides for each selected track
            for track in selected_tracks:
                track_dir = self.platform_guides_dir / track
                track_file = self.platform_guides_dir / f"{track}.md"

                track_content_parts: list[str] = []

                # First, try subdirectory structure (preferred for task 7.6)
                if track_dir.exists() and track_dir.is_dir():
                    # Load all .md files from the track subdirectory
                    md_files = sorted(track_dir.glob("*.md"))
                    for md_file in md_files:
                        try:
                            with open(md_file, "r", encoding="utf-8") as f:
                                content = f.read()
                                # Add file header for context
                                track_content_parts.append(
                                    f"## {md_file.name}\n\n{content}"
                                )
                        except Exception as e:
                            span.record_exception(e)
                            # Continue loading other files even if one fails
                            continue

                # Fallback to flat structure (backward compatible)
                elif track_file.exists() and track_file.is_file():
                    try:
                        with open(track_file, "r", encoding="utf-8") as f:
                            track_content_parts.append(f.read())
                    except Exception as e:
                        span.record_exception(e)
                        continue

                # Combine all content for this track
                if track_content_parts:
                    guides[track] = "\n\n---\n\n".join(track_content_parts)

            # Also load any general guides from general/ subdirectory or general.md file
            general_dir = self.platform_guides_dir / "general"

            general_content_parts: list[str] = []

            # Try general/ subdirectory first (preferred)
            general_dir_processed = False
            if general_dir.exists() and general_dir.is_dir():
                md_files = sorted(general_dir.glob("*.md"))
                for md_file in md_files:
                    try:
                        with open(md_file, "r", encoding="utf-8") as f:
                            content = f.read()
                            general_content_parts.append(
                                f"## {md_file.name}\n\n{content}"
                            )
                    except Exception as e:
                        span.record_exception(e)
                        continue
                # Only mark as processed if files were actually loaded
                if general_content_parts:
                    general_dir_processed = True

            # Fallback to general.md, common.md, overview.md files
            # Only load flat files if general/ subdirectory wasn't already processed
            # (prevents duplicate content if both subdirectory and flat files exist)
            if not general_dir_processed:
                for guide_name in ["general.md", "common.md", "overview.md"]:
                    guide_path = self.platform_guides_dir / guide_name
                    if guide_path.exists() and guide_path.is_file():
                        try:
                            with open(guide_path, "r", encoding="utf-8") as f:
                                general_content_parts.append(f.read())
                        except Exception as e:
                            span.record_exception(e)
                            continue

            # Add general content if found
            if general_content_parts:
                guides["general"] = "\n\n---\n\n".join(general_content_parts)

            span.set_attribute("guides_found_count", len(guides))
            span.set_attribute("guide_tracks", str(list(guides.keys())))
            span.add_event("platform_guides_filtered", {"count": len(guides)})

            return guides
