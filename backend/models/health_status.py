from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class HealthStatus(BaseModel):
    """
    Represents the current operational status of the RAG agent service
    """
    status: str = Field(
        ...,
        description="Overall system status",
        enum=["healthy", "degraded", "unavailable"],
        example="healthy"
    )
    timestamp: datetime = Field(
        ...,
        description="ISO 8601 timestamp of status check",
        example="2025-12-26T10:00:00Z"
    )
    services: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Status of individual services",
        example={
            "agent": {"status": "healthy"},
            "qdrant": {"status": "healthy"},
            "api": {"status": "healthy"}
        }
    )
    version: str = Field(
        ...,
        description="API version",
        pattern=r"^\d+\.\d+\.\d+$",
        example="1.0.0"
    )

    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-12-26T10:00:00Z",
                "services": {
                    "agent": {"status": "healthy"},
                    "qdrant": {"status": "healthy"},
                    "api": {"status": "healthy"}
                },
                "version": "1.0.0"
            }
        }