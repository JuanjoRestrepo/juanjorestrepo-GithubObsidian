# systemd Services

## Table of Contents
1. systemd Architecture and Unit Graph
2. Unit File Anatomy
3. Service Management — systemctl Reference
4. Journal Querying — journalctl Reference
5. Service Hardening Directives
6. Production Unit Files for DE Tools
7. systemd Timers — cron Replacement
8. Socket Activation
9. Log Rotation and Management

---

## §1 systemd Architecture and Unit Graph

```
systemd (PID 1)
│
├── Unit types: .service .socket .timer .path .mount .target .slice
│
├── Targets (runlevels equivalent):
│   ├── poweroff.target     (runlevel 0)
│   ├── rescue.target       (runlevel 1 — single user)
│   ├── multi-user.target   (runlevel 3 — no GUI) ← DE servers use this
│   ├── graphical.target    (runlevel 5 — GUI)
│   └── reboot.target       (runlevel 6)
│
├── Slices (cgroup hierarchy):
│   ├── system.slice    ← systemd services run here
│   ├── user.slice      ← user session services
│   └── machine.slice   ← VMs, containers
│
└── Sockets → Services (on-demand activation)
```

```bash
systemctl list-units --type=service              # All loaded services
systemctl list-units --type=service --state=failed
systemctl list-unit-files --type=service         # All available (enabled/disabled/static)
systemctl list-dependencies airflow-scheduler    # Dependency graph
systemctl list-dependencies --reverse nginx      # What depends ON nginx
```

**Boot sequence inspection:**

```bash
systemd-analyze                          # Total boot time
systemd-analyze blame                    # Per-service boot times sorted
systemd-analyze critical-chain           # Critical path through boot
systemd-analyze plot > boot.svg          # Visual boot timeline
```

---

## §2 Unit File Anatomy

Unit files live in:
- `/lib/systemd/system/` — package-provided (do not edit)
- `/etc/systemd/system/` — admin overrides (edit here)
- `/etc/systemd/system/<unit>.d/override.conf` — drop-in overrides (preferred for partial changes)

```ini
# /etc/systemd/system/airflow-scheduler.service
[Unit]
Description=Apache Airflow Scheduler
Documentation=https://airflow.apache.org/docs/
After=network-online.target postgresql.service redis.service
Wants=network-online.target
Requires=postgresql.service
PartOf=airflow.target                  # Optional: grouped restart with a target

[Service]
# ─── Process type ────────────────────────────────────────────────────────────
Type=simple                            # Process stays in foreground; PID is main process
# Type=forking                         # Legacy: forks to background; set PIDFile=
# Type=notify                          # Process signals ready via sd_notify()
# Type=oneshot                         # Runs to completion (good for ExecStart scripts)
# Type=exec                            # Like simple but waits for exec() to complete

# ─── Identity ────────────────────────────────────────────────────────────────
User=airflow
Group=airflow
WorkingDirectory=/opt/airflow

# ─── Environment ─────────────────────────────────────────────────────────────
EnvironmentFile=/etc/airflow/environment    # key=value file; never inline secrets

# ─── Execution ───────────────────────────────────────────────────────────────
ExecStart=/opt/pyenvs/airflow/bin/airflow scheduler
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -SIGTERM $MAINPID

# ─── Lifecycle ───────────────────────────────────────────────────────────────
TimeoutStartSec=90
TimeoutStopSec=60                      # Time to graceful shutdown before SIGKILL
Restart=on-failure                     # Restart policy: no | on-success | on-failure | always
RestartSec=10s
StartLimitIntervalSec=120s
StartLimitBurst=3                      # Max 3 restarts in 120s before giving up

# ─── Resources ───────────────────────────────────────────────────────────────
LimitNOFILE=65536
LimitNPROC=4096
MemoryMax=4G
MemorySwapMax=0
CPUQuota=200%
OOMScoreAdjust=-900                    # Protect scheduler from OOM kill

# ─── Hardening (see §5) ──────────────────────────────────────────────────────
PrivateTmp=true
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/airflow /var/log/airflow /data
CapabilityBoundingSet=

# ─── Logging ─────────────────────────────────────────────────────────────────
StandardOutput=journal
StandardError=journal
SyslogIdentifier=airflow-scheduler

[Install]
WantedBy=multi-user.target
```

### Drop-In Override Pattern (Preferred for Partial Changes)

```bash
systemctl edit airflow-scheduler       # Opens /etc/systemd/system/airflow-scheduler.service.d/override.conf
```

```ini
# /etc/systemd/system/airflow-scheduler.service.d/override.conf
[Service]
MemoryMax=8G                           # Override only MemoryMax; all other directives preserved
```

```bash
systemctl daemon-reload                # Always required after editing unit files
systemctl restart airflow-scheduler
```

---

## §3 Service Management — systemctl Reference

