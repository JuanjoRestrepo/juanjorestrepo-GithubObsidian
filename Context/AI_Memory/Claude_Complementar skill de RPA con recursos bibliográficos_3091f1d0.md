---
title: "Complementar skill de RPA con recursos bibliográficos"
date: 2026-08-12T20:59:28.457707Z
tags: [ai_memory, claude_context]
summary: "**Conversation overview**  The person is working on building and enriching Claude skill files for a technical team, with a focus on RPA development and now distributed systems/system design. The conversation began with a prior context of having enriched an RPA skill (`rpa-development`) with a new `vbnet-expressions.md` reference file synthesized from a VB.NET UiPath book. In this session, the person uploaded a PDF called *The Big Archive — System Design 2025* by ByteByteGo and asked Claude to determine whether its contents were better suited to creating a new skill or enriching an existing one, then apply the best option autonomously.  Claude analyzed the existing skills (`software-architecture`, `api-engineering`, `web-devops`) and the PDF's content structure (442 pages, ~180 diagram-heavy cheatsheet articles), concluding that a new standalone skill called `system-design` was the correct approach. The book covered a genuinely unaddressed infrastructure layer — caching, databases/storage, messaging/streaming, networking protocols, and system design interview methodology — that was distinct from the code-structural focus of `software-architecture` and the API-contract focus of `api-engineering`. Claude created the full skill from scratch: a `SKILL.md` with a trigger description, quick decision guide, core vocabulary, and reference file index, plus five reference files (`scalability-and-caching.md`, `databases-and-storage.md`, `messaging-and-streaming.md`, `networking-and-protocols.md`, `case-studies-and-interview-method.md`). Claude also added scope-boundary notes to both `software-architecture` and `api-engineering` pointing to the new skill to prevent overlap confusion. The person also asked about writing a Warp rule for the RPA skill but that task was not completed in this session.  The person's pattern across both sessions is to upload a reference book and delegate the full extraction, synthesis, and skill-file writing entirely to Claude, expecting autonomous decisions on structure (new skill vs. enrichment, how many reference files, what to include vs. exclude). Technical terminology used includes: REFramework, VB.NET expressions, DataTable LINQ, Invoke Code, UiPath Studio, CAP theorem, sharding, consistent hashing, fan-out on write/read, token bucket, dead-letter queue, QUIC/HTTP3, Lambda vs. Kappa architecture, and ByteByteGo."
---

### Human
Complementa el Skill de RPA usando este libro como recurso.

### Assistant

