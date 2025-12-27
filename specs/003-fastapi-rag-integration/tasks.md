# Tasks: FastAPI integration for RAG agent backend and frontend

## Feature Overview
Integration of FastAPI with the existing RAG agent backend to expose agent capabilities via local API endpoints. The solution includes a FastAPI backend that connects to the existing RAG agent implementation and a Docusaurus frontend with embedded chatbot UI components that communicate with the backend API.

## Phase 1: Setup
**Goal**: Initialize project structure and dependencies

- [X] T001 Create backend/api.py as the main FastAPI entry point
- [X] T002 [P] Update backend/requirements.txt with FastAPI and related dependencies
- [X] T003 [P] Create backend/models directory for Pydantic models
- [X] T004 [P] Create website/src/components/Chatbot directory for chatbot UI components
- [X] T005 [P] Create website/src/services directory for API communication services

## Phase 2: Foundational
**Goal**: Implement core models and foundational services needed by all user stories

- [X] T006 Create backend/models/query_request.py with QueryRequest Pydantic model
- [X] T007 Create backend/models/query_response.py with QueryResponse Pydantic model
- [X] T008 Create backend/models/source_reference.py with SourceReference Pydantic model
- [X] T009 Create backend/models/health_status.py with HealthStatus Pydantic model
- [X] T010 Create backend/models/error_response.py with ErrorResponse Pydantic model
- [X] T011 Create backend/services/agent_service.py to interface with existing agent.py
- [X] T012 [P] Create backend/config/settings.py for API configuration

## Phase 3: User Story 1 - Query RAG Agent via API (P1)
**Goal**: Enable full-stack engineers to send queries to the RAG agent through a FastAPI endpoint

**Independent Test**: Can be fully tested by making HTTP requests to the FastAPI endpoint and receiving responses from the RAG agent, delivering the core value of agent interaction.

- [X] T013 [US1] Create POST /query endpoint in backend/api.py that accepts QueryRequest
- [X] T014 [P] [US1] Implement query processing logic in backend/services/agent_service.py
- [X] T015 [P] [US1] Connect agent_service to backend/agent.py for actual query processing
- [X] T016 [P] [US1] Add request validation using QueryRequest model in /query endpoint
- [X] T017 [P] [US1] Format response using QueryResponse model in /query endpoint
- [X] T018 [P] [US1] Handle error conditions and return appropriate HTTP status codes
- [X] T019 [P] [US1] Add logging for query processing in backend/services/agent_service.py
- [X] T020 [P] [US1] Test /query endpoint with valid request and verify response format
- [X] T021 [P] [US1] Test /query endpoint with malformed request and verify error response

## Phase 4: User Story 3 - Health Check and Status Monitoring (P3)
**Goal**: Enable full-stack engineers to check the health status of the RAG agent service

**Independent Test**: Can be tested by making GET requests to a health endpoint and verifying the system returns appropriate status information.

- [X] T022 [US3] Create GET /health endpoint in backend/api.py
- [X] T023 [P] [US3] Implement health check logic in backend/services/agent_service.py
- [X] T024 [P] [US3] Check connectivity to RAG agent and Qdrant services
- [X] T025 [P] [US3] Return HealthStatus model from /health endpoint
- [X] T026 [P] [US3] Test /health endpoint and verify status information

## Phase 5: User Story 2 - Chatbot UI Integration (P2)
**Goal**: Enable web users to interact with a chatbot UI component embedded in the Docusaurus website

**Independent Test**: Can be tested by loading the Docusaurus website and using the chatbot UI to send queries and receive responses.

- [X] T027 [US2] Create Chatbot component in website/src/components/Chatbot/Chatbot.jsx
- [X] T028 [P] [US2] Create ChatMessage component for displaying messages in website/src/components/Chatbot/ChatMessage.jsx
- [X] T029 [P] [US2] Create ChatInput component for user input in website/src/components/Chatbot/ChatInput.jsx
- [X] T030 [P] [US2] Implement API service for /query endpoint in website/src/services/api.js
- [X] T031 [P] [US2] Implement API service for /health endpoint in website/src/services/api.js
- [X] T032 [P] [US2] Connect Chatbot component to backend API services
- [X] T033 [P] [US2] Implement loading states and error handling in Chatbot component
- [X] T034 [P] [US2] Add basic styling to Chatbot component
- [X] T035 [P] [US2] Test chatbot UI integration with actual backend API

## Phase 6: Polish & Cross-Cutting Concerns
**Goal**: Complete the implementation with additional features and refinements

- [X] T036 Add request/response time metrics to QueryResponse model and implementation
- [X] T037 Implement concurrent request handling and performance optimization
- [X] T038 Add comprehensive error handling for Qdrant and agent service failures
- [X] T039 Add input validation and sanitization for security
- [X] T040 Update docusaurus.config.js to include the Chatbot component
- [X] T041 Add environment configuration for API endpoints
- [X] T042 Implement proper error boundaries in React components
- [X] T043 Add loading indicators and better UX in Chatbot UI
- [X] T044 Write basic tests for backend API endpoints
- [X] T045 Document the API endpoints and usage in README

## Dependencies
- User Story 1 (P1) can be implemented independently
- User Story 3 (P3) can be implemented independently
- User Story 2 (P2) depends on User Story 1 (needs working /query endpoint)

## Parallel Execution Examples
- Tasks T002-T005 can be executed in parallel (different files, no dependencies)
- Tasks T006-T010 can be executed in parallel (different model files)
- Tasks T014-T018 can be executed in parallel (different aspects of /query endpoint)
- Tasks T028-T029 can be executed in parallel (different UI components)

## Implementation Strategy
1. **MVP Scope**: Complete User Story 1 (T001-T021) to have a working API that can query the RAG agent
2. **Incremental Delivery**: Add health check (User Story 3), then UI integration (User Story 2)
3. **Polish Phase**: Add performance, security, and UX enhancements

## Website Integration
- Chatbot component is now available across the entire Docusaurus website via a floating button
- The chatbot appears on all pages and can be toggled open/closed
- Proper error boundaries and loading indicators implemented
- Global CSS styling applied for consistent appearance