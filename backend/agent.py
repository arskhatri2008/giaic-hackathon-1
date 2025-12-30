"""
RAG Agent Implementation using OpenAI Agents SDK

This module implements a RAG-enabled agent that can answer questions about book content
by retrieving relevant information from a Qdrant-based knowledge base.

Usage Examples:
    # Basic usage
    from agent import ask_question
    import asyncio

    async def main():
        response = await ask_question("What are the key concepts in the book?")
        print(response.answer)
        print(f"Sources: {len(response.sources)} chunks")

    asyncio.run(main())

    # Health check
    from agent import health_check
    import asyncio

    async def check_health():
        status = await health_check()
        print(status)

    asyncio.run(check_health())

    # Grounding verification
    from agent import verify_grounding
    import asyncio

    async def verify_response():
        result = await verify_grounding("What is AI?", ["artificial", "intelligence"])
        print(result)

    asyncio.run(verify_response())
"""

import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging
from openai import AsyncOpenAI


# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


class RetrievedChunk(BaseModel):
    """Model for a retrieved content chunk"""
    content_id: str
    text: str
    metadata: Dict[str, Any]


class AgentResponse(BaseModel):
    """Model for agent responses with source information"""
    answer: str
    sources: List[RetrievedChunk]
    grounded: bool

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the existing retrieve function from the retrieval pipeline
import sys
import os
sys.path.append(os.path.dirname(__file__))  # Add current directory to path
from retrieve import retrieve_book_content


# Global counter to track tool calls during a single query processing
_tool_call_count = 0
_TOOL_CALL_LIMIT = 3  # Maximum number of times the tool can be called per query

