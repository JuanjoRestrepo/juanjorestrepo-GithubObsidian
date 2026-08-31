### 📋 Estado de los modelos revisados y validados

|Modelo `gold`|Validado|Detalles Clave|
|---|---|---|
|✅ `gold_acquisition_trends_by_operator`|✔️|Validación por `operator`, `total_new_customers`, `execution_ts`.|
|✅ `gold_age_distribution_by_country_operator`|✔️|Verificado por `country`, `operator`, `age_bucket`.|
|✅ `gold_age_distribution_by_plan`|✔️|Verificado por `plan_type`, distribución y % de `UNKNOWN`.|
|✅ `gold_arpu_by_plan_type`|✔️|ARPU calculado correctamente con `users`, `total_revenue`, `arpu`.|
|✅ `gold_credit_score_segments`|✔️|Segmentos validados y puntaje promedio correcto.|
|✅ `gold_credit_vs_payment_behavior`|✔️|Matriz `credit_score_segment × payment_status`, todas combinaciones presentes.|
|✅ `gold_customer_distribution_by_country`|✔️|Nueva versión creada, validada por conteo total por `country`.|
|✅ `gold_customer_distribution_by_city`|✔️|Nueva versión creada, validada con top 5 y distribución por `city`.|
|✅ `gold_customer_distribution_by_operator`|✔️|Nueva versión creada, validada con top operadores.|
|✅ `gold_device_brand_popularity`|✔️|Conteo total por `device_brand`, todo OK.|
|✅ `gold_device_brand_by_country_operator`|✔️|Validado por combinaciones, diversidad y conteos.|

---

### 🟡 Próximos modelos pendientes (no vistos o parcialmente validados)

| Modelo `gold`                               | Estado    | Acción requerida                        |
| ------------------------------------------- | --------- | --------------------------------------- |
| ⏳ `gold_device_brand_by_plan`               | Pendiente | Revisar código, compilar, validar datos |
| ⏳ `gold_new_customer_trends`                | Pendiente | Compilar, validar distribución temporal |
| ⏳ `gold_operator_distribution`              | Pendiente | Revisar operadores por región, conteos  |
| ⏳ `gold_operator_summary`                   | Pendiente | KPIs agregados por operador             |
| ⏳ `gold_payment_issues`                     | Pendiente | % de issues de pago                     |
| ⏳ `gold_pending_payments`                   | Pendiente | Clientes con pagos pendientes           |
| ⏳ `gold_revenue_by_location`                | Pendiente | Ingresos por país o ciudad              |
| ⏳ `gold_revenue_stats_by_plan_and_operator` | Pendiente | Promedios y medianas por plan y op.     |
| ⏳ `gold_service_combinations`               | Pendiente | Combinaciones más comunes de servicios  |
| ⏳ `gold_service_popularity`                 | Pendiente | Servicios más contratados               |
| ⏳ `gold_top_customer_segments`              | Pendiente | Segmentos más valiosos                  |
| ❌ `gold_customer_distribution`              | Obsoleto  | Fue dividido correctamente en 3 modelos |







### ✅ Estado de cumplimiento de preguntas de negocio (Gold Layer)

| #   | Pregunta                                                                                                | ¿Resuelta? | Modelo                                                 | Comentario breve            |
| --- | ------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------ | --------------------------- |
| 1   | What is the average revenue per user (ARPU) by plan type?                                               | ✅ Sí       | `gold_arpu_by_plan_type`                               | Ya validado                 |
| 2   | What is the revenue distribution by geographic location?                                                | ✅ Sí       | `gold_revenue_by_location`                             | Por revisar ejecución final |
| 3   | Which customer segments generate the highest revenue?                                                   | ⚠️ Parcial | `gold_top_customer_segments`                           | Requiere revisión           |
| 4   | What is the distribution of customers by location?                                                      | ✅ Sí       | `gold_customer_distribution_by_city`, `..._by_country` | Hecho y validado            |
| 5   | What is the age distribution of customers by plan type?                                                 | ✅ Sí       | `gold_age_distribution_by_plan`                        | Validado                    |
| 6   | What is the age distribution by country and operator?                                                   | ✅ Sí       | `gold_age_distribution_by_country_operator`            | Validado                    |
| 7   | How are customers distributed across different operators?                                               | ✅ Sí       | `gold_customer_distribution_by_operator`               | Validado                    |
| 8   | What is customer segmentation by credit score ranges?                                                   | ✅ Sí       | `gold_credit_score_segments`                           | Validado                    |
| 9   | What are the most popular device brands?                                                                | ✅ Sí       | `gold_device_brand_popularity`                         | Validado                    |
| 10  | What is device brand preference by country/operator?                                                    | ✅ Sí       | `gold_device_brand_by_country_operator`                | Validado                    |
| 11  | What is device brand preference by plan type?                                                           | ✅ Sí       | `gold_device_brand_by_plan`                            | ✅ No se repite              |
| 12  | Which services are most commonly contracted?                                                            | ⚠️ Falta   | `❌`                                                    | Aún no implementado         |
| 13  | What service combinations are most popular?                                                             | ⚠️ Falta   | `❌`                                                    | Aún no implementado         |
| 14  | What percentage of customers have payment issues?                                                       | ⚠️ Falta   | `❌`                                                    | Modelo pendiente            |
| 15  | Which customers have pending payments?                                                                  | ⚠️ Falta   | `❌`                                                    | Modelo pendiente            |
| 16  | How does credit score correlate with payment behavior?                                                  | ✅ Sí       | `gold_credit_vs_payment_behavior`                      | Validado                    |
| 17  | How does the distribution of new customers change over time?                                            | ⚠️ Falta   | `❌`                                                    | Modelo pendiente            |
| 18  | What are customer acquisition trends by operator?                                                       | ✅ Sí       | `gold_acquisition_trends_by_operator`                  | Validado                    |
| 19  | What percentage of customers are active/suspended/inactive?                                             | ⚠️ Falta   | `❌`                                                    | Modelo pendiente            |
| 20  | Which service combinations drive highest revenue?                                                       | ⚠️ Falta   | `❌`                                                    | Modelo pendiente            |
| 21  | How do the mean and median monthly revenues per user compare across different plan types and operators? | ⚠️ Falta   | `❌`                                                    | Modelo pendiente            |



