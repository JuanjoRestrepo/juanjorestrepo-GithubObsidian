# Networking & Protocols

## 1. What Happens When You Type a URL Into a Browser

A complete walkthrough — useful as a system design interview answer and as a mental model for
debugging latency at any layer:

1. **DNS resolution** — browser checks its own cache, then OS cache, then a resolver (ISP or
   public resolver like 8.8.8.8). If uncached, the resolver queries root nameserver → TLD
   nameserver (`.com`) → authoritative nameserver for the domain, returning the IP. Each level
   caches per the record's TTL.
2. **TCP handshake** — SYN → SYN-ACK → ACK three-way handshake. This RTT is pure overhead
   before any data moves — one reason HTTP/2 and HTTP/3 emphasize connection reuse.
3. **TLS handshake** — client and server negotiate TLS version and cipher suite, exchange and
   validate certificates, derive a shared session key. TLS 1.3 reduced this to one RTT (down
   from two in TLS 1.2) and supports 0-RTT resumption for repeat connections.
4. **HTTP request** — browser sends the request over the encrypted connection.
5. **Server processing** — request hits load balancer → application server (or CDN edge cache
   if cacheable) → app queries DB/cache → response assembled.
6. **Response rendered** — browser parses HTML; discovers additional resources (CSS, JS,
   images); each may trigger its own DNS + TCP + TLS cycle unless already connected. Hence the
   value of HTTP/2 multiplexing and CDN-hosted shared assets that may already be cached.

---

## 2. TCP vs. UDP

|             | TCP                                                      | UDP                                                                          |
| ----------- | -------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Connection  | Connection-oriented (handshake required)                 | Connectionless                                                               |
| Reliability | Guaranteed delivery, retransmission, ordering            | No guarantees — packets may be lost, duplicated, or arrive out of order      |
| Overhead    | Higher (acks, flow control, congestion control)          | Minimal                                                                      |
| Use case    | Anything needing correctness: HTTP, email, file transfer | Latency-sensitive, loss-tolerant: video/voice streaming, gaming, DNS queries |

Real-time media deliberately chooses UDP: a dropped packet representing 20ms of audio is less
harmful than TCP retransmitting it and stalling everything behind it (head-of-line blocking).
This is also the motivation behind QUIC (HTTP/3's transport).

---

## 3. HTTP/1.1 → HTTP/2 → HTTP/3

|                       | HTTP/1.1                                  | HTTP/2                                                                               | HTTP/3                                                           |
| --------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Transport             | TCP                                       | TCP                                                                                  | QUIC (over UDP)                                                  |
| Multiplexing          | No — one request per connection at a time | Yes — multiple streams over one connection                                           | Yes — independent streams, no cross-stream head-of-line blocking |
| Head-of-line blocking | Severe at app layer                       | Reduced (app layer); still present at TCP layer (one lost packet blocks all streams) | Eliminated — QUIC streams are independent at the transport layer |
| Header compression    | None                                      | HPACK                                                                                | QPACK                                                            |
| Connection setup      | TCP + TLS handshake                       | Same as HTTP/1.1                                                                     | Combined transport + TLS 1.3 — fewer RTTs; 0-RTT resumption      |

HTTP/2 fixed application-layer inefficiency (multiplexing over one connection). HTTP/3 fixes
the underlying transport — a single lost packet no longer stalls unrelated streams. Most
relevant for high-latency or lossy networks (mobile).

---

## 4. Load Balancer vs. Reverse Proxy vs. API Gateway

|               | Load Balancer                                        | Reverse Proxy                                                 | API Gateway                                                                     |
| ------------- | ---------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Primary job   | Distribute traffic across multiple backend instances | Forward client requests to a backend, hiding backend topology | Manage full API traffic lifecycle: routing, auth, rate limiting, transformation |
| Typical scope | Traffic distribution + health checks                 | Single entry point; can also cache/compress/terminate TLS     | Cross-cutting API concerns across many microservices                            |
| Example       | AWS ALB/NLB, HAProxy                                 | nginx                                                         | Kong, AWS API Gateway, Apigee                                                   |

These often coexist: client → CDN → API gateway (auth, rate limiting, routing) → load balancer
(distributes to healthy instances) → reverse proxy on the instance (nginx in front of the app
process) → application. Smaller systems collapse several layers into one component.

---

## 5. Forward Proxy vs. Reverse Proxy

- **Forward proxy** — sits in front of the _client_; makes requests on the client's behalf to
  external servers. The external server sees the proxy, not the client. Used for client-side
  anonymity, content filtering, corporate egress control.
- **Reverse proxy** — sits in front of the _server_; receives client requests on the server's
  behalf. The client sees the proxy, not the backend. Used for load balancing, TLS termination,
  caching, hiding internal network topology.

The distinguishing question: forward proxy hides the _client_ from the destination; reverse
proxy hides the _destination_ (backend) from the client.

---

## 6. DNS Record Types

| Record | Purpose                                                       |
| ------ | ------------------------------------------------------------- |
| A      | Hostname → IPv4 address                                       |
| AAAA   | Hostname → IPv6 address                                       |
| CNAME  | Alias — hostname → another hostname                           |
| MX     | Mail exchange — where to deliver email for the domain         |
| TXT    | Arbitrary text — domain verification, SPF/DKIM authentication |
| NS     | Delegates a subdomain to specific nameservers                 |
| SOA    | Start of authority — administrative info about the DNS zone   |

---

## 7. Common Ports Reference

| Port  | Protocol / Service                    |
| ----- | ------------------------------------- |
| 22    | SSH                                   |
| 25    | SMTP                                  |
| 53    | DNS                                   |
| 80    | HTTP                                  |
| 443   | HTTPS                                 |
| 3306  | MySQL                                 |
| 5432  | PostgreSQL                            |
| 6379  | Redis                                 |
| 8080  | Alternate HTTP (dev servers, proxies) |
| 9092  | Kafka                                 |
| 27017 | MongoDB                               |
