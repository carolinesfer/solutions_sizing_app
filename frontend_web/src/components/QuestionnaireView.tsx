import React from 'react';

interface QuestionnaireViewProps {
  questionnaire: {
    qas: Array<{ id: string; answer: any }>;
    answered_pct: number;
    gaps: string[];
  };
}

export const QuestionnaireView: React.FC<QuestionnaireViewProps> = ({ questionnaire }) => {
  const handleDownload = () => {
    const dataStr = JSON.stringify(questionnaire, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'questionnaire.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold">Final Questionnaire</h2>
        <button
          onClick={handleDownload}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Download JSON
        </button>
      </div>

      <div className="mb-4">
        <p className="text-sm text-gray-600">
          Answered: {Math.round(questionnaire.answered_pct * 100)}%
        </p>
        {questionnaire.gaps.length > 0 && (
          <p className="text-sm text-yellow-600 mt-1">
            Unanswered questions: {questionnaire.gaps.join(', ')}
          </p>
        )}
      </div>

      <div className="space-y-4">
        {questionnaire.qas.map((qa) => (
          <div key={qa.id} className="border-b border-gray-200 pb-4 last:border-b-0">
            <p className="font-medium text-gray-900 mb-1">Question {qa.id}</p>
            <p className="text-gray-600 mb-2">Answer: {String(qa.answer)}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

