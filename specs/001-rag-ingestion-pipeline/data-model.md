# Data Model: RAG Ingestion Pipeline for Docusaurus Book Content

**Branch**: `001-rag-ingestion-pipeline` | **Date**: 2025-12-25 | **Spec**: [link to spec.md](../spec.md)
**Input**: Feature specification from `/specs/001-rag-ingestion-pipeline/spec.md`

## Data Model Summary

This document defines the data structures and schemas for the RAG ingestion pipeline, including content chunks, embedding vectors, and metadata storage in Qdrant.

## Core Data Models

### 1. ContentChunk

Represents a piece of extracted text from a Docusaurus page with associated metadata.

```python
class ContentChunk:
    id: str                    # Unique identifier (UUID)
    source_url: str           # Original URL of the content
    section_path: str         # Docusaurus section hierarchy (e.g., "module-1/chapter-2")
    title: str                # Page or section title
    content: str              # Clean extracted text content
    chunk_index: int          # Position of this chunk within the document
    total_chunks: int         # Total number of chunks from this document
    content_hash: str         # SHA-256 hash of content for deduplication
    extracted_at: datetime    # Timestamp when content was extracted
    word_count: int           # Number of words in the content
    metadata: dict            # Additional metadata (custom fields)
```

### 2. EmbeddingVector

Represents the semantic embedding of a content chunk with associated data.

```python
class EmbeddingVector:
    content_chunk: ContentChunk  # Reference to source content
    vector: List[float]         # The embedding vector (e.g., 1024-dimensional)
    model_name: str             # Name of the embedding model used
    model_version: str          # Version of the embedding model
    embedding_created_at: datetime  # Timestamp when embedding was generated
    vector_size: int            # Dimension of the embedding vector
```

### 3. CrawlJob

Represents a single execution of the ingestion pipeline with configuration and status tracking.

```python
class CrawlJob:
    id: str                    # Unique identifier (UUID)
    name: str                  # Human-readable name for the job
    target_urls: List[str]     # List of URLs to crawl
    started_at: datetime       # When the job started
    completed_at: datetime     # When the job completed (null if running)
    status: str                # Status: 'pending', 'running', 'completed', 'failed'
    processed_count: int       # Number of pages processed
    successful_count: int      # Number of pages successfully processed
    failed_count: int          # Number of pages that failed processing
    error_details: List[dict]  # Details of any errors encountered
    configuration: dict        # Crawl configuration (delays, concurrency, etc.)
    stats: dict                # Statistics about the crawl (timing, sizes, etc.)
```

## Qdrant Collection Schema

The Qdrant vector database will store embeddings with rich metadata for retrieval.

### Collection: `docusaurus_embeddings`

**Vector Configuration**:
- Size: 1024 (for Cohere embeddings)
- Distance: Cosine (recommended for text embeddings)

**Payload Schema**:
```json
{
  "source_url": "string",           // Original URL of the content
  "section_path": "string",         // Docusaurus section hierarchy
  "title": "string",                // Page or section title
  "chunk_index": "integer",         // Position of chunk in document
  "total_chunks": "integer",        // Total chunks from this document
  "content_hash": "string",         // SHA-256 hash for deduplication
  "extracted_at": "datetime",       // Timestamp of extraction
  "word_count": "integer",          // Number of words in content
  "content_preview": "string",      // First 200 characters of content for preview
  "custom_metadata": "object"       // Additional custom metadata as key-value pairs
}
```

**Indexing Strategy**:
- Index on `source_url` for fast URL-based lookups
- Index on `section_path` for hierarchical navigation
- Index on `content_hash` for deduplication checks
- Index on `extracted_at` for temporal queries

## Data Flow

### 1. Crawling and Extraction Process
```
URL → Crawler → Raw HTML → Text Extractor → ContentChunk (with hash)
```

### 2. Embedding Generation Process
```
ContentChunk → Normalizer → Embedder → EmbeddingVector (with vector)
```

### 3. Storage Process
```
EmbeddingVector → Qdrant Storage → Vector + Payload (with metadata)
```

## Data Validation Rules

### ContentChunk Validation
- `source_url` must be a valid URL format
- `content` must be non-empty and contain at least 50 characters
- `content_hash` must be a valid SHA-256 hash (64 characters)
- `chunk_index` must be >= 0 and < `total_chunks`
- `word_count` must be >= 0

### EmbeddingVector Validation
- `vector` must have exactly 1024 elements (for Cohere embeddings)
- `vector` elements must be floats between -1 and 1
- `model_name` must match expected Cohere model format
- `vector_size` must match the actual vector length

### CrawlJob Validation
- `status` must be one of the defined status values
- `processed_count` >= `successful_count` + `failed_count`
- `started_at` must be before `completed_at` (if completed)

## Data Relationships

### One-to-Many Relationships
- One `CrawlJob` → Many `ContentChunk` instances
- One `ContentChunk` → One `EmbeddingVector` (one-to-one in our case)

### Deduplication Logic
- Before storing a new embedding, check if `content_hash` already exists in Qdrant
- If hash exists, skip storing to prevent duplication
- If hash is new, proceed with embedding generation and storage

## Migration Considerations

### Schema Evolution
- Use semantic versioning for data models
- Maintain backward compatibility where possible
- Provide migration scripts for breaking changes
- Log schema version with each stored item

### Metadata Extensibility
- Use the `custom_metadata` field in Qdrant for future extensions
- Allow additional fields in ContentChunk without breaking existing code
- Design for extensibility in the data models