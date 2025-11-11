import { useState } from 'react';
import './QueryInput.css';

interface QueryInputProps {
  onSubmit: (query: string) => void;
  isLoading: boolean;
}

export function QueryInput({ onSubmit, isLoading }: QueryInputProps) {
  const [queryText, setQueryText] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedQuery = queryText.trim();
    if (!trimmedQuery) {
      setError('Please enter a question');
      return;
    }
    
    setError('');
    onSubmit(trimmedQuery);
    setQueryText('');
  };

  return (
    <form className="query-input" onSubmit={handleSubmit}>
      <div className="query-input-field">
        <label htmlFor="query" className="query-input-label">
          Ask your business formation question
        </label>
        <textarea
          id="query"
          className={`query-input-textarea ${error ? 'error' : ''}`}
          value={queryText}
          onChange={(e) => {
            setQueryText(e.target.value);
            if (error) setError('');
          }}
          placeholder="e.g., I'm starting a tech startup and plan to raise VC funding. Should I form an LLC or C-Corp?"
          rows={4}
          disabled={isLoading}
        />
        {error && <span className="query-input-error">{error}</span>}
      </div>
      <button
        type="submit"
        className="query-input-submit"
        disabled={isLoading || !queryText.trim()}
      >
        {isLoading ? 'Analyzing...' : 'Get Advice'}
      </button>
    </form>
  );
}
