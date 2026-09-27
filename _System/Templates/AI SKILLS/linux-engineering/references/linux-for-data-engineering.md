# Linux for Data Engineering

## Table of Contents
1. Server Initial Setup for DE Workloads
2. Python 3.12 with uv — Installation and Project Management
3. Apache Airflow on Linux — Systemd Deployment
4. Apache Spark on Linux — Standalone and YARN
5. Docker on Linux — Hardened Configuration
6. Data Transfer — rsync, rclone, scp Patterns
7. Large-File ETL Shell Patterns
8. Filesystem-Triggered Pipeline Execution
9. Pipeline Monitoring and Debugging One-Liners
10. Resource Tuning Reference for DE Workloads

---

## §1 Server Initial Setup for DE Workloads

```bash
# ─── Core dependencies ────────────────────────────────────────────────────────
# [Ubuntu 22.04 / 24.04]
apt update && apt install -y \
    curl wget git unzip build-essential \
    libssl-dev libffi-dev libpq-dev \
    python3-dev python3-pip \
    openjdk-21-jdk-headless \
    postgresql-client \
    nftables ufw fail2ban \
    sysstat iotop htop ncdu \
    inotify-tools parallel \
    jq yq                       # JSON/YAML CLI tools essential for pipeline scripts

# [RHEL 9 / Rocky 9]
dnf groupinstall "Development Tools" -y
dnf install -y \
    curl wget git unzip \
    openssl-devel libffi-devel postgresql-devel \
    python3-devel \
    java-21-openjdk-headless \
    postgresql \
    nftables firewalld fail2ban \
    sysstat iotop htop ncdu \
    inotify-tools parallel \
    jq

# ─── Java environment (required for Spark and Airflow Celery) ────────────────
# [Ubuntu]
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
# [RHEL]
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk

# Persist in /etc/profile.d/java.sh (login shells) AND /etc/environment (PAM sessions)
echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment
cat > /etc/profile.d/java.sh <<EOF
export JAVA_HOME=$JAVA_HOME
export PATH="\$JAVA_HOME/bin:\$PATH"
EOF

# ─── Filesystem layout ────────────────────────────────────────────────────────
install -d -m 755 -o root    -g root     /opt/pyenvs
install -d -m 755 -o root    -g root     /opt/spark
install -d -m 755 -o airflow -g airflow  /opt/airflow
install -d -m 750 -o airflow -g airflow  /etc/airflow
install -d -m 770 -o airflow -g airflow  /var/log/airflow
install -d -m 770 -o root    -g dataops  /data/raw
install -d -m 770 -o root    -g dataops  /data/processed
install -d -m 770 -o root    -g dataops  /data/staging
install -d -m 1777 -o root   -g root     /var/tmp/etl    # Sticky bit — each job owns its dir

# ─── Service accounts ─────────────────────────────────────────────────────────
useradd --system --no-create-home --shell /usr/sbin/nologin --home /opt/airflow airflow
useradd --system --no-create-home --shell /usr/sbin/nologin --home /opt/spark   spark
groupadd dataops
usermod -aG dataops airflow
usermod -aG docker  airflow      # If using DockerOperator
```

---

## §2 Python 3.12 with uv — Installation and Project Management

```bash
# ─── Install uv (the canonical Python toolchain for this stack) ───────────────
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or: pip install uv --break-system-packages  (avoid if possible)

# System-wide install for service accounts
curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin sh

# Verify
uv --version
uv python list               # Available Python versions

# ─── Project environment setup ────────────────────────────────────────────────
cd /opt/airflow
uv init --python 3.12        # Creates pyproject.toml, .python-version

# Add dependencies
uv add apache-airflow[celery,postgres,redis]==2.9.3
uv add pandas polars pyarrow sqlalchemy psycopg2-binary
uv add great-expectations pandera
uv add xgboost lightgbm catboost
uv add plotly seaborn

# Pin for reproducibility
uv lock                      # Creates uv.lock (commit to git)
uv sync                      # Install from lock file (CI/CD pattern)

# ─── Dedicated virtual env for each service ───────────────────────────────────
# Create env at a fixed path (systemd ExecStart= references this directly)
uv venv /opt/pyenvs/airflow --python 3.12
source /opt/pyenvs/airflow/bin/activate
uv pip install -r requirements.txt
# In systemd unit: ExecStart=/opt/pyenvs/airflow/bin/airflow scheduler

# ─── uv in scripts (no activation needed) ────────────────────────────────────
#!/usr/bin/env -S uv run --python 3.12
# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas", "psycopg2-binary"]
# ///
import pandas as pd
# uv run ./script.py  — creates ephemeral env, runs, exits
```

