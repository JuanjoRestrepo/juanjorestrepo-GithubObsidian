
Buen día a todos, mi nombre es Juan José Restrepo y hoy les vengo a presentar el análisis del Caso del Chatbot de Large Action Model de Adidas

> los LAM están entrenados para **ejecutar acciones** concretas dentro de aplicaciones y sistemas digitales

# (Página 1 — Executive Overview)
El contexto inicial rápidamente era que el Business Case reportaba brechas importantes en los principales KPIs operacionales del chatbot:

- Containment Rate por debajo del target,
- Resolution Rate considerablemente baja,
- y una Repeat Rate elevada.

A partir de ahí, el objetivo del análisis fue identificar:
- dónde estaba ocurriendo la fricción operacional,
- por qué el bot escalaba tantos contactos,
- y qué iniciativas generarían el mayor impacto sobre los KPIs del negocio.


Si observamos nuestros KPIs actuales, se está fallando en tres frentes simultáneamente:
- la Tasa de Contención está en 48% contra una meta del 55%
- la Tasa de Contacto Repetido está en el 28% cuando debería ser del 18%.
- la Tasa de Resolución está en el 30% contra un objetivo del 50%

A primera vista, la hipótesis sería que 
	***los usuarios rechazan el bot o no confían en él***.

Pero este gráfico nos dice lo contrario: 

## **(Señala cada barra mientras hablas)**

![[Pasted image 20260611173319.png]]


Tenemos tres canales de atención
1. El canal de `agentes humanos` maneja $398,000$ contactos — casi el $50\%$ del volumen total.
2. El canal `híbrido`, donde el bot inicia pero un agente termina, maneja $277,000$ contactos — otro $35\%$
3. Y el canal `bot-only`, donde el bot resuelve de inicio a fin sin intervención humana, maneja $124,000$ contactos — apenas el $15.5\%$

## **(Señala el callout "Bot participa en 50.2% pero solo contiene 15.5%")**
Ahora, si sumamos el canal `híbrido` y el `bot-only` 
- ***el bot está participando activamente en el 50.2% de todas las interacciones.***
- Pero **solo está conteniendo el 15.5%. 
- **Hay una brecha de 35 puntos porcentuales entre participación y contención real.

Eso significa que
> De cada 10 contactos donde el bot interviene, en 7 de ellos el bot no pudo terminar el trabajo y necesitó un agente humano para cerrar el caso.

###  **Falsa Contención**
A esto lo denomino **Falsa Contención**:
- el bot saluda y clasifica la intención del usuario, pero al carecer de capacidad transaccional, no puede resolver
- El sistema lo registra como un contacto 'contenido' porque técnicamente no escaló, pero en la realidad el cliente cerró la ventana porque no tuvo respuesta, y luego lo vuelve a llamar al bot.

### Esta dinámica explica los tres KPIs de forma simultánea: 

- la contención no llega al 55% porque el bot no termina los casos, 
- la resolución está en el 30% porque contener no es lo mismo que resolver, 
- y el contacto repetido está en el 28% porque los clientes sin respuesta vuelven a contactar el bot intentando de nuevo. 

- Los tres tienen la misma causa raíz."


## **(Señala el gráfico de Pareto en su conjunto antes de entrar en detalle)**_

Ahora bien, sabemos que hay un problema. La pregunta estratégica es: ¿por dónde empezamos?

- El bot tiene 19 categorías de contacto distintas
- Si intentamos mejorar las 19 al mismo tiempo, dispersamos recursos, tardamos más y el impacto es mínimo.
- Necesitamos un criterio de priorización que sea objetivo y que esté basado en los datos.

Para eso apliqué el **Principio de Pareto**, también conocido como la regla del 80/20. La lógica de este es:
> en la mayoría de los sistemas operacionales, una minoría de causas genera la mayoría del efecto.

