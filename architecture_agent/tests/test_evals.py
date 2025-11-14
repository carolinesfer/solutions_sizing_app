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
Pydantic Evals for Architecture Agent.

This module defines evaluation datasets and evaluators for systematically
testing the Architecture Agent's ability to generate solution architecture plans.
"""

import sys
from pathlib import Path

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from pydantic_evals.evaluators.built_in import IsInstance

from scoper_shared.schemas import ArchitecturePlan, QuestionnaireFinal

# Import agent after setting up path
custom_model_path = Path(__file__).parent.parent / "custom_model"
sys.path.insert(0, str(custom_model_path))

from agent import ArchitectureAgent


# Create evaluation dataset with test cases
architecture_dataset = Dataset(
    cases=[
        Case(
            name="churn_prediction_architecture",
            inputs=QuestionnaireFinal(
                qas=[
                    {"id": "q1", "answer": "Database"},
                    {"id": "q2", "answer": "Customer churn"},
                    {"id": "q3", "answer": "Cloud"},
                ],
                answered_pct=0.9,
                gaps=[],
            ),
            expected_output=ArchitecturePlan(
                steps=[],  # Will be populated by agent (10-16 steps)
                assumptions=[],
                risks=[],
            ),
            metadata={"difficulty": "medium", "domain": "classic_ml"},
        ),
        Case(
            name="time_series_architecture",
            inputs=QuestionnaireFinal(
                qas=[
                    {"id": "q1", "answer": "Time series data"},
                    {"id": "q2", "answer": "Monthly sales forecast"},
                ],
                answered_pct=0.85,
                gaps=["q3"],
            ),
            expected_output=ArchitecturePlan(
                steps=[],
                assumptions=[],
                risks=[],
            ),
            metadata={"difficulty": "medium", "domain": "time_series"},
        ),
    ],
    evaluators=[
        IsInstance(type_name="ArchitecturePlan"),
    ],
)


class StepCountEvaluator(Evaluator[QuestionnaireFinal, ArchitecturePlan]):
    """
    Evaluates if the architecture plan has the correct number of steps (10-16).
    
    Scores:
    - 1.0 if steps are between 10-16
    - 0.8 if steps are between 8-9 or 17-18
    - 0.5 if steps are between 6-7 or 19-20
    - 0.0 if steps are < 6 or > 20
    """

    def evaluate(self, ctx: EvaluatorContext[QuestionnaireFinal, ArchitecturePlan]) -> float:
        """Evaluate step count."""
        step_count = len(ctx.output.steps)
        
        if 10 <= step_count <= 16:
            return 1.0
        elif 8 <= step_count <= 18:
            return 0.8
        elif 6 <= step_count <= 20:
            return 0.5
        else:
            return 0.0


class StepCompletenessEvaluator(Evaluator[QuestionnaireFinal, ArchitecturePlan]):
    """
    Evaluates if all steps have required fields (id, name, purpose, inputs, outputs).
    
    Checks that steps are well-formed and complete.
    """

    def evaluate(self, ctx: EvaluatorContext[QuestionnaireFinal, ArchitecturePlan]) -> float:
        """Evaluate step completeness."""
        steps = ctx.output.steps
        
        if not steps:
            return 0.0
        
        complete_count = 0
        for step in steps:
            if (
                step.id
                and step.name
                and step.purpose
                and step.inputs
                and step.outputs
            ):
                complete_count += 1
        
        return complete_count / len(steps)


class AssumptionsRisksEvaluator(Evaluator[QuestionnaireFinal, ArchitecturePlan]):
    """
    Evaluates if assumptions and risks are identified.
    
    A good architecture plan should identify key assumptions and risks.
    """

    def evaluate(self, ctx: EvaluatorContext[QuestionnaireFinal, ArchitecturePlan]) -> float:
        """Evaluate assumptions and risks identification."""
        assumptions = ctx.output.assumptions
        risks = ctx.output.risks
        
        # Both should be present (even if empty lists)
        has_assumptions = assumptions is not None
        has_risks = risks is not None
        
        if has_assumptions and has_risks:
            # Bonus if they have content
            if len(assumptions) > 0 and len(risks) > 0:
                return 1.0
            elif len(assumptions) > 0 or len(risks) > 0:
                return 0.8
            else:
                return 0.6
        elif has_assumptions or has_risks:
            return 0.5
        else:
            return 0.3


# Add custom evaluators to dataset
architecture_dataset.add_evaluator(StepCountEvaluator())
architecture_dataset.add_evaluator(StepCompletenessEvaluator())
architecture_dataset.add_evaluator(AssumptionsRisksEvaluator())


async def run_architecture_agent(inputs: QuestionnaireFinal) -> ArchitecturePlan:
    """
    Task function for pydantic-evals.
    
    This function is called by the evaluation framework to test the agent.
    Note: The agent returns (ArchitecturePlan, str), but we only evaluate the plan.
    """
    agent = ArchitectureAgent()
    plan, _ = await agent.run(inputs)
    return plan


if __name__ == "__main__":
    # Run evaluation
    report = architecture_dataset.evaluate_sync(run_architecture_agent)
    report.print(include_input=True, include_output=True, include_durations=False)

