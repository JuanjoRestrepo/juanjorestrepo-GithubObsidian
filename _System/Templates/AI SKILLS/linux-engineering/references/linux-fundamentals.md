# Linux Fundamentals

## Table of Contents
1. Linux Architecture Model
2. Filesystem Hierarchy Standard (FHS)
3. File Types
4. Permission Model
5. Inodes and Links
6. Process Model
7. User and Group Model
8. Package Management — Dual Track
9. Environment Variables and Profile Load Order

---

## §1 Linux Architecture Model

```
[ User Applications: Python, Airflow, Spark, bash ]
[ Standard Library: glibc — wraps syscalls into C functions ]
[ System Call Interface: read/write/fork/exec/mmap/socket ]
[ Kernel Subsystems ]
  ├── Process Scheduler (CFS — Completely Fair Scheduler)
  ├── Virtual File System (VFS — unified interface over ext4/xfs/tmpfs/proc)
  ├── Memory Manager (paging, slab allocator, OOM killer)
  ├── Network Stack (TCP/IP, netfilter/nftables, sockets)
  └── Device Drivers (block, character, network)
[ Hardware: CPU, RAM, Disk, NIC ]
```

The shell is a userspace process that forks child processes for each command. It communicates with the kernel exclusively through glibc's syscall wrappers. This matters for Data Engineering: every `subprocess.run()` call in Python, every Airflow BashOperator, and every `os.fork()` goes through this stack — understanding it is prerequisite to debugging stalls, OOM kills, and permission errors.

---

## §2 Filesystem Hierarchy Standard (FHS)

```
/                   Root — everything hangs here
├── bin → usr/bin   User binaries (symlinked in modern distros)
├── sbin → usr/sbin System binaries
├── lib → usr/lib   Libraries
├── usr/            Secondary hierarchy (most software installs here)
│   ├── bin/        User commands
│   ├── lib/        Libraries and Python site-packages
│   ├── local/      Locally compiled software (higher PATH priority)
│   └── share/      Architecture-independent data
├── etc/            System configuration (text files only, version-controlled)
├── var/            Variable data — changes at runtime
│   ├── log/        System and application logs
│   ├── lib/        Persistent state (dpkg, dnf, airflow DB if SQLite)
│   ├── run/ → /run Runtime PIDs and sockets
│   └── spool/      Mail, print, cron queues
├── run/            Runtime data (tmpfs, cleared on reboot)
├── proc/           Virtual FS: kernel process and system info (see §process-filesystem-memory)
├── sys/            Virtual FS: kernel hardware/driver objects
├── dev/            Device files (block, character, pseudo)
├── tmp/            Ephemeral temp (cleared on reboot on most distros)
├── var/tmp/        Persistent temp (survives reboot — use for large intermediates)
├── home/           User home directories
├── root/           Root user home
├── opt/            Optional self-contained software packages
├── srv/            Data served by system services (web, ftp)
├── mnt/            Manual mount points
└── media/          Automounted removable media
```

**Data Engineering path conventions:**

| Component | Recommended Path |
|---|---|
| Airflow home | `/opt/airflow/` or `/home/airflow/` |
| Spark installation | `/opt/spark/` |
| Python uv environments | `/opt/pyenvs/<project>/` or `~/.local/share/uv/` |
| Pipeline logs | `/var/log/<pipeline-name>/` |
| Data landing zone | `/data/raw/` or `/mnt/data/raw/` |
| High-speed intermediate staging | `/dev/shm/` (RAM-backed tmpfs, cleared on reboot) |
| Large temp ETL intermediates | `/var/tmp/<job-id>/` (survives reboot, audit and clean via cron) |

---

## §3 File Types

The first character of `ls -la` output identifies the file type:

| Character | Type | Example / Notes |
|---|---|---|
| `-` | Regular file | Source code, data files, binaries |
| `d` | Directory | |
| `l` | Symbolic link | `/bin -> usr/bin`; can cross filesystems |
| `p` | Named pipe (FIFO) | IPC between processes; created with `mkfifo` |
| `s` | Unix domain socket | Airflow scheduler socket, Docker daemon socket |
| `b` | Block device | `/dev/sda` — disk, accessed in fixed-size blocks |
| `c` | Character device | `/dev/null`, `/dev/urandom` — streamed byte-by-byte |

```bash
# Identify file type without ls
file /usr/bin/python3   # ELF 64-bit LSB pie executable
file /dev/sda           # block special
stat /var/run/docker.sock  # socket
```

---

## §4 Permission Model

### Standard rwx Permissions

