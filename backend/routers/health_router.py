from fastapi import APIRouter
import logging

from models.health_status import HealthStatus
from models.error_response import ErrorResponse
from services.agent_service import AgentService
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router instance
health_router = APIRouter()

@health_router.get("/", response_model=HealthStatus, summary="Health check")
async def health_check():
    """
    Check the health status of the RAG agent service
    """
    try:
        # Log the health check request
        logger.info("Health check requested")

        # Use the AgentService to perform health check
        health_status = await AgentService.check_health()

        # Log successful health check
        logger.info(f"Health check completed, status: {health_status.status}")

        return health_status

    except Exception as e:
        logger.error(f"Error during health check: {str(e)}")

        # In case of error, return a degraded status
        error_health_status = HealthStatus(
            status="unavailable",
            timestamp=datetime.now(),
            services={
                "agent": {"status": "unavailable"},
                "qdrant": {"status": "unavailable"},
                "api": {"status": "unavailable"}
            },
            version="1.0.0"
        )

        return error_health_status


@health_router.get("/health", response_model=HealthStatus, summary="Health check")
async def health_check_full():
    """
    Check the health status of the RAG agent service
    (Duplicate endpoint for clarity - same functionality as the root GET)
    """
    try:
        # Log the health check request
        logger.info("Health check requested via /health endpoint")

        # Use the AgentService to perform health check
        health_status = await AgentService.check_health()

        # Log successful health check
        logger.info(f"Health check completed, status: {health_status.status}")

        return health_status

    except Exception as e:
        logger.error(f"Error during health check: {str(e)}")

        # In case of error, return a degraded status
        error_health_status = HealthStatus(
            status="unavailable",
            timestamp=datetime.now(),
            services={
                "agent": {"status": "unavailable"},
                "qdrant": {"status": "unavailable"},
                "api": {"status": "unavailable"}
            },
            version="1.0.0"
        )

        return error_health_status