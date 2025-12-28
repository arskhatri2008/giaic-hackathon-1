# Quickstart Guide: RAG Ingestion Pipeline for Docusaurus Book Content

**Branch**: `001-rag-ingestion-pipeline` | **Date**: 2025-12-25 | **Spec**: [link to spec.md](../spec.md)
**Input**: Feature specification from `/specs/001-rag-ingestion-pipeline/spec.md`

## Quickstart Summary

This guide provides a step-by-step process to set up and run the RAG ingestion pipeline for Docusaurus book content, from environment setup to first successful pipeline execution.

## Prerequisites

### System Requirements
- Python 3.9 or higher
- pip package manager
- Git for version control
- Access to Cohere API (API key)
- Access to Qdrant Cloud or self-hosted Qdrant instance

### External Services
- Cohere account with API key for embedding generation
- Qdrant vector database (Cloud Free Tier or self-hosted)

## Setup Process

### 1. Environment Setup

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd <repository-name>

# Navigate to backend directory
cd backend/

# Install uv (Python package manager) if not already installed
pip install uv
```

### 2. Dependency Installation

```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install project dependencies
uv pip install playwright cohere qdrant-client python-dotenv click tqdm structlog
```

### 3. Configuration Setup

Create a `.env` file in the backend directory with the following content:

```bash
# .env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here  # e.g., https://your-cluster-url.qdrant.tech
QDRANT_API_KEY=your_qdrant_api_key_here  # Only needed if using cloud instance
QDRANT_COLLECTION_NAME=docusaurus_embeddings
QDRANT_PORT=6333  # Default port, change if needed

# Crawler settings
CRAWLER_DELAY_BETWEEN_REQUESTS=1  # Delay in seconds between requests to same domain
CRAWLER_MAX_CONCURRENT_REQUESTS=5  # Max number of concurrent requests
CRAWLER_TIMEOUT=30  # Request timeout in seconds
CRAWLER_USER_AGENT="Docusaurus-RAG-Crawler/1.0"

# Embedding settings
EMBEDDING_MODEL=embed-english-v3.0
EMBEDDING_INPUT_TYPE=search_document  # Cohere-specific input type
EMBEDDING_BATCH_SIZE=96  # Max items per Cohere API call (under 99 limit)

# Processing settings
CHUNK_SIZE_TOKENS=512  # Target chunk size in tokens
CHUNK_OVERLAP_TOKENS=50  # Overlap between chunks to maintain context
```

### 4. Initialize Playwright Browser

```bash
# Install required browsers for Playwright
playwright install chromium
```

## Basic Usage

### 1. Run the Pipeline with Default Settings

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the ingestion pipeline
python main.py --urls "https://your-docusaurus-site.com" "https://another-site.com"
```

### 2. Run with Specific Configuration

```bash
# Run with custom settings
python main.py \
  --urls "https://docs.example.com" \
  --collection-name "my_embeddings" \
  --chunk-size 384 \
  --max-concurrent 3
```

### 3. Run with Configuration File

Create a `config.json` file:

```json
{
  "target_urls": ["https://docs.example.com", "https://another-docs.com"],
  "collection_name": "docusaurus_embeddings",
  "chunk_size_tokens": 512,
  "max_concurrent_requests": 5,
  "batch_size": 96
}
```

Then run:

```bash
python main.py --config config.json
```

## Pipeline Execution Flow

### 1. Crawling Phase
- The pipeline visits each URL in the target list
- Extracts clean text content from Docusaurus pages
- Preserves section hierarchy and metadata
- Skips navigation, headers, and other non-content elements

### 2. Processing Phase
- Chunks content based on semantic boundaries
- Normalizes text (removes extra whitespace, handles special characters)
- Calculates content hash for deduplication
- Prepares batches for embedding generation

### 3. Embedding Phase
- Sends content batches to Cohere API
- Generates semantic embeddings for each chunk
- Validates embedding dimensions and quality

### 4. Storage Phase
- Stores embeddings in Qdrant vector database
- Saves metadata with each vector (source URL, section, etc.)
- Implements deduplication using content hash
- Updates job status and statistics

## Verification Steps

### 1. Check Successful Execution
```bash
# Look for completion message
# Expected output: "Pipeline completed successfully. Processed X pages, stored Y embeddings."
```

### 2. Verify Data in Qdrant
- Log into your Qdrant dashboard
- Check that the collection exists and has the expected number of vectors
- Verify that metadata includes source URLs and section information

### 3. Test Deduplication
- Run the same URLs again
- Verify that the second run processes fewer or no new items due to deduplication

## Common Issues and Solutions

### Issue: Playwright Browser Not Found
**Solution**: Run `playwright install chromium` to install the required browser

### Issue: Cohere API Key Not Working
**Solution**: Verify your API key in the `.env` file and ensure your Cohere account is active

### Issue: Qdrant Connection Failed
**Solution**: Check your Qdrant URL and API key in the `.env` file, ensure the service is running

### Issue: Rate Limiting from Target Sites
**Solution**: Increase `CRAWLER_DELAY_BETWEEN_REQUESTS` in your configuration

## Next Steps

1. **Scale Up**: Add more Docusaurus sites to your target URL list
2. **Monitor Performance**: Track pipeline metrics and optimize as needed
3. **Set Up Scheduling**: Create scheduled runs for incremental updates
4. **Add Error Handling**: Implement alerting for pipeline failures
5. **Performance Tuning**: Adjust batch sizes and concurrency based on your specific needs