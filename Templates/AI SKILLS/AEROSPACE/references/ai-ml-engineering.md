# AI & ML Engineering for Physical Systems Reference

## Scope

Reinforcement learning for control and GNC, sensor fusion and state estimation,
computer vision for robot perception, and trajectory optimization using learning-based
and hybrid methods. Production-grade ML engineering standards throughout.

---

## 1. Reinforcement Learning for Control & GNC

### Problem Formulation Standard

Always define the MDP (Markov Decision Process) explicitly before implementation:

```
State space  (S): What does the agent observe? [units, bounds, noise model]
Action space (A): What can the agent command? [units, bounds, rate limits]
Reward (R)      : What behavior is incentivized? [shaped vs sparse, magnitude scale]
Episode horizon : Fixed-length or event-terminated?
Reset logic     : How does the environment reset safely?
```

### Algorithm Selection Guide

| System Type                       | Recommended Algorithm | Library             |
| --------------------------------- | --------------------- | ------------------- |
| Continuous action, model-free     | SAC, TD3              | `stable-baselines3` |
| Continuous action, model-based    | MBPO, Dreamer v3      | Custom / JAX        |
| Discrete action                   | PPO                   | `stable-baselines3` |
| Multi-agent (formation control)   | MADDPG, MAPPO         | `pettingzoo` + SB3  |
| GNC with known dynamics           | iLQR / DDP (not RL)   | CasADi / JAX        |
| GNC with unknown/complex dynamics | PPO with curriculum   | SB3 + Gymnasium     |

### Control-Specific RL Design Rules

- **Action space**: Use **normalized actions** `[-1, 1]` mapped to physical limits.
  Never expose raw actuator commands to the policy without normalization.
- **Observation space**: Normalize all observations to `[-1, 1]` or `[0, 1]`.
  Include: pose error, velocity error, actuator state (previous action). **Never** include
  absolute world position unless GPS-like accuracy is available at deployment.
- **Reward shaping**: Primary term (task success) + Secondary terms (energy, smoothness).
  Weight ratio: primary >> secondary. Log each term separately for debugging.
- **Sim2Real gap**: Apply domain randomization from day 1.
  Randomize: mass, inertia (±15%), friction (±30%), sensor noise (calibrated), latency.
- **Safety layer**: Always wrap RL policy with a safety filter (CBF — Control Barrier Function
  or hard clipping with fault detection). RL policies must **never** have unguarded access
  to actuators on real hardware.

### Training Infrastructure Template

```python
"""
RL Control Training Pipeline
==============================
Author    : [Name]
Date      : [YYYY-MM-DD]
Standard  : PEP 8, NumPy docstring
Framework : Stable-Baselines3 + Gymnasium + Weights & Biases
"""

import gymnasium as gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
import wandb
from wandb.integration.sb3 import WandbCallback


class RocketLandingEnv(gym.Env):
    """Powered descent RL environment.

    State  : [x, z, vx, vz, theta, omega, mass] — 7D
    Action : [throttle, gimbal_angle]            — 2D, normalized [-1, 1]
    Units  : SI (m, m/s, rad, rad/s, kg)
    Reward : see _compute_reward() docstring
    """

    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(self, render_mode: str | None = None) -> None:
        super().__init__()
        self.render_mode = render_mode

        # Observation space: normalized [-1, 1]
        self.observation_space = gym.spaces.Box(
            low=-1.0, high=1.0, shape=(7,), dtype=np.float32
        )
        # Action space: normalized [-1, 1] → mapped to [throttle, gimbal]
        self.action_space = gym.spaces.Box(
            low=-1.0, high=1.0, shape=(2,), dtype=np.float32
        )

        # Physical constants
        self.G0: float = 9.80665       # [m/s²]
        self.ISP: float = 225.0        # [s]
        self.THRUST_MAX: float = 3000.0  # [N]
        self.GIMBAL_MAX: float = 0.14   # [rad] (~8°)
        self.DT: float = 0.02          # [s] — 50 Hz sim

        self._state: np.ndarray = np.zeros(7, dtype=np.float64)
        self._step_count: int = 0

    def reset(
        self,
        seed: int | None = None,
        options: dict | None = None,
    ) -> tuple[np.ndarray, dict]:
        super().reset(seed=seed)
        # Domain randomization — applied every episode
        mass_nominal = 20.0  # [kg]
        self._state = np.array([
            self.np_random.uniform(-5.0, 5.0),   # x [m]
            self.np_random.uniform(80.0, 120.0),  # z [m]
            self.np_random.uniform(-2.0, 2.0),    # vx [m/s]
            self.np_random.uniform(-10.0, -5.0),  # vz [m/s]
            self.np_random.uniform(-0.1, 0.1),    # theta [rad]
            self.np_random.uniform(-0.05, 0.05),  # omega [rad/s]
            mass_nominal * self.np_random.uniform(0.85, 1.15),  # mass [kg]
        ], dtype=np.float64)
        self._step_count = 0
        return self._get_obs(), {}

    def _get_obs(self) -> np.ndarray:
        """Normalize state to [-1, 1] for policy input."""
        obs_scale = np.array([10.0, 120.0, 5.0, 15.0, 0.5, 1.0, 25.0])
        return np.clip(self._state / obs_scale, -1.0, 1.0).astype(np.float32)

    def _compute_reward(self, action: np.ndarray, terminated: bool) -> float:
        """Compute shaped reward.

        Returns
        -------
        float
            Reward components:
            - Landing accuracy: Gaussian on (x, vx, vz, theta) at touchdown.
            - Shaping: Potential-based (altitude × velocity alignment).
            - Fuel efficiency: Penalty on throttle magnitude.
            - Crash penalty: -100 if velocity at touchdown exceeds limits.
        """
        x, z, vx, vz, theta, omega, _ = self._state
        throttle = action[0]

        shaping = -(abs(x) * 0.1 + abs(vx) * 0.5 + abs(vz) * 0.2 + abs(theta) * 2.0)
        fuel_penalty = -0.01 * abs(throttle)
        reward = shaping + fuel_penalty

        if terminated:
            landing_success = (abs(vz) < 2.0 and abs(vx) < 1.0 and
                               abs(theta) < 0.1 and abs(x) < 1.0)
            reward += 100.0 if landing_success else -100.0

        return float(reward)

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool, dict]:
        raise NotImplementedError("Implement dynamics integration here")

    def check(self) -> None:
        """Run Gymnasium environment checker — call before training."""
        check_env(self, warn=True)
```

