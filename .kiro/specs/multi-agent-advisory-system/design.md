# Design Document

## Overview

The Multi-Agent Corporate Formation Advisory System is a full-stack application that coordinates three specialist AI agents to provide unified business formation advice. The system consists of a React frontend for user interaction and a Python backend powered by Google's Agent Development Kit (ADK) that orchestrates parallel agent consultation and synthesizes recommendations.

The architecture follows a hub-and-spoke pattern where a coordinator agent manages three specialist agents (Tax CPA, Legal Attorney, Business Strategist), each powered by Gemini 2.5 Flash for fast inference.

## Architecture

### High-Level Architecture

```
┌─────────┐      HTTPS      ┌──────────────┐      ADK       ┌─────────────┐
│  User   │ ◄──────────────► │ React + Vite │ ◄────────────► │ ADK Server  │
│ Browser │                  │   Frontend   │                │  (Python)   │
└─────────┘                  └──────────────┘                └──────┬──────┘
                                                                     │
                                                                     ▼
                                                            ┌────────────────┐
                                                            │  Coordinator   │
                                                            │     Agent      │
                                                            └────────┬───────┘
                                                                     │
                                    ┌────────────────────────────────┼────────────────────────┐
                                    │                                │                        │
                                    ▼                                ▼                        ▼
                            ┌───────────────┐              ┌─────────────────┐      ┌──────────────────┐
                            │   Tax CPA     │              │ Legal Attorney  │      │    Business      │
                            │     Agent     │              │      Agent      │      │  Strategist      │
                            └───────────────┘              └─────────────────┘      │      Agent       │
                                                                                     └──────────────────┘
```

### Technology Stack

**Frontend:**
- React 18+ with TypeScript
- Vite for build tooling and dev server
- Axios or Fetch API for HTTP communication
- CSS modules or Tailwind CSS for styling

**Backend:**
- Python 3.10+
- Google Agent Development Kit (ADK)
- Gemini 2.5 Flash (gemini-flash-latest)
- FastAPI or Flask for HTTP server
- Uvicorn for ASGI server

### Component Interaction Flow

1. User submits query through React UI
2. Frontend sends POST request to `/api/consult` endpoint
3. ADK Server receives request and passes to Coordinator Agent
4. Coordinator Agent delegates to three specialist agents in parallel
5. Each specialist agent analyzes the query from their domain perspective
6. Coordinator Agent collects responses and identifies conflicts
7. Coordinator Agent synthesizes unified recommendation
8. ADK Server returns structured JSON response
9. Frontend displays formatted recommendation to user

## Components and Interfaces

### Frontend Components

#### 1. QueryInput Component
**Purpose:** Capture user's business formation question

**Props:**
- `onSubmit: (query: string) => void`
- `isLoading: boolean`

**State:**
- `queryText: string`

**Behavior:**
- Provides textarea for multi-line input
- Validates non-empty input before submission
- Disables submit button during loading state
- Clears input after successful submission

#### 2. RecommendationDisplay Component
**Purpose:** Display the unified recommendation from the coordinator

**Props:**
- `recommendation: RecommendationResponse | null`
- `isLoading: boolean`

**Interface:**
```typescript
interface RecommendationResponse {
  recommendedStructure: string;
  keyBenefits: string[];
  tradeOffs: string[];
  nextSteps: string[];
  conflicts?: ConflictDetail[];
}

interface ConflictDetail {
  area: string;
  description: string;
  resolution: string;
}
```

**Behavior:**
- Shows loading spinner while waiting for response
- Renders structured sections for entity type, benefits, trade-offs, next steps
- Highlights conflicts in a dedicated section
- Provides clear visual hierarchy

#### 3. ClarificationDialog Component
**Purpose:** Handle follow-up questions from the coordinator

**Props:**
- `question: string`
- `onAnswer: (answer: string) => void`
- `isOpen: boolean`

**Behavior:**
- Displays as modal overlay
- Shows coordinator's clarifying question
- Captures user's response
- Sends response back to backend

#### 4. App Component
**Purpose:** Main application container and state management

**State:**
- `currentQuery: string`
- `recommendation: RecommendationResponse | null`
- `isLoading: boolean`
- `error: string | null`
- `clarificationNeeded: boolean`
- `clarificationQuestion: string`

**Methods:**
- `handleQuerySubmit(query: string): Promise<void>`
- `handleClarificationResponse(answer: string): Promise<void>`
- `handleError(error: Error): void`

### Backend Components

#### 1. Agent Definitions Module (`agents.py`)
**Purpose:** Define all four agents with their instructions and configurations

