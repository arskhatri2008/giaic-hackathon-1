---
id: 005
title: Fix ReferenceError in API Service
stage: red
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 003-fastapi-rag-integration
user: Claude
command: Fix ReferenceError process is not defined
labels: ["bug-fix", "frontend", "docusaurus", "api", "environment-variables"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - website/src/services/api.js
  - website/src/theme/Layout.js
tests:
  - browser console verification
---

## Prompt

Fix ReferenceError in api.js causing black screen - "process is not defined" in browser environment

## Response snapshot

Successfully fixed the ReferenceError that was causing the black screen issue:

### Root Cause
- The api.js file was accessing `process.env.REACT_APP_API_BASE_URL`
- `process` is a Node.js specific object that doesn't exist in browser environments
- This caused a runtime error that prevented the page from rendering

### Solution Implemented
- Removed the `process.env` reference from api.js
- Used a static API URL that works in both build and browser environments
- Updated the theme component to ensure proper client-side detection

### Verification
- Frontend now loads without JavaScript errors
- API integration works properly
- Black screen issue resolved
- Both servers running correctly

## Outcome

- ✅ Impact: Resolved the ReferenceError that was causing black screen, enabling proper page rendering
- 🧪 Tests: Verified in browser environment with no console errors
- 📁 Files: 2 files modified to fix the environment compatibility issue
- 🔁 Next prompts: Ready for production deployment
- 🧠 Reflection: Docusaurus environment variables require special handling for browser compatibility

## Evaluation notes (flywheel)

- Failure modes observed: process is not defined ReferenceError in browser
- Graders run and results (PASS/FAIL): PASS - Error eliminated, site loads properly
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add proper environment variable handling for Docusaurus