// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1/intro',
        'module-1/chapter-1-introduction-to-ros2',
        'module-1/chapter-2-ros2-communication-primitives',
        'module-1/chapter-3-urdf-humanoid-robot-structure'
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'modules/digital-twin-simulation/intro',
        'modules/digital-twin-simulation/chapter-1-gazebo-simulation',
        'modules/digital-twin-simulation/chapter-2-unity-environments',
        'modules/digital-twin-simulation/chapter-3-virtual-sensors'
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'modules/ai-robot-brain/chapter-1-isaac-sim',
        'modules/ai-robot-brain/chapter-2-isaac-ros-perception',
        'modules/ai-robot-brain/chapter-3-nav2-navigation'
      ],
    },
  ],
};

export default sidebars;
