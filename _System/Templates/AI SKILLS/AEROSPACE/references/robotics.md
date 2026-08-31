# Robotics Reference

## Scope

ROS2 node/package architecture, robot kinematics & dynamics, motion planning,
SLAM, perception pipelines, Gazebo simulation, URDF/XACRO modeling, and
hardware interface layers.

---

## 1. ROS2 Engineering Standards

### Package Structure (ament_cmake or ament_python)

```
robot_pkg/
├── CMakeLists.txt / setup.py
├── package.xml                  # All deps explicit with version bounds
├── config/
│   └── params.yaml              # All parameters externalized here
├── launch/
│   └── robot.launch.py
├── urdf/
│   └── robot.urdf.xacro
├── src/ (C++) or robot_pkg/ (Python)
│   ├── node_name.cpp / node_name.py
│   └── ...
├── include/robot_pkg/ (C++ only)
│   └── node_name.hpp
├── test/
│   └── test_node_name.cpp / test_node_name.py
└── msg/ srv/ action/            # Custom interfaces
```

### Node Design Principles

- **Single Responsibility**: One node = one well-defined function.
- **Parameter-driven**: No hardcoded values. All tunable parameters in `params.yaml`,
  declared with `declare_parameter()` with type and description.
- **QoS policies**: Always explicitly set QoS profiles. Do not use defaults.
  - Sensor data: `SensorDataQoS` (best effort, volatile).
  - State / control: `SystemDefaultsQoS` or reliable + transient local.
- **Lifecycle nodes**: Use `rclcpp_lifecycle::LifecycleNode` for all hardware-interfacing nodes.
- **Executors**: Use `MultiThreadedExecutor` with callback groups for concurrent I/O.
- **Timers**: Use `WallTimer` for control loops; verify jitter with `ros2 topic hz`.

### C++ Node Template

```cpp
/**
 * @file controller_node.cpp
 * @brief Closed-loop joint controller node for [Robot Name].
 *
 * Author    : [Name]
 * Date      : [YYYY-MM-DD]
 * Standard  : Google C++ Style Guide, MISRA C++:2008 (where applicable)
 * ROS2 ver  : Humble / Iron
 * Units     : SI throughout (rad, rad/s, N·m, s)
 */

#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

class ControllerNode : public rclcpp::Node {
public:
  explicit ControllerNode(const rclcpp::NodeOptions& options)
  : Node("controller_node", options)
  {
    // Declare parameters with defaults and descriptions
    this->declare_parameter<double>("control_frequency_hz", 500.0);
    this->declare_parameter<std::vector<double>>("kp_gains", {1.0, 1.0, 1.0});

    const double freq = this->get_parameter("control_frequency_hz").as_double();
    assert(freq > 0.0 && freq <= 2000.0);  // Sanity check [Hz]

    const auto period = std::chrono::duration<double>(1.0 / freq);
    timer_ = this->create_wall_timer(period,
      std::bind(&ControllerNode::control_loop_callback, this));

    joint_state_sub_ = this->create_subscription<sensor_msgs::msg::JointState>(
      "/joint_states", rclcpp::SensorDataQoS(),
      std::bind(&ControllerNode::joint_state_callback, this, std::placeholders::_1));

    cmd_pub_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(
      "/joint_commands", rclcpp::SystemDefaultsQoS());

    RCLCPP_INFO(this->get_logger(), "ControllerNode initialized at %.1f Hz", freq);
  }

private:
  void joint_state_callback(const sensor_msgs::msg::JointState::SharedPtr msg);
  void control_loop_callback();

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_state_sub_;
  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr cmd_pub_;
};
```

---

## 2. Kinematics & Dynamics

### Forward Kinematics — DH Convention

- Always use **Modified DH parameters** (Craig convention) for consistency with `roboticstoolbox`.
- Represent poses as **homogeneous transformation matrices** `T ∈ SE(3)` or `(R, t)` pairs.
- For redundant manipulators: use **pseudo-inverse Jacobian** with null-space projection for
  secondary objectives (joint limit avoidance, singularity avoidance).

### Singularity Handling

