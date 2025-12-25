import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from models.data_models import ContentChunk, EmbeddingVector, CrawlJob
from utils.helpers import calculate_content_hash, validate_content, clean_text, chunk_text, count_words, normalize_text
from config.settings import settings


class TestContentChunk:
    """Test cases for ContentChunk data model."""

    def test_content_chunk_creation(self):
        """Test ContentChunk can be created with required fields."""
        chunk = ContentChunk(
            id="test-id",
            source_url="https://example.com",
            section_path="test/section",
            title="Test Title",
            content="Test content",
            chunk_index=0,
            total_chunks=1,
            content_hash="test-hash",
            extracted_at=None,
            word_count=2,
            metadata={}
        )

        assert chunk.id == "test-id"
        assert chunk.source_url == "https://example.com"
        assert chunk.content == "Test content"


class TestUtils:
    """Test cases for utility functions."""

    def test_calculate_content_hash(self):
        """Test content hash calculation."""
        content = "test content"
        hash_value = calculate_content_hash(content)

        # Hash should be a 64-character hex string
        assert len(hash_value) == 64
        assert all(c in '0123456789abcdef' for c in hash_value)

        # Same content should produce same hash
        same_hash = calculate_content_hash("test content")
        assert hash_value == same_hash

        # Different content should produce different hash
        diff_hash = calculate_content_hash("different content")
        assert hash_value != diff_hash

    def test_validate_content(self):
        """Test content validation."""
        # Valid content should pass
        assert validate_content("This is valid content with enough length", min_length=10) == True

        # Short content should fail
        assert validate_content("Short", min_length=10) == False

        # Empty content should fail
        assert validate_content("") == False
        assert validate_content(None) == False

    def test_clean_text(self):
        """Test text cleaning."""
        dirty_text = "  This   has   extra   spaces  \n\t and\ttabs\n\n"
        clean = clean_text(dirty_text)

        # Should have single spaces, no leading/trailing whitespace
        assert clean == "This has extra spaces and tabs"

    def test_chunk_text(self):
        """Test text chunking."""
        text = "word " * 100  # 100 words
        chunks = chunk_text(text, chunk_size=50, overlap=10)

        # Should have 2 chunks with overlap
        assert len(chunks) == 2

        # First chunk should be ~50 words
        assert len(chunks[0].split()) <= 50

        # Second chunk should start with overlapping words
        first_chunk_words = set(chunks[0].split()[-10:])  # Last 10 words of first chunk
        second_chunk_words = set(chunks[1].split()[:20])  # First 20 words of second chunk

        # There should be overlap
        overlap = first_chunk_words.intersection(second_chunk_words)
        assert len(overlap) > 0

    def test_count_words(self):
        """Test word counting."""
        assert count_words("This has five words") == 5
        assert count_words("") == 0
        assert count_words("   ") == 0
        assert count_words("One") == 1

    def test_normalize_text(self):
        """Test text normalization."""
        dirty_text = "  This   text   has   issues  \n\t and\tformatting\n\n"
        normalized = normalize_text(dirty_text)

        # Should be cleaned and normalized
        assert normalized == "This text has issues and formatting"


class TestCrawlJob:
    """Test cases for CrawlJob data model."""

    def test_crawl_job_creation(self):
        """Test CrawlJob can be created with required fields."""
        job = CrawlJob("test-job", ["https://example.com"])

        assert job.name == "test-job"
        assert job.target_urls == ["https://example.com"]
        assert job.status == 'pending'
        assert job.processed_count == 0
        assert job.successful_count == 0
        assert job.failed_count == 0

    def test_crawl_job_lifecycle(self):
        """Test CrawlJob lifecycle methods."""
        job = CrawlJob("test-job", ["https://example.com"])

        # Start the job
        job.start_job()
        assert job.status == 'running'

        # Add some successful items
        job.increment_success()
        job.increment_success()
        assert job.successful_count == 2
        assert job.processed_count == 2

        # Add some errors
        job.add_error("Test error", "https://example.com/page")
        assert job.failed_count == 1
        assert len(job.error_details) == 1

        # Complete the job
        job.complete_job()
        assert job.status == 'completed'


if __name__ == "__main__":
    pytest.main([__file__])