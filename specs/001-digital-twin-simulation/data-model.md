# Data Model: Digital Twin Simulation for Humanoid Robotics

## Overview
Conceptual data models for the Digital Twin Simulation module documentation. These models represent the key concepts and relationships that will be explained in the three chapters.

## Entity: Digital Twin
**Definition**: A virtual representation of a physical humanoid robot that includes physics, visual, and sensor properties for simulation purposes

**Attributes**:
- `id`: Unique identifier for the digital twin instance
- `robotModel`: Reference to the humanoid robot URDF model
- `physicsProperties`: Gravity, mass, friction, and collision parameters
- `visualProperties`: Appearance, textures, and rendering parameters
- `sensorConfiguration`: List of virtual sensors attached to the robot
- `environment`: Reference to the simulation environment

**Relationships**:
- One Digital Twin connects to one Robot Model (URDF)
- One Digital Twin connects to one Environment
- One Digital Twin connects to many Virtual Sensors

## Entity: Simulation Environment
**Definition**: A virtual space that includes physics properties, environmental conditions, and interactive objects for robot testing

**Attributes**:
- `id`: Unique identifier for the environment
- `name`: Descriptive name of the environment
- `physicsEngine`: Reference to the physics engine (e.g., Gazebo)
- `visualEngine`: Reference to the rendering engine (e.g., Unity)
- `objects`: List of static and dynamic objects in the environment
- `environmentalConditions`: Lighting, gravity, atmospheric properties

**Relationships**:
- One Environment connects to many Digital Twins
- One Environment connects to many Objects

## Entity: Virtual Sensor
**Definition**: Simulated perception devices that generate realistic sensor data for testing perception and planning algorithms

**Attributes**:
- `id`: Unique identifier for the sensor
- `type`: Sensor type (LiDAR, RGB Camera, Depth Camera, IMU, etc.)
- `position`: Position relative to the robot base
- `orientation`: Orientation relative to the robot base
- `parameters`: Sensor-specific configuration parameters
- `noiseModel`: Parameters for simulating realistic sensor noise

**Relationships**:
- One Virtual Sensor connects to one Digital Twin
- One Virtual Sensor produces many Sensor Data readings

## Entity: Sensor Data
**Definition**: The output from virtual sensors that feeds into perception and planning systems

**Attributes**:
- `id`: Unique identifier for the data reading
- `sensorId`: Reference to the sensor that produced the data
- `timestamp`: Time when the data was captured
- `data`: The actual sensor reading (point cloud, image, etc.)
- `frameId`: Coordinate frame of reference for the data

**Relationships**:
- One Sensor Data connects to one Virtual Sensor
- Many Sensor Data readings connect to one Perception System

## Entity: ROS 2 Integration
**Definition**: Communication interfaces that allow simulated robots to interact with ROS 2 control systems and nodes

**Attributes**:
- `nodeName`: Name of the ROS 2 node
- `topics`: List of topics for communication
- `services`: List of services for communication
- `actions`: List of actions for communication
- `messageTypes`: Types of messages used in communication

**Relationships**:
- One ROS 2 Integration connects to one Digital Twin
- One ROS 2 Integration connects to many Topics, Services, and Actions

## Entity: Perception System
**Definition**: The system that processes sensor data to extract meaningful information about the environment

**Attributes**:
- `id`: Unique identifier for the perception system
- `algorithms`: List of perception algorithms used
- `outputs`: Types of information produced (objects, obstacles, etc.)
- `parameters`: Configuration parameters for perception algorithms

**Relationships**:
- One Perception System consumes many Sensor Data readings
- One Perception System connects to one Planning System

## Entity: Planning System
**Definition**: The system that uses perception information to make decisions about robot behavior

**Attributes**:
- `id`: Unique identifier for the planning system
- `algorithms`: List of planning algorithms used
- `goals`: Types of goals the system can handle
- `constraints`: Physical and environmental constraints

**Relationships**:
- One Planning System receives input from one Perception System
- One Planning System produces commands for one Control System

## Entity: Control System
**Definition**: The system that translates planning decisions into robot actuator commands

**Attributes**:
- `id`: Unique identifier for the control system
- `controllers`: List of controllers (position, velocity, etc.)
- `jointNames`: Names of joints being controlled
- `parameters`: Control parameters (gains, limits, etc.)

**Relationships**:
- One Control System receives commands from one Planning System
- One Control System connects to one Digital Twin

## State Transitions

### Digital Twin States
- **Idle**: Digital twin exists but not running simulation
- **Initializing**: Loading robot model and environment
- **Running**: Simulation is active with physics and sensors
- **Paused**: Simulation temporarily stopped
- **Stopped**: Simulation ended, data preserved

### Sensor Data States
- **Pending**: Sensor has been configured but not yet active
- **Active**: Sensor is collecting data
- **Processing**: Data is being processed by perception system
- **Ready**: Data is ready for use by downstream systems

## Validation Rules

### From Functional Requirements
- **FR-001**: Physics properties must include gravity, collisions, friction, and joint constraints
- **FR-002**: Must support integration with ROS 2 control loops
- **FR-003**: Must allow safe simulation without real-world hardware damage
- **FR-004**: Must support multiple sensor types (LiDAR, cameras, IMUs)
- **FR-005**: Sensor data must include realistic noise characteristics
- **FR-006**: Must synchronize physics and visual simulation
- **FR-007**: Must support sim-to-real transfer considerations
- **FR-008**: Must provide high-fidelity visual environments
- **FR-009**: Must allow repeatable and controlled scenarios
- **FR-010**: Must support URDF-compatible robot models