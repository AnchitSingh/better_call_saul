import { useState } from 'react';
import { QueryInput } from './components/QueryInput';
import { RecommendationDisplay } from './components/RecommendationDisplay';
import { ClarificationDialog } from './components/ClarificationDialog';
import { submitQuery, ApiError } from './api/client';
import type { RecommendationResponse } from './types';
import './App.css';

function App() {
  const [currentQuery, setCurrentQuery] = useState('');
  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [clarificationNeeded, setClarificationNeeded] = useState(false);
  const [clarificationQuestion, setClarificationQuestion] = useState('');
  const [sessionId] = useState(() => `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  const [clarifications, setClarifications] = useState<Record<string, string>>({});

  const handleQuerySubmit = async (query: string) => {
    setCurrentQuery(query);
    setIsLoading(true);
    setError(null);
    setRecommendation(null);

    try {
      const response = await submitQuery(query, {
        sessionId,
        clarifications: Object.keys(clarifications).length > 0 ? clarifications : undefined,
      });

      if (response.needsClarification && response.clarificationQuestion) {
        setClarificationQuestion(response.clarificationQuestion);
        setClarificationNeeded(true);
      } else {
        setRecommendation(response);
      }
    } catch (err) {
      handleError(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClarificationResponse = async (answer: string) => {
    setClarificationNeeded(false);
    setIsLoading(true);
    setError(null);

    const updatedClarifications = {
      ...clarifications,
      [clarificationQuestion]: answer,
    };
    setClarifications(updatedClarifications);

    try {
      const response = await submitQuery(currentQuery, {
        sessionId,
        clarifications: updatedClarifications,
      });

      if (response.needsClarification && response.clarificationQuestion) {
        setClarificationQuestion(response.clarificationQuestion);
        setClarificationNeeded(true);
      } else {
        setRecommendation(response);
      }
    } catch (err) {
      handleError(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleError = (err: unknown) => {
    if (err instanceof ApiError) {
      setError(err.message);
    } else if (err instanceof Error) {
      setError(err.message);
    } else {
      setError('An unexpected error occurred. Please try again.');
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">Business Formation Advisor</h1>
        <p className="app-subtitle">
          Get coordinated advice from tax, legal, and business strategy experts
        </p>
      </header>

      <main className="app-main">
        <QueryInput onSubmit={handleQuerySubmit} isLoading={isLoading} />

        {error && (
          <div className="app-error">
            <p className="app-error-message">{error}</p>
            <button
              className="app-error-retry"
              onClick={() => {
                setError(null);
                if (currentQuery) {
                  handleQuerySubmit(currentQuery);
                }
              }}
            >
              Try Again
            </button>
          </div>
        )}

        <RecommendationDisplay recommendation={recommendation} isLoading={isLoading} />
      </main>

      <ClarificationDialog
        question={clarificationQuestion}
        onAnswer={handleClarificationResponse}
        isOpen={clarificationNeeded}
      />
    </div>
  );
}

export default App;
