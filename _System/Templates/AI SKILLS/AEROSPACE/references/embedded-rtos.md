# Embedded Systems & Real-Time Engineering Reference

## Scope

Safety-critical firmware, RTOS-based systems (FreeRTOS, Zephyr, ChibiOS, RTIC),
bare-metal C/C++, Rust embedded, device drivers, communication protocols (CAN, SPI,
I2C, UART, SpaceWire), and hardware-in-the-loop (HIL) integration.

---

## 1. Safety-Critical Embedded Standards

### MISRA C:2012 — Mandatory Rules Always Enforced

Critical rules for aerospace/robotics firmware:

- **Rule 15.5**: A function shall have a single point of exit.
- **Rule 17.3**: No implicit function declarations.
- **Rule 18.1**: Pointer arithmetic bounds must be provable.
- **Rule 21.3**: No `malloc`/`free` — use static allocation only in safety-critical paths.
- **Rule 14.3**: No unreachable code.
- **Rule 16.4**: Every `switch` has a `default` clause.
- **Rule 12.1**: Use parentheses to clarify operator precedence — always.

### NASA JPL 10 Rules Implementation in C/C++

```c
/**
 * @file attitude_estimator.c
 * @brief Attitude estimation via quaternion EKF.
 *
 * Author   : [Name]
 * Date     : [YYYY-MM-DD]
 * Standard : NASA-STD-8739.8, MISRA C:2012, NASA JPL 10 Rules
 * Platform : STM32H7 / FreeRTOS
 * Units    : SI (rad, rad/s, m/s², s)
 *
 * Deviation record:
 *   None.
 */

#include <stdint.h>
#include <stdbool.h>
#include <assert.h>
#include "attitude_estimator.h"
#include "imu_driver.h"

/* JPL Rule 8: Limit preprocessor to include guards and simple constants */
#define QUAT_COMPONENTS   (4U)
#define STATE_DIM         (7U)   /* [q0 q1 q2 q3 bx by bz] */
#define MAX_ITERATIONS    (100U) /* JPL Rule 2: bounded loops */

/* All constants named with units in comment */
static const float GYRO_NOISE_VARIANCE   = 1.0e-6f;  /* [(rad/s)²/Hz] */
static const float ACCEL_NOISE_VARIANCE  = 1.0e-4f;  /* [(m/s²)²/Hz]  */
static const float INIT_ATT_VARIANCE     = 1.0e-3f;  /* [rad²] */

/**
 * @brief Initialize attitude estimator state.
 *
 * @param[out] state  Pointer to estimator state struct. Must not be NULL.
 * @return true on success, false on invalid input.
 *
 * @note Not thread-safe. Call once before task creation.
 */
bool att_estimator_init(AttEstimatorState_t* const state)
{
    /* JPL Rule 7: Check return values / parameters */
    if (state == NULL) {
        return false;
    }

    /* Initialize to identity quaternion */
    state->q[0] = 1.0f;
    state->q[1] = 0.0f;
    state->q[2] = 0.0f;
    state->q[3] = 0.0f;

    /* JPL Rule 5: Minimum 2 assertions per function */
    assert(state->q[0] == 1.0f);
    assert(state->q[1] == 0.0f);

    return true;
}
```

---

## 2. RTOS Patterns

### FreeRTOS — Task Design

