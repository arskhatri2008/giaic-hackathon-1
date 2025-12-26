#!/usr/bin/env python3
"""
Example script: Basic RAG retrieval validation
"""

import asyncio
import sys
import os

# Add the current directory to the Python path so we can import retrieve module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieve import RetrievalValidator


async def basic_retrieval_example():
    """Example of basic retrieval validation."""
    print("=== Basic RAG Retrieval Validation Example ===\n")

    # Initialize the validator
    validator = RetrievalValidator()

    # Example 1: Basic query
    print("1. Basic Query Example:")
    query_text = "What is machine learning?"

    print(f"   Query: \"{query_text}\"")
    result = await validator.validate_retrieval(query_text, limit=3, min_score=0.6)

    print(f"   Retrieved {result.total_results} chunks:")
    for i, chunk in enumerate(result.retrieved_chunks, 1):
        print(f"     {i}. Score: {chunk.relevance_score:.2f} - {chunk.title}")
        print(f"        URL: {chunk.source_url}")
        print(f"        Content preview: {chunk.content[:100]}...")

    print(f"   Validation Success: {result.validation_report['success']}")
    print(f"   Execution Time: {result.execution_time:.2f}s\n")

    # Example 2: More specific query
    print("2. Specific Query Example:")
    query_text = "How to implement semantic search in RAG systems?"

    print(f"   Query: \"{query_text}\"")
    result = await validator.validate_retrieval(query_text, limit=2, min_score=0.7)

    print(f"   Retrieved {result.total_results} chunks:")
    for i, chunk in enumerate(result.retrieved_chunks, 1):
        print(f"     {i}. Score: {chunk.relevance_score:.2f} - {chunk.title}")
        print(f"        URL: {chunk.source_url}")

    print(f"   Validation Success: {result.validation_report['success']}")
    print(f"   Execution Time: {result.execution_time:.2f}s\n")


if __name__ == "__main__":
    asyncio.run(basic_retrieval_example())