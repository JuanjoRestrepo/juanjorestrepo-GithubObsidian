# Linux Security Hardening

## Table of Contents
1. Hardening Philosophy and CIS Benchmark Overview
2. Initial Server Hardening Checklist
3. sudo and PAM Configuration
4. SSH Hardening Checklist (Cross-Reference)
5. File System Security Audit
6. AppArmor — Ubuntu MAC Framework
7. SELinux — RHEL/Rocky MAC Framework
8. auditd — System Audit Subsystem
9. fail2ban — Intrusion Prevention
10. Kernel Hardening via sysctl
11. Secrets Hygiene and Vault Integration
12. Patch Management — Automated Updates

---

## §1 Hardening Philosophy and CIS Benchmark Overview

The CIS (Center for Internet Security) Benchmarks define two levels:
- **Level 1:** Essential configuration for any server. Low operational impact. Apply universally.
- **Level 2:** Defense-in-depth for high-sensitivity environments. May break some software.

For Data Engineering servers: apply **Level 1 fully**, apply **Level 2 selectively**, and document every deviation with a business justification in your runbook.

```bash
# Run automated CIS compliance check
# [Ubuntu]
apt install -y lynis
lynis audit system --profile /etc/lynis/default.prf | tee /var/log/lynis-audit.log

# [RHEL/Rocky]
dnf install -y scap-security-guide openscap-scanner
oscap xccdf eval \
    --profile xccdf_org.ssgproject.content_profile_cis_server_l1 \
    --results /tmp/cis-results.xml \
    --report  /tmp/cis-report.html \
    /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
```

---

## §2 Initial Server Hardening Checklist

Execute immediately after provisioning a new server, before deploying any workload.

```bash
# ─── 1. System update ─────────────────────────────────────────────────────────
# [Ubuntu]
apt update && apt upgrade -y && apt autoremove -y

# [RHEL/Rocky]
dnf update -y && dnf autoremove -y

# ─── 2. Remove unnecessary packages ─────────────────────────────────────────
# [Ubuntu] — telnet, rsh, nis, tftp are CIS L1 removals
apt purge -y telnet rsh-client rsh-redone-client nis yp-tools tftpd

# [RHEL/Rocky]
dnf remove -y telnet ypbind rsh tftp

# ─── 3. Disable unused services ──────────────────────────────────────────────
for svc in avahi-daemon cups rpcbind nfs-server; do
    systemctl disable --now "$svc" 2>/dev/null || true
done

# ─── 4. Set timezone to UTC on all servers ────────────────────────────────────
timedatectl set-timezone UTC
timedatectl status

# ─── 5. Enable and configure NTP ─────────────────────────────────────────────
# [Ubuntu — systemd-timesyncd (lightweight NTP client)]
systemctl enable --now systemd-timesyncd
timedatectl show-timesync

# [RHEL — chrony]
dnf install chrony -y
systemctl enable --now chronyd
chronyc tracking

# ─── 6. Disable IPv6 if not required ─────────────────────────────────────────
# /etc/sysctl.d/99-disable-ipv6.conf
echo "net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1" > /etc/sysctl.d/99-disable-ipv6.conf
sysctl --system

# ─── 7. Core dump restriction ────────────────────────────────────────────────
# /etc/security/limits.d/99-coredump.conf
echo "* hard core 0" > /etc/security/limits.d/99-coredump.conf
echo "fs.suid_dumpable = 0" > /etc/sysctl.d/99-coredump.conf
sysctl --system

# ─── 8. GRUB bootloader password (CIS L2 — prevents single-user mode bypass) ─
# Only apply on physical/dedicated hosts
grub2-setpassword    # [RHEL] — prompts for password, stores in /boot/grub2/user.cfg
# [Ubuntu]: grub-mkpasswd-pbkdf2 → paste hash into /etc/grub.d/40_custom

# ─── 9. Banner and MOTD (legal notice for compliance) ──────────────────────
echo "Authorized use only. Activity is monitored and logged." > /etc/issue
echo "Authorized use only. Activity is monitored and logged." > /etc/issue.net
echo "" > /etc/motd
```