```c
/* Task creation: always specify stack size explicitly based on analysis */
#define CONTROL_TASK_STACK_WORDS  512U   /* Words (4 bytes each) = 2 KB */
#define CONTROL_TASK_PRIORITY     (configMAX_PRIORITIES - 2U)  /* High, not highest */

static StaticTask_t control_task_tcb;
static StackType_t  control_task_stack[CONTROL_TASK_STACK_WORDS];

static void control_task(void* pvParameters)
{
    (void)pvParameters;  /* MISRA: cast to void to suppress warning */

    TickType_t last_wake_time = xTaskGetTickCount();
    const TickType_t period_ticks = pdMS_TO_TICKS(2U);  /* 500 Hz control loop */

    for (;;) {  /* FreeRTOS tasks must never return */
        /* Block until next period — precise timing */
        vTaskDelayUntil(&last_wake_time, period_ticks);

        /* Read sensors */
        ImuData_t imu_data;
        const bool imu_ok = imu_read(&imu_data);

        if (!imu_ok) {
            fault_handler_trigger(FAULT_IMU_TIMEOUT);
            continue;  /* MISRA 15.5: single exit — use continue for loop body */
        }

        /* Run estimator and controller */
        att_estimator_update(&imu_data);
        controller_step();
    }
}

/* CRITICAL: Use static allocation — no heap after init */
void create_control_task(void)
{
    const TaskHandle_t handle = xTaskCreateStatic(
        control_task,
        "ControlTask",
        CONTROL_TASK_STACK_WORDS,
        NULL,
        CONTROL_TASK_PRIORITY,
        control_task_stack,
        &control_task_tcb
    );
    assert(handle != NULL);  /* Must succeed — static allocation cannot fail */
}
```

### Priority Assignment — Rate Monotonic Analysis (RMA)

| Task              | Period  | Priority | WCET   | CPU% |
| ----------------- | ------- | -------- | ------ | ---- |
| IMU read / EKF    | 2 ms    | Highest  | 0.4 ms | 20%  |
| Control loop      | 2 ms    | High     | 0.3 ms | 15%  |
| Actuator output   | 2 ms    | High     | 0.1 ms | 5%   |
| Telemetry         | 100 ms  | Medium   | 2.0 ms | 2%   |
| Logging / storage | 1000 ms | Low      | 5.0 ms | 0.5% |

**Total CPU utilization < 70% — leave margin for ISRs and OS overhead.**

### Zephyr RTOS

- Use `CONFIG_THREAD_STACK_INFO=y` for stack overflow detection.
- Device drivers via **Device Tree** — no hardcoded addresses.
- All peripheral access through Zephyr HAL APIs only.
- Power management: implement `PM_DEVICE` API for all custom drivers.

---

## 3. Rust Embedded (RTIC Framework)

```rust
//! Attitude control firmware — RTIC v2.0
//!
//! Author    : [Name]
//! Date      : [YYYY-MM-DD]
//! Platform  : STM32F4 (cortex-m4)
//! Standard  : Rust API Guidelines, clippy clean, no unsafe without justification
//! Units     : SI throughout

#![no_std]
#![no_main]

use rtic::app;
use stm32f4xx_hal::{pac, prelude::*};

/// Control loop period [ms]
const CONTROL_PERIOD_MS: u32 = 2;

#[app(device = pac, peripherals = true, dispatchers = [EXTI0])]
mod app {
    use super::*;

    #[shared]
    struct Shared {
        attitude_q: [f32; 4],  // Unit quaternion [q0, q1, q2, q3]
    }

    #[local]
    struct Local {
        // hardware handles
    }

    #[init]
    fn init(ctx: init::Context) -> (Shared, Local) {
        // System clock, peripheral init here
        control_loop::spawn().unwrap();
        (
            Shared { attitude_q: [1.0, 0.0, 0.0, 0.0] },
            Local {},
        )
    }

    /// Control loop — highest priority, deterministic timing
    #[task(priority = 3, shared = [attitude_q])]
    async fn control_loop(mut ctx: control_loop::Context) {
        loop {
            // Read IMU, update estimator, compute control output
            ctx.shared.attitude_q.lock(|q| {
                // Update quaternion state
                let _ = q;  // placeholder
            });
            // Re-spawn after period
            rtic_monotonics::systick::Systick::delay(
                (CONTROL_PERIOD_MS as u64).millis()
            ).await;
        }
    }
}
```

### Rust Safety Rules for Embedded

- `unsafe` blocks require a `// SAFETY:` comment justifying why it is sound.
- No `unwrap()` in production paths — use `expect("context")` or handle errors.
- `#[no_std]` always for bare-metal targets.
- DMA buffers: use `#[link_section = ".dma_buffers"]` and ensure cache coherency.

