from fastapi import APIRouter, HTTPException
from typing import Optional
import logging
import html
import re

from models.query_request import QueryRequest
from models.query_response import QueryResponse
from models.error_response import ErrorResponse
from services.agent_service import AgentService
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router instance
query_router = APIRouter()

def sanitize_input(text: str) -> str:
    """
    Sanitize input text to prevent injection attacks
    """
    # Remove potentially dangerous characters/sequences
    sanitized = html.escape(text)
    # Additional sanitization can be added here as needed
    return sanitized

@query_router.post("/", response_model=QueryResponse, summary="Query the RAG agent")
async def query_agent_endpoint(query_request: QueryRequest):
    """
    Send a query to the RAG agent and receive a response with supporting sources
    """
    try:
        # Sanitize the query input
        sanitized_query = sanitize_input(query_request.query)

        # Update the query request with sanitized input
        query_request.query = sanitized_query

        # Log the incoming request
        logger.info(f"Processing query: {query_request.query[:100]}...")

        # Use the AgentService to process the query
        response = await AgentService.query_agent(query_request)

        # Log successful response
        logger.info(f"Query processed successfully, response length: {len(response.response)}")

        return response

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")

        # Create error response
        error_response = ErrorResponse(
            error=f"Error processing query: {str(e)}",
            code="QUERY_PROCESSING_ERROR",
            timestamp=datetime.now(),
            details={"query": query_request.query}
        )

        # Raise HTTP exception with the error response
        raise HTTPException(
            status_code=500,
            detail=error_response.dict()
        )


@query_router.post("/query", response_model=QueryResponse, summary="Query the RAG agent")
async def query_agent_full_endpoint(query_request: QueryRequest):
    """
    Send a query to the RAG agent and receive a response with supporting sources
    (Duplicate endpoint for clarity - same functionality as the root POST)
    """
    try:
        # Log the incoming request
        logger.info(f"Processing query via /query endpoint: {query_request.query[:100]}...")

        # Use the AgentService to process the query
        response = await AgentService.query_agent(query_request)

        # Log successful response
        logger.info(f"Query processed successfully, response length: {len(response.response)}")

        return response

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")

        # Create error response
        error_response = ErrorResponse(
            error=f"Error processing query: {str(e)}",
            code="QUERY_PROCESSING_ERROR",
            timestamp=datetime.now(),
            details={"query": query_request.query}
        )

        # Raise HTTP exception with the error response
        raise HTTPException(
            status_code=500,
            detail=error_response.dict()
        )