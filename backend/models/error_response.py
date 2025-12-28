from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ErrorResponse(BaseModel):
    """
    Standardized error response format
    """
    error: str = Field(
        ...,
        description="Error message",
        min_length=1,
        max_length=500,
        example="Invalid query format"
    )
    code: str = Field(
        ...,
        description="Error code",
        pattern=r"^[A-Z_]+$",
        example="INVALID_QUERY"
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional error details",
        example={
            "field": "query",
            "reason": "Query is too short"
        }
    )
    timestamp: datetime = Field(
        ...,
        description="ISO 8601 timestamp of error",
        example="2025-12-26T10:00:00Z"
    )

    class Config:
        schema_extra = {
            "example": {
                "error": "Invalid query format",
                "code": "INVALID_QUERY",
                "details": {
                    "field": "query",
                    "reason": "Query is too short"
                },
                "timestamp": "2025-12-26T10:00:00Z"
            }
        }