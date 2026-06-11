
Buen día a todos, mi nombre es Juan José Restrepo y hoy les vengo a presentar el análisis del Caso del Chatbot de Large Action Model de Adidas

> los LAM están entrenados para **ejecutar acciones** concretas dentro de aplicaciones y sistemas digitales

# (Página 1 — Executive Overview)
El contexto inicial rápidamente era que...

Si observamos nuestros KPIs actuales, se está fallando en tres frentes simultáneamente:
- la Tasa de Contención está en 48% contra una meta del 55%
- la Tasa de Contacto Repetido está en el 28% cuando debería ser del 18%.
- la Tasa de Resolución está apenas en el 30% contra un objetivo del 50%

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
- El sistema lo registra como un contacto 'contenido' porque técnicamente no escaló, pero en la realidad el cliente cerró la ventana sin respuesta, y luego vuelve a llamar.

### Esta dinámica explica los tres KPIs de forma simultánea: 

- la contención no llega al 55% porque el bot no termina los casos, 
- la resolución está en el 30% porque contener no es lo mismo que resolver, 
- y el contacto repetido está en el 28% porque los clientes sin respuesta vuelven. Los tres tienen la misma causa raíz."