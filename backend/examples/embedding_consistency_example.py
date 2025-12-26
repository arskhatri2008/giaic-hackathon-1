#!/usr/bin/env python3
"""
Example script: Embedding consistency validation
"""

import asyncio
import sys
import os

# Add the current directory to the Python path so we can import retrieve module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieve import RetrievalValidator


async def embedding_consistency_example():
    """Example of embedding consistency validation."""
    print("=== Embedding Consistency Validation Example ===\n")

    # Initialize the validator
    validator = RetrievalValidator()

    # Validate embedding consistency
    print("Validating embedding consistency between ingestion and retrieval...")
    consistency_result = await validator.validate_embedding_consistency()

    print(f"  Consistency Check: {consistency_result['consistency_check']}")
    print(f"  Ingestion Model: {consistency_result['ingestion_model']}")
    print(f"  Retrieval Model: {consistency_result['retrieval_model']}")
    print(f"  Parameters Match: {consistency_result['parameters_match']}")
    print(f"  Validation Message: {consistency_result['validation_message']}\n")

    if consistency_result['consistency_check']:
        print("[PASS] Embedding parameters are consistent!")
    else:
        print("[FAIL] Embedding parameters are inconsistent - this may affect retrieval quality.")


if __name__ == "__main__":
    asyncio.run(embedding_consistency_example())