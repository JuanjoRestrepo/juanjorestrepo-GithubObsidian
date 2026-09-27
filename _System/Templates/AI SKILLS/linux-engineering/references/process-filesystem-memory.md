# Process, Filesystem, and Memory

## Table of Contents
1. /proc Virtual Filesystem Reference
2. /sys Virtual Filesystem
3. Virtual Memory Model and OOM Killer
4. File Descriptors and Limits
5. IPC Mechanisms
6. cgroups v2 — Containers and Resource Control
7. Linux Namespaces — What Docker Actually Does

---

## §1 /proc Virtual Filesystem Reference

`/proc` is a kernel interface disguised as a filesystem. Files are generated on-read; writes into writable entries change kernel state. Zero bytes on disk.

### Per-Process Entries: `/proc/[PID]/`

```bash
PID=$(pgrep -f "airflow scheduler" | head -1)

# Open file descriptors
ls -la /proc/$PID/fd                  # All open files, sockets, pipes
ls /proc/$PID/fd | wc -l             # FD count (diagnose fd leak)
readlink /proc/$PID/fd/0             # stdin target
readlink /proc/$PID/fd/1             # stdout target

# Memory maps
cat /proc/$PID/maps                  # Virtual address space: file-backed + anonymous regions
cat /proc/$PID/smaps                 # Detailed per-region memory stats (RSS, PSS, Dirty)
cat /proc/$PID/status                # Human-readable: VmRSS, VmPeak, Threads, FDSize

# Environment and command line
cat /proc/$PID/environ | tr '\0' '\n'  # All env vars of running process
cat /proc/$PID/cmdline | tr '\0' ' '   # Full command line

# Resource consumption
cat /proc/$PID/stat                  # Raw kernel stats (CPU time, state, parent PID)
cat /proc/$PID/io                    # Read/write byte counts — I/O attribution per process
cat /proc/$PID/net/tcp               # Open TCP connections for this process's net namespace
```

**Data Engineering use cases:**
```bash
# Verify Airflow scheduler loaded the correct DB connection env var
grep -z "AIRFLOW__DATABASE" /proc/$PID/environ | tr '\0' '\n'

# Count open FDs for a leaky Spark worker
ls /proc/$PID/fd 2>/dev/null | wc -l

# Identify which files a stalled ETL job has open
ls -la /proc/$PID/fd | grep -v "^total" | awk '{print $NF}'
```

### System-Wide /proc Entries

```bash
# CPU information — detect core count for parallelism tuning
cat /proc/cpuinfo | grep "^processor" | wc -l   # Logical core count
cat /proc/cpuinfo | grep "model name" | head -1

# Memory overview — critical for Spark/Pandas sizing decisions
cat /proc/meminfo
# Key fields:
# MemTotal:     Total physical RAM
# MemFree:      Completely unused
# MemAvailable: Realistically available (free + reclaimable cache) — USE THIS
# Buffers:      Raw disk block cache
# Cached:       Page cache (file data) — reclaimable under pressure
# SwapTotal/SwapFree: Swap space
# Dirty:        Pages written but not yet flushed to disk
# HugePages_*:  Huge page usage (Spark/JVM benefits from this)

# Load average (1, 5, 15 minute) and running/total processes
cat /proc/loadavg

# Kernel tunables (readable; many writable via sysctl)
cat /proc/sys/vm/swappiness              # 0-100: preference for swapping
cat /proc/sys/vm/overcommit_memory       # 0=heuristic, 1=always, 2=never
cat /proc/sys/fs/file-max                # System-wide open file limit
cat /proc/sys/net/ipv4/tcp_syncookies   # SYN flood protection
```

---

## §2 /sys Virtual Filesystem

`/sys` (sysfs) exposes kernel objects — devices, drivers, buses, and kernel subsystems — as a structured directory tree.

```bash
# Block device information
ls /sys/block/                           # All block devices
cat /sys/block/sda/size                  # Device size in 512-byte sectors
cat /sys/block/sda/queue/scheduler       # I/O scheduler: [none] mq-deadline kyber
cat /sys/block/sda/queue/rotational      # 0=SSD, 1=HDD — tuning decisions

# Set I/O scheduler for SSDs (reduces latency for random I/O pipelines)
echo "none" > /sys/block/nvme0n1/queue/scheduler

# CPU frequency and power state
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor  # performance|powersave|schedutil
echo "performance" > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# cgroups v2 hierarchy root
ls /sys/fs/cgroup/                       # Root cgroup tree
cat /sys/fs/cgroup/memory.stat          # System-wide memory accounting
```

---

## §3 Virtual Memory Model and OOM Killer

