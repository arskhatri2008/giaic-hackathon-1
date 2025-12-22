---
title: "Module 3 Assessment - AI-Robot Brain (NVIDIA Isaac™)"
sidebar_label: "Assessment"
description: "Assessment questions to validate learning outcomes for Module 3"
---

# Module 3 Assessment - AI-Robot Brain (NVIDIA Isaac™)

This assessment validates the learning outcomes for Module 3, covering NVIDIA Isaac Sim, Isaac ROS perception, and Nav2 navigation for humanoid robots.

## Assessment Questions

### SC-001: Users understand Isaac's role as the AI brain for humanoid robots with at least 85% accuracy on assessment questions

1. What is the primary role of NVIDIA Isaac in humanoid robotics?
   a) A communication protocol for robot networks
   b) An AI brain that enables perception, navigation, and training through simulation and robotics frameworks
   c) A hardware component for motor control
   d) A programming language for robotics

2. Which of the following best describes the relationship between Isaac Sim, Isaac ROS, and Nav2 in the AI brain architecture?
   a) They are competing technologies
   b) They serve completely independent functions
   c) They form a pipeline from simulation and perception to navigation for humanoid robots
   d) They only work with wheeled robots

### SC-006: Users can complete understanding of Isaac's perception capabilities in under 45 minutes of learning time

3. What are the key perception capabilities provided by Isaac ROS?
   a) Only camera processing
   b) Hardware-accelerated perception pipelines including Visual SLAM and sensor fusion
   c) Only navigation planning
   d) Only simulation capabilities

4. How does Visual SLAM contribute to humanoid robot autonomy?
   a) It provides communication between robots
   b) It enables robots to simultaneously localize themselves and map their environment
   c) It controls the robot's motors
   d) It manages the robot's power consumption

### Additional Assessment Questions

5. What is the purpose of domain randomization in Isaac Sim?
   a) To make simulations run faster
   b) To vary visual and physical parameters during training to improve sim-to-real transfer
   c) To reduce the need for sensors
   d) To limit the robot's movement

6. Which sensors are commonly fused in Isaac ROS perception systems for humanoid robots?
   a) Only cameras
   b) Only IMUs
   c) Cameras and IMUs
   d) Only LiDAR sensors

7. What are the main challenges of path planning for bipedal humanoids compared to wheeled robots?
   a) No differences exist
   b) Bipedal locomotion requires careful balance and step constraint considerations
   c) Humanoid robots are faster
   d) Humanoid robots need less computation

8. How does Nav2 handle dynamic obstacle avoidance?
   a) By stopping the robot permanently
   b) Through local planner behaviors that adjust paths in real-time
   c) By ignoring moving obstacles
   d) By slowing down the robot only

9. What is the role of costmaps in Nav2 navigation?
   a) To store robot code
   b) To represent the environment with static and dynamic obstacles
   c) To manage robot hardware
   d) To store robot logs

10. How does Isaac Sim bridge simulation to reality?
    a) Through domain randomization and adaptation techniques
    b) By replacing real robots completely
    c) By reducing the need for perception
    d) Through hardware upgrades only

## Answer Key

1. b) An AI brain that enables perception, navigation, and training through simulation and robotics frameworks
2. c) They form a pipeline from simulation and perception to navigation for humanoid robots
3. b) Hardware-accelerated perception pipelines including Visual SLAM and sensor fusion
4. b) It enables robots to simultaneously localize themselves and map their environment
5. b) To vary visual and physical parameters during training to improve sim-to-real transfer
6. c) Cameras and IMUs
7. b) Bipedal locomotion requires careful balance and step constraint considerations
8. b) Through local planner behaviors that adjust paths in real-time
9. b) To represent the environment with static and dynamic obstacles
10. a) Through domain randomization and adaptation techniques

## Scoring

- **Passing Score**: 85% (8.5 out of 10 questions correct)
- **Time Limit**: 45 minutes
- **Purpose**: Validate understanding of Isaac's role as the AI brain for humanoid robots