En nuestro caso, eso se traduce en que 
- **pocas categorías de contacto concentran la mayor parte del volumen.**

Por lo que si podemos identificar cuáles son esas categorías, podemos ignorar el resto temporalmente y concentrar toda la inversión donde realmente impacte.

## **(Señala el eje izquierdo y las barras azules)**

Las barras azules que ven aquí representan el volumen de contactos por categoría, ordenadas de mayor a menor de izquierda a derecha.

- La barra más alta es `Existing Order` con $270,000$ contactos. 
- La segunda es `Returns & Refunds` con $245,000$. 
- Y desde ahí las barras caen rápidamente.

## **(Señala el eje derecho y la línea naranja acumulativa)**

La línea naranja que sube de izquierda a derecha es la clave del análisis. *Es el porcentaje acumulado de volumen*. 

Cada punto de esa línea nos  dice: 
> "con todas las categorías hasta aquí, ¿qué porcentaje del volumen total ya estoy cubriendo?"


Observen cómo la línea sube de forma muy pronunciada en las primeras categorías y luego se aplana casi completamente. 
-  esa curva pronunciada al inicio nos dice que hay una concentración bastante grande en pocas categorías.


## (Señala el punto de la línea correspondiente a Support on Ordering, la cuarta barra)

Cuando llegamos a la cuarta categoría, `Support on Ordering`, la línea acumulativa ya está en el $81.7\%$.

Esto ya nos dice que **Cuatro de las diecinueve** categorías ya explican más del 80% del volumen total de contactos de la operación.

Y este dato nos dice que **si optimizamos solo estas cuatro categorías, estamos impactando el 80% del problema.**

Las otras quince categorías, que representan el 18% restante del volumen, se pueden abordar más adelante con menor urgencia y menor inversión.

Por eso es que al usar el Pareto, podenos determinar qué tiene más impacto al momento de arreglar una problemática y en el orden correcto.

---

# (Página 2 — Intent Deep Dive)

Ahora, si entramos al detalle de esas categorías en la Página 2, el diagnóstico se vuelve aún más preciso.

Este gráfico de barras apiladas nos muestra, para cada categoría, qué proporción del volumen termina en cada canal. Hay dos hallazgos a destacar:

## (Señala las barras de Customer Feedback y Support on Ordering)

1. **Primero, `Customer Feedback` y `Support on Ordering` tienen cero por ciento de contención por bot o casi nula**

> Esto quiero decir que EL $91\%$ y el $90\%$ respectivamente va directo a agentes humanos.
> y el bot no participa casi en absoluto

Y aquí hay una distinción estratégica importante:
- enviar el feedback de un cliente frustrado a un agente humano es la decisión correcta, porque requiere empatía y juicio y manejo emocional. Eso no se automatiza
- Pero enviar más de 50,000 consultas del tipo `cómo hago un pedido`  del tipo de `Support Ordering`, a un agente humano operativamente no sería lo más eficiente, sino más bien se debería tratar como un **FAQ**, **Preguntas Frecuentes**, un banco de FAQs usando un flujo de texto para procesarlas y no requerir de ayuda externa humana

## **(Señala las barras de Existing Order y Returns & Refunds)**

2. **Segundo**: en las categorías de mayor volumen, `Existing Order` y `Returns & Refunds`

**El patrón híbrido supera al bot-only.**

> Esto confirma el diagnóstico: **el bot identifica y clasifica la intención del usuario correctamente, pero en la mayoría de los casos no puede terminar el trabajo y necesita escalar a un agente.

**¿Por qué ocurre esto?**

Porque estas consultas no son informacionales, son transaccionales, es decir:
- Cuando un cliente pregunta por el estado de su devolución, la respuesta no es siempre la misma para todos, osea no es una respuesta estática
	NO ES "tu devolución específica, con tu número de orden específico, está en este estado en este momento"
