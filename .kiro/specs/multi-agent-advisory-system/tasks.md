# Implementation Plan

- [x] 1. Set up project structure and initialize both frontend and backend
  - Create root directory structure with separate `frontend/` and `backend/` folders
  - Initialize React + Vite project in `frontend/` with TypeScript template
  - Initialize Python project in `backend/` with virtual environment and requirements.txt
  - Create `.gitignore` files for both frontend (node_modules, dist) and backend (venv, __pycache__)
  - Set up environment variable templates (.env.example) for both layers
  - _Requirements: 5.1, 7.1_

- [x] 2. Implement backend ADK agent system
- [x] 2.1 Create agent definitions module
  - Write `backend/agents.py` with all four agent definitions (Tax CPA, Legal Attorney, Business Strategist, Coordinator)
  - Configure each agent with Gemini Flash model and domain-specific instructions
  - Set up coordinator agent as root agent with three sub-agents
  - Include the structured response format template in coordinator instructions
  - _Requirements: 5.1, 5.2, 5.3, 2.2, 2.3, 2.4_

- [x] 2.2 Create API server with consultation endpoint
  - Write `backend/server.py` using FastAPI framework
  - Implement POST `/api/consult` endpoint that accepts query and optional context
  - Implement GET `/api/health` endpoint for service monitoring
  - Add CORS middleware configuration for frontend origin
  - Integrate root_agent.run() call in consultation endpoint
  - _Requirements: 5.4, 7.1, 7.2, 7.3_

- [x] 2.3 Implement response parser module
  - Write `backend/parser.py` with functions to parse coordinator text output
  - Implement `parse_agent_response()` to extract recommended structure, benefits, trade-offs, next steps
  - Implement `identify_conflicts()` to detect and structure conflict information
  - Add regex patterns for section extraction based on coordinator's output format
  - Handle parsing errors gracefully with fallback values
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 3.2, 3.3_

- [x] 2.4 Add input validation and error handling
  - Implement request validation in server.py (query length, required fields)
  - Add try-catch blocks for agent execution errors
  - Implement error response formatting with appropriate HTTP status codes
  - Add logging for debugging agent execution issues
  - _Requirements: 7.5, 5.4_

- [x] 2.5 Create context manager for clarification flow
  - Write `backend/context.py` with ConversationContext class
  - Implement session management for multi-turn clarification
  - Add methods to store and retrieve clarification history
  - Integrate context manager with consultation endpoint
  - _Requirements: 6.1, 6.2, 6.5_

- [ ]* 2.6 Write backend unit tests
  - Create `backend/tests/test_parser.py` to test response parsing logic
  - Create `backend/tests/test_server.py` to test API endpoints with mock agents
  - Create `backend/tests/test_context.py` to test session management
  - Test error handling for various failure scenarios
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 3. Implement frontend React application
- [x] 3.1 Create TypeScript interfaces and types
  - Write `frontend/src/types/index.ts` with all data model interfaces
  - Define ConsultRequest, RecommendationResponse, ConflictDetail types
  - Export types for use across components
  - _Requirements: 7.2_

- [x] 3.2 Create API client module
  - Write `frontend/src/api/client.ts` with HTTP client functions
  - Implement `submitQuery()` function using fetch or axios
  - Add error handling for network failures and HTTP errors
  - Configure base URL from environment variable
  - _Requirements: 1.2, 7.3, 7.4_

- [x] 3.3 Implement QueryInput component
  - Create `frontend/src/components/QueryInput.tsx`
  - Add textarea for multi-line query input
  - Implement validation for non-empty input
  - Add submit button with loading state
  - Style component with clear visual hierarchy
  - _Requirements: 1.1, 6.3_

- [x] 3.4 Implement RecommendationDisplay component
  - Create `frontend/src/components/RecommendationDisplay.tsx`
  - Add sections for recommended structure, benefits, trade-offs, next steps
  - Implement loading spinner for waiting state
  - Add conflict highlighting section when conflicts exist
  - Style with clear visual separation between sections
  - _Requirements: 1.4, 1.5, 3.3, 4.2, 4.3, 4.4_

- [x] 3.5 Implement ClarificationDialog component
  - Create `frontend/src/components/ClarificationDialog.tsx`
  - Build modal overlay for clarification questions
  - Add input field for user's clarification response
  - Implement submit handler to send response back
  - Style as centered modal with backdrop
  - _Requirements: 6.3, 6.4_

- [x] 3.6 Implement main App component with state management
  - Create `frontend/src/App.tsx` as main container
  - Set up state for query, recommendation, loading, error, clarification
  - Implement `handleQuerySubmit()` to call API and update state
  - Implement `handleClarificationResponse()` for follow-up flow
  - Wire up all child components with props and callbacks
  - Add error display for user-friendly error messages
  - _Requirements: 1.2, 1.3, 1.4, 6.4, 7.3, 7.4_

- [x] 3.7 Add styling and responsive design
  - Create global styles or configure Tailwind CSS
  - Ensure responsive layout for mobile and desktop
  - Add loading animations and transitions
  - Style error states with appropriate colors
  - _Requirements: 1.1, 1.3, 1.4, 1.5_

- [ ]* 3.8 Write frontend unit tests
  - Create tests for QueryInput validation logic
  - Create tests for RecommendationDisplay rendering with various data
  - Create tests for ClarificationDialog modal behavior
  - Create tests for API client error handling
  - Use Vitest and React Testing Library
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 6.3, 6.4, 7.3, 7.4_

- [-] 4. Integrate frontend and backend
- [x] 4.1 Configure environment variables
  - Set up `backend/.env` with Google ADK API key
  - Set up `frontend/.env` with backend API URL
  - Document required environment variables in README
  - _Requirements: 5.1, 7.1_

- [x] 4.2 Test end-to-end flow locally
  - Start backend server with uvicorn
  - Start frontend dev server with Vite
  - Submit test query and verify full flow works
  - Test clarification flow if coordinator requests more info
  - Verify error handling for network failures
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 4.5, 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 4.3 Verify parallel agent execution
  - Add logging to backend to track agent execution timing
  - Confirm all three specialist agents execute in parallel
  - Measure total response time (should be ~5 seconds, not ~15 seconds)
  - _Requirements: 2.1, 5.4_

- [ ] 4.4 Test conflict identification
  - Submit queries that should produce conflicting advice (e.g., tax efficiency vs VC funding)
  - Verify coordinator identifies and documents conflicts
  - Verify conflicts display correctly in frontend
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ]* 4.5 Write integration tests
  - Create E2E tests using Playwright for complete user journey
  - Test query submission → recommendation display flow
  - Test clarification flow with mock backend
  - Test error recovery scenarios
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 5. Prepare for deployment
- [x] 5.1 Create Docker configuration for backend
  - Write `backend/Dockerfile` for Python application
  - Create `backend/docker-compose.yml` for local testing
  - Ensure all dependencies are in requirements.txt
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 5.2 Configure frontend build for production
  - Update Vite config for production builds
  - Set up environment variable handling for production API URL
  - Test production build locally
  - _Requirements: 1.1, 7.1_

- [x] 5.3 Create deployment documentation
  - Write README.md with setup instructions for both frontend and backend
  - Document environment variables and their purposes
  - Add instructions for running locally and deploying to cloud
  - Include example queries for testing
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 7.1_

- [x] 5.4 Add rate limiting and security headers
  - Implement rate limiting middleware in FastAPI (10 requests per minute per IP)
  - Add security headers (HSTS, CSP, X-Frame-Options)
  - Configure CORS for production frontend origin only
  - _Requirements: 7.5_
