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
Pydantic Evals for Requirement Analyzer Agent.

This module defines evaluation datasets and evaluators for systematically
testing the Requirement Analyzer Agent's ability to extract facts and identify gaps.
"""

import sys
from pathlib import Path

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.evaluators.built_in import IsInstance

from scoper_shared.schemas import FactExtractionModel, UseCaseInput

# Import agent after setting up path
custom_model_path = Path(__file__).parent.parent / "custom_model"
sys.path.insert(0, str(custom_model_path))

from agent import RequirementAnalyzerAgent


# Create evaluation dataset with test cases
requirement_analyzer_dataset = Dataset(
    cases=[
        Case(
            name="churn_prediction_basic",
            inputs=UseCaseInput(
                paragraph="We need to predict customer churn using historical transaction data and customer demographics.",
                use_case_title="Customer Churn Prediction",
                transcript=None,
            ),
            expected_output=FactExtractionModel(
                use_case_title="Customer Churn Prediction",
                technical_confidence_score=0.7,  # Minimum threshold
                key_extracted_requirements=["predict customer churn", "historical transaction data", "customer demographics"],
                domain_keywords=["classic_ml"],
                identified_gaps=[],  # May vary
            ),
            metadata={"difficulty": "easy", "domain": "classic_ml"},
        ),
        Case(
            name="time_series_forecast",
            inputs=UseCaseInput(
                paragraph="Forecast monthly sales for the next 12 months using time series data from the past 3 years.",
                use_case_title="Sales Forecast",
                transcript=None,
            ),
            expected_output=FactExtractionModel(
                use_case_title="Sales Forecast",
                technical_confidence_score=0.7,
                key_extracted_requirements=["forecast monthly sales", "time series data"],
                domain_keywords=["time_series"],
                identified_gaps=[],
            ),
            metadata={"difficulty": "medium", "domain": "time_series"},
        ),
        Case(
            name="nlp_sentiment_analysis",
            inputs=UseCaseInput(
                paragraph="Analyze customer reviews to determine sentiment and extract key topics.",
                use_case_title="Customer Review Analysis",
                transcript="Customer wants to understand what customers are saying about their product.",
            ),
            expected_output=FactExtractionModel(
                use_case_title="Customer Review Analysis",
                technical_confidence_score=0.7,
                key_extracted_requirements=["analyze customer reviews", "determine sentiment", "extract key topics"],
                domain_keywords=["nlp"],
                identified_gaps=[],
            ),
            metadata={"difficulty": "medium", "domain": "nlp"},
        ),
        Case(
            name="incomplete_requirements",
            inputs=UseCaseInput(
                paragraph="We want to build a recommendation system.",
                use_case_title="Recommendation System",
                transcript=None,
            ),
            expected_output=FactExtractionModel(
                use_case_title="Recommendation System",
                technical_confidence_score=0.3,  # Low due to incomplete info
                key_extracted_requirements=["recommendation system"],
                domain_keywords=["classic_ml"],
                identified_gaps=["data source", "deployment environment", "target metric"],
            ),
            metadata={"difficulty": "hard", "domain": "classic_ml", "has_gaps": True},
        ),
    ],
    evaluators=[
        IsInstance(type_name="FactExtractionModel"),
    ],
)


class TechnicalConfidenceEvaluator(Evaluator[UseCaseInput, FactExtractionModel]):
    """
    Evaluates if technical_confidence_score is within reasonable bounds.
    
    Scores:
    - 1.0 if confidence is >= 0.7 (high confidence)
    - 0.8 if confidence is >= 0.5 (medium confidence)
    - 0.5 if confidence is >= 0.3 (low confidence)
    - 0.0 if confidence < 0.3 (very low confidence)
    """

    def evaluate(self, ctx: EvaluatorContext[UseCaseInput, FactExtractionModel]) -> float:
        """Evaluate technical confidence score."""
        score = ctx.output.technical_confidence_score
        if score >= 0.7:
            return 1.0
        elif score >= 0.5:
            return 0.8
        elif score >= 0.3:
            return 0.5
        else:
            return 0.0


class RequirementsExtractionEvaluator(Evaluator[UseCaseInput, FactExtractionModel]):
    """
    Evaluates if key requirements were extracted correctly.
    
    Checks if expected requirements appear in the extracted requirements list.
    """

    def evaluate(self, ctx: EvaluatorContext[UseCaseInput, FactExtractionModel]) -> float:
        """Evaluate requirements extraction quality."""
        if not ctx.expected_output:
            return 0.5  # Can't evaluate without expected output
        
        expected_reqs = {req.lower() for req in ctx.expected_output.key_extracted_requirements}
        actual_reqs = {req.lower() for req in ctx.output.key_extracted_requirements}
        
        if not expected_reqs:
            return 0.5
        
        # Calculate overlap
        overlap = len(expected_reqs & actual_reqs)
        total = len(expected_reqs)
        
        if total == 0:
            return 0.5
        
        return overlap / total


class DomainKeywordEvaluator(Evaluator[UseCaseInput, FactExtractionModel]):
    """
    Evaluates if correct domain keywords were identified.
    
    Checks if expected domain keywords appear in the identified keywords.
    """

    def evaluate(self, ctx: EvaluatorContext[UseCaseInput, FactExtractionModel]) -> float:
        """Evaluate domain keyword identification."""
        if not ctx.expected_output:
            return 0.5
        
        expected_domains = set(ctx.expected_output.domain_keywords)
        actual_domains = set(ctx.output.domain_keywords)
        
        if not expected_domains:
            return 0.5
        
        # Calculate overlap
        overlap = len(expected_domains & actual_domains)
        total = len(expected_domains)
        
        if total == 0:
            return 0.5
        
        return overlap / total


# Add custom evaluators to dataset
requirement_analyzer_dataset.add_evaluator(TechnicalConfidenceEvaluator())
requirement_analyzer_dataset.add_evaluator(RequirementsExtractionEvaluator())
requirement_analyzer_dataset.add_evaluator(DomainKeywordEvaluator())


async def run_requirement_analyzer(inputs: UseCaseInput) -> FactExtractionModel:
    """
    Task function for pydantic-evals.
    
    This function is called by the evaluation framework to test the agent.
    """
    agent = RequirementAnalyzerAgent()
    return await agent.run(inputs)


if __name__ == "__main__":
    # Run evaluation
    report = requirement_analyzer_dataset.evaluate_sync(run_requirement_analyzer)
    report.print(include_input=True, include_output=True, include_durations=False)

