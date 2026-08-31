# Rocketry Mathematics & Applied Physics Reference

## Scope

Rigorous mathematical and physical foundations for university-level rocket engineering:
vector calculus, ODEs/PDEs, rigid body dynamics, orbital mechanics, aerothermodynamics,
structural mechanics, numerical methods, and MATLAB best practices. All consistent with
NASA JPL and SpaceX engineering standards.

---

## 0. Mathematical Constants & Numerical Precision

### The NASA Pi Standard (JPL-Official)

For all rocketry and aerospace calculations, use **exactly 15 significant decimal digits**
of π. This is the official JPL standard for their highest-accuracy interplanetary navigation.

```matlab
% MATLAB — define all physical constants in a dedicated constants file
% constants.m  —  Source: NIST CODATA 2018, NASA JPL standard

PI          = 3.141592653589793;   % π — JPL standard (15 sig. decimals)
G0          = 9.80665;             % Standard gravity [m/s²]  — ISO 80000-3
G_GRAV      = 6.67430e-11;        % Gravitational constant [N·m²/kg²]
R_EARTH     = 6.3781e6;           % Earth mean radius [m]  — WGS84
M_EARTH     = 5.9722e24;          % Earth mass [kg]
MU_EARTH    = 3.986004418e14;     % Earth gravitational parameter [m³/s²]
R_GAS       = 8.314462618;        % Universal gas constant [J/(mol·K)]
ATM_SEA     = 101325.0;           % Standard sea-level pressure [Pa]
GAMMA_AIR   = 1.4;                % Ratio of specific heats, air [-]
```

**Best Practice Rule**: Never type π inline as `3.14` or `3.14159`.
Always use the named constant `PI` or `pi` (MATLAB built-in: `pi` = `3.141592653589793`).
Using `pi` in MATLAB directly already satisfies the JPL standard — it is stored as an
IEEE 754 double, which carries 15–17 significant decimal digits.

---

## 1. Vector Calculus in Rocketry

### 1.1 Coordinate Frames — Always Define Before Any Vector Operation

| Frame | Name                         | Usage                                  |
| ----- | ---------------------------- | -------------------------------------- |
| ECI   | Earth-Centered Inertial      | Orbital mechanics, inertial navigation |
| ECEF  | Earth-Centered Earth-Fixed   | Ground track, GPS                      |
| NED   | North-East-Down              | Atmospheric flight, local navigation   |
| Body  | Body-fixed (nose-tail)       | Forces, moments, control               |
| Wind  | Aligned with velocity vector | Aerodynamic angle of attack, beta      |

**Transformation Convention**: rotation matrices `R ∈ SO(3)`, applied as `v_B = R_B_from_N · v_N`.
Document frame of each vector in every function header.

### 1.2 Gradient, Divergence, and Curl

Applied in rocketry for:

- **Pressure field**: `∇P` drives nozzle flow and external aerodynamic loads.
- **Temperature field**: `∇T` governs heat flux into structure (`q'' = -k∇T`).
- **Velocity field (CFD)**: `∇·V = 0` (incompressible), `∇×V = ω` (vorticity).

```matlab
% Numerical gradient of pressure field over altitude h [m]
% P: pressure array [Pa], h: altitude array [m]
dP_dh = gradient(P, h);   % dP/dh [Pa/m] — MATLAB gradient() uses central differences
```

### 1.3 Line Integrals — Work and Impulse

Total impulse (integral of thrust over burn time):

```
            t_burn
I_total = ∫       F(t) dt     [N·s]
            0
```

```matlab
% Numerical integration of thrust curve — Simpson's rule or MATLAB integral()
I_total = trapz(t_burn, F_thrust);   % [N·s]  — trapezoidal rule
% For smooth curves, prefer:
I_total_smooth = integral(@(t) thrust_interp(t), t0, t_burn_end);
```

### 1.4 Surface and Volume Integrals — Pressure Loads & Mass Properties

Aerodynamic force from distributed surface pressure:

```
F_aero = ∬_S  (p - p_∞) n̂ dA      [N]
```

Center of mass from variable-density structure:

```
r_CG = (1/m_total) · ∭_V ρ(r) · r dV
```

```matlab
% Center of mass along rocket axis — discrete segments
m_segments = [m1, m2, m3, ...];      % [kg]
x_segments = [x1, x2, x3, ...];      % Axial position of each segment CG [m]
x_CG = dot(m_segments, x_segments) / sum(m_segments);   % [m]
```

