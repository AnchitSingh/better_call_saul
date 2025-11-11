import type { RecommendationResponse } from '../types';
import './RecommendationDisplay.css';

interface RecommendationDisplayProps {
  recommendation: RecommendationResponse | null;
  isLoading: boolean;
}

export function RecommendationDisplay({ recommendation, isLoading }: RecommendationDisplayProps) {
  if (isLoading) {
    return (
      <div className="recommendation-loading">
        <div className="spinner"></div>
        <p>Consulting with tax, legal, and business strategy experts...</p>
      </div>
    );
  }

  if (!recommendation) {
    return null;
  }

  return (
    <div className="recommendation-display">
      <div className="recommendation-card primary">
        <h2>Recommended Structure</h2>
        <p className="highlight">{recommendation.recommendedStructure}</p>
      </div>

      <div className="recommendation-card">
        <h3>Key Benefits</h3>
        <ul className="benefits-list">
          {recommendation.keyBenefits.map((benefit, index) => (
            <li key={index}>{benefit}</li>
          ))}
        </ul>
      </div>

      <div className="recommendation-card">
        <h3>Trade-offs</h3>
        <ul className="tradeoffs-list">
          {recommendation.tradeOffs.map((tradeOff, index) => (
            <li key={index}>{tradeOff}</li>
          ))}
        </ul>
      </div>

      {recommendation.conflicts && recommendation.conflicts.length > 0 && (
        <div className="recommendation-card conflicts">
          <h3>⚠️ Areas of Consideration</h3>
          <div className="conflicts-container">
            {recommendation.conflicts.map((conflict, index) => (
              <div key={index} className="conflict-item">
                <h4>{conflict.area}</h4>
                <p>{conflict.description}</p>
                <p><strong>Resolution:</strong> {conflict.resolution}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="recommendation-card">
        <h3>Next Steps</h3>
        <ol className="steps-list">
          {recommendation.nextSteps.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ol>
      </div>
    </div>
  );
}
