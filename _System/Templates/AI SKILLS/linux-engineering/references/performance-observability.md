# Linux Performance and Observability

## Table of Contents
1. The USE Method — Analytical Framework
2. CPU Analysis
3. Memory Analysis
4. Disk I/O Analysis
5. Network I/O Analysis
6. Process-Level Tracing — strace and lsof
7. perf — CPU Profiling and Flame Graphs
8. eBPF via BCC and bpftrace
9. Log Mining with grep/awk/sed
10. Observability Toolkit Quick Reference

---

## §1 The USE Method — Analytical Framework

Developed by Brendan Gregg. For every resource (CPU, memory, disk, network, file descriptors), measure three metrics:

| Metric | Definition | Signal |
|---|---|---|
| **U**tilization | % of time resource is busy | High sustained utilization → saturation approaching |
| **S**aturation | Queue depth or wait time when resource is overloaded | Non-zero saturation → performance impact |
| **E**rrors | Error events on the resource | Any non-zero rate requires investigation |

**Resource checklist for DE workloads:**

| Resource | Utilization Tool | Saturation Tool | Errors Tool |
|---|---|---|---|
| CPU | `mpstat`, `top` | `vmstat r` column | `perf stat` |
| Memory | `free`, `/proc/meminfo` | `vmstat si/so` (swap) | `dmesg` OOM events |
| Disk I/O | `iostat %util` | `iostat await`, `iotop` | `smartctl`, `dmesg` |
| Network | `sar -n DEV` | `ss` backlog, `netstat` drops | `ip -s link` errors |
| File Descriptors | `/proc/sys/fs/file-nr` | `ulimit -n` vs. usage | `dmesg` EMFILE |

---

## §2 CPU Analysis

```bash
# ─── Instantaneous CPU state ─────────────────────────────────────────────────
top -b -n 1               # Snapshot mode (scriptable)
htop                      # Interactive, per-core bars, process tree
btop                      # Modern TUI with GPU support

# ─── Per-CPU utilization (mpstat) ────────────────────────────────────────────
mpstat -P ALL 2 5         # All CPUs, 2-second intervals, 5 samples
# Key columns: %usr %sys %iowait %steal %idle
# iowait > 20%: process blocked on I/O → disk bottleneck
# steal  > 5%:  hypervisor stealing CPU → noisy neighbor on VM

# ─── Load average interpretation ─────────────────────────────────────────────
# /proc/loadavg: 1min 5min 15min
# On N-core system: load > N means saturation (processes waiting for CPU)
nproc                           # Core count
uptime                          # Load averages
awk '{ print $1/'"$(nproc)"'*100 "% CPU load" }' /proc/loadavg  # % of capacity

# ─── vmstat — system-wide snapshot ───────────────────────────────────────────
vmstat 2 10               # 2-second intervals, 10 samples
# Key columns:
# r:  processes in run queue (waiting for CPU) — saturation indicator
# b:  processes in uninterruptible sleep (D state) — I/O wait
# si/so: swap-in/swap-out (non-zero = severe memory pressure)
# us/sy/id/wa/st: user/system/idle/iowait/stolen

# ─── sar — historical CPU (sysstat suite) ────────────────────────────────────
# [Ubuntu] apt install sysstat && systemctl enable --now sysstat
# [RHEL]   dnf install sysstat && systemctl enable --now sysstat
sar -u 2 10               # CPU utilization at 2s intervals
sar -u -f /var/log/sysstat/sa$(date +%d)  # Today's historical data
sar -u -s 08:00:00 -e 10:00:00            # Narrow time window

# ─── Per-process CPU ─────────────────────────────────────────────────────────
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head -20
pidstat -u 2 5            # Per-process CPU at intervals (from sysstat)
```

---

## §3 Memory Analysis