---

## 4. Communication Protocols

### CAN Bus (Aerospace / Robotics Actuators)

- **CANopen** for robotics (DS301/DS402 device profiles).
- **UAVCAN / DroneCAN** for UAV/rocket avionics.
- Always implement message timeout detection (watchdog per node).
- Bit rate: 1 Mbit/s for nodes < 40 m; use CAN FD for high-bandwidth data.
- Error frame handling: implement bus-off recovery with exponential backoff.

### SPI / I2C Sensor Drivers

```c
/**
 * @brief Read IMU register with retry and CRC check.
 * Satisfies: MISRA C:2012 Rule 15.5, JPL Rule 7.
 *
 * @param[in]  reg_addr  Register address.
 * @param[out] data      Output buffer. Must not be NULL.
 * @param[in]  len       Number of bytes to read.
 * @return ImuStatus_t   IMU_OK on success, error code otherwise.
 */
ImuStatus_t imu_read_register(
    const uint8_t reg_addr,
    uint8_t* const data,
    const uint8_t len)
{
    uint8_t retry_count = 0U;
    ImuStatus_t status = IMU_ERROR_COMM;

    assert(data != NULL);
    assert(len > 0U);

    /* Retry up to MAX_RETRIES — JPL Rule 2: bounded loop */
    while ((retry_count < IMU_MAX_RETRIES) && (status != IMU_OK)) {
        status = spi_transfer(IMU_CS_PIN, reg_addr, data, len);
        retry_count++;
    }

    return status;
}
```

### SpaceWire (Space-Grade Interconnect)

- ECSS-E-ST-50-12C compliance required for space-grade designs.
- Use hardware SpaceWire cores (STAR-Dundee IP or GRLIB AMBA IP).
- Time distribution via SpaceWire Time Codes for synchronization.

---

## 5. HIL (Hardware-in-the-Loop) Testing

### HIL Architecture

```
[Simulation Host]                    [Target Hardware]
  RocketPy / JSBSim / Gazebo    ↔    MCU / FPGA
  (plant dynamics)                    (GNC firmware)
         ↑                                 ↓
  Sensor emulation (DAC)         Actuator commands (ADC)
         └─────── Real-Time I/O (UART/CAN/Ethernet) ───┘
```

### HIL Checklist

- [ ] Simulation runs at real-time factor ≥ 1.0 on host.
- [ ] All sensor models include noise, bias, and saturation.
- [ ] Actuator models include bandwidth, saturation, and dead-zone.
- [ ] Fault injection tested: sensor dropout, actuator stuck, bus timeout.
- [ ] Code running in HIL is identical byte-for-byte to flight binary.
- [ ] Timing verified with oscilloscope: control period jitter < 1% of nominal.

---

## 6. Build System & CI/CD for Embedded

### CMake + CTest for C/C++

```cmake
# Enforce compiler warnings — treat as errors
target_compile_options(firmware PRIVATE
    -Wall -Wextra -Werror
    -Wpedantic
    -Wconversion
    -Wshadow
    -fstack-usage          # Generate .su files for stack analysis
)

# Static analysis via clang-tidy
set(CMAKE_CXX_CLANG_TIDY "clang-tidy;-checks=cert-*,misra-*,cppcoreguidelines-*")
```

### Cargo for Rust

```toml
[profile.release]
opt-level = "z"      # Optimize for size
lto = true
codegen-units = 1
panic = "abort"      # No unwinding in embedded — saves code size

[profile.release.build-override]
opt-level = 3
```

### CI Pipeline Requirements

1. Compile for all target architectures (native + cross).
2. Static analysis (PC-lint, clang-tidy, or Polyspace).
3. Unit tests on host with sanitizers: ASan, UBsan.
4. Coverage report: target ≥ 80% line coverage, 100% for safety-critical modules.
5. Stack depth analysis: all tasks verified within allocated stack.
6. Binary size report: alert if flash usage exceeds 80% of budget.
