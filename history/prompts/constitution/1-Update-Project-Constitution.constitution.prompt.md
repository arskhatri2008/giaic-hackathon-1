---
id: 1
title: Update-Project-Constitution
stage: constitution
date: 2025-12-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Claude-User
command: /sp.constitution
labels: [constitution, spec-driven-development, ai-book]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: AI-Spec-Driven Interactive Book with Embedded RAG Chatbot

Description:
Design, author, and deploy an AI-native technical book using Docusaurus and GitHub Pages.
The book must be written, structured, and maintained using Spec-Kit Plus and Claude Code,
and enhanced with a fully integrated Retrieval-Augmented Generation (RAG) chatbot that
answers questions based on the book's content, including user-selected text.

The system must support user authentication, personalization, and multilingual (Urdu) translation.

---------------------------------------------------------------------

Core Principles:

- Spec-Driven Development:
  All content, features, APIs, and workflows must be defined and evolved through clear,
  versioned specifications before implementation.

- Accuracy & Groundedness:
  All technical explanations must be correct, reproducible, and aligned with current
  best practices in AI engineering, RAG systems, and modern web development.

- Modular & Reusable Intelligence:
  Use Claude Code Subagents and Agent Skills to create reusable, composable intelligence
  for writing, reviewing, summarizing, personalizing, translating, and chatbot reasoning.

- Personalization-by-Design:
  Content must adapt to the user's declared software and hardware background collected at signup.

- User-Centric Clarity:
  Content must remain understandable, structured, and progressive for readers with
  varying technical backgrounds.

---------------------------------------------------------------------

Key Standards:

Content & Book Authoring:
- Written using Docusaurus (MDX format)
- Structured as chapters, sections, and sub-sections
- Generated and maintained via Spec-Kit Plus workflows
- Deployed to GitHub Pages
- Each chapter must support:
  - Default (non-personalized) view
  - Personalized view (based on user profile)
  - Urdu translation view

RAG Chatbot:
- Embedded directly into the published book UI
- Built using:
  - OpenAI Agents / ChatKit SDKs
  - FastAPI backend
  - Neon Serverless Postgres (metadata, users, auth links)
  - Qdrant Cloud Free Tier (vector storage)
- Capabilities:
  - Answer questions about the entire book
  - Answer questions based ONLY on user-selected text
  - Respect user authentication and personalization context
  - No hallucinated answers outside indexed content

Reusable Intelligence:
- Claude Code Subagents must be created for:
  - Chapter authoring
  - Technical review
  - Fact validation
  - Content personalization
  - Urdu translation
  - RAG prompt construction
- Agent Skills must be reusable across chapters and features

Authentication & User Profiling:
- Signup & Signin implemented using https://www.better-auth.com/
- At signup, explicitly collect:
  - Programming experience level
  - Preferred languages & frameworks
  - AI/ML background
  - Hardware capability (local vs cloud, GPU availability)
- User profile must drive:
  - Content depth
  - Examples complexity
  - Terminology selection

Personalization & Translation:
- Each chapter must include:
  - A "Personalize Content" button
  - A "Translate to Urdu" button
- Personalization must:
  - Preserve factual correctness
  - Adapt tone, depth, and examples
- Translation must:
  - Maintain technical accuracy
  - Preserve code blocks and identifiers

---------------------------------------------------------------------

Constraints:

- No hardcoded content outside specs
- All AI-generated content must be reviewable and regenerable
- No chatbot responses without verified retrieval context
- No personalization without authenticated user context
- No translation that alters technical meaning
- All services must use free or serverless tiers where specified

---------------------------------------------------------------------

Success Criteria:

- Book is fully published on GitHub Pages
- All chapters authored via Spec-Kit Plus + Claude Code
- RAG chatbot correctly answers:
  - Global book questions
  - Selected-text-only questions
- Authentication and personalization work end-to-end
- Urdu translat
```

## Response snapshot

The project constitution has been successfully updated for the "AI-Spec-Driven Interactive Book with Embedded RAG Chatbot" project. The new constitution includes:

Core Principles:
- Spec-Driven Development
- Accuracy & Groundedness
- Modular & Reusable Intelligence
- Personalization-by-Design
- User-Centric Clarity

Additional sections include Key Standards, Constraints, Success Criteria, and Governance. The constitution version is set to 1.0.0 with ratification and amendment dates set to 2025-12-20.

## Outcome

- ✅ Impact: Updated project constitution with comprehensive principles and standards
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Plan and implement initial features based on new constitution
- 🧠 Reflection: Constitution now provides clear governance for the AI book project with RAG chatbot

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on constitution