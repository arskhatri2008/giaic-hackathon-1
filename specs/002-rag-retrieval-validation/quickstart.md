# Quickstart: RAG Retrieval Pipeline Validation

## Overview
Quickstart guide for setting up and running the RAG retrieval validation system.

## Prerequisites

### Environment Setup
1. Python 3.11+ installed
2. pip and virtual environment tools
3. Access to Cohere API key
4. Access to Qdrant vector database

### Required Environment Variables
Set up the following in your `.env` file:
```bash
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=docusaurus_embeddings
```

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (using existing backend requirements)
cd backend
pip install -r requirements.txt
```

### 3. Verify Environment Variables
```bash
# Check that required environment variables are set
python -c "import os; print('COHERE_API_KEY set:', bool(os.getenv('COHERE_API_KEY')))"
python -c "import os; print('QDRANT_URL set:', bool(os.getenv('QDRANT_URL')))"
```

## Running Retrieval Validation

### 1. Basic Retrieval Test
```bash
# Run a basic retrieval test
cd backend
python retrieve.py --query "What is ROS 2?"
```

### 2. Validation with Specific Parameters
```bash
# Run retrieval with specific parameters
python retrieve.py --query "Explain semantic search" --limit 5 --min-score 0.7
```

### 3. Embedding Consistency Validation
```bash
# Validate embedding consistency between ingestion and retrieval
python retrieve.py --validate-consistency
```

### 4. Run Semantic Similarity Validation Test
```bash
# Run the semantic similarity validation test
python retrieve.py --test-semantic
```

### 5. Batch Validation
```bash
# Run multiple test queries for comprehensive validation
python retrieve.py --validate-all
```

### 6. Example Usage Scripts
The repository includes example scripts demonstrating various validation scenarios:

```bash
# Run basic retrieval example
python backend/examples/basic_retrieval_example.py

# Run embedding consistency example
python backend/examples/embedding_consistency_example.py

# Run semantic validation test
python backend/examples/semantic_validation_test.py

# Run comprehensive final validation
python backend/examples/final_validation_test.py
```

## Testing the Implementation

### 1. Unit Tests
```bash
# Run unit tests for retrieval functionality
cd backend
python -m pytest tests/test_retrieve.py -v
```

### 2. Integration Tests
```bash
# Run integration tests that connect to Qdrant
python -m pytest tests/test_retrieve.py::test_retrieval_integration -v
```

### 3. Validation Tests
```bash
# Run full validation suite
python retrieve.py --test-suite
```

## Expected Output

When running validation, you should see output similar to:

```
Starting RAG retrieval validation...
Query: "What is ROS 2?"
Retrieved 3 chunks with relevance scores:
1. (0.89) ROS 2 Introduction - https://example.com/docs/ros2-intro
2. (0.85) ROS 2 Architecture - https://example.com/docs/ros2-architecture
3. (0.78) ROS 2 Communication - https://example.com/docs/ros2-communication

Validation successful: All metadata present, relevance scores above threshold.
```

## Troubleshooting

### Common Issues

1. **Connection to Qdrant fails**:
   - Verify QDRANT_URL and QDRANT_API_KEY are correct
   - Check network connectivity to Qdrant instance

2. **Cohere API error**:
   - Verify COHERE_API_KEY is valid and has sufficient quota
   - Check that the embedding model is accessible

3. **No results returned**:
   - Verify that the Qdrant collection has been populated by the ingestion pipeline
   - Check that the collection name matches between ingestion and retrieval

### Validation Report
The system will generate a validation report with:
- Query execution success/failure
- Metadata completeness verification
- Relevance score thresholds
- Embedding consistency validation