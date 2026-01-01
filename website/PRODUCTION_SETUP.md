# Production Deployment Configuration

## Backend URL Configuration

For the deployed application to work properly, you need to configure the backend API URL in your deployment environment.

### Vercel Environment Variables

Set the following environment variable in your Vercel project settings:

- `BACKEND_URL`: The URL of your deployed backend API server (e.g., `https://your-backend-app.herokuapp.com` or `https://your-backend.onrender.com`)

### Required Setup

The frontend application relies on a backend API server to handle:
- `/api/query` - for processing user queries against the documentation
- `/api/health` - for health checks

### Deployment Options

You have two options for deployment:

1. **Separate Backend Deployment**: Deploy the FastAPI backend to a cloud platform (Heroku, Render, Railway, etc.) and set the `BACKEND_URL` environment variable to point to that deployment.

2. **Local Development**: For local development, the backend runs on `http://127.0.0.1:8000` by default.

### Environment Variables

Make sure to set these environment variables in your production environment:

```
BACKEND_URL=https://your-actual-backend-domain.com
```

The Vercel API routes in `/src/pages/api/` will proxy requests from the frontend to the backend server specified in the `BACKEND_URL` environment variable.