```python
import numpy as np

SINGULARITY_THRESHOLD = 1e-3  # Manipulability threshold [dimensionless]

def damped_pseudoinverse(J: np.ndarray, lambda_damp: float = 1e-4) -> np.ndarray:
    """Levenberg-Marquardt damped pseudo-inverse for singularity robustness.

    Parameters
    ----------
    J : np.ndarray, shape (m, n)
        Jacobian matrix [m outputs, n joints].
    lambda_damp : float
        Damping factor. Increase near singularities.

    Returns
    -------
    np.ndarray, shape (n, m)
        Damped pseudo-inverse J^+.

    Reference
    ---------
    Nakamura & Hanafusa (1986), "Inverse kinematic solutions with singularity robustness."
    """
    assert J.ndim == 2, "Jacobian must be a 2D matrix"
    m, n = J.shape
    manipulability = np.sqrt(max(0.0, np.linalg.det(J @ J.T)))
    if manipulability < SINGULARITY_THRESHOLD:
        lambda_damp *= 10.0  # Increase damping near singularities
    return J.T @ np.linalg.inv(J @ J.T + lambda_damp * np.eye(m))
```

---

## 3. SLAM

### Algorithm Selection Guide

| Scenario                         | Recommended Algorithm   | Library        |
| -------------------------------- | ----------------------- | -------------- |
| 2D indoor, LiDAR                 | Cartographer, GMapping  | ROS2 nav2      |
| 3D outdoor, LiDAR                | LIO-SAM, LOAM           | ROS2 pkg       |
| Visual, feature-rich environment | ORB-SLAM3               | C++ standalone |
| Visual-Inertial                  | VINS-Mono / VINS-Fusion | ROS2 wrapper   |
| Resource-constrained             | Hector SLAM (2D)        | ROS2 pkg       |

### Sensor Fusion for State Estimation

- Use **EKF** (Extended Kalman Filter) for mildly nonlinear systems.
- Use **UKF** (Unscented Kalman Filter) for strongly nonlinear systems.
- Use **factor graphs** (GTSAM / g2o) for full SLAM with loop closure.
- IMU pre-integration: always use proper manifold integration on `SO(3)` — never naive Euler.
- Covariance matrices: always positive-definite; add small diagonal `ε·I` if numerical
  issues arise.

---

## 4. Motion Planning

### Planner Selection

| Task                           | Algorithm        | Library            |
| ------------------------------ | ---------------- | ------------------ |
| Point-to-point, holonomic      | RRT*, PRM*       | OMPL (via MoveIt2) |
| Narrow passages                | KPIECE, BiEST    | OMPL               |
| Dynamic environments           | TEB, DWA         | nav2               |
| Manipulation with constraints  | CBiRRT, AtlasRRT | MoveIt2            |
| Whole-body / loco-manipulation | TRAC-IK + MPC    | Custom             |

### Path Post-Processing (Always Required)

1. **Shortcutting**: Remove redundant waypoints.
2. **Smoothing**: Apply `B-spline` or `polynomial` interpolation.
3. **Time parameterization**: Use `time_optimal_trajectory_generation` (Ruckig / Totp3).
4. **Collision re-check**: Validate smoothed path in dense collision checker.

---

## 5. Gazebo Simulation Standards

### World & Model Best Practices

- Use **SDF** (not URDF) for Gazebo worlds; generate URDF via XACRO for ROS2 integration.
- Set `<real_time_factor>1.0</real_time_factor>` for control validation; reduce for speed.
- Inertial parameters: compute from CAD (Meshlabs or Fusion360 export). Never use guesses.
- Friction / contact coefficients: validated against physical experiments before use in
  control design.
- Plugin selection: `ros_gz_sim` (Gazebo Harmonic) for ROS2 Humble+.

### Simulation-to-Reality (Sim2Real) Checklist

- [ ] Mass / inertia properties match physical hardware (within 5%).
- [ ] Motor model includes backlash, friction, and bandwidth limitations.
- [ ] Sensor noise models calibrated from real sensor datasheets.
- [ ] Communication latency modeled (use `gazebo_ros_control` with explicit delay plugin).
- [ ] Domain randomization configured if policy trained via RL.

---

## 6. Hardware Abstraction Layer (HAL)

### ros2_control Architecture

```
Hardware Interface (ros2_control)
    └── hardware_interface::SystemInterface  (your custom HAL)
          ├── on_init()       — parse URDF params, open comms
          ├── read()          — read joint states from hardware [rad, rad/s, N·m]
          └── write()         — send commands to hardware
Controller Manager
    ├── JointTrajectoryController  (position/velocity tracking)
    ├── DiffDriveController        (mobile bases)
    └── Custom controllers         (via controller_interface::ControllerInterface)
```

- **Never** call blocking I/O in `read()` / `write()` — use async comms with shared memory.
- **Always** implement state machine: UNCONFIGURED → INACTIVE → ACTIVE → FINALIZED.
- **Watchdog**: Hardware must enter safe state if `write()` not called within 2× control period.
