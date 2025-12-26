# Data Model: RAG Retrieval Pipeline Validation

## Overview
Data models for RAG retrieval validation system that ensures semantic similarity search functionality and metadata integrity.

## Core Entities

### RetrievedContentChunk
**Description**: A segment of documentation content retrieved from Qdrant with associated metadata and relevance scoring.

**Fields**:
- `id` (string): Unique identifier for the chunk
- `source_url` (string): Original URL where content was crawled from
- `title` (string): Title of the content chunk
- `content` (string): The actual content text
- `content_hash` (string): Hash for deduplication purposes
- `relevance_score` (float): Semantic similarity score (0.0-1.0)
- `word_count` (int): Number of words in the content
- `section_path` (string): Path of the section in the documentation structure
- `extracted_at` (datetime): Timestamp when content was originally extracted

**Validation Rules**:
- `relevance_score` must be between 0.0 and 1.0
- `source_url` must be a valid URL format
- `content` must not be empty
- `content_hash` must be unique within the result set

### SemanticQuery
**Description**: A text-based search query processed through the embedding model to find semantically similar content.

**Fields**:
- `text` (string): The query text to search for
- `embedding_vector` (list[float]): Vector representation of the query
- `query_metadata` (dict): Additional metadata about the query

**Validation Rules**:
- `text` must not be empty
- `embedding_vector` must match the expected dimension for the Cohere model

### RetrievalResult
**Description**: Container for results returned by the retrieval system.

**Fields**:
- `query` (SemanticQuery): The original query that was executed
- `retrieved_chunks` (list[RetrievedContentChunk]): List of content chunks returned
- `execution_time` (float): Time taken to execute the query in seconds
- `total_results` (int): Total number of results found
- `validation_report` (dict): Report on retrieval success/failure

**Validation Rules**:
- `retrieved_chunks` must be ordered by relevance_score (descending)
- `execution_time` must be positive
- `total_results` must match length of retrieved_chunks

### ValidationError
**Description**: Represents errors that occur during retrieval validation.

**Fields**:
- `error_type` (string): Type of validation error
- `message` (string): Human-readable error message
- `timestamp` (datetime): When error occurred
- `query_context` (SemanticQuery): Query that caused the error

## Relationships

```
SemanticQuery --[executes]-> RetrievalResult
RetrievalResult --[contains]-> RetrievedContentChunk
RetrievalResult --[may have]-> ValidationError
```

## State Transitions

### RetrievalResult States
1. **PENDING**: Query submitted, waiting for execution
2. **PROCESSING**: Query is being executed against Qdrant
3. **VALIDATED**: Results retrieved and validated successfully
4. **FAILED**: Error occurred during retrieval or validation