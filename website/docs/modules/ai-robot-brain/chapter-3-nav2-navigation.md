---
title: "Navigation and Path Planning with Nav2"
sidebar_label: "Chapter 3: Nav2 Navigation"
description: "Fundamentals of robotic navigation stacks for bipedal humanoids"
tags: [navigation, nav2, path-planning, obstacle-avoidance, robotics]
learning_objectives:
  - "Understand fundamentals of robotic navigation stacks"
  - "Explain path planning for bipedal humanoids"
  - "Describe obstacle avoidance and environment awareness"
  - "Identify integration of navigation with AI planning"
prerequisites:
  - "Chapters 1 and 2"
  - "Understanding of humanoid robot structure (Module 1)"
estimated_time: "55 minutes"
---

# Chapter 3: Navigation and Path Planning with Nav2

[Return to Quickstart Guide](./quickstart)

## Introduction to Nav2 Navigation Stack

The Navigation2 (Nav2) stack is the next-generation navigation framework for ROS 2, designed to provide reliable path planning and navigation capabilities for mobile robots. Nav2 represents a complete rewrite of the ROS 1 navigation stack with improved architecture, better performance, and enhanced features for modern robotics applications.

For humanoid robots, Nav2 provides the foundation for autonomous navigation, enabling robots to plan paths through complex environments, avoid obstacles, and reach desired destinations safely. While originally designed for wheeled robots, Nav2's modular architecture allows for adaptation to bipedal locomotion with appropriate plugins and parameter tuning.

## Fundamentals of Robotic Navigation

Robotic navigation is the process by which a robot determines how to move from its current location to a desired goal location while avoiding obstacles and respecting environmental constraints. The navigation problem can be broken down into several key components:

### Core Navigation Components

<details>
<summary>Navigation System Components (Accessibility: List of core navigation system elements)</summary>

A typical robotic navigation system includes:

1. **Localization**: Determining the robot's position in the environment
2. **Mapping**: Creating or using a representation of the environment
3. **Path Planning**: Computing a route from start to goal
4. **Motion Control**: Executing the planned path with the robot's actuators
5. **Recovery**: Handling situations where navigation fails or gets stuck

</details>

### Navigation Challenges for Humanoid Robots

Humanoid robots face unique navigation challenges compared to wheeled robots:

- **Bipedal Locomotion**: Requires careful planning to maintain balance
- **Step Constraints**: Must navigate around obstacles that wheeled robots could traverse
- **Dynamic Balance**: Need to maintain stability during movement
- **Limited Turning Radius**: Cannot turn in place like differential drive robots
- **Terrain Sensitivity**: More susceptible to uneven terrain

## Path Planning for Bipedal Humanoids

Path planning is the process of computing a sequence of actions or poses that will move the robot from its current state to a goal state. For humanoid robots, this involves additional considerations compared to wheeled robots.

### Global vs. Local Path Planning

Nav2 implements a layered approach to path planning:

#### Global Planner

The global planner computes a high-level path from start to goal:

<details>
<summary>Global Planner Algorithms (Accessibility: List of path planning algorithms)</summary>

Common global planner algorithms include:

- **A* (A-star)**: Optimal pathfinding algorithm with heuristic
- **Dijkstra**: Finds shortest path without heuristic
- **Theta***: Any-angle pathfinding algorithm
- **Lazy Theta***: Optimized version of Theta*

Each algorithm has different performance characteristics and path quality.

</details>

- Uses a static map of the environment
- Considers known obstacles
- Produces a geometric path (sequence of poses)
- Typically runs less frequently (e.g., when goal changes)

#### Local Planner

The local planner executes the global path while avoiding dynamic obstacles:

- Operates in a local window around the robot
- Incorporates real-time sensor data
- Adjusts path to avoid unexpected obstacles
- Runs at high frequency (e.g., 10-20 Hz)

### Humanoid-Specific Path Planning Considerations

Path planning for bipedal robots requires special considerations:

#### Footstep Planning

Humanoid robots must plan where to place each foot:

- Ensures stable walking patterns
- Considers terrain traversability
- Maintains center of mass within support polygon
- Plans for step height and spacing

#### Kinematic Constraints

Humanoid robots have complex kinematic constraints:

- Joint angle limits
- Balance requirements
- Step height limitations
- Turning radius constraints

## Obstacle Avoidance Strategies

Obstacle avoidance is critical for safe navigation in dynamic environments. Nav2 provides several strategies for obstacle avoidance that can be adapted for humanoid robots.

### Collision Avoidance

The primary goal of obstacle avoidance is to prevent the robot from colliding with obstacles:

- **Static obstacles**: Pre-mapped obstacles that don't move
- **Dynamic obstacles**: Moving objects that must be avoided in real-time
- **Probabilistic obstacles**: Uncertain obstacle locations or movements

### Local Planner Behaviors

