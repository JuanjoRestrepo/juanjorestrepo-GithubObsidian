# Linux Networking

## Table of Contents
1. Network Stack Overview
2. ip Suite — Modern Network Configuration
3. ss — Socket and Connection Inspection
4. DNS Resolution Stack
5. nftables — Modern Firewall
6. SSH Hardening
7. Docker Bridge Networking and Network Namespaces
8. Traffic Capture and Debugging
9. Data Engineering Network Patterns

---

## §1 Network Stack Overview

```
Application (Python, Airflow, Spark)
     │
  Sockets (AF_INET, AF_UNIX)
     │
  Transport: TCP (reliable) / UDP (fast, unreliable)
     │
  Network: IP routing, ICMP
     │
  netfilter / nftables (packet filtering hooks here)
     │
  Network driver (kernel module)
     │
  NIC (physical or virtual: eth0, ens3, eno1, enp0s3)
```

**Interface naming convention (systemd predictable names):**
- `eno1` — onboard NIC (embedded)
- `ens3` — PCIe slot NIC
- `enp2s0` — bus/slot NIC
- `eth0` — still common in containers and VMs
- `lo` — loopback (127.0.0.1/8, ::1/128)

---

## §2 ip Suite — Modern Network Configuration

`iproute2` (`ip` command) replaces deprecated `ifconfig`, `route`, `arp`, `netstat`.

### Address Management

```bash
ip addr show                       # All interfaces with IPs
ip addr show ens3                  # Specific interface
ip -brief addr show                # Compact: interface state IP

# Add/remove IP (temporary — survives until reboot or interface bounce)
ip addr add 10.0.0.10/24 dev ens3
ip addr del 10.0.0.10/24 dev ens3

# Bring interface up/down
ip link set ens3 up
ip link set ens3 down
ip link show                       # All interfaces: state, MAC, MTU
ip -brief link show                # Compact format
```

### Routing

```bash
ip route show                      # Full routing table
ip route show table main           # Explicit — same as above
ip route get 8.8.8.8              # Which route would be used to reach 8.8.8.8

# Add/delete routes (temporary)
ip route add 10.20.0.0/16 via 10.0.0.1 dev ens3
ip route del 10.20.0.0/16
ip route add default via 10.0.0.1  # Default gateway

# Persistent routing: NetPlan (Ubuntu) or NetworkManager (RHEL)
```

### Ubuntu Persistent Config — NetPlan

```yaml
# /etc/netplan/01-netcfg.yaml
network:
  version: 2
  ethernets:
    ens3:
      addresses:
        - 10.0.0.10/24
      gateway4: 10.0.0.1           # Deprecated in newer NetPlan — use routes:
      routes:
        - to: default
          via: 10.0.0.1
      nameservers:
        addresses: [1.1.1.1, 8.8.8.8]
      dhcp4: false
```
```bash
netplan apply                      # Apply without reboot
netplan try                        # Apply with 120-second auto-revert safety
```

### RHEL Persistent Config — NetworkManager

```bash
nmcli con show                     # List all connections
nmcli con show ens3                # Connection details
nmcli con mod ens3 ipv4.addresses "10.0.0.10/24"
nmcli con mod ens3 ipv4.gateway "10.0.0.1"
nmcli con mod ens3 ipv4.dns "1.1.1.1 8.8.8.8"
nmcli con mod ens3 ipv4.method manual
nmcli con up ens3
```

---

## §3 ss — Socket and Connection Inspection

`ss` replaces deprecated `netstat`. Directly reads kernel socket data — faster and more accurate.

```bash
ss -tulpn          # TCP+UDP Listening sockets with PIDs and process names
# -t: TCP  -u: UDP  -l: listening  -p: process  -n: numeric (no DNS resolution)

ss -tnp state established          # Established TCP connections with PIDs
ss -tnp state time-wait            # TIME_WAIT connections (port exhaustion indicator)

# Filter by port
ss -tnp 'sport = :8080'           # Source port 8080
ss -tnp 'dport = :5432'           # Destination port 5432 (PostgreSQL connections)

# Data Engineering port audit
ss -tulpn | grep -E ':(8080|5432|6379|9092|7077|4040|8888|9870)'
# Ports: Airflow:8080, PostgreSQL:5432, Redis:6379, Kafka:9092
#        Spark Master:7077, Spark UI:4040, Jupyter:8888, HDFS NameNode:9870

# Connection count per state
ss -tn | awk 'NR>1 {print $1}' | sort | uniq -c | sort -rn
```

---

## §4 DNS Resolution Stack

```
Application → getaddrinfo() → NSS → /etc/nsswitch.conf
                                 ├── files  → /etc/hosts        (checked first)
                                 ├── resolve → systemd-resolved  (Ubuntu default)
                                 ├── dns    → /etc/resolv.conf   (traditional)
                                 └── mdns4  → Avahi (mDNS .local)
```