```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now let me read the UiPath standards reference and then extract the PDF content.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now let me check the existing reference files structure.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now I have a complete picture of the book's content and the existing skill. Let me now build the new reference file and wire it into the skill.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now update the main SKILL.md to wire in the new reference file.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Now update `uipath-standards.md` to point to the new file from the Expression Language section.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

All three files updated correctly. Let me do a final sanity check on the cross-references.
```
This block is not supported on your current device yet.
```

Everything is correctly wired. Here's a summary of what was done and why each decision was made.

---

## Cambios realizados al RPA Skill

### Nuevo archivo: `references/vbnet-expressions.md` (873 líneas)

El libro de Leon Petrou cubre el gap más frecuente en equipos RPA: desarrolladores que saben arrastrar actividades pero no saben resolver transformaciones de datos con una sola expresión, recurriendo a workflows de workaround que son lentos, difíciles de mantener y violan Single Responsibility. El nuevo archivo convierte ese libro en una referencia de producción, organizada en 10 secciones:

| Sección | Contenido |
|---|---|
| §1 — Fundamentals | Sistema de tipos VB.NET, conversiones, lambdas, operadores nulos, tabla de namespaces requeridos por imports, símbolos de IntelliSense |
| §2 — DataTable (16 patrones) | Row count, select columns, sheet names, Top N, Max/Min/Avg/Sum, reorder column (Invoke Method), rename, column-to-list, Clone vs Copy, Reverse, Dedup (GroupBy + DefaultView), DataTable-to-string, LINQ Join, Intersect/Except, HTML email table, LINQ Where |
| §3 — File/Directory | Latest file by creation time, delete all files, get files by type/pattern |
| §4 — Strings | Trim, Split (con la trampa del Char literal `","c`), Replace (encadenable), IsNumeric, word count, char count, Reverse, SecureString→String |
| §5 — Collections | List init, Add/Remove, ToArray/ToList, Intersect/Except, Dictionary init/add/access/ContainsKey |
| §6 — Email | Message properties, attachment filter regex, LIFO sort con `DateTime.Parse` del header |
| §7 — DateTime | DateDiff, compare time, DaysInMonth, formato ToString (tabla completa de specifiers), TimeSpan para Delay, ParseExact locale-safe, TryParseExact en Invoke Code, aritmética AddDays/AddMonths/etc. |
| §8 — Invoke Code | Sum column, computed column, row filter; estándares: `Dim`, DBNull guard, args Out/InOut |
| §9 — Debugging | Tabla de 14 síntomas → causa → resolución |
| §10 — Cheat Sheet | Expresiones más usadas por categoría para consulta rápida |

Dos decisiones de diseño que difieren del libro original: (1) la expresión de sort de mail usa `DateTime.Parse(x.Headers("date"))` en lugar de la cadena raw del libro, porque el string raw da orden lexicográfico incorrecto en varios formatos de servidor. (2) El `SecureString → String` incluye la nota de seguridad sobre minimizar el lifetime de la variable, que el libro omite.

### Actualización: `SKILL.md`

Dos cambios en el cuerpo principal:

**Lifecycle Stage 3 — Build — UiPath**: añadido un bullet explícito que establece que las transformaciones de datos se resuelven con expresiones (no con workflows de workaround) y que VB.NET es el lenguaje obligatorio, con referencia al nuevo archivo.

**Reference Files list**: añadida la entrada descriptiva para `vbnet-expressions.md`, coherente con el formato del resto de la lista.

### Actualización: `references/uipath-standards.md`

En la sección de Expression Language (justo después del punto "When C# is still the right choice"), añadido un bullet que enlaza el razonamiento de VB-vs-C# con la biblioteca de expresiones concreta, y establece la expectativa de que todo desarrollador use el reference antes de construir un workflow alternativo para algo que un Assign puede resolver.

### Human
Ayudame a escribir una Rule para Warp sobre esta skill, ponle un name y lo demas de la rule

### Assistant

```
This block is not supported on your current device yet.
```



### Human
I have a book on pdf called System Design by The Big Archive and its content seems to be super helpful, important and useful. How can we use it to create a new skill or enrich a current existing one? Apply the best option

### Assistant

```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

This is a huge, mostly diagram-based compilation of infographics, which would be expensive to extract and largely overlaps with existing skills. My best move is to propose enriching an existing skill rather than building a redundant new one from these images.

Rather than folding this into the existing software-architecture skill, I think this content deserves its own new skill on "System Design Interview & Distributed Systems Fundamentals" -- the existing skill is about code-level structural decisions (DDD, hexagonal, CQRS), while this book covers broader distributed systems building blocks like caching, load balancing, message queues, and databases at scale. Given the low effort budget here, I'll be decisive and propose creating this new skill.…
```
This block is not supported on your current device yet.
```

Good, there's real accessible text underneath the diagrams even though visuals dominate, so I can extract content across the whole document to build a distilled, organized skill since each article has a title and bullet text. Given the scope of 442 pages and roughly 180 topics, I need to be decisive and efficient—my plan is to recommend creating a new skill called "system-design-interview."…
```
This block is not supported on your current device yet.
```

With about 41K words over 442 pages, the text density is fairly low, fitting a diagram-heavy book. I'm deciding to create a new skill called `system-design` since the content spans distributed systems, networking, databases, caching, and APIs — broad enough to be distinct from the more structural `software-architecture` skill.

