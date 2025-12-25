import asyncio
import structlog
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from config.settings import settings
from models.data_models import ContentChunk
from utils.helpers import calculate_content_hash, count_words, normalize_text
from .base_crawler import BaseCrawler

logger = structlog.get_logger()


class DocusaurusCrawler(BaseCrawler):
    """Docusaurus-specific crawler that extracts clean text content from Docusaurus websites."""

    def __init__(self):
        super().__init__()
        self.content_chunks: List[ContentChunk] = []
        self.visited_urls: set = set()

    async def crawl(self, start_urls: List[str]) -> List[ContentChunk]:
        """
        Crawl Docusaurus websites and extract clean text content.
        Returns a list of ContentChunk objects with extracted content.
        """
        logger.info("Starting Docusaurus crawling", start_urls=start_urls)
        self.content_chunks = []

        # Use Playwright for browser automation
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=True,  # Set to False for debugging
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            context = await browser.new_context(
                user_agent=settings.crawler_user_agent
            )

            try:
                for start_url in start_urls:
                    logger.info("Processing start URL", url=start_url)
                    await self._crawl_url(context, start_url)
            finally:
                await browser.close()

        logger.info("Crawling completed", total_chunks=len(self.content_chunks))
        return self.content_chunks

    async def _crawl_url(self, context, url: str, depth: int = 0, max_depth: int = 2):
        """Recursively crawl a URL and its linked pages up to max_depth."""
        if url in self.visited_urls or depth > max_depth:
            return

        self.visited_urls.add(url)
        logger.info("Crawling page", url=url, depth=depth)

        page = None
        try:
            page = await context.new_page()
            if page is None:
                logger.error("Failed to create page object", url=url)
                return
            page.set_default_timeout(settings.crawler_timeout * 1000)  # Don't await this method

            # Navigate to the page
            await page.goto(url, wait_until="domcontentloaded")

            # Extract content using Docusaurus-specific selectors
            content_data = await self._extract_content(page, url)

            if content_data:
                # Process and store the content
                content_chunk = self._process_content(content_data, url)
                if content_chunk:
                    self.content_chunks.append(content_chunk)
                    logger.info("Content extracted", url=url, content_length=len(content_chunk.content))

            # Find and crawl additional links if within max depth
            if depth < max_depth:
                links = await self._find_internal_links(page, url)
                for link in links:
                    if link not in self.visited_urls:
                        await self._crawl_url(context, link, depth + 1, max_depth)

        except Exception as e:
            logger.error("Error crawling page", url=url, error=str(e))
            import traceback
            logger.error("Full traceback", url=url, traceback=traceback.format_exc())
            # Add error to crawl job tracking if needed
            pass
        finally:
            if page:
                try:
                    await page.close()
                except:
                    pass  # Ignore errors when closing page

    async def _extract_content(self, page, url: str) -> Optional[Dict]:
        """Extract content from a Docusaurus page using appropriate selectors."""
        try:
            # Wait for content to load with broader selectors for Docusaurus sites
            await page.wait_for_selector('main, .markdown, .theme-doc-markdown, article, .content, .hero__title, .hero__subtitle, .container, .main-wrapper, body', timeout=10000)

            # Extract the main content - use broader selectors to handle various Docusaurus structures
            content_selectors = [
                '.markdown',
                '.theme-doc-markdown',
                'main',
                'article',
                '.container',
                '.heroBanner_qdFl',  # Specific to this site's banner
                '.hero__title',      # Hero title
                '.hero__subtitle',   # Hero subtitle
                '.features_t9lD',    # Features section
                '.main-wrapper',     # Main wrapper
                '.theme-doc-content', # Common Docusaurus content class
                '.markdown > div',   # Nested markdown content
                '.content',
                'body'
            ]
            content = ""

            for selector in content_selectors:
                try:
                    elements = page.locator(selector)
                    count = await elements.count()
                    if count > 0:
                        element = elements.first
                        if element:  # Check if element is not None
                            element_text = await element.inner_text()
                            if element_text and len(element_text.strip()) > 50:  # If we get meaningful content, break
                                content = element_text
                                break
                except Exception as e:
                    logger.debug(f"Error extracting content with selector {selector}", error=str(e))
                    continue  # Try next selector if current one fails

            # If still no substantial content, try alternative approaches
            if not content or len(content.strip()) <= 50:
                try:
                    # Try to get all paragraphs and headings
                    all_text_elements = page.locator('h1, h2, h3, h4, p, li, td, th')
                    count = await all_text_elements.count()

                    if count > 0:
                        all_texts = []
                        for i in range(min(count, 20)):  # Limit to first 20 elements to avoid huge content
                            try:
                                element = all_text_elements.nth(i)
                                if element:
                                    text = await element.inner_text()
                                    if text and len(text.strip()) > 5:
                                        all_texts.append(text.strip())
                            except:
                                continue

                        content = ' '.join(all_texts)

                except Exception as e:
                    logger.debug("Alternative content extraction failed", error=str(e))

            # Extract title - try multiple possible title selectors including Docusaurus-specific ones
            title_selectors = [
                '.hero__title',      # Docusaurus hero title
                'h1.hero__title',    # More specific hero title
                'h1',
                'title',
                'h2',
                'h3',
                '[data-rh="true"][property="og:title"]',  # Open Graph title
                '.navbar__title',    # Navbar title
                '.hero__subtitle'    # Use subtitle as title if no h1
            ]
            title = ""
            for selector in title_selectors:
                try:
                    title_elements = page.locator(selector)
                    count = await title_elements.count()
                    if count > 0:
                        title_element = title_elements.first
                        if title_element:  # Check if element is not None
                            title_text = await title_element.inner_text()
                            if title_text and title_text.strip():
                                title = title_text.strip()
                                break
                except Exception as e:
                    logger.debug(f"Error extracting title with selector {selector}", error=str(e))
                    continue

            # If no title found, try to extract from URL or meta tag
            if not title:
                try:
                    # Try to get title from meta tag
                    title_elements = page.locator('title')
                    count = await title_elements.count()
                    if count > 0:
                        title_element = title_elements.first
                        if title_element:
                            title = await title_element.inner_text()
                except:
                    pass

            # Extract section path from URL
            parsed_url = urlparse(url)
            path_parts = [part for part in parsed_url.path.split('/') if part]
            section_path = '/'.join(path_parts) or 'home'

            if content and len(content.strip()) > 10:  # Minimum content length (reduced from 50 to 10)
                return {
                    'url': url,
                    'title': title,
                    'content': content,
                    'section_path': section_path
                }

        except Exception as e:
            logger.warning("Could not extract content from page", url=url, error=str(e))

        return None

    async def _find_internal_links(self, page, base_url: str) -> List[str]:
        """Find internal links on the page that belong to the same domain."""
        try:
            # Get all links on the page
            links_locator = page.locator('a[href]')
            count = await links_locator.count()
            internal_links = []

            for i in range(count):
                try:
                    link = links_locator.nth(i)
                    if link:  # Check if link element is not None
                        href = await link.get_attribute('href')
                        if href:
                            # Resolve relative URLs
                            full_url = urljoin(base_url, href)

                            # Only include internal links to the same domain
                            if self.is_valid_url(full_url, base_url):
                                # Filter out non-content links (like navigation, social links, etc.)
                                link_text = await link.inner_text()
                                link_title = await link.get_attribute('title') or ''

                                # Skip links that are clearly navigation or non-content
                                if not any(skip in link_text.lower() for skip in ['home', 'blog', 'github', 'twitter', 'linkedin']) and \
                                   not any(skip in link_title.lower() for skip in ['home', 'blog', 'github', 'twitter', 'linkedin']):
                                    internal_links.append(full_url)
                except Exception as e:
                    logger.debug(f"Error processing link {i}", error=str(e))
                    continue  # Skip problematic links

            # Remove duplicates while preserving order
            unique_links = []
            for link in internal_links:
                if link not in unique_links:
                    unique_links.append(link)

            return unique_links[:20]  # Limit to prevent excessive crawling

        except Exception as e:
            logger.warning("Could not find internal links", url=base_url, error=str(e))
            return []

    def _process_content(self, content_data: Dict, url: str) -> Optional[ContentChunk]:
        """Process extracted content into a ContentChunk object."""
        try:
            # Normalize the content
            normalized_content = normalize_text(content_data['content'])

            # Calculate content hash for deduplication
            content_hash = calculate_content_hash(normalized_content)

            # Check if content is already processed (deduplication)
            if content_hash in [chunk.content_hash for chunk in self.content_chunks]:
                logger.debug("Content already exists (deduplication)", url=url)
                return None

            # Count words
            word_count = count_words(normalized_content)

            # Create ContentChunk object
            chunk = ContentChunk(
                id=f"chunk_{len(self.content_chunks)}",  # This would be a proper UUID in production
                source_url=content_data['url'],
                section_path=content_data['section_path'],
                title=content_data['title'],
                content=normalized_content,
                chunk_index=0,  # Single chunk for now, will implement chunking later
                total_chunks=1,
                content_hash=content_hash,
                extracted_at=content_data.get('extracted_at'),  # Will set to current time below
                word_count=word_count,
                metadata={'source_type': 'docusaurus', 'original_title': content_data['title']}
            )

            # Set the extracted_at timestamp
            from datetime import datetime
            chunk.extracted_at = datetime.now()

            return chunk

        except Exception as e:
            logger.error("Error processing content", url=url, error=str(e))
            return None