- Para dar esa respuesta, el bot necesita conectarse en tiempo real al sistema de gestión de pedidos — el OMS — consultar el estado de esa orden concreta y devolver un resultado dinámico.
- Si esa conexión no existe, el bot reconoce perfectamente que el cliente quiere saber el estado de su devolución, pero no tiene forma de consultarlo.
- Entonces hace lo único que puede: escala al agente humano, que sí tiene acceso al OMS

***No es un problema de inteligencia artificial. El bot entiende al cliente. El problema es que el bot no tiene las herramientas conectadas para actuar sobre lo que entendió.***

Es exactamente como contratar a alguien brillante para un trabajo y no darle acceso a los sistemas que necesita para hacerlo.

## (Señala la tabla y el gráfico de automatización en la mitad inferior de la Página 2)

En la parte inferior de esta página cuantifiqué las subcategorías con mayor potencial de automatización. 
- Son 7 intents/intenciones que suman 278,000 contactos.
- Pero no todos son iguales en términos de lo que se necesita para automatizarlos.
- El color verde es complejidad baja, el amarillo es complejidad media.

> La diferencia entre los dos niveles es una sola pregunta: **¿la respuesta es siempre la misma para todos los usuarios, o depende de los datos específicos de ese cliente en ese momento?**


**Las de complejidad baja**
- `Size`, `Explain how to order,`` Payment Process Information` — 
	- responden siempre igual para cualquier usuario. Por ejemplo, La guía de tallas de Adidas es la misma para todo el mundo, El proceso de cómo hacer un pedido es el mismo para todo el mundo.
	- El bot solo necesita tener esa información bien estructurada en su base de conocimiento y devolvérsela al cliente.
No necesita de integraciones técnicas. Cero dependencias de sistemas externos. Se puede activar en semanas con configuración pura.

Las de complejidad media
- `Return status`, `In transit`, `label Request` — son dinámicas. La respuesta cambia para cada cliente y para cada momento.
	- Para decirle a un cliente si su devolución fue aprobada, el bot necesita autenticarlo, tomar su número de orden y consultarlo contra el sistema de devoluciones en tiempo real.
	- Para confirmar que un paquete está en tránsito, necesita disparar una consulta a la API del carrier con el tracking ID de ese envío específico.
	- Para generar una etiqueta de retorno, necesita conectarse a la plataforma de logística inversa, verificar la elegibilidad de esa orden y generar un documento único.
	
Todas requieren que ingeniería construya una conexión API entre el bot y los sistemas de backend.


## (Señala ahora la tabla en la parte inferior derecha)

Esta tabla a la derecha es la traducción operacional de todo lo que acabo de explicar.
Para cada uno de los 7 intents, me dice cuatro cosas con precisión:
- el volumen total de contactos que representa esa oportunidad
- la complejidad de implementación
- qué integración técnica específica se necesita o si no se necesita ninguna
- y en qué fase del roadmap va

Por ejemplo, `Explain how to order`: 
- 56,000 contactos, complejidad baja, ninguna integración, Fase 1

`Return status`
- 61,000 contactos, complejidad media, requiere OMS API, Fase 2. Y así para cada uno.


---

# (Página 3 — Action Plan)

Ahora que entendimos dónde están las fricciones operacionales, la siguiente pregunta es:

> ¿Cómo convertimos este diagnóstico en un plan ejecutable y priorizado?

El roadmap que proponemos organiza las iniciativas según dos variables:
- impacto operacional,
- y complejidad de implementación.

Y la lógica del plan es progresiva:

- Primero recuperamos visibilidad y resolvemos quick wins.
- Después habilitamos resolución transaccional real.
- Finalmente refinamos inteligencia conversacional y reducimos falsa contención.

Cada fase desbloquea la siguiente.


## **(Señala el Gantt visual a la izquierda)**

#### **Fase 1, días 0 a 30 — Victorias Tempranas sin dependencias técnicas pesada**

