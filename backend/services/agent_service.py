import logging
from typing import Optional
from datetime import datetime
from models.query_request import QueryRequest
from models.query_response import QueryResponse
from models.health_status import HealthStatus
from models.source_reference import SourceReference
import asyncio
import sys
import os
from asyncio import Semaphore
from config.settings import settings

# Add the backend directory to the path to import agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agent import ask_question, health_check
except ImportError as e:
    logging.error(f"Could not import agent module: {e}")
    ask_question = None
    health_check = None

# Import retrieve module to check Qdrant connectivity
try:
    from retrieve import retrieve_book_content
except ImportError as e:
    logging.error(f"Could not import retrieve module: {e}")
    retrieve_book_content = None

logger = logging.getLogger(__name__)

# Create a semaphore to limit concurrent requests
concurrent_request_semaphore = Semaphore(settings.max_concurrent_requests)


class AgentService:
    """
    Service class to interface with the existing RAG agent implementation
    """

    @staticmethod
    async def query_agent(query_request: QueryRequest) -> QueryResponse:
        """
        Process a query request and return a response from the RAG agent
        """
        start_time = datetime.now()

        # Acquire semaphore to limit concurrent requests
        async with concurrent_request_semaphore:
            try:
                # Extract the query from the request
                query_text = query_request.query

                # Call the existing agent implementation
                if ask_question is None:
                    raise Exception("Agent module not available")

                # Run the agent call with a subprocess to ensure complete isolation and timeout control
                import asyncio
                import concurrent.futures
                import functools

                def run_agent_in_isolated_context(query_text):
                    import asyncio
                    import sys
                    import os
                    # Add the backend directory to the path to import modules
                    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    if backend_dir not in sys.path:
                        sys.path.insert(0, backend_dir)

                    # Import inside the function to ensure proper context
                    from agent import ask_question, reset_tool_call_counter

                    # Create a new event loop for this execution
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        # Reset tool call counter for this query
                        reset_tool_call_counter()
                        # Run the agent call
                        return loop.run_until_complete(ask_question(query_text))
                    finally:
                        loop.close()

                # Execute the agent call with timeout using ThreadPoolExecutor
                loop = asyncio.get_event_loop()
                try:
                    # Use partial to pass the query_text argument
                    agent_func = functools.partial(run_agent_in_isolated_context, query_text)
                    agent_response = await asyncio.wait_for(
                        loop.run_in_executor(None, agent_func),
                        timeout=settings.agent_timeout
                    )
                except asyncio.TimeoutError:
                    raise Exception(f"Agent response timeout after {settings.agent_timeout} seconds")
                except Exception as agent_error:
                    logger.error(f"Agent service error: {str(agent_error)}")
                    raise

                # Calculate execution time
                execution_time = (datetime.now() - start_time).total_seconds()

                # Create a simple query response
                # Note: In a real implementation, we'd need to extract source references
                # from the agent response, but for now we'll return a basic response
                response = QueryResponse(
                    response=agent_response,
                    query_id=f"query-{int(start_time.timestamp())}",
                    timestamp=start_time,
                    execution_time=execution_time,
                    status="success"
                )

                return response

            except Exception as e:
                logger.error(f"Error querying agent: {str(e)}")
                execution_time = (datetime.now() - start_time).total_seconds()

                # Return error response
                response = QueryResponse(
                    response=f"Error processing query: {str(e)}",
                    query_id=f"query-{int(start_time.timestamp())}",
                    timestamp=start_time,
                    execution_time=execution_time,
                    status="error"
                )

                return response

    @staticmethod
    async def check_health() -> HealthStatus:
        """
        Check the health status of the RAG agent service and its dependencies
        """
        timestamp = datetime.now()

        # Initialize service statuses
        agent_status = "unavailable"
        qdrant_status = "unavailable"
        api_status = "healthy"  # API itself is running

        try:
            # Check if the agent module is available
            if ask_question is not None:
                try:
                    # If we have the health_check function, call it
                    if health_check:
                        health_result = await health_check()
                        agent_status = "healthy" if health_result.get("status") == "healthy" else "degraded"
                    else:
                        # If no specific health check function, just test if the module loads
                        agent_status = "healthy"
                except Exception as e:
                    logger.error(f"Agent health check failed: {str(e)}")
                    agent_status = "degraded"
            else:
                logger.error("Agent module not available")
                agent_status = "unavailable"

            # Check Qdrant connectivity by attempting a simple retrieval
            if retrieve_book_content is not None:
                try:
                    # Test Qdrant with a simple query
                    test_results = retrieve_book_content("test", min_score=0.0, limit=1)
                    qdrant_status = "healthy" if len(test_results) >= 0 else "degraded"  # Even empty results mean it's accessible
                except Exception as e:
                    logger.error(f"Qdrant health check failed: {str(e)}")
                    qdrant_status = "unavailable"
            else:
                logger.error("Retrieve module not available for Qdrant check")
                qdrant_status = "unavailable"

            # Determine overall status based on all services
            overall_status = "healthy"
            if agent_status == "unavailable" or qdrant_status == "unavailable":
                overall_status = "unavailable"
            elif agent_status == "degraded" or qdrant_status == "degraded":
                overall_status = "degraded"

            # Create a health status response
            health_status = HealthStatus(
                status=overall_status,
                timestamp=timestamp,
                services={
                    "agent": {"status": agent_status},
                    "qdrant": {"status": qdrant_status},
                    "api": {"status": api_status}
                },
                version="1.0.0"
            )

            return health_status

        except Exception as e:
            logger.error(f"Health check error: {str(e)}")

            # Return error status
            health_status = HealthStatus(
                status="unavailable",
                timestamp=timestamp,
                services={
                    "agent": {"status": "unavailable"},
                    "qdrant": {"status": "unavailable"},
                    "api": {"status": "unavailable"}
                },
                version="1.0.0"
            )

            return health_status