**Exports:**
- `tax_agent: Agent`
- `legal_agent: Agent`
- `strategy_agent: Agent`
- `root_agent: Agent` (coordinator)

**Agent Configuration:**
```python
Agent(
    name: str,
    model: str,  # "gemini-flash-latest"
    description: str,
    instruction: str,
    sub_agents: List[Agent] = []
)
```

**Design Decision:** Each agent has domain-specific instructions that guide their analysis. The coordinator's instructions include the workflow and response format template.

#### 2. API Server Module (`server.py`)
**Purpose:** Expose HTTP endpoints for frontend communication

**Endpoints:**

**POST /api/consult**
- Request Body: `{ "query": string, "context": object }`
- Response: `RecommendationResponse`
- Status Codes: 200 (success), 400 (invalid input), 500 (server error)

**GET /api/health**
- Response: `{ "status": "healthy", "agents": ["TaxCPA", "CorporateAttorney", "BusinessStrategist", "Coordinator"] }`
- Status Codes: 200 (success)

**Implementation:**
```python
@app.post("/api/consult")
async def consult(request: ConsultRequest):
    try:
        # Initialize ADK session
        response = root_agent.run(request.query, context=request.context)
        
        # Parse and structure response
        structured_response = parse_agent_response(response)
        
        return structured_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### 3. Response Parser Module (`parser.py`)
**Purpose:** Convert coordinator agent's text response into structured JSON

**Functions:**
- `parse_agent_response(text: str) -> RecommendationResponse`
- `extract_section(text: str, section_name: str) -> List[str]`
- `identify_conflicts(text: str) -> List[ConflictDetail]`

**Design Decision:** The coordinator agent outputs in a predictable format, making regex-based parsing reliable. Fallback to LLM-based parsing if format deviates.

#### 4. Context Manager Module (`context.py`)
**Purpose:** Manage conversation context and clarification flow

**Classes:**
```python
class ConversationContext:
    session_id: str
    query_history: List[str]
    clarifications: Dict[str, str]
    
    def add_clarification(self, question: str, answer: str)
    def get_full_context(self) -> str
```

**Design Decision:** Maintain session state to support multi-turn clarification without losing original query context.

## Data Models

### Frontend Data Models

```typescript
// Request payload sent to backend
interface ConsultRequest {
  query: string;
  context?: {
    sessionId?: string;
    clarifications?: Record<string, string>;
  };
}

// Response received from backend
interface RecommendationResponse {
  recommendedStructure: string;
  keyBenefits: string[];
  tradeOffs: string[];
  nextSteps: string[];
  conflicts?: ConflictDetail[];
  needsClarification?: boolean;
  clarificationQuestion?: string;
}

interface ConflictDetail {
  area: string;
  description: string;
  resolution: string;
}
```

### Backend Data Models

```python
from pydantic import BaseModel
from typing import List, Optional, Dict

class ConsultRequest(BaseModel):
    query: str
    context: Optional[Dict[str, any]] = None

class ConflictDetail(BaseModel):
    area: str
    description: str
    resolution: str

class RecommendationResponse(BaseModel):
    recommended_structure: str
    key_benefits: List[str]
    trade_offs: List[str]
    next_steps: List[str]
    conflicts: Optional[List[ConflictDetail]] = None
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
```

## Error Handling

### Frontend Error Handling

**Network Errors:**
- Display user-friendly message: "Unable to connect to advisory service"
- Provide retry button
- Log error details to console

**Validation Errors:**
- Show inline validation messages
- Prevent submission of empty queries
- Highlight required fields

**Server Errors (5xx):**
- Display: "Service temporarily unavailable. Please try again."
- Offer option to save query for later

**Client Errors (4xx):**
- Parse error message from server
- Display specific guidance (e.g., "Please provide more details about your business")

### Backend Error Handling

**Agent Execution Errors:**
```python
try:
    response = root_agent.run(query)
except AgentTimeoutError:
    return JSONResponse(
        status_code=504,
        content={"error": "Analysis taking longer than expected. Please try again."}
    )
except AgentExecutionError as e:
    logger.error(f"Agent execution failed: {e}")
    return JSONResponse(
        status_code=500,
        content={"error": "Unable to complete analysis. Please contact support."}
    )
