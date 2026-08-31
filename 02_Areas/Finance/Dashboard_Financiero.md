---
tags: [finance, davibank, dashboard]
status: active
last_updated: 2026-08-31
---

# 🏦 Dashboard Financiero: DAVIbank

> [!warning] Protocolo de Privacidad (Ring 0)
> Este directorio está protegido por el firewall `.agentignore`. El procesamiento de extractos CSV y la visualización de balances operan 100% de forma local en este dispositivo.

## 📥 Flujo de Importación Mensual

1. Descarga el archivo de movimientos (.csv) desde la Banca Virtual DAVIbank.
2. Guárdalo directamente en la carpeta interna: `Extractos_CSV/`.
3. El plugin de finanzas actualizará los gráficos de balance automáticamente.

## 📊 Registro de Extractos Procesados

```dataview
TABLE file.ctime AS "Fecha de Importación", file.size AS "Peso del Archivo"
FROM "02_Areas/Finance/Extractos_CSV"
WHERE file.ext = "csv"
SORT file.ctime DESC
```
