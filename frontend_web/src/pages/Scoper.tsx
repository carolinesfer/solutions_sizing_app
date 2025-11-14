import React, { useState, useEffect } from 'react';
import { startScoping, getWorkflowState, submitClarification, getResults } from '@/api/scoper';
import type { StartWorkflowRequest, WorkflowStateResponse, WorkflowResultsResponse } from '@/api/scoper/types';
import { ScoperWorkflow } from '@/components/ScoperWorkflow';
import { ClarificationQuestion } from '@/components/ClarificationQuestion';
import { QuestionnaireView } from '@/components/QuestionnaireView';
import { ArchitecturePlanView } from '@/components/ArchitecturePlanView';

type WorkflowPhase = 'input' | 'processing' | 'clarification' | 'results';

export const Scoper: React.FC = () => {
  const [phase, setPhase] = useState<WorkflowPhase>('input');
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [workflowState, setWorkflowState] = useState<WorkflowStateResponse | null>(null);
  const [results, setResults] = useState<WorkflowResultsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [inputData, setInputData] = useState<StartWorkflowRequest>({
    paragraph: '',
    transcript: '',
    use_case_title: '',
  });

  const handleStart = async () => {
    if (!inputData.paragraph || !inputData.use_case_title) {
      setError('Please provide a paragraph and use case title');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await startScoping(inputData);
      setWorkflowId(response.workflow_id);
      setPhase('processing');

      // Poll for state updates
      await pollWorkflowState(response.workflow_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to start workflow');
      setLoading(false);
    }
  };

  const pollWorkflowState = async (id: string) => {
    try {
      const state = await getWorkflowState(id);
      setWorkflowState(state);

      if (state.state === 'Q_CLARIFY') {
        setPhase('clarification');
        setLoading(false);
      } else if (state.state === 'DONE') {
        await loadResults(id);
      } else {
        // Continue polling
        setTimeout(() => pollWorkflowState(id), 2000);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to get workflow state');
      setLoading(false);
    }
  };

  const handleClarificationAnswer = async (questionId: string, answer: any) => {
    if (!workflowId) return;

    setLoading(true);
    setError(null);

    try {
      const response = await submitClarification(workflowId, {
        question_id: questionId,
        answer,
      });

      if (response.completed) {
        setPhase('processing');
        await pollWorkflowState(workflowId);
      } else {
        setWorkflowState({
          ...workflowState!,
          current_question: response.next_question || null,
        });
        setLoading(false);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to submit answer');
      setLoading(false);
    }
  };

  const loadResults = async (id: string) => {
    try {
      const workflowResults = await getResults(id);
      setResults(workflowResults);
      setPhase('results');
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to load results');
      setLoading(false);
    }
  };

  if (phase === 'input') {
    return (
      <div className="container mx-auto p-6 max-w-4xl">
        <h1 className="text-3xl font-bold mb-6">Agentic Professional Services Scoper</h1>
        <p className="text-gray-600 mb-6">
          Enter your use case description to generate a tailored questionnaire and solution architecture plan.
        </p>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Use Case Title *
            </label>
            <input
              type="text"
              value={inputData.use_case_title}
              onChange={(e) => setInputData({ ...inputData, use_case_title: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Customer Churn Prediction"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Use Case Description *
            </label>
            <textarea
              value={inputData.paragraph}
              onChange={(e) => setInputData({ ...inputData, paragraph: e.target.value })}
              rows={8}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Describe your use case, requirements, and goals..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Call Transcript (Optional)
            </label>
            <textarea
              value={inputData.transcript || ''}
              onChange={(e) => setInputData({ ...inputData, transcript: e.target.value })}
              rows={6}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Paste call transcript if available..."
            />
          </div>

          <button
            onClick={handleStart}
            disabled={loading || !inputData.paragraph || !inputData.use_case_title}
            className="w-full bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Starting...' : 'Start Scoping'}
          </button>
        </div>
      </div>
    );
  }

  if (phase === 'processing') {
    return (
      <div className="container mx-auto p-6 max-w-4xl">
        <ScoperWorkflow state={workflowState?.state || 'PROCESSING'} />
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mt-4">
            {error}
          </div>
        )}
      </div>
    );
  }

  if (phase === 'clarification' && workflowState?.current_question) {
    return (
      <div className="container mx-auto p-6 max-w-4xl">
        <ScoperWorkflow state={workflowState.state} />
        <ClarificationQuestion
          question={workflowState.current_question}
          onSubmit={(answer) => handleClarificationAnswer(workflowState.current_question!.id, answer)}
          loading={loading}
        />
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mt-4">
            {error}
          </div>
        )}
      </div>
    );
  }

  if (phase === 'results' && results) {
    return (
      <div className="container mx-auto p-6 max-w-4xl">
        <h1 className="text-3xl font-bold mb-6">Scoping Results</h1>
        <div className="space-y-8">
          <QuestionnaireView questionnaire={results.questionnaire_final} />
          <ArchitecturePlanView
            plan={results.architecture_plan}
            markdown={results.architecture_markdown}
          />
        </div>
      </div>
    );
  }

  return null;
};

