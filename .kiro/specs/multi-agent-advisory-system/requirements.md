# Requirements Document

## Introduction

The Multi-Agent Corporate Formation Advisory System (working name: "Better Call Saul") addresses a critical gap in business consulting: the lack of coordination between tax, legal, and strategic advisors. When entrepreneurs seek guidance on business entity formation (LLC vs S-Corp vs C-Corp), they often receive conflicting or incomplete advice from professionals working in isolation. This system provides a unified, conflict-aware response by coordinating three specialist AI agents (Tax CPA, Corporate Attorney, Business Strategist) through a coordinator agent, all powered by Google's Agent Development Kit (ADK) and Gemini 2.5 Flash.

## Glossary

- **ADK**: Google's Agent Development Kit, the framework used to build and orchestrate AI agents
- **Coordinator Agent**: The orchestration agent that manages parallel consultation with specialist agents and synthesizes unified recommendations
- **Tax CPA Agent**: Specialist agent focused on tax implications, deductions, and fiscal optimization
- **Legal Attorney Agent**: Specialist agent focused on legal compliance, liability protection, and regulatory requirements
- **Business Strategist Agent**: Specialist agent focused on growth strategy, scalability, and operational execution
- **React Frontend**: The user-facing web application built with React and Vite
- **ADK Server**: The backend server that hosts and executes the agent system
- **Unified Response**: A synthesized recommendation that identifies conflicts between specialist advice and presents benefits and trade-offs
- **Entity Type**: Business structure options including LLC, S-Corp, and C-Corp

## Requirements

### Requirement 1

**User Story:** As an entrepreneur, I want to submit my business formation question through a web interface, so that I can receive coordinated advice from multiple professional perspectives

#### Acceptance Criteria

1. THE React Frontend SHALL provide a text input interface for users to submit business formation questions
2. WHEN a user submits a question, THE React Frontend SHALL send the query via HTTPS to the ADK Server
3. THE React Frontend SHALL display a loading state while waiting for the response
4. WHEN the ADK Server returns a response, THE React Frontend SHALL display the unified recommendation to the user
5. THE React Frontend SHALL present the response in a structured format showing recommended entity type, benefits, trade-offs, and next steps

### Requirement 2

**User Story:** As an entrepreneur, I want the system to analyze my question from tax, legal, and strategic perspectives simultaneously, so that I receive comprehensive advice quickly

#### Acceptance Criteria

1. WHEN the Coordinator Agent receives a user query, THE Coordinator Agent SHALL delegate the query to all three specialist agents in parallel
2. THE Tax CPA Agent SHALL analyze tax implications including pass-through vs double taxation, QBI deductions, and payroll tax considerations
3. THE Legal Attorney Agent SHALL assess liability protection, compliance requirements, and ownership flexibility
4. THE Business Strategist Agent SHALL evaluate growth trajectory, scalability, and operational complexity
5. THE Coordinator Agent SHALL wait for all three specialist agents to complete their analysis before proceeding to synthesis

### Requirement 3

**User Story:** As an entrepreneur, I want the system to identify conflicts between different professional perspectives, so that I understand where trade-offs exist

#### Acceptance Criteria

1. WHEN all specialist agents have provided their analysis, THE Coordinator Agent SHALL compare recommendations across tax, legal, and strategic dimensions
2. THE Coordinator Agent SHALL identify conflicts where specialist recommendations diverge
3. THE Coordinator Agent SHALL document specific areas of conflict in the unified response
4. THE Coordinator Agent SHALL explain why conflicts exist between different professional perspectives
5. THE Coordinator Agent SHALL present conflicts as trade-offs rather than contradictions

### Requirement 4

**User Story:** As an entrepreneur, I want to receive a single unified recommendation with clear next steps, so that I can make an informed decision and take action

#### Acceptance Criteria

1. THE Coordinator Agent SHALL synthesize specialist inputs into a single recommended entity type
2. THE Coordinator Agent SHALL provide a minimum of three key benefits for the recommended structure
3. THE Coordinator Agent SHALL provide a minimum of two trade-offs for the recommended structure
4. THE Coordinator Agent SHALL provide a minimum of three actionable next steps
5. THE Unified Response SHALL follow a consistent format with sections for recommended structure, benefits, trade-offs, and next steps

### Requirement 5

**User Story:** As a system administrator, I want the backend to use Google ADK with Gemini 2.5 Flash, so that the system provides fast and cost-effective inference

#### Acceptance Criteria

1. THE ADK Server SHALL initialize four agents using the Google ADK framework
2. THE ADK Server SHALL configure all agents to use the Gemini Flash model
3. THE Coordinator Agent SHALL be designated as the root agent with three sub-agents
4. THE ADK Server SHALL expose an API endpoint that accepts user queries and returns coordinator responses
5. THE ADK Server SHALL handle agent orchestration and parallel execution through the ADK framework

### Requirement 6

**User Story:** As an entrepreneur, I want the system to clarify my business context when needed, so that the advice is tailored to my specific situation

#### Acceptance Criteria

1. WHEN a user query lacks sufficient context, THE Coordinator Agent SHALL request clarifying information
2. THE Coordinator Agent SHALL identify missing information related to business stage, industry, funding plans, or geographic location
3. THE React Frontend SHALL display clarifying questions to the user
4. WHEN the user provides additional context, THE React Frontend SHALL send the updated information to the Coordinator Agent
5. THE Coordinator Agent SHALL incorporate clarifying information into the specialist agent consultation

### Requirement 7

**User Story:** As a developer, I want the frontend and backend to communicate via a well-defined API, so that the system is maintainable and scalable

#### Acceptance Criteria

1. THE ADK Server SHALL expose an HTTP endpoint that accepts POST requests with user queries
2. THE ADK Server SHALL return responses in JSON format with structured recommendation data
3. THE React Frontend SHALL send requests to the ADK Server using HTTPS protocol
4. THE React Frontend SHALL handle error responses from the ADK Server gracefully
5. THE ADK Server SHALL validate incoming requests and return appropriate error codes for invalid inputs
