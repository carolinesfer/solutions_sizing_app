import apiClient from '../apiClient';
import type {
  StartWorkflowRequest,
  StartWorkflowResponse,
  WorkflowStateResponse,
  ClarificationAnswerRequest,
  ClarificationAnswerResponse,
  WorkflowResultsResponse,
} from './types';

/**
 * Start a new scoping workflow.
 */
export async function startScoping(
  request: StartWorkflowRequest
): Promise<StartWorkflowResponse> {
  const response = await apiClient.post<StartWorkflowResponse>('v1/scoper/start', request);
  return response.data;
}

/**
 * Get the current state of a workflow.
 */
export async function getWorkflowState(
  workflowId: string
): Promise<WorkflowStateResponse> {
  const response = await apiClient.get<WorkflowStateResponse>(
    `v1/scoper/${workflowId}/state`
  );
  return response.data;
}

/**
 * Submit a clarification answer and get the next question.
 */
export async function submitClarification(
  workflowId: string,
  answer: ClarificationAnswerRequest
): Promise<ClarificationAnswerResponse> {
  const response = await apiClient.post<ClarificationAnswerResponse>(
    `v1/scoper/${workflowId}/clarify`,
    answer
  );
  return response.data;
}

/**
 * Get the final results of a completed workflow.
 */
export async function getResults(workflowId: string): Promise<WorkflowResultsResponse> {
  const response = await apiClient.get<WorkflowResultsResponse>(
    `v1/scoper/${workflowId}/results`
  );
  return response.data;
}

