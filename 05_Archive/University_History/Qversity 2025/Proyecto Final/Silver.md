
### ⚠️ Columnas con advertencias

|Columna|Problema detectado|
|---|---|
|`record_uuid`|Tiene 58 valores nulos. Decidir si deben eliminarse o dejarse.|
|`first_name`|121 nulos. Además, posible presencia de nombres muy cortos o vacíos.|
|`phone_number`|No tiene nulos, pero hay duplicados. Revisar si son válidos o se deben deduplicar.|
|`device_model`|Tiene 20 nulos. Validar si es un campo obligatorio.|
|`registration_date`|76 nulos. Validar si son aceptables.|
|`credit_score`|Tiene valores fuera de rango (ej. -90). Filtrar < 0 o > 900.|
|`monthly_bill_usd`|Contiene valores negativos. Reemplazar por NULL o revisar su lógica.|
|`monthly_data_gb`|Puede contener valores negativos. Validar.|
|`data_usage_current_month`|Puede contener valores negativos. Validar.|
|`latitude`|Algunas coordenadas están fuera del rango válido (-90 a 90).|
|`longitude`|Algunas coordenadas están fuera del rango válido (-180 a 180).|
|`age`|Rango poco realista (ej. -10, 198). Mantener solo edades entre 10 y 100 aprox.|

### ✅ Columnas sin problemas

Solo para referencia:

- `raw_id`
    
- `customer_id`
    
- `email` (casi perfecta)
    
- `city`, `country`, `status`, `plan_type`, `operator` (ya fueron limpiadas)
    
- `device_brand`
    
- `last_payment_date`
    
- `contracted_services`
    
- `ingestion_ts`




## ✅ Solución final recomendada (con lógica del negocio)

Vamos a mapear así:

|Valor original|Estado final|
|---|---|
|ACTIVE / ACTIVO|`ACTIVE`|
|INACTIVE / INACTIVO|`INACTIVE`|
|SUSPENDED / SUSPENDIDO|`SUSPENDED`|
|VALID, INVALID, vacíos, nulos|`UNKNOWN`|