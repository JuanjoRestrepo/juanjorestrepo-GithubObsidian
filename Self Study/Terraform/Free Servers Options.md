---
title: "Free Servers Options"
date: 2026-08-27
tags:
  - self-study
  - cloud-infrastructure
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Si quieres algo "Gratis para siempre" (Literal)

- **Oracle Cloud (OCI):** Tiene una capa "Always Free" que te da hasta 4 instancias ARM con 24GB de RAM gratis para siempre. Terraform también funciona excelente ahí.
- **Google Cloud (GCP):** Ofrece una instancia `e2-micro` gratis para siempre en ciertas regiones de EE.UU.


### 2. Comparativa: OCI vs. GCP vs. AWS
Si quieres algo que puedas dejar encendido meses sin pagar nada:

|**Proveedor**|**Capa Gratuita (Always Free)**|**Potencia**|**Dificultad Terraform**|
|---|---|---|---|
|**Oracle (OCI)**|4 CPUs ARM + 24GB RAM|⭐⭐⭐⭐⭐ (Brutal)|Media|
|**Google (GCP)**|1 instancia `e2-micro`|⭐ (Muy débil)|Alta|
|**AWS**|`t2.micro` (solo 12 meses)|⭐⭐|Muy Alta|
|**DigitalOcean**|$200 USD (por 60-90 días)|⭐⭐⭐|**Muy Baja (Ideal para empezar)**|

**Recomendación:** Si quieres aprender Terraform _hoy mismo_ sin esperar las 72h, vete por **Oracle Cloud (OCI)**. Es la que más recursos te da gratis. Si quieres aprender lo que más pide el mercado laboral, ve por **AWS**, pero prepárate para escribir mucho más código.

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Cloud & Infrastructure|Cloud e infraestructura]].
- Criterio de producción: Trata la infraestructura como código: revisa el plan, controla versiones, evita secretos en el estado y usa ejecución reproducible.
