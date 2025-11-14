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
Pydantic Evals for Questionnaire Agent.

This module defines evaluation datasets and evaluators for systematically
testing the Questionnaire Agent's ability to generate tailored questionnaires.
"""

import sys
from pathlib import Path

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.evaluators.built_in import IsInstance

from scoper_shared.schemas import FactExtractionModel, QuestionnaireDraft

# Import agent after setting up path
custom_model_path = Path(__file__).parent.parent / "custom_model"
sys.path.insert(0, str(custom_model_path))

from agent import QuestionnaireAgent


# Create evaluation dataset with test cases
questionnaire_dataset = Dataset(
    cases=[
        Case(
            name="churn_prediction_questionnaire",
            inputs=FactExtractionModel(
                use_case_title="Customer Churn Prediction",
                technical_confidence_score=0.85,
                key_extracted_requirements=["predict customer churn", "historical transaction data"],
                domain_keywords=["classic_ml"],
                identified_gaps=["data source location", "deployment environment"],
            ),
            expected_output=QuestionnaireDraft(
                questions=[],  # Will be populated by agent
                selected_from_master_ids=[],
                delta_questions=[],
                coverage_estimate=0.7,  # Minimum threshold
            ),
            metadata={"difficulty": "medium", "domain": "classic_ml", "has_gaps": True},
        ),
        Case(
            name="time_series_questionnaire",
            inputs=FactExtractionModel(
                use_case_title="Sales Forecast",
                technical_confidence_score=0.8,
                key_extracted_requirements=["forecast monthly sales", "time series data"],
                domain_keywords=["time_series"],
                identified_gaps=[],
            ),
            expected_output=QuestionnaireDraft(
                questions=[],
                selected_from_master_ids=[],
                delta_questions=[],
                coverage_estimate=0.7,
            ),
            metadata={"difficulty": "easy", "domain": "time_series"},
        ),
    ],
    evaluators=[
        IsInstance(type_name="QuestionnaireDraft"),
    ],
)


class CoverageEvaluator(Evaluator[FactExtractionModel, QuestionnaireDraft]):
    """
    Evaluates if coverage_estimate is reasonable.
    
    Scores:
    - 1.0 if coverage >= 0.8 (high coverage)
    - 0.8 if coverage >= 0.6 (medium coverage)
    - 0.5 if coverage >= 0.4 (low coverage)
    - 0.0 if coverage < 0.4 (very low coverage)
    """

    def evaluate(self, ctx: EvaluatorContext[FactExtractionModel, QuestionnaireDraft]) -> float:
        """Evaluate coverage estimate."""
        coverage = ctx.output.coverage_estimate
        if coverage >= 0.8:
            return 1.0
        elif coverage >= 0.6:
            return 0.8
        elif coverage >= 0.4:
            return 0.5
        else:
            return 0.0


class DeltaQuestionsEvaluator(Evaluator[FactExtractionModel, QuestionnaireDraft]):
    """
    Evaluates if delta questions were generated for identified gaps.
    
    If gaps exist, delta questions should be generated.
    """

    def evaluate(self, ctx: EvaluatorContext[FactExtractionModel, QuestionnaireDraft]) -> float:
        """Evaluate delta question generation."""
        gaps = ctx.input.identified_gaps
        delta_questions = ctx.output.delta_questions
        
        if not gaps:
            # No gaps expected, so no delta questions is fine
            return 1.0 if not delta_questions else 0.8
        
        # If gaps exist, we should have delta questions
        if delta_questions:
            return 1.0
        else:
            return 0.3  # Penalty for missing delta questions when gaps exist


class QuestionQualityEvaluator(Evaluator[FactExtractionModel, QuestionnaireDraft]):
    """
    Evaluates if questions are well-formed and relevant.
    
    Checks that questions have required fields and are not empty.
    """

    def evaluate(self, ctx: EvaluatorContext[FactExtractionModel, QuestionnaireDraft]) -> float:
        """Evaluate question quality."""
        questions = ctx.output.questions
        
        if not questions:
            return 0.3  # Should have at least some questions
        
        # Check that all questions have required fields
        valid_count = 0
        for q in questions:
            if q.id and q.text and q.type:
                valid_count += 1
        
        if len(questions) == 0:
            return 0.0
        
        return valid_count / len(questions)


# Add custom evaluators to dataset
questionnaire_dataset.add_evaluator(CoverageEvaluator())
questionnaire_dataset.add_evaluator(DeltaQuestionsEvaluator())
questionnaire_dataset.add_evaluator(QuestionQualityEvaluator())


async def run_questionnaire_agent(inputs: FactExtractionModel) -> QuestionnaireDraft:
    """
    Task function for pydantic-evals.
    
    This function is called by the evaluation framework to test the agent.
    """
    agent = QuestionnaireAgent()
    return await agent.run(inputs)


if __name__ == "__main__":
    # Run evaluation
    report = questionnaire_dataset.evaluate_sync(run_questionnaire_agent)
    report.print(include_input=True, include_output=True, include_durations=False)