def retrieve_book_content_tool(query: str) -> List[Dict[str, Any]]:
    """
    Retrieve relevant book content based on the query.

    Args:
        query: The search query to find relevant book content

    Returns:
        List of content chunks with text and metadata
    """
    global _tool_call_count
    _tool_call_count += 1

    if _tool_call_count > _TOOL_CALL_LIMIT:
        logger.warning(f"Tool call limit reached ({_TOOL_CALL_LIMIT}), returning empty results")
        return []

    logger.info(f"Retrieving content for query: {query} (call #{_tool_call_count})")
    try:
        # Lower the minimum score threshold to allow more content to be retrieved
        results = retrieve_book_content(query, limit=5, min_score=0.1)  # Lowered from default 0.7, increased limit
        logger.info(f"Retrieved {len(results)} content chunks for query: {query}")
        # Return the results directly as the tool output
        return results
    except Exception as e:
        logger.error(f"Error retrieving content for query '{query}': {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def reset_tool_call_counter():
    """Reset the tool call counter for a new query"""
    global _tool_call_count
    _tool_call_count = 0


# Simple RAG agent implementation using OpenAI API with function calling
async def simple_rag_agent(question: str) -> str:
    """
    Simple RAG agent that retrieves content and sends it to OpenAI for response generation.
    """
    try:
        # Retrieve relevant content
        retrieved_content = retrieve_book_content_tool(question)

        if not retrieved_content:
            return "I couldn't find any relevant content to answer your question about that topic."

        # Format the retrieved content for context
        context_text = "Here is the relevant information I found:\n\n"
        for i, chunk in enumerate(retrieved_content):
            context_text += f"Source {i+1}:\n"
            context_text += f"Title: {chunk.get('metadata', {}).get('title', 'No title')}\n"
            context_text += f"URL: {chunk.get('metadata', {}).get('source_url', 'No URL')}\n"
            context_text += f"Content: {chunk.get('text', '')}\n\n"

        # Create the full prompt with context
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided context. Only use information from the provided context to answer questions. If the context doesn't contain information to answer the question, say so clearly. Always cite the source when providing information."
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {question}\n\nPlease provide a detailed answer based on the context, citing the sources when possible."
            }
        ]

        # Call the OpenAI API
        response = await client.chat.completions.create(
            model="xiaomi/mimo-v2-flash:free",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Error in simple RAG agent: {str(e)}")
        return "I encountered an error processing your question. Please try again."


import time

async def ask_question(question: str) -> str:
    """
    Ask a question to the RAG agent and get a response.

    Args:
        question: The question to ask about the book content

    Returns:
        String response from the agent
    """
    start_time = time.time()
    logger.info(f"Processing question: {question}")

    # Reset the tool call counter for this new query
    reset_tool_call_counter()

    try:
        # Use the simple RAG agent instead of the Runner
        response = await simple_rag_agent(question)
        end_time = time.time()
        processing_time = end_time - start_time
        logger.info(f"Successfully processed question in {processing_time:.2f}s: {question[:50]}...")

        # Reset the tool call counter after processing
        reset_tool_call_counter()

        return response
    except Exception as e:
        end_time = time.time()
        processing_time = end_time - start_time
        logger.error(f"Error processing question '{question}' after {processing_time:.2f}s: {str(e)}")
        # Reset the tool call counter even in case of error
        reset_tool_call_counter()
        # Return a default response in case of error
        return "I'm sorry, I encountered an error processing your question."


async def verify_grounding(question: str, expected_keywords: list = None) -> dict:
    """
    Verify that the agent's response is grounded in retrieved content.

    Args:
        question: The question to ask
        expected_keywords: Optional list of keywords that should appear in the response if properly grounded

    Returns:
        Dictionary with verification results
    """
    # First, get the agent response
    answer_text = await ask_question(question)

    # Check if the response contains expected keywords if provided
    keyword_check = True
    if expected_keywords:
        keyword_check = any(keyword.lower() in answer_text.lower() for keyword in expected_keywords)

    # Additional grounding checks
    source_citation_check = any(
        phrase in answer_text.lower() for phrase in
        ["source:", "according to", "cited from", "retrieved", "found in", "reference"]
    )

    # Check if response seems to reference specific information
    informational_check = len(answer_text) > 20  # Basic check for substantive response

    # Return verification results
    return {
        "question": question,
        "response": answer_text,
        "sources_count": 0,  # Cannot determine without structured response
        "contains_expected_keywords": keyword_check,
        "shows_source_citation": source_citation_check,
        "informational_response": informational_check,
        "grounding_verification": "completed"
    }


async def check_content_sufficiency(query: str, min_chunks: int = 1, min_relevance_score: float = 0.5) -> dict:
    """
    Check if the retrieved content is sufficient to answer the query.

    Args:
        query: The query to check content sufficiency for
        min_chunks: Minimum number of content chunks required
        min_relevance_score: Minimum relevance score for content to be considered sufficient

    Returns:
        Dictionary with sufficiency check results
    """
    # Get the agent response
    answer_text = await ask_question(query)

    # Check if the response indicates insufficient information
    insufficient_indicators = [
        "insufficient information",
        "not enough information",
        "no relevant content",
        "don't have enough information",
        "unable to find",
        "not mentioned in the provided content"
    ]

    has_insufficient_indicator = any(indicator.lower() in answer_text.lower()
                                   for indicator in insufficient_indicators)

    # Estimate content sufficiency based on response characteristics
    content_sufficient = not has_insufficient_indicator and len(answer_text) > 50

    return {
        "query": query,
        "response_length": len(answer_text),
        "sources_count": 0,  # Cannot determine without structured response
        "has_insufficient_indicator": has_insufficient_indicator,
        "estimated_content_sufficient": content_sufficient,
        "sufficiency_check": "completed"
    }


async def test_agent_retrieval(query: str) -> dict:
    """
    Test the agent's ability to invoke retrieval tool with various queries.

    Args:
        query: The query to test

    Returns:
        Dictionary with test results
    """
    try:
        # This function will be used to test retrieval
        response_text = await ask_question(query)
        return {
            "query": query,
            "response_length": len(response_text),
            "sources_count": 0,  # Cannot determine without structured response
            "success": True,
            "response": response_text,
            "sources": []  # Cannot determine without structured response
        }
    except Exception as e:
        return {
            "query": query,
            "success": False,
            "error": str(e)
        }


async def health_check() -> dict:
    """
    Health check function to verify the agent is running properly.

    Returns:
        Dictionary with health status information
    """
    import time
    start_time = time.time()

    try:
        # Test that the retrieval function works
        # We'll test by trying to retrieve content with a simple query
        from retrieve import retrieve_book_content
        test_retrieval = retrieve_book_content("test", limit=1, min_score=0.0)

        # If we get here, the basic functionality is working
        end_time = time.time()
        return {
            "status": "healthy",
            "message": "RAG agent is running properly",
            "retrieval_available": True,
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "response_time": end_time - start_time
        }

    except Exception as e:
        end_time = time.time()
        return {
            "status": "error",
            "message": f"Health check failed: {str(e)}",
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "response_time": end_time - start_time
        }


async def main():
    """Example usage and testing of the RAG agent"""
    # Run health check first
    health_status = await health_check()
    print(f"Health Check: {health_status}")

    if health_status["status"] != "healthy":
        print("Agent is not healthy, stopping execution")
        return

    # Test basic functionality
    question = "What are the key concepts in the book?"
    response_text = await ask_question(question)
    print(f"\nResponse: {response_text}")
    print(f"Response length: {len(response_text)} characters")

    # Test grounding verification
    grounding_result = await verify_grounding(question, ["key", "concept"])
    print(f"\nGrounding verification: {grounding_result}")

    # Test content sufficiency
    sufficiency_result = await check_content_sufficiency(question)
    print(f"\nContent sufficiency check: {sufficiency_result}")

    # Test with various queries
    test_queries = [
        "What is the main topic?",
        "Can you summarize the content?",
        "Tell me about the book"
    ]

    print("\nTesting various queries:")
    for query in test_queries:
        test_result = await test_agent_retrieval(query)
        sufficiency_check = await check_content_sufficiency(query)
        print(f"Query: {query}")
        print(f"Result: {test_result}")
        print(f"Sufficiency: {sufficiency_check}")
        print("---")

    # Test with a query that might have no relevant content
    print("\nTesting with potentially irrelevant query:")
    no_content_query = "What is the capital of Mars?"
    no_content_result = await test_agent_retrieval(no_content_query)
    no_content_sufficiency = await check_content_sufficiency(no_content_query)
    print(f"Query: {no_content_query}")
    print(f"Result: {no_content_result}")
    print(f"Sufficiency: {no_content_sufficiency}")


if __name__ == "__main__":
    asyncio.run(main())