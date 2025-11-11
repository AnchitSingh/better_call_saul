import { useState } from 'react';
import './ClarificationDialog.css';

interface ClarificationDialogProps {
  question: string;
  onAnswer: (answer: string) => void;
  isOpen: boolean;
}

export function ClarificationDialog({ question, onAnswer, isOpen }: ClarificationDialogProps) {
  const [answer, setAnswer] = useState('');

  if (!isOpen) {
    return null;
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (answer.trim()) {
      onAnswer(answer.trim());
      setAnswer('');
    }
  };

  return (
    <div className="dialog-backdrop">
      <div className="dialog-container">
        <div className="dialog-header">
          <h3>Additional Information Needed</h3>
        </div>
        
        <div className="dialog-body">
          <p className="dialog-question">{question}</p>
          
          <form onSubmit={handleSubmit}>
            <textarea
              className="dialog-textarea"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Enter your response..."
              rows={4}
              autoFocus
            />
            
            <div className="dialog-actions">
              <button
                type="submit"
                className="dialog-submit"
                disabled={!answer.trim()}
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