```
  drwxr-xr-x  2  airflow  airflow  4096  Sep 10 12:00  dags/
  │└─┬──┘└─┬─┘└┬┘
  │  │     │   └── Others: r-x (5)
  │  │     └────── Group:  r-x (5)
  │  └──────────── Owner:  rwx (7)
  └─────────────── Type:   d (directory)
```

| Permission | On File | On Directory |
|---|---|---|
| `r` (4) | Read file content | List directory contents |
| `w` (2) | Write/truncate file | Create, delete, rename files within |
| `x` (1) | Execute as program | Traverse (enter) the directory |

```bash
chmod 750 /opt/airflow/          # Owner: rwx, Group: r-x, Others: ---
chmod 640 /etc/airflow/.env      # Owner: rw-, Group: r--, Others: ---
chmod u+x,go-w pipeline.sh       # Symbolic: add exec to owner, remove write from group+others
chown airflow:airflow /opt/airflow -R
```

### Special Permission Bits

| Bit | Octal | Effect on File | Effect on Directory |
|---|---|---|---|
| setuid | 4000 | Executable runs as file owner (e.g., `passwd` runs as root) | No effect on most systems |
| setgid | 2000 | Executable runs as file group | New files inherit directory's group |
| sticky | 1000 | (rarely used on files) | Only file owner/root can delete — used on `/tmp` |

```bash
chmod 4755 /usr/bin/binary   # setuid + 755
chmod 2775 /data/shared/     # setgid on shared dir — all new files inherit group
chmod 1777 /tmp              # sticky — standard for world-writable dirs

# Find all setuid/setgid files (security audit)
find / -type f \( -perm -4000 -o -perm -2000 \) -ls 2>/dev/null
```

### umask and Default Permissions

`umask` subtracts from the default: 666 for files, 777 for directories.

```bash
umask 022   # Files: 644, Dirs: 755 — standard server default
umask 027   # Files: 640, Dirs: 750 — tighter for service accounts
```

Set persistent umask in `/etc/profile.d/umask.sh` or in the user's `~/.bashrc`.

### ACLs (Fine-Grained Control)

```bash
# Grant the 'dataops' group read access to a directory without changing ownership
setfacl -m g:dataops:rx /data/raw/
getfacl /data/raw/

# Default ACL: inherited by new files/subdirs
setfacl -d -m g:dataops:rx /data/raw/
```

---

## §5 Inodes and Links

Every file has an **inode** (index node) storing: permissions, UID/GID, timestamps (atime/mtime/ctime), size, block pointers. The inode does NOT store the filename — the filename lives in the directory entry pointing to the inode number.

```bash
stat /opt/airflow/dags/my_dag.py   # Full inode detail
ls -li /opt/airflow/dags/          # -i flag shows inode number
```

**Hard link:** second directory entry pointing to the same inode. Same filesystem only. Deleting one entry does not delete the data until link count reaches zero.

```bash
ln /data/raw/file.csv /data/processed/file.csv
```

**Symbolic link:** a file whose content is a path string. Can cross filesystems. Broken if target moves or is deleted.

```bash
ln -s /opt/spark/current /opt/spark/3.5.1   # Version-agnostic path pattern
readlink -f /opt/spark/current              # Resolve full absolute path
```

```bash
# Find all broken symlinks
find /opt -xtype l 2>/dev/null
```

---

## §6 Process Model

```
fork()  →  child is a copy of parent (copy-on-write pages)
exec()  →  replaces child's image with new program binary
wait()  →  parent collects child's exit status
```

**Process states (visible in `ps`, `top`, `htop`):**

| State | Meaning | DE Relevance |
|---|---|---|
| `R` | Running or runnable (on CPU) | Normal |
| `S` | Sleeping — waiting for event (interruptible) | Idle workers |
| `D` | Uninterruptible sleep — waiting for I/O | Disk/NFS stall → cannot be killed |
| `T` | Stopped (SIGSTOP or debugger) | |
| `Z` | Zombie — exited, parent hasn't called wait() | Airflow subprocess leak |

```bash
ps aux --sort=-%mem | head -20   # Top memory consumers
ps -ef --forest                  # Process tree with parent/child relationships
ps -o pid,ppid,stat,cmd -p $(pgrep -d, airflow)
```

**Zombie detection and resolution:**

```bash
ps aux | awk '$8 == "Z"'   # List zombie processes
# Fix: kill the parent process so init (PID 1) adopts and reaps the zombie
```

---

## §7 User and Group Model

```
/etc/passwd:  username:x:UID:GID:comment:home_dir:shell
/etc/shadow:  username:$6$hashed_password:last_changed:...  (root-readable only)
/etc/group:   groupname:x:GID:user1,user2,user3
```

**Service account pattern for DE tools (no login shell, no password):**

