#!/usr/bin/env python3
"""Direct test to verify the retrieval and tool calling components work"""

import asyncio
from retrieve import retrieve_book_content

async def test_retrieval_directly():
    """Test the retrieval function directly"""
    print("=== Testing retrieval function directly ===")

    # Test with a query that should match ROS 2 content
    query = "What is ROS 2?"
    results = retrieve_book_content(query, min_score=0.3)

    print(f"Query: {query}")
    print(f"Retrieved {len(results)} chunks")

    for i, chunk in enumerate(results[:2]):  # Show first 2 chunks
        print(f"Chunk {i+1}:")
        print(f"  Title: {chunk['metadata']['title']}")
        print(f"  Score: {chunk['metadata']['relevance_score']}")
        print(f"  Content preview: {chunk['text'][:100]}...")
        print()

    return len(results) > 0

def test_tool_function():
    """Test the tool function directly"""
    print("=== Testing tool function directly ===")

    # Import the tool function
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from agent import retrieve_book_content_tool

    query = "What is ROS 2?"
    results = retrieve_book_content_tool(query)

    print(f"Tool query: {query}")
    print(f"Tool returned {len(results)} chunks")

    for i, chunk in enumerate(results[:2]):  # Show first 2 chunks
        print(f"Tool Chunk {i+1}:")
        print(f"  Content ID: {chunk['content_id']}")
        print(f"  Metadata: {chunk['metadata']}")
        print(f"  Content preview: {chunk['text'][:100]}...")
        print()

    return len(results) > 0

if __name__ == "__main__":
    print("Direct system test\n")

    # Test retrieval directly
    retrieval_success = asyncio.run(test_retrieval_directly())

    # Test tool function
    tool_success = test_tool_function()

    print("=== Summary ===")
    print(f"Direct retrieval: {'✓ SUCCESS' if retrieval_success else '✗ FAILED'}")
    print(f"Tool function: {'✓ SUCCESS' if tool_success else '✗ FAILED'}")

    if retrieval_success and tool_success:
        print("\nThe retrieval system is working correctly!")
        print("The issue is likely in how the agent processes tool results,")
        print("not in the retrieval or tool calling components themselves.")
    else:
        print("\nThere are issues with the retrieval components.")