# Robotics & Embedded ROS 2 Control Stack

An independent, hands-on exploration of the Robot Operating System (**ROS 2 Jazzy**), embedded hardware-in-the-loop interfacing, closed-loop actuator control, and reactive autonomous navigation.

---

## 📌 Project Overview

This repository was created as an exploratory self-study project to acquire practical, end-to-end competencies in modern robotics engineering. The goal was to bridge low-level embedded hardware with high-level robotic autonomy:

- **Hardware-Software Interfacing**: Developing asynchronous serial communication bridges between microcontrollers (STM32 with onboard IMU and motor encoders) and the ROS 2 computational graph.
- **Actuator Teleoperation & Feedback Control**: Implementing synchronized master-slave teleoperation, closed-loop position control, and proportional-derivative (PD) impedance control loops with runtime parameter reconfiguration.
- **Kinematics & 3D Visualization**: Estimating robot state and dead-reckoning motion through IMU acceleration integration and encoder tick decoding, broadcasting dynamic coordinate frames via `tf2_ros` for real-time tracking in RViz2.
- **Autonomous Reactive Navigation**: Designing and deploying a reactive Bug0 obstacle avoidance controller that processes 2D LiDAR range scans (`LaserScan`) to navigate simulated and physical differential drive robots.

---

## 🏛️ System Architecture

The workspace is organized into modular ROS 2 packages adhering to best practices in interface decoupling, node composability, and testing:

```text
Robotics-Intro/
├── bags/                           # Telemetry logs and rosbag recordings
├── deliverables/                   # Experimental validation screenshots and plots
└── src/
    ├── first_interfaces/           # Custom message & service definitions for foundation nodes
    │   ├── msg/ExampleMessage.msg
    │   └── srv/ExampleService.srv
    │
    ├── first_package/              # Core communication fundamentals
    │   ├── simple_publisher.py     # Periodic string telemetry publisher
    │   ├── simple_subscriber.py    # Listener node with callback execution
    │   ├── simple_pubsub_node.py   # Bidirectional message forwarder node
    │   ├── simple_service.py       # Integer addition service server
    │   └── simple_service_parameter.py # Service with dynamic runtime parameter tuning
    │
    ├── stm_interfaces/             # Specialized embedded communication interfaces
    │   ├── msg/STMState.msg        # Telemetry: encoder ticks, velocity, 3-axis accel & gyro
    │   ├── msg/STMControl.msg      # Actuator command: control mode, setpoint, Kp, PWM
    │   └── srv/STMSetControlType.srv # Runtime mode and gain configuration service
    │
    └── stm_station/                # Primary hardware bridge, controllers & navigation package
        ├── config/                 # Parameter configurations (YAML)
        │   ├── bug0_params.yaml    # Obstacle avoidance distances and velocities
        │   └── serial_params.yaml  # Serial port, baud rate, and device namespace parameters
        ├── launch/                 # Modular system launch files
        │   ├── stm_serial_node_launch.py      # Standalone hardware bridge
        │   ├── stm_station_launch.py          # Serial bridge + master-slave controller
        │   ├── stm_station_launch_all.py      # Full stack: bridge, controller, TF node & RViz
        │   ├── stm_visualization_launch.py    # Telemetry tracking & RViz visualization
        │   └── stm_bug0_launch.py             # Reactive Bug0 navigation launch
        ├── rviz/
        │   └── stm_config.rviz     # Pre-configured RViz display layout
        ├── stm_station/            # Node implementations & Python modules
        │   ├── bug0.py             # Pure-Python Bug0 decision logic & sector extraction
        │   ├── bug0_node.py        # Reactive LiDAR obstacle avoidance ROS 2 node
        │   ├── control_master_slave.py  # Master-slave synchronized position tracking
        │   ├── control_position.py      # Closed-loop proportional (P) position controller
        │   ├── control_node.py          # Closed-loop PD impedance controller
        │   ├── motion.py           # IMU integration & dead-reckoning kinematics model
        │   ├── protocol.py         # Serial packet serialization and framing
        │   ├── serial_node.py      # Bidirectional serial bridge using STMState/STMControl
        │   ├── turtlebot_control.py # Actuator-to-velocity teleoperation mapping
        │   └── visualization_node.py # IMU/Encoder integration & TF transform broadcaster
        └── test/                   # Automated unit test suite (pytest)
```

