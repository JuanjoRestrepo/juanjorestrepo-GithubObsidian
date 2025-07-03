

![[Pasted image 20250702173124.png]]


# 🔷 1. **Capa Bronze – `bronze.customers_raw`**

### 📄 Tabla: `bronze.customers_raw`

|Columna|Tipo|Descripción|
|---|---|---|
|`id`|`int`|Clave primaria técnica (única por registro)|
|`raw_json`|`jsonb`|Objeto JSON bruto del cliente|
|`ingestion_timestamp`|`datetime`|Timestamp de cuándo se cargó|

- **Propósito**: almacenar el _dato crudo_ tal como viene de la fuente.
    
- **Por qué `id` es PK**: representa unívocamente un registro crudo.
    
- **Por qué no hay FK**: esta tabla no depende de nadie; es el origen del pipeline.
    
- **Cardinalidad**: no tiene relaciones hacia atrás, pero **una fila alimenta una o más filas Silver** (1:N).
    

---

# 🪙 2. **Capa Silver – Datos limpios y normalizados (3NF)**

## 🧍‍♂️ `silver_customers`

|Columna clave|Rol|
|---|---|
|`raw_id`|`PK` técnica|
|`customer_id`|ID de negocio|

- **Por qué `raw_id` es PK**: referencia exacta al registro en Bronze.
    
- **Por qué no se usa `customer_id` como PK**: hay duplicados (clientes con múltiples cargas), por eso haces `ROW_NUMBER()` en deduplicación para 
    
- **Relación con `bronze.customers_raw`**:
    - **1:N** → un registro de Bronze puede derivar en múltiples registros Silver (diferentes `ingestion_ts`) con el mismo `customer_id`.
        
- **Campos**: todos los atributos atómicos de un cliente: nombre, email, score, ubicación, plan, etc.
    

---

## 💳 `silver_payments`

|Columna clave|Rol|
|---|---|
|`raw_id`|`FK`|
|`payment_date`|`PK`|

- **Por qué esta tabla existe**: en `raw_json` los pagos vienen en un array (`payment_history`). Lo explotas con `jsonb_array_elements`.
    
- **Relación con `silver_customers`**:
    - **1:N** → un cliente (por su `raw_id`) puede tener múltiples pagos.
        
- **PK compuesta**: `raw_id + payment_date` garantiza unicidad por pago por cliente.
    
- **Campos**: fecha de pago, monto, validez, estado (SUCCESS, LATE, FAILED, etc).
    

---

## 📡 `silver_service`

|Columna clave|Rol|
|---|---|
|`raw_id`|`FK`|
|`service_name`|`PK`|

- **Por qué esta tabla existe**: igual que `payment_history`, `contracted_services` es un array JSON.
    
- **Relación con `silver_customers`**:
    
    - **1:N** → un cliente puede tener múltiples servicios contratados.
        
- **PK compuesta**: `raw_id + service_name`, porque un cliente puede tener una única instancia de cada servicio.
    
- **Campos**: nombre del servicio en limpio (SMS, ROAMING, etc).
    

---

# 🟡 3. **Capa Gold – Métricas y agregaciones por pregunta de negocio**

La **capa Gold** se construye sobre Silver y **no almacena relaciones explícitas con claves foráneas**, porque su objetivo es **desnormalizar para facilitar el análisis**. Veamos los tipos de relaciones e intenciones:

---

### 🎯 Ejemplos de Gold 1:1 (derivan de `silver_customers` por clave única)

|Tabla|Clave Primaria|Relación|Justificación|
|---|---|---|---|
|`gold_arpu_by_plan_type`|`plan_type`|1:1|Agrega por tipo de plan — cada `plan_type` genera un único ARPU|
|`gold_operator_distribution`|`operator`|1:1|Cada operador tiene su propio conteo|
|`gold_credit_score_segments`|`credit_score_segment`|1:1|Cada segmento de score aparece una vez|

---