```bash
# /etc/nsswitch.conf — resolution order
# hosts: files resolve [!UNAVAIL=return] dns myhostname
cat /etc/nsswitch.conf | grep hosts

# /etc/hosts — override DNS; critical for cluster hostname resolution
# Format: IP  canonical-name  aliases
10.0.0.11  spark-master  spark-master.internal
10.0.0.12  spark-worker-1
10.0.0.13  spark-worker-2

# /etc/resolv.conf
cat /etc/resolv.conf
# nameserver 1.1.1.1
# nameserver 8.8.8.8
# search internal.company.com  ← short hostname expansion

# DNS debugging
resolvectl query spark-master.internal    # systemd-resolved lookup with source
dig spark-master.internal                  # Direct DNS query
dig @1.1.1.1 spark-master.internal        # Query specific resolver
nslookup spark-master.internal            # Legacy; still useful
host spark-master.internal
```

---

## §5 nftables — Modern Firewall

`nftables` replaces `iptables`/`ip6tables`/`arptables`. Ubuntu 20.04+ and RHEL 9 default firewall backend.

**Ubuntu uses `ufw` (frontend to nftables). RHEL uses `firewalld` (also nftables backend).**

### Ubuntu — ufw

```bash
ufw status verbose
ufw enable
ufw default deny incoming
ufw default allow outgoing

# Allow specific services
ufw allow ssh                          # Port 22 TCP
ufw allow 8080/tcp comment "Airflow webserver"
ufw allow from 10.0.0.0/24 to any port 5432 comment "PostgreSQL internal only"
ufw deny 9092/tcp comment "Block Kafka external access"

ufw delete allow 8080/tcp             # Remove a rule
ufw reload
```

### RHEL / Rocky — firewalld

```bash
systemctl enable --now firewalld
firewall-cmd --state

# Zone-based model: 'public' zone is default for external interfaces
firewall-cmd --get-default-zone
firewall-cmd --zone=public --list-all

# Permanent rules (--permanent requires reload to take effect)
firewall-cmd --permanent --zone=public --add-port=8080/tcp
firewall-cmd --permanent --zone=public --add-service=postgresql
firewall-cmd --permanent --zone=internal --add-source=10.0.0.0/24
firewall-cmd --permanent --zone=internal --add-port=7077/tcp  # Spark Master
firewall-cmd --reload

# Remove rule
firewall-cmd --permanent --zone=public --remove-port=8080/tcp
firewall-cmd --reload
```

### Raw nftables (Direct — Distro-Agnostic)

```bash
nft list ruleset                        # View all rules
nft list tables                         # List tables

# Atomic ruleset from file (preferred over incremental adds)
# /etc/nftables.d/de-server.conf
```

```nft
#!/usr/sbin/nft -f
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        iif lo accept comment "Allow loopback"
        ct state established,related accept comment "Allow established connections"
        ct state invalid drop

        tcp dport 22 accept comment "SSH"
        tcp dport 8080 accept comment "Airflow webserver"
        ip saddr 10.0.0.0/24 tcp dport 5432 accept comment "PostgreSQL internal"
        ip saddr 10.0.0.0/24 tcp dport 7077 accept comment "Spark Master internal"
        ip saddr 10.0.0.0/24 tcp dport { 4040-4050 } accept comment "Spark UI internal"

        # ICMP for diagnostics
        icmp type { echo-request } accept
        icmpv6 type { echo-request, nd-neighbor-solicit, nd-router-advert } accept

        log prefix "DROP: " flags all drop
    }
    chain forward { type filter hook forward priority 0; policy drop; }
    chain output  { type filter hook output  priority 0; policy accept; }
}
```

```bash
nft -f /etc/nftables.d/de-server.conf
systemctl enable nftables
```

---

## §6 SSH Hardening

Full hardening checklist for production Data Engineering servers.

### /etc/ssh/sshd_config

```ini
# Protocol and authentication
Port 22                          # Change to non-standard if high-noise environment
Protocol 2
PermitRootLogin no               # NEVER allow root login via SSH
PasswordAuthentication no        # Key-only authentication — mandatory
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
ChallengeResponseAuthentication no
UsePAM yes                       # Required for PAM (2FA, account lockout)

# Access restriction
AllowUsers airflow dataops deploy  # Whitelist specific users — deny all others
MaxAuthTries 3                   # Fail after 3 attempts (triggers fail2ban faster)
MaxSessions 10
LoginGraceTime 20s               # Time window to complete auth

# Session security
ClientAliveInterval 300          # Send keepalive every 5 min
ClientAliveCountMax 2            # Drop after 2 missed keepalives (10 min idle)
TCPKeepAlive yes
X11Forwarding no                 # Disable if X11 not needed
AllowAgentForwarding no          # Disable unless agent forwarding is explicitly required
AllowTcpForwarding no            # Disable unless tunneling required

# Cryptographic hardening (modern algorithms only)
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# Logging
LogLevel VERBOSE                 # Logs accepted key fingerprints — audit trail
```