---

## 2. Sensor Fusion & State Estimation

### EKF Implementation Standard

```python
"""
Extended Kalman Filter — Generic Template
==========================================
Reference  : Thrun, Burgard, Fox — "Probabilistic Robotics" (2005)
             Bar-Shalom et al. — "Estimation with Applications to
             Tracking and Navigation" (2001)
Units      : All in SI
"""
import numpy as np
from dataclasses import dataclass, field


@dataclass
class EKFState:
    """EKF state container.

    Attributes
    ----------
    x : np.ndarray
        State mean vector [n,].
    P : np.ndarray
        State covariance matrix [n, n]. Must remain positive-definite.
    """
    x: np.ndarray
    P: np.ndarray

    def __post_init__(self) -> None:
        assert self.x.ndim == 1, "State must be 1D"
        n = self.x.shape[0]
        assert self.P.shape == (n, n), "Covariance shape mismatch"
        # Verify positive-definiteness
        eigenvalues = np.linalg.eigvalsh(self.P)
        assert np.all(eigenvalues > 0), "Covariance must be positive-definite"


class ExtendedKalmanFilter:
    """Generic EKF with Joseph-form covariance update for numerical stability.

    Parameters
    ----------
    f : callable
        State transition function f(x, u, dt) → x_next.
    h : callable
        Measurement function h(x) → z_pred.
    F_jacobian : callable
        Jacobian of f w.r.t. x: F(x, u, dt) → [n×n].
    H_jacobian : callable
        Jacobian of h w.r.t. x: H(x) → [m×n].
    Q : np.ndarray
        Process noise covariance [n×n].
    R : np.ndarray
        Measurement noise covariance [m×m].
    """

    def __init__(self, f, h, F_jacobian, H_jacobian, Q, R):
        self.f = f
        self.h = h
        self.F_jac = F_jacobian
        self.H_jac = H_jacobian
        self.Q = Q
        self.R = R

    def predict(self, state: EKFState, u: np.ndarray, dt: float) -> EKFState:
        """EKF predict step."""
        F = self.F_jac(state.x, u, dt)
        x_pred = self.f(state.x, u, dt)
        P_pred = F @ state.P @ F.T + self.Q
        return EKFState(x=x_pred, P=P_pred)

    def update(self, state: EKFState, z: np.ndarray) -> EKFState:
        """EKF update step with Joseph-form for numerical stability."""
        H = self.H_jac(state.x)
        z_pred = self.h(state.x)
        S = H @ state.P @ H.T + self.R
        K = state.P @ H.T @ np.linalg.inv(S)
        x_upd = state.x + K @ (z - z_pred)

        # Joseph form: numerically more stable than P = (I - KH)P
        n = state.x.shape[0]
        I_KH = np.eye(n) - K @ H
        P_upd = I_KH @ state.P @ I_KH.T + K @ self.R @ K.T

        # Symmetrize to prevent drift
        P_upd = 0.5 * (P_upd + P_upd.T)
        return EKFState(x=x_upd, P=P_upd)
```

### IMU Preintegration on SO(3)

