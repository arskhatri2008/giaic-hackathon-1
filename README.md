# FastAPI RAG Agent Integration

This project integrates FastAPI with the existing RAG agent backend to expose agent capabilities via local API endpoints. The solution includes a FastAPI backend that connects to the existing RAG agent implementation and a Docusaurus frontend with embedded chatbot UI components that communicate with the backend API.

## Backend: RAG Agent API

The backend provides a FastAPI interface to interact with the RAG (Retrieval-Augmented Generation) agent.

### Endpoints

#### POST /api/
Send a query to the RAG agent and receive a response with supporting sources.

**Request Body**:
```json
{
  "query": "What is ROS 2?",
  "context": "I'm learning about robotics frameworks",
  "user_id": "user-123",
  "session_id": "sess-456",
  "include_sources": true
}
```

**Response**:
```json
{
  "response": "ROS 2 is the next-generation Robot Operating System...",
  "sources": [
    {
      "id": "doc-001",
      "title": "Introduction to ROS 2 Concepts",
      "url": "https://example.com/ros2-intro",
      "relevance_score": 0.85,
      "content_preview": "ROS 2 is designed to address the limitations of ROS 1..."
    }
  ],
  "query_id": "query-789",
  "timestamp": "2025-12-26T10:00:00Z",
  "execution_time": 2.5,
  "status": "success"
}
```

#### POST /api/query
Same functionality as the root POST endpoint.

#### GET /api/health
Check the health status of the RAG agent service.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-26T10:00:00Z",
  "services": {
    "agent": {"status": "healthy"},
    "qdrant": {"status": "healthy"},
    "api": {"status": "healthy"}
  },
  "version": "1.0.0"
}
```

### Environment Variables

- `QDRANT_URL`: URL for the Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `COHERE_API_KEY`: API key for Cohere embeddings
- `OPENROUTER_API_KEY`: API key for OpenRouter (if using OpenRouter models)
- `API_HOST`: Host for the API server (default: 0.0.0.0)
- `API_PORT`: Port for the API server (default: 8000)

### Running the Backend API

```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

#### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Frontend: Docusaurus Chatbot UI

The frontend provides a chatbot UI component that can be embedded in the Docusaurus website.

### Running the Frontend

```bash
cd website
npm install
npm start
```

### Chatbot Component

The chatbot component can be embedded in Docusaurus pages using the `<Chatbot />` component.

## Architecture

- **Backend**: FastAPI server with RAG agent integration
- **Frontend**: Docusaurus website with React chatbot component
- **Data Flow**: Query → FastAPI → RAG Agent → Response → Frontend
- **Services**: Agent, Qdrant vector store, Cohere embeddings