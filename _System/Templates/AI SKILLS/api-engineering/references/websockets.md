# WebSockets — Full-Duplex Real-Time Communication

**Sources:** IETF RFC 6455 (*The WebSocket Protocol*, December 2011 — Fette & Melnikov,
Google/Isode); RFC 7692 (permessage-deflate compression extension, 2015); RFC 8441 (WebSocket
over HTTP/2 bootstrapping, 2018); RFC 9220 (WebSocket over HTTP/3, 2022); OWASP WebSocket
Security Cheat Sheet (2024 edition); OWASP Web Security Testing Guide (WSTG-CLNT-10, 2025
edition, A01:2025 Broken Access Control); CVE-2024-37890 (ws library DoS, CVSS 7.5, fixed in
ws 8.17.1); WebSocket.org guides (Ably, March 2026).

---

## 1. What WebSockets Actually Are (and Are Not)

WebSocket is a **full-duplex, persistent communication protocol** over a single TCP connection,
standardized by IETF RFC 6455 in December 2011. Unlike HTTP, which follows a strict
request/response cycle, a WebSocket connection stays open and either side can send messages
to the other at any time — no polling, no repeated handshakes, no request needed to "ask" for
data.

```
HTTP (request/response — half-duplex):
  Client ──── GET /data ────▶ Server
  Client ◀─── 200 OK + data ── Server
  (connection may close)
  Client ──── GET /data ────▶ Server   ← must ask again for next update
  Client ◀─── 200 OK + data ── Server

WebSocket (full-duplex — both directions simultaneously):
  Client ──── HTTP Upgrade ────▶ Server
  Client ◀─── 101 Switching Protocols ── Server
  (TCP connection stays open)
  Client ◀────── push ────── Server    ← server sends at will
  Client ──────── push ─────▶ Server    ← client sends at will
  Client ◀────── push ────── Server    ← interleaved, no request needed
```

**Protocol extensions (beyond core RFC 6455):**
- RFC 7692 (2015) — `permessage-deflate` compression, reducing message size significantly for
  text-heavy workloads (JSON, HTML). Server negotiates via `Sec-WebSocket-Extensions` header.
- RFC 8441 (2018) — WebSocket bootstrapping over HTTP/2 (`CONNECT` with `protocol: websocket`),
  allowing WebSocket connections to share HTTP/2's single TCP connection and multiplexing.
- RFC 9220 (2022) — WebSocket over HTTP/3 (QUIC). No TCP head-of-line blocking; UDP-based.

**WebTransport (2021+, W3C/IETF):** a newer protocol over HTTP/3/QUIC that offers both
reliable streams and unreliable datagrams in the browser. Not a replacement — WebSocket
remains the dominant standard for 2026; WebTransport is useful for specific low-latency/datagram
use cases (gaming with acceptable packet loss, live video). Most production use cases should
still reach for WebSocket.

---

## 2. The Handshake — How an HTTP Connection Becomes a WebSocket

WebSocket connections always begin as standard HTTP requests. The client sends an HTTP/1.1
`Upgrade` request, and the server responds with `101 Switching Protocols`. After this, the
TCP connection switches to the WebSocket framing protocol — HTTP is no longer spoken.

```http
GET /ws/chat HTTP/1.1
Host: api.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
Sec-WebSocket-Protocol: chat, superchat
Origin: https://example.com
```

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
Sec-WebSocket-Protocol: chat
```

**`Sec-WebSocket-Key` / `Sec-WebSocket-Accept` mechanics:** the server concatenates the
client's key with the magic GUID `258EAFA5-E914-47DA-95CA-C5AB0DC85B11` (defined in RFC 6455),
computes SHA-1, and base64-encodes the result. This proves the server actually read and
understood the handshake — it's not a security mechanism (it's not a secret), it's a protocol
correctness check to prevent accidental WebSocket connections from non-WebSocket clients.

**Critical security point — the handshake is the ONLY moment you can use HTTP mechanisms:**
HTTP headers (including `Authorization`, `Cookie`, `Origin`) are only available during the
handshake. After `101`, the connection is raw TCP frames — no HTTP, no headers. This has major
implications for authentication (see Section 4).

---

## 3. Node.js Implementation — ws (Native) and Socket.IO

### Option A: `ws` — The Low-Level Standard Library

```bash
pnpm add ws
pnpm add -D @types/ws
```

```typescript
// server/websocket.ts
import { WebSocket, WebSocketServer } from "ws";
import http from "http";

