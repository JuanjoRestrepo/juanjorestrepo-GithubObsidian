---
title: "ESTRUCTUA DE CARPETAS"
date: 2026-08-27
tags:
  - self-study
  - data-science-engineering
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

```bash
worldcup-2026-pipeline/
│
├── docker/
│   └── postgres/
│       └── init.sql
│
├── src/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── ingestion/
│   │   └── (vacío por ahora)
│   │
│   ├── processing/
│   │   └── (vacío por ahora)
│   │
│   └── modeling/
│       └── (vacío por ahora)
│
├── tests/
│   └── test_db_connection.py
│
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Data Science & Engineering|Ciencia e ingeniería de datos]].
- Criterio de producción: Preserva linaje, esquemas y calidad de datos; separa datos crudos, validados y listos para consumo antes de modelar o publicar.
