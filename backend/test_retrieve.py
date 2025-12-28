#!/usr/bin/env python3
"""
Tests for the RAG retrieval validation functionality.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

from retrieve import RetrievalValidator, SemanticQuery, RetrievedContentChunk, verify_configurations
from datetime import datetime


class TestRetrievalValidator:
    """Test class for the RetrievalValidator functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.validator = RetrievalValidator()

    @pytest.mark.asyncio
    async def test_validate_retrieval_basic(self):
        """Test basic retrieval validation functionality."""
        # Mock the Cohere client to return a sample embedding
        with patch.object(self.validator.cohere_client, 'create_embedding_vectors') as mock_cohere:
            mock_embedding = Mock()
            mock_embedding.vector = [0.1, 0.2, 0.3, 0.4, 0.5]
            mock_cohere.return_value = [mock_embedding]

            # Mock the Qdrant storage to return sample results
            with patch.object(self.validator.qdrant_storage, 'retrieve_similar') as mock_qdrant:
                # Create mock search result in the format expected by retrieve_similar
                mock_result = {
                    "id": "test_id",
                    "score": 0.85,
                    "payload": {
                        "source_url": "https://example.com/test",
                        "title": "Test Title",
                        "content_preview": "Test content for validation",
                        "content_hash": "hash123",
                        "word_count": 5,
                        "section_path": "test-section",
                        "extracted_at": datetime.now().isoformat()
                    }
                }
                mock_qdrant.return_value = [mock_result]

                # Run the validation
                result = await self.validator.validate_retrieval("test query", limit=1, min_score=0.5)

                # Assert the result
                assert result.query.text == "test query"
                assert result.total_results == 1
                assert result.validation_report["success"] is True
                assert len(result.retrieved_chunks) == 1
                assert result.retrieved_chunks[0].title == "Test Title"
                assert result.retrieved_chunks[0].relevance_score == 0.85

    @pytest.mark.asyncio
    async def test_validate_retrieval_with_low_score_filter(self):
        """Test retrieval validation with low score filtering."""
        # Mock the Cohere client to return a sample embedding
        with patch.object(self.validator.cohere_client, 'create_embedding_vectors') as mock_cohere:
            mock_embedding = Mock()
            mock_embedding.vector = [0.1, 0.2, 0.3, 0.4, 0.5]
            mock_cohere.return_value = [mock_embedding]

            # Mock the Qdrant storage to return a result with low score
            with patch.object(self.validator.qdrant_storage, 'retrieve_similar') as mock_qdrant:
                # Create mock search result with low score in the format expected by retrieve_similar
                mock_result = {
                    "id": "test_id",
                    "score": 0.3,  # Below the default 0.7 threshold
                    "payload": {
                        "source_url": "https://example.com/test",
                        "title": "Test Title",
                        "content_preview": "Test content for validation",
                        "content_hash": "hash123",
                        "word_count": 5,
                        "section_path": "test-section",
                        "extracted_at": datetime.now().isoformat()
                    }
                }
                mock_qdrant.return_value = [mock_result]

                # Run the validation with default min_score=0.7
                result = await self.validator.validate_retrieval("test query", limit=1)

                # Assert that the low-scoring result was filtered out
                assert result.total_results == 0
                assert result.validation_report["success"] is True  # Still successful, just no results above threshold

    @pytest.mark.asyncio
    async def test_validate_retrieval_error_handling(self):
        """Test retrieval validation error handling."""
        # Mock the Cohere client to raise an exception
        with patch.object(self.validator.cohere_client, 'create_embedding_vectors') as mock_cohere:
            mock_cohere.side_effect = Exception("Cohere API error")

            # Run the validation
            result = await self.validator.validate_retrieval("test query")

            # Assert the error handling
            assert result.validation_report["success"] is False
            assert "Cohere API error" in result.validation_report["message"]
            assert result.total_results == 0

    def test_validate_metadata_complete(self):
        """Test metadata validation for complete metadata."""
        chunk = RetrievedContentChunk(
            id="test_id",
            source_url="https://example.com/test",
            title="Test Title",
            content="Test content",
            content_hash="hash123",
            relevance_score=0.85,
            word_count=5,
            section_path="test-section",
            extracted_at=datetime.now()
        )

        is_valid = self.validator._validate_metadata(chunk)
        assert is_valid is True

    def test_validate_metadata_incomplete(self):
        """Test metadata validation for incomplete metadata."""
        # Test with empty source_url
        chunk = RetrievedContentChunk(
            id="test_id",
            source_url="",
            title="Test Title",
            content="Test content",
            content_hash="hash123",
            relevance_score=0.85,
            word_count=5,
            section_path="test-section",
            extracted_at=datetime.now()
        )

        is_valid = self.validator._validate_metadata(chunk)
        assert is_valid is False

        # Test with empty title
        chunk = RetrievedContentChunk(
            id="test_id",
            source_url="https://example.com/test",
            title="",
            content="Test content",
            content_hash="hash123",
            relevance_score=0.85,
            word_count=5,
            section_path="test-section",
            extracted_at=datetime.now()
        )

        is_valid = self.validator._validate_metadata(chunk)
        assert is_valid is False

    @pytest.mark.asyncio
    async def test_validate_embedding_consistency(self):
        """Test embedding consistency validation."""
        # Mock the Cohere client properties
        with patch.object(self.validator.cohere_client, 'model', 'embed-english-v3.0'), \
             patch.object(self.validator.cohere_client, 'input_type', 'search_document'), \
             patch('retrieve.settings') as mock_settings:

            mock_settings.embedding_model = 'embed-english-v3.0'
            mock_settings.embedding_input_type = 'search_document'

            consistency_result = await self.validator.validate_embedding_consistency()

            assert consistency_result["consistency_check"] is True
            assert consistency_result["parameters_match"] is True
            assert consistency_result["ingestion_model"] == 'embed-english-v3.0'
            assert consistency_result["retrieval_model"] == 'embed-english-v3.0'

    @pytest.mark.asyncio
    async def test_validate_embedding_consistency_mismatch(self):
        """Test embedding consistency validation with mismatch."""
        # Mock the Cohere client properties to be different from settings
        with patch.object(self.validator.cohere_client, 'model', 'embed-english-v3.0'), \
             patch.object(self.validator.cohere_client, 'input_type', 'search_document'), \
             patch('retrieve.settings') as mock_settings:

            mock_settings.embedding_model = 'embed-multilingual-v2.0'  # Different model
            mock_settings.embedding_input_type = 'search_document'

            consistency_result = await self.validator.validate_embedding_consistency()

            assert consistency_result["consistency_check"] is False
            assert consistency_result["parameters_match"] is False
            assert consistency_result["ingestion_model"] == 'embed-multilingual-v2.0'
            assert consistency_result["retrieval_model"] == 'embed-english-v3.0'

    @pytest.mark.asyncio
    async def test_validate_retrieval_qdrant_connection_error(self):
        """Test retrieval validation with Qdrant connection error."""
        # Mock the Cohere client to return a sample embedding
        with patch.object(self.validator.cohere_client, 'create_embedding_vectors') as mock_cohere:
            mock_embedding = Mock()
            mock_embedding.vector = [0.1, 0.2, 0.3, 0.4, 0.5]
            mock_cohere.return_value = [mock_embedding]

            # Mock the Qdrant storage to raise a connection error
            with patch.object(self.validator.qdrant_storage, 'retrieve_similar') as mock_qdrant:
                mock_qdrant.side_effect = ConnectionError("Qdrant connection failed")

                # Run the validation
                result = await self.validator.validate_retrieval("test query", limit=1, min_score=0.5)

                # Assert the error handling
                assert result.validation_report["success"] is False
                assert "Qdrant connection error" in result.validation_report["message"]
                assert result.total_results == 0

    @pytest.mark.asyncio
    async def test_validate_retrieval_empty_query_handling(self):
        """Test retrieval validation with empty query."""
        # Run the validation with empty query
        result = await self.validator.validate_retrieval("", limit=1, min_score=0.5)

        # Assert that the validation handles empty query appropriately
        # (This depends on the implementation - it might fail or return empty results)
        assert result.validation_report is not None  # Should return a validation report