---

## §3 Apache Airflow on Linux — Systemd Deployment

### Environment File

```bash
# /etc/airflow/environment  (mode 640, root:airflow)
install -m 640 -o root -g airflow /dev/null /etc/airflow/environment
cat > /etc/airflow/environment <<'EOF'
AIRFLOW_HOME=/opt/airflow
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
AIRFLOW__CORE__FERNET_KEY=<generated_fernet_key>
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:<password>@localhost:5432/airflow
AIRFLOW__CELERY__BROKER_URL=redis://localhost:6379/0
AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:<password>@localhost:5432/airflow
AIRFLOW__WEBSERVER__SECRET_KEY=<random_secret>
AIRFLOW__LOGGING__BASE_LOG_FOLDER=/var/log/airflow
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
EOF
chmod 640 /etc/airflow/environment
```

### Database Initialization

```bash
sudo -u airflow /opt/pyenvs/airflow/bin/airflow db migrate
sudo -u airflow /opt/pyenvs/airflow/bin/airflow users create \
    --username admin --firstname Admin --lastname User \
    --role Admin --email admin@company.com --password "$(openssl rand -base64 24)"
```

### Systemd Units

```ini
# /etc/systemd/system/airflow-scheduler.service
[Unit]
Description=Airflow Scheduler
After=network-online.target postgresql.service redis.service
Requires=postgresql.service

[Service]
Type=simple
User=airflow
Group=airflow
EnvironmentFile=/etc/airflow/environment
WorkingDirectory=/opt/airflow
ExecStart=/opt/pyenvs/airflow/bin/airflow scheduler
Restart=on-failure
RestartSec=10s
TimeoutStopSec=60
LimitNOFILE=65536
MemoryMax=4G
MemorySwapMax=0
OOMScoreAdjust=-900
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/opt/airflow /var/log/airflow /data
StandardOutput=journal
StandardError=journal
SyslogIdentifier=airflow-scheduler

[Install]
WantedBy=multi-user.target
```

```bash
# Deploy all Airflow units and enable
for unit in airflow-scheduler airflow-webserver airflow-worker airflow-flower; do
    systemctl daemon-reload
    systemctl enable --now "$unit"
    systemctl status "$unit" --no-pager -l
done

# Health checks
sudo -u airflow /opt/pyenvs/airflow/bin/airflow jobs check
sudo -u airflow /opt/pyenvs/airflow/bin/airflow dags list
```

---

## §4 Apache Spark on Linux — Standalone Cluster

```bash
# ─── Installation ─────────────────────────────────────────────────────────────
SPARK_VERSION="3.5.1"
HADOOP_VERSION="3"
curl -O "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"
tar xzf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" -C /opt/spark/ --strip-components=1
chown -R spark:spark /opt/spark
ln -sfn /opt/spark /opt/spark/current    # Version-agnostic symlink

# ─── Environment ──────────────────────────────────────────────────────────────
# /etc/spark/environment (640, root:spark)
cat > /etc/spark/environment <<EOF
SPARK_HOME=/opt/spark
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
SPARK_MASTER_HOST=10.0.0.11
SPARK_WORKER_MEMORY=6g
SPARK_WORKER_CORES=4
SPARK_DAEMON_MEMORY=1g
SPARK_LOG_DIR=/var/log/spark
SPARK_PID_DIR=/run/spark
EOF

# ─── spark-defaults.conf ──────────────────────────────────────────────────────
cat > /opt/spark/conf/spark-defaults.conf <<'EOF'
spark.master                  spark://10.0.0.11:7077
spark.eventLog.enabled        true
spark.eventLog.dir            /data/spark-events
spark.history.fs.logDirectory /data/spark-events

# Memory tuning for Pandas-heavy workloads
spark.executor.memory         4g
spark.executor.memoryOverhead 1g
spark.driver.memory           2g
spark.sql.adaptive.enabled    true
spark.sql.adaptive.coalescePartitions.enabled true

# Parquet optimizations
spark.sql.parquet.compression.codec  snappy
spark.sql.parquet.filterPushdown     true
EOF

# ─── Resource allocation via cgroups (systemd unit) ──────────────────────────
# MemoryMax and CPUQuota in the unit file constrain the entire Spark JVM process tree
# This is the correct mechanism for Spark on Linux — not YARN on standalone clusters
```

