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
Unit tests for Pydantic schema validation in scoper_shared.

Tests validate that all schemas correctly enforce their constraints,
handle optional fields, and reject invalid data.
"""

import pytest
from pydantic import ValidationError

from scoper_shared.schemas import (
    ArchitecturePlan,
    ArchitectureStep,
    FactExtractionModel,
    Question,
    QuestionnaireDraft,
    QuestionnaireFinal,
    UseCaseInput,
)


class TestUseCaseInput:
    """Test cases for UseCaseInput schema."""

    def test_valid_input_with_all_fields(self) -> None:
        """Test UseCaseInput with all fields provided."""
        input_data = UseCaseInput(
            paragraph="Test paragraph",
            transcript="Test transcript",
            use_case_title="Test Use Case",
        )
        assert input_data.paragraph == "Test paragraph"
        assert input_data.transcript == "Test transcript"
        assert input_data.use_case_title == "Test Use Case"

    def test_valid_input_without_transcript(self) -> None:
        """Test UseCaseInput with optional transcript omitted."""
        input_data = UseCaseInput(
            paragraph="Test paragraph",
            use_case_title="Test Use Case",
        )
        assert input_data.transcript is None

    def test_missing_required_fields(self) -> None:
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError):
            UseCaseInput(paragraph="Test")  # Missing use_case_title


class TestFactExtractionModel:
    """Test cases for FactExtractionModel schema."""

    def test_valid_fact_extraction(self) -> None:
        """Test FactExtractionModel with valid data."""
        facts = FactExtractionModel(
            use_case_title="Test Use Case",
            technical_confidence_score=0.85,
            key_extracted_requirements=["req1", "req2"],
            domain_keywords=["time_series"],
            identified_gaps=["gap1"],
        )
        assert facts.technical_confidence_score == 0.85
        assert len(facts.key_extracted_requirements) == 2

    def test_confidence_score_bounds(self) -> None:
        """Test that confidence score must be between 0.0 and 1.0."""
        # Valid bounds
        FactExtractionModel(
            use_case_title="Test",
            technical_confidence_score=0.0,
            key_extracted_requirements=[],
        )
        FactExtractionModel(
            use_case_title="Test",
            technical_confidence_score=1.0,
            key_extracted_requirements=[],
        )

        # Invalid: below 0.0
        with pytest.raises(ValidationError):
            FactExtractionModel(
                use_case_title="Test",
                technical_confidence_score=-0.1,
                key_extracted_requirements=[],
            )

        # Invalid: above 1.0
        with pytest.raises(ValidationError):
            FactExtractionModel(
                use_case_title="Test",
                technical_confidence_score=1.1,
                key_extracted_requirements=[],
            )

    def test_default_empty_lists(self) -> None:
        """Test that domain_keywords and identified_gaps default to empty lists."""
        facts = FactExtractionModel(
            use_case_title="Test",
            technical_confidence_score=0.5,
            key_extracted_requirements=[],
        )
        assert facts.domain_keywords == []
        assert facts.identified_gaps == []


class TestQuestion:
    """Test cases for Question schema."""

    def test_valid_question_all_types(self) -> None:
        """Test Question with all valid question types."""
        # Free text
        Question(id="q1", text="What is your use case?", type="free_text")

        # Boolean
        Question(id="q2", text="Is this urgent?", type="bool")

        # Single select
        Question(
            id="q3",
            text="Select one:",
            type="single_select",
            options=["Option A", "Option B"],
        )

        # Multi select
        Question(
            id="q4",
            text="Select all that apply:",
            type="multi_select",
            options=["Option A", "Option B", "Option C"],
        )

    def test_question_with_tracks(self) -> None:
        """Test Question with domain tracks."""
        question = Question(
            id="q1",
            text="Test question",
            type="free_text",
            tracks=["time_series", "nlp"],
        )
        assert "time_series" in question.tracks
        assert "nlp" in question.tracks

    def test_question_with_rationale(self) -> None:
        """Test Question with rationale."""
        question = Question(
            id="q1",
            text="Test question",
            type="free_text",
            rationale="This helps us understand the data source",
        )
        assert question.rationale is not None

    def test_invalid_question_type(self) -> None:
        """Test that invalid question type raises ValidationError."""
        with pytest.raises(ValidationError):
            Question(id="q1", text="Test", type="invalid_type")


class TestArchitectureStep:
    """Test cases for ArchitectureStep schema."""

    def test_valid_step(self) -> None:
        """Test ArchitectureStep with valid data."""
        step = ArchitectureStep(
            id=1,
            name="Data Ingestion",
            purpose="Extract data from source",
            inputs=["Raw data"],
            outputs=["Cleansed data"],
        )
        assert step.id == 1
        assert step.name == "Data Ingestion"
        assert len(step.inputs) == 1
        assert len(step.outputs) == 1

    def test_step_with_empty_inputs_outputs(self) -> None:
        """Test ArchitectureStep with empty inputs/outputs (defaults)."""
        step = ArchitectureStep(
            id=1,
            name="Test Step",
            purpose="Test purpose",
        )
        assert step.inputs == []
        assert step.outputs == []


class TestQuestionnaireDraft:
    """Test cases for QuestionnaireDraft schema."""

    def test_valid_draft(self) -> None:
        """Test QuestionnaireDraft with valid data."""
        question1 = Question(id="q1", text="Question 1", type="free_text")
        question2 = Question(id="q2", text="Question 2", type="bool")
        delta_question = Question(id="q3", text="Delta question", type="single_select")

        draft = QuestionnaireDraft(
            questions=[question1, question2, delta_question],
            selected_from_master_ids=["q1", "q2"],
            delta_questions=[delta_question],
            coverage_estimate=0.75,
        )
        assert len(draft.questions) == 3
        assert len(draft.selected_from_master_ids) == 2
        assert len(draft.delta_questions) == 1
        assert draft.coverage_estimate == 0.75

    def test_coverage_estimate_bounds(self) -> None:
        """Test that coverage_estimate must be between 0.0 and 1.0."""
        question = Question(id="q1", text="Test", type="free_text")

        # Valid bounds
        QuestionnaireDraft(
            questions=[question],
            selected_from_master_ids=[],
            delta_questions=[],
            coverage_estimate=0.0,
        )
        QuestionnaireDraft(
            questions=[question],
            selected_from_master_ids=[],
            delta_questions=[],
            coverage_estimate=1.0,
        )

        # Invalid: below 0.0
        with pytest.raises(ValidationError):
            QuestionnaireDraft(
                questions=[question],
                selected_from_master_ids=[],
                delta_questions=[],
                coverage_estimate=-0.1,
            )

        # Invalid: above 1.0
        with pytest.raises(ValidationError):
            QuestionnaireDraft(
                questions=[question],
                selected_from_master_ids=[],
                delta_questions=[],
                coverage_estimate=1.1,
            )


class TestQuestionnaireFinal:
    """Test cases for QuestionnaireFinal schema."""

    def test_valid_final(self) -> None:
        """Test QuestionnaireFinal with valid data."""
        final = QuestionnaireFinal(
            qas=[
                {"id": "q1", "answer": "Answer 1"},
                {"id": "q2", "answer": "Answer 2"},
            ],
            answered_pct=0.90,
            gaps=["q3"],
        )
        assert len(final.qas) == 2
        assert final.answered_pct == 0.90
        assert "q3" in final.gaps

    def test_answered_pct_bounds(self) -> None:
        """Test that answered_pct must be between 0.0 and 1.0."""
        # Valid bounds
        QuestionnaireFinal(qas=[], answered_pct=0.0, gaps=[])
        QuestionnaireFinal(qas=[], answered_pct=1.0, gaps=[])

        # Invalid: below 0.0
        with pytest.raises(ValidationError):
            QuestionnaireFinal(qas=[], answered_pct=-0.1, gaps=[])

        # Invalid: above 1.0
        with pytest.raises(ValidationError):
            QuestionnaireFinal(qas=[], answered_pct=1.1, gaps=[])

    def test_default_empty_gaps(self) -> None:
        """Test that gaps defaults to empty list."""
        final = QuestionnaireFinal(
            qas=[{"id": "q1", "answer": "Answer"}],
            answered_pct=1.0,
        )
        assert final.gaps == []


class TestArchitecturePlan:
    """Test cases for ArchitecturePlan schema."""

    def test_valid_plan_with_min_steps(self) -> None:
        """Test ArchitecturePlan with minimum 10 steps."""
        steps = [
            ArchitectureStep(
                id=i,
                name=f"Step {i}",
                purpose=f"Purpose {i}",
                inputs=[],
                outputs=[],
            )
            for i in range(1, 11)
        ]

        plan = ArchitecturePlan(
            steps=steps,
            assumptions=["Assumption 1"],
            risks=["Risk 1"],
        )
        assert len(plan.steps) == 10

    def test_valid_plan_with_max_steps(self) -> None:
        """Test ArchitecturePlan with maximum 16 steps."""
        steps = [
            ArchitectureStep(
                id=i,
                name=f"Step {i}",
                purpose=f"Purpose {i}",
                inputs=[],
                outputs=[],
            )
            for i in range(1, 17)
        ]

        plan = ArchitecturePlan(steps=steps)
        assert len(plan.steps) == 16

    def test_plan_too_few_steps(self) -> None:
        """Test that ArchitecturePlan rejects fewer than 10 steps."""
        steps = [
            ArchitectureStep(
                id=i,
                name=f"Step {i}",
                purpose=f"Purpose {i}",
                inputs=[],
                outputs=[],
            )
            for i in range(1, 10)
        ]

        with pytest.raises(ValidationError):
            ArchitecturePlan(steps=steps)

    def test_plan_too_many_steps(self) -> None:
        """Test that ArchitecturePlan rejects more than 16 steps."""
        steps = [
            ArchitectureStep(
                id=i,
                name=f"Step {i}",
                purpose=f"Purpose {i}",
                inputs=[],
                outputs=[],
            )
            for i in range(1, 18)
        ]

        with pytest.raises(ValidationError):
            ArchitecturePlan(steps=steps)

    def test_default_empty_assumptions_risks(self) -> None:
        """Test that assumptions and risks default to empty lists."""
        steps = [
            ArchitectureStep(
                id=i,
                name=f"Step {i}",
                purpose=f"Purpose {i}",
                inputs=[],
                outputs=[],
            )
            for i in range(1, 11)
        ]

        plan = ArchitecturePlan(steps=steps)
        assert plan.assumptions == []
        assert plan.risks == []
        assert plan.notes is None

    def test_plan_with_all_fields(self) -> None:
        """Test ArchitecturePlan with all fields populated."""
        steps = [
            ArchitectureStep(
                id=i,
                name=f"Step {i}",
                purpose=f"Purpose {i}",
                inputs=[f"Input {i}"],
                outputs=[f"Output {i}"],
            )
            for i in range(1, 12)
        ]

        plan = ArchitecturePlan(
            steps=steps,
            assumptions=["Assumption 1", "Assumption 2"],
            risks=["Risk 1"],
            notes="Additional notes here",
        )
        assert len(plan.steps) == 11
        assert len(plan.assumptions) == 2
        assert len(plan.risks) == 1
        assert plan.notes == "Additional notes here"

