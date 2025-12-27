# Data Model: FastAPI RAG Agent Integration

## Overview
This document defines the data models for the FastAPI RAG agent integration, including request/response schemas and data flow patterns.

## Entity: QueryRequest
**Description**: Represents a user query to the RAG agent
**Fields**:
- `query`: string (required) - The user's question or query text
- `context`: string (optional) - Additional context to provide to the agent
- `user_id`: string (optional) - Identifier for the requesting user
- `session_id`: string (optional) - Session identifier for conversation context
- `include_sources`: boolean (optional) - Whether to include source references in response

**Validation Rules**:
- `query` must be 1-2000 characters
- `context` must be 0-5000 characters if provided
- `user_id` must follow UUID format if provided
- `session_id` must follow UUID format if provided

## Entity: QueryResponse
**Description**: Contains the agent's response to a user query
**Fields**:
- `response`: string (required) - The agent's answer to the query
- `sources`: array of SourceReference (optional) - References to documents used
- `query_id`: string (required) - Unique identifier for the query
- `timestamp`: string (required) - ISO 8601 timestamp of response
- `execution_time`: number (optional) - Time taken to generate response in seconds
- `status`: string (required) - Status of the request (success, error, partial)

**Validation Rules**:
- `response` must be 1-10000 characters
- `sources` array length must be 0-20 items
- `query_id` must be a valid UUID
- `status` must be one of: "success", "error", "partial"

## Entity: SourceReference
**Description**: Reference to a document or source used in the response
**Fields**:
- `id`: string (required) - Unique identifier for the source
- `title`: string (required) - Title of the source document
- `url`: string (optional) - URL to the source
- `relevance_score`: number (required) - Relevance score (0-1)
- `content_preview`: string (optional) - Preview of the relevant content

**Validation Rules**:
- `id` must be 1-100 characters
- `title` must be 1-200 characters
- `url` must be a valid URL format if provided
- `relevance_score` must be between 0 and 1
- `content_preview` must be 0-500 characters

## Entity: HealthStatus
**Description**: Represents the current operational status of the RAG agent service
**Fields**:
- `status`: string (required) - Overall system status (healthy, degraded, unavailable)
- `timestamp`: string (required) - ISO 8601 timestamp of status check
- `services`: object (required) - Status of individual services
- `version`: string (required) - API version

**Validation Rules**:
- `status` must be one of: "healthy", "degraded", "unavailable"
- `version` must follow semantic versioning format (e.g., "1.0.0")

## Entity: ErrorResponse
**Description**: Standardized error response format
**Fields**:
- `error`: string (required) - Error message
- `code`: string (required) - Error code
- `details`: object (optional) - Additional error details
- `timestamp`: string (required) - ISO 8601 timestamp of error

**Validation Rules**:
- `error` must be 1-500 characters
- `code` must be 1-50 uppercase characters
- `timestamp` must be valid ISO 8601 format

## API Endpoints Data Flow

### POST /query
**Request**: QueryRequest
**Response**: QueryResponse or ErrorResponse
**Description**: Process a user query and return an agent response

### GET /health
**Request**: None
**Response**: HealthStatus or ErrorResponse
**Description**: Check the health status of the RAG agent service

## State Transitions

### Query Processing
1. **Received**: QueryRequest received by API
2. **Processing**: Agent is working on the query
3. **Retrieved**: Relevant content has been retrieved from Qdrant
4. **Responded**: Agent has generated a response
5. **Completed**: Response has been returned to client

Each state transition includes appropriate logging and metrics collection.