---
title: "Aerospace Robotics Skill Building"
date: 2026-04-03T00:18:51.309486Z
tags: [ai_memory, claude_context]
summary: "**Conversation Overview**  The person worked with Claude to collaboratively build a comprehensive engineering skill file using the skill-creator framework. The skill, named `aerospace-robotics-engineering`, is intended for a university rocket project and covers five core domains: control systems (PID, MPC, LQR, state-space), robotics (ROS/ROS2, SLAM, kinematics), rocket and aerospace engineering (GNC, propulsion, trajectory), embedded systems and RTOS (FreeRTOS, Zephyr, RTIC/Rust), and AI/ML for physical systems (RL for control, sensor fusion, computer vision, trajectory optimization). The skill was structured as a main `SKILL.md` hub with five domain reference files, following the person's explicit preference for modular organization over a monolithic file.  Through a structured intake process using multi-select questions, the person specified: all five engineering domains, languages C/C++, Python, MATLAB/Simulink, Rust, and JavaScript, NASA-STD/NPR and MISRA C/C++ safety standards, simulation toolchains RocketPy, OpenRocket, JSBSim, FlightGear, and Gazebo, and context-dependent code style guides. In a second session, the person requested a sixth reference file covering rocketry mathematics and applied physics, including vector calculus, differential equations, orbital mechanics, thermodynamics, structural mechanics, numerical methods, and MATLAB best practices. The person also asked Claude to verify whether NASA uses 15 digits of pi — Claude confirmed this is accurate based on JPL's official standard, explaining that `3.141592653589793` is sufficient for any engineering application and that MATLAB's built-in `pi` constant already satisfies this standard.  Two targeted fixes were applied at the person's direction: the `description` field in `SKILL.md` was condensed from 1,271 to 871 characters to comply with the 1,024-character limit (preserving all domain keywords and trigger phrases through syntactic compression), and the phrase "before responding" was appended to the multi-domain instruction sentence. The person provided the exact before/after text for that edit, indicating a preference for precise, literal edits when specifying changes. The final skill package was repackaged and delivered as `aerospace-robotics-engineering.skill` after each change."
---

### Human
Let's create a skill together using your skill-creator skill. First ask me what the skill should do.

### Assistant
 The user wants to create a new skill using the skill-creator skill. Let me first read the skill-creator SKILL.md file, then ask the user what the skill should do.
```
This block is not supported on your current device yet.
```

Now I have a good understanding of the skill-creator workflow. Let me ask the user what the skill should do.I've reviewed the skill-creator framework. Let's get started.

**What should this new skill do?**

Describe it in as much detail as you'd like — the problem it solves, the kinds of tasks it should handle, any tools or workflows it should follow, and what a good output looks like. The more context you provide upfront, the less back-and-forth we'll need before drafting.

### Human
This skill should be focused on control, robotics and rockets engineering, programming, design and developing in all the languages related to these fields applying all the best engineering and designing practices like a top professional, from NASA, Space X

### Assistant
 Great, the user wants a skill focused on control systems, robotics, and rockets/aerospace engineering. Let me ask more targeted questions to nail down the scope before drafting.Excellent domain choice — highly specialized and technically demanding. Before drafting, I need to sharpen the scope across several dimensions. Let me ask the precise questions that will determine the skill's architecture.
```
This block is not supported on your current device yet.
```

I need to wait for the user's response to these questions. But since the tool was called and there's no actual UI response (this is a simulation), I'll present the questions and wait for the user to respond.Please select your answers above, then I'll follow up with a second round of more targeted questions around standards, simulation toolchains, and edge cases before we draft anything.

### Human
Q: Which engineering domains should this skill explicitly cover? (Select all that apply)
A: Control Systems (PID, MPC, LQR, state-space), Robotics (kinematics, SLAM, ROS/ROS2), Rocket & Aerospace (GNC, propulsion, trajectory), Embedded Systems & Real-Time (RTOS, firmware), AI & Machine Learning Engineering

Q: Which programming languages / frameworks are in scope? (Select all that apply)
A: C / C++ (embedded, real-time), Python (simulation, ML, scripting), MATLAB / Simulink, Rust (safety-critical systems), JavaScript (Node.js/React)

Q: What is the primary output this skill should produce? (Select all that apply)
A: All of the above