```bash
# Create a system account for Airflow — no home dir login, locked password
useradd --system --no-create-home --shell /usr/sbin/nologin airflow
useradd --system --no-create-home --shell /usr/sbin/nologin spark

# Add to supplementary groups (e.g., docker group for socket access)
usermod -aG docker airflow
```

```bash
id airflow               # UID, GID, supplementary groups
groups airflow           # Group memberships
getent passwd airflow    # Lookup from NSS (works with LDAP too)
```

---

## §8 Package Management — Dual Track

### Ubuntu / Debian (apt + dpkg)

```bash
apt update && apt upgrade -y               # Refresh index, upgrade all
apt install python3.12 python3.12-venv -y
apt remove <pkg>          # Remove package, keep config files
apt purge <pkg>           # Remove package AND config files
apt autoremove            # Remove orphaned dependencies
apt-cache search spark    # Search available packages
apt-cache show openjdk-21-jdk  # Package metadata

# Which package owns a file?
dpkg -S /usr/bin/python3

# List installed packages
dpkg -l | grep -i airflow

# Install a local .deb
dpkg -i ./custom-package.deb
apt-get install -f    # Fix broken dependencies after dpkg install
```

Repository management:
```bash
# Add a repo (preferred over add-apt-repository for servers)
echo "deb [signed-by=/usr/share/keyrings/custom.gpg] https://repo.example.com/apt stable main" \
  | tee /etc/apt/sources.list.d/custom.list

# Pinning — prevent a package from upgrading
echo "Package: python3.12\nPin: version 3.12.*\nPin-Priority: 1001" \
  > /etc/apt/preferences.d/python312
```

### RHEL / Rocky Linux (dnf + rpm)

```bash
dnf install java-21-openjdk python3.12 -y
dnf update -y
dnf remove <pkg>
dnf search spark
dnf info python3.12

# Enable EPEL (Extra Packages for Enterprise Linux) — required on RHEL/Rocky
dnf install epel-release -y    # Rocky
# RHEL: subscription-manager repos --enable codeready-builder-for-rhel-9-x86_64-rpms
# Then: dnf install epel-release

# Which package owns a file?
rpm -qf /usr/bin/python3

# List installed packages
rpm -qa | grep -i java

# Install a local .rpm
rpm -ivh ./custom-package.rpm
dnf localinstall ./custom-package.rpm   # Resolves deps automatically

# Module streams (RHEL 9 application streams)
dnf module list python39
dnf module enable python39:3.9
```

---

## §9 Environment Variables and Profile Load Order

Understanding load order is essential: Python, Airflow, Spark, and Java all depend on correctly set env vars that only work if loaded in the right context.

### Key Variables for the DE Stack

```bash
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
SPARK_HOME=/opt/spark
HADOOP_HOME=/opt/hadoop
PYTHONPATH=/opt/airflow/plugins:/opt/mylib
AIRFLOW_HOME=/opt/airflow
UV_PROJECT_ENVIRONMENT=/opt/pyenvs/myproject
PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$HOME/.local/bin:$PATH
```

### Bash Profile Load Order

```
Login shell (ssh, su -, console login):
  /etc/profile
    └── /etc/profile.d/*.sh  (each file, alphabetically)
  ~/.bash_profile  ← if found, stops here
  OR ~/.bash_login ← second choice
  OR ~/.profile    ← third choice (also read by sh, dash)
      └── ~/.bashrc (usually sourced explicitly from ~/.bash_profile)

Interactive non-login shell (new terminal in existing session):
  /etc/bash.bashrc  [Ubuntu] / /etc/bashrc  [RHEL]
  ~/.bashrc

Non-interactive shell (scripts, cron, systemd ExecStart=):
  *** NOTHING IS SOURCED AUTOMATICALLY ***
  Set env vars explicitly in: EnvironmentFile=, --login flag, or script header
```

### Persistent System-Wide Variables

```bash
# /etc/environment — simplest; key=value only; no shell syntax; no export keyword
# Loaded by PAM for login sessions (ssh, display manager)
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
AIRFLOW_HOME=/opt/airflow

# /etc/profile.d/de-stack.sh — shell syntax; login shells and su -
export SPARK_HOME=/opt/spark
export PATH="$SPARK_HOME/bin:$PATH"
```

### Systemd Service Env Injection (Most Reliable for Daemons)

```ini
# /etc/airflow/environment  — plain key=value, no export, no quotes needed
AIRFLOW_HOME=/opt/airflow
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:${DB_PASS}@localhost/airflow
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# In the unit file:
[Service]
EnvironmentFile=/etc/airflow/environment
```

```bash
# Verify what a running service actually sees
systemctl show airflow-scheduler.service | grep Environment
cat /proc/$(pgrep -f "airflow scheduler")/environ | tr '\0' '\n'
```