---

## §3 sudo and PAM Configuration

### sudo

```bash
# ALWAYS edit sudoers with visudo — syntax validation prevents lockout
visudo -f /etc/sudoers.d/dataops

# /etc/sudoers.d/dataops
# Grant specific commands only — never ALL on production
%dataops ALL=(airflow) NOPASSWD: /opt/pyenvs/airflow/bin/airflow dags list
%dataops ALL=(root)    PASSWD:   /bin/systemctl restart airflow-scheduler

# Never do this on production:
# %dataops ALL=(ALL) NOPASSWD: ALL  ← Gives root to everyone in group

# Audit sudo usage
grep sudo /var/log/auth.log          # [Ubuntu]
grep sudo /var/log/secure            # [RHEL]
journalctl _COMM=sudo --since today  # systemd-based audit
```

### PAM — Password Policy and Account Lockout

```bash
# ─── [Ubuntu] Install and configure libpam-pwquality ────────────────────────
apt install libpam-pwquality -y

# /etc/security/pwquality.conf
cat > /etc/security/pwquality.conf <<'EOF'
minlen = 14
minclass = 4
maxrepeat = 3
maxsequence = 3
dcredit = -1
ucredit = -1
ocredit = -1
lcredit = -1
dictcheck = 1
EOF

# ─── Account lockout via pam_faillock (replaces pam_tally2) ─────────────────
# /etc/security/faillock.conf
cat > /etc/security/faillock.conf <<'EOF'
deny = 5                # Lock after 5 failed attempts
fail_interval = 900     # Within 15 minute window
unlock_time = 900       # Lock for 15 minutes
even_deny_root = true   # Apply to root too
audit = true            # Log to audit log
EOF

# Verify lockout status / manually unlock
faillock --user dataops         # Show failure count
faillock --user dataops --reset # Manually unlock

# Password aging
chage -l dataops                # View password aging policy
chage -M 90 -m 1 -W 14 dataops # Max 90 days, min 1 day, 14 day warning
```

---

## §5 File System Security Audit

```bash
# Find all SUID and SGID binaries — review after each package install
find / -xdev -type f \( -perm -4000 -o -perm -2000 \) -print 2>/dev/null | \
    sort > /var/log/suid-sgid-baseline.txt

# Compare against baseline
diff /var/log/suid-sgid-baseline.txt <(find / -xdev -type f \( -perm -4000 -o -perm -2000 \) -print 2>/dev/null | sort)

# Find world-writable files (not in /tmp or /proc)
find / -xdev -type f -perm -0002 -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null

# Find world-writable directories without sticky bit
find / -xdev -type d -perm -0002 -not -perm -1000 2>/dev/null

# Files with no owner (orphaned — indicator of package removal without cleanup)
find / -xdev -nouser -o -nogroup 2>/dev/null | grep -v "^/proc"

# Immutable flag — protect critical files from modification
chattr +i /etc/passwd /etc/shadow /etc/group    # Cannot be modified even as root
lsattr /etc/passwd                               # Shows ----i---- attribute
chattr -i /etc/shadow                            # Remove immutable flag
```

---

## §6 AppArmor — Ubuntu MAC Framework

AppArmor enforces mandatory access control via profiles that define exactly which files, capabilities, and network sockets a process can access.

```bash
# Status
aa-status                          # Running mode of all profiles
systemctl status apparmor

# Modes per profile
# enforcing: violations blocked and logged
# complain:  violations only logged — use during profile development
# disabled:  not loaded

# Switch modes
aa-enforce  /etc/apparmor.d/usr.bin.python3
aa-complain /etc/apparmor.d/usr.bin.python3
aa-disable  /etc/apparmor.d/usr.bin.python3
apparmor_parser -r /etc/apparmor.d/usr.bin.python3   # Reload profile
```

### Writing a Profile for a Python ETL Service

```bash
# Generate base profile from binary (run in complain mode first)
aa-genprof /opt/etl/run_pipeline.py
# Execute the program normally to generate capability events
# Press 'S' to scan and 'F' to finish → saves profile
```

