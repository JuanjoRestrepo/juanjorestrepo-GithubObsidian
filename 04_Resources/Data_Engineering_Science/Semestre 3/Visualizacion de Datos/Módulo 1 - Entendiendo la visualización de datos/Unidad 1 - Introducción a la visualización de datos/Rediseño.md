---
title: "Rediseño"
date: 2026-08-27
tags:
  - maestria
  - semestre-3
  - visualizacion-datos
  - apuntes
status: reference
---



```mermaid
flowchart TB
  subgraph Sidebar
    P[Selector de país] --> S
    S[Selector de producto] --> M
    M[Menú módulos]
  end
  subgraph MainPanel
    A[Card: Treemap]
    B[Card: Growth Opportunity]
    C[Card: Product Space]
    D[Card: Trade Map]
    E[Card: Global Share]
    F[Card: Trade Over Time]
  end
  Sidebar --> MainPanel

  %% Interactividad
  A -- click filtra --> D
  D -- click filtra --> A

```
