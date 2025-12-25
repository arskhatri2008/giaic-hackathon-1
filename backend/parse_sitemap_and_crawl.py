#!/usr/bin/env python3
"""
Script to parse sitemap.xml and run the Docusaurus crawler with all extracted URLs.
This addresses the issue where the crawler wasn't ingesting all documentation pages.
"""

import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
import subprocess
import sys
import os

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
    # Use the current directory (backend) for execution
    current_dir = os.path.dirname(__file__)

    print(f"Running crawler with {len(urls)} URLs...")

    # Build command with all URLs
    cmd = [sys.executable, 'main.py']
    for url in urls:
        cmd.extend(['--urls', url])

    print("Command:", " ".join(cmd))

    # Execute the command in the current directory
    result = subprocess.run(cmd, cwd=current_dir, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    return result.returncode

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
        sys.exit(1)

if __name__ == "__main__":
    main()