
# Full Project Intake: Adidas LAM Chatbot — Senior Data Science Analysis

## Section 1 — Contexto y planteamiento del problema (Notas clave para la presentación)

**¿Qué es esto?:** 
Un ejercicio práctico para un candidato a Especialista Senior en Chatbots en Adidas LAM. 

- Responsable del bot de principio a fin en una operación multinacional (mercados de habla hispana y portuguesa). 
- El bot es la **primera línea de soporte digital** para **pedidos, pagos y devoluciones**. 
- Durante la presentación de 20 minutos, se espera que demuestre mi enfoque, no una solución completa.
### El marco de 3 KPI y por qué es importante:

| KPI              | Current | Target | Gap       | Severity |
| ---------------- | ------- | ------ | --------- | -------- |
| Containment Rate | 48%     | 55%    | −7pp      | Medium   |
| Repeat Rate      | 28%     | 18%    | +10pp     | High     |
| Resolution Rate  | 30%     | 50%    | **−20pp** | Critical |

- Lo más importante que hay que entender antes de analizar los datos: **estos tres KPI están relacionados causalmente, no son independientes.**
- *La resolución impulsa la repetición, y juntas limitan la contención. *
- La brecha de resolución no solo es la mayor (+20 pp), sino que **es la causa principal de las otras dos.**

---
## Section 2 — Análisis profundo de datos: Lo que realmente muestran las cifras

El conjunto de datos contiene **798.617 registros de contacto en total** distribuidos en 3 modos de gestión. A continuación, se muestra el desglose real del volumen:

| Channel                             | Volume  | Share     |
| ----------------------------------- | ------- | --------- |
| Agent Only                          | 398,203 | **49.9%** |
| Hybrid (bot starts, agent finishes) | 276,844 | **34.7%** |
| Bot Only                            | 123,570 | **15.5%** |

**Observación crítica sobre la conciliación de KPI:** 
- El volumen de contactos gestionados únicamente por bots representa el $15,5\%$ del total, pero la contención declarada es del $48\%$
- Esto indica que los datos en Excel son un **subconjunto filtrado** (por ejemplo, *contactos escalados + muestra de contactos gestionados por bots*), o que la **Contención/Containment** se mide a nivel de $sesión/conversación$ con un denominador que excluye el $spam/la falta de contacto$ y ciertas sesiones transitorias. 
- Esto debe indicarse como una **suposición explícita** en la presentación. 
	>Los datos representan una muestra de contactos multicanal. Los KPI se indican a nivel de programa; el conjunto de datos se utiliza para el análisis de distribución relativa y la estimación de oportunidades.

### 2.1 — El hallazgo más crítico: El bot desvía, no resuelve

Utilizando directamente los KPI indicados:
- El bot **gestiona** el $48\%$ de los contactos (sin escalarlos).
- Pero solo **resuelve** el $30\%$ de todos los contactos.
- Por lo tanto: **resolución dentro del rango de gestión = $30 / 48 = 62,5\%$**.
- Esto significa que **el $37,5\%$ de todos los contactos gestionados no se resuelven**; el bot cierra la conversación sin solucionar el problema del cliente.

Este es el hallazgo analítico más importante para la presentación. 

- La brecha no radica principalmente en la **desviación de volumen (contención)**, sino en la **calidad de la resolución dentro del flujo contenido** 
- El bot desvía a los clientes de los agentes, pero **no logra resolver sus problemas**, lo que genera una tasa de repetición del $28\%$ (los clientes regresan porque la primera interacción no les ayudó). 
- Esto amplifica los costos posteriores: también se incurre en costos de agente por el contacto repetido.

### 2.2 — Fallo en la clasificación de intenciones: Una crisis oculta en la calidad de los datos

Dos etiquetas de subcategoría revelan fallos sistemáticos en el procesamiento del lenguaje natural (PLN) y la clasificación de intenciones:

|Failure Mode|Total Volume|Agent Channel|Hybrid Channel|Bot Channel|
|---|---|---|---|---|
|**"Left Blank"** (sub-intent not captured)|**197,508**|137,979|56,166|3,363|
|**"Not defined by Bot"** (intent unrecognized)|**63,902**|1|22,547|41,354|
|**Combined**|**261,410**||||

