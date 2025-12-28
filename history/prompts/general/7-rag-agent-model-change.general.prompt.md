---
id: 7
title: "RAG Agent Model Change and System Fix"
stage: "general"
date: "2025-12-26"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "001-rag-agent-sdk"
user: "user"
command: "change model from mistralai/devstral-2512:free to xiaomi/mimo-v2-flash:free"
labels: ["rag", "agent", "model", "fix", "openrouter"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "backend/agent.py"
tests: []
outcome: "Successfully fixed the RAG agent by changing the model to one that properly supports tool calling with OpenRouter, enabling the agent to incorporate retrieved content into responses"
evaluation: "The system now properly retrieves content from Qdrant and incorporates it into agent responses"
---

# Prompt History Record: RAG Agent Model Change and System Fix

## Summary
Changed the OpenRouter model in the RAG agent from `mistralai/devstral-2512:free` to `xiaomi/mimo-v2-flash:free` to fix tool calling compatibility issues.

## Context
The RAG agent was not properly incorporating retrieved content into its responses despite the retrieval system working correctly. The issue was identified as the original model not fully supporting the OpenAI Agents SDK's tool calling functionality when used through OpenRouter.

## Changes Made
- Updated `backend/agent.py` to use `xiaomi/mimo-v2-flash:free` model instead of `mistralai/devstral-2512:free`
- Maintained all other configurations and functionality

## Results
- Agent now properly retrieves content from Qdrant
- Tool calling functionality works correctly
- Agent successfully incorporates retrieved content into responses
- System demonstrates full RAG pipeline functionality

## Technical Details
- The new model has better compatibility with OpenRouter's tool calling implementation
- Previously, the agent would return "I don't have enough information" despite retrieving content
- Now the agent provides detailed responses based on retrieved content
- Qdrant retrieval, Cohere embeddings, and overall pipeline remain functional

## Validation
- Direct retrieval tests confirm Qdrant connectivity
- Agent response tests show proper content incorporation
- Tool calling flow verified end-to-end