# Scalability & Load Balancing

**Sources:** Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017),
Ch. 1 (Reliability, Scalability, Maintainability); Google SRE Book (Beyer et al., O'Reilly,
2016), Ch. 18 (Software Engineering in SRE); Alex Xu, *System Design Interview* Vol. 1,
Ch. 1; NGINX documentation on load balancing algorithms; AWS Elastic Load Balancing
documentation; Martin Abbott & Michael Fisher, *The Art of Scalability* (Addison-Wesley,
2010) — the Scale Cube model.

---

## 1. Defining Scalability

Kleppmann's definition is the most precise in the literature: scalability is not a one-
dimensional property ("is system X scalable?") but a set of questions about the system's
ability to cope with increased load: "If the system grows in a particular way, what are our
options for coping with the growth?"

**Load parameters** — quantify your load before discussing scaling:
- Requests per second (RPS) to a web server
- Ratio of reads to writes in a database
- Number of simultaneously active users in a chat room
- Hit rate on a cache
- Distribution of data (does one user have 30M followers while most have 200?)

The "30M follower" example is Twitter's actual design problem — the naive "read-time fan-out"
approach (query all followees on each timeline load) is O(followee count) and collapses at
scale. The solution required a hybrid write-time fan-out for regular users and read-time for
celebrities. This illustrates why load distribution, not just average load, determines the
correct architecture.

**Performance metrics** — two numbers describe a system's performance under load:
- **Latency** — how long one request takes. Report as percentiles (p50, p95, p99, p999), not
  averages. Averages hide the long tail. Jeff Dean's "tail latency amplification": if a
  request fans out to 100 backend services, the overall latency is the max of 100 independent
  latency distributions — the p99 of the composite becomes close to the p99.99 of each backend.
- **Throughput** — how many requests per second the system can handle at a given latency SLO.

---

## 2. Vertical vs Horizontal Scaling

```
Vertical Scaling (Scale Up):           Horizontal Scaling (Scale Out):
┌────────────────────┐                 ┌──────┐  ┌──────┐  ┌──────┐
│  Original Server    │                 │ Srv1  │  │ Srv2  │  │ Srv3  │
│  4 CPU, 16 GB RAM  │                 │      │  │      │  │      │
└────────────────────┘                 └──────┘  └──────┘  └──────┘
         │                                   Load Balancer above
         ▼
┌────────────────────┐
│  Upgraded Server   │
│  32 CPU, 256 GB RAM│
└────────────────────┘
```

**Vertical scaling:**
- Zero application changes — drop-in upgrade
- No distributed systems complexity
- Hard ceiling: largest available instance
- Single point of failure (unless warm standby added)
- Cost curve is superlinear — 4× the CPU often costs 8×+ the price
- **Use first** — it's often sufficient and operationally simple

**Horizontal scaling:**
- Theoretically unlimited ceiling
- Requires stateless application design (no in-process session state)
- Introduces load balancing, distributed state, consistency complexity
- Failure of one instance is handled by routing around it
- Linear cost scaling
- **Use when vertical ceiling hit, or when fault tolerance requires multiple instances anyway**

**The Scale Cube (Abbott & Fisher)** — three orthogonal scaling axes:
```
X-axis: Horizontal duplication — clone the service, load-balance across N instances
Y-axis: Functional decomposition — split by function (users service, orders service)
Z-axis: Data partitioning — each instance handles a subset of data (sharding)
```

Most scaling problems are solved on X first, then Y (microservices), then Z (sharding).
Z-axis scaling is the most complex and should be deferred until genuinely necessary.

---

## 3. Load Balancers

A load balancer distributes incoming requests across a pool of backend servers, ensuring no
single server is overwhelmed and providing failover when servers become unavailable.

### L4 vs L7

| | Layer 4 (Transport) | Layer 7 (Application) |
|---|---|---|
| **Operates on** | TCP/UDP (IP + port only) | HTTP headers, URL, cookies, content |
| **Routing decisions** | Source IP, destination port | URL path, Host header, cookie value |
| **Performance** | Faster — minimal packet inspection | Slightly slower — full request parse |
| **SSL termination** | No | Yes (decrypts, inspects, re-encrypts or sends plaintext to backend) |
| **Sticky sessions** | IP hash (crude) | Cookie-based (accurate) |
| **Content-based routing** | Impossible | `/api/*` → API servers, `/static/*` → CDN |
| **Products** | AWS NLB, HAProxy (TCP mode) | AWS ALB, NGINX, Cloudflare, Envoy |