const server = http.createServer(app);  // share with Express
const wss = new WebSocketServer({
  server,
  maxPayload: 1024 * 1024,  // 1MB — always set; default is 100MB (DoS risk)
});

wss.on("connection", (ws: WebSocket, req: http.IncomingMessage) => {
  // Validate origin during handshake
  const origin = req.headers.origin;
  if (!isAllowedOrigin(origin)) {
    ws.close(1008, "Origin not allowed");
    return;
  }

  // Authenticate during handshake (see Section 4)
  const token = extractTokenFromHandshake(req);
  const user = verifyToken(token);
  if (!user) {
    ws.close(1008, "Unauthorized");
    return;
  }

  // Heartbeat tracking
  (ws as any).isAlive = true;
  ws.on("pong", () => { (ws as any).isAlive = true; });

  ws.on("message", (data: Buffer, isBinary: boolean) => {
    // ALWAYS validate incoming messages — treat as untrusted input (OWASP)
    const text = isBinary ? data : data.toString("utf8");
    const parsed = safeParseJson(text);
    if (!parsed) { ws.close(1007, "Invalid message"); return; }

    handleMessage(ws, user, parsed);
  });

  ws.on("close", (code: number, reason: Buffer) => {
    console.log(`Connection closed: ${code} — ${reason.toString()}`);
  });

  ws.on("error", (err: Error) => {
    console.error("WebSocket error:", err);
    // Do NOT re-throw — errors on individual connections must not crash the server
  });
});

// Ping/pong heartbeat — detect dead connections (crucial for servers with many clients)
const heartbeat = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!(ws as any).isAlive) {
      ws.terminate();  // terminate, don't close — assumes the connection is already dead
      return;
    }
    (ws as any).isAlive = false;
    ws.ping();
  });
}, 30_000);

wss.on("close", () => clearInterval(heartbeat));
```

```typescript
// client/websocket.ts — browser client with reconnection
class ReconnectingWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private readonly maxAttempts = 10;

  connect(): void {
    this.ws = new WebSocket(
      `wss://api.example.com/ws/chat?token=${getToken()}`,  // token in URL query for browser clients
    );

    this.ws.addEventListener("open", () => {
      this.reconnectAttempts = 0;  // reset on successful connection
    });

    this.ws.addEventListener("message", (event) => {
      const data = JSON.parse(event.data as string);
      this.handleMessage(data);
    });

    this.ws.addEventListener("close", (event) => {
      if (!event.wasClean && this.reconnectAttempts < this.maxAttempts) {
        // Exponential backoff reconnect — same algorithm as HTTP retries
        const delay = Math.min(1000 * 2 ** this.reconnectAttempts, 30_000);
        const jittered = delay * (0.75 + Math.random() * 0.5);
        setTimeout(() => { this.reconnectAttempts++; this.connect(); }, jittered);
      }
    });
  }

  send(message: unknown): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }
}
```

### Option B: Socket.IO — Abstraction Layer with Rooms and Fallbacks

Socket.IO wraps WebSocket with automatic fallback to long-polling, built-in rooms (namespaced
channels), acknowledgement callbacks, and automatic reconnection. Use it when: you need
rooms/namespaces, acknowledgements, or IE11/proxy-restricted environment fallback support.
Use raw `ws` when: you want minimal overhead, full protocol control, or are building a backend
service (not browser-facing).

```typescript
// server — socket.io with auth middleware
import { Server } from "socket.io";
import { createServer } from "http";

const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: process.env.ALLOWED_ORIGINS?.split(","), credentials: true },
  maxHttpBufferSize: 1e6,  // 1MB — equivalent to ws maxPayload
});

