import asyncio
import click
from typing import List
import structlog
import logging
from crawlers.docusaurus_crawler import DocusaurusCrawler
from embeddings.cohere_client import CohereClient
from storage.qdrant_client import QdrantStorage
from config.settings import settings
from models.data_models import CrawlJob

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

@click.command()
@click.option('--urls', '-u', multiple=True, help='Target URLs to crawl')
@click.option('--collection-name', default='docusaurus_embeddings', help='Qdrant collection name')
@click.option('--chunk-size', default=512, help='Target chunk size in tokens')
@click.option('--max-concurrent', default=5, help='Max concurrent requests')
def main(urls: List[str], collection_name: str, chunk_size: int, max_concurrent: int):
    """
    RAG ingestion pipeline for Docusaurus book content.
    Crawls Docusaurus websites, generates embeddings, and stores them in Qdrant.
    """
    logger.info("Starting Docusaurus RAG ingestion pipeline",
                urls=urls, collection=collection_name, chunk_size=chunk_size)

    if not urls:
        logger.error("No URLs provided. Use --urls to specify target URLs to crawl.")
        return

    # Update collection name if provided
    if collection_name != 'docusaurus_embeddings':
        settings.qdrant_collection_name = collection_name

    logger.info(f"Pipeline configured with {len(urls)} URLs to process")

    # Run the pipeline
    asyncio.run(run_pipeline(urls, collection_name))


async def run_pipeline(urls: List[str], collection_name: str):
    """Run the complete Docusaurus RAG pipeline."""
    # Create a job tracker
    job = CrawlJob("docusaurus-rag-pipeline", urls)
    job.start_job()

    try:
        logger.info("Initializing Docusaurus crawler")
        crawler = DocusaurusCrawler()

        logger.info("Starting crawl process", urls=urls)
        content_chunks = await crawler.crawl(urls)

        logger.info("Crawling completed", chunk_count=len(content_chunks))
        job.stats['crawled_chunks'] = len(content_chunks)

        if not content_chunks:
            logger.warning("No content extracted, stopping pipeline")
            job.fail_job("No content extracted from provided URLs")
            return

        # Generate embeddings
        logger.info("Initializing Cohere client for embedding generation")
        cohere_client = CohereClient()

        # Extract text content from chunks for embedding
        texts = [chunk.content for chunk in content_chunks]
        logger.info("Starting embedding generation", text_count=len(texts))

        embedding_vectors = cohere_client.create_embedding_vectors(texts, urls[0] if urls else "")

        logger.info("Embedding generation completed", vector_count=len(embedding_vectors))
        job.stats['generated_embeddings'] = len(embedding_vectors)

        # Store embeddings in Qdrant
        logger.info("Initializing Qdrant storage")
        qdrant_storage = QdrantStorage()

        # Ensure collection exists
        qdrant_storage.ensure_collection_exists()

        logger.info("Storing embeddings in Qdrant", vector_count=len(embedding_vectors))
        success = qdrant_storage.store_embeddings(embedding_vectors)

        if success:
            final_count = qdrant_storage.get_embedding_count()
            job.stats['stored_embeddings'] = final_count
            logger.info("Embeddings successfully stored in Qdrant", total_count=final_count)

        # Print summary
        for i, (chunk, vector) in enumerate(zip(content_chunks[:3], embedding_vectors[:3])):  # Show first 3 as sample
            logger.info(f"Stored chunk {i+1}", url=chunk.source_url, title=chunk.title,
                       content_length=len(chunk.content), vector_size=vector.vector_size)

        if len(embedding_vectors) > 3:
            logger.info(f"... and {len(embedding_vectors) - 3} more embeddings stored")

        # Complete the job
        job.complete_job()
        logger.info("Pipeline completed successfully",
                   stats=job.stats,
                   processed=job.processed_count,
                   successful=job.successful_count,
                   failed=job.failed_count)

    except Exception as e:
        logger.error("Pipeline failed", error=str(e))
        job.fail_job(str(e))
        raise


if __name__ == "__main__":
    main()