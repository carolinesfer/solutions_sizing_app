import React from 'react';

interface ScoperWorkflowProps {
  state: string;
}

const stateLabels: Record<string, string> = {
  INGEST: 'Receiving Input',
  ANALYZE: 'Analyzing Requirements',
  ROUTE: 'Routing to Domain',
  KB_FETCH: 'Fetching Knowledge Base',
  Q_DRAFT: 'Drafting Questionnaire',
  Q_CLARIFY: 'Clarification',
  Q_FREEZE: 'Validating Questionnaire',
  PLAN_ARCH: 'Generating Architecture',
  DONE: 'Complete',
  PROCESSING: 'Processing...',
};

const stateSteps = [
  'INGEST',
  'ANALYZE',
  'ROUTE',
  'KB_FETCH',
  'Q_DRAFT',
  'Q_CLARIFY',
  'Q_FREEZE',
  'PLAN_ARCH',
  'DONE',
];

export const ScoperWorkflow: React.FC<ScoperWorkflowProps> = ({ state }) => {
  const currentIndex = stateSteps.indexOf(state);
  const progress = currentIndex >= 0 ? ((currentIndex + 1) / stateSteps.length) * 100 : 0;

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-4">Workflow Progress</h2>
      <div className="mb-2">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            {stateLabels[state] || state}
          </span>
          <span className="text-sm text-gray-500">{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>
      <div className="flex justify-between text-xs text-gray-500 mt-2">
        {stateSteps.slice(0, 5).map((step) => (
          <span
            key={step}
            className={stateSteps.indexOf(state) >= stateSteps.indexOf(step) ? 'text-blue-600' : ''}
          >
            {step}
          </span>
        ))}
      </div>
    </div>
  );
};

