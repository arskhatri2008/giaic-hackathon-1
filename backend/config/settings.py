import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Configuration settings for the Docusaurus RAG pipeline."""

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