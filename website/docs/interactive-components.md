# Interactive Components Documentation

This document provides an overview of the interactive components created for the Docusaurus website, including their purpose, usage, and API.

## Components Overview

### InteractiveSidebar
A collapsible sidebar navigation component with keyboard accessibility support.

**Props:**
- `items`: Array of navigation items with title, path, and optional children
- `currentPath`: Current active path for highlighting
- `isCollapsed`: Whether the sidebar is collapsed
- `className`: Additional CSS classes

**Features:**
- Collapsible sections with keyboard navigation
- Active path highlighting
- Responsive design
- Accessibility compliance

### ResponsiveNavbar
A responsive navigation bar that adapts to different screen sizes.

**Props:**
- `logo`: Logo object with alt, src, and href
- `title`: Navbar title
- `items`: Navigation items array
- `className`: Additional CSS classes

**Features:**
- Mobile menu toggle
- Responsive breakpoints
- Scroll effects
- Accessibility compliance

### Breadcrumb
Breadcrumb navigation component showing the user's current location.

**Props:**
- `items`: Breadcrumb items array
- `className`: Additional CSS classes
- `homeLabel`: Label for home link
- `separator`: Separator character between items

**Features:**
- Dynamic breadcrumb generation
- Accessibility attributes
- Responsive design

### ExpandableSection
Collapsible content sections with smooth animations.

**Props:**
- `title`: Section title
- `children`: Content to be expanded/collapsed
- `defaultExpanded`: Whether to start expanded
- `className`: Additional CSS classes
- `onToggle`: Callback when expanded state changes

**Features:**
- Smooth animations
- Keyboard navigation
- Accessibility compliance

### InteractiveCodeBlock
Interactive code block with copy functionality.

**Props:**
- `code`: Code string to display
- `language`: Programming language for syntax highlighting
- `showLineNumbers`: Whether to show line numbers
- `title`: Optional title for the code block
- `className`: Additional CSS classes
- `onCopy`: Callback when code is copied

**Features:**
- Copy to clipboard functionality
- Line numbers
- Syntax highlighting
- Accessibility support

### KnowledgeCheck
Interactive quiz component for knowledge validation.

**Props:**
- `question`: The question text
- `options`: Array of answer options
- `explanation`: Explanation for the correct answer
- `className`: Additional CSS classes
- `onComplete`: Callback when quiz is completed

**Features:**
- Multiple choice questions
- Immediate feedback
- Explanation display
- Accessibility compliance

### TabbedInterface
Tabbed interface for multi-language code examples.

**Props:**
- `tabs`: Array of tab items with label and content
- `defaultActiveTab`: Index of the default active tab
- `className`: Additional CSS classes

**Features:**
- Keyboard navigation
- Tab management
- Accessibility attributes

## State Management

The interactive components use a centralized React Context for state management:

- `InteractiveContextProvider`: Provides global state to all interactive components
- `useInteractiveContext`: Hook to access the global state
- `useInteractiveActions`: Hook to dispatch actions to update state

### Shared State Properties

#### UI State
- `sidebarCollapsed`: Whether the sidebar is collapsed
- `theme`: Current theme (light/dark/auto)
- `mobileMenuOpen`: Whether the mobile menu is open
- `currentBreakpoint`: Current responsive breakpoint
- `language`: Current language
- `accessibilityMode`: Whether accessibility mode is enabled

#### Navigation State
- `currentPath`: Current active path
- `expandedSections`: List of expanded section IDs
- `breadcrumbTrail`: Current breadcrumb trail

## Usage Example

```jsx
import InteractiveUIProvider from './components/InteractiveUIProvider';
import InteractiveSidebar from './components/InteractiveSidebar/InteractiveSidebar';
import ResponsiveNavbar from './components/ResponsiveNavbar/ResponsiveNavbar';

function App() {
  return (
    <InteractiveUIProvider>
      <ResponsiveNavbar
        title="My Docs"
        items={[
          { label: 'Home', to: '/' },
          { label: 'Docs', to: '/docs' }
        ]}
      />
      <InteractiveSidebar
        items={[
          { title: 'Getting Started', path: '/docs/getting-started' },
          {
            title: 'Advanced Topics',
            path: '/docs/advanced',
            children: [
              { title: 'Configuration', path: '/docs/advanced/config' }
            ]
          }
        ]}
        currentPath="/docs/getting-started"
      />
    </InteractiveUIProvider>
  );
}
```

## Accessibility Features

All components include:
- Proper ARIA attributes
- Keyboard navigation support
- Screen reader compatibility
- Focus management
- High contrast mode support
- Reduced motion support

## Responsive Design

Components adapt to:
- Mobile (up to 768px)
- Tablet (768px - 996px)
- Desktop (996px+)

## Styling

- CSS Modules for scoped styling
- Responsive breakpoints
- Theme support
- Accessibility-focused styles
- Smooth animations with reduced motion support