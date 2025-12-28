import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Configuration settings for the Docusaurus RAG pipeline and FastAPI service."""

    def __init__(self):
        # Cohere Configuration
        self.cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        # Qdrant Configuration
        self.qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")
        self.qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "docusaurus_embeddings")
        self.qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))

        # Crawler Settings
        self.crawler_delay_between_requests: int = int(os.getenv("CRAWLER_DELAY_BETWEEN_REQUESTS", "1"))
        self.crawler_max_concurrent_requests: int = int(os.getenv("CRAWLER_MAX_CONCURRENT_REQUESTS", "5"))
        self.crawler_timeout: int = int(os.getenv("CRAWLER_TIMEOUT", "30"))
        self.crawler_user_agent: str = os.getenv("CRAWLER_USER_AGENT", "Docusaurus-RAG-Crawler/1.0")

        # Embedding Settings
        self.embedding_model: str = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")
        self.embedding_input_type: str = os.getenv("EMBEDDING_INPUT_TYPE", "search_document")
        self.embedding_batch_size: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "96"))

        # Processing Settings
        self.chunk_size_tokens: int = int(os.getenv("CHUNK_SIZE_TOKENS", "512"))
        self.chunk_overlap_tokens: int = int(os.getenv("CHUNK_OVERLAP_TOKENS", "50"))

        # API Configuration
        self.api_title: str = os.getenv("API_TITLE", "RAG Agent API")
        self.api_description: str = os.getenv("API_DESCRIPTION", "API for interacting with the RAG (Retrieval-Augmented Generation) agent")
        self.api_version: str = os.getenv("API_VERSION", "1.0.0")
        self.api_host: str = os.getenv("API_HOST", "0.0.0.0")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))

        # CORS Configuration
        self.cors_origins: str = os.getenv("CORS_ORIGINS", "*")  # In production, replace with specific origins
        self.cors_allow_credentials: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "True").lower() == "true"
        self.cors_allow_methods: str = os.getenv("CORS_ALLOW_METHODS", "*")
        self.cors_allow_headers: str = os.getenv("CORS_ALLOW_HEADERS", "*")

        # Agent Configuration
        self.agent_timeout: int = int(os.getenv("AGENT_TIMEOUT", "30"))  # seconds
        self.max_concurrent_requests: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))

        # Logging Configuration
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.log_format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # OpenRouter Configuration
        self.openrouter_api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")

    def validate(self) -> bool:
        """Validate that all required settings are properly configured."""
        errors = []

        if not self.cohere_api_key:
            errors.append("COHERE_API_KEY is required")

        if not self.qdrant_url:
            errors.append("QDRANT_URL is required")

        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")

        return True


# Create a global settings instance
settings = Settings()