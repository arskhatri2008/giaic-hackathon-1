#!/usr/bin/env python3
"""
Test script to verify that the retrieval function works with the event loop fix
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from retrieve import retrieve_book_content
from agent import ask_question

async def test_retrieval_directly():
    """Test the retrieval function directly"""
    print("Testing retrieval function directly...")

    try:
        results = retrieve_book_content("artificial intelligence", limit=3)
        print(f"Direct retrieval results: {len(results)} chunks retrieved")
        for i, chunk in enumerate(results[:2]):  # Show first 2 results
            print(f"  Chunk {i+1}: {chunk['text'][:100]}...")
    except Exception as e:
        print(f"Direct retrieval error: {str(e)}")

async def test_retrieval_via_agent():
    """Test the retrieval function via the agent (which causes the event loop issue)"""
    print("\nTesting retrieval via agent...")

    try:
        response = await ask_question("What is artificial intelligence?")
        print(f"Agent response: {response}")
    except Exception as e:
        print(f"Agent retrieval error: {str(e)}")

async def main():
    print("Testing retrieval function fix...\n")

    await test_retrieval_directly()
    await test_retrieval_via_agent()

if __name__ == "__main__":
    asyncio.run(main())