I'll build this out with SKILL.md as the core overview plus separate reference files covering scalability/distributed systems, databases/caching, networking/protocols, API security/auth, and case studies like Instagram and Netflix. Since this is the user's own uploaded book, I'm planning to grep the text for section boundaries using the table of contents, then hand-curate original, reformulated content into each reference file rather than copy-pasting directly.…
```
This block is not supported on your current device yet.
```

This confirms software-architecture and api-engineering already cover the overlapping CQRS, DDD, API design, and OAuth/JWT content from the ByteByteGo book at expert level. The real gap is broader distributed-systems infrastructure knowledge—things like caching systems and message queues—that aren't covered by existing skills.

Given this, the cleanest path forward is a new "system-design" skill dedicated to distributed systems infrastructure: databases, caching, networking, message queues, scalability, and classic system design case studies like Instagram or Netflix, since this doesn't fit the structural-code-pattern focus of software-architecture. I'll make sure it cross-references software-architecture and api-engineering to avoid duplication.…
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Ahora los archivos de referencia. Empiezo con caching/scalability:
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Ahora el archivo de metodología y casos de estudio:
```
This block is not supported on your current device yet.
```

Verifico que todo quedó correctamente enlazado y con el tamaño adecuado:
```
This block is not supported on your current device yet.
```

Todo dentro de límites (description: 1004/1024 caracteres, sin emojis). Ahora añado las referencias cruzadas desde `software-architecture` y `api-engineering` para que apunten de vuelta a este nuevo skill.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Listo. Aquí está el resumen de lo que se hizo:

## Decisión tomada

El libro (442 páginas, ~180 artículos tipo cheatsheet de ByteByteGo) mezcla tres categorías de contenido: **(1)** patrones estructurales de código que ya cubren `software-architecture` y `api-engineering` a nivel experto (DDD, CQRS, hexagonal, OAuth2/JWT, rate limiting), **(2)** contenido efímero de moda IA (top apps 2025, roadmaps de LLM) que no vale la pena fijar en un skill porque caduca rápido, y **(3)** una capa genuinamente no cubierta: **infraestructura de sistemas distribuidos** — caching, bases de datos/almacenamiento, mensajería, networking/protocolos y metodología de system design.

Por eso creé un **skill nuevo, `system-design`**, en vez de mezclarlo en los existentes (habría duplicado contenido) o crear un mega-archivo (habría violado el principio de un reference por dominio).

## Estructura creada

```
/mnt/skills/user/system-design/
├── SKILL.md                                    (113 líneas — overview, decision guide, NFRs)
└── references/
    ├── scalability-and-caching.md              (135 líneas)
    ├── databases-and-storage.md                (134 líneas)
    ├── messaging-and-streaming.md               (113 líneas)
    ├── networking-and-protocols.md              (130 líneas)
    └── case-studies-and-interview-method.md     (151 líneas)
```

**Contenido por archivo**: load balancing algorithms, patrones de cache (aside/through/back) con sus failure modes (stampede, penetration, avalanche); decision matrix relacional vs. NoSQL, formas normales, estrategias de indexado, sharding, topologías de replicación; SQS vs SNS vs EventBridge vs Kafka vs RabbitMQ, delivery guarantees, DLQ; el flujo completo "qué pasa al escribir una URL", TCP vs UDP, HTTP/1→2→3, load balancer vs reverse proxy vs API gateway; y un framework repetible de 5 pasos para cualquier pregunta de system design con 3 diseños resueltos (feed tipo Instagram, acortador de URLs, rate limiter).

**Cross-referencing**: añadí notas de "Scope" en `software-architecture` y `api-engineering` que remiten a `system-design` para la capa de infraestructura, evitando solapamiento.

### Human
No encuentro el nuevo skill

### Assistant

```
This block is not supported on your current device yet.
```

---

## Contexto de Estudio y Enlaces Relacionados
- **MOC Maestro**: [[MOC - AI Memory & Context]]
- **Dominio**: AI Memory & Context Knowledge Base
