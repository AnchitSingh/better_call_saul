import type { ConsultRequest, RecommendationResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export class ApiError extends Error {
  statusCode?: number;
  details?: unknown;
  
  constructor(
    message: string,
    statusCode?: number,
    details?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
    this.details = details;
  }
}

export async function submitQuery(
  query: string,
  context?: ConsultRequest['context']
): Promise<RecommendationResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/consult`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, context }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.error || `HTTP error ${response.status}`,
        response.status,
        errorData
      );
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ApiError('Unable to connect to advisory service. Please check your connection.');
    }
    
    throw new ApiError('An unexpected error occurred. Please try again.');
  }
}
