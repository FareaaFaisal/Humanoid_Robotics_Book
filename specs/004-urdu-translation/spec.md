# Feature Specification: Translate Chapter Content to Urdu

**Feature Branch**: `004-urdu-translation`
**Created**: 2025-12-10
**Status**: Draft
**Input**: User description: "Feature: Translate Chapter Content to Urdu..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Translate to Urdu (Priority: P1)

As a user, I want to translate the content of each chapter into Urdu so that I can read chapters in my preferred language.

**Why this priority**: This feature makes the book accessible to a wider, Urdu-speaking audience.

**Independent Test**: A user can click a "Translate to Urdu" button on a chapter page, and the main content of the chapter is translated into Urdu.

**Acceptance Scenarios**:
1. **Given** the chapter content is displayed in the original language, **When** the user clicks the "Translate to Urdu" button, **Then** the chapter content should be translated into Urdu and the button text should change to "Original Language".
2. **Given** the chapter content is currently in Urdu, **When** the user clicks the "Original Language" button, **Then** the chapter content should revert to the original language and the button text should change back to "Translate to Urdu".
3. **Given** the user clicks the "Translate to Urdu" button and the translation service fails, **Then** an error message "Translation failed. Please try again." should be shown, and the chapter content should remain in the original language.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A "Translate to Urdu" button MUST be present on each chapter page.
- **FR-002**: Clicking the button MUST translate the chapter content to Urdu.
- **FR-003**: The translation MUST be performed using the Context7 MCP.
- **FR-004**: No API keys MUST be exposed in the frontend.
- **FR-005**: The translation MUST preserve the MDX structure and code blocks.
- **FR-006**: User translation events SHOULD be tracked using `localStorage`.

### Key Entities
- **TranslateButton**: A UI component that triggers the translation.
- **ChapterContent**: The main content of the chapter that needs to be translated.
- **TranslationService**: The backend service that interacts with the Context7 MCP.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of chapter pages have a functional "Translate to Urdu" button.
- **SC-002**: The translation and reversion process completes in under 3 seconds.
- **SC-003**: The translated content preserves all original MDX formatting, including code blocks, in 100% of tests.
- **SC-004**: User translation events are successfully logged to `localStorage`.