```bash
# Validate config before restarting
sshd -t
systemctl reload sshd

# Test from a second session before closing the current one
ssh -o ConnectTimeout=5 -i ~/.ssh/id_ed25519 user@server
```

### Key Management

```bash
# Generate modern key pair (Ed25519 — preferred over RSA)
ssh-keygen -t ed25519 -C "dataops@company.com" -f ~/.ssh/id_ed25519

# Deploy public key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub airflow@10.0.0.11

# Or manually
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys

# SSH agent for key forwarding in pipelines
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
# Forward agent for hop-through deployments (only to trusted hosts)
ssh -A airflow@10.0.0.11
```

---

## §7 Docker Bridge Networking and Network Namespaces

```bash
# Default bridge network (docker0): 172.17.0.0/16
docker network ls
docker network inspect bridge

# Container-to-container: use user-defined bridge networks (NOT default docker0)
# User-defined bridge provides DNS by container name
docker network create --driver bridge --subnet 172.20.0.0/16 de-network

docker run -d --name postgres     --network de-network postgres:16
docker run -d --name airflow-web  --network de-network airflow webserver
# airflow-web can reach postgres via hostname "postgres" — no IP lookup needed

# Port publication: host-to-container NAT via iptables/nftables
docker run -p 127.0.0.1:8080:8080 airflow-web   # Bind to loopback only — security
# NEVER bind to 0.0.0.0 for admin interfaces in production

# Inspect networking from host
docker inspect --format '{{.NetworkSettings.Networks}}' airflow-web
ip link show type veth
ip addr show docker0

# Enter container network namespace from host (debug without docker exec)
CONTAINER_PID=$(docker inspect --format '{{.State.Pid}}' airflow-web)
nsenter --target "$CONTAINER_PID" --net ss -tulpn
```

---

## §8 Traffic Capture and Debugging

```bash
# tcpdump — basic capture
tcpdump -i ens3 -n                          # All traffic on ens3, no DNS resolution
tcpdump -i ens3 -n port 5432               # PostgreSQL traffic
tcpdump -i ens3 -n host 10.0.0.12          # Traffic to/from specific host
tcpdump -i ens3 -n 'tcp and port 9092'     # Kafka traffic
tcpdump -i any -n -w /tmp/capture.pcap     # Write to file for Wireshark analysis

# Connectivity testing
nc -zv 10.0.0.11 5432                      # TCP port reachability test (no data)
nc -zv -u 10.0.0.11 514                    # UDP port test
timeout 5 bash -c 'cat < /dev/tcp/10.0.0.11/8080' && echo "OPEN" || echo "CLOSED"

# curl for REST API debugging in ETL scripts
curl -v --max-time 10 \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     https://api.internal/health

# nmap — service discovery and port scan audit
nmap -sV -p 22,5432,8080,9092 10.0.0.0/24
nmap -sU -p 53,123 10.0.0.1              # UDP scan (DNS, NTP)
```

---

## §9 Data Engineering Network Patterns

### rclone for Cloud Storage Transfer

```bash
# /etc/rclone/rclone.conf — configure remotes (see rclone config interactive)
[s3-prod]
type = s3
provider = AWS
env_auth = true              # Use IAM role / instance profile (preferred over keys)
region = us-east-1

# Transfer patterns
rclone copy /data/processed/ s3-prod:my-bucket/processed/ \
    --transfers 8 \          # Parallel file transfers
    --checkers 16 \          # Parallel checksum verification
    --bwlimit 100M \         # Bandwidth limit: 100 MB/s
    --progress \
    --log-file /var/log/rclone/transfer.log \
    --log-level INFO

rclone sync /data/processed/ s3-prod:my-bucket/ \
    --exclude "*.tmp" \
    --backup-dir s3-prod:my-bucket-backup/$(date +%Y%m%d)/
```

### WireGuard VPN for Data Pipeline Ingress

```bash
# [Ubuntu] Install
apt install wireguard -y

# Generate key pair on server
wg genkey | tee /etc/wireguard/server_private.key | \
    wg pubkey > /etc/wireguard/server_public.key
chmod 600 /etc/wireguard/server_private.key
```

```ini
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.100.0.1/24
PrivateKey = <SERVER_PRIVATE_KEY>
ListenPort = 51820
PostUp   = nft add rule inet filter input udp dport 51820 accept
PostDown = nft delete rule inet filter input udp dport 51820 accept

[Peer]
PublicKey = <CLIENT_PUBLIC_KEY>
AllowedIPs = 10.100.0.2/32    # Specific IP for this client — not 0.0.0.0/0
```

```bash
systemctl enable --now wg-quick@wg0
wg show              # Status and peer handshake times
```
