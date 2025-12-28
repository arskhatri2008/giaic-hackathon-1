# Quickstart: RAG-Enabled Agent using OpenAI Agents SDK

## Prerequisites

- Python 3.11+
- uv package manager
- OpenAI API key
- Qdrant database with book content indexed
- Access to the retrieval function from Spec-2

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env to include your OpenAI API key and Qdrant configuration
   ```

## Running the Agent

1. **Start the RAG agent**
   ```bash
   python backend/agent.py
   ```

2. **Or run with uv**
   ```bash
   uv run backend/agent.py
   ```

## Basic Usage

```python
from backend.agent import RAGAgent

# Initialize the agent
agent = RAGAgent()

# Ask a question about the book content
response = agent.ask("What are the key concepts in chapter 1?")
print(response)
```

## Configuration

The agent can be configured with:

- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_HOST`: Host address for Qdrant database
- `QDRANT_PORT`: Port for Qdrant database
- `QDRANT_COLLECTION`: Collection name containing book content

## Testing

Run the tests to ensure everything is working:

```bash
# Run all tests
python -m pytest tests/

# Run specific agent tests
python -m pytest tests/test_agent.py
```