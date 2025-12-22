# Physical AI & Humanoid Robotics - Module 1: The Robotic Nervous System (ROS 2)

This documentation website provides comprehensive learning materials for understanding ROS 2 as the foundational nervous system for humanoid robots. It enables communication, control, and structural description of embodied AI systems.

## About This Module

Module 1: The Robotic Nervous System (ROS 2) introduces:

- **Introduction to ROS 2**: What ROS 2 is and why it exists, comparing it to traditional software architectures
- **Communication Primitives**: Understanding Nodes, Topics, Services, and Actions in ROS 2
- **Robot Structure with URDF**: Using Unified Robot Description Format to model humanoid robots

This module is designed for AI engineers and software developers transitioning into robotics, with Python and basic AI background.

## Interactive UI Features

This website includes a comprehensive suite of interactive UI components designed to enhance the learning experience:

### Navigation Components
- **Interactive Sidebar**: Collapsible navigation with keyboard accessibility support
- **Responsive Navbar**: Adapts to different screen sizes with mobile menu toggle
- **Breadcrumb Navigation**: Shows current location in the documentation hierarchy

### Content Components
- **Expandable Sections**: Collapsible content sections with smooth animations
- **Interactive Code Blocks**: Syntax-highlighted code with copy functionality
- **Knowledge Checks**: Interactive quizzes for validating understanding
- **Tabbed Interfaces**: Multi-language code examples in organized tabs

### Accessibility & Performance
- **WCAG 2.1 AA Compliance**: Full accessibility support with keyboard navigation
- **Responsive Design**: Works on mobile, tablet, and desktop devices
- **Performance Optimized**: React.memo and lazy loading for fast rendering
- **Theme Support**: Light/dark mode switching capability

## Learning Objectives

After completing this module, learners will be able to:
- Explain ROS 2 architecture and terminology
- Build basic ROS 2 nodes in Python using rclpy
- Understand how humanoid robots are structurally described using URDF
- Conceptually map AI decision-making to ROS execution

## Getting Started

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

### Installation

```bash
yarn
```

### Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server. Navigate to [http://localhost:3000](http://localhost:3000) to view the documentation.

### Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Project Structure

The documentation is organized into the following chapters under the "Module 1" section:
- Chapter 1: Introduction to ROS 2 as a Robotic Nervous System
- Chapter 2: ROS 2 Communication Primitives
- Chapter 3: Humanoid Robot Structure with URDF

Each chapter includes practical examples, visual diagrams, and hands-on exercises to reinforce learning.