**Use L7 for HTTP traffic** — content-based routing, SSL termination, and accurate health
checks (HTTP 200 vs TCP connection accepted) are worth the marginal overhead.

### Load Balancing Algorithms

```
Round Robin:
  Request 1 → Server A
  Request 2 → Server B
  Request 3 → Server C
  Request 4 → Server A  (wraps)
  ✅ Simple. ❌ Ignores server load — a slow request on Server A still gets the next one.

Weighted Round Robin:
  Servers have assigned weights (Server A=5, B=3, C=2 out of 10).
  5/10 requests go to A, 3/10 to B, 2/10 to C.
  ✅ Accounts for heterogeneous hardware. ❌ Static — doesn't adapt to runtime load.

Least Connections:
  Each request goes to the server with the fewest active connections.
  ✅ Adapts to runtime load — long-running requests don't back up one server.
  ❌ Slightly more complex to implement. Best for long-lived connections (WebSocket, gRPC).

Least Response Time (Least Latency):
  Request goes to server with fewest connections AND lowest observed response time.
  ✅ Most adaptive. ❌ Requires LB to track response time metrics per backend.

IP Hash:
  hash(client_ip) mod N → determines server.
  ✅ Same client always goes to same server (crude sticky sessions).
  ❌ Breaks when servers are added/removed — rehashing changes all assignments.
  Better: consistent hashing (see databases-at-scale.md) for minimal disruption.

Random:
  Request goes to a random server.
  ✅ Extremely simple. Surprisingly effective for large N (birthday paradox effect).
  ❌ Worst-case imbalance possible; no load awareness.
```

**The power of two choices** (Michael Mitzenmacher, 1998 — widely used in production):
Instead of picking randomly, pick two random servers and route to the less-loaded one.
Exponentially better tail load distribution than pure random, with only one extra comparison.
Used in NGINX's `random two least_conn` directive and in Envoy's load balancing.

### Health Checks

A load balancer must route only to healthy backends. Two health check types:

```
Passive (circuit-breaker style): LB observes real traffic. If a backend returns 5xx
or times out repeatedly, mark it unhealthy and stop routing to it. Resume after
successful health check. Low overhead — no extra requests.

Active: LB sends periodic probes (HTTP GET /health, TCP connection) on a timer.
Standard for HTTP APIs — active probes catch failures before real traffic hits them.
```

```nginx
# NGINX upstream with active health checks
upstream api_backend {
    least_conn;
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
    server 10.0.0.3:3000;
    keepalive 32;  # connection pool to backends — reduces TCP handshake overhead
}

server {
    location / {
        proxy_pass http://api_backend;
        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;

        # Passive health check:
        proxy_next_upstream error timeout http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 2;
    }
}
```

### Stateless Services — The Prerequisite for Horizontal Scaling

A stateless service stores no user-specific state in process memory. Any instance can handle
any request. This is the single most important design property for horizontal scalability.

```
❌ STATEFUL (cannot horizontally scale arbitrarily):
  User logs in → session stored in Server A's memory
  Next request routes to Server B → session not found → user logged out

✅ STATELESS (horizontally scalable):
  User logs in → session token (JWT) returned to client
  Next request arrives at Server B with token → Server B validates token
  independently — no shared memory needed

  OR: session stored in Redis (external, shared)
  Server A writes session → Server B reads it → any server handles any request
```

**Moving state externally:**
- Session state → Redis (fast, in-memory, TTL support)
- User uploads / files → Object storage (S3, GCS — not local disk)
- Configuration → Environment variables or secret manager (not hard-coded)

### Database Read Replicas — The First Horizontal Database Scaling Step

Before sharding (see `references/databases-at-scale.md`), add read replicas:

```
                    ┌──────────────────┐
  Writes ──────────▶│  Primary (leader)  │
                    └─────────┬────────┘
                              │  async replication
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
  Reads ─────▶│ Replica 1 │ │ Replica 2 │ │ Replica 3 │
              └──────────┘ └──────────┘ └──────────┘
```

- Writes go to the primary; reads distribute across replicas
- Replicas are eventually consistent — lag is typically milliseconds but is non-zero
- Never read from a replica immediately after a write you depend on being consistent
  (post-write, route that user's next read to primary for a brief window — "read-your-writes")
- Postgres `max_standby_streaming_delay` and `synchronous_standby_names` tune the replication
  lag vs durability trade-off

Replicas can handle read-heavy workloads (reporting, search, analytics) without touching the
primary, which is reserved for writes and strongly-consistent reads.
