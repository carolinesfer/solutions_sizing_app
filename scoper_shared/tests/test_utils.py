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
Unit tests for utility functions in scoper_shared.utils.

Tests validate Domain Router and KB Retriever functionality.
"""

import json
import tempfile
from pathlib import Path

import pytest

from scoper_shared.schemas import FactExtractionModel, Question
from scoper_shared.utils.domain_router import domain_router
from scoper_shared.utils.kb_retriever import KBRetriever


class TestDomainRouter:
    """Test cases for domain_router function."""

    def test_time_series_track(self) -> None:
        """Test that time series keywords route to time_series track."""
        facts = FactExtractionModel(
            use_case_title="Sales Forecast",
            technical_confidence_score=0.8,
            key_extracted_requirements=["forecast sales", "time series data"],
            domain_keywords=[],
            identified_gaps=[],
        )
        tracks = domain_router(facts)
        assert "time_series" in tracks

    def test_nlp_track(self) -> None:
        """Test that NLP keywords route to nlp track."""
        facts = FactExtractionModel(
            use_case_title="Text Classification",
            technical_confidence_score=0.8,
            key_extracted_requirements=["classify text", "NLP model"],
            domain_keywords=[],
            identified_gaps=[],
        )
        tracks = domain_router(facts)
        assert "nlp" in tracks

    def test_cv_track(self) -> None:
        """Test that computer vision keywords route to cv track."""
        facts = FactExtractionModel(
            use_case_title="Image Recognition",
            technical_confidence_score=0.8,
            key_extracted_requirements=["image classification", "CV model"],
            domain_keywords=[],
            identified_gaps=[],
        )
        tracks = domain_router(facts)
        assert "cv" in tracks

    def test_genai_rag_track(self) -> None:
        """Test that RAG/agent keywords route to genai_rag track."""
        facts = FactExtractionModel(
            use_case_title="RAG System",
            technical_confidence_score=0.8,
            key_extracted_requirements=["retrieval augmented generation", "agent"],
            domain_keywords=[],
            identified_gaps=[],
        )
        tracks = domain_router(facts)
        assert "genai_rag" in tracks

    def test_multiple_tracks(self) -> None:
        """Test that multiple tracks can be selected."""
        facts = FactExtractionModel(
            use_case_title="Time Series NLP",
            technical_confidence_score=0.8,
            key_extracted_requirements=["forecast", "text analysis"],
            domain_keywords=[],
            identified_gaps=[],
        )
        tracks = domain_router(facts)
        assert "time_series" in tracks
        assert "nlp" in tracks

    def test_default_classic_ml(self) -> None:
        """Test that default track is classic_ml when no keywords match."""
        facts = FactExtractionModel(
            use_case_title="Customer Churn",
            technical_confidence_score=0.8,
            key_extracted_requirements=["predict churn", "binary classification"],
            domain_keywords=[],
            identified_gaps=[],
        )
        tracks = domain_router(facts)
        assert "classic_ml" in tracks
        assert len(tracks) >= 1

    def test_domain_keywords_in_search(self) -> None:
        """Test that domain_keywords are included in search."""
        facts = FactExtractionModel(
            use_case_title="Some Use Case",
            technical_confidence_score=0.8,
            key_extracted_requirements=[],
            domain_keywords=["time series", "forecast"],
            identified_gaps=[],
        )
        tracks = domain_router(facts)
        assert "time_series" in tracks


class TestKBRetriever:
    """Test cases for KBRetriever class."""

    def test_get_master_questionnaire_list_format(self) -> None:
        """Test loading master questionnaire as list format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            questions_data = [
                {
                    "id": "q1",
                    "text": "What is your data source?",
                    "type": "single_select",
                    "options": ["Database", "API"],
                    "required": True,
                    "tracks": ["classic_ml"],
                },
                {
                    "id": "q2",
                    "text": "What is your target variable?",
                    "type": "free_text",
                    "required": True,
                    "tracks": ["classic_ml"],
                },
            ]
            questionnaire_path = kb_dir / "master_questionnaire.json"
            with open(questionnaire_path, "w", encoding="utf-8") as f:
                json.dump(questions_data, f)

            retriever = KBRetriever(kb_content_dir=kb_dir)
            questions = retriever.get_master_questionnaire()

            assert len(questions) == 2
            assert questions[0].id == "q1"
            assert questions[1].id == "q2"

    def test_get_master_questionnaire_dict_format(self) -> None:
        """Test loading master questionnaire as dict with 'questions' key."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            questions_data = {
                "questions": [
                    {
                        "id": "q1",
                        "text": "What is your data source?",
                        "type": "single_select",
                        "options": ["Database", "API"],
                        "required": True,
                        "tracks": ["classic_ml"],
                    }
                ]
            }
            questionnaire_path = kb_dir / "master_questionnaire.json"
            with open(questionnaire_path, "w", encoding="utf-8") as f:
                json.dump(questions_data, f)

            retriever = KBRetriever(kb_content_dir=kb_dir)
            questions = retriever.get_master_questionnaire()

            assert len(questions) == 1
            assert questions[0].id == "q1"

    def test_get_master_questionnaire_file_not_found(self) -> None:
        """Test that FileNotFoundError is raised when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            retriever = KBRetriever(kb_content_dir=kb_dir)

            with pytest.raises(FileNotFoundError):
                retriever.get_master_questionnaire()

    def test_get_master_questionnaire_invalid_json(self) -> None:
        """Test that ValueError is raised for invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            questionnaire_path = kb_dir / "master_questionnaire.json"
            with open(questionnaire_path, "w", encoding="utf-8") as f:
                f.write("invalid json {")

            retriever = KBRetriever(kb_content_dir=kb_dir)

            with pytest.raises(ValueError):
                retriever.get_master_questionnaire()

    def test_get_platform_guides(self) -> None:
        """Test loading platform guides for selected tracks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            guides_dir = kb_dir / "platform_guides"
            guides_dir.mkdir()

            # Create guide files
            (guides_dir / "time_series.md").write_text("# Time Series Guide\nContent here")
            (guides_dir / "nlp.md").write_text("# NLP Guide\nContent here")
            (guides_dir / "classic_ml.md").write_text("# Classic ML Guide\nContent here")

            retriever = KBRetriever(kb_content_dir=kb_dir)
            guides = retriever.get_platform_guides(["time_series", "nlp"])

            assert "time_series" in guides
            assert "nlp" in guides
            assert "classic_ml" not in guides
            assert "# Time Series Guide" in guides["time_series"]
            assert "# NLP Guide" in guides["nlp"]

    def test_get_platform_guides_missing_directory(self) -> None:
        """Test that empty dict is returned when platform_guides directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            retriever = KBRetriever(kb_content_dir=kb_dir)
            guides = retriever.get_platform_guides(["time_series"])

            assert guides == {}

    def test_get_platform_guides_missing_files(self) -> None:
        """Test that only existing guide files are returned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            guides_dir = kb_dir / "platform_guides"
            guides_dir.mkdir()
            (guides_dir / "time_series.md").write_text("# Time Series Guide")

            retriever = KBRetriever(kb_content_dir=kb_dir)
            guides = retriever.get_platform_guides(["time_series", "nonexistent"])

            assert "time_series" in guides
            assert "nonexistent" not in guides

    def test_get_platform_guides_general_guides(self) -> None:
        """Test that general guides (general.md, common.md) are loaded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            guides_dir = kb_dir / "platform_guides"
            guides_dir.mkdir()
            (guides_dir / "general.md").write_text("# General Guide")
            (guides_dir / "common.md").write_text("# Common Guide")

            retriever = KBRetriever(kb_content_dir=kb_dir)
            guides = retriever.get_platform_guides(["time_series"])

            assert "general" in guides
            assert "common" in guides

    def test_get_platform_guides_subdirectory_structure(self) -> None:
        """Test loading platform guides from subdirectory structure (task 7.6)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            guides_dir = kb_dir / "platform_guides"
            guides_dir.mkdir()

            # Create subdirectory structure
            time_series_dir = guides_dir / "time_series"
            time_series_dir.mkdir()
            (time_series_dir / "doc1.md").write_text("# Time Series Doc 1\nContent 1")
            (time_series_dir / "doc2.md").write_text("# Time Series Doc 2\nContent 2")

            nlp_dir = guides_dir / "nlp"
            nlp_dir.mkdir()
            (nlp_dir / "nlp_guide.md").write_text("# NLP Guide\nNLP content")

            general_dir = guides_dir / "general"
            general_dir.mkdir()
            (general_dir / "overview.md").write_text("# Overview\nGeneral content")

            retriever = KBRetriever(kb_content_dir=kb_dir)
            guides = retriever.get_platform_guides(["time_series", "nlp"])

            # Check that tracks are loaded
            assert "time_series" in guides
            assert "nlp" in guides
            # Check that multiple files are concatenated
            assert "Time Series Doc 1" in guides["time_series"]
            assert "Time Series Doc 2" in guides["time_series"]
            assert "Content 1" in guides["time_series"]
            assert "Content 2" in guides["time_series"]
            # Check that general guides are also loaded
            assert "general" in guides
            assert "Overview" in guides["general"]

    def test_get_platform_guides_subdirectory_preferred_over_flat(self) -> None:
        """Test that subdirectory structure is preferred over flat structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            kb_dir = Path(tmpdir)
            guides_dir = kb_dir / "platform_guides"
            guides_dir.mkdir()

            # Create both subdirectory and flat file
            time_series_dir = guides_dir / "time_series"
            time_series_dir.mkdir()
            (time_series_dir / "doc1.md").write_text("# Subdirectory Content")
            (guides_dir / "time_series.md").write_text("# Flat File Content")

            retriever = KBRetriever(kb_content_dir=kb_dir)
            guides = retriever.get_platform_guides(["time_series"])

            # Should load from subdirectory, not flat file
            assert "time_series" in guides
            assert "Subdirectory Content" in guides["time_series"]
            assert "Flat File Content" not in guides["time_series"]