---

## §5 Docker on Linux — Hardened Configuration

```bash
# ─── Installation ─────────────────────────────────────────────────────────────
# [Ubuntu]
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | gpg --dearmor -o /usr/share/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
    | tee /etc/apt/sources.list.d/docker.list
apt update && apt install docker-ce docker-ce-cli containerd.io -y

# [RHEL/Rocky]
dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
dnf install docker-ce docker-ce-cli containerd.io -y

# ─── /etc/docker/daemon.json — hardened configuration ────────────────────────
cat > /etc/docker/daemon.json <<'EOF'
{
  "log-driver": "journald",
  "log-opts": {
    "tag": "docker/{{.Name}}"
  },
  "storage-driver": "overlay2",
  "live-restore": true,
  "userland-proxy": false,
  "no-new-privileges": true,
  "icc": false,
  "default-ulimits": {
    "nofile": { "Name": "nofile", "Soft": 65536, "Hard": 65536 }
  },
  "max-concurrent-downloads": 4,
  "max-concurrent-uploads": 2
}
EOF
systemctl enable --now docker
systemctl daemon-reload && systemctl restart docker

# ─── cgroups v2 verification ─────────────────────────────────────────────────
# Docker on cgroups v2 is the default on Ubuntu 22.04+ and RHEL 9
# Verify: stat -fc %T /sys/fs/cgroup/  → output should be "cgroup2fs"
docker info | grep -i "cgroup\|cgroupdriver"

# ─── Rootless Docker for non-privileged DE environments ──────────────────────
# Run Docker daemon as the airflow user (no root required for image pulls)
# [Ubuntu] apt install uidmap
dockerd-rootless-setuptool.sh install --force
systemctl --user enable --now docker
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
```

---

## §6 Data Transfer — rsync, rclone, scp Patterns

### rsync — Local and Remote File Sync

```bash
# ─── Standard sync patterns ───────────────────────────────────────────────────
rsync -avz \
    --checksum \               # Verify by content hash, not just size+mtime
    --delete \                 # Remove files at destination not in source
    --exclude="*.tmp" \
    --exclude=".DS_Store" \
    --bwlimit=50000 \          # Bandwidth limit in KB/s (50 MB/s)
    --log-file=/var/log/rsync/transfer.log \
    /data/processed/ \
    airflow@10.0.0.13:/data/incoming/

# ─── Incremental backup with hardlinks (space-efficient history) ─────────────
BACKUP_DATE=$(date +%Y%m%d-%H%M%S)
rsync -avz --delete \
    --link-dest=/backup/$(ls /backup | tail -1) \   # Link unchanged files from last backup
    /data/raw/ \
    /backup/$BACKUP_DATE/

# ─── Parallel rsync with xargs for large directory trees ──────────────────────
find /data/raw/ -maxdepth 1 -type d | \
    xargs -P 4 -I {} rsync -avz --relative {} airflow@backup-host:/data/raw/
```

### rclone — Cloud Storage Operations

```bash
# Configure (interactive — run once per remote)
rclone config    # Creates /etc/rclone/rclone.conf or ~/.config/rclone/rclone.conf

# /etc/rclone/rclone.conf (for system service use — mode 640, root:airflow)
# [s3-prod]
# type = s3
# provider = AWS
# env_auth = true       ← Use IAM instance profile (no keys in config)
# region = us-east-1
# server_side_encryption = aws:kms

# ─── Transfer operations ──────────────────────────────────────────────────────
# Upload processed data to S3 (copy: no delete at destination)
rclone copy /data/processed/ s3-prod:my-bucket/processed/ \
    --transfers 8 --checkers 16 \
    --s3-upload-concurrency 8 \
    --bwlimit 100M \
    --stats 30s --stats-log-level NOTICE \
    --log-file /var/log/rclone/upload.log

# Sync (mirror: deletes at destination what's removed from source)
rclone sync /data/processed/ s3-prod:my-bucket/processed/ \
    --backup-dir s3-prod:my-bucket-archive/$(date +%Y%m%d)/ \
    --exclude "*.tmp" --exclude ".airflowignore"

# Download — pull data into landing zone
rclone copy s3-prod:source-bucket/daily/$(date +%Y/%m/%d)/ \
    /data/raw/$(date +%Y%m%d)/ \
    --transfers 16 --progress

# Mount S3 as filesystem (experimental — not for high-throughput ETL)
rclone mount s3-prod:my-bucket /mnt/s3 \
    --vfs-cache-mode writes \
    --daemon

# Bisync — two-way sync (e.g., between two cloud providers)
rclone bisync s3-prod:bucket-a gcs-prod:bucket-b --resync --checksum
```

