export interface StartWorkflowRequest {
  paragraph: string;
  transcript?: string | null;
  use_case_title: string;
}

export interface StartWorkflowResponse {
  workflow_id: string;
  state: string;
}

export interface WorkflowStateResponse {
  workflow_id: string;
  state: string;
  current_question?: {
    id: string;
    text: string;
    type: string;
    options?: string[];
    required: boolean;
    rationale?: string;
  } | null;
  progress?: {
    state: string;
  } | null;
}

export interface ClarificationAnswerRequest {
  question_id: string;
  answer: any;
}

export interface ClarificationAnswerResponse {
  workflow_id: string;
  state: string;
  next_question?: {
    id: string;
    text: string;
    type: string;
    options?: string[];
    required: boolean;
    rationale?: string;
  } | null;
  completed: boolean;
}

export interface WorkflowResultsResponse {
  workflow_id: string;
  questionnaire_final: {
    qas: Array<{ id: string; answer: any }>;
    answered_pct: number;
    gaps: string[];
  };
  architecture_plan: {
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
  architecture_markdown: string;
}

