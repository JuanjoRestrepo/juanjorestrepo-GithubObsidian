# Microservices vs Modular Monolith

**Sources:** Sam Newman, *Building Microservices* (2015, 2nd ed. 2021) — the canonical
industry reference; Martin Fowler's writing on the "Monolith First" strategy and the
"Distributed Monolith" anti-pattern; Melvin Conway's Conway's Law (1967) — team structure
inevitably shapes system architecture. Language-agnostic at the decision level; the trade-offs
discussed apply whether services are written in TypeScript, Python, Java, Go, or any mix.

---

## The Decision Is About Organization, Not Technology

The most common mistake in this decision is treating it as a technical choice ("microservices
are more scalable") when it is primarily an **organizational and operational** choice. A single
well-architected monolith can scale to enormous load (Shopify, GitHub, and Stack Overflow all
ran/run substantially monolithic for years at large scale). Microservices solve a coordination
problem between teams more than they solve a technical scaling problem.

---

## Modular Monolith

A single deployable application, internally organized into strict modules with enforced
boundaries — each module owns its own data access and exposes only a defined interface to
other modules. It is a monolith at the deployment level and (ideally) a well-bounded set of
domains at the code level.

```
┌─────────────────────────────────────────────────────────┐
│                  Single Deployable Application              │
│                                                             │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │
│  │  Orders Module  │  │ Inventory Module│  │ Billing Module │  │
│  │                │  │                │  │                │  │
│  │  - own tables   │  │  - own tables   │  │  - own tables   │  │
│  │  - own service  │  │  - own service  │  │  - own service  │  │
│  │  - public API   │◀─┼─ calls via     │  │  - public API   │  │
│  │    (interface)  │  │    interface   │  │                │  │
│  └───────────────┘  └───────────────┘  └───────────────┘  │
│         ▲                                        ▲          │
│         └────────────────────────────────────────┘          │
│              modules call each other's PUBLIC interface       │
│              only — never reach into another module's data    │
└─────────────────────────────────────────────────────────┘
                  Single database, single deploy
```

### Enforcing Module Boundaries in Code

```typescript
// src/modules/orders/index.ts — the ONLY file other modules may import from
export { OrderService } from "./order-service";
export type { Order, OrderStatus } from "./types";
// Everything else in this module (repositories, internal helpers) is NOT exported

// src/modules/billing/invoice-service.ts
// ✅ CORRECT — imports only the public interface
import { OrderService } from "@/modules/orders";

// ❌ WRONG — reaching into another module's internals
// import { OrderRepository } from "@/modules/orders/internal/order-repository";
```

Enforce this at the tooling level, not just by convention — ESLint's `import/no-restricted-paths`
or a dedicated tool like `dependency-cruiser` can fail the build if a module imports another
module's internals directly:

```javascript
// .dependency-cruiser.js
module.exports = {
  forbidden: [
    {
      name: "no-cross-module-internals",
      severity: "error",
      from: { path: "^src/modules/([^/]+)" },
      to: {
        path: "^src/modules/([^/]+)/(?!index)",
        pathNot: "^src/modules/$1", // allow importing your OWN module's internals
      },
    },
  ],
};
```

### Why Start Here

- Single deployment, single database transaction spanning multiple modules when genuinely
  needed (e.g., placing an order and decrementing inventory atomically) — no distributed
  transaction complexity
- Refactoring module boundaries is a code change, not a service migration project
- One CI/CD pipeline, one set of logs, one process to monitor — dramatically lower operational
  overhead for small-to-medium teams
- If module boundaries turn out wrong, they're cheap to fix; wrong microservice boundaries are
  expensive to fix (requires data migration, API versioning, coordinated deploys)

---

## Microservices

Multiple independently deployable services, each owning its own data store, communicating over
the network (REST, gRPC, or asynchronously via events — see `references/cqrs-event-driven.md`).

```
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│  Order Service  │      │ Inventory Service│      │ Billing Service │
│                │      │                │      │                │
│  own DB         │      │  own DB         │      │  own DB         │
│  own deploy     │      │  own deploy     │      │  own deploy     │
│  own team       │      │  own team       │      │  own team       │
└───────┬───────┘      └───────┬───────┘      └───────┬───────┘
        │      REST / gRPC / events over the network     │
        └──────────────────────┼──────────────────────────┘
                                ▼
                      API Gateway / Service Mesh
```

### The Distributed Monolith Anti-Pattern

The single most common failure mode when adopting microservices too early: services are split
by deployment but remain tightly coupled at the logic and data level — synchronous call chains
several services deep, shared databases between "independent" services, or a deploy of Service
A requiring a coordinated deploy of Service B. This configuration has **all the operational
cost of microservices with none of the independence benefit**.

```
❌ DISTRIBUTED MONOLITH (the failure mode):

Order Service ──sync call──▶ Inventory Service ──sync call──▶ Pricing Service ──sync call──▶ Tax Service

One request to place an order now requires 4 services to all be up, all respond in time,
and none of them can deploy a breaking change independently — this is a monolith with
network calls between its function boundaries, and all the network calls have made it
SLOWER and LESS reliable than the monolith it replaced.
```

**Diagnostic questions to detect this in an existing system:**
- Can each service be deployed independently, on its own schedule, without coordinating with
  other teams? If not — distributed monolith.
- Does a single user-facing request require a deep synchronous chain across 4+ services? If
  so — reconsider whether those should be one service, or whether the chain should become
  asynchronous/event-driven.
- Do two "independent" services share a database or tables? If so, they are not actually
  independent — this is the most damaging version of the anti-pattern.

### When Microservices Genuinely Earn Their Cost

- **Team size and Conway's Law:** once an engineering org grows past roughly 8-10 engineers
  per domain area, a single monolith codebase becomes a coordination bottleneck — merge
  conflicts, deploy queues, unclear ownership. Splitting along the bounded contexts already
  identified via DDD (see `references/ddd.md`) gives each team true deployment independence.
- **Genuinely different scaling profiles:** a video transcoding service and a user profile
  service have wildly different resource needs (CPU-heavy batch vs. lightweight request/
  response) — splitting them allows independent, appropriately-sized infrastructure.
- **Independent technology needs:** a machine learning inference service justifiably wants
  Python; the main web app is TypeScript — microservices allow this without forcing one
  language across the whole system.
- **Regulatory/compliance isolation:** a payments processing component may need PCI-DSS scope
  isolation that's cleaner to achieve as a genuinely separate, network-isolated service.

### Migration Path — Monolith to Microservices (Strangler Fig)

Never attempt a full rewrite. Extract one bounded context at a time, behind a routing layer
that gradually shifts traffic from the monolith to the new service.

```
Step 1: Monolith handles everything, including Billing
┌──────────────────────────────────┐
│           Monolith                 │
│  Orders │ Inventory │  Billing      │
└──────────────────────────────────┘

Step 2: New Billing Service built alongside; router directs SOME traffic to it
┌──────────────────────────────────┐    ┌───────────────┐
│           Monolith                 │    │ Billing Service │
│  Orders │ Inventory │ [Billing]     │◀──▶│   (new)         │
└──────────────────────────────────┘    └───────────────┘
      Router gradually shifts 100% of Billing traffic to the new service

Step 3: Billing fully extracted; monolith's Billing module is deleted
┌──────────────────────────────────┐    ┌───────────────┐
│           Monolith                 │    │ Billing Service │
│      Orders │ Inventory           │───▶│                │
└──────────────────────────────────┘    └───────────────┘
```

This is the Strangler Fig pattern (Fowler) — the new service grows around the old
functionality until the old code path can be safely removed, with the ability to roll back to
the monolith path at any point during the transition if issues arise.

---

## Integration Patterns Between Services

### Synchronous — REST / gRPC

Use when the caller needs an immediate response to proceed (e.g., checking payment
authorization before confirming an order).

```typescript
// gRPC is preferred over REST for internal service-to-service calls:
// strongly-typed contracts (protobuf), lower latency, native streaming support
// REST remains preferred for public-facing / external APIs (see api-first-integration-nfrs.md)
```

**Resilience is mandatory for synchronous inter-service calls** — see the Circuit Breaker and
Retry patterns in `references/api-first-integration-nfrs.md` (NFR: Reliability section). A
synchronous call chain without these patterns turns one service's outage into a cascading
failure across every service that calls it.

### Asynchronous — Events

Use when the caller doesn't need to wait for the result, or when decoupling deploy/failure
domains matters more than immediate consistency. Full pattern and message broker comparison in
`references/cqrs-event-driven.md`.

### API Gateway

A single entry point that routes external requests to the appropriate internal service,
often also handling cross-cutting concerns (auth, rate limiting, request logging) so
individual services don't each reimplement them.

```
Client ──▶ API Gateway ──┬──▶ Order Service
                          ├──▶ Inventory Service
                          └──▶ Billing Service

Gateway handles: auth verification, rate limiting, request routing, response aggregation
```

### Backend for Frontend (BFF)

When multiple client types (web, mobile, third-party partners) need different shapes of the
same underlying data, a BFF is a thin service per client type that aggregates and reshapes
calls to the backend services — avoiding one generic API trying to serve every client's needs
awkwardly.

---

## When NOT to Use Microservices (Over-Engineering Check)

This is the most over-adopted pattern in modern software architecture — reached for based on
what large companies do publicly, not based on the requirements of the system actually being
built.

**Do not use microservices when:**
- The team is smaller than ~8-10 engineers — a modular monolith gives nearly all the code
  organization benefit without any of the distributed systems tax (network failures,
  distributed tracing, service discovery, data consistency across service boundaries)
- The domain boundaries are not yet well understood — splitting into services locks in
  boundaries that are expensive to change; get the boundaries right inside a monolith first
  (using DDD's bounded contexts), then extract services once boundaries have proven stable
- There's no genuine scaling asymmetry or team-coordination problem driving the decision —
  "microservices are the modern way to build software" is not a valid justification
- The team has no experience operating distributed systems (service discovery, distributed
  tracing, eventual consistency, network partition handling) — the learning curve is real and
  mistakes here cause production incidents, not just slower feature delivery

**Warning sign of over-application:** a team of 4 engineers running 15 microservices, each in
its own repo, each requiring its own CI/CD pipeline, its own on-call rotation understanding,
and its own database — for a product with modest traffic and a single, cohesive domain. This
consumes the majority of engineering time on operational overhead (deploying, monitoring,
debugging cross-service issues) rather than building features. The correct fix is almost
always consolidation back toward a modular monolith, not further splitting.

**The single best heuristic (Newman, paraphrased):** if you can't clearly articulate which
team owns which service and why that team needs independent deployment — you don't need
microservices yet. Start with a modular monolith with clean internal boundaries; those
boundaries are also exactly what you'll extract into services later, if and when the
organizational need genuinely arises.

---

## Sam Newman's Model — *Building Microservices* (O'Reilly, 2nd ed. 2021)

*Building Microservices* (O'Reilly, 2021) is the definitive industry reference on the topic.
The second edition refined three foundational ideas that the first edition (2015) treated
less precisely: information hiding as the core boundary principle, coupling as the primary
risk metric, and independent deployability as the non-negotiable test of a genuine
microservice. These are summarized below.

### Independent Deployability — The Non-Negotiable Test

Newman's most important clarification in the second edition: a microservice is defined by
**independent deployability**, not by size, not by the number of lines of code, not by
running in a container.

> "I want to stress this point: if you take only one thing from this book, it should be
> this: ensure that you embrace the concept of independent deployability of your
> microservices." — Sam Newman, Building Microservices, 2nd ed., Ch. 1

**Independent deployability means:** you can deploy a new version of Service A without
requiring any coordinated change to Service B, Service C, or any other service in the
system — and you can do this safely without knowing what version of Service A every consumer
is currently running.

This is only achievable when services are **loosely coupled** at the interface level. A
service that exposes a contract it can never break (because breaking it would require
coordinated deployment of 10 other services simultaneously) is not independently deployable
in practice, even if it deploys in isolation technically.

### Information Hiding — The Boundary Principle

Newman grounds microservice boundary design in David Parnas's 1972 paper "On the Criteria
to Be Used in Decomposing Systems into Modules" (ACM Communications): the key criterion for
module decomposition is **information hiding** — each module should hide design decisions
that are likely to change, exposing only a stable interface.

Applied to microservices: each service should hide its internal implementation details
(database schema, business logic, data structures) completely behind a stable API contract.
If changing a service's internal schema requires changes to consumers, information hiding
has been violated — the internal detail has leaked.

```
✅ INFORMATION HIDING — contract is stable:
  Order Service exposes: GET /orders/{id} → OrderResponse (id, status, total)
  Internal: Postgres schema changes from orders table to orders + order_items table
  Consumers: unaffected — they never knew about the schema

❌ LEAKY ABSTRACTION — internal detail exposed:
  Order Service returns raw DB column names in the response
  Schema change → every consumer's field mappings break → coordinated deploy required
```

### Coupling Types — Newman's Four Categories

Newman's second edition introduces a precise taxonomy of coupling types, ordered by severity.
Identifying which type of coupling exists in your system determines the correct fix.

```
Most acceptable → Least acceptable:

Domain Coupling
Pass-Through Coupling
Common Coupling
Content Coupling  ← most damaging
```

**Domain Coupling (acceptable — unavoidable in a distributed system):**
Service A must call Service B because A's operation genuinely depends on B's domain
capability. An Order Service calling a Payment Service for authorization is domain coupling.
It's unavoidable in a system where services are decomposed along business domains.

Minimize it by designing services to be as self-contained as possible; question whether
a call to another service is truly necessary or whether the data can be replicated.

```
Order Service ──calls──▶ Payment Service
(needs payment authorization — domain coupling, acceptable)
```

**Pass-Through Coupling (moderate risk — refactor the API):**
Service A receives data only to forward it to Service C, without using it itself. A
change to what Service C needs now requires a change to Service A's contract — even though
A has no business reason to be involved.

```
❌ Pass-Through Coupling:
API Gateway ──passes customer data──▶ Order Service ──forwards customer data──▶ Notification Service
(Order Service doesn't need customer data; it's just a pass-through)

✅ Fix: Notification Service gets the event with an orderId; fetches customer data directly
from Customer Service if it needs it, or event includes all needed data at origin.
```

**Common Coupling (high risk — extract shared ownership):**
Multiple services share a common resource — typically a shared database, shared config, or
shared mutable state. A change to the schema or config affects all services simultaneously.
Deploying Service A may require a schema migration that breaks Service B.

```
❌ Common Coupling (shared database):
Order Service ──reads/writes──▶ ┌─────────────┐ ◀──reads/writes── Inventory Service
                                  │ Shared DB    │
                                  └─────────────┘

✅ Fix: each service owns its own database; data shared by reference (orderId) not by
shared access. Services communicate via API or events, not shared tables.
```

**Content Coupling (most severe — indicates wrong service boundary):**
Service A reaches directly into Service B's internal implementation — calling private
methods, reading internal database tables, accessing B's in-memory state directly.
This is the worst form; it violates information hiding completely.

In practice: this usually manifests as Service A reading directly from Service B's
database rather than going through B's API. A schema change in B breaks A immediately.

```
❌ Content Coupling:
Order Service ──SELECT * FROM inventory.stock_items──▶ Inventory DB
(Order Service bypasses Inventory Service's API entirely)

✅ Fix: Order Service calls Inventory Service's API:
Order Service ──GET /inventory/items/{id}/availability──▶ Inventory Service ──▶ its own DB
```

### Cohesion — The Positive Counterpart to Coupling

While coupling describes what should be separated, cohesion describes what should be together.
Newman applies Robert Martin's cohesion principle: **"gather together the things that change
for the same reason; separate those things that change for different reasons."**

A service with high cohesion handles one clear business capability. When a feature request
changes the behavior of that capability, it changes code in one service. If a single feature
request routinely changes code in 5 services — the boundaries are wrong; the capability is
too fragmented.

### Communication Styles — *Building Microservices* Chapter 4

Newman distinguishes communication by two axes: synchronicity and interaction style.

```
                    Request/Response          Event-Driven
                 ┌──────────────────────┬─────────────────────┐
  Synchronous    │ REST (most common)    │ (rare — sync events │
                 │ gRPC                  │  usually polling)   │
                 ├──────────────────────┼─────────────────────┤
  Asynchronous   │ REST + polling        │ Message broker      │
                 │ gRPC client-streaming │ (Kafka, RabbitMQ)   │
                 └──────────────────────┴─────────────────────┘
```

**Newman's key insight on in-process vs inter-process calls:**

When a method call becomes a network call, three things change:
1. **Latency**: in-process ~100ns → network call ~500μs–10ms. A chain of 10 synchronous
   service calls adds 5–100ms minimum, before any processing time.
2. **Failure modes**: in-process calls succeed or throw an exception; network calls can hang
   indefinitely (timeout required), be partially received, or fail after the remote side
   already processed the request (requires idempotency — see `api-engineering/resilience-patterns.md`).
3. **Interface stability**: in-process method signatures can be refactored with IDE support;
   inter-process contracts must be versioned and backward-compatible across independent deploy
   cycles.

**Synchronous (REST/gRPC) — when to use:**
```
✅ Immediate response is required to proceed (payment authorization before confirming order)
✅ Simple request/response with a well-bounded, stable contract
✅ gRPC for internal service-to-service: strongly-typed protobufs, lower latency,
   native streaming; prefer over REST for backend-to-backend where JSON schema flexibility
   is not needed
```

**Asynchronous events — when to use:**
```
✅ Caller does not need an immediate response (audit log, notification, analytics event)
✅ Multiple consumers need to react to one event (fan-out)
✅ Decoupling deploy cycles matters — consumer and producer deploy independently
✅ Resilience: if consumer is down, messages queue until it recovers
✅ Event replay needed (new service needs historical data)
```

### Saga Pattern — Workflow Across Services (Chapter 6)

Newman dedicates a full chapter to Sagas as the correct replacement for distributed 2PC
(two-phase commit) for business processes that span multiple services. This section
supplements the Saga coverage in `references/api-first-integration-nfrs.md`.

A Saga is a sequence of local transactions, each publishing an event or message that
triggers the next step. If any step fails, compensating transactions undo the preceding steps.

**Orchestration (one service coordinates):**
```
Order Service (Orchestrator)
  ──(1) reserve inventory──▶ Inventory Service → Success
  ──(2) charge payment──────▶ Payment Service → Failure
  ──(3) COMPENSATE: release inventory──▶ Inventory Service
```

```typescript
// Orchestration Saga — Order Service coordinates all steps
class PlaceOrderSaga {
  async execute(order: Order): Promise<void> {
    // Step 1 — reserve inventory
    await inventoryService.reserve(order.items);

    try {
      // Step 2 — charge payment
      const payment = await paymentService.charge(order.customerId, order.total);

      try {
        // Step 3 — confirm order
        await orderRepo.confirm(order.id, payment.chargeId);
      } catch (err) {
        // Compensate steps 1 and 2
        await paymentService.refund(payment.chargeId);
        await inventoryService.release(order.items);
        throw err;
      }
    } catch (err) {
      // Compensate step 1 only
      await inventoryService.release(order.items);
      throw err;
    }
  }
}
```

**Choreography (services react to events):**
```
Order Service ──publishes──▶ order.created event
  Inventory Service subscribes ──▶ reserves stock ──publishes──▶ inventory.reserved
  Payment Service subscribes ──▶ charges card ──publishes──▶ payment.completed
  Order Service subscribes ──▶ confirms order
  IF Payment Service fails ──publishes──▶ payment.failed
  Inventory Service subscribes to payment.failed ──▶ releases reservation
```

**Orchestration vs Choreography — Newman's guidance:**

| | Orchestration | Choreography |
|---|---|---|
| **Visibility** | Explicit flow in one place — easy to reason about | Flow implicit in event subscriptions — harder to trace |
| **Coupling** | Orchestrator knows all participants | Services only know events — loose coupling |
| **Testing** | Test the orchestrator in isolation | Must trace event chains across services |
| **Failure handling** | Compensations explicit in orchestrator | Compensating events must be choreographed |
| **Best for** | Complex workflows with many steps and conditions | Simple fan-out, decoupled reactions |

Newman notes that choreography scales better for simple fan-out but becomes opaque for complex
workflows with conditional branches. For complex multi-step business processes, orchestration
(often via a dedicated workflow engine like Temporal or AWS Step Functions) makes the failure
and compensation logic explicit and observable.

### Testing Strategies — The Microservices Testing Diamond

Newman's testing guidance inverts the traditional testing pyramid for microservices:
fewer end-to-end tests (expensive, brittle, slow), more contract tests (fast, targeted).

```
       /\
      /  \
     / E2E \   ← few — cover only critical user journeys
    /────────\
   /  Contract \  ← many — verify inter-service contracts (Pact)
  /────────────\
 /   Unit Tests  \  ← foundation — fast, isolated, high coverage on business logic
/──────────────────\
```

**Consumer-Driven Contract Tests (CDCT — Pact):**
The consumer of a service's API defines a contract (the subset of the API it actually uses).
The provider runs the consumer's contract as part of its own test suite, verifying it hasn't
broken any consumer. This replaces many E2E tests with fast, isolated contract verification.

```typescript
// Consumer side — defines what it expects (Pact)
const interaction = {
  state: "an order with ID 123 exists",
  uponReceiving: "a request for order 123",
  withRequest: { method: "GET", path: "/orders/123" },
  willRespondWith: {
    status: 200,
    body: { id: "123", status: "CONFIRMED", total: 99.99 },
  },
};

// Provider side — verifies it satisfies the consumer's contract
// Run as part of Order Service's test suite
```

### Service-to-Service Security

Newman's second edition significantly expands security to cover service-to-service authentication
— an area the first edition treated briefly.

**mTLS (Mutual TLS) — the zero-trust standard for internal service communication:**
Every service presents a certificate; the receiver validates both the caller's identity and
the connection encryption. No shared secrets, no API keys in environment variables.

```yaml
# Kubernetes — enforce mTLS between all pods via Istio service mesh
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # all inter-service communication must use mTLS
```

**JWT propagation — user identity flows through the call chain:**
When a user makes a request, the API gateway validates their JWT and injects a service-to-
service token (often a new, scoped JWT) that downstream services use to identify both the
original user and the calling service.

```typescript
// API Gateway — extract user identity, inject service token
app.use(async (req, res, next) => {
  const userToken = req.headers.authorization;
  const user = await validateUserJWT(userToken);

  // Create a service-to-service token with user context
  const serviceToken = createServiceToken({
    sub: user.id,
    roles: user.roles,
    callerService: "api-gateway",
    audience: "internal-services",
  });

  req.headers["x-service-token"] = serviceToken;
  next();
});

// Downstream service validates the service token
app.use((req, res, next) => {
  const token = req.headers["x-service-token"];
  const claims = validateServiceJWT(token);  // checks audience, issuer, expiry
  req.user = claims;
  next();
});
```

Newman recommends mTLS for transport security (who is allowed to call whom at the network
level) and JWT propagation for identity context (who is the originating user, what are their
permissions) — treating them as complementary, not alternatives.