```bash
# Enable/disable (controls whether service starts at boot)
systemctl enable airflow-scheduler           # Create symlink in WantedBy target
systemctl enable --now airflow-scheduler     # Enable AND start immediately
systemctl disable airflow-scheduler          # Remove symlink
systemctl disable --now airflow-scheduler    # Disable AND stop immediately
systemctl mask nginx                         # Prevent service from being started at all
systemctl unmask nginx

# Start/stop/restart
systemctl start   airflow-scheduler
systemctl stop    airflow-scheduler
systemctl restart airflow-scheduler
systemctl reload  airflow-scheduler          # Send SIGHUP (reload config, no restart)
systemctl reload-or-restart airflow-scheduler

# Status and inspection
systemctl status airflow-scheduler          # State, recent log tail, PID, cgroup
systemctl is-active  airflow-scheduler      # Prints: active | inactive | failed
systemctl is-enabled airflow-scheduler      # Prints: enabled | disabled | static
systemctl is-failed  airflow-scheduler      # Exit 0 if failed

# Show all directives resolved for a unit (includes defaults + overrides)
systemctl show airflow-scheduler
systemctl show airflow-scheduler --property=MainPID,MemoryMax,Restart

# After editing unit files
systemctl daemon-reload
```

---

## §4 Journal Querying — journalctl Reference

```bash
# Follow live output
journalctl -f -u airflow-scheduler                    # Follow specific service
journalctl -f -u airflow-scheduler -u airflow-webserver  # Multiple units

# Historical queries
journalctl -u airflow-scheduler                       # All logs for this unit
journalctl -u airflow-scheduler -n 200                # Last 200 lines
journalctl -u airflow-scheduler --since "2024-09-10 08:00:00"
journalctl -u airflow-scheduler --since "1 hour ago" --until "30 min ago"
journalctl -u airflow-scheduler --since today

# Priority filtering
journalctl -u airflow-scheduler -p err                # Errors and above only
journalctl -u airflow-scheduler -p warning            # Warnings and above
# Priorities: emerg(0) alert(1) crit(2) err(3) warning(4) notice(5) info(6) debug(7)

# Structured output for log ingestion pipelines
journalctl -u airflow-scheduler -o json               # One JSON object per line
journalctl -u airflow-scheduler -o json-pretty        # Formatted JSON (debug)
journalctl -u airflow-scheduler -o cat                # Message only (no metadata)

# Kernel messages only
journalctl -k --since "1 hour ago"                    # dmesg equivalent with timestamps
journalctl -k | grep -i "oom\|killed\|error"

# Disk usage and maintenance
journalctl --disk-usage
journalctl --vacuum-size=500M      # Reduce journal to 500 MB
journalctl --vacuum-time=30d       # Remove logs older than 30 days

# Boot-specific logs
journalctl -b                      # Current boot
journalctl -b -1                   # Previous boot
journalctl --list-boots            # All stored boots with timestamps
```

---

## §5 Service Hardening Directives

These directives go in the `[Service]` section. They use Linux security features to sandbox the service — reduce blast radius if the service is compromised.

```ini
[Service]
# ─── Filesystem isolation ────────────────────────────────────────────────────
PrivateTmp=true              # Service gets isolated /tmp and /var/tmp (tmpfs)
ProtectSystem=strict         # /usr, /boot, /etc mounted read-only
ProtectSystem=full           # /usr, /boot mounted read-only (/etc still writable)
ProtectHome=true             # /home, /root, /run/user inaccessible
ProtectHome=read-only        # /home readable but not writable
ReadWritePaths=/opt/airflow /var/log/airflow /data    # Exceptions to ProtectSystem=strict
ReadOnlyPaths=/etc/airflow   # Explicitly read-only (config files)
InaccessiblePaths=/proc/sysrq-trigger

# ─── Process isolation ───────────────────────────────────────────────────────
NoNewPrivileges=true         # Prevents privilege escalation via setuid/setcap
PrivateDevices=true          # Only grants access to pseudo-devices (/dev/null, /dev/random)
PrivateNetwork=false         # Set true only for services needing no network
PrivateUsers=true            # Isolated user namespace (requires kernel 3.9+)

# ─── Capability control ──────────────────────────────────────────────────────
CapabilityBoundingSet=                           # Empty: strip ALL capabilities
CapabilityBoundingSet=CAP_NET_BIND_SERVICE       # Only allow binding to ports < 1024
AmbientCapabilities=CAP_NET_BIND_SERVICE         # Grant capability without being root

# ─── Syscall filtering ───────────────────────────────────────────────────────
SystemCallFilter=@system-service                 # Allow common service syscalls only
SystemCallFilter=~@debug @reboot @mount          # Explicitly deny dangerous syscall groups
SystemCallErrorNumber=EPERM                      # Return EPERM instead of killing process

# ─── Namespace isolation ─────────────────────────────────────────────────────
ProtectKernelTunables=true   # /proc/sys, /sys read-only
ProtectKernelModules=true    # Prevents module loading/unloading
ProtectKernelLogs=true       # Prevents access to kernel log ring buffer
ProtectClock=true            # Prevents changing system clock
ProtectControlGroups=true    # /sys/fs/cgroup read-only
RestrictNamespaces=true      # Prevents creating new namespaces (except user)
LockPersonality=true         # Prevents changing ABI personality

# ─── Network restrictions ────────────────────────────────────────────────────
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX   # Only TCP/IP and Unix sockets
IPAddressDeny=any
IPAddressAllow=10.0.0.0/8 127.0.0.0/8              # Only internal and loopback

# ─── Memory security ─────────────────────────────────────────────────────────
MemoryDenyWriteExecute=true  # Prevents W+X mappings (mitigates shellcode injection)
RestrictRealtime=true        # Prevents real-time scheduling (DoS mitigation)
```

