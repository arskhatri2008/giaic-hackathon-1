from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import settings
from config.settings import settings

# Create FastAPI app instance
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# Add CORS middleware
# Parse comma-separated origins or use wildcard
if settings.cors_origins == "*":
    cors_origins = ["*"]
else:
    # Split comma-separated origins and strip whitespace
    cors_origins = [origin.strip() for origin in settings.cors_origins.split(",")]

# Handle methods properly - split comma-separated values if not wildcard
if settings.cors_allow_methods == "*":
    allow_methods = ["*"]
else:
    # Split comma-separated methods and strip whitespace
    allow_methods = [method.strip() for method in settings.cors_allow_methods.split(",")]

# Handle headers properly - split comma-separated values if not wildcard
if settings.cors_allow_headers == "*":
    allow_headers = ["*"]
else:
    # Split comma-separated headers and strip whitespace
    allow_headers = [header.strip() for header in settings.cors_allow_headers.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

# Import routers after app creation to avoid circular imports
from routers.query_router import query_router
from routers.health_router import health_router

# Include routers
app.include_router(query_router, prefix="/api", tags=["query"])
app.include_router(health_router, prefix="/api", tags=["health"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "RAG Agent API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)