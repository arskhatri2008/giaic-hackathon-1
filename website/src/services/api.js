// API base URL - using relative path for deployment compatibility
// In development, this will connect to http://localhost:8000/api (if using proxy)
// In deployment, this will connect to the same domain's /api endpoint
const API_BASE_URL = '/api';

/**
 * Query the RAG agent API
 * @param {Object} queryData - The query request object
 * @param {string} queryData.query - The user's query
 * @param {string} [queryData.context] - Additional context
 * @param {string} [queryData.user_id] - User identifier
 * @param {string} [queryData.session_id] - Session identifier
 * @param {boolean} [queryData.include_sources=true] - Whether to include sources
 * @returns {Promise<Object>} The API response
 */
export const queryAPI = async (queryData) => {
  try {
    // Check if fetch is available
    if (typeof fetch === 'undefined') {
      throw new Error('Fetch API is not available in this environment');
    }

    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(queryData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Query API error:', error);
    throw error;
  }
};

/**
 * Check the health status of the API
 * @returns {Promise<Object>} The health status
 */
export const healthAPI = async () => {
  try {
    // Check if fetch is available
    if (typeof fetch === 'undefined') {
      throw new Error('Fetch API is not available in this environment');
    }

    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Health API error:', error);
    throw error;
  }
};