---

## §7 Large-File ETL Shell Patterns

```bash
# ─── Split a large CSV for parallel processing ─────────────────────────────────
HEADER=$(head -1 /data/raw/large.csv)
TOTAL_ROWS=$(tail -n +2 /data/raw/large.csv | wc -l)
CHUNK_SIZE=500000

tail -n +2 /data/raw/large.csv | \
    split -l $CHUNK_SIZE - /var/tmp/etl/chunk_ \
    --filter='{ printf "%s\n" "$HEADER"; cat; } > /var/tmp/etl/$FILE.csv'

# Process chunks in parallel
find /var/tmp/etl/ -name "chunk_*.csv" | \
    parallel --jobs 8 --joblog /var/log/etl/parallel.log \
             "python3 /opt/etl/process_chunk.py {}"

# ─── Memory-bounded sort for files exceeding RAM ──────────────────────────────
sort \
    --parallel=8 \           # Use 8 CPU cores
    -S 4G \                  # Use max 4 GB RAM (spills to disk if larger)
    -T /var/tmp/etl/ \       # Temp directory on fast disk
    -t',' -k3,3n \           # Sort by column 3 numerically
    /data/raw/large.csv > /data/processed/sorted.csv

# ─── tmpfs RAM disk for high-speed intermediate staging ───────────────────────
# Mount in /etc/fstab for persistence
# tmpfs /dev/shm tmpfs defaults,size=8G 0 0
# (already mounted; adjust size via /etc/fstab or remount)
mount -o remount,size=8G /dev/shm     # Resize at runtime

# Use for hot intermediates
cp /data/raw/lookup_table.parquet /dev/shm/
python3 etl.py --lookup /dev/shm/lookup_table.parquet   # RAM-speed access
rm /dev/shm/lookup_table.parquet                         # Explicit cleanup

# ─── Checksum verification for pipeline data integrity ────────────────────────
# Generate checksums after landing
find /data/raw/$(date +%Y%m%d)/ -name "*.parquet" \
    -exec sha256sum {} + > /data/raw/$(date +%Y%m%d)/checksums.sha256

# Verify before processing
sha256sum --check /data/raw/$(date +%Y%m%d)/checksums.sha256 || {
    echo "CHECKSUM MISMATCH — aborting pipeline" >&2
    exit 1
}
```

---

## §8 Filesystem-Triggered Pipeline Execution

```bash
# ─── inotifywait watcher service ──────────────────────────────────────────────
# /etc/systemd/system/landing-watcher.service
```

```ini
[Unit]
Description=Data Landing Zone File Watcher
After=network-online.target

[Service]
Type=simple
User=airflow
Group=airflow
EnvironmentFile=/etc/airflow/environment
ExecStart=/opt/etl/bin/landing_watcher.sh
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=landing-watcher

[Install]
WantedBy=multi-user.target
```

```bash
# /opt/etl/bin/landing_watcher.sh
#!/usr/bin/env bash
set -euo pipefail

WATCH_DIR="/data/raw/landing"
LOG_PREFIX="$(date -Iseconds) [landing-watcher]"

echo "$LOG_PREFIX Watching: $WATCH_DIR"

inotifywait \
    --monitor \                              # Keep watching (don't exit after first event)
    --recursive \
    --event close_write \                    # File finished being written
    --event moved_to \                       # File moved into watched dir
    --format '%w%f' \                        # Full path of changed file
    "$WATCH_DIR" | \
while IFS= read -r filepath; do
    # Validate file type before triggering
    case "$filepath" in
        *.csv|*.parquet|*.jsonl)  ;;
        *) echo "$LOG_PREFIX Skipping non-data file: $filepath"; continue ;;
    esac

    echo "$LOG_PREFIX New file: $filepath"

    # Trigger Airflow DAG via CLI (non-blocking)
    airflow dags trigger ingest_landing_file \
        --conf "{\"file_path\": \"$filepath\"}" &
done
```

