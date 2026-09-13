---
name: software-architecture
description: >
  Expert-level software architecture and system design skill, language- and domain-agnostic.
  Use whenever the user makes structural decisions about organizing, designing, or evolving a
  software system — not which framework to use, but how to shape the system itself. Triggers:
  Clean Architecture, Hexagonal Architecture, Ports and Adapters, Onion Architecture,
  Domain-Driven Design (DDD), bounded contexts, aggregates, CQRS, Event Sourcing, Event-Driven
  Architecture, microservices vs monolith, modular monolith, API-First design, integration
  patterns (Saga, Outbox, Strangler Fig, Anti-Corruption Layer), Non-Functional Requirements
  (NFRs), enterprise architecture review, system design, "how should I structure this",
  "microservices or monolith", "design this domain", "review my architecture". Applies across
  all languages and stacks, not limited to web dev. When in doubt about a structural decision
  (vs a tooling/deployment one), use this skill.
---

# Software Architecture & System Design Skill

Structural, language-agnostic architecture guidance grounded in the source literature (Evans,
Vernon, Fowler, Cockburn, Martin) and current industry standards (Microsoft Azure Architecture
Center, AWS Well-Architected Framework, ThoughtWorks Technology Radar). Complements
`web-devops` — this skill answers *how should the system be shaped*; `web-devops` answers
*how do I build and ship it*.

---

## How to Use This Skill

1. **Identify the nature of the question** — structural/design (this skill) vs tooling/deployment
   (`web-devops`). A question like "should I use microservices" is architecture; "how do I
   Dockerize this" is DevOps.
2. **Always ask about scale and team size first** if not stated — nearly every pattern here has
   a cost that is only justified past a certain complexity threshold. Recommending a heavyweight
   pattern for a small team/simple domain is a common and costly mistake.
3. **Always include the "when NOT to use" section** for any pattern you recommend — every
   pattern here has real adoption cost (cognitive load, boilerplate, operational complexity).
4. **Prefer the simplest architecture that satisfies the requirements.** Complexity must be
   earned by genuine need, never applied by default or to look sophisticated.
5. **Produce**: architecture diagrams (ASCII or via the Visualizer tool for complex diagrams),
   code structure, illustrative code in TypeScript and/or Python, and a rationale that explicitly
   states trade-offs — never present a pattern as free of cost.

---

## Quick Decision Guide

| Question | Likely answer |
|---|---|
| "My domain logic is tangled with my framework/DB code" | Clean / Hexagonal Architecture |
| "My business domain is genuinely complex, with real domain experts" | DDD (start with strategic patterns) |
| "My domain is simple CRUD" | **Skip DDD** — plain layered architecture is correct |
| "Read and write workloads have very different scale/shape needs" | CQRS (only if read/write asymmetry is real) |
| "I need a full audit trail / temporal queries are a core requirement" | Event Sourcing (rare — high cost) |
| "Should I split into microservices?" | **Default: no.** Start with a Modular Monolith. Split only when a team/deploy/scale boundary genuinely requires it |
| "Multiple teams need to consume this API independently" | API-First Design |
| "I need to migrate a legacy system incrementally" | Strangler Fig pattern |
| "Two services need consistency across a distributed transaction" | Saga pattern (never distributed 2PC) |
| "I'm not sure if my architecture is enterprise-ready" | Enterprise Architecture Review Checklist + NFR audit |

---

## 1. Clean / Hexagonal / Onion Architecture — The Ports & Adapters Family

These three are variations of the same core idea, popularized respectively by Robert C. Martin
(Clean Architecture, 2012), Alistair Cockburn (Hexagonal / Ports & Adapters, 2005), and Jeffrey
Palermo (Onion Architecture, 2008). All three enforce the **Dependency Rule**: dependencies
point inward, toward the domain; the domain knows nothing about frameworks, databases, or UI.

**Core principle:** your business logic should be testable and runnable with zero knowledge of
Express, FastAPI, PostgreSQL, or any external system. Frameworks and databases are *details*,
plugged in from the outside via interfaces (ports) and their implementations (adapters).

→ See `references/clean-hexagonal-onion.md` for the layer diagrams, TypeScript and Python
implementations, dependency inversion patterns, and when this adds unnecessary indirection.

---

## 2. Domain-Driven Design (DDD)

Eric Evans' 2003 book *Domain-Driven Design: Tackling Complexity in the Heart of Software*
introduced strategic and tactical patterns for modeling complex business domains in close
collaboration with domain experts. Vaughn Vernon's *Implementing Domain-Driven Design* (2013)
refined the tactical patterns for modern practice.

**Strategic patterns:** Bounded Context, Ubiquitous Language, Context Mapping.
**Tactical patterns:** Entities, Value Objects, Aggregates, Domain Events, Repositories,
Domain Services, Factories.

**Critical filter before applying DDD:** DDD is a heavyweight investment justified only when
the domain has genuine business complexity — not technical complexity. A CRUD app with complex
infrastructure is not a DDD candidate. A domain with intricate business rules, multiple expert
stakeholders, and evolving requirements is.

→ See `references/ddd.md` for bounded context mapping, aggregate design rules, TypeScript and
Python tactical pattern implementations, and the "CRUD trap" anti-pattern.

---

## 3. CQRS & Event-Driven Architecture

**CQRS** (Command Query Responsibility Segregation), formalized by Greg Young building on
Bertrand Meyer's Command-Query Separation principle, splits the read model from the write model.
**Event Sourcing** stores state as a sequence of immutable events rather than current state.
**Event-Driven Architecture (EDA)** decouples services via asynchronous events rather than
synchronous calls.

These three are frequently combined but are **independent decisions** — you can use CQRS
without Event Sourcing, EDA without CQRS, and so on. Conflating them is a common mistake.

