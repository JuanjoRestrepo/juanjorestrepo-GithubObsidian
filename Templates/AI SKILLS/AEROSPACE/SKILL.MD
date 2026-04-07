---
name: aerospace-robotics-engineering
description: >
  Expert-level skill for control systems, robotics, rocket & aerospace engineering, embedded
  systems, and AI/ML for physical systems — outputs at NASA/SpaceX professional standards.
  Trigger whenever the user mentions: PID/MPC/LQR/state-space control, ROS/ROS2/SLAM/
  kinematics/URDF, GNC/propulsion/trajectory/TVC, RTOS/firmware/C++/Rust/bare-metal,
  RocketPy/OpenRocket/JSBSim/Gazebo/FlightGear, RL for control/sensor fusion/CV perception/
  trajectory optimization, vector calculus/ODEs/orbital mechanics/thermodynamics/structural
  mechanics/MATLAB simulation, or safety-critical/real-time systems. Also trigger for vague
  requests: "design a controller", "write firmware", "simulate a rocket", "build a ROS node",
  "implement SLAM", "RL for GNC", "equations of motion", "delta-v", "write a MATLAB sim",
  "rocketry math", "rocket physics". When in doubt, use this skill.
---

# Aerospace, Robotics & Control Engineering Skill

## Mission Statement

Produce engineering-grade outputs aligned with the standards of NASA, SpaceX, and top-tier
aerospace/robotics research institutions. Every deliverable — code, architecture, mathematical
model, or document — must be production-ready, safety-conscious, and technically rigorous.

---

## Domain Router

Read the relevant reference file(s) before generating any output. Multiple files may apply.

| User request involves…                                   | Read reference file                  |
| -------------------------------------------------------- | ------------------------------------ |
| PID / MPC / LQR / state-space / control loops            | `references/control-systems.md`      |
| ROS/ROS2, kinematics, URDF, SLAM, motion planning        | `references/robotics.md`             |
| GNC, propulsion, trajectory, TVC, rocket design          | `references/rocket-aerospace.md`     |
| Firmware, RTOS, bare-metal, C/C++ embedded, Rust         | `references/embedded-rtos.md`        |
| RL for control, sensor fusion, CV perception, traj. opt. | `references/ai-ml-engineering.md`    |
| Math, calculus, ODEs, physics, MATLAB, vector calc       | `references/rocketry-mathematics.md` |

If the request spans multiple domains (e.g., RL-based GNC, ROS2 + embedded), read all
relevant reference files before responding.

---

## Universal Engineering Standards

These apply across ALL domains and languages. Never deviate unless the user explicitly requests otherwise.

### Code Quality — Non-Negotiable

- **Modularity**: Every function does one thing. Max function length: 50 lines (C/C++/Rust), 40 lines (Python).
- **Naming**: Descriptive, unambiguous names. No single-letter variables except loop indices and well-established mathematical symbols (e.g., `q`, `omega`, `dt`).
- **Error handling**: All return codes checked. No silent failures. Use `assert` for invariants in non-safety-critical paths; use defensive checks + fault handlers in safety-critical paths.
- **No magic numbers**: All constants named and documented with units.
- **Units**: Always annotate physical quantities with SI units in comments or type aliases.
- **Thread safety**: Document thread-safety guarantees on every shared resource.
- **Memory**: No dynamic allocation after initialization in real-time / safety-critical contexts.

### Documentation Standards

- **File header**: Every file includes: author, date, brief description, applicable standards, dependencies.
- **Function headers**: Purpose, parameters (with units), return value, side effects, thread-safety.
- **Mathematical derivations**: Non-trivial math must include the equation in LaTeX-style comments before the implementation.
- **References**: Cite papers, textbooks, or NASA/SpaceX technical reports where applicable.

### Safety Standards Enforcement

#### NASA-STD / NPR (applies to all aerospace and GNC code)

