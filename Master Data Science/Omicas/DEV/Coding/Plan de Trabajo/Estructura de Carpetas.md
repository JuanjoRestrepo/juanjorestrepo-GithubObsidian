
```graphql

Omicas/
├── Docs/  
│   ├── Plan_trabajo.docx         ← Plan formal, cronograma, diagrama arquitectónico  
│   ├── Arquitectura.drawio       ← Diagrama C4 / flujo de datos  
│   └── schema.json               ← Esquema maestro (puede apuntar al de Scopus o ampliarse)  
│
├── Scopus/                       ← Código específico para extracción Scopus  
│   ├── config.py                 ← Variables de entorno y carga de API Key  
│   ├── api.py                    ← Lógica de llamadas y paginación (Bronze)  
│   ├── schema.json               ← JSON Schema de “artículos” (modelo silver)  
│   ├── parser.py                 ← Mapeo a dict plano (silver)  
│   ├── validator.py              ← Validación contra el schema (silver)  
│   ├── main.py                   ← Orquestador rápido (hoy gold-lite)  
│   └── requirements.txt  
│
├── ETL/  
│   ├── Bronze/  
│   │   └── extract_scopus.py     ← Extrae raw_scopus.json (Bronze layer)  
│   ├── Silver/  
│   │   └── clean_scopus.py       ← Toma raw, parsea, valida → cleaned + errors (Silver)  
│   └── Gold/  
│       └── export_scopus.py      ← Toma cleaned → CSV / BD / MinIO / repositorio (Gold)  
│
├── scripts/  
│   └── to_obsidian.py            ← Convierte JSON limpios a notas Markdown en Obsidian  
│
├── Notebooks/  
│   ├── 01_scopus_exploratorio.ipynb  
│   └── 02_dashboard_piloto.ipynb  
│
└── README.md                     ← Descripción general y “Quick Start” para el pipeline  


```

Omicas/
├── Docs/  
│   ├── Plan_trabajo.docx         ← Plan formal, cronograma, diagrama arquitectónico  
│   ├── Arquitectura.drawio       ← Diagrama C4 / flujo de datos  
│   └── schema.json               ← Esquema maestro (puede apuntar al de Scopus o ampliarse)  
│
├── Scopus/                       ← Código específico para extracción Scopus  
│   ├── config.py                 ← Variables de entorno y carga de API Key  
│   ├── api.py                    ← Lógica de llamadas y paginación (Bronze)  
│   ├── schema.json               ← JSON Schema de “artículos” (modelo silver)  
│   ├── parser.py                 ← Mapeo a dict plano (silver)  
│   ├── validator.py              ← Validación contra el schema (silver)  
│   ├── main.py                   ← Orquestador rápido (hoy gold-lite)  
│   └── requirements.txt  
│
├── ETL/  
│   ├── Bronze/  
│   │   └── extract_scopus.py     ← Extrae raw_scopus.json (Bronze layer)  
│   ├── Silver/  
│   │   └── clean_scopus.py       ← Toma raw, parsea, valida → cleaned + errors (Silver)  
│   └── Gold/  
│       └── export_scopus.py      ← Toma cleaned → CSV / BD / MinIO / repositorio (Gold)  
│
├── scripts/  
│   └── to_obsidian.py            ← Convierte JSON limpios a notas Markdown en Obsidian  
│
├── Notebooks/  
│   ├── 01_scopus_exploratorio.ipynb  
│   └── 02_dashboard_piloto.ipynb  
│
└── README.md                     ← Descripción general y “Quick Start” para el pipeline  