# Test functions for the verify_configurations function
def test_verify_configurations_success():
    """Test configuration verification with valid settings."""
    with patch('retrieve.settings') as mock_settings:
        mock_settings.cohere_api_key = 'test-key'
        mock_settings.qdrant_url = 'https://test.qdrant.com'
        mock_settings.qdrant_api_key = 'test-qdrant-key'
        mock_settings.qdrant_collection_name = 'test-collection'

        result = verify_configurations()
        assert result is True


def test_verify_configurations_missing_cohere_key():
    """Test configuration verification with missing Cohere API key."""
    with patch('retrieve.settings') as mock_settings:
        mock_settings.cohere_api_key = None  # Missing key
        mock_settings.qdrant_url = 'https://test.qdrant.com'
        mock_settings.qdrant_api_key = 'test-qdrant-key'
        mock_settings.qdrant_collection_name = 'test-collection'

        with pytest.raises(ValueError, match="COHERE_API_KEY not found in settings"):
            verify_configurations()


def test_verify_configurations_missing_qdrant_url():
    """Test configuration verification with missing Qdrant URL."""
    with patch('retrieve.settings') as mock_settings:
        mock_settings.cohere_api_key = 'test-key'
        mock_settings.qdrant_url = None  # Missing URL
        mock_settings.qdrant_api_key = 'test-qdrant-key'
        mock_settings.qdrant_collection_name = 'test-collection'

        with pytest.raises(ValueError, match="QDRANT_URL not found in settings"):
            verify_configurations()


