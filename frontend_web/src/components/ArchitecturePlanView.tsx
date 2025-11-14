import React from 'react';
import ReactMarkdown from 'react-markdown';

interface ArchitecturePlanViewProps {
  plan: {
    steps: Array<{
      id: string;
      name: string;
      purpose: string;
      inputs: string;
      outputs: string;
    }>;
    assumptions: string[];
    risks: string[];
    notes?: string;
  };
  markdown: string;
}

export const ArchitecturePlanView: React.FC<ArchitecturePlanViewProps> = ({ plan, markdown }) => {
  const handleDownload = () => {
    const dataBlob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'architecture_plan.md';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold">Solution Architecture Plan</h2>
        <button
          onClick={handleDownload}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Download Markdown
        </button>
      </div>

      <div className="prose max-w-none mb-6">
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </div>

      <div className="mt-6 space-y-4">
        <div>
          <h3 className="text-lg font-semibold mb-2">Steps ({plan.steps.length})</h3>
          <div className="space-y-3">
            {plan.steps.map((step) => (
              <div key={step.id} className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-medium">{step.name}</h4>
                <p className="text-sm text-gray-600">{step.purpose}</p>
                <div className="mt-2 text-xs text-gray-500">
                  <p><strong>Inputs:</strong> {step.inputs}</p>
                  <p><strong>Outputs:</strong> {step.outputs}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {plan.assumptions.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold mb-2">Assumptions</h3>
            <ul className="list-disc list-inside space-y-1">
              {plan.assumptions.map((assumption, idx) => (
                <li key={idx} className="text-gray-700">{assumption}</li>
              ))}
            </ul>
          </div>
        )}

        {plan.risks.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold mb-2">Risks</h3>
            <ul className="list-disc list-inside space-y-1">
              {plan.risks.map((risk, idx) => (
                <li key={idx} className="text-gray-700">{risk}</li>
              ))}
            </ul>
          </div>
        )}

        {plan.notes && (
          <div>
            <h3 className="text-lg font-semibold mb-2">Notes</h3>
            <p className="text-gray-700">{plan.notes}</p>
          </div>
        )}
      </div>
    </div>
  );
};

