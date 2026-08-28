---
title: "Fraud Detection Platform"
date: 1775628927.29998
tags: [ai_memory, claude_context]
summary: ""
---

### Human
Help me to make this project for my portfolio

# SentinelStream: End-to-End Fraud Detection Platform
### Backend + Data Engineering + Machine Learning

## 📝 Contexto del Proyecto
En el sector Fintech, la detección de fraude no es solo un problema de predicción, sino de **latencia e integridad de datos**. Este proyecto simula una plataforma financiera que procesa miles de transacciones móviles. El sistema implementa un pipeline **ELT (Extract, Load, Transform)** para analítica batch y un **Microservicio de Inferencia** para decisiones en tiempo real.

Se utiliza el dataset **PaySim**, que simula transacciones de dinero móvil, permitiendo aplicar lógica de negocio real sobre variables como balances de cuenta, tipos de transferencia y montos sospechosos.

---

## 🎯 Objetivos
* **Ingesta Robusta:** Orquestar el flujo de datos crudos mediante **Airflow**, asegurando la resiliencia del pipeline.
* **Transformación Escalable:** Implementar una **arquitectura de medallas** (Bronze, Silver, Gold) utilizando **dbt** para garantizar trazabilidad y calidad.
* **Modelado Predictivo:** Desarrollar un modelo de clasificación capaz de identificar patrones de fraude en datos desbalanceados.
* **Servicio en Producción:** Desplegar una API de alto rendimiento con **FastAPI** que consuma el modelo entrenado para validación inmediata.
* **Infraestructura como Código:** Garantizar la portabilidad de todo el stack mediante **Docker**.

---

## 🛠️ Stack Tecnológico
* **Lenguaje Principal:** Python 3.11+
* **Orquestación:** Apache Airflow
* **Transformación de Datos:** dbt (data build tool)
* **Base de Datos:** PostgreSQL (Data Warehouse local)
* **

TE EN CUENTA LOS SOURCES QUE TE DI DE: SKILL.md, etl_patterns, ml_evaluation, eda_templates y el contex.txt que es el mismo texto que te acabo de pasar, pero para que no olvides el contexto del proyecto a desarrollar como todo un data engineer profesiona y data scientist

### Assistant
This is a strong portfolio project. The key now is to structure it at a **production-grade level**, not as a notebook experiment. I’ll define a **complete blueprint + implementation roadmap** aligned with your standards (ETL rigor, ML evaluation, deployability).

---

# 1. System Architecture (High-Level)

You are not building “a model”. You are building a **data platform with ML embedded**.

### Core Components

```
                ┌────────────────────┐
                │   PaySim Dataset   │
                └─────────┬──────────┘
                          │
                    (Airflow DAG)
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
   Bronze Layer                        Metadata / Logs
 (Raw Ingestion)                            │
        │                                   │
        ▼
   Silver Layer (dbt)
 (Cleaned + Validated)
        │
        ▼
   Gold Layer (dbt)
 (Feature-ready tables)
        │
        ▼
   ML Training Pipeline
        │
        ▼
   Model Registry (local/artifacts)
        │
        ▼
   FastAPI Inference Service
        │
        ▼
   Real-time Predictions
```

---

# 2. Repository Structure (Production-Ready)

This is critical for portfolio quality.

```
sentinelstream/
│
├── airflow/
│   ├── dags/
│   │   └── etl_pipeline.py
│   └── docker-compose.yml
│
├── dbt/
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   └── dbt_project.yml
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── src/
│   ├── config/
│   │   └── settings.yaml
│   ├── ingestion/
│   ├── validation/
│   ├── features/
│   ├── modeling/
│   ├── evaluation/
│   └── utils/
│
├── api/
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── model_loader.py
│   │   └── inference.py
│   └── Dockerfile
│
├── notebooks/
│   └── eda_paysim.ipynb
│
├── tests/
│
├── docker/
│   ├── postgres/
│   └── airflow/
│
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 3. Data Engineering Pipeline (ELT Design)

### Why ELT (not ETL)?
- You leverage **PostgreSQL + dbt** for transformations
- Better **lineage, versioning, and testing**

---

## 3.1 Airflow DAG (Orchestration)

Based on best practices fileciteturn0file1:

### Responsibilities:
- Download/load PaySim
- Push to PostgreSQL (Bronze)
- Trigger dbt runs
- Validate outputs

### DAG Design

```python
# airflow/dags/etl_pipeline.py

def ingest_task():
    # Load CSV → PostgreSQL (raw schema)
    pass

def dbt_bronze():
    # dbt run --select bronze
    pass

def dbt_silver():
    # dbt run --select silver
    pass

def dbt_gold():
    # dbt run --select gold
    pass

def validate_gold():
    # Pandera / SQL checks
    pass
