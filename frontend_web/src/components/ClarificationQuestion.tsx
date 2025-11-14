import React, { useState } from 'react';

interface Question {
  id: string;
  text: string;
  type: string;
  options?: string[];
  required: boolean;
  rationale?: string;
}

interface ClarificationQuestionProps {
  question: Question;
  onSubmit: (answer: any) => void;
  loading?: boolean;
}

export const ClarificationQuestion: React.FC<ClarificationQuestionProps> = ({
  question,
  onSubmit,
  loading = false,
}) => {
  const [answer, setAnswer] = useState<any>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (answer) {
      onSubmit(answer);
      setAnswer('');
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
      <h3 className="text-lg font-semibold mb-4">Clarification Question</h3>
      <p className="text-gray-700 mb-4">{question.text}</p>
      {question.rationale && (
        <p className="text-sm text-gray-500 mb-4 italic">{question.rationale}</p>
      )}

      <form onSubmit={handleSubmit}>
        {question.type === 'single_select' && question.options ? (
          <div className="space-y-2 mb-4">
            {question.options.map((option) => (
              <label key={option} className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="radio"
                  name="answer"
                  value={option}
                  checked={answer === option}
                  onChange={(e) => setAnswer(e.target.value)}
                  className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        ) : question.type === 'boolean' ? (
          <div className="space-y-2 mb-4">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="answer"
                value="true"
                checked={answer === 'true'}
                onChange={(e) => setAnswer(e.target.value === 'true')}
                className="w-4 h-4 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-gray-700">Yes</span>
            </label>
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="answer"
                value="false"
                checked={answer === 'false'}
                onChange={(e) => setAnswer(e.target.value === 'false')}
                className="w-4 h-4 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-gray-700">No</span>
            </label>
          </div>
        ) : (
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 mb-4"
            placeholder="Enter your answer..."
          />
        )}

        <button
          type="submit"
          disabled={loading || !answer}
          className="w-full bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'Submitting...' : 'Submit Answer'}
        </button>
      </form>
    </div>
  );
};

