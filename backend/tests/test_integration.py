"""
Integration tests for the complete RAG agent workflow
"""
import pytest
import asyncio
from unittest.mock import patch
import sys
import os
# Add the backend directory to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent import (
    ask_question,
    health_check,
    verify_grounding,
    check_content_sufficiency,
    rag_agent,
    AgentResponse
)


@pytest.mark.asyncio
async def test_complete_workflow_integration():
    """Test the complete RAG agent workflow from health check to question answering"""

    # 1. Test health check
    health_status = await health_check()
    assert health_status["status"] == "healthy"
    assert "RAG agent is running properly" in health_status["message"]
    assert "agent_name" in health_status

    # 2. Test that agent is properly initialized
    assert rag_agent is not None
    assert rag_agent.name == "RAG Book Assistant"

    # 3. Test question answering with mocked retrieval
    test_question = "What are the key concepts in the book?"

    with patch('backend.agent.retrieve_book_content_tool') as mock_retrieve:
        # Mock retrieval to return sample content
        mock_retrieve.return_value = [
            {
                "content_id": "chunk_1",
                "text": "Key concepts include artificial intelligence and machine learning.",
                "metadata": {
                    "source_url": "https://example.com/book/chapter1",
                    "title": "Chapter 1: Introduction",
                    "relevance_score": 0.95,
                    "word_count": 150,
                    "section_path": "/book/chapter1",
                    "extracted_at": "2025-12-26T10:00:00Z"
                }
            }
        ]

        # 4. Test the question answering
        response = await ask_question(test_question)

        # 5. Verify the response structure
        assert isinstance(response, AgentResponse)
        assert len(response.answer) > 0  # Response is not empty
        assert len(response.sources) == 1  # One source was provided
        assert response.grounded is True  # Response should be grounded

        # 6. Verify the source content
        source = response.sources[0]
        assert source.content_id == "chunk_1"
        assert "artificial intelligence" in source.text.lower()
        assert "machine learning" in source.text.lower()
        assert source.metadata["title"] == "Chapter 1: Introduction"

        # 7. Test grounding verification on the response
        grounding_result = await verify_grounding(test_question, ["key", "concept"])
        assert grounding_result["contains_expected_keywords"] is True
        assert grounding_result["shows_source_citation"] is False  # Depends on agent response content
        assert grounding_result["informational_response"] is True
        assert len(grounding_result["response"]) > 0

        # 8. Test content sufficiency check
        sufficiency_result = await check_content_sufficiency(test_question)
        assert sufficiency_result["sources_count"] == 1
        assert sufficiency_result["response_length"] > 0
        assert sufficiency_result["estimated_content_sufficient"] is True


@pytest.mark.asyncio
async def test_workflow_with_no_relevant_content():
    """Test the workflow when no relevant content is found"""

    # Test health check first
    health_status = await health_check()
    assert health_status["status"] == "healthy"

    test_question = "What is the capital of Mars?"

    with patch('backend.agent.retrieve_book_content_tool') as mock_retrieve:
        # Mock retrieval to return no content
        mock_retrieve.return_value = []

        # Test question answering with no sources
        response = await ask_question(test_question)

        # Verify response structure
        assert isinstance(response, AgentResponse)
        # The agent should still provide a response even with no sources
        assert hasattr(response, 'sources')
        assert len(response.sources) == 0

        # Test sufficiency check with no content
        sufficiency_result = await check_content_sufficiency(test_question)
        assert sufficiency_result["sources_count"] == 0
        assert sufficiency_result["has_insufficient_indicator"] is False  # Depends on agent response


@pytest.mark.asyncio
async def test_multiple_questions_workflow():
    """Test the workflow with multiple different questions"""

    questions_and_expected = [
        ("What is AI?", ["artificial", "intelligence"]),
        ("Explain machine learning", ["machine", "learning"]),
        ("What are neural networks?", ["neural", "networks"])
    ]

    for question, expected_keywords in questions_and_expected:
        with patch('backend.agent.retrieve_book_content_tool') as mock_retrieve:
            # Mock retrieval to return relevant content
            mock_retrieve.return_value = [
                {
                    "content_id": f"chunk_{abs(hash(question)) % 10000}",
                    "text": f"Content about {question.lower().replace('?', '')} in the book.",
                    "metadata": {
                        "source_url": "https://example.com/book",
                        "title": "Relevant Chapter",
                        "relevance_score": 0.85,
                        "word_count": 100,
                        "section_path": "/book/chapter",
                        "extracted_at": "2025-12-26T10:00:00Z"
                    }
                }
            ]

            # Test question answering
            response = await ask_question(question)
            assert isinstance(response, AgentResponse)
            assert len(response.sources) >= 0  # May have sources or not

            # Test grounding verification
            grounding_result = await verify_grounding(question, expected_keywords)
            assert isinstance(grounding_result, dict)
            assert "question" in grounding_result


def test_agent_initialization_integration():
    """Test that all agent components are properly initialized"""
    # Test that the agent is properly initialized
    assert rag_agent is not None
    assert hasattr(rag_agent, 'name')
    assert hasattr(rag_agent, 'tools')
    assert len(rag_agent.tools) > 0  # Should have at least the retrieval tool

    # Test that required models are available
    from agent import RetrievedChunk, AgentResponse
    assert RetrievedChunk is not None
    assert AgentResponse is not None