**Critical filter:** CQRS is justified when read and write workloads have genuinely different
scale, shape, or consistency requirements. Applying CQRS to a simple CRUD resource roughly
doubles your code for no benefit — Martin Fowler explicitly warns of this in his own writing
on the pattern.

→ See `references/cqrs-event-driven.md` for the command/query separation, event sourcing
trade-offs, eventual consistency handling, and TypeScript/Python implementations.

---

## 4. Microservices vs Modular Monolith

The industry default has shifted. Following widely cited retrospectives (including Shopify's
and Amazon Prime Video's public postmortems on monolith consolidation), the current consensus
across Microsoft Azure Architecture Center, AWS, and ThoughtWorks is: **start with a modular
monolith; extract microservices only when a genuine scaling, team, or deployment boundary
demands it.**

Microservices solve **organizational** scaling problems (independent team deployment cadence)
far more reliably than they solve **technical** scaling problems, and they introduce
distributed systems complexity (network calls, eventual consistency, distributed tracing,
service mesh) that a monolith never has to deal with.

→ See `references/microservices-monolith.md` for the decision framework, modular monolith
structure (module boundaries enforced in-process), the strangler fig migration path, and
real-world case studies of both directions (monolith → microservices and the reverse).

---

## 5. API-First Design & Integration Patterns

**API-First Design** means the API contract (OpenAPI/AsyncAPI spec) is designed and agreed
upon before implementation begins — the contract becomes the source of truth that both API
producers and consumers build against in parallel.

**Integration patterns** solve the problem of getting distributed components to work together
reliably: **Saga** (distributed transactions without 2PC), **Outbox** (reliable event
publishing alongside DB writes), **Strangler Fig** (incremental legacy migration),
**Anti-Corruption Layer** (isolating a clean domain model from a messy external one).

→ See `references/api-first-integration-nfrs.md` for OpenAPI-first workflows, the Saga pattern
(choreography vs orchestration), the Transactional Outbox pattern, and migration strategies.

---

## 6. Non-Functional Requirements (NFRs) & Enterprise Architecture Review

NFRs — scalability, reliability, security, maintainability, observability, performance,
availability — are frequently treated as afterthoughts, yet ISO/IEC 25010 (the international
standard for software quality) treats them as first-class requirements equal to functional
ones. An architecture review that only validates functional correctness is incomplete.

→ See `references/api-first-integration-nfrs.md` for the ISO/IEC 25010 quality model, the full
Enterprise Architecture Review Checklist, and NFR-driven architecture decision records (ADRs).

---

## 7. Programming Concepts — Foundational Knowledge

Architecture is only sound when the code it shapes is also sound. The patterns in this skill
rest on foundational programming knowledge: OOP, SOLID, design patterns, data structures,
algorithms, concurrency, and code quality principles. These concepts underpin Clean
Architecture (Dependency Inversion is DIP applied at scale), DDD (Entities and Value Objects
are OOP done correctly), CQRS (Command/Query Separation is CQS at the method level first),
and every other pattern in this skill.

→ See `references/programming-concepts.md` for variables and scope, higher-order functions,
all four OOP pillars with practical examples, SOLID principles with TypeScript and Python
code, GoF design patterns (Singleton, Factory, Builder, Adapter, Decorator, Observer,
Strategy, Command), data structures selection guide, Big O notation, recursion and
memoization, async/await and the event loop, race conditions and mutexes, DRY/KISS/YAGNI,
naming discipline, and debugging techniques — grounded in Clean Code (Martin), The Pragmatic
Programmer (Thomas & Hunt), CLRS, and the Gang of Four.

---

## Cross-Cutting: Avoiding Over-Engineering

Every pattern in this skill has genuine adoption cost. The single most common architecture
mistake — more common than under-engineering — is applying a sophisticated pattern to a
problem that doesn't need it, driven by resume-building or premature scaling anxiety rather
than actual requirements.

**Apply this test before recommending any pattern in this skill:**
1. What specific, current problem does this solve that the simpler alternative does not?
2. What is the team's ability to operate this pattern's complexity long-term?
3. Would YAGNI (You Aren't Gonna Need It) apply here — is this solving a problem you don't
   have yet?
4. Could this decision be deferred without cost until the need is proven?

If you cannot answer #1 concretely, recommend the simpler alternative and note the pattern
as a documented future option, not a current implementation.

---

## Reference Files

- `references/programming-concepts.md` — OOP pillars (encapsulation, abstraction,
  inheritance, polymorphism), SOLID principles, GoF design patterns (Singleton, Factory,
  Builder, Adapter, Decorator, Observer, Strategy, Command), data structures selection guide,
  Big O notation, recursion and memoization, concurrency vs parallelism, async/await event
  loop, race conditions and mutexes, DRY/KISS/YAGNI, naming discipline, debugging techniques
- `references/clean-hexagonal-onion.md` — Ports & Adapters family: layer diagrams, dependency
  inversion, TypeScript and Python implementations, when this is unnecessary indirection
- `references/ddd.md` — strategic and tactical DDD patterns, bounded context mapping,
  aggregate design rules, the CRUD trap anti-pattern
- `references/cqrs-event-driven.md` — CQRS, Event Sourcing, Event-Driven Architecture,
  eventual consistency handling, when each is (and isn't) justified
- `references/microservices-monolith.md` — decision framework, modular monolith structure,
  strangler fig migration, real-world case studies
- `references/api-first-integration-nfrs.md` — API-First workflow, Saga, Outbox,
  Anti-Corruption Layer, Strangler Fig, ISO/IEC 25010 quality model, Enterprise Architecture
  Review Checklist, NFR-driven ADRs
