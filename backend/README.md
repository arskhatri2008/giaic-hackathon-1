# Docusaurus RAG Ingestion Pipeline

A pipeline for ingesting Docusaurus website content, generating semantic embeddings using Cohere, and storing them in Qdrant vector database for RAG applications.

## Features

- Crawls and extracts clean text from deployed Docusaurus websites
- Generates semantic embeddings using Cohere embedding models
- Stores embeddings with metadata in Qdrant vector database
- Data is chunked, normalized, and ready for retrieval use
- Pipeline can be rerun incrementally without duplication

## Prerequisites

- Python 3.9+
- Access to Cohere API (API key)
- Access to Qdrant Cloud or self-hosted Qdrant instance

## Setup

1. Clone the repository
2. Navigate to the `backend` directory
3. Install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

4. Install Playwright browsers:

```bash
playwright install chromium
```

5. Copy the environment template and configure your settings:

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Usage

```bash
# Run the ingestion pipeline
python main.py --urls "https://your-docusaurus-site.com" "https://another-site.com"

# Run with custom settings
python main.py \
  --urls "https://docs.example.com" \
  --collection-name "my_embeddings" \
  --chunk-size 384 \
  --max-concurrent 3
```

## Configuration

The pipeline can be configured via environment variables in the `.env` file or command-line arguments. See `.env.example` for all available options.

## Architecture

The pipeline consists of several components:
- **Crawlers**: Extract content from Docusaurus websites
- **Processors**: Chunk and normalize content
- **Embeddings**: Generate semantic vectors using Cohere
- **Storage**: Persist vectors in Qdrant with metadata