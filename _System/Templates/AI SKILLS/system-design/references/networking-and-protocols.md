# Networking & Protocols

**Sources:** IETF RFCs — TCP (RFC 793), HTTP/1.1 (RFC 7230–7235), HTTP/2 (RFC 7540),
HTTP/3 (RFC 9114), TLS 1.3 (RFC 8446), DNS (RFC 1034/1035); Google QUIC Working Group,
"QUIC: A UDP-Based Multiplexed and Secure Transport" (IETF, 2021); Martin Kleppmann,
*Designing Data-Intensive Applications* (O'Reilly, 2017); Alex Xu, *System Design Interview*
Vol. 1 (2020), Ch. 1; Cloudflare Learning Center (TCP, TLS, HTTP, DNS, CDN documentation).

---

## 1. What Happens When You Type a URL Into a Browser

A complete request lifecycle — useful as a system design interview answer and as a mental
model for isolating latency at any layer.

**1. DNS resolution** — browser checks its own cache, then OS cache, then a configured
resolver (ISP or public resolver such as 8.8.8.8). If uncached, the resolver performs a
recursive query: root nameserver → TLD nameserver (`.com`) → authoritative nameserver for
the domain, returning the IP. Each level caches per the record's TTL. Total added latency:
0 ms (cache hit) to ~100 ms (full recursive resolution across the hierarchy).

**2. TCP handshake** — SYN → SYN-ACK → ACK. This three-way handshake is pure overhead
before any data moves — one full round-trip time (RTT) consumed before the first byte of
HTTP. This is why HTTP/2 and HTTP/3 emphasize connection reuse and 0-RTT resumption.

**3. TLS handshake** — client and server negotiate TLS version and cipher suite, exchange
and validate certificates, and derive a shared session key. TLS 1.3 reduced this to one RTT
(down from two in TLS 1.2) and supports 0-RTT resumption for repeat connections, where
the client can send application data in the first message.

**4. HTTP request** — browser sends the request over the established encrypted connection.

**5. Server processing** — request hits load balancer → application server (or CDN edge
cache if cacheable) → app queries DB/cache → response assembled.

**6. Response rendering** — browser parses HTML; discovers additional sub-resources (CSS,
JS, images); each may trigger its own DNS + TCP + TLS cycle unless already connected or
pre-fetched. Hence the value of HTTP/2 multiplexing, connection coalescing, and CDN-hosted
shared assets that may already be cached at the edge near the user.

**Latency contributions per phase (approximate):**
```
Phase                       Approximate added latency
DNS resolution (cache hit)  0 ms
DNS resolution (full query) 20–100 ms (recursive, across hierarchy)
TCP handshake               1 RTT  (~1 ms same DC, ~150 ms cross-continent)
TLS 1.3 handshake           1 RTT  (+ 0-RTT resumption on repeat connections)
TLS 1.2 handshake           2 RTT
Server processing           1–100 ms (depends on app + DB)
Network transfer            proportional to response size and bandwidth
```

---

## 2. TCP vs. UDP

| | TCP | UDP |
|---|---|---|
| Connection model | Connection-oriented — handshake required before data | Connectionless — send immediately |
| Reliability | Guaranteed delivery, automatic retransmission, in-order delivery | No guarantees — packets may be lost, duplicated, or arrive out of order |
| Flow & congestion control | Yes — receiver signals capacity; sender backs off on congestion | None |
| Overhead | Higher (acks, seq numbers, handshake) | Minimal headers |
| Latency profile | Higher — head-of-line blocking on packet loss | Lower — no blocking on retransmission |
| Use cases | Anything requiring correctness: HTTP, HTTPS, email (SMTP), file transfer (FTP, SFTP) | Latency-sensitive, loss-tolerant: video/voice streaming (WebRTC), online gaming, DNS queries |

**Why real-time media deliberately chooses UDP:** a dropped packet representing 20 ms of
audio is less harmful than TCP retransmitting it and stalling all subsequent packets behind
it (head-of-line blocking). The application can conceal the gap with interpolation. This
is the same motivation behind QUIC — the transport layer underlying HTTP/3.

---

## 3. HTTP/1.1 → HTTP/2 → HTTP/3

| | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| **Transport** | TCP | TCP | QUIC (over UDP) |
| **Multiplexing** | No — one in-flight request per connection; pipelining exists but is broken in practice | Yes — multiple independent streams over one TCP connection | Yes — multiple independent streams; each stream is independent at the transport layer |
| **Head-of-line blocking** | Severe at app layer (one request blocks the next) | Eliminated at app layer; still present at TCP layer — a single lost packet stalls all streams | Eliminated at both layers — QUIC streams are independent; one lost packet only blocks that stream |
| **Header compression** | None | HPACK (static + dynamic Huffman table) | QPACK (HPACK-compatible, handles out-of-order delivery) |
| **Connection setup** | TCP handshake + TLS handshake (2–3 RTT) | Same as HTTP/1.1 | Combined QUIC + TLS 1.3 — 1 RTT on first connection; 0-RTT resumption for repeat |
| **Server push** | No | Yes (proactively send resources before client requests them) | Yes (deprecated in practice — prefetch headers serve the same purpose with fewer issues) |

**Key distinction:** HTTP/2 fixed the application-layer bottleneck (multiplexing over one
connection instead of opening 6–8 parallel TCP connections per origin). HTTP/3 fixes the
underlying transport — a single lost UDP packet no longer stalls unrelated streams because
each QUIC stream has its own independent retransmission state. Most impactful for mobile
and lossy network conditions.

---

## 4. Load Balancer vs. Reverse Proxy vs. API Gateway

| | Load Balancer | Reverse Proxy | API Gateway |
|---|---|---|---|
| **Primary responsibility** | Distribute traffic across multiple backend instances | Forward client requests to a backend, hiding backend topology | Manage full API traffic lifecycle: routing, authentication, rate limiting, transformation, observability |
| **Typical scope** | Traffic distribution + health checks + failover | Single entry point; may also cache, compress, and terminate TLS | Cross-cutting concerns across many microservices or APIs |
| **Examples** | AWS ALB/NLB, HAProxy, GCP Load Balancing | NGINX, Apache httpd | Kong, AWS API Gateway, Apigee, Traefik |
| **Layer** | L4 or L7 | L7 | L7 |

**These components commonly coexist in one stack:**
```
Client
  → CDN (edge cache for static / cacheable content)
    → API Gateway (authentication, rate limiting, routing)
      → Load Balancer (distributes to healthy instances)
        → Reverse Proxy per instance (NGINX in front of app process)
          → Application server
```

Smaller systems frequently collapse several layers into one component — e.g., NGINX acting
as both reverse proxy and load balancer, or an API Gateway handling both routing and TLS
termination. The distinction matters for system design interviews: name the responsibility,
then name a concrete implementation.

---

## 5. Forward Proxy vs. Reverse Proxy

**Forward proxy** — deployed in front of the *client*; makes outbound requests on the
client's behalf. The destination server sees the proxy's IP, not the client's. Used for:
client-side anonymity, content filtering, corporate egress control, TLS inspection of
outbound traffic.

**Reverse proxy** — deployed in front of the *server*; receives inbound requests on the
server's behalf. The client sees the proxy, not the backend. Used for: load balancing, TLS
termination, response caching, hiding internal network topology, DDoS absorption.

**The distinguishing question:** a forward proxy hides the *client* from the destination;
a reverse proxy hides the *server* (backend) from the client.

```
Forward proxy:                    Reverse proxy:
Client → [Forward Proxy] → Server    Client → [Reverse Proxy] → Server
Server sees proxy IP                 Client sees proxy IP
```

---

## 6. DNS Record Types

| Record | Purpose | Example |
|---|---|---|
| **A** | Hostname → IPv4 address | `api.example.com → 93.184.216.34` |
| **AAAA** | Hostname → IPv6 address | `api.example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | Alias — hostname → another hostname | `www.example.com → example.com` |
| **MX** | Mail exchange — where to deliver email for the domain | `example.com → mail.example.com` (with priority) |
| **TXT** | Arbitrary text — domain verification, SPF/DKIM authentication | `"v=spf1 include:_spf.google.com ~all"` |
| **NS** | Delegates a subdomain (or zone) to specific authoritative nameservers | `example.com NS ns1.cloudflare.com` |
| **SOA** | Start of Authority — administrative info about the DNS zone (serial, refresh, TTL) | One per zone |
| **PTR** | Reverse DNS — IP address → hostname (used in email authentication) | `34.216.184.93.in-addr.arpa → api.example.com` |

**TTL (Time To Live):** every DNS record carries a TTL in seconds. Resolvers and clients
cache the response for that duration. Lower TTL = faster propagation of changes; higher TTL
= better performance (fewer recursive queries). Standard values: 300 s (5 min) for records
that may change, 86400 s (24 h) for stable records, 3600 s (1 h) for a safe default.

---

## 7. Common Ports Reference

| Port | Protocol / Service | Notes |
|---|---|---|
| 22 | SSH | Secure shell; also used for SFTP |
| 25 | SMTP | Mail transfer between servers |
| 53 | DNS | UDP for queries; TCP for zone transfers |
| 80 | HTTP | Plaintext web traffic |
| 443 | HTTPS | TLS-encrypted web traffic |
| 3306 | MySQL | Default MySQL database port |
| 5432 | PostgreSQL | Default PostgreSQL database port |
| 6379 | Redis | Default Redis port |
| 8080 | Alternate HTTP | Common for dev servers, local proxies, or secondary HTTP endpoints |
| 9092 | Kafka | Default Kafka broker port |
| 27017 | MongoDB | Default MongoDB port |
| 5672 | RabbitMQ | Default AMQP port |
| 2181 | ZooKeeper | Legacy Kafka metadata coordination (removed in Kafka 4.0 / KRaft) |
| 2379/2380 | etcd | Client requests / peer communication |
| 9200 | Elasticsearch | REST API |
| 9300 | Elasticsearch | Inter-node communication |
