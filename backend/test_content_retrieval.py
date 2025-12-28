#!/usr/bin/env python3
"""
Test script to verify that the agent can retrieve and use book content
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from agent import ask_question, health_check

async def test_content_retrieval():
    print("=== Testing Content Retrieval ===")

    # Health check
    health = await health_check()
    print(f"Health: {health['status']}")

    # Test queries that might have relevant content
    test_queries = [
        "What is this book about?",
        "Tell me about the content",
        "What topics are covered?",
        "Give me an overview",
        "What subjects does this discuss?"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing query: '{query}'")
        try:
            response = await ask_question(query)
            print(f"   Response: {response}")

            # Check if response indicates insufficient information
            if "don't have enough information" in response.lower() or "no relevant content" in response.lower():
                print("   Status: No relevant content found")
            else:
                print("   Status: Content found and used in response")
        except Exception as e:
            print(f"   Error: {str(e)}")

    # Test direct retrieval function
    print(f"\n=== Testing Direct Retrieval ===")
    from retrieve import retrieve_book_content

    # Test with lower threshold
    results = retrieve_book_content("book content", min_score=0.3)
    print(f"Direct retrieval with min_score=0.3: {len(results)} chunks retrieved")

    for i, chunk in enumerate(results[:2]):  # Show first 2 results
        print(f"  Chunk {i+1}: {chunk['text'][:150]}...")

if __name__ == "__main__":
    asyncio.run(test_content_retrieval())