```bash
# ─── System memory overview ──────────────────────────────────────────────────
free -h                   # Human-readable; use 'available' column NOT 'free'
cat /proc/meminfo         # Full breakdown (see §process-filesystem-memory §1)

# ─── Per-process memory ──────────────────────────────────────────────────────
ps -eo pid,cmd,%mem,rss --sort=-%mem | head -20
# RSS = Resident Set Size in KB — pages currently in physical RAM

# smem — accurate shared memory accounting
# apt install smem / dnf install smem
smem -s rss -r -t | head -20    # Sorted by RSS, totals at bottom
smem -P airflow -r               # Filter processes matching "airflow"

# ─── Swap activity ───────────────────────────────────────────────────────────
vmstat 2 | awk '{print $7, $8}'  # si (swap-in) so (swap-out) columns
# Non-zero si/so = system is actively swapping → severe performance impact

# ─── Page cache and memory pressure ─────────────────────────────────────────
# Dropping cache (ONLY on dev/testing — never production during pipeline run)
sync && echo 3 > /proc/sys/vm/drop_caches

# ─── OOM monitoring ──────────────────────────────────────────────────────────
dmesg --level=err,warn | grep -i "out of memory\|oom\|killed process"
journalctl -k --since "1 hour ago" | grep -i oom

# ─── Process memory maps ─────────────────────────────────────────────────────
PID=$(pgrep -f "airflow scheduler")
cat /proc/$PID/status | grep -E "^Vm|^Rss|^Threads"
# VmPeak: peak virtual memory used
# VmRSS:  current resident set size (physical RAM)
# VmSwap: memory swapped out

# pmap — address space breakdown
pmap -x $PID | sort -rn -k3 | head -20   # Sort by RSS descending
```

---

## §4 Disk I/O Analysis

```bash
# ─── iostat — block device utilization ───────────────────────────────────────
iostat -xz 2 10
# Key columns:
# %util:   % of time device was busy (100% = saturation)
# await:   average I/O wait time in ms (>20ms for SSD is concerning)
# r/s w/s: read/write operations per second (IOPS)
# rkB/s wkB/s: read/write throughput KB/s

# ─── iotop — per-process I/O ─────────────────────────────────────────────────
iotop -o -d 2             # -o: only processes with active I/O; -d: interval
iotop -b -n 5 -o          # Batch mode (scriptable)

# ─── Disk space ──────────────────────────────────────────────────────────────
df -h                     # Filesystem usage (filesystem-level)
df -i                     # Inode usage — a full inode table blocks writes even with free space

# ncdu — interactive disk usage explorer
# apt install ncdu / dnf install ncdu
ncdu /data/               # Navigate to find large files/dirs

# du alternatives
du -sh /data/* | sort -rh | head -20   # Largest items in /data/
du -sh --exclude=proc /var/log/*  | sort -rh

# ─── Disk health ─────────────────────────────────────────────────────────────
# apt install smartmontools / dnf install smartmontools
smartctl -a /dev/sda                          # SMART data and health
smartctl -t short /dev/sda && sleep 120 && smartctl -l selftest /dev/sda

# ─── Block device and filesystem info ────────────────────────────────────────
lsblk -f                  # Devices with filesystem type, UUID, mount points
blkid                     # Block device UUIDs and filesystem types
findmnt --real            # Active mount table with options
```

---

## §5 Network I/O Analysis

```bash
# ─── Interface statistics ────────────────────────────────────────────────────
ip -s link show ens3      # TX/RX bytes, errors, drops per interface
sar -n DEV 2 10           # Network throughput at intervals
# Key: rxkB/s txkB/s — compare against interface capacity

# ─── Per-process network ─────────────────────────────────────────────────────
# nethogs — per-process bandwidth (apt/dnf install nethogs)
nethogs ens3

# iftop — per-connection bandwidth (apt/dnf install iftop)
iftop -i ens3 -n          # -n: no DNS resolution

# ─── Connection state analysis ───────────────────────────────────────────────
# Large TIME_WAIT count: port exhaustion risk (heavy HTTP to external APIs)
ss -tn | awk 'NR>1 {print $1}' | sort | uniq -c
# Large CLOSE_WAIT count: application not closing connections (connection leak)

# Retransmission rate — high rate indicates network congestion or packet loss
ss -tin | grep retrans
cat /proc/net/snmp | grep -i "retranssegs\|outsegs"
```

---

## §6 Process-Level Tracing — strace and lsof

### strace — System Call Tracer

```bash
# Attach to a running process — diagnose a stall without restart
strace -p $PID                          # Trace all syscalls in real time
strace -p $PID -e trace=read,write,open,close,stat  # Filter to file syscalls
strace -p $PID -e trace=network         # Network syscalls only

# Measure time per syscall — identify where a process spends time
strace -p $PID -T -tt 2>&1 | head -50
# -T: show time spent in each syscall
# -tt: print wall-clock timestamp (microsecond precision)

# Trace a subprocess from launch
strace -f python3 /opt/etl/ingest.py \  # -f: follow forked children
    -o /tmp/strace.out \                 # Write to file (avoids terminal flood)
    -e trace=openat,read,write,connect
cat /tmp/strace.out | awk -F'"' '/openat/{print $2}' | sort -u  # Files opened

# Diagnose "hanging" job: strace shows WHICH syscall it's blocked in
strace -p $PID 2>&1 | head -5
# Common patterns:
# futex(..., FUTEX_WAIT...) — waiting for a lock (GIL, threading.Lock)
# epoll_wait(...)           — waiting for I/O event (normal for async server)
# read(5, ...)              — blocked reading from fd 5 → check /proc/$PID/fd/5
# connect(...)              — blocked on TCP connect → network/firewall issue
```

