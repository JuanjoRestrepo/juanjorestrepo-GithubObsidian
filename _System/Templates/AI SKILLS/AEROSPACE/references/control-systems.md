# Control Systems Reference

## Scope

Classical control (PID, lead-lag), modern control (LQR, LQE/Kalman, state feedback),
optimal control (MPC, iLQR), nonlinear control (feedback linearization, sliding mode,
Lyapunov-based), and robust control (H-infinity).

---

## 1. Problem Formulation Standards

Always begin by clearly defining:

- **Plant model**: Continuous-time or discrete-time state-space `ẋ = Ax + Bu, y = Cx + Du`
- **Operating point**: Linearization point if nonlinear plant
- **Performance specs**: Rise time, settling time, overshoot, steady-state error, bandwidth
- **Robustness specs**: Gain margin (≥ 6 dB), phase margin (≥ 45°), disk margin preferred
- **Constraints**: Actuator saturation, rate limits, state constraints

Document all assumptions: linearity, time-invariance, observability, controllability.
Always verify controllability (rank of `[B AB A²B … Aⁿ⁻¹B]`) and observability
(rank of `[C; CA; CA²; … CAⁿ⁻¹]`) before proceeding.

---

## 2. PID Control

### Design Workflow

1. Obtain or identify plant transfer function / step response.
2. Choose tuning method: Ziegler-Nichols (initial), IMC-based (preferred for robustness),
   or direct synthesis.
3. Implement with anti-windup (back-calculation preferred over clamping).
4. Add derivative filter: `N/(s + N)` where `N ≈ 5–20 × ω_c`.
5. Verify gain and phase margins on Bode plot.
6. Test with step, ramp, and disturbance inputs.

### Code Pattern (Python — `python-control`)

```python
"""
PID Controller with Anti-Windup
================================
Author      : [Name]
Date        : [YYYY-MM-DD]
Standard    : PEP 8, NumPy docstring
Description : Discrete-time PID with back-calculation anti-windup.
              Units: time [s], error [SI units of controlled variable].
"""

import numpy as np


# Controller gains — tune via IMC method
KP: float = 1.0   # Proportional gain [output_unit / error_unit]
KI: float = 0.1   # Integral gain     [output_unit / (error_unit · s)]
KD: float = 0.05  # Derivative gain   [output_unit · s / error_unit]
N_FILTER: float = 10.0   # Derivative filter coefficient [rad/s]
K_AWU: float = 0.5       # Anti-windup back-calculation gain [1/s]
U_MIN: float = -1.0      # Actuator lower limit [output_unit]
U_MAX: float = 1.0       # Actuator upper limit [output_unit]


class PIDController:
    """Discrete-time PID controller with anti-windup and derivative filter.

    Parameters
    ----------
    kp : float
        Proportional gain.
    ki : float
        Integral gain.
    kd : float
        Derivative gain.
    n_filter : float
        Derivative filter pole frequency [rad/s].
    k_awu : float
        Anti-windup back-calculation gain.
    u_min : float
        Lower actuator saturation limit.
    u_max : float
        Upper actuator saturation limit.
    dt : float
        Sample period [s].
    """

    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        n_filter: float,
        k_awu: float,
        u_min: float,
        u_max: float,
        dt: float,
    ) -> None:
        assert dt > 0.0, "Sample period must be positive [s]"
        assert u_min < u_max, "Actuator limits must satisfy u_min < u_max"
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.n = n_filter
        self.k_awu = k_awu
        self.u_min = u_min
        self.u_max = u_max
        self.dt = dt
        self._integral: float = 0.0
        self._deriv_state: float = 0.0  # filtered derivative state

    def reset(self) -> None:
        """Reset integrator and derivative state to zero."""
        self._integral = 0.0
        self._deriv_state = 0.0

    def update(self, error: float) -> float:
        """Compute control output for one time step.

        Parameters
        ----------
        error : float
            Setpoint minus measured value (e = r - y).

        Returns
        -------
        float
            Saturated control output u [output_unit].
        """
        assert np.isfinite(error), "Error signal must be finite"

        # Derivative (filtered): d/dt approximated via Euler + first-order filter
        # D(s) = KD · N·s / (s + N)  →  discrete Euler
        deriv_raw = (error - self._deriv_state) / self.dt
        self._deriv_state += self.dt * self.n * (error - self._deriv_state)
        deriv_out = self.kd * self.n * (error - self._deriv_state)

        # Unsaturated output
        u_unsat = self.kp * error + self._integral + deriv_out

        # Saturate
        u_sat = float(np.clip(u_unsat, self.u_min, self.u_max))

        # Anti-windup: back-calculation
        self._integral += self.dt * (
            self.ki * error + self.k_awu * (u_sat - u_unsat)
        )

        return u_sat
```

