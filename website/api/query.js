export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Check if BACKEND_URL is configured
  const BACKEND_URL = process.env.BACKEND_URL;

  if (!BACKEND_URL) {
    return res.status(500).json({
      error: 'BACKEND_URL environment variable is not configured',
      message: 'Please set the BACKEND_URL environment variable in your Vercel deployment settings to point to your backend server.'
    });
  }

  try {
    const backendUrl = `${BACKEND_URL}/api/query`;

    // Forward the request to the backend
    const response = await fetch(backendUrl, {
      method: 'POST', // Always forward as POST for query endpoint
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(req.body),
    });

    // Get the response from the backend
    const data = await response.json();

    // Return the response from the backend
    res.status(response.status).json(data);
  } catch (error) {
    console.error('API proxy error:', error);
    res.status(500).json({
      error: 'Failed to connect to backend server',
      message: 'The backend server is not accessible. Please ensure your BACKEND_URL is correctly configured and the server is running.'
    });
  }
}

export const config = {
  api: {
    bodyParser: {
      sizeLimit: '10mb', // Adjust as needed
    },
  },
};