- Never integrate angular velocity with naive Euler integration on Euler angles.
- Use **rotation matrix** or **quaternion** integration on the manifold.
- For factor-graph SLAM: implement **IMU preintegration** (Forster et al., 2017 — TRO).
- Library: GTSAM (`PreintegratedImuMeasurements`) for full IMU preintegration.

---

## 3. Computer Vision for Robot Perception

### Perception Pipeline Architecture

```
[Camera / LiDAR / Depth]
        ↓
[Preprocessing: undistortion, filtering]
        ↓
[Feature extraction / Detection]     ← YOLO, SAM, ORB, SIFT
        ↓
[Pose estimation / 3D reconstruction] ← PnP, ICP, NeRF
        ↓
[State estimation fusion]            ← EKF / Factor graph
        ↓
[Planning / Control input]
```

### Engineering Standards for Vision Nodes

- **Camera calibration**: Always intrinsic + extrinsic. Use `camera_calibration` (ROS2).
  Reproject error < 0.5 px before any use in state estimation.
- **Latency budget**: Vision pipeline latency must be accounted for in control loop design.
  Compensate with forward prediction using IMU.
- **Inference on edge**: Use TensorRT (NVIDIA) or ONNX Runtime for deployment.
  Profile on target hardware — never assume laptop performance translates.
- **Confidence thresholds**: Every detection includes confidence score.
  Define minimum threshold and fallback behavior explicitly.

### Depth Estimation / 3D Reconstruction

```python
import open3d as o3d
import numpy as np

def filter_pointcloud(pcd: o3d.geometry.PointCloud,
                      voxel_size: float = 0.05) -> o3d.geometry.PointCloud:
    """Downsample and remove outliers from point cloud.

    Parameters
    ----------
    pcd : o3d.geometry.PointCloud
        Input point cloud.
    voxel_size : float
        Voxel grid size for downsampling [m].

    Returns
    -------
    o3d.geometry.PointCloud
        Filtered point cloud.
    """
    assert voxel_size > 0.0, "Voxel size must be positive [m]"
    # Voxel downsampling
    pcd_down = pcd.voxel_down_sample(voxel_size)
    # Statistical outlier removal
    pcd_clean, _ = pcd_down.remove_statistical_outlier(
        nb_neighbors=20, std_ratio=2.0
    )
    return pcd_clean
```

---

## 4. Trajectory Optimization (Learning-Based & Hybrid)

### Method Selection

| Scenario                              | Method                          |
| ------------------------------------- | ------------------------------- |
| Smooth trajectory, known dynamics     | Direct collocation (CasADi)     |
| Real-time replanning                  | iLQR / DDP (JAX — JIT compiled) |
| Learning the cost function            | Inverse RL (MaxEnt IRL)         |
| Learning feasible trajectory manifold | Diffusion Policy / FlowMatching |
| Hybrid: warm-start optimizer with ML  | Neural network + CasADi polish  |

### iLQR in JAX (JIT-Compiled, Real-Time Capable)

```python
import jax
import jax.numpy as jnp
from functools import partial

@partial(jax.jit, static_argnums=(0,))
def ilqr_backward_pass(dynamics_fn, cost_fn, xs, us, horizon):
    """iLQR backward pass — JIT compiled for real-time execution.

    Reference: Li & Todorov (2004), "Iterative Linear Quadratic Regulator Design
               for Nonlinear Biological Movement Systems."
    """
    # Linearize dynamics and quadraticize cost along nominal trajectory
    # Returns: Ks (feedback gains), ks (feedforward), dV (value improvement)
    raise NotImplementedError("Implement per system dynamics")
```

---

## 5. ML Engineering Standards

### Model Development Lifecycle

1. **Requirement**: Define performance metric and acceptance criteria before training.
2. **Data**: Document source, preprocessing pipeline, train/val/test split. Version with DVC.
3. **Baseline**: Always establish a simple baseline (PID, LQR) before training RL/ML.
4. **Training**: Log all hyperparameters and metrics (W&B or MLflow). Reproducible seeds.
5. **Evaluation**: Evaluate on held-out sim conditions AND real hardware (or HIL).
6. **Safety validation**: Adversarial testing — find failure modes before deployment.
7. **Deployment**: Versioned model artifact, reproducible inference environment (Docker/ONNX).

### Forbidden Practices

- ❌ Training on test data (even inadvertently via repeated evaluation).
- ❌ Deploying a model without measuring inference latency on target hardware.
- ❌ Using floating-point models on MCUs without quantization analysis.
- ❌ Undocumented hyperparameter tuning — all trials logged.
- ❌ No safety layer between RL policy and physical actuators.

### Sim2Real Validation Protocol

1. Train in simulation with domain randomization.
2. Test on 100 held-out sim scenarios (unseen randomization seeds).
3. HIL testing with real avionics / motor controllers (plant in simulation).
4. Benchtop hardware testing with constrained motion.
5. Incremental field testing with abort thresholds and safety observer.
