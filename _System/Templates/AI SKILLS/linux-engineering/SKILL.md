---
name: "linux-engineering"
description: "Expert Linux reference for developers and data engineers: advanced Bash, process/memory/cgroups, networking, systemd, CIS hardening, eBPF/perf, and DE-applied patterns. Trigger for any Linux, shell, server, sysadmin, DevOps, or infrastructure question."
---

# Linux Engineering Skill

Expert-level Linux reference covering Ubuntu/Debian and RHEL/Rocky Linux, calibrated for software developers and data engineers. Spans sysadmin fundamentals, advanced Bash scripting, kernel-adjacent operational knowledge, production security hardening, and applied Data Engineering workflows on Linux servers.

---

## Trigger Keywords

linux · bash · shell · zsh · sh · systemd · journald · cron · cgroups · namespaces · proc · kernel · ssh · sshd · nftables · iptables · firewalld · selinux · apparmor · auditd · sudo · chmod · chown · chattr · rsync · scp · rclone · strace · perf · bpftrace · bcc · ebpf · htop · btop · vmstat · iostat · iotop · sar · lsof · ss · ip · tcpdump · nmap · apt · dpkg · dnf · rpm · systemctl · journalctl · ulimit · sysctl · proc · sys · tmpfs · inotify · mkfifo · xargs · parallel · awk · sed · grep · find · tar · fail2ban · vault · cis · hardening · daemon · uv-on-linux · airflow-linux · spark-linux · docker-linux · container · server-setup · server-config · linux-security · bash-script · shell-script · linux-permissions · linux-networking · linux-performance · linux-observability

---

## Domain → Reference File Map

Read the reference file(s) that match the query domain. Multiple files may apply simultaneously.

| Domain | Reference File | Load When |
|---|---|---|
| OS model, FHS, file types, permissions, packages, env vars | `references/linux-fundamentals.md` | Concepts, file system layout, user/group model, distro package tooling |
| Advanced Bash: arrays, traps, process substitution, getopts | `references/bash-advanced.md` | Script authoring, error handling, data pipeline shell patterns |
| /proc, /sys, cgroups v2, namespaces, IPC, OOM, fd limits | `references/process-filesystem-memory.md` | Process management, container internals, memory pressure debugging |
| Networking, SSH hardening, nftables, Docker bridge, DNS | `references/networking-linux.md` | Network config, firewall rules, SSH lockdown, connectivity debugging |
| systemd units, timers, journald, service security directives | `references/systemd-services.md` | Writing service files for DE tools, log querying, boot management |
| CIS hardening, AppArmor, SELinux, auditd, secrets hygiene | `references/security-hardening.md` | Server hardening, compliance auditing, access control, secrets patterns |
| USE method, perf, strace, eBPF/BCC, disk/memory profiling | `references/performance-observability.md` | Profiling pipelines, debugging stalls, flame graphs, resource contention |
| Applied DE: uv, Airflow, Spark, Docker, rclone, ETL shell | `references/linux-for-data-engineering.md` | Full Data Engineering stack setup and operation on Linux servers |

---

## Canonical Sources

| Source | Domain |
|---|---|
| GNU `man` pages (coreutils, util-linux, iproute2, bash, systemd) | All |
| Ubuntu Server Guide 22.04 / 24.04 LTS | Debian/Ubuntu |
| RHEL 9 / Rocky Linux 9 Official Documentation | RHEL/RPM |
| CIS Ubuntu Linux 22.04 LTS Benchmark v2.x | Security — Ubuntu |
| CIS Red Hat Enterprise Linux 9 Benchmark v2.x | Security — RHEL |
| NIST SP 800-123 (Guide to General Server Security) | Security — General |
| Brendan Gregg — *Systems Performance* 2nd ed. (2020) | Observability |
| Brendan Gregg — *BPF Performance Tools* (2019) | eBPF / BCC / bpftrace |
| Michael Kerrisk — *The Linux Programming Interface* (2010) | Kernel API / Syscalls |
| William Shotts — *The Linux Command Line* 2nd ed. (2019) | Shell / CLI |
| systemd.io official documentation | systemd |
| Docker Engine Documentation (docs.docker.com) | Containers |
| AppArmor Docs (ubuntu.com/server/docs/apparmor) | Ubuntu security |
| SELinux User and Administrator's Guide (access.redhat.com) | RHEL security |

---

## Distro Coverage Policy

- **Primary:** Ubuntu 22.04 LTS / 24.04 LTS — most common Data Engineering server target and default cloud AMI base.
- **Secondary:** RHEL 9 / Rocky Linux 9 — enterprise cluster standard (Spark, Hadoop ecosystems).
- When procedures diverge by distro, present both tracks side-by-side under `[Ubuntu]` / `[RHEL/Rocky]` labels.
- Package names, config paths, firewall tools, and service names that differ between distros are always called out explicitly.

---

## Output Standards

- All shell commands use full flags with explanations; never rely on unexplained abbreviations.
- Code blocks always declare the interpreter: ` ```bash `, ` ```python `, ` ```ini `, ` ```toml `.
- Security-relevant commands include a warning when destructive, irreversible, or privilege-escalating.
- All Bash scripts open with `#!/usr/bin/env bash` and `set -euo pipefail`.
- Production systemd unit files always include hardening directives (§ systemd-services.md §5).
- Never hardcode credentials, tokens, or secrets in any file, unit, or script — always use `EnvironmentFile=` or a secrets manager integration.
