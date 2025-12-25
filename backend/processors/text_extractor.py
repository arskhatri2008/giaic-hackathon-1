from typing import Dict, Optional
import structlog
from bs4 import BeautifulSoup

logger = structlog.get_logger()


class TextExtractor:
    """Extract clean text content from HTML, specifically optimized for Docusaurus sites."""

    def __init__(self):
        pass

    def extract_text_from_html(self, html_content: str, url: str = "") -> str:
        """
        Extract clean text from HTML content, removing navigation, headers, and other non-content elements.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove common non-content elements
            for element in soup.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style']):
                element.decompose()

            # Remove elements with common class names for navigation/components
            non_content_classes = [
                'navbar', 'sidebar', 'toc', 'table-of-contents', 'pagination',
                'footer', 'nav', 'menu', 'header', 'search', 'ads', 'advertisement'
            ]

            for class_name in non_content_classes:
                for element in soup.find_all(class_=class_name):
                    element.decompose()

            # Try to find the main content area (common in Docusaurus)
            main_content = None
            content_selectors = [
                '.markdown', '.theme-doc-markdown', '.main-content',
                '.doc-content', '.content', '.container', 'main', '.article'
            ]

            for selector in content_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            # If we found main content, use it; otherwise use the whole body
            content_element = main_content if main_content else soup.body or soup

            # Extract text and clean it up
            text = content_element.get_text(separator=' ', strip=True)

            # Clean up excessive whitespace
            import re
            text = re.sub(r'\s+', ' ', text)

            return text.strip()
        except Exception as e:
            logger.error("Error extracting text from HTML", url=url, error=str(e))
            return ""

    def extract_title_from_html(self, html_content: str) -> str:
        """
        Extract the title from HTML content.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Try different methods to get the title
            title = ""

            # First try to find h1 in main content areas
            content_selectors = ['.markdown', '.theme-doc-markdown', '.main-content', '.doc-content']
            for selector in content_selectors:
                h1 = soup.select_one(f"{selector} h1")
                if h1:
                    title = h1.get_text().strip()
                    break

            # If no title found in content, try standard title tag
            if not title:
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.get_text().strip()

            # If still no title, try first h1 on page
            if not title:
                h1 = soup.find('h1')
                if h1:
                    title = h1.get_text().strip()

            return title
        except Exception as e:
            logger.error("Error extracting title from HTML", error=str(e))
            return ""