// Authentication middleware — runs on every new connection attempt
io.use((socket, next) => {
  const token = socket.handshake.auth.token as string | undefined;
  if (!token) return next(new Error("Missing authentication token"));
  const user = verifyToken(token);
  if (!user) return next(new Error("Invalid token"));
  socket.data.user = user;
  next();
});

io.on("connection", (socket) => {
  const user = socket.data.user as AuthenticatedUser;

  // Join user-specific and role-specific rooms
  socket.join(`user:${user.id}`);
  socket.join(`role:${user.role}`);

  socket.on("message:send", async (payload: MessagePayload, ack) => {
    // Authorization check per action — connection ≠ authorization for all actions
    if (!canSendMessage(user, payload.roomId)) {
      return ack({ error: "Forbidden" });
    }
    const message = await messageService.create(user.id, payload);
    io.to(`room:${payload.roomId}`).emit("message:new", message);
    ack({ messageId: message.id });  // acknowledgement to sender
  });
});

// Targeted server-to-client push (from anywhere in your codebase):
io.to(`user:${userId}`).emit("notification", { type: "order_shipped", orderId });
```

### Python — WebSockets Library (ASGI)

```python
# FastAPI + websockets — native ASGI WebSocket support (no separate library needed)

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)) -> None:
    # Authenticate BEFORE accepting — reject during handshake
    user = await verify_token(token)
    if not user:
        await websocket.close(code=1008, reason="Unauthorized")
        return

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            # Validate every message — treat as untrusted input
            validated = await validate_message(data)
            response = await handle_message(user, validated)
            await websocket.send_json(response)

    except WebSocketDisconnect as e:
        logger.info("WebSocket disconnected", code=e.code)
    except Exception as e:
        logger.error("WebSocket error", error=str(e))
        await websocket.close(code=1011, reason="Internal error")
```

---

## 4. Authentication & Authorization (the Hard Part)

**The WebSocket authentication problem:** HTTP headers are only available during the HTTP
upgrade handshake. Standard Authorization headers can be sent in the upgrade request, but the
browser's WebSocket API (`new WebSocket(url)`) does not allow setting custom headers before
the connection opens — making header-based auth impossible from browser clients.

### Recommended Approaches

**Option 1 — Token in URL query parameter (most common for browser clients):**
```typescript
// Client
const ws = new WebSocket(`wss://api.example.com/ws?token=${accessToken}`);

// Server — extract and validate during handshake, before accepting
wss.on("headers", (headers, req) => {
  const url = new URL(req.url!, "http://placeholder");
  const token = url.searchParams.get("token");
  // Token validation happens in the verifyClient callback below
});