### lsof — List Open Files

```bash
# All open files for a process
lsof -p $PID
lsof -p $PID -n -P               # -n: no hostname resolution, -P: no port name resolution

# Which process has a file open?
lsof /data/raw/batch.parquet

# All network connections for a process
lsof -p $PID -i

# All processes with open connections to PostgreSQL port
lsof -i :5432 -n -P

# Files preventing unmount (busy filesystem)
lsof +D /data/raw/

# Deleted files still held open (consuming disk space invisibly)
lsof | grep "(deleted)"
# Fix: identify PID, restart process to release the fd
```

---

## §7 perf — CPU Profiling and Flame Graphs

```bash
# [Ubuntu] apt install linux-perf / linux-tools-$(uname -r)
# [RHEL]   dnf install perf

# ─── perf stat — hardware counter summary ────────────────────────────────────
perf stat python3 /opt/etl/transform.py
# Key metrics: cache-misses, branch-misses, instructions per cycle (IPC)
# Low IPC (<1.0): memory-bound workload — consider columnar formats (Parquet)

# ─── perf record — CPU sampling (flame graph data collection) ────────────────
# Sample a running process at 99Hz for 30 seconds
perf record -F 99 -p $PID -g --call-graph dwarf -- sleep 30
# -F 99: 99Hz (avoid exactly 100Hz — avoids lockstep with 100Hz timer)
# -g: capture call graphs (stack traces)
# --call-graph dwarf: most accurate for Python/JVM (better than fp)

# ─── Flame Graph generation ──────────────────────────────────────────────────
# apt install git / clone brendangregg/FlameGraph
git clone --depth=1 https://github.com/brendangregg/FlameGraph.git /opt/FlameGraph

perf script > /tmp/perf.script
/opt/FlameGraph/stackcollapse-perf.pl /tmp/perf.script | \
    /opt/FlameGraph/flamegraph.pl \
        --title "Airflow Scheduler — $(date +%Y%m%d)" \
        --width 1600 > /tmp/flamegraph.svg

# Open in browser (X11 or copy to dev machine)
python3 -m http.server 8888 --directory /tmp &

# ─── perf top — live CPU hot functions ───────────────────────────────────────
perf top -p $PID                        # Per-function CPU % in real time
```

---

## §8 eBPF via BCC and bpftrace

eBPF programs run in the kernel for zero-overhead, production-safe tracing. BCC provides Python bindings. bpftrace provides a high-level scripting language for one-liners.

```bash
# [Ubuntu]  apt install bpfcc-tools python3-bpfcc bpftrace
# [RHEL]    dnf install bcc bcc-tools bpftrace
# Requires kernel >= 4.9 (use 5.x+ for full feature set)

# ─── BCC — pre-built tools ───────────────────────────────────────────────────

# execsnoop: trace every new process execution
/usr/share/bcc/tools/execsnoop -T
# Use case: find what Airflow BashOperator is actually running

# opensnoop: trace every file open() call system-wide
/usr/share/bcc/tools/opensnoop -p $PID
# Use case: find what config/data files a pipeline is reading

# tcpconnect: trace TCP connection attempts
/usr/share/bcc/tools/tcpconnect -p $PID
# Use case: verify pipeline is connecting to correct DB host/port

# biolatency: block I/O latency histogram
/usr/share/bcc/tools/biolatency -m 10    # 10-second latency histogram in ms
# Use case: diagnose slow disk affecting Parquet read/write

# ext4slower: trace slow ext4 operations (> threshold ms)
/usr/share/bcc/tools/ext4slower 10       # Operations taking > 10ms
# Use case: identify I/O bottleneck in file-based ETL pipelines

# pythoncalls: trace Python function calls (requires Python usdt probes)
/usr/share/bcc/tools/pythoncalls -p $PID 10

# ─── bpftrace — one-liners ────────────────────────────────────────────────────

# Count syscalls by name for a specific process
bpftrace -e "tracepoint:syscalls:sys_enter_* /pid == $PID/ { @[probe] = count(); }"

# Trace file opens by filename pattern for a process
bpftrace -e 'tracepoint:syscalls:sys_enter_openat /pid == '"$PID"'/ { printf("%s\n", str(args->filename)); }'

# Block I/O latency histogram (all processes)
bpftrace -e 'tracepoint:block:block_rq_issue { @start[args->dev, args->sector] = nsecs; }
             tracepoint:block:block_rq_complete /@start[args->dev, args->sector]/
             { @latency_us = hist((nsecs - @start[args->dev, args->sector]) / 1000);
               delete(@start[args->dev, args->sector]); }'

# Count outbound TCP connections by destination port (pipeline external calls)
bpftrace -e 'kprobe:tcp_connect { @[((struct sock*)arg0)->__sk_common.skc_dport] = count(); }'

# Python GC pause time distribution
bpftrace -e 'usdt:/usr/bin/python3:gc__start { @start[tid] = nsecs; }
             usdt:/usr/bin/python3:gc__done  { @gc_us = hist((nsecs - @start[tid])/1000); }'

# Trace all network I/O bytes per process
bpftrace -e 'kprobe:tcp_sendmsg { @sent_bytes[comm] = sum(arg2); }
             kprobe:tcp_recvmsg { @recv_bytes[comm] = sum(arg2); }' -c "sleep 10"
```