```apparmor
# /etc/apparmor.d/opt.etl.run_pipeline
#include <tunables/global>

/opt/etl/run_pipeline.py {
  #include <abstractions/base>
  #include <abstractions/python>

  # Read access
  /opt/etl/**              r,
  /opt/pyenvs/etl/**       r,
  /etc/etl/environment     r,
  /data/raw/**             r,

  # Write access
  /data/processed/**       rw,
  /var/log/etl/**          rw,
  /tmp/etl.**              rw,

  # Network — outbound to PostgreSQL and S3
  network tcp,

  # Capabilities
  capability setuid,       # If the script drops privileges

  # Deny everything else
  deny /etc/shadow         r,
  deny /proc/sysrq-trigger rw,
}
```

```bash
apparmor_parser -r /etc/apparmor.d/opt.etl.run_pipeline
aa-enforce /etc/apparmor.d/opt.etl.run_pipeline

# Monitor violations
aa-logprof                         # Interactive: review violations, update profile
journalctl | grep "apparmor"       # Raw log entries
grep "DENIED" /var/log/syslog      # [Ubuntu] AppArmor denials
```

---

## §7 SELinux — RHEL/Rocky MAC Framework

```bash
# Status
sestatus
getenforce                         # Enforcing | Permissive | Disabled

# Toggle mode (temporary — until reboot)
setenforce 1    # Enforcing
setenforce 0    # Permissive (use during troubleshooting ONLY — never leave permissive)

# Permanent mode: /etc/selinux/config
sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config
```

### Context and Labels

```bash
# Every file, process, and port has a label: user:role:type:level
ls -Z /opt/airflow/                     # File contexts
ps -eZ | grep airflow                   # Process contexts
semanage port -l | grep 8080            # Port contexts

# Fix context after moving files
restorecon -Rv /opt/airflow/
chcon -R -t httpd_sys_content_t /opt/airflow/www/   # Temporary

# Booleans — toggle features without writing policy
getsebool -a | grep airflow
setsebool -P httpd_can_network_connect on   # -P makes persistent
```

### Diagnosing and Resolving Violations

```bash
# View AVC denials
ausearch -m avc -ts recent
journalctl | grep "avc:  denied"
sealert -a /var/log/audit/audit.log     # Human-readable analysis with suggested fix

# Generate allow rule from denial (review before applying!)
ausearch -m avc -ts recent | audit2allow -M my_airflow_policy
# Review my_airflow_policy.te — understand what is being allowed
semodule -i my_airflow_policy.pp       # Install the policy module

# List installed custom policy modules
semodule -l | grep my_
```

---

## §8 auditd — System Audit Subsystem

```bash
# Status
systemctl status auditd
auditctl -s              # Kernel audit status: enabled, backlog

# /etc/audit/rules.d/99-de-server.rules — persistent rules
```

```
# Delete existing rules first
-D

# Set failure mode: 1=log to syslog, 2=panic (production: use 1)
-b 8192          # Backlog buffer
-f 1

# ─── Authentication and authorization ───────────────────────────────────────
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/sudoers -p wa -k privilege_escalation
-w /etc/sudoers.d/ -p wa -k privilege_escalation
-w /var/log/auth.log -p wa -k authentication     # [Ubuntu]
-w /var/log/secure -p wa -k authentication       # [RHEL]

# ─── Privileged commands ─────────────────────────────────────────────────────
-a always,exit -F arch=b64 -S execve -C uid!=euid -F euid=0 -k privilege_escalation
-a always,exit -F path=/usr/bin/sudo -F perm=x -k sudo_exec

# ─── Data access (pipeline data directories) ────────────────────────────────
-w /data/sensitive/ -p rwxa -k data_access
-w /etc/airflow/ -p wa -k config_change

# ─── Network (suspicious outbound connections) ───────────────────────────────
-a always,exit -F arch=b64 -S connect -k network_outbound

# Make rules immutable until reboot (CIS L2)
# -e 2
```

