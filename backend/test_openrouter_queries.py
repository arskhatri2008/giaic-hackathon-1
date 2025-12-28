#!/usr/bin/env python3
"""
Test the RAG agent with OpenRouter API using various queries
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to Python path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from agent import ask_question, health_check

async def test_queries():
    print("Testing RAG agent with OpenRouter API...")

    # Check health
    print("\n1. Health Check:")
    health_status = await health_check()
    print(f"   Health status: {health_status['status']}")
    print(f"   Message: {health_status['message']}")
    print(f"   Response time: {health_status['response_time']}s")

    # Test queries
    test_queries = [
        "What is artificial intelligence?",
        "Explain machine learning",
        "What are neural networks?",
        "How does deep learning work?",
        "What is natural language processing?",
        "Hello, how are you?",
        "What can you help me with?"
    ]

    print(f"\n2. Testing {len(test_queries)} queries:")

    for i, query in enumerate(test_queries, 1):
        print(f"\n   Query {i}: {query}")
        try:
            response = await ask_question(query)
            print(f"   Response: {response}")
            print(f"   Response length: {len(response)} characters")
        except Exception as e:
            print(f"   Error: {str(e)}")

    print(f"\n3. Testing with a longer query:")
    long_query = "Can you explain in detail what artificial intelligence is, how it works, what are its main applications, and what are the current challenges in the field?"
    print(f"   Query: {long_query}")
    try:
        response = await ask_question(long_query)
        print(f"   Response: {response}")
        print(f"   Response length: {len(response)} characters")
    except Exception as e:
        print(f"   Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_queries())