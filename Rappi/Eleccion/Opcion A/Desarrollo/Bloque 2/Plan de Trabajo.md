

### Próxima etapa: análisis e informe de insights

Aquí una propuesta de flujo de trabajo:
1. **Exploración de datos crudos**
    - Cargar `data/output/results.json` con Pandas / Python
    - Ver cuántos registros `success`, `not_found`, `error`
    - Ver distribución de precios por zona
    - Ver casos donde `deliveryFeeValue` o `serviceFeeValue` son `null` (gaps)

2. **Limpieza / transformación**
    - Establecer valores por defecto o imputaciones para `null`
    - Normalizar nombres de productos
    - Filtrar duplicados (múltiples registros del mismo producto-zona)
    
3. **Visualizaciones e insights**
    - Comparar precios promedio de “Big Mac”, “Combo Mediano”, “Coca-Cola 500ml” por zona
    - Identificar cuántas veces Rappi ofrece descuento (casos con `priceWasOffer = true`) vs sin descuento
    - Mapas o gráficos geográficos (si tienes lat/long de las direcciones)
    - Graficar distribución de tarifas de entrega cuando sí están presentes
    - Hallazgos: zonas donde somos más caros, más baratos, gran variabilidad, etc.
    
4. **Top 5 insights accionables + recomendaciones**  
    Cada insight debe tener:
    - Qué encontraste
    - Por qué importa
    - Qué se puede hacer
    
5. **Formato entregable**
    - Notebook + exportar gráficos
    - PowerPoint o PDF con los gráficos e insights resumidos
