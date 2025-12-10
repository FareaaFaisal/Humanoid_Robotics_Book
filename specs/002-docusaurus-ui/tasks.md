# Tasks: Modern & Interactive Docusaurus Interface

**Input**: Design documents from `/specs/002-docusaurus-ui/`
**Prerequisites**: plan.md, spec.md

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel
- **[Story]**: Maps to user story (US1, US2, etc.)

## Phase 1: Foundational (Blocking Prerequisites)
**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T001 [P] [US1] Add "Inter" font to `src/css/custom.css` from Google Fonts.
- [X] T002 [US1] Update `docusaurus.config.ts` to set dark mode as the default.

---

## Phase 2: User Story 1 - Dark Mode Theme (Priority: P1) 🎯 MVP
**Goal**: Implement the dark mode theme with the specified color palette.
**Independent Test**: The site loads in dark mode and the color scheme is applied correctly.

### Implementation for User Story 1
- [X] T003 [US1] In `src/css/custom.css`, define and apply the primary (`#1E1E2F`) and secondary (`#FF7F50`) colors for the dark theme.
- [X] T004 [US1] In `src/css/custom.css`, apply the "Inter" font to the body and headings.
- [X] T005 [US1] In `src/css/custom.css`, add styles for rounded corners and a subtle shadow to images within docs pages.

---

## Phase 3: User Story 2 - Modern Navigation (Priority: P2)
**Goal**: Implement the sticky navbar and collapsible sidebar.
**Independent Test**: The navbar is sticky and the sidebar is collapsible and styled correctly.

### Implementation for User Story 2
- [X] T006 [P] [US2] In `docusaurus.config.ts`, update the navbar to be sticky.
- [X] T007 [US2] In `src/css/custom.css`, add a semi-transparent background with a blur effect to the sticky navbar.
- [X] T008 [P] [US2] In `docusaurus.config.ts`, ensure the sidebar is collapsible.
- [X] T009 [US2] In `src/css/custom.css`, set the sidebar width to 280px and background to `#121212`.
- [X] T010 [US2] In `src/css/custom.css`, style the active chapter in the sidebar.

---

## Phase 4: Polish & Cross-Cutting Concerns
**Purpose**: Final touches and improvements.

- [X] T011 [P] In `docusaurus.config.ts`, add the global search bar to the navbar.
- [X] T012 In `src/css/custom.css`, add hover effects to links in the navbar and footer.
- [X] T013 In `src/css/custom.css`, add smooth animations for sidebar collapse/expand and theme toggle.
