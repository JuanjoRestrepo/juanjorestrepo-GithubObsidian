# Necesidad

En la compañía hay documentación de los robots, la idea es que el chatbot pueda traer la documentación de tal robot por medio del chatbot en lugar de buscarlo manual. La KeyWord va de acuerdo al código del robot Generar un Chatbot para la empresa de RPA. Como capturar documentos de un Drive, necesito el manual de usuario ta ta ta, el chatbot vaya al drive y traiga el link de doc. Revisar API de Google Drive, cómo se pueden hacer esos chatbots. Necesito el documento tal y que a partir de esa palabra clave, el robot vaya a buscarlo

Investigar acerca de Chatbots basados en reglas. De Google


# Investigar:

- Temas de Chatbots en GOOGLE
- Herramientas para eso
- Pruebas de concepto. Que reciba información y que le entregue opciones de acuerdo a la pregunta del usuario. 
- Todo en la suite de Google

_________________________________________________________

## Temas de Chatbots en Google:

1. **Dialogflow:** Es una plataforma de desarrollo de chatbots de Google que utiliza técnicas de procesamiento de lenguaje natural (NLP) para crear conversaciones interactivas con los usuarios. Dialogflow permite diseñar flujos de conversación, definir reglas y entrenar al chatbot para comprender y responder a las preguntas de los usuarios.
    
2. **Google Assistant:** Es un asistente virtual desarrollado por Google que permite a los usuarios interactuar con dispositivos y servicios utilizando comandos de voz. Los desarrolladores pueden crear aplicaciones y chatbots que funcionen en el ecosistema de Google Assistant.

## Herramientas para Chatbots en Google:

1. **Dialogflow:** Como se mencionó anteriormente, Dialogflow es la herramienta principal para crear chatbots basados en reglas dentro del ecosistema de Google.
    
2. **Google Cloud Platform:** Puedes utilizar las capacidades de Google Cloud para alojar y gestionar tu chatbot. Google Cloud ofrece una variedad de servicios que pueden ser útiles para implementar y escalar tus soluciones de chatbot.
    
## Pruebas de Concepto:

Puedes realizar pruebas de concepto utilizando Dialogflow para crear un chatbot que reciba información y proporcione opciones en función de la pregunta del usuario. Aquí hay una descripción general de cómo podrías abordar esto:

1. **Definir Intenciones:** En Dialogflow, define las "intenciones" que representarán las preguntas o frases que los usuarios podrían decir. Asocia estas intenciones con respuestas predefinidas o acciones específicas.
    
2. **Crear Reglas de Respuesta:** Dentro de cada intención, puedes configurar respuestas basadas en reglas. Por ejemplo, si un usuario pregunta sobre restaurantes, el chatbot podría proporcionar opciones como "Mostrar restaurantes cercanos" o "Mostrar restaurantes de comida italiana".
    
3. **Desarrollar Flujo de Conversación:** Configura el flujo de conversación estableciendo preguntas y respuestas secuenciales. Puedes usar entidades para extraer información específica de las preguntas del usuario.
    
4. **Probar en la Consola de Pruebas:** Utiliza la consola de pruebas de Dialogflow para interactuar con el chatbot y verificar cómo responde a diferentes entradas.
    
## Suite de Google:

Tanto Dialogflow como Google Assistant son parte del ecosistema de Google, lo que los convierte en herramientas adecuadas para cumplir con los requisitos de tu proyecto dentro de la suite de Google.

Recuerda que esta es una guía general para abordar tu proyecto. Te recomiendo explorar la documentación oficial de Dialogflow y Google Cloud Platform para obtener detalles más específicos sobre la implementación y las mejores prácticas. ¡Buena suerte con tu investigación y proyecto!

_________________________________________________________
Los **chatbots** son programas informáticos diseñados para interactuar con usuarios humanos a través de lenguaje natural, simulando una conversación fluida

. La misión principal de los chatbots es brindar respuestas, asistencia y realizar tareas específicas de manera eficiente y sin intervención humana directa.

Los chatbots basados ​​en reglas, o chatbots con secuencias de comandos, son la forma más antigua de chatbots que se desarrollaron en función de reglas o secuencias de comandos predefinidas. Las respuestas están diseñadas en base a un script predefinido mediante una serie de declaraciones condicionales que verifican las palabras clave o frases en la entrada del usuario y brindan las respuestas correspondientes según estas condiciones.

