import os
import sys
from dotenv import load_dotenv
import argparse

# Load environment variables
load_dotenv()

# Add backend to Python path
sys.path.insert(0, './backend')

def run_pipeline():
    """Run the RAG ingestion pipeline"""
    from main import main
    import requests
    from xml.etree import ElementTree as ET

    # Get the sitemap URL from environment or use default
    sitemap_url = os.getenv("DEPLOY_VERCEL_URL", "https://giaic-hackathon-1-ten.vercel.app/sitemap.xml")

    print(f"Fetching sitemap from: {sitemap_url}")

    # Fetch and parse the sitemap to get all URLs
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Parse the XML sitemap
        root = ET.fromstring(response.content)

        # Extract all URLs from the sitemap
        urls = []
        for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            urls.append(url_elem.text)

        print(f"Found {len(urls)} URLs in sitemap")

        # Filter out non-documentation URLs if needed
        doc_urls = [url for url in urls if '/docs/' in url or url.endswith('/')]
        print(f"Filtered to {len(doc_urls)} documentation URLs")

    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        # Fallback to a single URL if sitemap fetching fails
        doc_urls = [sitemap_url.replace('/sitemap.xml', '')]

    print(f"Running backend pipeline with {len(doc_urls)} URLs")

    # Run the main function with all URLs from the sitemap
    main.callback(urls=doc_urls, collection_name='docusaurus_embeddings', chunk_size=512, max_concurrent=5)

def run_agent_server():
    """Run the RAG agent server"""
    import asyncio
    import json
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    from agent import ask_question

    class RAGRequestHandler(BaseHTTPRequestHandler):
        def _set_headers(self, status_code=200):
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

        def do_OPTIONS(self):
            self._set_headers(200)

        def do_POST(self):
            if self.path == '/ask' or self.path == '/api/query':
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)

                    request_data = json.loads(post_data.decode('utf-8'))

                    # Handle both 'question' (for /ask) and 'query' (for /api/query) formats
                    question = request_data.get('question', '')
                    if not question:
                        question = request_data.get('query', '')

                    if not question:
                        self._set_headers(400)
                        response = {'error': 'Question or query is required'}
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                        return

                    # Run the agent asynchronously
                    # Use a timeout mechanism that works on Windows
                    import threading
                    import time

                    result = [None]
                    exception = [None]

                    def run_agent():
                        try:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            result[0] = loop.run_until_complete(ask_question(question))
                        except Exception as e:
                            exception[0] = e

                    thread = threading.Thread(target=run_agent)
                    thread.daemon = True
                    thread.start()
                    thread.join(timeout=30)  # 30 second timeout

                    if thread.is_alive():
                        # Thread is still running after timeout
                        self._set_headers(408)  # Request Timeout
                        response = {'error': 'Request timeout - processing took too long'}
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                        return

                    if exception[0]:
                        raise exception[0]

                    self._set_headers(200)
                    response_data = {
                        'answer': result[0],
                        'status': 'success'
                    }
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))

                except ConnectionResetError:
                    # Client disconnected before we could respond
                    pass
                except Exception as e:
                    try:
                        self._set_headers(500)
                        response = {'error': str(e)}
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                    except:
                        # If we can't even send an error response, just pass
                        pass
            else:
                try:
                    self._set_headers(404)
                    response = {'error': 'Endpoint not found'}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                except:
                    pass

        def do_GET(self):
            if self.path == '/health':
                self._set_headers(200)
                response = {'status': 'healthy', 'agent_ready': True}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self._set_headers(404)
                response = {'error': 'Endpoint not found'}
                self.wfile.write(json.dumps(response).encode('utf-8'))

    port = int(os.getenv("PORT", 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, RAGRequestHandler)
    print(f"Starting RAG agent server on port {port}...")
    print("Endpoints available:")
    print("  GET  /health - Health check")
    print("  POST /ask   - Ask a question")
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Backend System")
    parser.add_argument("mode", choices=["pipeline", "agent"], help="Run mode: pipeline for ingestion, agent for question answering")

    args = parser.parse_args()

    if args.mode == "pipeline":
        run_pipeline()
    elif args.mode == "agent":
        run_agent_server()