## 📊 Gold Models Summary

| Model Name                              | Purpose                                       | Output Columns                                                                 | Materialization |
|-----------------------------------------|-----------------------------------------------|-------------------------------------------------------------------------------|-----------------|
| `gold_arpu_by_plan_type`              | ARPU per plan                                 | `plan_type`, `arpu`                                                         | table           |
| `gold_pending_payments`               | List customers with pending payments          | `customer_id`, `amount_due`, `due_date`                                     | table           |
| `gold_operator_summary`               | Revenue and engagement per operator           | `operator`, `total_customers`, `total_revenue`, `pct_active_customers`, `pct_payment_issues` | table           |
| `gold_device_brand_by_plan`           | Device brands per plan type                   | `plan_type`, `device_brand`, `count`                                        | table           |
| `gold_device_brand_by_country_operator`| Device brands by country and operator         | `country`, `operator`, `device_brand`, `count`                              | table           |
| `gold_device_brand_popularity`        | Overall popularity of device brands           | `device_brand`, `count`                                                     | table           |
| `gold_age_distribution_by_plan`       | Customer age by plan type                     | `plan_type`, `age_group`, `count`                                           | table           |
| `gold_age_distribution_by_country_operator`| Age distribution per country/operator     | `country`, `operator`, `age_group`, `count`                                | table           |
| `gold_credit_score_segments`          | Group users by credit score                   | `credit_score_segment`, `count`                                             | table           |
| `gold_credit_vs_payment_behavior`     | Correlation of credit score and payment issues| `credit_score_segment`, `payment_issue_flag`, `count`                       | table           |
| `gold_payment_issues`                 | Users with any late/failed payments           | `customer_id`, `status`, `payment_date`, ...                               | table           |
| `gold_customer_status_distribution`   | Customer status share                         | `status`, `count`, `percentage`                                             | table           |
| `gold_customer_distribution_by_city`  | Customers by city                             | `city`, `count`                                                             | table           |
| `gold_customer_distribution_by_country`| Customers by country                          | `country`, `count`                                                          | table           |
| `gold_customer_distribution_by_operator`| Customers by operator                        | `operator`, `count`                                                         | table           |
| `gold_service_popularity`             | Most used individual services                 | `service_name`, `count`                                                     | table           |
| `gold_service_combinations`           | Most frequent service combinations            | `service_combo`, `count`                                                    | table           |
| `gold_high_revenue_service_combinations`| Top revenue-generating combos               | `service_combo`, `avg_revenue`                                              | table           |
| `gold_revenue_distribution_by_geo`    | Revenue by country-region                     | `country`, `region`, `total_revenue`                                        | table           |
| `gold_revenue_stats_by_plan_and_operator`| Mean vs median revenue by plan/operator     | `plan_type`, `operator`, `mean`, `median`                                   | table           |
| `gold_new_customer_trends_by_operator`| Monthly new customers per operator            | `operator`, `month`, `new_customers`                                        | table           |
| `gold_acquisition_trends_by_operator` | Acquisition share evolution                   | `operator`, `month`, `pct_acquired`                                         | table           |
| `gold_operator_distribution`          | Operator market share                         | `operator`, `customer_count`                                                | table           |
| `gold_top_customer_segments`          | Top segments by revenue                       | `segment`, `arpu`, `total_revenue`                                          | table           |

_(Full details available in dbt documentation or project README)_



