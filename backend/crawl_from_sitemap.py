#!/usr/bin/env python3
"""
Script to parse sitemap.xml and run the Docusaurus crawler with all extracted URLs.
This addresses the issue where the crawler wasn't ingesting all documentation pages.
"""

import os
import sys
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
import subprocess

# Add the backend directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

def parse_sitemap(sitemap_url):
    """Parse sitemap.xml and extract all URLs."""
    print(f"Fetching sitemap: {sitemap_url}")
    response = requests.get(sitemap_url)
    response.raise_for_status()

    # Parse the XML
    root = ET.fromstring(response.content)

    # Handle different sitemap formats (with and without namespaces)
    namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    urls = []
    for url_element in root.findall('sitemap:url', namespace):
        loc_element = url_element.find('sitemap:loc', namespace)
        if loc_element is not None:
            urls.append(loc_element.text)

    # If namespace approach didn't work, try without namespace
    if not urls:
        for url_element in root.findall('url'):
            loc_element = url_element.find('loc')
            if loc_element is not None:
                urls.append(loc_element.text)

    print(f"Found {len(urls)} URLs in sitemap")
    return urls

def filter_docs_urls(urls):
    """Filter URLs to only include documentation pages."""
    docs_urls = []
    for url in urls:
        if '/docs/' in url:
            docs_urls.append(url)

    print(f"Filtered to {len(docs_urls)} documentation URLs")
    return docs_urls

def run_crawler_with_urls(urls):
    """Run the backend crawler with the provided URLs."""
    print(f"Running crawler with {len(urls)} URLs...")

    # Import the main function directly instead of using subprocess
    from main import main

    # Call the main function with the URLs
    # We'll call it with the URLs as a list, using default values for other parameters
    try:
        main.callback(
            urls=urls,
            collection_name='docusaurus_embeddings',
            chunk_size=512,
            max_concurrent=5
        )
        return 0
    except Exception as e:
        print(f"Error running crawler: {e}")
        import traceback
        traceback.print_exc()
        return 1

def main():
    sitemap_url = "https://giaic-hackathon-1-ten.vercel.app/sitemap.xml"

    try:
        # Parse sitemap to get all URLs
        all_urls = parse_sitemap(sitemap_url)

        # Filter for documentation URLs only
        docs_urls = filter_docs_urls(all_urls)

        print("Sample documentation URLs:")
        for url in docs_urls[:5]:  # Show first 5 URLs
            print(f"  - {url}")

        if len(docs_urls) > 10:  # Show last 2 as well if there are many
            print("  ...")
            for url in docs_urls[-2:]:
                print(f"  - {url}")

        # Run the crawler with documentation URLs
        return_code = run_crawler_with_urls(docs_urls)

        print(f"Crawler finished with return code: {return_code}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()