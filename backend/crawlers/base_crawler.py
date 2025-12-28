import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import List, Optional
from urllib.parse import urljoin, urlparse
import structlog
from config.settings import settings

logger = structlog.get_logger()


class BaseCrawler(ABC):
    """Base class for web crawlers with common functionality."""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.timeout = aiohttp.ClientTimeout(total=settings.crawler_timeout)
        self.headers = {
            'User-Agent': settings.crawler_user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=self.timeout,
            headers=self.headers
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    def is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if URL is valid and belongs to the same domain for safety."""
        try:
            parsed = urlparse(url)
            base_parsed = urlparse(base_domain)

            # Check if it's a valid URL with http/https scheme
            if parsed.scheme not in ['http', 'https']:
                return False

            # For safety, only crawl the same domain as the base URL
            return parsed.netloc == base_parsed.netloc
        except Exception:
            return False

    def get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        return urlparse(url).netloc

    @abstractmethod
    async def crawl(self, start_urls: List[str]) -> List[str]:
        """Abstract method to crawl URLs and return content."""
        pass