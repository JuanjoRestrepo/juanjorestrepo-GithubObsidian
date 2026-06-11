
Buen día a todos, mi nombre es Juan José Restrepo y hoy les vengo a presentar el análisis del Caso del Chatbot de Large Action Model de Adidas

> los LAM están entrenados para **ejecutar acciones** concretas dentro de aplicaciones y sistemas digitales

El contexto inicial rápidamente era que...

Si observamos nuestros KPIs actuales, estamos fallando en tres frentes simultáneamente:
- la Tasa de Contención está en 48% contra una meta del 55%
- la Tasa de Contacto Repetido está en el 28% cuando debería ser del 18%.
- la Tasa de Resolución está apenas en el 30% contra un objetivo del 50%

A primera vista, la hipótesis sería que 
	***los usuarios rechazan el bot o no confían en él***.

Pero este gráfico nos dice lo contrario: 

Tenemos tres canales de atención
1. El canal de `agentes humanos` maneja 398,000 contactos — casi el 50% del volumen total.
2. El canal `híbrido`, donde el bot inicia pero un agente termina, maneja 277,000 contactos — otro 35%
3. Y el canal `bot-only`, donde el bot resuelve de inicio a fin sin intervención humana, maneja 124,000 contactos — apenas el 15.5%.

	***el bot participa activamente en el 50.2% de todas las interacciones.***

**(Señala el callout debajo del gráfico de barras de distribución por canal)**

![[Pasted image 20260611164757.png]]

El problema raíz no es de adopción. 

El problema es lo que yo denomino **Falsa Contención**: 
	el bot saluda, clasifica la intención del usuario, pero al carecer de capacidad transaccional, no puede resolver.

El sistema lo registra como un contacto 'contenido' porque técnicamente nunca llegó a un agente, pero en la realidad el cliente cerró la ventana sin respuesta.