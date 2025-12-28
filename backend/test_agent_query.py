#!/usr/bin/env python3
"""
Simple test to check if the RAG agent can process queries with OpenRouter API
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to Python path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from backend.agent import ask_question, health_check, rag_agent

async def test_agent():
    print("Testing RAG agent with OpenRouter API...")

    # First, check health
    print("\n1. Checking health...")
    health_status = await health_check()
    print(f"Health status: {health_status}")

    if health_status["status"] != "healthy":
        print("Agent is not healthy, stopping test")
        return

    # Test with a simple query (mocked for now to avoid actual API calls during test)
    print("\n2. Testing with sample query...")
    try:
        # This will attempt to connect to the OpenRouter API
        response = await ask_question("What is artificial intelligence?")
        print(f"Response received: {response}")
        print(f"Answer: {response.answer}")
        print(f"Sources: {len(response.sources)}")
        print(f"Grounded: {response.grounded}")
    except Exception as e:
        print(f"Error during query: {str(e)}")
        print("This may be due to API key issues or network connectivity")

if __name__ == "__main__":
    asyncio.run(test_agent())