---

## §9 Log Mining with grep/awk/sed

```bash
# ─── grep patterns for pipeline monitoring ────────────────────────────────────
# Count errors in Airflow logs
grep -c "ERROR" /var/log/airflow/scheduler.log

# Extract ERROR lines with timestamps
grep "ERROR" /var/log/airflow/scheduler.log | \
    grep -oP '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*' | tail -50

# Find log entries from last N minutes
find /var/log/airflow/ -newer /tmp/timestamp_ref -name "*.log" \
    -exec grep "ERROR" {} + 2>/dev/null

# ─── awk for structured log parsing ──────────────────────────────────────────
# Extract and count HTTP status codes from access log
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -rn

# Sum bytes transferred per hour
awk '{split($4, t, ":"); print t[2], $10}' /var/log/nginx/access.log | \
    awk '{sum[$1]+=$2} END {for(h in sum) print h, sum[h]/1024/1024 "MB"}' | sort -n

# Parse Airflow task duration from structured logs
grep "Task exited" /var/log/airflow/dag_processor.log | \
    awk -F'duration=' '{print $2}' | \
    awk '{sum+=$1; count++} END {printf "Avg: %.2fs Total: %.0f\n", sum/count, sum}'

# ─── sed for log transformation and cleanup ───────────────────────────────────
# Remove ANSI color codes from logs (Airflow/Spark colored output)
sed 's/\x1b\[[0-9;]*m//g' /var/log/airflow/task.log > /tmp/clean.log

# Replace timestamps for comparison (normalize)
sed 's/[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} [0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}/TIMESTAMP/g'

# Extract structured fields
sed -n 's/.*dag_id=\([^ ]*\).*/\1/p' /var/log/airflow/scheduler.log | sort | uniq -c
```

---

## §10 Observability Toolkit Quick Reference

| Scenario | First Tool | Deep Dive Tool |
|---|---|---|
| High CPU — which process? | `htop`, `top` | `perf top -p $PID` |
| High CPU — which function? | `perf top -p $PID` | `perf record` + flame graph |
| High I/O wait | `iostat -xz 2` | `iotop -o`, `biolatency` (BCC) |
| Memory pressure | `free -h`, `vmstat` si/so | `smem`, `/proc/$PID/smaps` |
| OOM kill | `dmesg | grep oom` | `journalctl -k`, `oom_score` |
| Network bottleneck | `sar -n DEV 2` | `iftop`, `nethogs` |
| Hanging/stalled process | `strace -p $PID` | `lsof -p $PID`, `bpftrace` |
| FD exhaustion | `ls /proc/$PID/fd \| wc -l` | `lsof -p $PID \| wc -l` |
| Slow disk | `iostat await` | `ext4slower 10` (BCC) |
| New process spawned? | `execsnoop` (BCC) | `strace -f -e trace=execve` |
| File access audit | `opensnoop -p $PID` (BCC) | `strace -e trace=openat -p $PID` |
| TCP connection trace | `tcpconnect` (BCC) | `tcpdump -i any -n port $PORT` |
| Historical CPU/disk | `sar -u / sar -d` | `/var/log/sysstat/sa*` |
| Spark/Airflow GC | JVM GC logs | `bpftrace` usdt python probes |
| Pipeline bottleneck | flame graph | USE method checklist |