**$261.410$ contactos ($32,7\%$ del volumen total) no tienen una subintención correctamente clasificada.** 

- Esto no es un problema de modelado, sino de **diseño de diálogo y taxonomía**. 
- El bot dirige las conversaciones a flujos, pero **no logra identificar lo que el cliente** realmente desea dentro de esos flujos.
- No se puede mejorar la resolución sin **corregir primero la clasificación**.

El patrón ***"Not defined by Bot"*** en el canal exclusivo para bots ($41.354$) es particularmente alarmante: 

- El bot **gestiona estos contactos (sin escalarlos)**, pero **no reconoce la subintención**, lo que significa que o bien *responde con una respuesta genérica o no logra resolver el problema*. 
- Esto explica una gran parte del $37,5\%$ de los contactos gestionados pero sin resolver.

### 2.3 — Rendimiento a nivel de categoría (Contención de bots por categoría)

|Category|Total Volume|Bot%|Hybrid%|Agent%|Assessment|
|---|---|---|---|---|---|
|Existing Order|270,531|18.6%|42.1%|39.3%|High volume, low bot rate, major opportunity|
|Returns & Refunds|245,084|22.1%|30.4%|47.5%|Highest agent leakage, complex but tractable|
|Customer Feedback|78,932|**0.0%**|8.9%|**91.1%**|Near-zero bot handling — routing failure|
|Support on Ordering|58,100|**1.1%**|8.7%|**90.2%**|52k+ "Explain how to order" going to agents|
|Spam/No Contact|44,314|3.0%|60.5%|36.6%|Noise/filter issue, not a bot improvement target|
|Payment|32,024|20.7%|41.1%|38.3%|Sensitive but partially automatable|
|Membership|14,998|2.8%|52.5%|44.8%|Low bot rate, high hybrid — flow abandonment|
|Product Information|14,785|5.6%|**74.6%**|19.8%|Mostly hybrid — informational, should be bot|
|Apps & Website|6,941|**29.8%**|42.3%|27.8%|Best bot performance after Not-defined|

### 2.4 — Principales oportunidades de automatización (priorizadas según el volumen de fugas de agentes)

Las siguientes subcategorías presentan un alto volumen de escalamiento por parte de los agentes, una baja tasa de bots y son técnicamente viables para la automatización:

| Category            | Subcategory                   | Agent Vol | Hybrid Vol | Bot%  | Automation Type                      |
| ------------------- | ----------------------------- | --------- | ---------- | ----- | ------------------------------------ |
| Support on Ordering | **Explain how to order**      | 52,148    | 4,165      | 0.4%  | Pure informational — FAQ bot         |
| Returns & Refunds   | **Return status**             | 30,817    | 18,098     | 20.9% | Transactional — OMS integration      |
| Existing Order      | **Size**                      | 20,702    | 20,571     | 31.8% | Product info + FAQ                   |
| Existing Order      | **Not delivered**             | 15,842    | 13,517     | 3.7%  | Transactional — carrier integration  |
| Existing Order      | **In transit**                | 11,238    | 14,978     | 12.4% | Transactional — order tracking API   |
| Returns & Refunds   | **Label Request**             | 12,139    | 14,028     | 7.9%  | Transactional — label generation API |
| Existing Order      | **Delay**                     | 10,584    | 13,885     | 7.1%  | Transactional + proactive messaging  |
| Payment             | **Payment rejection**         | 5,726     | 6,145      | 15.4% | Sensitive — partial automation       |
| Returns & Refunds   | **Refund proof**              | 7,436     | 4,338      | 0.0%  | Document/status API                  |
| Existing Order      | **Failed intent of delivery** | 5,070     | 4,875      | 0.0%  | Carrier integration                  |

**Potencial de automatización conservador (60 % del volumen de contactos no generados por bots para las 15 intenciones principales):** 

- *$~198,000$ contactos adicionales*: Si se capturara, el volumen de contactos generados exclusivamente por bots se triplicaría aproximadamente, lo que impulsaría directamente la contención por encima del $55\%$.


