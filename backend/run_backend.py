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

    # Get the URL from environment or use default
    url = os.getenv("DEPLOY_VERCEL_URL", "https://giaic-hackathon-1-ten.vercel.app")

    print(f"Running backend pipeline with URL: {url}")

    # Run the main function with the URL
    # Simulate command line arguments
    sys.argv = ["run_backend.py", "--urls", url]

    # Call main function directly with the URL
    main.callback(urls=[url], collection_name='docusaurus_embeddings', chunk_size=512, max_concurrent=5)

def run_agent_server():
    """Run the RAG agent server"""
    import asyncio
    import json
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    from agent import ask_question, rag_agent

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
            if self.path == '/ask':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)

                try:
                    request_data = json.loads(post_data.decode('utf-8'))
                    question = request_data.get('question', '')

                    if not question:
                        self._set_headers(400)
                        response = {'error': 'Question is required'}
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                        return

                    # Run the agent asynchronously
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(ask_question(question))

                    self._set_headers(200)
                    response_data = {
                        'answer': response,
                        'status': 'success'
                    }
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))

                except Exception as e:
                    self._set_headers(500)
                    response = {'error': str(e)}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self._set_headers(404)
                response = {'error': 'Endpoint not found'}
                self.wfile.write(json.dumps(response).encode('utf-8'))

        def do_GET(self):
            if self.path == '/health':
                self._set_headers(200)
                response = {'status': 'healthy', 'agent_ready': rag_agent is not None}
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