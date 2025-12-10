# Data Model (UI Component Structure)

This document defines the structure of the UI components for the "Modern & Interactive Docusaurus Interface" feature.

## Key Entities

- **Theme**: A global set of CSS variables and styles that define the look and feel of the site.
- **Navbar**: The main navigation bar at the top of the page.
- **Sidebar**: The collapsible navigation sidebar for the documentation.
- **Footer**: The footer at the bottom of the page.
- **DocsPage**: The container for the documentation content.
- **Card**: A styled container for a section of content.
- **Search**: The global search component.

## Component Hierarchy

The UI will be composed of the following components:

```
- Root
  - Navbar
    - Brand
    - Links (Home, Chapters, About, Contact)
    - Search
  - Sidebar
    - Module (Category)
      - Chapter (Doc)
  - DocsPage
    - Card
      - Title
      - Content
  - Footer
    - Links (GitHub, Documentation)
    - Copyright
```

## Entity: Theme

- **Description**: Defines the global styles for the site.
- **Properties**:
    - `primary-color`: `#1E1E2F`
    - `secondary-color`: `#FF7F50`
    - `font-family`: "Inter", sans-serif

## Entity: Navbar

- **Description**: The top navigation bar.
- **Properties**:
    - `sticky`: `true`
    - `background`: `rgba(30, 30, 47, 0.8)` with `backdrop-filter: blur(10px)`

## Entity: Sidebar

- **Description**: The documentation sidebar.
- **Properties**:
    - `collapsible`: `true`
    - `width`: `280px`
    - `background`: `#121212`
    - `active-chapter-background`: `#FF7F50`

## Entity: Card

- **Description**: A styled container for a section of content on the docs pages.
- **Properties**:
    - `background`: `#1E1E2F`
    - `border-radius`: `8px`
    - `box-shadow`: `0 4px 6px rgba(0, 0, 0, 0.1)`
