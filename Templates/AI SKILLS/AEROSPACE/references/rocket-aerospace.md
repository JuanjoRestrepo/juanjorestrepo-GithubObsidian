# Rocket & Aerospace Engineering Reference

## Scope

GNC (Guidance, Navigation & Control), propulsion design, trajectory optimization,
aerodynamic modeling, structural analysis fundamentals, and simulation with
RocketPy, OpenRocket, JSBSim, and FlightGear.

---

## 1. GNC System Architecture

### Standard GNC Loop

```
[Guidance]                [Navigation]              [Control]
Trajectory reference  →   State estimation    →     Actuator commands
(where to go)             (where we are)            (how to get there)
     ↑                          ↑                         |
     └──────── Mission Computer ─────────────────────────┘
                                ↑
                         [Sensors: IMU, GPS, baro, star tracker]
```

### Navigation: IMU + GPS Fusion

- **INS mechanization**: Strapdown, quaternion-based attitude integration on `SO(3)`.
- **Attitude representation**: Use **unit quaternions** (not Euler angles) for all computations
  to avoid gimbal lock. Only convert to Euler for display/logging.
- **Frame conventions**: Follow **NED** (North-East-Down) for atmospheric flight;
  **ECI/ECEF** for orbital. Document frame clearly in every function.
- **GPS/INS fusion**: Loose coupling (EKF on position/velocity) for simplicity;
  tight coupling (EKF on pseudorange) for GPS-degraded environments.

```python
"""
Quaternion attitude integration — strapdown INS
================================================
Convention : q = [q0, q1, q2, q3] = [scalar, vector]
Reference  : Titterton & Weston, "Strapdown Inertial Navigation Technology", 2nd ed.
Units      : omega [rad/s], dt [s]
"""
import numpy as np

def quaternion_kinematics(q: np.ndarray, omega: np.ndarray, dt: float) -> np.ndarray:
    """Propagate quaternion attitude given body angular rate.

    Parameters
    ----------
    q : np.ndarray, shape (4,)
        Current quaternion [q0, q1, q2, q3], must be unit norm.
    omega : np.ndarray, shape (3,)
        Body angular rate vector [rad/s].
    dt : float
        Integration time step [s].

    Returns
    -------
    np.ndarray, shape (4,)
        Updated unit quaternion.
    """
    assert abs(np.linalg.norm(q) - 1.0) < 1e-6, "Input quaternion must be unit norm"
    assert dt > 0.0, "Time step must be positive [s]"

    # Omega matrix for quaternion kinematics: q_dot = 0.5 * Omega(omega) * q
    wx, wy, wz = omega
    Omega = np.array([
        [ 0,  -wx, -wy, -wz],
        [ wx,  0,   wz, -wy],
        [ wy, -wz,  0,   wx],
        [ wz,  wy, -wx,  0 ]
    ])  # shape (4,4)

    # Zero-order hold integration (exact for constant omega over dt)
    omega_norm = np.linalg.norm(omega)
    if omega_norm < 1e-10:  # Near-zero rotation
        q_new = q + 0.5 * dt * Omega @ q
    else:
        angle = omega_norm * dt
        q_new = (np.cos(angle / 2.0) * np.eye(4) +
                 np.sin(angle / 2.0) / omega_norm * Omega) @ q

    return q_new / np.linalg.norm(q_new)  # Re-normalize to prevent drift
```

---

## 2. Guidance: Trajectory Optimization

### Method Selection

| Scenario                          | Method                          | Tool           |
| --------------------------------- | ------------------------------- | -------------- |
| Ascent trajectory, 3-DOF          | Direct collocation / GPOPS      | CasADi + IPOPT |
| Powered descent (propulsive land) | Lossless convexification (SCvx) | CasADi / CVXPY |
| Orbital transfer                  | Indirect (Pontryagin), STK      | SciPy + custom |
| Atmospheric reentry               | Predictor-corrector guidance    | C++ / Python   |
| Real-time online replanning       | iLQR / DDP                      | Python (jax)   |

### Trajectory Design Constraints (always enforce)

- **Q∞ (dynamic pressure)**: Max structural limit [Pa] — never exceeded.
- **Angle of attack α**: Bounded to avoid aerodynamic instability.
- **Altitude rate**: Bounded during coast phase for thermal loads.
- **MECO / staging**: Defined by propellant mass fractions (Tsiolkovsky).
- **Landing accuracy**: CEP (Circular Error Probable) specified in requirements.

### Tsiolkovsky Rocket Equation

```python
# Δv = Isp · g0 · ln(m0 / mf)
# Always verify propellant budget with margin ≥ 10% (NASA margin policy)

G0_M_S2: float = 9.80665  # Standard gravity [m/s²] — ISO 80000

def delta_v(isp_s: float, m_initial_kg: float, m_final_kg: float) -> float:
    """Compute ideal delta-v from Tsiolkovsky equation.

    Parameters
    ----------
    isp_s : float
        Specific impulse [s].
    m_initial_kg : float
        Initial mass including propellant [kg].
    m_final_kg : float
        Final (dry) mass [kg].

    Returns
    -------
    float
        Ideal delta-v [m/s].
    """
    assert isp_s > 0.0, "Specific impulse must be positive [s]"
    assert m_initial_kg > m_final_kg > 0.0, "Mass values inconsistent [kg]"
    return isp_s * G0_M_S2 * np.log(m_initial_kg / m_final_kg)
```

---

## 3. Control: Attitude Control

### TVC (Thrust Vector Control)

