<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: All sections (new constitution)
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
  - README.md ⚠ pending
Follow-up TODOs: None
-->

# AI-Spec-Driven Interactive Book with Embedded RAG Chatbot Constitution

## Core Principles

### Spec-Driven Development
All content, features, APIs, and workflows must be defined and evolved through clear, versioned specifications before implementation. This ensures that all development follows a predetermined plan and maintains consistency across the project.

### Accuracy & Groundedness
All technical explanations must be correct, reproducible, and aligned with current best practices in AI engineering, RAG systems, and modern web development. This principle ensures that the content remains factually accurate and technically sound.

### Modular & Reusable Intelligence
Use Claude Code Subagents and Agent Skills to create reusable, composable intelligence for writing, reviewing, summarizing, personalizing, translating, and chatbot reasoning. This promotes efficiency and consistency across different aspects of the project.

### Personalization-by-Design
Content must adapt to the user's declared software and hardware background collected at signup. This ensures that the educational material is tailored to each user's specific background and needs.

### User-Centric Clarity
Content must remain understandable, structured, and progressive for readers with varying technical backgrounds. This ensures accessibility and comprehension for all users regardless of their starting skill level.

## Key Standards and Constraints

### Content & Book Authoring Standards
- Written using Docusaurus (MDX format)
- Structured as chapters, sections, and sub-sections
- Generated and maintained via Spec-Kit Plus workflows
- Deployed to GitHub Pages
- Each chapter must support:
  - Default (non-personalized) view
  - Personalized view (based on user profile)
  - Urdu translation view

### RAG Chatbot Standards
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

### Authentication & User Profiling Standards
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

### Personalization & Translation Standards
- Each chapter must include:
  - A "Personalize Content" button
  - A "Translate to Urdu" button
- Personalization must:
  - Preserve factual correctness
  - Adapt tone, depth, and examples
- Translation must:
  - Maintain technical accuracy
  - Preserve code blocks and identifiers

### Reusable Intelligence Standards
- Claude Code Subagents must be created for:
  - Chapter authoring
  - Technical review
  - Fact validation
  - Content personalization
  - Urdu translation
  - RAG prompt construction
- Agent Skills must be reusable across chapters and features

## Constraints

- No hardcoded content outside specs
- All AI-generated content must be reviewable and regenerable
- No chatbot responses without verified retrieval context
- No personalization without authenticated user context
- No translation that alters technical meaning
- All services must use free or serverless tiers where specified

## Success Criteria

- Book is fully published on GitHub Pages
- All chapters authored via Spec-Kit Plus + Claude Code
- RAG chatbot correctly answers:
  - Global book questions
  - Selected-text-only questions
- Authentication and personalization work end-to-end
- Urdu translation available for all content

## Governance

This constitution governs all development activities for the AI-Spec-Driven Interactive Book project. All team members must adhere to these principles and standards. Any deviation from these principles must be documented and justified. Changes to this constitution require explicit approval and must follow the established amendment procedures.

**Version**: 1.0.0 | **Ratified**: 2025-12-20 | **Last Amended**: 2025-12-20