const wss = new WebSocketServer({
  server,
  verifyClient: ({ req }) => {
    const url = new URL(req.url!, "http://placeholder");
    const token = url.searchParams.get("token");
    const user = verifyToken(token ?? "");
    if (!user) return false;  // reject with 401
    (req as any).user = user;  // attach user to request for later use
    return true;
  },
});
```

**Security note:** tokens in query parameters can appear in server logs and proxy access logs.
Mitigate by: using short-lived tokens (≤ 5 minutes TTL) specifically for WebSocket connections,
generated via a dedicated endpoint the client calls before connecting; rotating them; and
configuring your web server/proxy to not log query strings.

**Option 2 — Cookie (for browser clients in same-origin setups):**
```typescript
// Browser automatically sends cookies on WebSocket connections to the same origin
// Server extracts the session cookie during handshake
const wss = new WebSocketServer({
  verifyClient: ({ req }) => {
    const sessionId = parseCookies(req.headers.cookie ?? "")["session_id"];
    const user = validateSession(sessionId);
    return !!user;
  },
});
```

**Option 3 — First-message auth (for non-browser clients / internal services):**
```typescript
// Server accepts the connection, then expects authentication as the first message
// within a timeout — close if auth doesn't arrive in time
wss.on("connection", (ws) => {
  const authTimeout = setTimeout(() => {
    ws.close(1008, "Authentication timeout");
  }, 5_000);  // 5 seconds to send credentials

  ws.once("message", (data) => {
    clearTimeout(authTimeout);
    const msg = JSON.parse(data.toString());
    if (msg.type !== "auth" || !verifyToken(msg.token)) {
      ws.close(1008, "Unauthorized");
      return;
    }
    (ws as any).user = decodeToken(msg.token);
    ws.send(JSON.stringify({ type: "auth_ok" }));
    // Set up normal message handler now
    ws.on("message", handleAuthenticatedMessage);
  });
});
```

**Authorization per message — mandatory (OWASP):**

A WebSocket connection being authenticated does NOT authorize every action the client
might request through it. Authorization must be re-checked per action:

```typescript
ws.on("message", (data) => {
  const msg = JSON.parse(data.toString());

  switch (msg.action) {
    case "chat:send":
      if (!canSendToRoom(user, msg.roomId)) {
        ws.send(JSON.stringify({ error: "Forbidden", action: msg.action }));
        return;
      }
      break;
    case "admin:kick":
      if (user.role !== "admin") {
        ws.send(JSON.stringify({ error: "Admin only", action: msg.action }));
        return;
      }
      break;
  }
});
```

---

## 5. Security (OWASP WebSocket Security Cheat Sheet, 2024)

### Cross-Site WebSocket Hijacking (CSWSH) — the WebSocket CSRF

An attacker's website can open a WebSocket to your API if your server doesn't validate the
`Origin` header. Unlike CSRF in HTTP, there's no SameSite cookie attribute or CSRF token to
save you — WebSocket connections bypass these. Validate the `Origin` header **during the
handshake** as the primary defense.

```typescript
const ALLOWED_ORIGINS = new Set(process.env.ALLOWED_ORIGINS!.split(","));

const wss = new WebSocketServer({
  verifyClient: ({ origin }) => {
    if (!ALLOWED_ORIGINS.has(origin)) {
      console.warn(`Rejected WebSocket from disallowed origin: ${origin}`);
      return false;
    }
    return true;
  },
});
```

### Always Use `wss://` (TLS) in Production

`ws://` (unencrypted) is equivalent to `http://` — all traffic is plaintext. `wss://` is
WebSocket over TLS, equivalent to `https://`. OWASP A04:2025 (Cryptographic Failures)
explicitly calls this out.

### Input Validation — Every Message is Untrusted (OWASP A05:2025 — Injection)

```typescript
ws.on("message", (data) => {
  let parsed: unknown;
  try {
    parsed = JSON.parse(data.toString());
  } catch {
    ws.close(1007, "Invalid data format");  // close code 1007 = invalid data
    return;
  }

  // Validate with Zod (TypeScript) or Pydantic (Python) — same discipline as HTTP
  const result = MessageSchema.safeParse(parsed);
  if (!result.success) {
    ws.send(JSON.stringify({ error: "Validation failed" }));
    return;
  }

  processMessage(result.data);
});
```

### Resource Limits — Prevent DoS

```typescript
const wss = new WebSocketServer({
  maxPayload: 1024 * 1024,  // 1MB max message size — always set explicitly
});

// Message rate limiting — apply per connection, not just per IP
const messageCount = new Map<WebSocket, number>();

ws.on("message", () => {
  const count = (messageCount.get(ws) ?? 0) + 1;
  messageCount.set(ws, count);
  if (count > 100) {  // 100 messages per minute
    ws.close(1008, "Rate limit exceeded");
    return;
  }
});
setInterval(() => messageCount.clear(), 60_000);  // reset counter each minute
```

**CVE-2024-37890 (ws library, CVSS 7.5):** sending a WebSocket request with more headers
than `server.options.maxHeadersCount` allows could crash the ws server. Fixed in ws 8.17.1
(backported to 7.5.10, 6.2.3, 5.2.4). **If you haven't updated `ws` since mid-2024, check
your version now.**

### Dependency: Keep WebSocket Libraries Updated

```bash
# Check for known vulnerabilities
pnpm audit
# Update ws specifically
pnpm update ws
```

---

## 6. Horizontal Scaling — The Key Operational Challenge

