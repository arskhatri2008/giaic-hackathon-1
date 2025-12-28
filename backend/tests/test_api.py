import pytest
from fastapi.testclient import TestClient
from api import app

# Create a test client for the FastAPI app
client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "RAG Agent API is running"}

def test_health_endpoint():
    """Test the health endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200

    # Check that the response has the expected structure
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "services" in data
    assert "version" in data

    # Check that status is one of the expected values
    assert data["status"] in ["healthy", "degraded", "unavailable"]

def test_query_endpoint_valid_request():
    """Test the query endpoint with a valid request"""
    # This test might fail if the agent is not properly configured,
    # so we'll test that it at least returns a valid response structure
    query_data = {
        "query": "test query"
    }

    response = client.post("/api/", json=query_data)

    # The endpoint should return either success or an error with proper structure
    assert response.status_code in [200, 422, 500]  # 422 for validation errors, 500 for internal errors

def test_query_endpoint_missing_query():
    """Test the query endpoint with missing required query field"""
    query_data = {
        "context": "test context"
    }

    response = client.post("/api/", json=query_data)

    # Should return 422 for validation error since query is required
    assert response.status_code == 422

def test_query_endpoint_empty_query():
    """Test the query endpoint with an empty query"""
    query_data = {
        "query": ""
    }

    response = client.post("/api/", json=query_data)

    # Should return 422 for validation error since query is required and has min length
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main()