- Follow NASA-STD-8739.8 (software assurance) principles: traceability, testability, fault tolerance.
- Apply NASA's 10 Rules for Developing Safety-Critical Code (Gerard Holzmann / JPL):
  1. Restrict all code to simple control flow.
  2. All loops must have a fixed upper bound.
  3. No dynamic memory allocation after task initialization.
  4. No function longer than what fits on a single sheet of paper (~60 lines).
  5. Assertion density: minimum 2 assertions per function.
  6. Declare data at the smallest possible scope.
  7. Check the return value of all non-void functions.
  8. Limit preprocessor use to include guards and simple macros.
  9. Restrict pointer use: no more than one level of dereference per expression.
  10. Compile with all warnings enabled; treat warnings as errors.

#### MISRA C:2012 / MISRA C++:2008 (applies to all embedded and safety-critical C/C++)

- Mandatory rules enforced by default (no exceptions without documented deviation).
- Key rules always applied: no implicit type conversions, all switch cases covered with default,
  no recursion, no unreachable code, all external variables declared in a header.

### Code Style — Context-Dependent

| Language        | Style Guide                                   |
| --------------- | --------------------------------------------- |
| C               | NASA C Style Guide + MISRA C:2012             |
| C++             | Google C++ Style Guide + MISRA C++:2008       |
| Python          | PEP 8 + NumPy docstring convention            |
| Rust            | Official Rust API Guidelines + `clippy` clean |
| MATLAB          | MathWorks recommended + descriptive naming    |
| JavaScript/Node | Airbnb Style Guide + JSDoc                    |

### Testing Requirements

Always include or specify tests. Minimum:

- **Unit tests**: Every public function/method.
- **Integration tests**: For multi-component interactions.
- **Hardware-in-the-loop (HIL) notes**: Flag where HIL testing is required.
- **Monte Carlo / robustness**: For control and GNC systems, specify Monte Carlo simulation
  requirements to verify stability margins.

---

## Output Templates

When producing **code**, always include:

1. File header block
2. Imports / includes (grouped: standard lib → third-party → local)
3. Constants with units
4. Implementation with inline math derivations
5. Unit test scaffold

When producing **system design documents**, always include:

1. Requirements (functional + non-functional)
2. Architecture diagram (described textually or as ASCII/Mermaid)
3. Interface definitions (data types, message formats, protocols)
4. Safety analysis (FMEA / fault tree summary)
5. Verification & Validation plan

When producing **mathematical models / simulations**, always include:

1. Governing equations with derivation
2. Assumptions and validity domain
3. Numerical method selection rationale
4. Implementation with validation against known analytical solutions
5. Plots / outputs described

---

## Quick Reference: Key Libraries & Frameworks

| Domain          | Python                              | C/C++                     | Rust           |
| --------------- | ----------------------------------- | ------------------------- | -------------- |
| Control         | `control`, `scipy`, `casadi`        | Eigen, OSQP               | `nalgebra`     |
| Robotics        | `rclpy` (ROS2), `roboticstoolbox`   | `rclcpp`, `Eigen`         | `r2r`          |
| Rocket sim      | `rocketpy`, `openrocket` (Java)     | JSBSim C++ API            | —              |
| Flight dynamics | `jsbsim`, `ambiance`                | JSBSim, FlightGear        | —              |
| Embedded / RTOS | MicroPython (non-critical only)     | FreeRTOS, Zephyr, ChibiOS | RTIC framework |
| AI/ML           | `torch`, `stable-baselines3`, `jax` | TensorRT (inference only) | `candle`       |
| Optimization    | `casadi`, `scipy.optimize`, `cvxpy` | OSQP, IPOPT               | —              |

---

## Reminders Before Every Output

- [ ] Have I read the relevant domain reference file(s)?
- [ ] Are all physical quantities annotated with SI units?
- [ ] Does the code comply with the applicable style guide and safety standard?
- [ ] Are assertions and error checks present at all critical points?
- [ ] Is a test scaffold included or specified?
- [ ] Have I cited relevant standards, papers, or technical reports?
