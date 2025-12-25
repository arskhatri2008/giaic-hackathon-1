import cohere
from typing import List, Dict, Optional
import structlog
import time
from config.settings import settings
from models.data_models import EmbeddingVector
from utils.helpers import normalize_text

logger = structlog.get_logger()


class CohereClient:
    """Client for interacting with Cohere API to generate embeddings."""

    def __init__(self):
        if not settings.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(settings.cohere_api_key)
        self.model = settings.embedding_model
        self.input_type = settings.embedding_input_type
        self.batch_size = settings.embedding_batch_size
        # Rate limiting: requests per minute
        self.requests_per_minute = 60  # Default, can be adjusted based on plan
        self.min_request_interval = 60.0 / self.requests_per_minute

    def _make_request_with_retry(self, func, max_retries=3, base_delay=1):
        """
        Make a request with exponential backoff retry logic.
        """
        for attempt in range(max_retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries:
                    # Final attempt failed, raise the exception
                    logger.error("Max retries reached for Cohere API request",
                                error=str(e), attempts=attempt + 1)
                    raise e
                else:
                    # Calculate delay with exponential backoff
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Request failed, retrying in {delay}s",
                                  attempt=attempt + 1, error=str(e))
                    time.sleep(delay)

    def _rate_limit(self, last_request_time: Optional[float]) -> float:
        """
        Implement rate limiting to respect API quotas.
        """
        current_time = time.time()
        if last_request_time is not None:
            elapsed = current_time - last_request_time
            if elapsed < self.min_request_interval:
                sleep_time = self.min_request_interval - elapsed
                time.sleep(sleep_time)
                current_time = time.time()

        return current_time

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        Handles batching internally to respect API limits.
        """
        all_embeddings = []
        last_request_time = None

        # Process in batches to respect API limits
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            logger.info(f"Processing embedding batch {i//self.batch_size + 1}",
                       batch_size=len(batch))

            # Apply rate limiting
            last_request_time = self._rate_limit(last_request_time)

            # Make request with retry logic
            def make_embedding_request():
                return self.client.embed(
                    texts=batch,
                    model=self.model,
                    input_type=self.input_type
                )

            try:
                response = self._make_request_with_retry(make_embedding_request)

                # Extract embeddings from response
                batch_embeddings = response.embeddings
                all_embeddings.extend(batch_embeddings)

                logger.info(f"Completed embedding batch {i//self.batch_size + 1}",
                           embeddings_count=len(batch_embeddings))

                # Update last request time
                last_request_time = time.time()

            except Exception as e:
                logger.error("Error generating embeddings for batch",
                            batch_start=i, batch_size=len(batch), error=str(e))
                # Raise the exception to halt processing if embeddings fail
                raise

        return all_embeddings

    def create_embedding_vectors(self, texts: List[str]) -> List[EmbeddingVector]:
        """
        Create EmbeddingVector objects from texts by generating embeddings.
        """
        logger.info("Creating embedding vectors", text_count=len(texts))

        # Normalize texts before embedding
        normalized_texts = [normalize_text(text) for text in texts]

        # Generate embeddings
        embeddings = self.generate_embeddings(normalized_texts)

        # Create EmbeddingVector objects
        embedding_vectors = []
        for i, (text, embedding) in enumerate(zip(normalized_texts, embeddings)):
            # Create a minimal ContentChunk for the embedding vector
            # In a full implementation, we'd have proper ContentChunk objects
            from models.data_models import ContentChunk
            from datetime import datetime

            content_chunk = ContentChunk(
                id=f"temp_chunk_{i}",
                source_url="",
                section_path="",
                title="",
                content=text,
                chunk_index=0,
                total_chunks=1,
                content_hash="",
                extracted_at=datetime.now(),
                word_count=len(text.split()),
                metadata={}
            )

            embedding_vector = EmbeddingVector(
                content_chunk=content_chunk,
                vector=embedding,
                model_name=self.model,
                model_version="",  # Cohere doesn't provide version in response
                embedding_created_at=datetime.now(),
                vector_size=len(embedding)
            )

            embedding_vectors.append(embedding_vector)

        logger.info("Created embedding vectors", vector_count=len(embedding_vectors))
        return embedding_vectors

    def validate_embedding(self, embedding: List[float]) -> bool:
        """
        Validate that an embedding has the expected properties.
        """
        if not isinstance(embedding, list):
            logger.error("Embedding is not a list", embedding_type=type(embedding))
            return False

        expected_size = 1024  # Cohere's default embedding size for most models
        if len(embedding) != expected_size:
            logger.error("Embedding has incorrect size",
                        actual_size=len(embedding), expected_size=expected_size)
            return False

        # Check that all values are floats
        if not all(isinstance(val, (int, float)) for val in embedding):
            logger.error("Embedding contains non-numeric values")
            return False

        return True