### 2.5 — La paradoja de "Cómo devolver" (Bot Canary)

*"Cómo devolver" (Devoluciones y reembolsos)* es la subcategoría con mejor rendimiento del bot: 

- Gestiona el $51,7\%$ del volumen exclusivamente mediante el bot ($19,915$ contactos). 
- Sin embargo, $6,856$ contactos siguen siendo atendidos por agentes y $11,764$ se gestionan mediante un sistema híbrido.
- Esto indica que el bot **tiene la capacidad de gestionar las devoluciones informativas**, pero *algún problema en el enrutamiento o el flujo de diálogo* está provocando que una *gran parte de los contactos se desvíe a los canales humanos*. 
- Esto representa una solución rápida: 
	>corregir la lógica de enrutamiento de un flujo que ya funciona correctamente en el bot.



---
## Section 3 — Resumen del diagnóstico de la causa raíz

Hay **tres niveles de fallo**, cada uno agravando el anterior:
#### **Nivel 1: Fallo de entrada (¿Por qué el bot no entiende?):**
- El $32,7\%$ de los contactos *no tienen una subintención clasificada (Campo en blanco + Sin definir).*
- La taxonomía de NLU/intención está incompleta. El bot desconoce las necesidades de los clientes en muchas categorías de alto volumen.

#### **Nivel 2: Fallo de resolución (¿Por qué el bot no resuelve el problema?):**
- Incluso cuando se reconoce la intención, el bot a menudo no puede resolver el problema. 
* Las intenciones de alto volumen más automatizables (*estado de devolución, seguimiento de pedidos, generación de etiquetas*) requieren integraciones del sistema con las API de OMS/WMS/transportistas, las cuales parecen estar ausentes o incompletas.

#### **Nivel 3: Fallo del bucle (¿Por qué los clientes vuelven?):**
- Sin una resolución en el primer contacto, el $28\%$ de los clientes vuelven a contactar. 
- *Cada nuevo contacto genera una carga tanto para el bot como para el agente de respaldo*, lo que **incrementa el coste de cada interacción inicial** sin resolver.


---


## Section 4 — Recomendaciones sobre tecnología y arquitectura de la solución

Dado el tipo de problema, el alcance y las limitaciones, recomiendo lo siguiente:

### **Para el análisis y el panel de control (esta presentación y el monitoreo continuo):**

1. Los *datos están estructurados, en formato tabular y son de tamaño moderado* (menos de 1 millón de filas). No se requiere GPU ni computación distribuida.

#### Stack primario:
- Python 3.12 + pandas + Plotly para análisis
- Power BI o Tableau para el panel ejecutivo
- Para la presentación, una aplicación interactiva Plotly Dash o un informe estático HTML de Plotly se crean más rápido y resultan más impactantes que una presentación estática.
- Para el proceso de análisis basado en notebooks: Python + pandas + Seaborn (distribuciones) + Plotly (interactivo)
- Great Expectations o Pandera para la validación de contratos de datos.


### Para el trabajo de mejora del chatbot (más allá de la presentación):

La arquitectura actual del bot es crucial en este caso, y aún no se dispone de esa información. Sin embargo, la recomendación general es la siguiente:

1. **El problema de la clasificación de intenciones apunta a la necesidad de:** 
	1. **(a)** reentrenar el *NLU (Natural Language Understanding)* con datos de conversación *debidamente etiquetados*, 
	2. **(b)** utilizar una capa de modelo de lenguaje grande de reserva (GPT-4/Claude) para la clasificación de intenciones sin entrenamiento previo en los casos de `"No definido"` y `"En blanco"`, o 
	3. **(c)** adoptar un enfoque híbrido donde las intenciones de alta confianza permanezcan en el flujo determinista y las de baja confianza se redirijan a la generación de respuestas asistida por el modelo de lenguaje.

2. **El problema de la resolución apunta a** 
	1. la necesidad de integraciones de API con el sistema de gestión de pedidos, 
	2. la plataforma de gestión de devoluciones 
	3. y las API de seguimiento de transportistas. 
	
	Sin estas integraciones, la tasa de resolución no puede mejorar significativamente, independientemente de las mejoras en el NLU.

