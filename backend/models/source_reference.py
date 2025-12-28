from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class SourceReference(BaseModel):
    """
    Reference to a document or source used in the response
    """
    id: str = Field(
        ...,
        description="Unique identifier for the source",
        min_length=1,
        max_length=100,
        example="doc-001"
    )
    title: str = Field(
        ...,
        description="Title of the source document",
        min_length=1,
        max_length=200,
        example="Introduction to ROS 2 Concepts"
    )
    url: Optional[HttpUrl] = Field(
        None,
        description="URL to the source",
        example="https://example.com/ros2-intro"
    )
    relevance_score: float = Field(
        ...,
        description="Relevance score (0-1)",
        ge=0,
        le=1,
        example=0.85
    )
    content_preview: Optional[str] = Field(
        None,
        description="Preview of the relevant content",
        max_length=500,
        example="ROS 2 is designed to address the limitations of ROS 1..."
    )

    class Config:
        schema_extra = {
            "example": {
                "id": "doc-001",
                "title": "Introduction to ROS 2 Concepts",
                "url": "https://example.com/ros2-intro",
                "relevance_score": 0.85,
                "content_preview": "ROS 2 is designed to address the limitations of ROS 1..."
            }
        }