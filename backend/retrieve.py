#!/usr/bin/env python3
"""
RAG Retrieval Pipeline Validation and Testing

This module provides functionality to validate the RAG retrieval system by:
1. Performing semantic similarity searches against Qdrant vector database
2. Verifying retrieved content chunks contain proper metadata
3. Validating embedding consistency between ingestion and retrieval
4. Providing deterministic results for identical queries
"""

import asyncio
import time
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime

import structlog

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


from config.settings import settings
from embeddings.cohere_client import CohereClient
from storage.qdrant_client import QdrantStorage
from models.data_models import ContentChunk


def verify_configurations():
    """Verify Cohere and Qdrant configurations from existing backend settings."""
    logger.info("Verifying Cohere and Qdrant configurations")

    # Check if required settings are available
    cohere_api_key = settings.cohere_api_key
    qdrant_url = settings.qdrant_url
    qdrant_api_key = settings.qdrant_api_key
    qdrant_collection_name = settings.qdrant_collection_name

    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY not found in settings")

    if not qdrant_url:
        raise ValueError("QDRANT_URL not found in settings")

    if not qdrant_api_key:
        raise ValueError("QDRANT_API_KEY not found in settings")

    if not qdrant_collection_name:
        raise ValueError("QDRANT_COLLECTION_NAME not found in settings")

    logger.info("Configuration verification completed",
                qdrant_url=qdrant_url,
                collection=qdrant_collection_name)

    return True


# Import at the end to avoid circular dependencies
if __name__ == "__main__":
    import sys
    import argparse


@dataclass
class SemanticQuery:
    """A text-based search query processed through the embedding model to find semantically similar content."""
    text: str
    embedding_vector: Optional[List[float]] = None
    query_metadata: Optional[Dict[str, Any]] = None


@dataclass
class RetrievedContentChunk:
    """A segment of documentation content retrieved from Qdrant with associated metadata and relevance scoring."""
    id: str
    source_url: str
    title: str
    content: str
    content_hash: str
    relevance_score: float
    word_count: int
    section_path: str
    extracted_at: datetime


@dataclass
class RetrievalResult:
    """Container for results returned by the retrieval system."""
    query: SemanticQuery
    retrieved_chunks: List[RetrievedContentChunk]
    execution_time: float
    total_results: int
    validation_report: Dict[str, Any]


@dataclass
class ValidationError:
    """Represents errors that occur during retrieval validation."""
    error_type: str
    message: str
    timestamp: datetime
    query_context: SemanticQuery