la arquitectura de los chatbots basados ​​en reglas generalmente consta de 3 partes en un nivel alto: la interfaz de usuario, el motor de procesamiento de lenguaje natural (NLP) y el motor de reglas.

1. **Interfaz de usuario:** la interfaz de usuario es la plataforma o aplicación a través de la cual el usuario interactúa con el chatbot. Puede ser un sitio web, una aplicación de mensajería o una plataforma que admita la comunicación basada en texto.
2. **Motor de procesamiento de lenguaje natural (NLP):** El motor [de NLP](https://www.analyticsvidhya.com/blog/2022/01/nlp-tutorials-part-i-from-basics-to-advance/) es responsable de procesar la entrada del usuario y convertirla en un formato legible por máquina. Implica dividir la entrada del usuario en palabras, identificar las partes del discurso y extraer información relevante, ya sea haciendo el mapeo de sinónimos, la revisión ortográfica y la traducción de idiomas.

4. **Motor de reglas:** el motor de reglas es el cerebro del chatbot. Es responsable de interpretar la entrada del usuario, determinar la intención y seleccionar la respuesta adecuada según las reglas predefinidas. Por ejemplo, si la entrada del usuario contiene una palabra clave específica, el chatbot tendrá una respuesta particular o realizará una acción específica.


 El motor de reglas contiene un conjunto de árboles de decisión, donde cada nodo representa una regla específica que debe seguir el chatbot.
# DialogFlow

Dialogflow es una plataforma de comprensión del lenguaje natural que facilita el diseño y la integración de una interfaz de usuario conversacional en su aplicación móvil, aplicación web, dispositivo, bot, sistema de respuesta de voz interactivo, etc. 

Herramienta de Google que permite construir asistentes virtuales de voz y texto. Permite construir interfaces conversacionales ricas y naturales de manera sencilla.

Con Dialogflow, puede proporcionar formas nuevas y atractivas para que los usuarios interactúen con su producto. Dialogflow puede analizar múltiples tipos de entradas de sus clientes, incluidas entradas de texto o audio (como desde un teléfono o una grabación de voz). También puede responder a sus clientes de varias maneras, ya sea a través de texto o con voz sintética.
[Dialogflow](https://cloud.google.com/dialogflow/docs/) 

Dialogflow nos ayuda con todo el ciclo de vida de construcción de la gente, desde la parte de gestión de la conversación, ayudándonos con un motor de comprensión del lenguaje natural, hasta la parte de integración con los diferentes canales y nuestros propios sistemas para construir respuestas ricas y customizadas para el propio usuario

![[Pasted image 20230811131237.png]]

# ¿Por qué utilizar Dialogflow?

![[Pasted image 20230811130911.png]]

**Dialogflow** nos aporta funcionalidades como:

- **Darnos velocidad de implementación:** para construir nuestro Chatbot con muy pocas interacciones de ejemplo, es decir, utilizar conjuntos de palabras que los usuarios emplean para interactuar con el modelo y para ello se requerirán pocas muestras de entrenamiento para comenzar.
- **Consta de más de 40 agentes preconfigurados:** para construir agentes de cualquier tipo, es decir, si queremos por ejemplo crear un agente que se encargue de gestionar tickets, podes usar el modelo base como punto de partida y customizarlo en base a nuestras necesidades

	- Un agente virtual que maneja conversaciones simultáneas con sus usuarios finales. Es un módulo de comprensión del lenguaje natural que comprende los matices del lenguaje humano. Dialogflow traduce el texto o el audio del usuario final durante una conversación en datos estructurados que sus aplicaciones y servicios pueden entender. Usted diseña y construye un agente de Dialogflow para manejar los tipos de conversaciones que requiere su sistema.
	- Un agente de Dialogflow es similar a un agente de un centro de llamadas humano. Los entrena a ambos para manejar los escenarios de conversación esperados, y su entrenamiento no necesita ser demasiado explícito.

- **Conseguir interacciones más eficientes con los usuario:** gracias a las capacidades de comprensión del Lenguaje Natural se incorpora para que las interacciones sean mucho más naturales
- **Múltiples opciones de integración:** de manera que sea posible incorporar diferentes sistemas al Chatbot. Como por ejemplo, integrar el Dialogflow a un sistema de reservas de un restaurante en tiempo real, para así monitorear si hay disponibilidad y hacer la reserva.
- **Cloud Functions:** servicio de computación serverless,, que permite ejecutar programas sin tener que gestionar ningún servidor, de forma que se puedan construir respuestas con mayor complejidad
- **Incorpora Herramientas de Analítica:** para una mejora constante del Chatbot, en base a cómo lo utilizan los usuarios.
- Despliegue en cualquier plataforma, como Twilio, Facebook, Google Home, etc...

## SDK: 
A software development kit (SDK) is a set of software tools and programs provided by hardware and software vendors that developers can use to build applications for specific platforms. SDKs help developers easily integrate their apps with a vendor's services.

# Conceptos a tener claros antes de desarrollar nuestro Chatbot

## 1. Intenciones
Son los objetivos o acciones que queremos lograr con nuestro Chatbot. Por ejemplo, en el caso del restaurante pueden ser:
- Reservar una mesa
- Consultar el menú
- Consultar los horarios
- Ubicación (sedes)

## 2. Entidades
Es lo que nos permite extraer información importante en base a las interacciones del usuario, bien sea, porque el usuario en la primera petición ya nos está dando esa información o mediante preguntas que vendrán posteriormente para tener claro qué es lo que busca.
En el caso de la reserva de una mesa, necesitamos conocer:
- En qué restaurante
- En qué día (hora)

Las entidades pueden ser de tipo abierto, como una fecha, o más específicas, como el nombre de los restaurantes, esto será un número de opciones cerrado

## 3. Contexto
Es importante que la conversación tenga un flujo lógico, es decir, si primero se pregunta por el menú del restaurante y posteriormente, que queremos reservar una mesa en ese restaurante, no es lógico volver a preguntar cuál es el nombre del restaurante

Es por eso que es bueno jugar con los contextos para transferir la información entre las diferentes intenciones y que la conversación sea lo más natural posible.

# 4. Cumplimiento
Cuando ya sea tiene bien definida toda la conversación, se pasa a la ejecución.
En el caso del restaurante, lo que se busca es reservar una mesa, es decir, queremos **verificar en el sistema si hay un espacio libre** y **ejecutar una reserva** para que luego se **bloquee ese espacio libre**

## Dialogflow CX and ES

Dialogflow proporciona dos servicios de agente virtual diferentes, cada uno de los cuales tiene su propio tipo de agente, interfaz de usuario, API, bibliotecas de clientes y documentación:

|   |   |
|---|---|
|[Dialogflow CX](https://cloud.google.com/dialogflow/cx/docs)|Proporciona un tipo de agente avanzado adecuado para agentes grandes o muy complejos.|
|[Dialogflow ES](https://cloud.google.com/dialogflow/es/docs)|Proporciona el tipo de agente estándar adecuado para agentes pequeños y simples.|

## Agent types

Los siguientes tipos de agentes están disponibles:

|   |   |
|---|---|
|[CX agent](https://cloud.google.com/dialogflow/cx/docs/basics)|Este es un tipo de agente avanzado que es adecuado para agentes grandes o muy complejos. [Flows](https://cloud.google.com/dialogflow/cx/docs/concept/flow) y [pages](https://cloud.google.com/dialogflow/cx/docs/concept/page) son los componentes básicos del diseño de conversaciones y [controladores de estado](https://cloud.google.com/dialogflow/cx/docs/concept/handler)|
|[ES agent](https://cloud.google.com/dialogflow/es/docs/basics)| Este es el tipo de agente estándar que es adecuado para agentes pequeños a medianos y simples a moderadamente complejos. Las [intenciones](https://cloud.google.com/dialogflow/docs/editions) son los componentes básicos del diseño de la conversación y los [contextos](https://cloud.google.com/dialogflow/es/docs/contexts-overview) se utilizan para controlar las rutas de la conversación.|

# Bibliografía

1. [GCloud](https://gcloud.devoteam.com/es/blog/que-es-dialogflow-asistente-virtual-google/)
2. [My Playlist](https://www.youtube.com/playlist?list=PLlA18wVsi2ZU6J8TyXjq3DTT6Ty8bsgyn)
3. [Creating Chatbots on Google Cloud - Google for Developers](https://developers.google.com/learn/topics/chatbots)

_________________________________________________________
# Alternativas a Dialogflow
Existen varias alternativas a Dialogflow que también ofrecen capacidades de desarrollo de chatbots y procesamiento de lenguaje natural. Algunas de las alternativas populares incluyen:

1. **Microsoft Bot Framework:** Desarrollado por Microsoft, este marco proporciona herramientas para crear chatbots y asistentes virtuales en múltiples plataformas. Incluye integración con servicios de Microsoft como Azure Cognitive Services para el procesamiento de lenguaje natural. 
	[MS Bot Framework](https://dev.botframework.com)
    
2. **Amazon Lex:** Proporcionado por Amazon Web Services (AWS), Lex permite crear chatbots de voz y texto utilizando tecnología de reconocimiento de voz y procesamiento de lenguaje natural. Es especialmente adecuado para integrarse con los asistentes virtuales de Amazon, como Alexa.
    
3. **IBM Watson Assistant:** Ofrecido por IBM, Watson Assistant permite crear chatbots y asistentes virtuales con capacidades de NLP y análisis de sentimiento. Puedes integrarlos en aplicaciones web, móviles y dispositivos de IoT.
	[IBM CHATBOTS](https://www.ibm.com/topics/chatbots?utm_medium=OSocial&utm_source=Youtube&utm_content=000027BD&utm_term=10004432&utm_id=YTDescription-101-What-is-a-Chatbot-LH-AI-Virtual-Assistant-vs-Chatbot-Guide)
	
4. **Wit.ai:** Propiedad de Facebook, Wit.ai es una plataforma de procesamiento de lenguaje natural que permite construir chatbots y aplicaciones interactivas. Está diseñada para ser fácil de usar y ofrece una API para la comprensión del lenguaje.
    
5. **Rasa:** Rasa es una plataforma de código abierto que permite a los desarrolladores crear chatbots y asistentes virtuales personalizados. Ofrece control total sobre el flujo de conversación y se puede integrar con diferentes canales de comunicación.
    
6. **Botpress:** Otra opción de código abierto, Botpress permite crear chatbots y asistentes virtuales con una interfaz gráfica intuitiva. Ofrece características como flujos de conversación, integraciones y personalización.
    
7. **SnatchBot:** Esta plataforma en la nube permite crear chatbots de texto y voz sin necesidad de programación. Ofrece una interfaz visual para diseñar flujos de conversación y es adecuada para casos de uso variados.
    
Estas son solo algunas de las alternativas disponibles en el mercado. Cada una tiene sus propias características, ventajas y enfoques, por lo que te recomiendo investigar más sobre cada una para determinar cuál se adapta mejor a las necesidades de tu proyecto.

# Watch the following videos

|Título   |Link   |
|---|---|
|Video 1|[Halc Zone](https://www.youtube.com/watch?v=YkT6Jeq4IGk&t=87s) |
|Video 2|[Crea tu primer agente conversacional con Dialogflow](https://www.youtube.com/watch?v=b0QU7XGX5F8)|
|Video 3|[RPA with Chatbots Using UiPath and Google Dialog Flow](https://www.youtube.com/watch?v=QL7mxjjs0Ps&list=PLKGu_xEgzk3tbEulshDo6Yi3r9hg_iT_e)|
|Video 4|[Build UiPath Chatbot with Google Dialogflow](https://www.youtube.com/watch?v=__5luCyqoJI)|
|Video 5|[Connect Chatbot To Backend - Dialogflow Fulfillment - Ultimate Tutorial](https://www.youtube.com/watch?v=8ao93nfjeSo)|

# UiPath and Druid

Video
https://www.uipath.com/resources/automation-demo/uipath-chatbots-automate-conversational-processes

Druid
https://cloud.uipath.com/uipatgnynbwq/marketplace_/listings/druid-chatbot

Amelia
https://www.uipath.com/solutions/technology/amelia-conversational-ai

Tqlia
https://cloud.uipath.com/uipatgnynbwq/marketplace_/listings/tqa-chatgpt?utm_source=internal&utm_medium=related&utm_campaign=openai9789&clickSource=Listings.Related&clickSource=Listings.Related


