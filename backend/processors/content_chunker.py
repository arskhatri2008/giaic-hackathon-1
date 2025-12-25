from typing import List
import structlog
from config.settings import settings
from utils.helpers import chunk_text

logger = structlog.get_logger()


class ContentChunker:
    """Chunk content into appropriate segments for optimal embedding quality."""

    def __init__(self):
        self.chunk_size = settings.chunk_size_tokens
        self.overlap = settings.chunk_overlap_tokens

    def chunk_content(self, content: str, source_url: str = "") -> List[dict]:
        """
        Chunk content into segments with overlap to maintain context.
        Returns a list of dictionaries with chunk information.
        """
        if not content:
            return []

        logger.info("Chunking content", url=source_url, original_length=len(content))

        # Use the utility function to chunk the text
        chunks = chunk_text(content, chunk_size=self.chunk_size, overlap=self.overlap)

        chunk_objects = []
        for i, chunk_text in enumerate(chunks):
            chunk_obj = {
                'content': chunk_text,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'source_url': source_url,
                'word_count': len(chunk_text.split())
            }
            chunk_objects.append(chunk_obj)

        logger.info("Content chunking completed", url=source_url,
                   chunk_count=len(chunks), avg_chunk_size=len(content)//len(chunks) if chunks else 0)

        return chunk_objects

    def validate_chunk(self, chunk: dict) -> bool:
        """
        Validate that a chunk meets quality requirements.
        """
        if not chunk.get('content'):
            return False

        if len(chunk['content'].strip()) < 10:  # Minimum content length
            return False

        return True