### Assistant
 Good, now I have a clearer picture. Let me ask a second round of more targeted questions to nail down standards, toolchains, and specific behaviors before drafting.Good. Full-spectrum coverage across all five domains with all output types. Now let me drill into the standards, toolchains, and behavioral specifics that will define the quality bar for this skill.
```
This block is not supported on your current device yet.
```

Please select your answers above. Once you respond, I have one final focused question about code output conventions and then we move directly into drafting.

### Human
Q: Which industry standards & safety frameworks should the skill enforce? (Select all that apply)
A: MISRA C/C++ (safety-critical embedded), NASA-STD / NPR (NASA coding & safety standards)

Q: Which simulation & toolchain ecosystems should be explicitly supported? (Select all that apply)
A: OpenRocket / RASAero (rocket trajectory), JSBSim / FlightGear (flight dynamics), Gazebo / RViz (ROS simulation), RocketPy

Q: For AI/ML in this context, what is the primary application focus? (Select all that apply)
A: Reinforcement Learning for control & GNC, Sensor fusion & state estimation, Computer Vision for robotics perception, Trajectory Optimization

### Assistant
 Now I have a comprehensive picture. Let me ask one final question about code conventions and then draft the skill.One final round before drafting — this covers code conventions and the structural organization of the skill itself.
```
This block is not supported on your current device yet.
```



### Human
Q: Which code style conventions should the skill enforce per language?
A: All of the above, context-dependent

Q: How should the skill be structured internally?
A: Main SKILL.md + separate reference files per domain (recommended)

### Assistant
 Now I have everything I need to draft the skill. Let me create a comprehensive skill with:

1. Main SKILL.md hub
2. Separate reference files per domain:
   - control-systems.md
   - robotics.md
   - rocket-aerospace.md
   - embedded-rtos.md
   - ai-ml-engineering.md

Let me design this carefully following the skill-creator guidelines.

Structure:
```
aerospace-robotics-engineering/
├── SKILL.md (main hub, routing, universal standards)
└── references/
    ├── control-systems.md
    ├── robotics.md
    ├── rocket-aerospace.md
    ├── embedded-rtos.md
    └── ai-ml-engineering.md
```

Now let me draft each file. I'll start with SKILL.md and then the reference files.

For SKILL.md:
- YAML frontmatter with name and description (pushy description)
- Overview of the skill
- Domain routing table
- Universal engineering standards (code style per language, safety standards)
- When to read which reference file

Let me draft this now.

**SKILL.md main hub content:**
- Name: aerospace-robotics-engineering
- Description: comprehensive trigger description
- Universal standards section
- Domain router
- Code style per language
- Safety standards enforcement

**References:**

1. `control-systems.md` - PID, MPC, LQR, state-space, simulation with Python/MATLAB/Simulink
2. `robotics.md` - ROS2, kinematics, SLAM, Gazebo, CoppeliaSim/Webots
3. `rocket-aerospace.md` - GNC, propulsion, trajectory, OpenRocket, RocketPy, JSBSim
4. `embedded-rtos.md` - C/C++, Rust, MISRA, RTOS patterns, firmware
5. `ai-ml-engineering.md` - RL for control/GNC, sensor fusion, CV for perception, trajectory optimization

Let me write these out now. I need to be comprehensive but concise enough to fit within the skill framework guidelines (main SKILL.md under 500 lines, reference files as needed).

Let me draft the files:Perfect. I have everything needed to draft the full skill package. Let me build it now — main hub plus all five domain reference files.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now let me package the skill using the package_skill script if available, otherwise I'll present the files directly.Now let me verify the full structure and package the skill.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

The skill is packaged and ready. Here is a precise breakdown of what was built:

---

**Skill: `aerospace-robotics-engineering`**

**Structure — 6 files:**

| File | Purpose | Lines |
|------|---------|-------|
| `SKILL.md` | Main hub: domain router, universal standards, code style matrix, NASA JPL 10 rules, output templates | 154 |
| `references/control-systems.md` | PID, LQR/LQE, MPC — with full Python code patterns, stability checklists, MATLAB standards | ~200 |
| `references/robotics.md` | ROS2 node architecture, kinematics, SLAM, motion planning, Gazebo sim2real | ~220 |
| `references/rocket-aerospace.md` | GNC, quaternion INS, trajectory optimization, RocketPy, JSBSim, propulsion, NASA margins | ~230 |
| `references/embedded-rtos.md` | MISRA C, FreeRTOS, Zephyr, RTIC/Rust, CAN/SPI/SpaceWire, HIL, CI/CD for firmware | ~240 |
| `references/ai-ml-engineering.md` | RL for GNC, EKF template, CV perception pipeline, iLQR/JAX, sim2real protocol | ~250 |

