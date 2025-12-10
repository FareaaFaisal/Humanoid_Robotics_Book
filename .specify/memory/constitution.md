<!--
Sync Impact Report:
- Version: 1.0.0 → 1.1.0
- Added Sections:
  - V. Chapter Translation
- Templates requiring updates:
  - ⚠ .specify/templates/plan-template.md
  - ⚠ .specify/templates/spec-template.md
  - ⚠ .specify/templates/tasks-template.md
-->
# Book on *Physical AI & Humanoid Robotics* Constitution

## Core Principles

### I. Technical Accuracy
Based on verified robotics and AI sources. All factual claims MUST have traceable citations. Rationale: Ensures the content is reliable and academically sound.

### II. Clarity and Accessibility
Writing MUST be clear and accessible for students, hobbyists, and early researchers, targeting a Flesch-Kincaid Grade Level of 10-14. Zero plagiarism is tolerated. Rationale: Makes complex topics understandable to a broad audience.

### III. Reproducible Engineering
Provide reproducible engineering details, including algorithms, diagrams, and hardware specifications. All diagrams and tables MUST be original or properly credited. Rationale: Enables readers to replicate and build upon the work.

### IV. Clear Scope
Clearly distinguish between the current state-of-the-art and future/conceptual ideas. All claims MUST be verified with sources. Rationale: Prevents confusion and manages reader expectations.

### V. Chapter Translation
The book MUST support chapter translation using the Context7 MCP for translation. All API keys MUST be handled securely and not exposed in the frontend. Translations MUST preserve the original MDX structure and code blocks. User translation events SHOULD be tracked for analytics (localStorage is acceptable). Rationale: Makes the book accessible to a wider, global audience.

## Content and Format Standards

- **Citation Style**: All sources MUST use the IEEE citation style.
- **Source Quality**: A minimum of 50% of sources MUST be from peer-reviewed publications (e.g., IEEE, ACM, Springer, Elsevier).
- **Technology Stack**: The project MUST be developed using Docusaurus (Markdown/MDX) and deployed to GitHub Pages.
- **Word Count**: The final manuscript SHOULD be between 20,000 and 40,000 words.
- **Chapter Structure**: Each chapter MUST include a summary, key definitions, diagrams, and a reference list.
- **Coverage**: The book MUST cover:
  - Physical AI foundations
  - Humanoid locomotion and control
  - Perception systems (vision, tactile, proprioception)
  - Motion planning and behavior models
  - Safety, ethics, and real-world case studies

## Success Criteria

- All technical claims are verified with traceable citations.
- The writing style is consistently clear, technical, and aligned with the defined grade level.
- All diagrams and tables are original or have proper credit.
- The Docusaurus project builds successfully without errors.
- The final output is successfully deployed to GitHub Pages.
- The project fully aligns with this constitution and all generated specifications.

## Governance

This constitution is the single source of truth for project standards and principles. All development artifacts, including specifications, plans, and code, MUST adhere to it. The project will follow the Spec-Kit Plus workflow (spec → draft → refine → final).

**Version**: 1.1.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-07