La primera fase no busca construir capacidades avanzadas de IA.
Primero necesitamos resolver dos problemas fundamentales:

- falta de visibilidad,
- y automatizaciones básicas que hoy siguen llegando a agentes.

La primera acción es corregir el problema de `Left Blank`.

- Ya que actualmente, cerca de 197,000 contactos — aproximadamente el 25% de toda la operación — no tienen subcategoría registrada.

Eso significa que:
- el sistema pierde granularidad,
- dificulta el análisis causal,
- limita el routing inteligente,
- y además reduce la capacidad futura de entrenamiento NLP.


Por eso proponemos hacer obligatoria la captura de subcategoría dentro del CRM.

Porque operacionalmente existe una regla simple:

> No podemos optimizar lo que no podemos medir.

Y esto es importante:  
esta fase no solo mejora reporting.  
También crea la base de datos que necesitaremos más adelante para entrenar nuevos intents y mejorar automatización

Ahora, una vez recuperamos visibilidad, el segundo quick win es activar correctamente intents FAQ de alta frecuencia.

El mejor ejemplo es:  
`Explain how to order`.

Actualmente genera más de 56,000 contactos que siguen terminando en agentes humanos.

Y aquí aparece algo importante:  
- este flujo no requiere integraciones complejas.  
- No necesita OMS.  
- No necesita APIs externas.  
- No necesita autenticación avanzada.

La respuesta es prácticamente estática.

Por eso esta iniciativa tiene el mejor ratio impacto-esfuerzo de toda la propuesta:

- bajo costo técnico,
- implementación rápida,
- e impacto inmediato en Containment Rate.


Ahora bien, después de resolver quick wins y mejorar observabilidad, el siguiente cuello de botella ya no es de diseño conversacional.

Es de capacidad transaccional.
#### **Fase 2, días 30 a 60 — Core Transaccional. La integración que desbloquea la resolución real**

Aquí entramos al principal hallazgo técnico de todo el análisis:

- el bot sí entiende muchas intenciones,  
- pero no puede completar la resolución.

Y esto ocurre especialmente en procesos post-compra.

## (Señala las barras de “Return status” e “In transit”)
Por ejemplo:
- `Return status`
- e `In transit`

si recordamos, representan juntos más de 91,000 contactos.

Y si lo pensamos desde la experiencia del cliente, el flujo actual funciona así:
1. El cliente entra al chat preguntando por su devolución o envío.
2. El bot entiende correctamente la intención.
3. Pero en ese momento encuentra una limitación crítica:  
    no tiene acceso al OMS ni al sistema de tracking.
4. Entonces escala el caso al agente.
5. El agente abre manualmente el sistema, consulta el estado y responde.

Y aquí está el insight clave:
- El problema no es NLP.  
- El problema es ausencia de integración transaccional.

Porque responder este caso no requiere razonamiento complejo.  
Solo requiere consultar información que ya existe en un sistema.

Y mientras esa integración no exista:
- los contactos seguirán escalando,
- el canal híbrido seguirá creciendo,
- y los clientes seguirán recontactando cuando no reciben actualizaciones.

De hecho, este es precisamente el mecanismo que explica gran parte del 28% de Repeat Rate reportado en el Business Case.

Por eso esta fase propone:
- integración OMS,
- integración con tracking APIs,
- autenticación de usuario,
- y resolución automática end-to-end desde el bot.

Esta es la fase con mayor impacto esperado sobre:
- Resolution Rate,
- reducción de escalaciones,
- y disminución de contactos repetidos.



Ahora, incluso si resolvemos integraciones y automatización, todavía queda un problema más :

**el sistema aún tiene conversaciones que ni siquiera logra clasificar correctamente.**

Y eso nos lleva a la Fase 3.

#### **Fase 3, días 60 a 90 — Eliminar la Falsa Contención**

