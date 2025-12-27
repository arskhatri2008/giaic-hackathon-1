from pydantic import BaseModel, Field
from typing import Optional
import re


class QueryRequest(BaseModel):
    """
    Represents a user query to the RAG agent
    """
    query: str = Field(
        ...,
        description="The user's question or query text",
        min_length=1,
        max_length=2000,
        example="What is ROS 2 and how does it differ from ROS 1?"
    )
    context: Optional[str] = Field(
        None,
        description="Additional context to provide to the agent",
        max_length=5000,
        example="I'm learning about robotics frameworks"
    )
    user_id: Optional[str] = Field(
        None,
        description="Identifier for the requesting user",
        pattern=r"^[a-zA-Z0-9-_]+$",
        example="user-123"
    )
    session_id: Optional[str] = Field(
        None,
        description="Session identifier for conversation context",
        pattern=r"^[a-zA-Z0-9-_]+$",
        example="sess-456"
    )
    include_sources: Optional[bool] = Field(
        True,
        description="Whether to include source references in response",
        example=True
    )

    class Config:
        schema_extra = {
            "example": {
                "query": "What is ROS 2?",
                "context": "I'm learning about robotics frameworks",
                "include_sources": True
            }
        }