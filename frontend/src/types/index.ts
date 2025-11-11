// Request payload sent to backend
export interface ConsultRequest {
  query: string;
  context?: {
    sessionId?: string;
    clarifications?: Record<string, string>;
  };
}

// Conflict detail structure
export interface ConflictDetail {
  area: string;
  description: string;
  resolution: string;
}

// Response received from backend
export interface RecommendationResponse {
  recommendedStructure: string;
  keyBenefits: string[];
  tradeOffs: string[];
  nextSteps: string[];
  conflicts?: ConflictDetail[];
  needsClarification?: boolean;
  clarificationQuestion?: string;
}