Aquí abordamos el problema de falsa contención.
El análisis mostró que:
- el 82.5% de los contactos `Not defined by Bot`
- permanecen en el canal `bot_only`
- sin escalar correctamente a un agente humano.

Eso significa que el bot:
- no entendió la intención,
- pero tampoco transfirió el caso.

Desde el punto de vista del sistema, el contacto aparece como “contenido”.  
Pero desde el punto de vista del cliente, el problema nunca fue resuelto.

Es decir:
- hay contención en métricas, 
- pero abandono en experiencia real.

## (Señala rápidamente Left Blank Monitor)

Y este problema se conecta directamente con la Fase 1.

Porque hoy existen casi 197,000 contactos `Left Blank` donde la operación no está capturando suficiente información.

A medida que esa visibilidad mejore:
- aparecerán nuevos patrones recurrentes,
- nuevas subcategorías,
- y nuevos intents entrenables.

Por eso la Fase 3 tiene dos objetivos:
1. expandir la cobertura del árbol de intents,
2. y mejorar la lógica de fallback y escalamiento inteligente.


La meta final no es únicamente aumentar contención.

La meta es lograr:
- contención con resolución real,
- menor abandono,
- y una experiencia consistente de extremo a extremo.


### En resumen:
- La Fase 1 mejora observabilidad y captura quick wins.
- La Fase 2 habilita resolución transaccional real.
- Y la Fase 3 transforma al bot de un sistema reactivo a una plataforma conversacional realmente inteligente.

Y lo más importante es que el roadmap está priorizado sobre evidencia cuantitativa:  
cada iniciativa fue seleccionada por volumen impactado, fricción operacional y potencial de mejora en KPI.










# NO


1. **Primero Governanza de Datos — Eliminación de “Left Blank”:**
	1. Se piensa capturar de subcategoría en el CRM (Gestión de la Relación con el Cliente) para eliminar los $197,000$ contactos que hoy quedan sin clasificar como `Left Blank`. 
	2. Pues casi el $25\%$ de la operación es actualmente un punto ciego analítico. 
	3. Sino se corrige esto, cualquier primero, cualquier decisión de inversión en Fase 2 y Fase 3 estará basada en datos incompletos.
	4. dado que no podemos optimizar lo que no podemos medir
2. La segunda acción es Activar el enrutamiento correcto para las FAQs de alta frecuencia.
	1. `Explain how to order` tiene $56,000$ contactos yendo a agentes humanos
	2. y como se vió en la Página 2, este *intent* tiene complejidad baja y cero integraciones requeridas ya que la respuesta es siempre la misma para cualquier usuario
	3. 

#### **Fase 2, días 30 a 60 — Core Transaccional. La integración que desbloquea la resolución real**

Esta fase es sobre darle al bot la capacidad de hacer lo que hoy solo un agente puede hacer.

En la tabla, la fila de 'OMS Integration: Return status + In transit':
1. Muestra $91,804$ contactos impactados con un impacto proyectado de `Resolution Rate` +8pp y `Repeat Rate` -4pp.
2. Son los números más altos de impacto en KPI de toda la tabla. Y no es casualidad, porque estos dos intents generan el ciclo más dañino de toda la operación.
3. Si lo pensamos desde la perspectiva del cliente, en donde hizo una devolución y lleva varios días sin saber si fue aprobada
	1. Contacta al bot. El bot lo saluda, identifica que quiere saber el estado de su devolución, y en ese momento se topa con la pared: ***no tiene acceso al sistema donde está esa información***
	2. Ahí luego Escala al agente.
	3. El agente busca en el OMS, le da la respuesta en tres minutos y cierra el caso
4. Ese contacto fue resuelto, pero consumió tiempo de un agente humano para responder algo que era una consulta de lectura pura: ***solo requería mirar un dato en un sistema***
5. Y si ese mismo cliente no recibe una actualización proactiva en los días siguientes, vuelve a contactar.

