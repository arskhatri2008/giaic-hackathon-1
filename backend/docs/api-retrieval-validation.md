# RAG Retrieval Validation API Documentation

## Overview

The RAG Retrieval Validation API provides functionality to validate the RAG (Retrieval-Augmented Generation) retrieval system by:

1. Performing semantic similarity searches against Qdrant vector database
2. Verifying retrieved content chunks contain proper metadata
3. Validating embedding consistency between ingestion and retrieval
4. Providing deterministic results for identical queries

## Main Components

### RetrievalValidator Class

The main class for validating RAG retrieval pipeline functionality.

#### Methods

- `validate_retrieval(query_text: str, limit: int = 5, min_score: float = 0.7) -> RetrievalResult`
  - Primary method to validate retrieval functionality with a semantic query
  - Parameters:
    - `query_text`: The semantic query text to validate
    - `limit`: Maximum number of results to return (default: 5)
    - `min_score`: Minimum relevance score threshold (default: 0.7)
  - Returns: `RetrievalResult` object with query, results, and validation report

- `semantic_similarity_search(query_text: str, limit: int = 5, min_score: float = 0.7) -> RetrievalResult`
  - Perform semantic similarity search function that queries Qdrant and returns ranked results
  - Parameters: Same as `validate_retrieval`
  - Returns: `RetrievalResult` object

- `validate_embedding_consistency() -> Dict[str, Any]`
  - Validate embedding consistency between ingestion and retrieval
  - Returns: Dictionary with consistency validation results

- `test_semantic_similarity_validation() -> Dict[str, Any]`
  - Run semantic similarity validation test
  - Returns: Dictionary with test results and validation metrics

### Data Classes

#### SemanticQuery
Represents a text-based search query processed through the embedding model.

- `text: str` - The query text
- `embedding_vector: Optional[List[float]]` - The embedding vector
- `query_metadata: Optional[Dict[str, Any]]` - Additional metadata

#### RetrievedContentChunk
Represents a segment of documentation content retrieved from Qdrant.

- `id: str` - Unique identifier
- `source_url: str` - Source URL of the content
- `title: str` - Title of the content
- `content: str` - Content preview
- `content_hash: str` - Hash of the content
- `relevance_score: float` - Relevance score (0.0-1.0)
- `word_count: int` - Number of words in content
- `section_path: str` - Path to the section
- `extracted_at: datetime` - When the content was extracted

#### RetrievalResult
Container for results returned by the retrieval system.

- `query: SemanticQuery` - The original query
- `retrieved_chunks: List[RetrievedContentChunk]` - Retrieved content chunks
- `execution_time: float` - Time taken to execute the query
- `total_results: int` - Total number of results returned
- `validation_report: Dict[str, Any]` - Validation report with success metrics

## Command-Line Interface

The module provides a command-line interface for retrieval validation. Run from the backend directory:

```bash
cd backend
python -m retrieve --query "Your query text" --limit 5 --min-score 0.7
```

### CLI Options

- `--query, -q`: The query text to validate (required)
- `--limit, -l`: Maximum number of results to return (default: 5)
- `--min-score, -m`: Minimum relevance score threshold (default: 0.7)
- `--validate-consistency`: Validate embedding consistency only
- `--test-semantic`: Run semantic similarity validation test

### Example Usage

```bash
# Navigate to backend directory first
cd backend

# Perform a basic retrieval validation
python -m retrieve --query "What is semantic search?" --limit 3 --min-score 0.6

# Validate embedding consistency only
python -m retrieve --validate-consistency

# Run semantic similarity validation test
python -m retrieve --test-semantic
```

## Configuration

The validator uses the following configuration from `config.settings`:

- `cohere_api_key` - Cohere API key for embeddings
- `qdrant_url` - Qdrant vector database URL
- `qdrant_api_key` - Qdrant API key
- `qdrant_collection_name` - Name of the collection to search
- `embedding_model` - Model used for embeddings
- `embedding_input_type` - Input type for embeddings

## Error Handling

The API handles various error scenarios:

- Qdrant connection failures
- Empty query handling
- Queries that return no relevant results
- Malformed embedding parameters
- Invalid configuration settings

## Validation Metrics

The validation report includes the following metrics:

- `execution_time`: Time taken to execute the query
- `total_chunks`: Total number of retrieved chunks
- `metadata_complete`: Whether all required metadata is present
- `embedding_consistency`: Whether embedding parameters match between ingestion and retrieval