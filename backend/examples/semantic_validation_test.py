#!/usr/bin/env python3
"""
Example script: Semantic similarity validation test
"""

import asyncio
import sys
import os

# Add the current directory to the Python path so we can import retrieve module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieve import RetrievalValidator


async def semantic_validation_test():
    """Example of running semantic similarity validation test."""
    print("=== Semantic Similarity Validation Test ===\n")

    # Initialize the validator
    validator = RetrievalValidator()

    # Run the semantic similarity validation test
    print("Running semantic similarity validation test...")
    test_result = await validator.test_semantic_similarity_validation()

    print(f"  Test Passed: {test_result['test_passed']}")
    print(f"  Message: {test_result['message']}")
    print(f"  Metrics: {test_result['metrics']}")

    print(f"\n  Detailed Metrics:")
    print(f"    Query Executed: {test_result['metrics']['query_executed']}")
    print(f"    Results Count: {test_result['metrics']['results_count']}")
    print(f"    Execution Time: {test_result['metrics']['execution_time']:.2f}s")
    print(f"    Validation Success: {test_result['metrics']['validation_success']}")
    print(f"    Metadata Complete: {test_result['metrics']['metadata_complete']}")

    if 'relevance_scores' in test_result['metrics']:
        print(f"    Relevance Scores: {test_result['metrics']['relevance_scores']}")

    if test_result['test_passed']:
        print("\n[PASS] Semantic similarity validation test passed!")
    else:
        print("\n[FAIL] Semantic similarity validation test failed.")


if __name__ == "__main__":
    asyncio.run(semantic_validation_test())