---

## 3. LQR / LQE (Linear Quadratic Regulator + Estimator)

### Design Workflow

1. Define continuous-time state-space `(A, B, C, D)`.
2. Select weighting matrices:
   - `Q`: state cost — diagonal, weights on state deviations (normalized by max acceptable deviation²).
   - `R`: input cost — diagonal, weights on control effort (normalized by max actuator²).
   - **Bryson's Rule**: `Q_ii = 1 / max_acceptable_state_i²`, `R_jj = 1 / max_acceptable_input_j²`
3. Solve discrete algebraic Riccati equation (DARE) for digital implementation.
4. Pair with Kalman filter (LQE) for output feedback: design `(Q_w, R_v)` noise covariances.
5. Verify closed-loop eigenvalue placement and step response.

### Stability Verification Checklist

- [ ] All closed-loop eigenvalues strictly in left-half plane (continuous) or inside unit circle (discrete).
- [ ] Gain margin ≥ 6 dB, phase margin ≥ 45°.
- [ ] Condition number of `A - BK` checked for numerical sensitivity.
- [ ] Kalman filter convergence verified (positive-definite `P` at steady state).

---

## 4. Model Predictive Control (MPC)

### Problem Formulation

```
minimize   Σ_{k=0}^{N-1} [ x_k' Q x_k + u_k' R u_k ] + x_N' P x_N
subject to  x_{k+1} = A x_k + B u_k          (dynamics)
            u_min ≤ u_k ≤ u_max               (input constraints)
            Δu_min ≤ u_k - u_{k-1} ≤ Δu_max  (rate constraints)
            x_min ≤ x_k ≤ x_max               (state constraints)
```

### Implementation Guidelines

- **Prediction horizon `N`**: Start with N = 10–20 samples; increase until performance plateaus.
- **Terminal cost `P`**: Use LQR solution for guaranteed stability (Mayne et al., 2000).
- **Solver**: Use `OSQP` (C/C++) or `casadi` + `IPOPT` (Python) for nonlinear MPC.
- **Warm starting**: Always warm-start with previous solution shifted by one step.
- **Computational budget**: Verify solver completes within `dt / 2` on target hardware.
- **Soft constraints**: Prefer soft constraints with large penalty over hard constraints
  to avoid infeasibility.

### Key Libraries

```python
# Linear MPC with CasADi
import casadi as ca
import numpy as np

# Nonlinear MPC template
opti = ca.Opti()
X = opti.variable(n_states, N + 1)
U = opti.variable(n_inputs, N)
# ... constraints and cost defined here
opti.solver('ipopt', {'ipopt.print_level': 0, 'print_time': 0})
```

---

## 5. Simulation & Validation Standards

### Python (`python-control` + `scipy`)

```python
import control
import numpy as np

# Always verify before designing controller:
def verify_system(A, B, C, D):
    """Verify controllability and observability."""
    sys = control.StateSpace(A, B, C, D)
    Co = control.ctrb(A, B)
    Ob = control.obsv(A, C)
    assert np.linalg.matrix_rank(Co) == A.shape[0], "System not controllable"
    assert np.linalg.matrix_rank(Ob) == A.shape[0], "System not observable"
    return sys
```

### MATLAB/Simulink Standards

- Use `lqr()`, `kalman()`, `dare()` from Control System Toolbox.
- All Simulink models: fixed-step solver, explicit sample times on all blocks.
- Model referencing for subsystem isolation.
- Use `sltest` for automated Simulink test cases.
- Export linearized models with `linearize()` for frequency-domain analysis.

### Required Validation Plots

1. **Step response**: Rise time, settling time, overshoot annotated.
2. **Bode plot**: Gain/phase margins annotated.
3. **Nyquist plot**: Stability confirmation.
4. **Pole-zero map**: Closed-loop pole locations.
5. **Time-domain simulation**: Against nonlinear model if plant was linearized.

---

## 6. Common Pitfalls — Checklist

- [ ] Discretization method chosen intentionally (ZOH preferred for sample-and-hold; Tustin/bilinear for frequency-domain fidelity).
- [ ] Sample rate ≥ 10× closed-loop bandwidth.
- [ ] Actuator dynamics included in plant model if bandwidth is comparable to control bandwidth.
- [ ] Sensor noise modeled and Kalman filter / observer designed accordingly.
- [ ] Wind-up prevention implemented for all integrators.
- [ ] Bumpless transfer implemented for mode switching.
- [ ] All gains stored in a configuration structure / header — never hardcoded inline.
