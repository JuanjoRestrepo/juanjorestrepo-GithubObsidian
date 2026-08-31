---
tags: [finance, config, davibank]
status: active
last_updated: 2026-08-31
---

# 🏷️ Reglas de Categorización Automática (DAVIbank CSV)

> [!info] Mecanismo de Mapeo
> El motor de importación analiza la columna de descripción o establecimiento de tu CSV de DAVIbank y asigna las etiquetas correspondientes si encuentra alguna de las palabras clave.

## 📋 Mapeo de Transacciones

```yaml
rules:
  # Categoria: Alimentacion y Mercado
  - category: 'Alimentacion/Mercado'
    tags: ['#gasto/mercado', '#finanzas/alimentacion']
    keywords:
      - 'EXITO'
      - 'CARULLA'
      - 'JUMBO'
      - 'ALKOSTO'
      - 'D1'
      - 'ARAPLUS'

  # Categoria: Transporte y Movilidad
  - category: 'Transporte/Movilidad'
    tags: ['#gasto/transporte']
    keywords:
      - 'UBER'
      - 'CABIFY'
      - 'DIDIDRIVE'
      - 'TERPEL'
      - 'TEXACO'
      - 'BIXXUS'

  # Categoria: Servicios y Suscripciones
  - category: 'Servicios/Suscripciones'
    tags: ['#gasto/suscripciones', '#gasto/servicios']
    keywords:
      - 'NETFLIX'
      - 'SPOTIFY'
      - 'OPENAI'
      - 'AWS'
      - 'GITHUB'
      - 'APPLE.COM'

  # Categoria: Transferencias y Movimientos Bancarios
  - category: 'Transferencias/Bancos'
    tags: ['#transferencia', '#movimiento/interno']
    keywords:
      - 'TRANSFIYA'
      - 'TRANSFERENCIA'
      - 'DAVIPLATA'
      - 'ABONO'
      - 'RETIRO CAJERO'

  # Categoria por Defecto (Unclassified)
  - category: 'Sin Categorizar'
    tags: ['#gasto/revision_pendiente']
    keywords: []
```