```bash
augenrules --load                          # Load rules from /etc/audit/rules.d/
auditctl -l                                # List active rules

# Query audit log
ausearch -k identity --start today         # By key
ausearch -ua airflow --start yesterday     # By user
ausearch -m USER_LOGIN --start "this week" # By message type
aureport --auth --start today              # Authentication summary report
aureport --failed                          # All failures
```

---

## §9 fail2ban

```bash
# [Ubuntu]  apt install fail2ban
# [RHEL]    dnf install fail2ban

# /etc/fail2ban/jail.d/sshd.local
```

```ini
[sshd]
enabled  = true
port     = ssh
filter   = sshd
backend  = systemd
maxretry = 5
findtime = 10m
bantime  = 1h
banaction = nftables-multiport
```

```ini
# /etc/fail2ban/jail.d/airflow.local
[airflow]
enabled  = true
port     = 8080
filter   = airflow
logpath  = /var/log/airflow/webserver.log
maxretry = 10
findtime = 5m
bantime  = 30m
```

```bash
systemctl enable --now fail2ban
fail2ban-client status                  # All active jails
fail2ban-client status sshd             # Banned IPs for sshd
fail2ban-client set sshd unbanip 1.2.3.4  # Manual unban
```

---

## §10 Kernel Hardening via sysctl

```bash
# /etc/sysctl.d/99-hardening.conf
```

```ini
# ─── Network: spoofing, redirects, SYN floods ───────────────────────────────
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_timestamps = 0

# ─── Memory and address randomization ───────────────────────────────────────
kernel.randomize_va_space = 2          # Full ASLR
fs.suid_dumpable = 0                   # Disable core dumps for setuid
kernel.dmesg_restrict = 1             # Restrict dmesg to root
kernel.kptr_restrict = 2              # Hide kernel pointers from /proc
```

```bash
sysctl --system                        # Apply all sysctl.d files
sysctl -p /etc/sysctl.d/99-hardening.conf  # Apply specific file
sysctl net.ipv4.tcp_syncookies         # Verify current value
```

---

## §11 Secrets Hygiene and Vault Integration

```bash
# Environment file pattern — permission 640, owned by root:serviceaccount
install -m 640 -o root -g airflow /dev/null /etc/airflow/secrets.env
cat > /etc/airflow/secrets.env <<'EOF'
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:CHANGE_ME@localhost/airflow
AIRFLOW__CORE__FERNET_KEY=CHANGE_ME
EOF
# In unit file: EnvironmentFile=/etc/airflow/secrets.env

# HashiCorp Vault — retrieve secrets in scripts
export VAULT_ADDR="https://vault.internal:8200"
export VAULT_TOKEN="$(cat /run/secrets/vault-token)"  # From instance role or AppRole

DB_PASS=$(vault kv get -field=password secret/de/postgres/airflow)
export DB_PASS

# Audit trail: Vault logs every secret access with identity and timestamp

# NEVER:
echo "password123" > /opt/airflow/config.py   # Plaintext in code
git commit -m "add config" config.py           # Secrets in git history
env | grep -i pass                             # Exposed via /proc/environ to any user
```

---

## §12 Patch Management

### Ubuntu — unattended-upgrades

```bash
apt install unattended-upgrades apt-listchanges -y
dpkg-reconfigure --priority=low unattended-upgrades

# /etc/apt/apt.conf.d/50unattended-upgrades
# Unattended-Upgrade::Allowed-Origins {
#     "${distro_id}:${distro_codename}-security";
# };
# Unattended-Upgrade::Automatic-Reboot "false";   # Control reboot window
# Unattended-Upgrade::Mail "ops@company.com";

systemctl status unattended-upgrades
unattended-upgrades --dry-run --debug
```

### RHEL / Rocky — dnf-automatic

```bash
dnf install dnf-automatic -y

# /etc/dnf/automatic.conf
# [commands]
# apply_updates = yes
# upgrade_type = security  # Only security updates automatically

systemctl enable --now dnf-automatic.timer
systemctl list-timers dnf-automatic.timer
```