class RetrievalValidator:
    """Main class for validating RAG retrieval pipeline functionality."""

    def __init__(self):
        """Initialize the retrieval validator with necessary clients."""
        self.cohere_client = CohereClient()
        self.qdrant_storage = QdrantStorage()
        self.logger = logger.bind(component="RetrievalValidator")

    async def retrieve_basic(self, query_text: str):
        """
        Create basic retrieval function that connects to Qdrant.

        Args:
            query_text: The query text to retrieve similar content for

        Returns:
            List of retrieved content chunks
        """
        self.logger.info("Starting basic retrieval", query=query_text)

        # Create embedding for the query
        query_embedding = await self._create_query_embedding(query_text)

        # Query Qdrant with the embedding
        retrieved_chunks = await self._query_qdrant(query_embedding, limit=5)

        self.logger.info("Basic retrieval completed", chunk_count=len(retrieved_chunks))
        return retrieved_chunks

    async def semantic_similarity_search(self, query_text: str, limit: int = 5, min_score: float = 0.7) -> RetrievalResult:
        """
        Implement semantic similarity search function that queries Qdrant and returns ranked results.

        Args:
            query_text: The semantic query text to search for
            limit: Maximum number of results to return
            min_score: Minimum relevance score threshold

        Returns:
            RetrievalResult containing the query, results, and validation report
        """
        start_time = time.time()

        # Create semantic query object
        query = self.create_semantic_query(query_text)

        try:
            # Execute Cohere embedding for query text
            query_embedding = await self._create_query_embedding(query_text)
            query.embedding_vector = query_embedding

            # Execute Qdrant query with semantic similarity
            retrieved_chunks = await self._query_qdrant(query_embedding, limit)

            # Filter results by minimum score threshold
            filtered_chunks = self.filter_by_relevance_score(retrieved_chunks, min_score)

            # Sort results by relevance score (descending)
            sorted_chunks = self.rank_results_by_relevance(filtered_chunks)

            execution_time = time.time() - start_time

            # Check embedding consistency
            consistency_result = await self.validate_embedding_consistency()

            # Create validation report
            metrics = {
                "execution_time": execution_time,
                "total_chunks": len(sorted_chunks),
                "metadata_complete": all(self._validate_metadata(chunk) for chunk in sorted_chunks),
                "embedding_consistency": consistency_result["consistency_check"]
            }
            validation_report = self.create_validation_report(
                success=True,
                message=f"Successfully retrieved {len(sorted_chunks)} relevant chunks",
                metrics=metrics
            )

            return RetrievalResult(
                query=query,
                retrieved_chunks=sorted_chunks,
                execution_time=execution_time,
                total_results=len(sorted_chunks),
                validation_report=validation_report
            )

        except Exception as e:
            execution_time = time.time() - start_time

            # Check embedding consistency even in error case
            consistency_result = await self.validate_embedding_consistency()

            metrics = {
                "execution_time": execution_time,
                "total_chunks": 0,
                "metadata_complete": False,
                "embedding_consistency": consistency_result["consistency_check"]
            }
            validation_report = self.create_validation_report(
                success=False,
                message=f"Error during retrieval: {str(e)}",
                metrics=metrics
            )

            # Create an empty query object for error case
            error_query = self.create_semantic_query(query_text)
            error_query.embedding_vector = None

            return RetrievalResult(
                query=error_query,
                retrieved_chunks=[],
                execution_time=execution_time,
                total_results=0,
                validation_report=validation_report
            )

    async def validate_retrieval(self, query_text: str, limit: int = 5, min_score: float = 0.7) -> RetrievalResult:
        """
        Validate retrieval functionality with a semantic query (alias for semantic_similarity_search).

        Args:
            query_text: The semantic query text to validate
            limit: Maximum number of results to return
            min_score: Minimum relevance score threshold

        Returns:
            RetrievalResult containing the query, results, and validation report
        """
        return await self.semantic_similarity_search(query_text, limit, min_score)

    async def execute_cohere_embedding(self, query_text: str) -> List[float]:
        """
        Create function to execute Cohere embedding for query text.

        Args:
            query_text: The text to create an embedding for

        Returns:
            List of float values representing the embedding vector
        """
        self.logger.info("Executing Cohere embedding for query", query=query_text)

        # Use the same embedding parameters as the ingestion pipeline
        embedding_vectors = self.cohere_client.create_embedding_vectors([query_text], query_text)

        if not embedding_vectors or len(embedding_vectors) == 0:
            raise ValueError("Failed to create embedding vector for query")

        self.logger.info("Cohere embedding created successfully", vector_size=len(embedding_vectors[0].vector))
        return embedding_vectors[0].vector

    async def _create_query_embedding(self, query_text: str) -> List[float]:
        """Create embedding vector for query text using Cohere (internal method)."""
        return await self.execute_cohere_embedding(query_text)

    def create_semantic_query(self, query_text: str) -> SemanticQuery:
        """
        Implement semantic query creation using Cohere embeddings.

        Args:
            query_text: The text for the semantic query

        Returns:
            SemanticQuery object with the query text and metadata
        """
        self.logger.info("Creating semantic query object", query=query_text)

        query = SemanticQuery(
            text=query_text,
            query_metadata={
                "created_at": datetime.now().isoformat(),
                "embedding_model": self.cohere_client.model,
                "input_type": self.cohere_client.input_type
            }
        )

        self.logger.info("Semantic query object created", query_id=id(query))
        return query

    async def query_qdrant_semantic_similarity(self, query_embedding: List[float], limit: int) -> List[RetrievedContentChunk]:
        """
        Implement Qdrant query function with semantic similarity.

        Args:
            query_embedding: The embedding vector to search for similar content
            limit: Maximum number of results to return

        Returns:
            List of RetrievedContentChunk objects with semantic similarity matches
        """
        self.logger.info("Querying Qdrant with semantic similarity", vector_size=len(query_embedding), limit=limit)

        try:
            # Use Qdrant's search functionality with the query embedding
            results = self.qdrant_storage.retrieve_similar(query_embedding, limit)

            # Convert results to RetrievedContentChunk objects
            retrieved_chunks = []
            for result in results:
                # result contains: id, score, payload
                payload = result.get('payload', {})

                chunk = RetrievedContentChunk(
                    id=result['id'],
                    source_url=payload.get('source_url', ''),
                    title=payload.get('title', ''),
                    content=payload.get('content_preview', ''),  # Using content_preview from payload
                    content_hash=payload.get('content_hash', ''),
                    relevance_score=result['score'],
                    word_count=payload.get('word_count', 0),
                    section_path=payload.get('section_path', ''),
                    extracted_at=payload.get('extracted_at', datetime.now().isoformat() if hasattr(datetime.now(), 'isoformat') else datetime.now())
                )
                retrieved_chunks.append(chunk)

            self.logger.info("Retrieved chunks from Qdrant", count=len(retrieved_chunks))
            return retrieved_chunks

        except Exception as e:
            self.logger.error("Error querying Qdrant", error=str(e))
            # Instead of raising immediately, create a more descriptive error
            error_msg = f"Qdrant connection error: {str(e)}"
            raise ConnectionError(error_msg) from e

    async def _query_qdrant(self, query_embedding: List[float], limit: int) -> List[RetrievedContentChunk]:
        """Query Qdrant with semantic similarity and return retrieved chunks (internal method)."""
        return await self.query_qdrant_semantic_similarity(query_embedding, limit)

    def _validate_metadata(self, chunk: RetrievedContentChunk) -> bool:
        """Validate that the retrieved chunk contains all required metadata."""
        # Check that required fields exist and are not empty/blank
        required_fields = [
            chunk.source_url,
            chunk.title,
            chunk.content,
            chunk.content_hash
        ]

        # All required fields must be non-empty strings
        for field in required_fields:
            if not isinstance(field, str) or not field.strip():
                return False

        return True

    def rank_results_by_relevance(self, chunks: List[RetrievedContentChunk]) -> List[RetrievedContentChunk]:
        """
        Create helper function for result ranking by relevance score.

        Args:
            chunks: List of RetrievedContentChunk objects to rank

        Returns:
            List of RetrievedContentChunk objects sorted by relevance score (descending)
        """
        self.logger.info("Ranking results by relevance", chunk_count=len(chunks))

        ranked_chunks = sorted(chunks, key=lambda x: x.relevance_score, reverse=True)

        self.logger.info("Results ranked by relevance")
        return ranked_chunks

    def filter_by_relevance_score(self, chunks: List[RetrievedContentChunk], min_score: float) -> List[RetrievedContentChunk]:
        """
        Create helper function for relevance score filtering.

        Args:
            chunks: List of RetrievedContentChunk objects to filter
            min_score: Minimum relevance score threshold

        Returns:
            List of RetrievedContentChunk objects with scores above the threshold
        """
        self.logger.info("Filtering results by relevance score", min_score=min_score, chunk_count=len(chunks))

        filtered_chunks = [chunk for chunk in chunks if chunk.relevance_score >= min_score]

        self.logger.info("Results filtered by relevance score", filtered_count=len(filtered_chunks))
        return filtered_chunks

    def create_validation_report(self, success: bool, message: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Define validation report structure for retrieval results.

        Args:
            success: Whether the validation was successful
            message: Validation result message
            metrics: Additional metrics about the validation

        Returns:
            Dictionary with validation report structure
        """
        self.logger.info("Creating validation report", success=success)

        report = {
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }

        self.logger.info("Validation report created", report=report)
        return report

    async def test_semantic_similarity_validation(self) -> Dict[str, Any]:
        """
        Create test function for semantic similarity validation.

        Returns:
            Dictionary with test results and validation metrics
        """
        self.logger.info("Running semantic similarity validation test")

        try:
            # Run a test query to validate semantic similarity search
            test_query = "What is semantic search?"
            result = await self.semantic_similarity_search(test_query, limit=3, min_score=0.5)

            # Validate the results
            test_metrics = {
                "query_executed": test_query,
                "results_count": result.total_results,
                "execution_time": result.execution_time,
                "validation_success": result.validation_report["success"],
                "metadata_complete": result.validation_report["metrics"]["metadata_complete"],
                "relevance_scores": [chunk.relevance_score for chunk in result.retrieved_chunks]
            }

            # Validate that we got results with good relevance scores
            success = (
                result.total_results > 0 and
                result.validation_report["success"] and
                all(score >= 0.5 for score in test_metrics["relevance_scores"])
            )

            test_result = {
                "test_passed": success,
                "message": f"Semantic similarity validation {'passed' if success else 'failed'}",
                "metrics": test_metrics
            }

            self.logger.info("Semantic similarity validation test completed", test_result=test_result)
            return test_result

        except Exception as e:
            test_result = {
                "test_passed": False,
                "message": f"Semantic similarity validation failed with error: {str(e)}",
                "metrics": {
                    "query_executed": "What is semantic search?",
                    "results_count": 0,
                    "execution_time": 0,
                    "error": str(e)
                }
            }

            self.logger.error("Semantic similarity validation test failed", error=str(e))
            return test_result

    async def validate_embedding_consistency(self) -> Dict[str, Any]:
        """
        Validate embedding consistency between ingestion and retrieval.

        Returns:
            Dictionary with consistency validation results
        """
        try:
            # Get the Cohere model and parameters used for retrieval
            retrieval_model = self.cohere_client.model
            retrieval_input_type = self.cohere_client.input_type

            # For now, assume these match the ingestion parameters
            # In a real implementation, you'd compare with the known ingestion parameters
            ingestion_model = settings.embedding_model
            ingestion_input_type = settings.embedding_input_type

            parameters_match = (
                retrieval_model == ingestion_model and
                retrieval_input_type == ingestion_input_type
            )

            return {
                "consistency_check": parameters_match,
                "ingestion_model": ingestion_model,
                "retrieval_model": retrieval_model,
                "parameters_match": parameters_match,
                "validation_message": "Embedding parameters are consistent" if parameters_match else "Embedding parameters differ between ingestion and retrieval"
            }
        except Exception as e:
            return {
                "consistency_check": False,
                "ingestion_model": "unknown",
                "retrieval_model": "unknown",
                "parameters_match": False,
                "validation_message": f"Error validating consistency: {str(e)}"
            }


async def main():
    """Command-line interface for retrieval validation."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="RAG Retrieval Pipeline Validation")
    parser.add_argument("--query", "-q", type=str, help="The query text to validate")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Maximum number of results to return")
    parser.add_argument("--min-score", "-m", type=float, default=0.7, help="Minimum relevance score threshold")
    parser.add_argument("--validate-consistency", action="store_true", help="Validate embedding consistency only")
    parser.add_argument("--test-semantic", action="store_true", help="Run semantic similarity validation test")

    args = parser.parse_args()

    # If no query is provided and consistency validation is not requested, show help
    if not args.query and not args.validate_consistency and not args.test_semantic:
        parser.print_help()
        sys.exit(1)

    validator = RetrievalValidator()

    if args.validate_consistency:
        # Validate embedding consistency only
        consistency_result = await validator.validate_embedding_consistency()
        print("Embedding Consistency Validation:")
        print(f"  Consistency Check: {consistency_result['consistency_check']}")
        print(f"  Ingestion Model: {consistency_result['ingestion_model']}")
        print(f"  Retrieval Model: {consistency_result['retrieval_model']}")
        print(f"  Parameters Match: {consistency_result['parameters_match']}")
        print(f"  Validation Message: {consistency_result['validation_message']}")
    elif args.test_semantic:
        # Run semantic similarity validation test
        test_result = await validator.test_semantic_similarity_validation()
        print("Semantic Similarity Validation Test:")
        print(f"  Test Passed: {test_result['test_passed']}")
        print(f"  Message: {test_result['message']}")
        print(f"  Metrics: {test_result['metrics']}")
    elif args.query:
        # Perform retrieval validation
        print(f"Starting RAG retrieval validation...")
        print(f"Query: \"{args.query}\"")

        result = await validator.validate_retrieval(args.query, args.limit, args.min_score)

        print(f"Retrieved {result.total_results} chunks with relevance scores:")
        for i, chunk in enumerate(result.retrieved_chunks, 1):
            print(f"{i}. ({chunk.relevance_score:.2f}) {chunk.title} - {chunk.source_url}")

        print(f"\nValidation Report:")
        print(f"  Success: {result.validation_report['success']}")
        print(f"  Message: {result.validation_report['message']}")
        print(f"  Execution Time: {result.execution_time:.2f}s")
        print(f"  Total Chunks: {result.validation_report['metrics']['total_chunks']}")
        print(f"  Metadata Complete: {result.validation_report['metrics']['metadata_complete']}")
        print(f"  Embedding Consistency: {result.validation_report['metrics']['embedding_consistency']}")


# Global cache for clients to avoid multiple Qdrant instances
_client_cache = {}

def retrieve_book_content(query: str, limit: int = 5, min_score: float = 0.7, max_retries: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieve relevant book content based on the query.

    This function provides a simple interface for the RAG agent to retrieve
    content from the Qdrant database with retry logic.

    Args:
        query: The search query to find relevant book content
        limit: Maximum number of results to return (default 5)
        min_score: Minimum relevance score threshold (default 0.7)
        max_retries: Maximum number of retry attempts (default 3)

    Returns:
        List of content chunks with text and metadata
    """
    import logging
    from storage.qdrant_client import QdrantStorage
    from embeddings.cohere_client import CohereClient
    from config.settings import settings

    for attempt in range(max_retries + 1):
        try:
            # Use cached clients if available, otherwise create new ones
            cache_key = "default"

            if cache_key not in _client_cache:
                # Initialize the required clients and store them in cache
                cohere_client = CohereClient()
                qdrant_storage = QdrantStorage()

                _client_cache[cache_key] = {
                    'cohere_client': cohere_client,
                    'qdrant_storage': qdrant_storage
                }
            else:
                # Use cached clients
                cached = _client_cache[cache_key]
                cohere_client = cached['cohere_client']
                qdrant_storage = cached['qdrant_storage']

            # Create embedding for the query
            query_embedding = cohere_client.create_embedding_vectors([query], query)[0].vector

            # Query Qdrant directly
            results = qdrant_storage.retrieve_similar(query_embedding, limit)

            # Convert results to the expected format
            chunks = []
            for result in results:
                payload = result.get('payload', {})

                # Filter by minimum score if needed
                if result['score'] >= min_score:
                    chunk_dict = {
                        "content_id": result['id'],
                        "text": payload.get('content_preview', '') or payload.get('content', '') or payload.get('content_chunk', '') or '',
                        "metadata": {
                            "source_url": payload.get('source_url', ''),
                            "title": payload.get('title', ''),
                            "relevance_score": result['score'],
                            "word_count": payload.get('word_count', 0),
                            "section_path": payload.get('section_path', ''),
                            "extracted_at": payload.get('extracted_at', ''),
                            "content_hash": payload.get('content_hash', ''),
                            "chunk_index": payload.get('chunk_index', 0),
                            "total_chunks": payload.get('total_chunks', 0),
                            "custom_metadata": payload.get('custom_metadata', {})
                        }
                    }
                    chunks.append(chunk_dict)

            logging.info(f"Direct retrieval completed, found {len(chunks)} chunks with score >= {min_score}")
            return chunks

        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries:  # Last attempt
                logging.error("All retry attempts exhausted, returning empty results")
                import traceback
                traceback.print_exc()
                return []
            else:
                import time
                wait_time = 2 ** attempt  # Exponential backoff
                logging.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    # This should never be reached due to the return in the loop, but included for safety
    return []


if __name__ == "__main__":
    asyncio.run(main())