---

## ⚙️ Core Technical Modules

### 1. Embedded Serial Hardware Bridge
The serial communication layer (`serial_node.py`) establishes high-frequency (1 kHz) bidirectional data streaming with microcontroller firmware over USB/UART:
- **Telemetry Parsing**: Decodes ASCII brace-framed packets `"{enc, vel, ax, ay, az, gx, gy, gz}\n"` into typed, timestamped `stm_interfaces/msg/STMState` messages.
- **Command Transmission**: Formats actuator drive packets `"{mode, setpoint, kp, pwm}\n"` with safety clamps (PWM bounded to $\pm 250$) and safe watchdog timeout handling.
- **Standard & Custom Interfaces**: Supports both standard ROS `Float32MultiArray` arrays and strongly-typed custom interfaces.

### 2. Master-Slave Teleoperation & Closed-Loop Control
Enables dual-actuator synchronization where a remote slave station tracks the state of a master unit:
- **Dynamic Service Configuration**: The `set_control_type` service (`STMSetControlType`) allows switching control modes on the fly:
  - **Mode 0 (Stop / Disarm)**: Actuators immediately halted.
  - **Mode 1 (Onboard Position Tracking)**: Master encoder position transmitted as a setpoint to the slave firmware position regulator.
  - **Mode 2 (Closed-Loop Host Control)**:
    - *Proportional (P) Position Control* (`control_position.py`):
      $$u_{\text{pwm}} = \text{clamp}(K_p \cdot (p_{\text{master}} - p_{\text{slave}}), -250, 250)$$
    - *Impedance / PD Control* (`control_node.py`):
      $$u_{\text{pwm}} = \text{clamp}(K_p \cdot (p_{\text{master}} - p_{\text{slave}}) + K_d \cdot (v_{\text{master}} - v_{\text{slave}}), -250, 250)$$
- **Dynamic Reconfiguration**: ROS 2 parameter callbacks (`parameter_callback`) reconfigure topic subscriptions and publisher namespaces at runtime without taking down the node.

### 3. Kinematics, Dead-Reckoning & RViz Visualization
The visualization subsystem (`visualization_node.py`, `motion.py`) tracks the 3D pose of the robot/actuator:
- **Orientation Calculation**: Computes actuator yaw angle from raw optical encoder ticks:
  $$\theta = \text{ticks} \cdot \frac{2\pi}{24 \cdot 9.7} \quad (\text{24 ticks/rev, 9.7:1 gear reduction})$$
- **Inertial Dead-Reckoning**: Integrates 3-axis linear acceleration ($a_x, a_y, a_z$) to estimate velocity and translation:
  - Performs baseline bias calibration over the initial stationary samples.
  - Applies a deadband filter ($0.5 \, \text{m/s}^2$) to suppress sensor noise drift during zero-velocity intervals.
- **TF2 Transform Broadcasting**: Streams the dynamic transform tree (`world` $\to$ `stm_station`) with converted Euler-to-quaternion rotations for real-time visualization in RViz2.

### 4. Autonomous Reactive Navigation (Bug0 Algorithm)
A complete reactive obstacle avoidance pipeline (`bug0_node.py`, `bug0.py`):
- **Sector Segmentation**: Partitions the 2D planar LiDAR scan (`sensor_msgs/msg/LaserScan`) into forward-facing angular sectors:
  - **Front Sector**: $[-30^\circ, +30^\circ]$
  - **Left Sector**: $[+30^\circ, +90^\circ]$
  - **Right Sector**: $[-90^\circ, -30^\circ]$
