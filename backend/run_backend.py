import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to Python path
sys.path.insert(0, './backend')

# Import and run the main function
from main import main

# Get the URL from environment or use default
url = os.getenv("DEPLOY_VERCEL_URL", "https://giaic-hackathon-1-ten.vercel.app")

print(f"Running backend pipeline with URL: {url}")

# Run the main function with the URL
if __name__ == "__main__":
    # Simulate command line arguments
    import sys
    sys.argv = ["run_backend.py", "--urls", url]

    # Call main function directly with the URL
    from main import main
    main.callback(urls=[url], collection_name='docusaurus_embeddings', chunk_size=512, max_concurrent=5)