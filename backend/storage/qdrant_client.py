from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
import structlog
from config.settings import settings
from models.data_models import EmbeddingVector

logger = structlog.get_logger()


class QdrantStorage:
    """Client for storing embeddings in Qdrant vector database."""

    def __init__(self):
        # Initialize Qdrant client based on configuration
        if settings.qdrant_url.startswith('http'):
            # Use HTTP connection
            if settings.qdrant_api_key:
                self.client = QdrantClient(
                    url=settings.qdrant_url,
                    api_key=settings.qdrant_api_key,
                    port=settings.qdrant_port
                )
            else:
                self.client = QdrantClient(
                    url=settings.qdrant_url,
                    port=settings.qdrant_port
                )
        elif settings.qdrant_url.startswith('.') or settings.qdrant_url.startswith('/'):
            # Use local storage mode
            self.client = QdrantClient(path=settings.qdrant_url)
        else:
            # Use local connection via host/port
            if settings.qdrant_api_key:
                self.client = QdrantClient(
                    host=settings.qdrant_url,
                    port=settings.qdrant_port,
                    api_key=settings.qdrant_api_key
                )
            else:
                self.client = QdrantClient(
                    host=settings.qdrant_url,
                    port=settings.qdrant_port
                )

        self.collection_name = settings.qdrant_collection_name

    def ensure_collection_exists(self):
        """
        Ensure the collection exists with the appropriate configuration.
        Creates it if it doesn't exist.
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if self.collection_name not in collection_names:
                logger.info("Creating Qdrant collection", collection=self.collection_name)

                # Create collection with 1024-dimensional vectors (for Cohere embeddings)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1024,  # Cohere embedding dimension
                        distance=models.Distance.COSINE
                    )
                )

                # Create payload index for content_hash to support deduplication
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="content_hash",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                # Create payload index for source_url for efficient retrieval
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="source_url",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                logger.info("Qdrant collection created with schema", collection=self.collection_name)
            else:
                logger.info("Qdrant collection already exists", collection=self.collection_name)

        except Exception as e:
            logger.error("Error ensuring collection exists", collection=self.collection_name, error=str(e))
            raise

    def store_embeddings(self, embedding_vectors: List[EmbeddingVector]) -> bool:
        """
        Store embedding vectors in Qdrant with metadata.
        Implements deduplication using content_hash.
        """
        if not embedding_vectors:
            logger.info("No embeddings to store")
            return True

        logger.info("Starting embedding storage", count=len(embedding_vectors))

        # Prepare points for insertion
        points = []
        skipped_count = 0

        for i, embedding_vector in enumerate(embedding_vectors):
            content_chunk = embedding_vector.content_chunk

            # Check for duplicates using content_hash
            existing_points = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="content_hash",
                            match=models.MatchValue(value=content_chunk.content_hash)
                        )
                    ]
                ),
                limit=1
            )

            if existing_points[0]:  # If duplicate found
                logger.debug("Skipping duplicate content", url=content_chunk.source_url, hash=content_chunk.content_hash)
                skipped_count += 1
                continue

            # Create payload with metadata
            payload = {
                "source_url": content_chunk.source_url,
                "section_path": content_chunk.section_path,
                "title": content_chunk.title,
                "chunk_index": content_chunk.chunk_index,
                "total_chunks": content_chunk.total_chunks,
                "content_hash": content_chunk.content_hash,
                "extracted_at": content_chunk.extracted_at.isoformat() if content_chunk.extracted_at else "",
                "word_count": content_chunk.word_count,
                "content_preview": content_chunk.content[:200],  # First 200 chars for preview
                "custom_metadata": content_chunk.metadata
            }

            # Create point for Qdrant - use the content chunk ID directly (should be UUID)
            point = models.PointStruct(
                id=content_chunk.id,  # Use content_chunk's UUID directly
                vector=embedding_vector.vector,
                payload=payload
            )

            points.append(point)

        if points:
            logger.info(f"Storing {len(points)} embeddings (skipped {skipped_count} duplicates)")

            try:
                # Upload points to Qdrant
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )

                logger.info("Embeddings successfully stored", stored_count=len(points))
            except Exception as e:
                logger.error("Error storing embeddings", error=str(e))
                raise
        else:
            logger.info("All embeddings were duplicates, nothing to store")

        return True

    def retrieve_similar(self, query_vector: List[float], limit: int = 10) -> List[Dict]:
        """
        Retrieve similar embeddings from Qdrant.
        """
        try:
            # Use the query_points method which is available in QdrantClient
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit
            )

            retrieved_items = []
            for result in results.points:
                item = {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload,
                }
                # Add vector only if available in the result
                if hasattr(result, 'vector') and result.vector is not None:
                    item["vector"] = result.vector
                retrieved_items.append(item)

            logger.info("Similarity search completed", result_count=len(retrieved_items))
            return retrieved_items

        except Exception as e:
            logger.error("Error retrieving similar embeddings", error=str(e))
            raise

    def get_embedding_count(self) -> int:
        """
        Get the total count of embeddings in the collection.
        """
        try:
            count = self.client.count(
                collection_name=self.collection_name
            )
            return count.count
        except Exception as e:
            logger.error("Error getting embedding count", error=str(e))
            return 0