### 📊 Ejemplos de Gold 1:N (agregan por combinaciones)

|Tabla|PK compuesta|Relación Silver → Gold|Ejemplo|
|---|---|---|---|
|`gold_device_brand_by_country_operator`|`country + operator + brand`|1:N|Cada combinación produce una fila|
|`gold_age_distribution_by_country_operator`|`country + operator + bucket`|1:N|Cada combinación de país/operador tiene varios rangos etarios|
|`gold_revenue_stats_by_plan_and_operator`|`plan_type + operator`|1:N|Compara medias/medianas por doble dimensión|

---

### 💰 Ejemplos de Gold con agregaciones sobre múltiples relaciones

|Tabla|Origen|Relación Silver → Gold|Justificación analítica|
|---|---|---|---|
|`gold_high_revenue_service_combinations`|`silver_customers` + `silver_service`|N:N (mediante join por `raw_id`)|Permite analizar qué combinaciones de servicios generan más ARPU|
|`gold_credit_vs_payment_behavior`|`silver_customers` + `silver_payments`|N:N mediante `raw_id`|Evalúa score crediticio vs status de pago|

---

# 📐 Cardinalidad General

|Relación|Tipo|Descripción técnica|
|---|---|---|
|`bronze → silver_customers`|1:N|Un registro raw puede tener múltiples duplicados antes del deduping|
|`silver_customers → payments`|1:N|Un cliente puede tener múltiples pagos|
|`silver_customers → services`|1:N|Un cliente puede tener múltiples servicios contratados|
|`silver_customers → gold`|1:N|Cada modelo Gold agrega, agrupa o segmenta a partir de los datos base|
|`payments → gold`|1:N|Modelos como `payment_issues`, `pending_payments`, etc.|
|`services → gold`|1:N|Modelos como `service_popularity`, `service_combinations`|

---

# ✅ ¿Por qué se modeló así?

1. **Modularidad**: cada tabla representa una entidad o relación _única y clara_.
    
2. **Escalabilidad**: puedes agregar más columnas o reglas sin romper otras capas.
    
3. **Trazabilidad total**: puedes reconstruir todo desde Bronze si cambia el modelo.
    
4. **Alineación con dbt**: ideal para modelar pipelines mantenibles y testeables.
    
5. **Optimización de performance**: separas transformaciones costosas en capas progresivas.






- **What is the average revenue per user (ARPU) by plan type?**
    
    sql
    
    CopyEdit
    
    `SELECT   plan_type,   ROUND(AVG(monthly_bill_usd), 2) AS arpu FROM silver.silver_customers WHERE monthly_bill_usd IS NOT NULL GROUP BY plan_type ORDER BY arpu DESC;`
    
- **What is the revenue distribution by geographic location?**
    
    sql
    
    CopyEdit
    
    `SELECT   country,   city,   SUM(monthly_bill_usd)   AS revenue,   COUNT(DISTINCT customer_id) AS unique_customers FROM silver.silver_customers WHERE monthly_bill_usd IS NOT NULL GROUP BY country, city ORDER BY revenue DESC;`
    
- **Which customer segments generate the highest revenue?**
    
    sql
    
    CopyEdit
    
    `WITH revenue_base AS (   SELECT     customer_id,     SUM(monthly_bill_usd) AS total_spent   FROM silver.silver_customers   GROUP BY customer_id ), segmented AS (   SELECT     customer_id,     total_spent,     NTILE(5) OVER (ORDER BY total_spent DESC) AS quintile   FROM revenue_base ) SELECT   quintile,   COUNT(*)               AS num_customers,   ROUND(AVG(total_spent),2) AS avg_spent,   MIN(total_spent)       AS min_spent,   MAX(total_spent)       AS max_spent FROM segmented GROUP BY quintile ORDER BY quintile;`
    
