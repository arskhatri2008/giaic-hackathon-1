import structlog
from typing import List
from utils.helpers import normalize_text

logger = structlog.get_logger()


class ContentNormalizer:
    """Normalize content for consistent processing."""

    def __init__(self):
        pass

    def normalize_content(self, content: str) -> str:
        """
        Normalize content by cleaning, standardizing, and preparing for processing.
        """
        if not content:
            return ""

        # Use the utility function for basic normalization
        normalized = normalize_text(content)

        # Additional normalization steps could be added here
        # For example, handling special characters, contractions, etc.

        logger.debug("Content normalized", original_length=len(content), normalized_length=len(normalized))

        return normalized

    def normalize_batch(self, contents: List[str]) -> List[str]:
        """
        Normalize a batch of content strings.
        """
        normalized_contents = []
        for content in contents:
            normalized = self.normalize_content(content)
            normalized_contents.append(normalized)

        logger.info("Batch normalization completed", count=len(contents))

        return normalized_contents