- **Reactive Policy**:
  - If front clearance $> 1.0 \, \text{m}$: commands forward drive ($v_x = 0.3 \, \text{m/s}$).
  - If front obstacle detected ($\le 1.0 \, \text{m}$): halts linear motion and initiates an in-place rotation towards whichever side offers greater clearance ($\omega_z = \pm 0.5 \, \text{rad/s}$).
  - Employs hysteresis (resumes forward cruising only after front clearance exceeds $1.2 \, \text{m}$) to eliminate state chatter.
  - Halts execution safely if side clearance falls below emergency margins ($0.4 \, \text{m}$) or if scan data becomes stale/invalid.
- **Dual Output**: Publishes both `geometry_msgs/msg/TwistStamped` for differential drive simulation (Gazebo / TurtleBot) and `stm_interfaces/msg/STMControl` for embedded motor driving.

---

## 🚀 Getting Started

### Prerequisites
- **Operating System**: Ubuntu 24.04 LTS (Noble Numbat)
- **ROS 2 Distribution**: ROS 2 Jazzy Jalisco
- **Build System**: `colcon` and `ament_python` / `ament_cmake`
- **Dependencies**:
  ```bash
  sudo apt-get update
  sudo apt-get install -y python3-serial python3-numpy python3-pytest \
      ros-jazzy-tf-transformations ros-jazzy-tf2-ros ros-jazzy-rviz2
  ```

### Build & Workspace Setup
Clone the repository and build using `colcon`:

```bash
# Source the ROS 2 environment
source /opt/ros/jazzy/setup.bash

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build the workspace
colcon build --symlink-install

# Source the local workspace overlay
source install/setup.bash
```

---

## 💻 Running the Nodes

### 1. Standalone Serial Communication Bridge
To connect to a microcontroller device on `/dev/ttyACM0`:

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p serial_port:=/dev/ttyACM0
```

Inspect the incoming telemetry stream:
```bash
ros2 topic echo /group_7/stm_state --once
```

### 2. Master-Slave Teleoperation
Launch both master and slave bridges (or connect with a partner node), then run the control node:

```bash
# Start the controller with master ID 7 and slave ID 2
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2
```

Enable position tracking or PD impedance control via service:
```bash
# Mode 1: Onboard position tracking
ros2 service call /group_7/set_control_type stm_interfaces/srv/STMSetControlType "{control_type: 1, kp: 1.0, kd: 0.0}"

# Mode 2: Closed-loop PD impedance control (Kp=1.2, Kd=0.1)
ros2 service call /group_7/set_control_type stm_interfaces/srv/STMSetControlType "{control_type: 2, kp: 1.2, kd: 0.1}"

# Disarm / Stop
ros2 service call /group_7/set_control_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"
```

### 3. Complete System Launch (Bridge + Control + RViz2)
To launch all nodes simultaneously with RViz visualization:

```bash
ros2 launch stm_station stm_station_launch_all.py
```

### 4. Autonomous Navigation (Bug0 with LiDAR)
Run the reactive obstacle avoidance node connected to a simulator or live laser scanner:

```bash
ros2 launch stm_station stm_bug0_launch.py
```

Inspect velocity commands:
```bash
ros2 topic echo /diff_drive_controller/cmd_vel
```

---

## 🧪 Testing & Verification

The project includes an automated test suite verifying protocol framing, kinematics calculations, and decision algorithms:

```bash
# Run the unit tests
PYTHONPATH=src/stm_station python3 -m pytest src/stm_station/test -v
```

Test coverage includes:
- `test_protocol.py`: Verifies packet framing, floating-point parsing, and saturation limits.
- `test_motion.py`: Tests bias offset calibration, time-step validity, and encoder scaling.
- `test_bug0.py`: Validates sector partitioning, geometric invariance, and obstacle turning decisions.
- `test_package_assets.py`: Validates setup entry points, resource indexes, and launch packaging.
- `test_ros_launch.py`: Asserts correct construction of all ROS 2 launch descriptions.

Telemetry recordings from test sessions are archived in `bags/` and can be replayed using:
```bash
ros2 bag play bags/d11_capture01
```

---

## 👤 Author

**Leonor Guedes**  
- Email: [leonorecaguedes@gmail.com](mailto:leonorecaguedes@gmail.com)  
- GitHub: [@LeoPlix](https://github.com/LeoPlix)  

*Developed as an independent practical study in robotics engineering and embedded control systems.*
