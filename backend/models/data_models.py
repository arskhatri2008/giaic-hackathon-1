from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from uuid import uuid4


@dataclass
class ContentChunk:
    """Represents a piece of extracted text from a Docusaurus page with associated metadata."""

    id: str  # Unique identifier (UUID)
    source_url: str  # Original URL of the content
    section_path: str  # Docusaurus section hierarchy (e.g., "module-1/chapter-2")
    title: str  # Page or section title
    content: str  # Clean extracted text content
    chunk_index: int  # Position of this chunk within the document
    total_chunks: int  # Total number of chunks from this document
    content_hash: str  # SHA-256 hash of content for deduplication
    extracted_at: datetime  # Timestamp when content was extracted
    word_count: int  # Number of words in the content
    metadata: Dict  # Additional metadata (custom fields)


@dataclass
class EmbeddingVector:
    """Represents the semantic embedding of a content chunk with associated data."""

    content_chunk: ContentChunk  # Reference to source content
    vector: List[float]  # The embedding vector (e.g., 1024-dimensional)
    model_name: str  # Name of the embedding model used
    model_version: str  # Version of the embedding model
    embedding_created_at: datetime  # Timestamp when embedding was generated
    vector_size: int  # Dimension of the embedding vector


@dataclass
class CrawlJob:
    """Represents a single execution of the ingestion pipeline with configuration and status tracking."""

    id: str  # Unique identifier (UUID)
    name: str  # Human-readable name for the job
    target_urls: List[str]  # List of URLs to crawl
    started_at: datetime  # When the job started
    completed_at: Optional[datetime]  # When the job completed (null if running)
    status: str  # Status: 'pending', 'running', 'completed', 'failed'
    processed_count: int  # Number of pages processed
    successful_count: int  # Number of pages successfully processed
    failed_count: int  # Number of pages that failed processing
    error_details: List[Dict]  # Details of any errors encountered
    configuration: Dict  # Crawl configuration (delays, concurrency, etc.)
    stats: Dict  # Statistics about the crawl (timing, sizes, etc.)

    def __init__(self, name: str, target_urls: List[str]):
        self.id = str(uuid4())
        self.name = name
        self.target_urls = target_urls
        self.started_at = datetime.now()
        self.completed_at = None
        self.status = 'pending'
        self.processed_count = 0
        self.successful_count = 0
        self.failed_count = 0
        self.error_details = []
        self.configuration = {}
        self.stats = {}

    def start_job(self):
        """Mark the job as running."""
        self.status = 'running'
        self.started_at = datetime.now()

    def complete_job(self):
        """Mark the job as completed."""
        self.status = 'completed'
        self.completed_at = datetime.now()

    def fail_job(self, error: str):
        """Mark the job as failed."""
        self.status = 'failed'
        self.completed_at = datetime.now()
        self.error_details.append({
            'timestamp': datetime.now().isoformat(),
            'error': error
        })

    def add_error(self, error: str, url: str = ""):
        """Add an error to the job's error details."""
        self.error_details.append({
            'timestamp': datetime.now().isoformat(),
            'error': error,
            'url': url
        })
        self.failed_count += 1

    def increment_success(self):
        """Increment the successful count."""
        self.successful_count += 1
        self.processed_count += 1

    def increment_processed(self):
        """Increment the processed count."""
        self.processed_count += 1