**Ese es el mecanismo exacto que genera el 28% de Tasa de Contacto Repetido.**

## (Señala Return status e In transit en el gráfico de barras de la parte inferior de Página 2)

![[Pasted image 20260611215840.png]]

Y si recordamos lo que vimos en la página anterior 
- el `Return status`tenía $61,857$ contactos 
- 'In transit' tenía 29,947.
- Son 91,000 contactos que hoy dependen de que un agente abra el OMS manualmente para responder una pregunta cuya respuesta ya existe en un sistema.
- Es por eso que la integración que construimos en esta fase es conceptualmente directa: 
	- una conexión API entre la plataforma del bot y el OMS 
	- que le permita autenticar al usuario, tomar su número de orden 
	- y devolver el estado en tiempo real, sin intervención humana.


#### **Fase 3, días 60 a 90 — Eliminar la Falsa Contención**

Para entender esta fase necesito que miremos este gráfico de la derecha.

>**el 82.5% de los contactos no definidos son gestionados por el bot sin resolución.**

## **Qué nos quiere decir esto?**
## **(Señala las dos barras del gráfico: Bot Only en rojo, Hybrid en amarillo)**
Tenemos aquí los contactos que el sistema etiqueta como `Not defined by Bot`
- Son contactos donde el bot no pudo identificar en absoluto a qué categoría pertenece la intención del usuario.
- Es decir, que el modelo de lenguaje recibió el mensaje del cliente, intentó clasificarlo, y no encontró ninguna *intent/inteción* conocida que coincidiera.

Ahora, lo que esperaríamos que ocurriera en ese escenario es que el bot reconociera su propia limitación y escalara el contacto a un agente humano
- Eso sería lo correcto. Pero lo que este gráfico nos muestra es que el 82.5% de esos contactos —$4,800 $de los $5,800$ totales — se quedó en el canal bot-only.
- El bot no escaló. Se quedó gestionando algo que no entendía.

**Entonces, ¿Qué le pasa al cliente en ese momento?**

El bot entra en un bucle:
- Le pide que reformule la pregunta. 
- El cliente reformula. 
- El bot sigue sin entender. 
- Le pide que reformule de nuevo. 
- El cliente, frustrado, cierra la ventana. 
- El sistema registra ese contacto como `contenido/contained` porque técnicamente nunca llegó a un agente.
- Pero el cliente no recibió ninguna respuesta.

**Es contención en los números y abandono en la realidad. Por eso lo denominamos Falsa Contención.**


## **(Pausa. Señala brevemente el Left Blank Monitor a la izquierda antes de volver al argumento central)**


Y este problema no está aislado. Si miran el monitor de 'Left Blank' a la izquierda,
- `Customer Feedback` tiene $77,000$ contactos sin subcategoría registrada, 
- `Returns & Refunds` tiene $47,00,$ 
- `Spam` y `No Contact` tiene $42,000$

Son **categorías enteras** donde ***ni el bot ni los agentes están capturando con qué subconsulta específica llegó el cliente***

- Eso significa que incluso cuando un agente resuelve el caso, el sistema no aprende qué fue lo que resolvió.
- Es decir, la operación trabaja pero no acumula inteligencia.

## (Vuelve al gráfico de Falsa Contención)

Es por eso que La Fase 3 ataca este problema desde dos ángulos:

1. **El primero es ampliar la cobertura de intents en la plataforma del bot**. 
	1. Hoy los contactos`not defined `son $5,800$, que parece poco. Pero ese número es solo lo que podemos ver. 
	2. Los $197,000$ `Left Blank` de la **Fase 1** que empezamos a clasificar correctamente van a revelar nuevos patrones de intención que hoy son invisibles. 
	3. Es posible que existan miles de consultas recurrentes que el bot nunca ha podido categorizar simplemente porque nadie las registró
	
 
 La Fase 1 nos da la visibilidad; la Fase 3 actúa sobre ella.