# Integration tests for end-to-end validation (T053)
class TestIntegration:
    """Integration tests for end-to-end validation."""

    @pytest.mark.asyncio
    async def test_end_to_end_retrieval_validation(self):
        """Test complete end-to-end retrieval validation workflow."""
        validator = RetrievalValidator()

        # Mock all dependencies to test the complete workflow
        with patch.object(validator.cohere_client, 'create_embedding_vectors') as mock_cohere, \
             patch.object(validator.qdrant_storage, 'retrieve_similar') as mock_qdrant:

            # Mock embedding response
            mock_embedding = Mock()
            mock_embedding.vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
            mock_cohere.return_value = [mock_embedding]

            # Mock Qdrant response with multiple results
            mock_results = [
                {
                    "id": "chunk_1",
                    "score": 0.85,
                    "payload": {
                        "source_url": "https://example.com/doc1",
                        "title": "Document 1 Title",
                        "content_preview": "This is the content of document 1 for testing purposes.",
                        "content_hash": "hash1",
                        "word_count": 10,
                        "section_path": "section1",
                        "extracted_at": datetime.now().isoformat()
                    }
                },
                {
                    "id": "chunk_2",
                    "score": 0.72,
                    "payload": {
                        "source_url": "https://example.com/doc2",
                        "title": "Document 2 Title",
                        "content_preview": "This is the content of document 2 for testing purposes.",
                        "content_hash": "hash2",
                        "word_count": 12,
                        "section_path": "section2",
                        "extracted_at": datetime.now().isoformat()
                    }
                }
            ]
            mock_qdrant.return_value = mock_results

            # Run end-to-end validation
            result = await validator.validate_retrieval(
                query_text="test semantic search query",
                limit=5,
                min_score=0.7
            )

            # Verify the complete workflow
            assert result.query.text == "test semantic search query"
            assert result.total_results == 2  # Both results above 0.7 threshold
            assert result.validation_report["success"] is True
            assert len(result.retrieved_chunks) == 2
            assert all(chunk.relevance_score >= 0.7 for chunk in result.retrieved_chunks)
            assert result.execution_time > 0
            assert result.validation_report["metrics"]["metadata_complete"] is True
            assert result.validation_report["metrics"]["embedding_consistency"] is True

            # Verify that Cohere and Qdrant were called
            mock_cohere.assert_called_once()
            mock_qdrant.assert_called_once()

    @pytest.mark.asyncio
    async def test_end_to_end_retrieval_with_error_handling(self):
        """Test end-to-end retrieval with error handling scenarios."""
        validator = RetrievalValidator()

        # Test with Cohere error
        with patch.object(validator.cohere_client, 'create_embedding_vectors') as mock_cohere:
            mock_cohere.side_effect = Exception("API Error")

            result = await validator.validate_retrieval("test query")

            assert result.validation_report["success"] is False
            assert "API Error" in result.validation_report["message"]
            assert result.total_results == 0

    @pytest.mark.asyncio
    async def test_end_to_end_retrieval_no_results(self):
        """Test end-to-end retrieval when no results match the criteria."""
        validator = RetrievalValidator()

        with patch.object(validator.cohere_client, 'create_embedding_vectors') as mock_cohere, \
             patch.object(validator.qdrant_storage, 'retrieve_similar') as mock_qdrant:

            # Mock embedding response
            mock_embedding = Mock()
            mock_embedding.vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
            mock_cohere.return_value = [mock_embedding]

            # Mock Qdrant response with low-scoring results
            mock_results = [
                {
                    "id": "chunk_1",
                    "score": 0.3,  # Below threshold
                    "payload": {
                        "source_url": "https://example.com/doc1",
                        "title": "Document 1 Title",
                        "content_preview": "This is the content of document 1 for testing purposes.",
                        "content_hash": "hash1",
                        "word_count": 10,
                        "section_path": "section1",
                        "extracted_at": datetime.now().isoformat()
                    }
                }
            ]
            mock_qdrant.return_value = mock_results

            # Run with high threshold to filter out results
            result = await validator.validate_retrieval(
                query_text="test query",
                limit=5,
                min_score=0.8  # High threshold
            )

            # Should return successful validation but with 0 results
            assert result.validation_report["success"] is True
            assert result.total_results == 0
            assert len(result.retrieved_chunks) == 0
            assert result.execution_time > 0


if __name__ == "__main__":
    pytest.main([__file__])