- Model as input torque about CG: `τ = F_thrust × r_TVC_to_CG`
- Account for: gimbal angle limits (typ. ±8°), gimbal slew rate limits, actuator dynamics.
- Design with LQR or pole placement; include robustness to CG shift during propellant burn.
- **Always simulate with varying CG** as propellant depletes.

### Aerodynamic Stability

- **Static margin**: Distance between center of pressure (CP) and center of gravity (CG).
  Positive static margin (CG ahead of CP) → passive stability.
  Minimum: 1 caliber (1 × body diameter). Verify with OpenRocket / RASAero.
- **Fin sizing**: Use Barrowman equations for subsonic CP estimation.

---

## 4. Simulation Toolchains

### RocketPy (Python — Primary Simulation Tool)

```python
"""
RocketPy 6-DOF simulation setup
================================
Reference: RocketPy documentation + Ceotto et al. (2021)
Units    : SI throughout
"""
from rocketpy import Rocket, SolidMotor, Environment, Flight

# Environment: always use real atmospheric data when available
env = Environment(latitude=28.5721, longitude=-80.648, elevation=0)
env.set_date((2025, 6, 1, 12))           # Launch date/time (UTC)
env.set_atmospheric_model(type="Forecast", file="GFS")

# Motor: verify with static fire data or manufacturer cert sheet
motor = SolidMotor(
    thrust_source="motor_cert.eng",     # RASP .eng file or thrust curve array
    dry_mass=0.125,                      # [kg]
    dry_inertia=(0.002, 0.002, 0.0001),  # (Ixx, Iyy, Izz) [kg·m²]
    nozzle_radius=0.021,                 # [m]
    grain_number=4,
    grain_density=1815,                  # [kg/m³] — KNSB typical
    grain_outer_radius=0.021,            # [m]
    grain_initial_inner_radius=0.01,     # [m]
    grain_initial_height=0.12,           # [m]
    grains_center_of_mass_position=0.4,  # From nozzle [m]
    center_of_dry_mass_position=0.4,
    nozzle_position=0,
    burn_time=3.5,                       # [s]
    throat_radius=0.011,                 # [m]
)

rocket = Rocket(
    radius=0.0635,           # [m]
    mass=14.426,             # Dry mass [kg]
    inertia=(6.321, 6.321, 0.034),  # (Ixx, Iyy, Izz) [kg·m²]
    power_off_drag="drag_off.csv",
    power_on_drag="drag_on.csv",
    center_of_mass_without_motor=0.688,  # [m] from nozzle end
    coordinate_system_orientation="tail_to_nose",
)
rocket.add_motor(motor, position=-1.255)
```

### JSBSim (Flight Dynamics — Fixed/Rotary Wing)

- Use `jsbsim` Python bindings for simulation; C++ API for embedded/HIL.
- Aircraft model in XML: `FDMExec.LoadModel("path/to/aircraft")`.
- Always validate against published flight data or wind tunnel data.
- Set `<output>` nodes for all state variables needed for control design.
- Trim aircraft before running dynamic maneuver simulations.

### OpenRocket / RASAero II

- Use for **CP/CG analysis** and **altitude prediction** during design phase.
- Export simulation data to CSV for post-processing in Python.
- Run **Monte Carlo** (≥ 1000 samples) with parameter dispersions for landing zone prediction.

---

## 5. Propulsion Design

### Engine Performance Parameters

| Parameter        | Symbol | Unit | Notes                                                   |
| ---------------- | ------ | ---- | ------------------------------------------------------- |
| Specific impulse | Isp    | s    | Vacuum Isp for upper stages                             |
| Thrust           | F      | N    | Sea-level vs vacuum; account for nozzle exit pressure   |
| Mass flow rate   | ṁ      | kg/s | ṁ = F / (Isp · g0)                                      |
| Chamber pressure | Pc     | Pa   | Design for min 20% above nozzle exit pressure           |
| Expansion ratio  | ε      | —    | Optimize for altitude; Over-expansion → flow separation |
| C\* efficiency   | η_c\*  | —    | Target ≥ 0.95 for well-designed combustion chamber      |

### Nozzle Design (De Laval)

- Throat conditions: `M = 1`, max temperature and pressure.
- Exit: matched to ambient pressure for max thrust efficiency.
- Method of Characteristics (MOC) for supersonic contour design.
- Divergence efficiency: `η_div = (1 + cos α) / 2` where α is half-angle.

---

## 6. Safety & Compliance

### Range Safety

- Flight termination system (FTS): always modeled as an independent system.
- Keep-out zones: define no-fly volume with margin ≥ 3σ of trajectory dispersion.
- Propellant venting / safing procedures documented before every flight.

### NASA Margin Policy (NPR 7120.5)

| Parameter             | Minimum Margin              |
| --------------------- | --------------------------- |
| Structural (yield)    | Factor of Safety ≥ 1.25     |
| Structural (ultimate) | Factor of Safety ≥ 1.40     |
| Propellant (delta-v)  | ≥ 10% above required        |
| Power                 | ≥ 20% above peak demand     |
| Mass (launch vehicle) | ≥ 15% above estimated       |
| Thermal               | ≥ 10°C margin on all limits |

---

## 7. Documentation Standards for Aerospace

Every design document must include:

1. **Requirements Traceability Matrix (RTM)**: Each requirement → design item → test.
2. **Failure Mode and Effects Analysis (FMEA)**: Top-level system FMEA minimum.
3. **Interface Control Document (ICD)**: All mechanical, electrical, software interfaces.
4. **Design Verification Review (DVR)** checklist before proceeding to fabrication.
