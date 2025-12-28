# Quickstart Guide: FastAPI RAG Agent Integration

## Overview
This guide provides instructions for setting up and running the FastAPI RAG agent integration with the Docusaurus frontend.

## Prerequisites
- Python 3.13 or higher
- Node.js 18+ and npm/yarn
- Access to Qdrant vector database
- OpenAI API key (or OpenRouter API key if using external provider)

## Backend Setup

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in the backend directory:
```env
OPENROUTER_API_KEY=your_openrouter_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
```

### 3. Run the FastAPI Server
```bash
cd backend
uvicorn api:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install Frontend Dependencies
```bash
cd website
npm install
```

### 2. Configure API Endpoint
Update the API endpoint in the chatbot component to point to your backend:
- Default: `http://localhost:8000`

### 3. Run the Docusaurus Server
```bash
cd website
npm run start
```

The website will be available at `http://localhost:3000`

## API Usage Examples

### Query the RAG Agent
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is ROS 2?",
    "include_sources": true
  }'
```

### Check Health Status
```bash
curl -X GET http://localhost:8000/health
```

## Frontend Integration

### Chatbot Component
The chatbot UI component is available in the Docusaurus theme:
- Located at: `website/src/components/Chatbot`
- Can be embedded in any MDX page using `<Chatbot />`
- Automatically connects to the backend API

## Development

### Running Tests
Backend tests:
```bash
cd backend
pytest tests/
```

Frontend tests:
```bash
cd website
npm run test
```

### API Documentation
The API documentation is automatically available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues
1. **Connection refused**: Ensure the backend server is running on port 8000
2. **API key errors**: Verify all environment variables are set correctly
3. **Qdrant connection**: Check that the Qdrant URL and API key are valid

### Debugging
Enable debug logging by setting the environment variable:
```bash
export LOG_LEVEL=DEBUG
```

## Next Steps
- Explore the API endpoints in the interactive documentation
- Integrate the chatbot component into your documentation pages
- Customize the chatbot UI to match your branding
- Add authentication for multi-user scenarios