---

**Next steps — your call on which direction to take:**

1. **Run test cases** — I draft 5–8 representative prompts (e.g., *"Design a PID controller for a rocket TVC system"*, *"Write a ROS2 lifecycle node for an IMU driver"*) and execute them with the skill active to validate quality.
2. **Refine a specific domain** — If any reference file needs deeper coverage (e.g., more MPC examples, orbital mechanics, specific RTOS), we iterate now.
3. **Optimize the trigger description** — Run the description optimization loop to maximize the rate at which Claude correctly activates this skill.

Which would you prefer?

### Human
Also add something related to the rocketry math, all the good practices and math/calculus fields, and advanced physics applied to this rocket project. All the vectorial calculus, differential equations, differential and integral calculus, physics fields related to rockets design and launching for this university project. Also using the matlab good practices. I have heard that NASA uses 15 digits of pi to perform their calculus, confirm if it is true, if not just apply the best practices used on this field

### Assistant
 The user wants to add a new reference file for advanced mathematics and physics applied to rocketry. They also want MATLAB best practices integrated. Let me also verify the NASA pi claim via web search.
```
This block is not supported on your current device yet.
```

The NASA pi question is confirmed. JPL uses exactly 15 decimal places: 3.141592653589793. Now let me add the rocketry mathematics reference file and update the SKILL.md to include it in the domain router.

