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
Pydantic Evals for Clarifier Agent.

This module defines evaluation datasets and evaluators for systematically
testing the Clarifier Agent's ability to conduct clarification loops.
"""

import sys
from pathlib import Path

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.evaluators.built_in import IsInstance

from scoper_shared.schemas import QuestionnaireDraft, QuestionnaireFinal, Question

# Import agent after setting up path
custom_model_path = Path(__file__).parent.parent / "custom_model"
sys.path.insert(0, str(custom_model_path))

from agent import ClarifierAgent


# Create evaluation dataset with test cases
clarifier_dataset = Dataset(
    cases=[
        Case(
            name="basic_clarification_loop",
            inputs=QuestionnaireDraft(
                questions=[
                    Question(
                        id="q1",
                        text="What is your data source?",
                        type="single_select",
                        options=["Database", "API", "File upload"],
                        required=True,
                    ),
                    Question(
                        id="q2",
                        text="Is this urgent?",
                        type="bool",
                        required=True,
                    ),
                ],
                selected_from_master_ids=["q1", "q2"],
                delta_questions=[],
                coverage_estimate=0.75,
            ),
            expected_output=QuestionnaireFinal(
                qas=[
                    {"id": "q1", "answer": "Database"},
                    {"id": "q2", "answer": True},
                ],
                answered_pct=1.0,
                gaps=[],
            ),
            metadata={"difficulty": "easy", "max_questions": 5},
        ),
        Case(
            name="partial_answers",
            inputs=QuestionnaireDraft(
                questions=[
                    Question(
                        id="q1",
                        text="What is your deployment environment?",
                        type="single_select",
                        options=["Cloud", "On-premise", "Hybrid"],
                        required=True,
                    ),
                    Question(
                        id="q2",
                        text="What is the target variable?",
                        type="free_text",
                        required=True,
                    ),
                ],
                selected_from_master_ids=["q1", "q2"],
                delta_questions=[],
                coverage_estimate=0.6,
            ),
            expected_output=QuestionnaireFinal(
                qas=[
                    {"id": "q1", "answer": "Cloud"},
                ],
                answered_pct=0.5,
                gaps=["q2"],
            ),
            metadata={"difficulty": "medium", "has_gaps": True},
        ),
    ],
    evaluators=[
        IsInstance(type_name="QuestionnaireFinal"),
    ],
)


class AnsweredPercentageEvaluator(Evaluator[QuestionnaireDraft, QuestionnaireFinal]):
    """
    Evaluates if answered_pct is calculated correctly.
    
    Scores based on how close the answered percentage is to the expected value.
    """

    def evaluate(self, ctx: EvaluatorContext[QuestionnaireDraft, QuestionnaireFinal]) -> float:
        """Evaluate answered percentage calculation."""
        if not ctx.expected_output:
            return 0.5
        
        expected_pct = ctx.expected_output.answered_pct
        actual_pct = ctx.output.answered_pct
        
        # Calculate difference
        diff = abs(expected_pct - actual_pct)
        
        if diff <= 0.1:
            return 1.0
        elif diff <= 0.2:
            return 0.8
        elif diff <= 0.3:
            return 0.6
        else:
            return 0.4


class GapIdentificationEvaluator(Evaluator[QuestionnaireDraft, QuestionnaireFinal]):
    """
    Evaluates if gaps are correctly identified.
    
    Checks if expected gaps match actual gaps.
    """

    def evaluate(self, ctx: EvaluatorContext[QuestionnaireDraft, QuestionnaireFinal]) -> float:
        """Evaluate gap identification."""
        if not ctx.expected_output:
            return 0.5
        
        expected_gaps = set(ctx.expected_output.gaps)
        actual_gaps = set(ctx.output.gaps)
        
        if not expected_gaps and not actual_gaps:
            return 1.0
        
        if not expected_gaps:
            return 0.5
        
        # Calculate overlap
        overlap = len(expected_gaps & actual_gaps)
        total = len(expected_gaps)
        
        if total == 0:
            return 1.0
        
        return overlap / total


class QACountEvaluator(Evaluator[QuestionnaireDraft, QuestionnaireFinal]):
    """
    Evaluates if the correct number of Q&A pairs were collected.
    
    Should match the number of questions in the draft (minus gaps).
    """

    def evaluate(self, ctx: EvaluatorContext[QuestionnaireDraft, QuestionnaireFinal]) -> float:
        """Evaluate Q&A pair count."""
        total_questions = len(ctx.input.questions)
        qa_count = len(ctx.output.qas)
        gaps = len(ctx.output.gaps)
        
        expected_answered = total_questions - gaps
        
        if qa_count == expected_answered:
            return 1.0
        elif abs(qa_count - expected_answered) <= 1:
            return 0.8
        else:
            return 0.5


# Add custom evaluators to dataset
clarifier_dataset.add_evaluator(AnsweredPercentageEvaluator())
clarifier_dataset.add_evaluator(GapIdentificationEvaluator())
clarifier_dataset.add_evaluator(QACountEvaluator())


async def run_clarifier_agent(inputs: QuestionnaireDraft) -> QuestionnaireFinal:
    """
    Task function for pydantic-evals.
    
    This function is called by the evaluation framework to test the agent.
    """
    agent = ClarifierAgent(max_questions=5)
    return await agent.run(inputs)


if __name__ == "__main__":
    # Run evaluation
    report = clarifier_dataset.evaluate_sync(run_clarifier_agent)
    report.print(include_input=True, include_output=True, include_durations=False)