---

## §9 Pipeline Monitoring and Debugging One-Liners

```bash
# ─── Airflow ─────────────────────────────────────────────────────────────────
# Running task instances
airflow tasks states-for-dag-run dag_id run_id

# Find failed tasks in the last 24h
airflow tasks list dag_id --tree
psql "$AIRFLOW__DATABASE__SQL_ALCHEMY_CONN" -c \
    "SELECT dag_id, task_id, state, start_date, end_date FROM task_instance
     WHERE state='failed' AND start_date > NOW() - INTERVAL '24 hours'
     ORDER BY start_date DESC;"

# ─── Process monitoring ───────────────────────────────────────────────────────
# All Airflow processes and their CPU/memory
ps -eo pid,ppid,cmd,%cpu,%mem,etime | grep -E "[a]irflow|[s]park" | sort -k4 -rn

# Watch file descriptor growth of scheduler (leak detection)
watch -n 5 "ls /proc/\$(pgrep -f 'airflow scheduler')/fd | wc -l"

# Memory pressure every 10 seconds
watch -n 10 "free -h; echo '---'; vmstat 1 2 | tail -1"

# ─── Spark ───────────────────────────────────────────────────────────────────
# Spark processes and their allocated memory
ps -eo pid,cmd,%mem,rss | grep -E "[s]park" | awk '{print $1, $NF/1024 "MB", $0}'

# Stale Spark worker processes (not registered with master)
diff <(curl -s http://localhost:8080/api/v1/applications | jq '.[].id' -r) \
     <(ps -eo cmd | grep "SparkSubmit" | awk '{print $NF}')

# ─── Disk space ──────────────────────────────────────────────────────────────
# Alert if any data partition exceeds 80%
df -h | awk 'NR>1 && /data|airflow|spark/ {
    gsub(/%/,"",$5); if($5+0 > 80) print "WARNING:", $6, "at", $5"%"}'

# Find and clean Spark shuffle files from crashed jobs
find /var/tmp/spark/ -name "shuffle_*.index" -mtime +1 -delete

# ─── Log tailing with color ───────────────────────────────────────────────────
journalctl -f -u airflow-scheduler | \
    GREP_COLOR='1;31' grep --color=always -E "ERROR|CRITICAL|$"

# Count errors per minute from Airflow scheduler
journalctl -u airflow-scheduler --since "1 hour ago" -o cat | \
    grep ERROR | \
    awk '{print substr($1,1,16)}' | \   # Truncate to minute resolution
    sort | uniq -c | sort -k2
```

---

## §10 Resource Tuning Reference for DE Workloads

```bash
# /etc/sysctl.d/99-de-tuning.conf
```

```ini
# ─── Virtual memory ──────────────────────────────────────────────────────────
vm.swappiness = 10                  # Prefer RAM; only swap under extreme pressure
vm.dirty_ratio = 20                 # % of RAM that can be dirty before sync
vm.dirty_background_ratio = 5      # % at which background writeback starts
vm.overcommit_memory = 0            # Heuristic overcommit (safe for Spark/Pandas)

# ─── File system ─────────────────────────────────────────────────────────────
fs.file-max = 2097152               # System-wide FD limit
fs.inotify.max_user_watches = 524288  # Required for inotifywait on large trees
fs.inotify.max_user_instances = 512

# ─── Network ─────────────────────────────────────────────────────────────────
net.core.somaxconn = 65535          # Backlog queue for incoming connections
net.core.netdev_max_backlog = 16384
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_syncookies = 1
net.ipv4.ip_local_port_range = 1024 65535  # Wider ephemeral port range for rclone/S3

# ─── Huge pages for JVM (Spark) ──────────────────────────────────────────────
# Transparent Huge Pages: disable for predictable JVM latency
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
# Persist via rc.local or systemd unit with ExecStart=

# ─── Per-limits file for DE service accounts ─────────────────────────────────
# /etc/security/limits.d/99-de-services.conf
# airflow soft nofile 65536
# airflow hard nofile 65536
# airflow soft nproc  8192
# airflow hard nproc  8192
# spark   soft nofile 65536
# spark   hard nofile 65536
# spark   soft memlock unlimited
# spark   hard memlock unlimited
```

```bash
# Apply sysctl without reboot
sysctl --system

# Verify specific values
sysctl fs.file-max vm.swappiness net.core.somaxconn
```