- **What is the distribution of customers by location (city)?**
    
    sql
    
    CopyEdit
    
    `SELECT   city,   COUNT(DISTINCT customer_id) AS customer_count FROM silver.silver_customers WHERE city IS NOT NULL GROUP BY city ORDER BY customer_count DESC;`
    
- **What is the age distribution of customers by plan type?**
    
    sql
    
    CopyEdit
    
    `WITH age_buckets AS (   SELECT     plan_type,     CASE       WHEN age BETWEEN 0  AND 17 THEN '0–17'       WHEN age BETWEEN 18 AND 25 THEN '18–25'       WHEN age BETWEEN 26 AND 35 THEN '26–35'       WHEN age BETWEEN 36 AND 45 THEN '36–45'       WHEN age BETWEEN 46 AND 60 THEN '46–60'       WHEN age > 60            THEN '60+'       ELSE 'UNKNOWN'     END AS age_bucket   FROM silver.silver_customers   WHERE age IS NOT NULL ) SELECT   plan_type,   age_bucket,   COUNT(*) AS cnt FROM age_buckets GROUP BY plan_type, age_bucket ORDER BY plan_type, age_bucket;`
    
- **What is the age distribution by country and operator?**
    
    sql
    
    CopyEdit
    
    `WITH age_buckets AS (   SELECT     country,     operator,     CASE        WHEN age < 30            THEN '<30'       WHEN age BETWEEN 30 AND 50 THEN '30–50'       WHEN age > 50             THEN '>50'       ELSE 'UNKNOWN'     END AS age_bucket   FROM silver.silver_customers   WHERE age IS NOT NULL ) SELECT   country,   operator,   age_bucket,   COUNT(*) AS customer_count FROM age_buckets GROUP BY country, operator, age_bucket ORDER BY country, operator, age_bucket;`
    
- **How are customers distributed across different operators?**
    
    sql
    
    CopyEdit
    
    `SELECT   operator,   COUNT(DISTINCT customer_id) AS customer_count FROM silver.silver_customers WHERE operator IS NOT NULL GROUP BY operator ORDER BY customer_count DESC;`
    
- **What is customer segmentation by credit score ranges?**
    
    sql
    
    CopyEdit
    
    `SELECT   credit_score_segment,   COUNT(*)             AS cnt,   ROUND(AVG(credit_score),2) AS avg_score FROM silver.silver_customers WHERE credit_score IS NOT NULL GROUP BY credit_score_segment ORDER BY cnt DESC;`
    
- **What are the most popular device brands?**
    
    sql
    
    CopyEdit
    
    `SELECT   device_brand,   COUNT(DISTINCT customer_id) AS num_customers FROM silver.silver_customers WHERE device_brand IS NOT NULL GROUP BY device_brand ORDER BY num_customers DESC;`
    
- **What is device brand preference by country/operator?**
    
    sql
    
    CopyEdit
    
    `SELECT   country,   operator,   device_brand,   COUNT(*)           AS customer_count FROM silver.silver_customers WHERE country IS NOT NULL   AND operator IS NOT NULL   AND device_brand IS NOT NULL GROUP BY country, operator, device_brand ORDER BY country, operator, customer_count DESC;`
    
- **What is device brand preference by plan type?**
    
    sql
    
    CopyEdit
    
    `SELECT   plan_type,   device_brand,   COUNT(*)           AS customer_count FROM silver.silver_customers WHERE plan_type IS NOT NULL   AND device_brand IS NOT NULL GROUP BY plan_type, device_brand ORDER BY plan_type, customer_count DESC;`
    
- **Which services are most commonly contracted?**
    
    sql
    
    CopyEdit
    
    `SELECT   service_name,   COUNT(DISTINCT raw_id) AS num_customers FROM silver.silver_services GROUP BY service_name ORDER BY num_customers DESC;`
    
- **What service combinations are most popular?**
    
    sql
    
    CopyEdit
    
    `WITH combos AS (   SELECT     raw_id,     STRING_AGG(service_name, '+' ORDER BY service_name) AS combo   FROM silver.silver_services   GROUP BY raw_id ) SELECT   combo AS services_combination,   COUNT(*) AS cnt FROM combos GROUP BY combo ORDER BY cnt DESC LIMIT 20;`
    