### How Memory Works on Linux

```
Process virtual address space (per-process, huge — 128TB on x86_64):
  ┌── Text segment (code) — mapped from binary, shared
  ├── Data segment (globals, heap via malloc/brk)
  ├── Memory-mapped files (mmap — Pandas uses this heavily)
  ├── Stack (grows downward)
  └── Anonymous mappings (malloc, Python objects)

Physical pages are only allocated on first access (copy-on-write for fork).
The kernel reclaims page cache under memory pressure before touching process memory.
```

**Key concepts for DE workloads:**

- **RSS (Resident Set Size):** Pages currently in physical RAM — the number that matters.
- **VSZ (Virtual Size):** Total virtual address space allocated — can be much larger than RSS; not a real memory usage number.
- **Page cache:** Linux caches all disk reads in RAM. `MemAvailable` (not `MemFree`) is the correct measure of usable memory.
- **Swap pressure:** When swap is active during Pandas or Spark jobs, performance collapses. Design for `MemAvailable > job_memory_footprint`.

### OOM Killer

The OOM killer activates when the system cannot satisfy a memory allocation and swap is exhausted. It selects a victim process based on `oom_score` and kills it.

```bash
# Check OOM score for a running process (higher = more likely to be killed)
cat /proc/$PID/oom_score
cat /proc/$PID/oom_score_adj   # Adjustable: -1000 (never kill) to 1000 (kill first)

# Protect a critical service from OOM kill (e.g., Airflow scheduler)
echo -1000 > /proc/$(pgrep -f "airflow scheduler")/oom_score_adj
# Make persistent in the systemd unit:
# OOMScoreAdjust=-900

# Monitor OOM kill events
dmesg | grep -i "oom\|killed process"
journalctl -k | grep -i "out of memory"

# Kernel memory overcommit policy
sysctl vm.overcommit_memory        # 0: heuristic (default), 1: always allow, 2: strict
sysctl vm.overcommit_ratio         # With mode 2: commit limit = RAM * ratio/100 + swap

# Recommended for Spark/heavy analytics servers:
sysctl -w vm.swappiness=10         # Strongly prefer RAM over swap
sysctl -w vm.overcommit_memory=0   # Heuristic — reasonable default
```

---

## §4 File Descriptors and Limits

FD exhaustion is a common failure mode for Airflow schedulers and long-running Python ETL daemons.

```bash
# Current limits for a running process
cat /proc/$PID/limits                   # Soft and hard limits for all resources

# System limits
ulimit -n                               # Current session soft FD limit
ulimit -Hn                              # Hard limit
ulimit -n 65536                         # Raise soft limit (up to hard limit) in session

# System-wide open FD count
cat /proc/sys/fs/file-nr               # [used] [free] [max]
sysctl fs.file-max                      # Maximum FDs across entire system
```

### Persistent Limit Configuration

```bash
# /etc/security/limits.conf or /etc/security/limits.d/airflow.conf
airflow   soft   nofile   65536
airflow   hard   nofile   65536
airflow   soft   nproc    4096
airflow   hard   nproc    4096

# For systemd-managed services (overrides pam limits for that unit)
[Service]
LimitNOFILE=65536
LimitNPROC=4096

# Kernel-level maximum (survives reboot via /etc/sysctl.d/)
# /etc/sysctl.d/99-limits.conf
fs.file-max = 2097152
```

---

## §5 IPC Mechanisms

| Mechanism | Use Case | Key Commands |
|---|---|---|
| Signals | Control process state, trigger reload | `kill -SIGUSR1 $PID`, `trap` |
| Unnamed pipes `\|` | Chain stdout→stdin in same session | Built into shell |
| Named pipes (FIFO) | Decouple producer/consumer processes | `mkfifo`, `cat > fifo &` |
| Unix domain sockets | High-throughput IPC on same host | Docker daemon, Airflow |
| Shared memory | Zero-copy data between processes | `mmap()`, `/dev/shm/` |

```bash
# Signal reference for DE operations
kill -SIGHUP  $PID    # (1)  Reload config without restart
kill -SIGTERM $PID    # (15) Graceful shutdown request
kill -SIGKILL $PID    # (9)  Force kill — no cleanup, no trap
kill -SIGUSR1 $PID    # (10) User-defined — Airflow uses this for log rotation
kill -SIGSTOP $PID    # (19) Pause process (preserves state)
kill -SIGCONT $PID    # (18) Resume a stopped process

# Named FIFO for decoupled producer/consumer ETL
mkfifo /tmp/transform_pipe
python3 producer.py > /tmp/transform_pipe &
python3 consumer.py < /tmp/transform_pipe
```

---