```

### Critical Engineering Decisions

- Idempotency: re-running DAG must not duplicate data
- Retry strategy (already in template)
- Logging for observability

---

## 3.2 dbt Layers (Medallion Architecture)

### Bronze
- Raw ingestion
- Minimal transformation
- Type casting

### Silver
- Data cleaning
- Null handling
- Business rules

Example:
```sql
WHERE amount > 0
AND oldbalanceOrg >= 0
```

### Gold (IMPORTANT)
This is where your portfolio stands out.

You must create **fraud features**, e.g.:

- balance_delta_orig = oldbalanceOrg - newbalanceOrig
- balance_delta_dest = newbalanceDest - oldbalanceDest
- is_balance_consistent (fraud signal)
- transaction_velocity (if time-based)

---

## 3.3 Data Validation (Non-negotiable)

From ETL standards fileciteturn0file1:

Use **Pandera**:

```python
Check.in_range(0, 1_000_000)
Check(lambda df: df["amount"] > 0)
```

Add:
- No negative balances
- Fraud label ∈ {0,1}
- No leakage columns

---

# 4. ML Pipeline (Fraud Detection)

## 4.1 Problem Framing

- Type: **Binary classification**
- Challenge: **Extreme class imbalance (~0.1%)**

---

## 4.2 Model Selection Strategy

From SKILL.md:

| Model        | Why |
|--------------|------|
| Logistic Reg | baseline, interpretable |
| RandomForest | nonlinear baseline |
| XGBoost      | **primary model (best for tabular fraud)** |

---

## 4.3 Pipeline (scikit-learn)

```python
Pipeline([
    ("scaler", StandardScaler()),  # only for linear models
    ("model", XGBClassifier(
        scale_pos_weight=ratio,
        eval_metric="aucpr"
    ))
])
```

### Why XGBoost?
- Handles imbalance well
- Robust to feature scaling
- State-of-the-art for tabular fraud

---

## 4.4 Evaluation (CRITICAL)

From evaluation reference fileciteturn0file2:

### DO NOT USE:
- Accuracy ❌

### USE:
- ROC-AUC
- PR-AUC (more important)
- Recall (fraud detection priority)
- MCC (balanced metric)

```python
metrics = evaluate_classifier(y_true, y_pred, y_prob)
```

---

## 4.5 Business Framing

You must explicitly define:

| Error Type | Impact |
|------------|--------|
| False Positive | user friction |
| False Negative | financial loss |

👉 Optimize for **high recall with acceptable precision**

---

# 5. FastAPI Inference Service

## Design

### Endpoint

```
POST /predict
```

### Input Schema

```python
class Transaction(BaseModel):
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float
    type: str
```

---

## Inference Flow

```
Request → Validation → Feature Engineering → Model → Response
```

---

## Example Response

```json
{
  "fraud_probability": 0.92,
  "is_fraud": true
}
```

---

## Key Engineering Points

- Load model once (singleton)
- Strict validation (Pydantic)
- No training logic inside API
- Latency < 100ms

---

# 6. Dockerization (Infra as Code)

You need **multi-service orchestration**:

### docker-compose

```
services:
  postgres
  airflow
  dbt
  api
```

---

## Why Docker?

- Reproducibility
- Easy deployment
- Clean environment isolation

---

# 7. EDA Notebook (Portfolio Quality)

Follow template fileciteturn0file3:

Sections:

1. Distribution of transaction types
2. Fraud vs non-fraud imbalance
3. Feature correlation
4. Balance inconsistencies
5. Outlier detection

Use:
- Seaborn → distributions
- Plotly → interactive fraud exploration

---

# 8. What Makes This Project “Senior-Level”

You must explicitly demonstrate:

### Data Engineering
- Idempotent pipelines
- Data validation layer
- dbt lineage

### Machine Learning
- Proper evaluation (PR-AUC, not accuracy)
- Imbalance handling
- Explainability (SHAP)

### Backend
- Production API
- Input validation
- Model serving best practices

### DevOps
- Dockerized system
- Modular architecture

---

# 9. Next Step (Execution Plan)

If you want, we can build this iteratively.

### Phase 1 (Data Layer)
- [ ] Setup PostgreSQL + Docker
- [ ] Load PaySim → Bronze
- [ ] Build dbt models

### Phase 2 (ML)
- [ ] EDA notebook
- [ ] Feature engineering
- [ ] Train XGBoost
- [ ] Evaluation + SHAP

### Phase 3 (Serving)
- [ ] FastAPI
- [ ] Model loading
- [ ] Endpoint

### Phase 4 (Orchestration)
- [ ] Airflow DAG
- [ ] Full pipeline automation

---

# 10. Critical Risks (You must handle)

- Data leakage (VERY common in PaySim)
- Imbalance bias
- Incorrect feature engineering
- No validation layer
- API tightly coupled to training code

---

If you want, next step I recommend:

👉 I can generate the **complete starter repo (with code for Airflow + dbt + FastAPI + ML pipeline)** following your standards.

Or we go step-by-step and build it like a real production system.