- **What percentage of customers have payment issues?**
    
    sql
    
    CopyEdit
    
    `WITH total AS (   SELECT COUNT(DISTINCT customer_id) AS tot FROM silver.silver_customers ), issues AS (   SELECT DISTINCT sc.customer_id   FROM silver.silver_payments sp   JOIN silver.silver_customers sc ON sp.raw_id = sc.raw_id   WHERE sp.status IN ('FAILED','LATE') ) SELECT   ROUND(100.0 * COUNT(*) / (SELECT tot FROM total), 2) AS pct_payment_issues FROM issues;`
    
- **Which customers have pending payments?**
    
    sql
    
    CopyEdit
    
    `SELECT   sc.customer_id,   sp.payment_date,   sp.amount FROM silver.silver_payments sp JOIN silver.silver_customers sc ON sp.raw_id = sc.raw_id WHERE sp.status = 'PENDING';`
    
- **How does credit score correlate with payment behavior?**
    
    sql
    
    CopyEdit
    
    `SELECT   sc.credit_score_segment,   sp.status AS payment_status,   COUNT(*)     AS cnt FROM silver.silver_customers sc JOIN silver.silver_payments sp ON sc.raw_id = sp.raw_id GROUP BY sc.credit_score_segment, sp.status ORDER BY sc.credit_score_segment, cnt DESC;`
    
- **How does the distribution of new customers change over time?**
    
    sql
    
    CopyEdit
    
    `SELECT   DATE_TRUNC('month', registration_date) AS month,   COUNT(DISTINCT customer_id)            AS new_customers FROM silver.silver_customers WHERE registration_date IS NOT NULL GROUP BY month ORDER BY month;`
    
- **What are customer acquisition trends by operator?**
    
    sql
    
    CopyEdit
    
    `SELECT   DATE_TRUNC('month', registration_date) AS month,   operator,   COUNT(DISTINCT customer_id)            AS new_customers FROM silver.silver_customers WHERE registration_date IS NOT NULL   AND operator IS NOT NULL GROUP BY month, operator ORDER BY month, operator;`
    
- **What percentage of customers are active/suspended/inactive?**
    
    sql
    
    CopyEdit
    
    `WITH status_counts AS (   SELECT     status,     COUNT(*) AS num_customers   FROM silver.silver_customers   GROUP BY status ), total AS (   SELECT SUM(num_customers) AS tot FROM status_counts ) SELECT   status,   num_customers,   ROUND(100.0 * num_customers / (SELECT tot FROM total), 2) AS pct_customers FROM status_counts ORDER BY num_customers DESC;`
    
- **Which service combinations drive highest revenue?**
    
    sql
    
    CopyEdit
    
    `WITH cust_sv AS (   SELECT     raw_id,     STRING_AGG(service_name, '+' ORDER BY service_name) AS combo   FROM silver.silver_services   GROUP BY raw_id ) SELECT   s.combo                AS services_combination,   SUM(sc.monthly_bill_usd) AS sum_revenue,   AVG(sc.monthly_bill_usd) AS avg_revenue FROM cust_sv s JOIN silver.silver_customers sc ON s.raw_id = sc.raw_id WHERE sc.monthly_bill_usd IS NOT NULL GROUP BY s.combo ORDER BY sum_revenue DESC LIMIT 20;`
    
- **How do the mean and median monthly revenues per user compare across different plan types and operators?**
    
    sql
    
    CopyEdit
    
    `SELECT   plan_type,   operator,   ROUND(AVG(monthly_bill_usd), 2) AS avg_revenue,   PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_bill_usd) AS median_revenue FROM silver.silver_customers WHERE monthly_bill_usd IS NOT NULL GROUP BY plan_type, operator ORDER BY avg_revenue DESC;`