---

## 2. Differential Equations of Flight

### 2.1 Equations of Motion — 6-DOF (Six Degrees of Freedom)

The complete rigid-body equations of motion in the body frame.

**Translational dynamics** (Newton's 2nd law, body frame):

```
m · (V̇_B + ω × V_B) = F_thrust + F_aero + R_B_from_N · F_gravity
```

**Rotational dynamics** (Euler's equations):

```
I · ω̇ + ω × (I · ω) = M_aero + M_TVC + M_RCS
```

where:

- `V_B` = velocity in body frame [m/s]
- `ω` = angular velocity vector [rad/s]
- `I` = inertia tensor [kg·m²] — updates as propellant burns
- `F_thrust`, `F_aero` = thrust and aerodynamic force vectors [N]
- `M_*` = applied moment vectors [N·m]

**Kinematic equations** (quaternion attitude propagation — see rocket-aerospace.md):

```
q̇ = (1/2) · Ω(ω) · q
ṙ_N = R_N_from_B · V_B
```

**Mass depletion** (Tsiolkovsky + burn model):

```
ṁ = -F_thrust / (Isp · g0)     [kg/s]
```

### 2.2 MATLAB ODE Solver Best Practices

```matlab
function dxdt = rocket_eom(t, x, params)
% rocket_eom — 6-DOF equations of motion for ascent phase.
%
% Inputs:
%   t      : time [s]
%   x      : state vector [pos(3); vel(3); quat(4); omega(3); mass(1)] — 14x1
%   params : struct with motor, aero, and geometry parameters
%
% Outputs:
%   dxdt   : state derivative [14x1]
%
% Units   : SI throughout (m, m/s, rad, rad/s, kg)
% Frame   : position/velocity in NED; attitude as quaternion (body from NED)

    % Unpack state — named indices prevent off-by-one errors
    r_NED  = x(1:3);    % Position [m]
    v_NED  = x(4:6);    % Velocity, NED frame [m/s]
    q      = x(7:10);   % Quaternion [q0 q1 q2 q3], body from NED
    omega  = x(11:13);  % Angular velocity, body frame [rad/s]
    mass   = x(14);     % Current mass [kg]

    assert(mass > params.dry_mass, 'Propellant depleted — terminate ODE');
    assert(abs(norm(q) - 1.0) < 1e-4, 'Quaternion norm drift detected');

    % Rotation matrix: body → NED
    R_NED_from_B = quat2rotm(q');   % MATLAB Aerospace Toolbox

    % Altitude from NED position
    altitude = -r_NED(3);           % NED: down is positive, altitude is -z [m]

    % Atmospheric model
    [rho, P_atm, T_atm, a_sound] = atmos_standard(altitude);

    % Aerodynamic forces and moments (body frame)
    v_body = R_NED_from_B' * v_NED;
    [F_aero_B, M_aero_B] = aero_model(v_body, rho, params);

    % Thrust (body frame, along nose direction = +x_B)
    F_thrust_mag = motor_thrust(t, params.motor);
    F_thrust_B   = [F_thrust_mag; 0; 0];    % [N]
    mdot         = -F_thrust_mag / (params.motor.Isp * params.G0);  % [kg/s]

    % TVC gimbal moment
    M_TVC_B = tvc_moment(t, F_thrust_mag, params);

    % Gravity in body frame
    g_NED = [0; 0; params.G0];   % NED: gravity along +z_NED [m/s²]
    F_grav_B = R_NED_from_B' * (mass * g_NED);

    % --- Equations of motion ---
    % Translation (NED frame)
    accel_NED = (1/mass) * (R_NED_from_B * (F_thrust_B + F_aero_B) + mass * g_NED);

    % Rotation (body frame) — Euler's equations
    I_body   = inertia_tensor(mass, params);   % Updates with mass depletion
    I_inv    = inv(I_body);
    alpha    = I_inv * (M_aero_B + M_TVC_B - cross(omega, I_body * omega));

    % Quaternion kinematics
    Omega_mat = [ 0,       -omega(1), -omega(2), -omega(3);
                  omega(1),  0,        omega(3), -omega(2);
                  omega(2), -omega(3),  0,        omega(1);
                  omega(3),  omega(2), -omega(1),  0      ];
    qdot = 0.5 * Omega_mat * q;

    % Assemble state derivative
    dxdt = [v_NED; accel_NED; qdot; alpha; mdot];
end
```

```matlab
% --- Integration call — ODE45 with event detection ---
options = odeset( ...
    'RelTol',   1e-8,  ...    % Tight tolerance for trajectory accuracy
    'AbsTol',   1e-10, ...
    'Events',   @apogee_event, ...    % Terminate at apogee
    'MaxStep',  0.01   ...    % Max step 10 ms — captures fast dynamics
);

[t_out, x_out, te, xe, ie] = ode45(@(t,x) rocket_eom(t, x, params), ...
                                    [0, t_max], x0, options);
```

**ODE Solver Selection Guide:**
| Scenario | Solver | Reason |
|----------------------------------|--------------|--------------------------------|
| Smooth trajectory, non-stiff | `ode45` | Default — Dormand-Prince RK4/5 |
| Stiff (combustion, fast aero) | `ode15s` | Gear's BDF method |
| High accuracy, smooth | `ode113` | Adams-Bashforth-Moulton |
| Real-time / fixed-step | Custom RK4 | Deterministic step size |

---

## 3. Orbital Mechanics

### 3.1 Two-Body Problem

```
r̈ = -μ/|r|³ · r      (vector form, ECI frame)

μ_Earth = 3.986004418 × 10¹⁴  m³/s²
```

### 3.2 Vis-Viva Equation

```
v² = μ (2/r - 1/a)

where:
  v  = orbital speed [m/s]
  r  = distance from center of Earth [m]
  a  = semi-major axis [m]
  μ  = gravitational parameter [m³/s²]
```

```matlab
function v = vis_viva(mu, r, a)
% vis_viva — compute orbital speed from vis-viva equation.
%
% Parameters:
%   mu : gravitational parameter [m³/s²]
%   r  : current radius from body center [m]
%   a  : semi-major axis [m] (Inf for escape trajectory)
%
% Returns:
%   v  : orbital speed [m/s]

    assert(r > 0 && mu > 0, 'Physical inputs required');
    if isinf(a)
        v = sqrt(2 * mu / r);   % Escape velocity
    else
        assert(a > 0, 'Semi-major axis must be positive for bound orbit [m]');
        v = sqrt(mu * (2/r - 1/a));
    end
end
```

### 3.3 Hohmann Transfer

```matlab
function [dv1, dv2, t_transfer] = hohmann_transfer(mu, r1, r2)
% Hohmann transfer delta-v budget.
% r1, r2 : initial and final circular orbit radii [m]
% dv1, dv2 : delta-v at each burn [m/s]
% t_transfer : transfer time [s]

    a_transfer = (r1 + r2) / 2;
    v1_circ    = sqrt(mu / r1);
    v2_circ    = sqrt(mu / r2);
    v1_trans   = sqrt(mu * (2/r1 - 1/a_transfer));
    v2_trans   = sqrt(mu * (2/r2 - 1/a_transfer));

    dv1        = abs(v1_trans - v1_circ);   % [m/s]
    dv2        = abs(v2_circ  - v2_trans);  % [m/s]
    t_transfer = PI * sqrt(a_transfer^3 / mu);   % [s]  — half orbital period
end
```

---

## 4. Atmospheric Physics

### 4.1 International Standard Atmosphere (ISA) — MATLAB Implementation

```matlab
function [rho, P, T, a] = atmos_standard(h)
% atmos_standard — ISA model, valid 0–86 km.
%
% Input : h   altitude [m]  (geometric, above MSL)
% Output: rho density [kg/m³], P pressure [Pa], T temperature [K],
%         a   speed of sound [m/s]
%
% Reference: ISO 2533:1975, ICAO Doc 7488

    % Constants
    R    = 287.0528;    % Specific gas constant, dry air [J/(kg·K)]
    g0   = 9.80665;     % Standard gravity [m/s²]
    gam  = 1.4;         % Ratio of specific heats [-]

    % ISA layer table: [base_alt [m], base_temp [K], lapse_rate [K/m]]
    layers = [
          0,   288.15, -6.5e-3;
      11000,   216.65,  0.0;
      20000,   216.65,  1.0e-3;
      32000,   228.65,  2.8e-3;
      47000,   270.65,  0.0;
      51000,   270.65, -2.8e-3;
      71000,   214.65, -2.0e-3;
    ];

    % Clip to model validity range
    h = max(0, min(h, 86000));

    % Find layer
    layer_idx = find(h >= layers(:,1), 1, 'last');
    h0 = layers(layer_idx, 1);
    T0 = layers(layer_idx, 2);
    L  = layers(layer_idx, 3);   % Lapse rate [K/m]

    % Base conditions at layer bottom
    [~, P0, ~, ~] = atmos_base_conditions(layer_idx, layers, R, g0);

    % Temperature
    T = T0 + L * (h - h0);   % [K]

    % Pressure
    if abs(L) < 1e-10   % Isothermal layer
        P = P0 * exp(-g0 * (h - h0) / (R * T0));
    else
        P = P0 * (T / T0)^(-g0 / (L * R));
    end

    % Density and speed of sound
    rho = P / (R * T);              % [kg/m³]
    a   = sqrt(gam * R * T);        % [m/s]
end
```

### 4.2 Dynamic Pressure and Mach Number

```matlab
% q_dyn : dynamic pressure [Pa]
% M     : Mach number [-]
% Always compute before any aerodynamic coefficient lookup

function [q_dyn, mach] = aero_conditions(v_mag, rho, a_sound)
    assert(rho > 0 && a_sound > 0, 'Atmospheric properties must be positive');
    q_dyn = 0.5 * rho * v_mag^2;   % [Pa]
    mach  = v_mag / a_sound;        % [-]
end
```

---

## 5. Thermodynamics & Propulsion Physics

### 5.1 Isentropic Nozzle Flow Relations

For a De Laval nozzle (critical at throat, M = 1):

```
T0/T = 1 + (γ-1)/2 · M²         (stagnation temperature ratio)
P0/P = (1 + (γ-1)/2 · M²)^(γ/(γ-1))  (stagnation pressure ratio)
A/A* = (1/M) · [(2/(γ+1)) · (1 + (γ-1)/2 · M²)]^((γ+1)/(2(γ-1)))  (area ratio)
```

```matlab
function [T_ratio, P_ratio, A_ratio] = isentropic_relations(M, gamma)
% isentropic_relations — stagnation and area ratios for isentropic nozzle flow.
%
% M     : Mach number [-], M > 0
% gamma : ratio of specific heats [-], typically 1.2–1.4 for rocket exhaust
%
% Returns ratios: T0/T, P0/P, A/A*

    assert(M > 0,         'Mach number must be positive');
    assert(gamma > 1.0,   'Gamma must exceed 1.0 for a real gas');

    base       = 1 + (gamma - 1)/2 * M^2;
    T_ratio    = base;
    P_ratio    = base^(gamma / (gamma - 1));
    A_ratio    = (1/M) * ((2/(gamma+1)) * base)^((gamma+1) / (2*(gamma-1)));
end
```

### 5.2 Exhaust Velocity and Specific Impulse

```
c* = sqrt(R_gas · T_c / M_mol · (2/(γ+1))^((γ+1)/(γ-1))) / sqrt(γ)
v_e = sqrt(2γ/(γ-1) · R_gas·T_c/M_mol · [1 - (P_e/P_c)^((γ-1)/γ)])
Isp = v_e / g0                           [s]
F   = ṁ · v_e + (P_e - P_∞) · A_e       [N]
```

---

## 6. Structural Mechanics for Rockets

### 6.1 Buckling and Axial Loads

Critical buckling load for a thin cylindrical shell under axial compression:

```
N_cr = 0.605 · E · t² / R       [N/m]  (classical formula — apply KDF ≈ 0.3–0.7)
```

where E = Young's modulus [Pa], t = wall thickness [m], R = radius [m].
**Knockdown factor (KDF)**: NASA SP-8007 specifies empirical knockdown factors
due to geometric imperfections. Always apply KDF before comparing to limit load.

### 6.2 Bending Moment During Max-Q

```
M_bending = q_dyn · C_N_alpha · A_ref · L_ref · sin(alpha)   [N·m]
```

Max-Q (maximum dynamic pressure) is the critical structural loading point.
Always verify structural margins at max-Q using:

- **Limit load**: Maximum expected load.
- **Ultimate load**: Limit load × 1.40 (NASA Factor of Safety — NPR 7120.5).

---

## 7. Numerical Methods Best Practices

### 7.1 Integration Methods

| Method                    | Order | Use Case                                  |
| ------------------------- | ----- | ----------------------------------------- |
| Euler (forward)           | 1     | Never for production — prototype only     |
| RK4 (classic)             | 4     | Fixed-step embedded control, HIL          |
| RK45 (Dormand-Prince)     | 4/5   | Variable-step simulation (MATLAB `ode45`) |
| Adams-Bashforth           | var   | Long integrations, smooth systems         |
| Verlet                    | 2     | Orbital mechanics — energy-conserving     |
| Leapfrog / Störmer-Verlet | 2     | Symplectic — orbital mechanics preferred  |

### 7.2 Numerical Differentiation

```matlab
% Always prefer central differences over forward differences (O(h²) vs O(h))
% df/dx ≈ [f(x+h) - f(x-h)] / (2h)   — central, error O(h²)

function df = central_diff(f, x, h)
    assert(h > 0, 'Step size must be positive');
    df = (f(x + h) - f(x - h)) / (2 * h);
end

% Optimal step size: h ≈ sqrt(eps_machine) * |x|  ≈ 1.5e-8 for doubles
h_opt = sqrt(eps) * max(abs(x), 1.0);
```

### 7.3 Root Finding — Event Detection in Flight

```matlab
% Apogee detection: vertical velocity = 0
function [value, isterminal, direction] = apogee_event(t, x)
    v_NED  = x(4:6);
    value      = v_NED(3);   % NED down-velocity: zero at apogee
    isterminal = 1;          % Stop integration
    direction  = 1;          % Zero crossing: negative → positive (v_z in NED)
end
```

---

## 8. MATLAB Engineering Best Practices

### 8.1 File and Code Organization

```
rocket_sim/
├── main_simulation.m        % Entry point — no logic, only setup + calls
├── constants.m              % All physical constants (run once, workspace)
├── config/
│   └── mission_params.m     % Mission-specific parameters (struct)
├── dynamics/
│   ├── rocket_eom.m
│   ├── inertia_tensor.m
│   └── motor_thrust.m
├── aerodynamics/
│   ├── aero_model.m
│   └── drag_coefficient.m
├── atmosphere/
│   └── atmos_standard.m
├── guidance/
│   └── trajectory_optimizer.m
├── analysis/
│   ├── plot_trajectory.m
│   └── monte_carlo.m
└── tests/
    └── test_*.m             % Unit tests via matlab.unittest
```

### 8.2 Mandatory MATLAB Conventions

```matlab
% -------------------------------------------------------------------------
% HEADER — Required on every function file
% -------------------------------------------------------------------------
function result = compute_delta_v(isp, m_initial, m_final)
% compute_delta_v  Ideal delta-v via Tsiolkovsky equation.
%
%   result = compute_delta_v(ISP, M_INITIAL, M_FINAL)
%
%   Inputs:
%     isp       - specific impulse [s]
%     m_initial - initial total mass including propellant [kg]
%     m_final   - final (dry) mass [kg]
%
%   Outputs:
%     result    - ideal delta-v [m/s]
%
%   Assumptions:
%     Vacuum delta-v (no gravity or drag losses)
%
%   Reference:
%     Tsiolkovsky, K.E. (1903). "The Exploration of Cosmic Space by
%     Means of Reaction Devices."
%
%   Example:
%     dv = compute_delta_v(300, 10.0, 3.0);   % → ~3,354 m/s
%
%   See also: ROCKET_EOM, MOTOR_THRUST

    % Input validation — always first block
    validateattributes(isp,       {'numeric'}, {'scalar','positive'}, ...
                       mfilename, 'isp',       1);
    validateattributes(m_initial, {'numeric'}, {'scalar','positive'}, ...
                       mfilename, 'm_initial', 2);
    validateattributes(m_final,   {'numeric'}, {'scalar','positive'}, ...
                       mfilename, 'm_final',   3);
    assert(m_initial > m_final, ...
        'compute_delta_v: m_initial must exceed m_final (propellant mass > 0)');

    % Computation
    G0     = 9.80665;   % Standard gravity [m/s²]
    result = isp * G0 * log(m_initial / m_final);   % [m/s]
end
```

### 8.3 Struct-Based Parameter Passing (Never Global Variables)

```matlab
% Build parameter struct before simulation — single source of truth
params.motor.Isp         = 220.0;         % [s]
params.motor.thrust_max  = 2500.0;        % [N]
params.motor.burn_time   = 4.2;           % [s]
params.motor.dry_mass    = 0.85;          % [kg]

params.geometry.diameter = 0.127;         % Body diameter [m]
params.geometry.length   = 2.4;           % Total length [m]
params.geometry.A_ref    = pi/4 * params.geometry.diameter^2;  % [m²]

params.mass.dry          = 12.5;          % Dry mass [kg]
params.mass.propellant   = 4.2;           % Propellant mass [kg]
params.G0                = 9.80665;       % [m/s²]
```

### 8.4 Plotting Standards

```matlab
function plot_trajectory(t, x, mission_name)
% plot_trajectory — standardized trajectory visualization.

    figure('Name', sprintf('%s — Trajectory', mission_name), ...
           'NumberTitle', 'off', 'Units', 'normalized', ...
           'Position', [0.05, 0.05, 0.9, 0.85]);

    altitude_m = -x(:,3);   % NED: altitude = -z_NED [m]
    altitude_km = altitude_m / 1e3;

    subplot(2, 3, 1);
    plot(t, altitude_km, 'b-', 'LineWidth', 1.5);
    xlabel('Time [s]');  ylabel('Altitude [km]');
    title('Altitude vs Time');  grid on;

    subplot(2, 3, 2);
    v_mag = vecnorm(x(:,4:6), 2, 2);   % Speed [m/s]
    plot(t, v_mag, 'r-', 'LineWidth', 1.5);
    xlabel('Time [s]');  ylabel('Speed [m/s]');
    title('Speed vs Time');  grid on;

    % Export as vector graphic for publication quality
    exportgraphics(gcf, sprintf('%s_trajectory.pdf', mission_name), ...
                   'ContentType', 'vector');
end
```

### 8.5 Monte Carlo Simulation Pattern

```matlab
function results = monte_carlo_dispersion(params, N_runs, sigma_table)
% monte_carlo_dispersion — launch dispersion analysis.
%
% sigma_table : struct with fields: mass, Isp, Cd, launch_angle
%               each field is 1-sigma uncertainty (fractional or absolute)

    results(N_runs) = struct('apogee', 0, 'landing_x', 0, 'max_q', 0);

    parfor k = 1:N_runs   % Parallel loop — requires Parallel Computing Toolbox
        p = params;       % Local copy for parfor safety

        % Sample dispersed parameters (normal distribution)
        p.mass.dry         = params.mass.dry * ...
                             (1 + sigma_table.mass * randn());
        p.motor.Isp        = params.motor.Isp * ...
                             (1 + sigma_table.Isp * randn());
        p.aero.Cd_scale    = 1 + sigma_table.Cd * randn();

        % Simulate
        [~, x_out] = run_simulation(p);

        % Extract metrics
        results(k).apogee    = max(-x_out(:,3));   % [m]
        results(k).landing_x = x_out(end,1);       % [m]
        results(k).max_q     = max(compute_q_dyn(x_out, p));  % [Pa]
    end

    % Report: 3-sigma landing ellipse, apogee statistics
    apogees    = [results.apogee];
    fprintf('Apogee: mean = %.1f m, 3σ = ±%.1f m\n', ...
             mean(apogees), 3*std(apogees));
end
```

---

## 9. Key Mathematical References

Students and engineers should be proficient with and cite from the following texts:

| Subject              | Reference                                                                |
| -------------------- | ------------------------------------------------------------------------ |
| Vector Calculus      | Marsden & Tromba, "Vector Calculus", 6th ed.                             |
| ODEs & Dynamics      | Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed.                        |
| Flight Dynamics      | Zipfel, "Modeling and Simulation of Aerospace Vehicle Dynamics", 3rd ed. |
| Orbital Mechanics    | Curtis, "Orbital Mechanics for Engineering Students", 3rd ed.            |
| Rocket Propulsion    | Sutton & Biblarz, "Rocket Propulsion Elements", 9th ed.                  |
| Atmospheric Reentry  | Anderson, "Introduction to Flight", 8th ed.                              |
| Numerical Methods    | Burden & Faires, "Numerical Analysis", 10th ed.                          |
| MATLAB for Engineers | Chapra & Canale, "Numerical Methods for Engineers", 7th ed.              |
| Structural Analysis  | Megson, "Aircraft Structures for Engineering Students", 5th ed.          |
| Thermodynamics       | Anderson, "Modern Compressible Flow", 3rd ed.                            |
