from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .source_reference import SourceReference


class QueryResponse(BaseModel):
    """
    Contains the agent's response to a user query
    """
    response: str = Field(
        ...,
        description="The agent's answer to the query",
        min_length=1,
        max_length=10000,
        example="ROS 2 is the next-generation Robot Operating System..."
    )
    sources: Optional[List[SourceReference]] = Field(
        None,
        description="References to documents used in the response",
        max_items=20
    )
    query_id: str = Field(
        ...,
        description="Unique identifier for the query",
        pattern=r"^[a-zA-Z0-9-_]+$",
        example="query-789"
    )
    timestamp: datetime = Field(
        ...,
        description="ISO 8601 timestamp of response",
        example="2025-12-26T10:00:00Z"
    )
    execution_time: Optional[float] = Field(
        None,
        description="Time taken to generate response in seconds",
        ge=0,
        example=2.5
    )
    status: str = Field(
        ...,
        description="Status of the request",
        enum=["success", "error", "partial"],
        example="success"
    )

    class Config:
        schema_extra = {
            "example": {
                "response": "ROS 2 is the next-generation Robot Operating System...",
                "sources": [
                    {
                        "id": "doc-001",
                        "title": "Introduction to ROS 2 Concepts",
                        "relevance_score": 0.85,
                        "content_preview": "ROS 2 is designed to address the limitations of ROS 1..."
                    }
                ],
                "query_id": "query-789",
                "timestamp": "2025-12-26T10:00:00Z",
                "execution_time": 2.5,
                "status": "success"
            }
        }