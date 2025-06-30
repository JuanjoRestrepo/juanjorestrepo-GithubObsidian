
![[Diagrama_Plantilla_Diseño_RPA.png]]

Están las siguientes etapas:

1. Inicializar (Initialize)
2. Obtener (Get)
3. Procesar (Process)
4. Finalizar (Finish)

Cada una de esas etapas puede tener un flujo interno y pueden darse 2 opciones:

# 1. Inicializar
_______________________________________________________
1. Que en la etapa de *Inicializar* tengamos un flujo creado, algo muy similar a:
		![[Pasted image 20230809152551.png]]

2. Que dentro de la misma máquina de estado, podamos tener interacción con las mismas aplicaciones, en donde está simplemente la descripción
		![[Pasted image 20230809152645.png]]

# 2. Obtener
_______________________________________________________
Aquí va a depender mucho del tipo de asistente. Si es un asistente de tipo *Despachador (Dispatcher)* o *Performador (Performer)*

1. **Si es Dispatcher:** significa que la cola que está apuntando hacia *Procesar*
		![[Pasted image 20230809153326.png]]
		
	significa que la información que se está tratando de capturar va directamente al *Orchestrator* a una *Cola* para ser procesada después. 
	De ahí estamos hablando de un **Proceso tipo Dispatcher** en donde en el *Obtener* vamos a los aplicativos, que iniciamos en la etapa de *Inicializar*, luego obtenemos datos y todo tipo de información que venga de un origen de datos, (El origen depende del tipo de proceso que se esté trabajando)

	Nota: Dependiendo del tipo de proceso nos daremos cuenta si es un Dispatcher o Performer y de dónde viene el origen de datos

En el proceso *Obtener* voy a extraer la información de una Cola, esa Cola está en el *Orchestrator*. 
Entonces cuando obtenga la información de la Cola, me voy automáticamente a *Procesar* para empezar a trabajar con esa información. Por esa razón existen esas dos colas como se ve en la siguiente imagen:

	![[Pasted image 20230809154001.png]]

Ya dependiendo del proceso, la persona del diseño determina:

1. **Si es un Robot Dispatcher:** la información se obtiene de una base de datos, de SAP, etc...
2. **Si es un Robot Performer:** la información se obtiene de una cola y se carga en la etapa de *Procesar*

# 3. Procesar
_______________________________________________________
Aquí es donde se manipula la data que se trajo del estado de *Obtener*. Entonces aquí podemos hacer lo siguiente:
1. Limpiar y organizar la data
2. Aplicar las reglas del negocio que se requieren integrar en el robot de acuerdo

Y obviamente, si es un *Robot Dispatcher*, esa data debe quedar almacenada en alguna parte al final de ser procesada. Entonces deberá ser cargada a una *Cola* para que otro Robot entre, la tome y la procese.

# 4. Finalizar
_______________________________________________________
Aquí vamos a poder cerrar todos esos aplicativos con los que se trabajaron durante la ejecución del asistente.
Entonces en esta etapa *finalizar* podemos encontrar un flujo que va a indicar cómo se cierran los aplicativos o simplemente el Pantallazo con los pasos sobre cómo cerrar el aplicativo.
Pero adicionalmente, tenemos la parte de eliminar o depurar el *DW*, porque ***NO DEBE QUEDAR NINGÚN ARCHIVO EN EL DW*** para no quedarnos sin espacio

NOTA: Tener en cuenta que esa información que se va a eliminar del *DW* no esté siendo usada por otro robot.
## ¿Cuándo la eliminamos? 
Cuando el Performer termine su ejecución.

![[Etapa_Finalizar.png]]

Adicional al reporte *DW* también tenemos un *Reporte Funcional*
![[Reporte_Funcional.png]]

La idea es que todos los robots peguen un reporte de qué hicieron durante su ejecución, con los tiempos y los comentarios en caso que haya alguno. Esto se hace para saber si una solicitud fue procesada exitosamente o si hubo un fallo durante la ejecución, ya sea un fallo de la aplicación o del negocio

## Muestra Reporte Funcional

![[Reporte_Funcional 1.png|900]]

## E-mail de Notificación
Adicional de eliminar la información del *DW* y creado el Reporte Funcional, debemos enviar un *Email* de notificación a Operación (y opcional al Negocio) que ya terminó la ejecución

![[Email_Notificacion_Finalizacion.png]]
## Reporte Técnico

Se usaría para indicadores de los robots, lo ideal es que esté en una Base de Datos.

## TEMA IMPORTANTE

En las etapas 

1. Inicializar (Initialize)
2. Obtener (Get)
3. Procesar (Process)
4. Finalizar (Finish)

Siempre se va a encontrar que las actividades que se presenten aquí

![[Pasted image 20230809152551.png]]

Van a tener una responsabilidad única. Esto va a la Programación Orientada a Módulos. En donde el módulo principal es el *Framework*

![[Pasted image 20230809161431.png]]

Y unos módulos secundarios, que son los que tendrán responsabilidades únicas, de cuáles son sus tareas (Iniciar un aplicativo, hacer un filtro de una data, procesarla, etc...)

![[Pasted image 20230809152551.png]]


# ¿Cómo son los procesos por dentro?

# 1. Inicialización

![[Pasted image 20230809165418.png]]
### Tipo de error si no se conecta a SAP

![[Pasted image 20230809165437.png]]

# 3. Procesar

![[Pasted image 20230809165645.png]]