**Practical hardening profile for a Data Engineering ETL service:**
```ini
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/data/staging /var/log/etl
ProtectKernelTunables=true
ProtectKernelModules=true
CapabilityBoundingSet=
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
SystemCallFilter=@system-service
```

---

## §6 Production Unit Files for DE Tools

### Airflow Webserver

```ini
[Unit]
Description=Apache Airflow Webserver
After=network-online.target airflow-scheduler.service
Requires=airflow-scheduler.service

[Service]
Type=simple
User=airflow
Group=airflow
EnvironmentFile=/etc/airflow/environment
ExecStart=/opt/pyenvs/airflow/bin/airflow webserver --port 8080
Restart=on-failure
RestartSec=15s
TimeoutStopSec=30
LimitNOFILE=65536
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/opt/airflow /var/log/airflow
StandardOutput=journal
StandardError=journal
SyslogIdentifier=airflow-webserver

[Install]
WantedBy=multi-user.target
```

### Spark History Server

```ini
[Unit]
Description=Apache Spark History Server
After=network-online.target

[Service]
Type=forking
User=spark
Group=spark
EnvironmentFile=/etc/spark/environment
ExecStart=/opt/spark/sbin/start-history-server.sh
ExecStop=/opt/spark/sbin/stop-history-server.sh
PIDFile=/opt/spark/spark-history-server.pid
TimeoutStartSec=60
TimeoutStopSec=30
LimitNOFILE=65536
MemoryMax=2G
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## §7 systemd Timers — cron Replacement

Timers have logging, dependency management, and missed-run handling that cron lacks.

```ini
# /etc/systemd/system/etl-daily.service
[Unit]
Description=Daily ETL Pipeline
After=network-online.target postgresql.service

[Service]
Type=oneshot
User=airflow
EnvironmentFile=/etc/airflow/environment
ExecStart=/opt/etl/run_daily.sh
StandardOutput=journal
StandardError=journal
SyslogIdentifier=etl-daily
```

```ini
# /etc/systemd/system/etl-daily.timer
[Unit]
Description=Run daily ETL at 02:00 UTC
Requires=etl-daily.service

[Timer]
# Calendar spec: Mon..Fri 02:00 UTC
OnCalendar=Mon..Fri 02:00:00 UTC
# Randomize start within 5 min window to avoid thundering herd
RandomizedDelaySec=5min
# If system was down at scheduled time, run immediately on next boot
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
systemctl enable --now etl-daily.timer
systemctl list-timers --all                     # All timers with next/last trigger
systemctl status etl-daily.timer
journalctl -u etl-daily.service --since today   # Last run output
```

**Calendar spec reference:**

```
daily                → *-*-* 00:00:00
hourly               → *-*-* *:00:00
weekly               → Mon *-*-* 00:00:00
monthly              → *-*-01 00:00:00
Mon..Fri 08:00 UTC   → Business days at 8am UTC
*:0/15               → Every 15 minutes
2024-09-15 12:00:00  → Specific one-time date
```

---

## §8 Socket Activation

```ini
# /etc/systemd/system/etl-api.socket
[Unit]
Description=ETL API Socket

[Socket]
ListenStream=0.0.0.0:8090
Accept=no
SocketUser=airflow

[Install]
WantedBy=sockets.target
```

```ini
# /etc/systemd/system/etl-api.service
[Unit]
Requires=etl-api.socket

[Service]
ExecStart=/opt/etl/api_server.py
StandardInput=socket
```

---

## §9 Log Rotation and Management

```bash
# /etc/systemd/journald.conf (system-wide journal config)
# [Journal]
# SystemMaxUse=2G         # Max disk space for persistent journal
# RuntimeMaxUse=200M      # Max for /run/log/journal (RAM)
# MaxRetentionSec=30day   # Auto-delete entries older than 30 days
# Compress=yes            # Compress archived journal files

# Apply and restart journal
systemctl restart systemd-journald

# For file-based logs (non-journald services writing to /var/log/)
# /etc/logrotate.d/airflow
```

```
/var/log/airflow/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 airflow airflow
    postrotate
        systemctl kill --kill-who=main --signal=SIGUSR1 airflow-scheduler.service 2>/dev/null || true
    endscript
}
```

```bash
logrotate -d /etc/logrotate.d/airflow   # Dry-run test
logrotate -f /etc/logrotate.d/airflow   # Force rotate now
```