```

**Input Validation:**
- Reject queries shorter than 10 characters
- Reject queries longer than 5000 characters
- Sanitize input to prevent injection attacks

**Rate Limiting:**
- Implement per-IP rate limiting (10 requests per minute)
- Return 429 status code when limit exceeded

**Graceful Degradation:**
- If one specialist agent fails, coordinator should still synthesize from available agents
- Mark response as "partial analysis" when not all agents respond

## Testing Strategy

### Frontend Testing

**Unit Tests (Vitest + React Testing Library):**
- Test QueryInput component validation logic
- Test RecommendationDisplay component rendering with various data shapes
- Test ClarificationDialog modal behavior
- Test API client error handling

**Integration Tests:**
- Test full user flow from query submission to recommendation display
- Test clarification flow with mock backend responses
- Test error state handling

**E2E Tests (Playwright):**
- Test complete user journey: submit query → receive recommendation
- Test clarification flow
- Test error recovery

### Backend Testing

**Unit Tests (pytest):**
- Test response parser with various coordinator outputs
- Test context manager session handling
- Test input validation logic
- Test error handling for each endpoint

**Integration Tests:**
- Test agent initialization and configuration
- Test coordinator agent workflow with mock specialist responses
- Test API endpoints with real ADK agents (using test mode)

**Agent Behavior Tests:**
- Verify each specialist agent produces domain-appropriate responses
- Verify coordinator identifies conflicts correctly
- Verify response format consistency

**Load Tests (Locust):**
- Test system under concurrent user load
- Measure response times for parallel agent execution
- Identify bottlenecks in agent orchestration

### Testing Priorities

1. **Critical Path:** Query submission → coordinator orchestration → unified response
2. **Error Handling:** Network failures, agent timeouts, invalid inputs
3. **Response Quality:** Verify coordinator synthesizes correctly and identifies conflicts
4. **Performance:** Ensure parallel agent execution completes within acceptable time (< 10 seconds)

## Design Decisions and Rationales

### 1. Parallel Agent Execution
**Decision:** Execute all three specialist agents in parallel rather than sequentially

**Rationale:** Reduces total response time from ~15 seconds (3 agents × 5 seconds) to ~5 seconds. ADK supports parallel execution natively.

### 2. Coordinator as Root Agent
**Decision:** Make coordinator the root agent with specialists as sub-agents

**Rationale:** Leverages ADK's built-in orchestration capabilities. Coordinator can delegate to sub-agents using ADK's agent calling mechanism.

### 3. Structured Response Format
**Decision:** Enforce a specific response template in coordinator instructions

**Rationale:** Makes parsing reliable and ensures consistent UX. Template includes all required sections (benefits, trade-offs, next steps).

### 4. Stateless API Design
**Decision:** Each request is self-contained; session state managed client-side

**Rationale:** Simplifies backend scaling. For clarification flow, frontend maintains context and sends full history with each request.

### 5. Gemini Flash Model
**Decision:** Use Gemini 2.5 Flash for all agents

**Rationale:** Balances cost and performance. Flash model provides fast inference (<2 seconds per agent) at lower cost than Pro model. Sufficient for advisory use case.

### 6. Single-Page Application
**Decision:** Build frontend as SPA with no routing

**Rationale:** Simple user flow doesn't require multiple pages. Keeps implementation minimal and focused.

### 7. No Database Persistence
**Decision:** Don't persist queries or recommendations

**Rationale:** MVP focuses on core functionality. Users can copy/paste recommendations. Future enhancement can add history.

## Security Considerations

1. **Input Sanitization:** Validate and sanitize all user inputs to prevent injection attacks
2. **Rate Limiting:** Prevent abuse through per-IP rate limiting
3. **HTTPS Only:** Enforce HTTPS for all frontend-backend communication
4. **API Key Management:** Store Google ADK API keys in environment variables, never in code
5. **CORS Configuration:** Restrict CORS to specific frontend origin in production
6. **Error Message Sanitization:** Don't expose internal error details to users

## Performance Considerations

1. **Parallel Execution:** Leverage ADK's parallel agent execution to minimize latency
2. **Response Streaming:** Consider streaming coordinator response as it's generated
3. **Caching:** Cache common queries and responses (future enhancement)
4. **Connection Pooling:** Reuse HTTP connections between frontend and backend
5. **Agent Warm-up:** Keep agents initialized to avoid cold start delays

## Deployment Architecture

**Frontend:**
- Deploy to Vercel or Netlify
- Static site hosting with CDN
- Environment variable for API endpoint URL

**Backend:**
- Deploy to Google Cloud Run or AWS Lambda
- Containerized Python application
- Auto-scaling based on request volume
- Environment variables for ADK API keys

**CI/CD:**
- GitHub Actions for automated testing and deployment
- Separate staging and production environments
- Automated tests must pass before deployment