## §6 cgroups v2 — Containers and Resource Control

cgroups v2 is the kernel mechanism behind Docker, Kubernetes, and systemd resource management. Understanding it explains why a Spark worker gets OOM-killed by the container runtime rather than the kernel.

### cgroups v2 Architecture

```
/sys/fs/cgroup/          ← Root cgroup (all system processes)
├── memory.max           ← Memory limit for root (usually infinity)
├── cpu.max              ← CPU bandwidth: quota/period
├── system.slice/        ← systemd system services
│   ├── airflow-scheduler.service/
│   │   ├── memory.max   ← e.g., "4294967296" (4GB)
│   │   ├── memory.current
│   │   ├── cpu.max      ← "200000 1000000" = 20% of one CPU
│   │   └── pids.max     ← Max process count
│   └── docker.service/
└── user.slice/          ← User session cgroups
```

```bash
# Which cgroup does a process belong to?
cat /proc/$PID/cgroup

# Live memory usage of a systemd service's cgroup
cat /sys/fs/cgroup/system.slice/airflow-scheduler.service/memory.current
cat /sys/fs/cgroup/system.slice/airflow-scheduler.service/memory.stat

# CPU throttling statistics (detect if a service is hitting CPU limits)
cat /sys/fs/cgroup/system.slice/airflow-scheduler.service/cpu.stat
# throttled_usec tells you how long the process was throttled

# Configure limits via systemd unit (preferred — persistent)
[Service]
MemoryMax=4G
MemorySwapMax=0        # Disable swap for this service
CPUQuota=200%          # Allow up to 2 full CPU cores
TasksMax=512           # Maximum PIDs (threads + processes)
```

### Container Memory Limits in Docker

```bash
# Docker translates --memory into cgroup v2 memory.max
docker run --memory=4g --memory-swap=4g \  # swap=memory means no extra swap
           --cpus=2 spark-worker

# Check effective limits from inside the container
cat /sys/fs/cgroup/memory.max
cat /sys/fs/cgroup/cpu.max

# This is why spark.executor.memory must stay below docker --memory
# The OOM kill at cgroup level is immediate and non-negotiable
```

---

## §7 Linux Namespaces — What Docker Actually Does

Linux namespaces partition kernel resources so a group of processes has its own isolated view. Docker does NOT use a hypervisor — it creates a set of namespaces and cgroup constraints around a process tree.

| Namespace | Isolates | API Flag | Practical Effect |
|---|---|---|---|
| `pid` | Process IDs | `CLONE_NEWPID` | Container sees its main process as PID 1 |
| `net` | Network stack | `CLONE_NEWNET` | Container gets its own network interfaces, routing table, iptables |
| `mnt` | Mount points | `CLONE_NEWNS` | Container filesystem (overlay) is isolated from host |
| `uts` | Hostname, domain | `CLONE_NEWUTS` | Container can have its own hostname |
| `ipc` | SysV IPC, POSIX MQ | `CLONE_NEWIPC` | Shared memory segments isolated |
| `user` | UID/GID mapping | `CLONE_NEWUSER` | UID 0 inside maps to non-privileged UID on host |
| `cgroup` | cgroup root view | `CLONE_NEWCGROUP` | Container sees only its own cgroup subtree |
| `time` | Clock offsets | `CLONE_NEWTIME` | Independent clock offsets per namespace (kernel 5.6+) |

### Inspecting Namespaces

```bash
# List all namespaces of a process
ls -la /proc/$PID/ns/

# Inspect a Docker container's namespaces
CONTAINER_PID=$(docker inspect --format '{{.State.Pid}}' my-container)
ls -la /proc/$CONTAINER_PID/ns/

# Enter a running container's namespace (from host) — powerful debugging tool
nsenter --target "$CONTAINER_PID" --net --pid \
    ip addr show                # See container's network interfaces from host

nsenter --target "$CONTAINER_PID" --mount --pid \
    ls /proc/1/fd               # Inspect container PID 1's open file descriptors

# Run an isolated shell in new namespaces (test namespace isolation without Docker)
unshare --pid --fork --mount-proc bash
echo $$  # Will show PID 1 — isolated from host PID namespace
```

### Network Namespace and Docker Bridge

```bash
# Docker creates a veth (virtual ethernet) pair for each container
# One end (veth*) stays on the host bridge (docker0)
# Other end (eth0) is moved into the container's net namespace

ip link show type veth           # List all veth pairs on host
ip addr show docker0             # Docker bridge interface (172.17.0.1/16 default)

# Trace a container's network path
bridge link show docker0         # Container MAC → veth mapping
ip netns list                    # Alternatively, named network namespaces
```
