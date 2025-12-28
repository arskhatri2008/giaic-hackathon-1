# Research: RAG Ingestion Pipeline for Docusaurus Book Content

**Branch**: `001-rag-ingestion-pipeline` | **Date**: 2025-12-25 | **Spec**: [link to spec.md](../spec.md)
**Input**: Feature specification from `/specs/001-rag-ingestion-pipeline/spec.md`

## Research Summary

This research document covers the technical investigation for implementing a RAG ingestion pipeline that crawls Docusaurus websites, generates embeddings using Cohere, and stores vectors in Qdrant.

## Phase 0: Technical Research

### 1. Docusaurus Website Crawling Approaches

**Option 1: Standard HTTP Requests + BeautifulSoup**
- Pros: Lightweight, fast, good for static content
- Cons: Cannot handle JavaScript-rendered content
- Tools: requests, BeautifulSoup4
- Best for: Static Docusaurus sites without dynamic content

**Option 2: Headless Browser (Playwright/Pyppeteer)**
- Pros: Handles JavaScript, can interact with dynamic content
- Cons: More resource-intensive, slower
- Tools: Playwright, Pyppeteer
- Best for: Modern Docusaurus sites with client-side rendering

**Decision**: Use Playwright for comprehensive content extraction that handles both static and dynamic Docusaurus sites.

### 2. Text Extraction from Docusaurus Pages

**Key Elements to Extract**:
- Main content area (usually `.markdown` or `.theme-doc-markdown`)
- Page titles and headings (h1, h2, h3, etc.)
- Navigation context (sidebar structure)
- Code blocks (may need special handling)
- Avoid: Navigation bars, headers, footers, TOC, links

**Approach**: Use CSS selectors to target main content areas while excluding navigation and UI elements.

### 3. Content Chunking Strategies

**Option 1: Fixed Token Length**
- Split at predetermined token counts (e.g., 512 tokens)
- Pros: Consistent chunk sizes
- Cons: May split contextually related content

**Option 2: Semantic Boundaries**
- Split at paragraph, section, or heading boundaries
- Pros: Maintains context, respects document structure
- Cons: Variable chunk sizes

**Decision**: Use semantic boundaries with max token length fallback to maintain document context while avoiding oversized chunks.

### 4. Cohere Embedding Models

**Available Models**:
- `embed-english-v3.0`: Latest English model with good performance
- `embed-multilingual-v3.0`: For multilingual content
- Dimensions: 1024 (recommended for retrieval tasks)

**Input Requirements**:
- Max 4096 tokens per request
- Multiple inputs in single request for efficiency
- Proper text preprocessing recommended

### 5. Qdrant Vector Database Integration

**Key Features**:
- Cloud Free Tier supports up to 100K vectors
- Supports metadata storage with vectors
- Provides similarity search capabilities
- Python client available

**Collection Schema**:
- Vector: embedding values (1024 dimensions)
- Payload: source_url, section, chunk_index, content_text, timestamp

### 6. Incremental Processing Strategy

**Approach**:
- Calculate content hash for each chunk
- Store hash in Qdrant payload or separate tracking system
- Compare hashes before processing to avoid duplicates
- Track last processed timestamp for each source

## Phase 1: Architecture Research

### Pipeline Architecture

```
[URL List] → [Crawler] → [Text Extractor] → [Chunker] → [Embedder] → [Qdrant Storage]
                ↓            ↓               ↓           ↓           ↓
           [Error Handling] [Validation] [Normalization] [Batching] [Deduplication]
```

### Error Handling Strategy

- Network errors during crawling (retry with exponential backoff)
- Cohere API errors (retry, queue for later, alert on persistent failures)
- Qdrant storage errors (retry, temporary storage, alert)
- Content parsing errors (log and continue with other content)

### Configuration Management

- Environment variables for API keys and service URLs
- Configuration file for crawling settings (delays, retries, etc.)
- Command-line arguments for source URLs and processing options

## Phase 2: Implementation Research

### Dependencies Analysis

**Core Dependencies**:
- `playwright`: For browser automation and content extraction
- `cohere`: For embedding generation
- `qdrant-client`: For vector database operations
- `python-dotenv`: For environment configuration
- `click`: For command-line interface

**Optional Dependencies**:
- `tqdm`: For progress tracking
- `structlog`: For structured logging

### Performance Considerations

- Batch embedding requests to Cohere for efficiency
- Parallel crawling with controlled concurrency
- Connection pooling for database operations
- Memory management for large content sets

### Security Considerations

- Secure handling of API keys (environment variables, not code)
- Input validation for URLs to prevent SSRF attacks
- Rate limiting to avoid overwhelming target sites
- Proper error logging without exposing sensitive information

## Research Conclusions

The technical approach is feasible using established Python libraries. Playwright provides robust content extraction capabilities, Cohere offers reliable embedding generation, and Qdrant provides suitable vector storage with metadata support. The incremental processing approach with content hashing will prevent duplication as required by the specification.