Nav2's local planner implements several behaviors for obstacle avoidance:

#### Trajectory Rollout

The local planner evaluates multiple possible trajectories:

- Samples potential paths in the local costmap
- Evaluates each trajectory for collisions and optimality
- Selects the best trajectory based on cost function
- Executes the selected trajectory

#### Recovery Behaviors

When navigation fails, Nav2 implements recovery behaviors:

<details>
<summary>Recovery Behavior Details (Accessibility: Table of navigation recovery behaviors)</summary>

| Behavior | Purpose | When Used | Success Rate |
|----------|---------|-----------|--------------|
| Clearing rotation | Clear stale obstacle data | Robot thinks it's blocked | High |
| Back-up | Escape tight spaces | Robot is too close to walls | Medium |
| Wiggling | Break out of local minima | Robot stuck in potential field | Low to Medium |

Custom recovery behaviors can be implemented for humanoid-specific challenges.

</details>

- **Clearing rotation**: Rotate in place to clear obstacle data
- **Back-up**: Move backward to escape tight spaces
- **Wiggling**: Small movements to break out of local minima

## Environment Awareness and Mapping

Environmental awareness is fundamental to successful navigation. Robots must maintain an understanding of their surroundings to navigate effectively.

### Costmap Representation

Nav2 uses costmaps to represent the environment:

- **Static layer**: Permanent obstacles from the map
- **Obstacle layer**: Dynamic obstacles from sensors
- **Inflation layer**: Safety margins around obstacles
- **Voxel layer**: 3D obstacle information (for humanoid navigation)

### Mapping for Humanoid Robots

Humanoid robots require specialized mapping considerations:

- **3D mapping**: Accounts for obstacles at different heights
- **Traversability analysis**: Determines which areas are safe to step on
- **Terrain classification**: Identifies different surface types
- **Step detection**: Identifies stairs, curbs, and level changes

## Integration with Higher-Level AI Planning

Navigation in humanoid robots is not isolated but integrated with higher-level AI planning systems that make decisions about where to go and what tasks to perform.

### Hierarchical Planning

Navigation integrates with multiple planning levels:

#### Task-Level Planning

- Determines what goals to pursue
- Sequences tasks based on objectives
- Coordinates with other systems

#### Path-Level Planning

- Computes geometric paths between waypoints
- Considers environmental constraints
- Integrates with motion planning

#### Motion-Level Planning

- Generates joint trajectories for locomotion
- Maintains balance during movement
- Coordinates with control systems

### Behavior Trees for Navigation

Modern navigation systems often use behavior trees to organize complex navigation behaviors:

- **Modular**: Each behavior is a separate node
- **Composable**: Behaviors can be combined in different ways
- **Debuggable**: Individual behaviors can be tested independently
- **Reactive**: System can respond to changing conditions

### Example Integration Architecture

<details>
<summary>Humanoid Navigation Integration (Accessibility: Diagram of navigation system architecture)</summary>

```
High-Level AI Planner
    ↓ (goals, tasks)
Task Manager
    ↓ (waypoints, constraints)
Nav2 Navigation System
    ↓ (local paths, commands)
Motion Control System
    ↓ (joint commands)
Humanoid Robot
```

</details>

## Knowledge Check

Test your understanding of Nav2 navigation concepts:

<details>
<summary>Knowledge Check: Nav2 Navigation</summary>

1. What are the differences between global and local planners in Nav2?
   - Answer: Global planner computes a high-level path from start to goal using static maps; Local planner executes the global path while avoiding dynamic obstacles in real-time.

2. What are the main challenges of navigation for humanoid robots compared to wheeled robots?
   - Answer: Humanoid robots face challenges like bipedal locomotion requirements, step constraints, dynamic balance needs, and limited turning radius.

3. What is the purpose of costmaps in Nav2?
   - Answer: Costmaps represent the environment with layers for static obstacles, dynamic obstacles, and safety margins to enable safe navigation.

</details>

## Chapter Summary and Key Takeaways

In this chapter, we've explored Nav2 as the navigation stack for humanoid robots. Key takeaways include:

- Nav2 provides a robust framework for path planning and navigation in ROS 2
- Humanoid robots require special considerations for bipedal locomotion in path planning
- Obstacle avoidance strategies must account for dynamic balance requirements
- Environmental awareness through costmaps is essential for safe navigation
- Integration with higher-level AI planning enables complex autonomous behaviors

[Return to Chapter 1: Isaac Sim and Synthetic Data](./chapter-1-isaac-sim) to review simulation concepts, or [return to Chapter 2: Isaac ROS for Perception and VSLAM](./chapter-2-isaac-ros-perception) to review perception capabilities that inform navigation decisions. This concludes Module 3: The AI-Robot Brain (NVIDIA Isaac™), which has covered the complete pipeline from simulation and perception to navigation for humanoid robots. The next module will integrate these capabilities in a capstone project.