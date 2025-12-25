import hashlib
from typing import List
import re


def calculate_content_hash(content: str) -> str:
    """Calculate SHA-256 hash of content for deduplication purposes."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def validate_content(content: str, min_length: int = 50) -> bool:
    """Validate content meets minimum quality requirements."""
    if not content or len(content.strip()) < min_length:
        return False
    return True


def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and normalizing line breaks."""
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Chunk text into segments with overlap to maintain context."""
    if not text:
        return []

    # Simple word-based chunking
    words = text.split()

    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start_idx = 0

    while start_idx < len(words):
        end_idx = start_idx + chunk_size
        chunk = ' '.join(words[start_idx:end_idx])
        chunks.append(chunk)

        # Move start index forward, considering overlap
        start_idx = end_idx - overlap if end_idx < len(words) else len(words)

    return chunks


def count_words(text: str) -> int:
    """Count the number of words in text."""
    if not text:
        return 0
    return len(text.split())


def normalize_text(text: str) -> str:
    """Normalize text for consistent processing."""
    if not text:
        return ""

    # Clean the text
    text = clean_text(text)

    # Additional normalization steps could be added here
    # For example, handling special characters, contractions, etc.

    return text