A WebSocket is a stateful, persistent connection between one client and one server instance.
When you run multiple server instances behind a load balancer, a message broadcasted on
Instance A doesn't reach clients connected to Instance B — unless you add a shared message
bus.

```
                  Load Balancer
                 /              \
            Instance A         Instance B
            [Client 1]         [Client 2]
            [Client 3]         [Client 4]

If Instance A wants to broadcast to ALL clients,
it must publish to a shared bus — not call wss.clients.forEach directly.
```

**Solution 1 — Redis Pub/Sub (most common for Node.js):**

```typescript
import { createClient } from "redis";

const publisher = createClient({ url: process.env.REDIS_URL });
const subscriber = createClient({ url: process.env.REDIS_URL });

await subscriber.subscribe("ws:broadcast", (message) => {
  const payload = JSON.parse(message);
  // Deliver to clients connected to THIS instance
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
});

// To broadcast from anywhere:
async function broadcastToAll(payload: unknown) {
  await publisher.publish("ws:broadcast", JSON.stringify(payload));
}

// For targeted messages (to a specific user):
async function sendToUser(userId: string, payload: unknown) {
  await publisher.publish(`ws:user:${userId}`, JSON.stringify(payload));
}
```

**Solution 2 — Sticky sessions (simpler, but fragile):**
Configure the load balancer to route all connections from the same client to the same instance
(based on IP or a cookie). Fragile because it breaks when an instance goes down mid-session,
and unbalances load when clients reconnect. Redis Pub/Sub scales better.

**Solution 3 — Managed WebSocket infrastructure (avoid reinventing):**
Ably, Pusher, Soketi (open-source Pusher-compatible), and LiveKit abstract the entire
horizontal scaling problem. For most teams, using a managed service for WebSocket delivery
is the right choice — real-time infrastructure is a solved problem with significant operational
complexity that doesn't need to be rebuilt for most use cases.

---

## 7. WebSocket Close Codes (RFC 6455 Section 7.4)

| Code | Name | Use when |
|---|---|---|
| 1000 | Normal Closure | Both sides finished normally |
| 1001 | Going Away | Server shutting down, or client navigating away |
| 1002 | Protocol Error | Protocol violation detected |
| 1003 | Unsupported Data | Received unexpected data type |
| 1007 | Invalid Frame Payload | UTF-8 decode failure in text frame |
| 1008 | Policy Violation | Auth failure, rate limit exceeded |
| 1009 | Message Too Big | Payload exceeds configured limit |
| 1011 | Internal Error | Unexpected server error |
| 1012 | Service Restart | Server restarting — client should reconnect |
| 1013 | Try Again Later | Temporary overload — client should retry with backoff |

**Always use close codes meaningfully** — they help clients decide whether to reconnect
immediately (1012), back off (1013), or not reconnect at all (1008 — auth failure).

---

## 8. When NOT to Use WebSockets

- **The data only flows one direction from server to client** — Server-Sent Events (SSE) over
  HTTP/2 is simpler, uses standard HTTP (proxies, load balancers, CDNs handle it without
  special config), and multiplexes over a single TCP connection; use SSE for notification
  feeds, dashboards, live logs
- **Infrequent updates tolerate some latency** — polling every few seconds is far simpler to
  implement, monitor, and debug; the complexity of persistent connections is not justified
  unless you need sub-second latency or frequent bidirectional messages
- **Request-response is the natural interaction model** — REST is designed for this; using
  WebSocket to send a message and wait for a specific reply is reinventing HTTP's semantics
  with more complexity
- **Heavy proxy/firewall environments** — some corporate proxies and firewalls drop WebSocket
  upgrade requests or terminate long-lived connections; SSE or long-polling degrade more
  gracefully in these environments (Socket.IO's fallback was built precisely for this)
- **The team has no prior WebSocket operational experience** — horizontal scaling, heartbeat
  management, connection lifecycle handling, and auth are genuinely more complex than HTTP
  APIs; a managed service (Ably, Pusher, Soketi) or SSE is often the correct first choice