Let me create a comprehensive `references/rocketry-mathematics.md` file covering:
1. The NASA pi answer (confirmed)
2. Vector calculus for rockets (gradient, divergence, curl, line/surface integrals)
3. Differential equations (ODEs for flight dynamics, PDEs for thermodynamics)
4. Integral calculus (mass integrals, impulse, work-energy)
5. Rigid body dynamics (Euler's equations, angular momentum)
6. Orbital mechanics (Kepler's laws, vis-viva)
7. Atmospheric models (standard atmosphere, dynamic pressure)
8. Thermodynamics and combustion
9. Structural mechanics basics
10. Numerical methods
11. MATLAB best practices for these calculationsConfirmed. Now building the mathematics & physics reference file, then updating the SKILL.md router.

The NASA JPL answer is precise and sourced directly: for JPL's highest accuracy calculations — interplanetary navigation — they use `3.141592653589793`, which is π to 15 decimal places. The rationale is compelling: using that value to compute the circumference of a circle with a 40-billion-mile diameter yields an error of just over half an inch. So the claim is **confirmed as correct** — 15 decimal places is the professional standard, and to compute the circumference of the observable universe to the precision of a hydrogen atom's diameter, you would only need 39 or 40 decimal places — meaning more than 15 is physically meaningless for any engineering application.
```
This block is not supported on your current device yet.
```

Now update the SKILL.md router to include the new reference file.
```
This block is not supported on your current device yet.
```

Also update the description to trigger on math/calculus requests.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now repackage and deliver.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Updated skill package delivered. Here is a precise account of what was added.

---

**On the NASA π question — confirmed and clarified:**

For interplanetary navigation — JPL's highest-accuracy calculations — they use exactly `3.141592653589793` (15 decimal places). This is confirmed by Marc Rayman, JPL's Chief Engineer for Mission Operations. The engineering rationale: using π rounded to the 15th decimal point to compute the circumference of a 40-billion-mile diameter circle yields an error of just over half an inch. And at cosmic scales, computing the circumference of the observable universe to an accuracy equal to a hydrogen atom's diameter would require only 39 or 40 decimal places — meaning 15 is more than sufficient for any rocket engineering application.

**Practical rule encoded in the skill**: In MATLAB, `pi` (the built-in constant) already stores `3.141592653589793` as an IEEE 754 double — it satisfies the JPL standard by default. Never use inline literals like `3.14` or `3.14159`.

---

**What was added — `references/rocketry-mathematics.md` (636 lines):**

The new reference file covers, in full production-ready MATLAB and mathematical form: the JPL π standard and all physical constants; coordinate frame conventions (ECI, ECEF, NED, Body, Wind); vector calculus applied to rocket engineering (gradient/divergence/curl, line and surface integrals for pressure loads and impulse); the complete 6-DOF equations of motion (translational, rotational via Euler's equations, quaternion kinematics, mass depletion); MATLAB ODE solver selection guide with `ode45`/`ode15s` patterns and event detection; orbital mechanics (vis-viva, Hohmann transfer); International Standard Atmosphere (ISA) MATLAB implementation; isentropic nozzle flow relations and exhaust velocity derivation; structural buckling and max-Q loading; numerical differentiation best practices (central differences, optimal step size); and a full MATLAB engineering conventions section covering file organization, `validateattributes`, struct-based parameter passing, plotting standards, and Monte Carlo dispersion analysis with `parfor`.

A curated reference table mapping each mathematical subject to the authoritative textbook (Sutton, Curtis, Zipfel, Strogatz, Anderson, etc.) is included at the end.

### Human
field 'description' in SKILL.md must be at most 1024 characters. Fix it but avoid losing the quality of the document

### Assistant
 Let me check the current description length and then trim it to under 1024 characters.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

It's 1271 characters, need to get it under 1024. Let me craft a tight version that preserves all the key trigger terms without sacrificing coverage. I need to cut ~250 characters while keeping all domain keywords.

Let me write a condensed version:

"Expert-level skill for control systems, robotics, rocket & aerospace engineering, embedded systems, and AI/ML for physical systems — at NASA/SpaceX professional standards. Trigger whenever the user mentions: PID/MPC/LQR/state-space, ROS/ROS2/SLAM/kinematics, GNC/propulsion/trajectory/TVC, RTOS/firmware/C++/Rust/bare-metal, RocketPy/OpenRocket/JSBSim/Gazebo/FlightGear, RL for control/sensor fusion/CV perception/trajectory optimization, vector calculus/ODEs/orbital mechanics/thermodynamics/structural mechanics/MATLAB simulation, or safety-critical/real-time systems. Also trigger for: "design a controller", "write firmware", "simulate a rocket", "ROS node", "SLAM", "RL for GNC", "equations of motion", "delta-v", "MATLAB sim", "rocketry math/physics". When in doubt, use this skill."

Let me count that...

"Expert-level skill for control systems, robotics, rocket & aerospace engineering, embedded systems, and AI/ML for physical systems — at NASA/SpaceX professional standards. Trigger whenever the user mentions: PID/MPC/LQR/state-space, ROS/ROS2/SLAM/kinematics, GNC/propulsion/trajectory/TVC, RTOS/firmware/C++/Rust/bare-metal, RocketPy/OpenRocket/JSBSim/Gazebo/FlightGear, RL for control/sensor fusion/CV perception/trajectory optimization, vector calculus/ODEs/orbital mechanics/thermodynamics/structural mechanics/MATLAB simulation, or safety-critical/real-time systems. Also trigger for: \"design a controller\", \"write firmware\", \"simulate a rocket\", \"ROS node\", \"SLAM\", \"RL for GNC\", \"equations of motion\", \"delta-v\", \"MATLAB sim\", \"rocketry math/physics\". When in doubt, use this skill."

Let me count: ~780 chars. That's fine, well under 1024. Let me be a bit more specific to improve triggering quality while staying under 1024.
```
This block is not supported on your current device yet.
```

860 characters — well under the limit, all trigger keywords preserved. Applying the fix.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

871 characters — 153 under the 1024 limit. Now repackage.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Fixed. The description went from **1,271 → 871 characters** (153 under the 1,024 limit).

The compression strategy was purely syntactic — no domain coverage was dropped:
- Verbose phrases like `"Use this skill whenever the user mentions: control loops (PID, MPC, LQR)"` became `"PID/MPC/LQR/state-space control"` — same trigger surface, half the characters.
- Redundant qualifiers (`"designed to produce"`, `"applied to physical systems"`, `"even for vague requests like"`) were tightened without changing meaning.
- All 6 domains, all simulation toolchains, all trigger phrases, and the "when in doubt" directive are fully intact.

### Human
CAN YOU ADD THIS "before responding" after this phrase on the skill file?

```skill
If the request spans multiple domains (e.g., RL-based GNC, ROS2 + embedded), read all relevant reference files.
```

The final paragraph should be:

```skill
If the request spans multiple domains (e.g., RL-based GNC, ROS2 + embedded), read all relevant reference files before responding.
```

### Assistant
 Simple edit.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Done. "before responding" added exactly as specified. The updated skill package is ready for download.

