---
banner: " https://enterprisersproject.com/sites/default/files/styles/large/public/2021-09/cio_automation_ai.png?itok=JO5heHa6"
tags:
  - CPI
  - Semestre8
---
# Automatización

Es el **proceso de diseño e implementación de tecnología y sistemas** que se usan para controlar y operar procesos y maquinarias de manera automática, sin la intervención humana directa

Se pueden emplear elementos computarizados, **electromecanicos, electroneumáticos y electrohidráulicos** para **realizar tareas secuenciales sin la intervención humana**

#### Existen dos tipos de automarización:

1. Automatización Basada en **Lógica Cableada**

	También conocida como automatización de relés, se basa en la interconexión física de dispositivos eléctricos y electrónicos, como cables y contactos, para controlar y automatizar procesos.

	Técnica para realizar **circuitos que controlan un proceso** de forma semiautomática o automática, en donde el tratamiento de datos se efectúa en conjunto con **Contactores, Bobinas, Relés, Temporizadores, Contadores**, etc...
	
1. Automatización Basada en **Lógica Programada**

	Utiliza sistemas programables, como los Controladores Lógicos Programables (PLCs), para controlar procesos y tareas de producción.
	Este tipo de automatización es muy flexible, ya que se pueden realizar cambios en el programa para adaptarse a diferentes procesos y detectar posibles errores.

##### Ventajas y Desvantajas
![[Pasted image 20230425223028.png|800]]


## Circuitos de Fuerza y Mando

En **todo sistema de lógica cableada** se distinguen dos partes principales:

1. **Circuito de FUERZA O POTENCIA**

	Se utilizan para **suministrar energía eléctrica a los dispositivos eléctricos y electrónicos** de la **maquinaria o el proceso industrial**. Estos circuitos suelen ser de **alta potencia y tensión**, y y se utilizan para controlar motores, calefacción, iluminación, entre otros.

	Los componentes principales de un circuito de fuerza/potencia incluyen **fusibles, interruptores de circuito, contactores, relés, motores y transformadores.**
	

1. **Circuito de MANDO O CONTROL**

	Se utilizan para **controlar los dispositivos eléctricos y electrónicos** de la maquinaria o el proceso industrial. Estos circuitos suelen ser de **baja potencia y tensión**, y se utilizan para controlar el funcionamiento de los dispositivos eléctricos y electrónicos.

	Los componentes principales de un circuito de mando/control incluyen **botones pulsadores, selectores, lámparas piloto, relés de control, Controladores Lógicos Programables (PLCs) y sensores.**

![[Pasted image 20230425215341.png]]

![[Pasted image 20230425220552.png|700]]

### **Elementos de Protección**

Es muy importante considerar los elementos de protección necesarios para garantizar la seguridad del personal y de los equipos.

1. Para las personas
	- Sistemas de puesta a tierra
	- Interruptor diferencial

3. Para la instalación
	- Fusibles
	- Interruptores
	- Sistemas de puesta a tierra
	
5. Para las cargas
	- Relé térmico
	- Guardamotor


### Fusibles: 
Son dispositivos de protección que **se utilizan para proteger los circuitos eléctricos contra sobrecargas y cortocircuitos**. Los fusibles se funden **cuando la corriente que pasa a través de ellos supera su capacidad nominal, interrumpiendo la circulación de la corriente** y protegiendo el circuito.
    
### Interruptores diferenciales (ID): 
Se utilizan para **proteger a las personas contra descargas eléctrica**s. Los ID **detectan la corriente de fuga a tierra y desconectan automáticamente la alimentación eléctrica** si se produce una fuga de corriente peligrosa.
    
### Interruptores magnetotérmicos: 
Son dispositivos de protección que se utilizan para **proteger los circuitos eléctricos contra sobrecargas y cortocircuitos**. Los interruptores magnetotérmicos pueden ser rearmables y **se activan cuando la corriente eléctrica supera un cierto valor límite.**
    
### Barreras de seguridad: 
Las barreras de seguridad se utilizan para separar las áreas peligrosas de los equipos y maquinarias en la automatización industrial, evitando el acceso de los trabajadores a estas zonas y minimizando los riesgos de accidentes.
    
### Sistemas de parada de emergencia: 
Los sistemas de parada de emergencia se utilizan para **detener de forma inmediata la maquinaria y los equipos en caso de emergencia.** Estos sistemas pueden ser accionados por un botón de emergencia o por una señal externa.

### Puestas a tierra: 
Se utilizan para **evitar descargas eléctricas y garantizar que los equipos y maquinarias estén conectados a una referencia de voltaje común**. Una puesta a tierra adecuada **reduce los riesgos de electrocución y protege los equipos y sistemas eléctricos contra daños debido a sobretensiones y cortocircuitos**.

### Disyuntor termomagnético:
Dispositivo de protección utilizado en sistemas eléctricos para proteger contra sobrecargas y cortocircuitos. Este dispositivo combina las funciones de un disyuntor térmico y un disyuntor magnético en un solo equipo.

La función del disyuntor térmico es proteger el circuito eléctrico contra sobrecargas prolongadas. Si la corriente eléctrica en el circuito supera el valor nominal del disyuntor durante un período de tiempo determinado, el elemento térmico del disyuntor se activa y abre el circuito, interrumpiendo el flujo de corriente eléctrica.

La función del disyuntor magnético es proteger el circuito eléctrico contra cortocircuitos. Si la corriente eléctrica en el circuito supera un valor muy alto, el campo magnético generado en la bobina del disyuntor magnético actúa sobre la armadura, produciendo una fuerza mecánica que abre el circuito eléctrico.



    
### Relés de protección: 
Dispositivos que se utilizan para **proteger los equipos y sistemas eléctricos contra sobrecargas, cortocircuitos y otros tipos de fallas.** Los relés de protección **detectan cambios en la corriente, la tensión y otros parámetros eléctricos, y activan un sistema de protección para interrumpir el suministro eléctric**o antes de que se produzca un daño irreparable.

### Relés térmicos:
Se utilizan para **proteger los motores eléctricos contra sobrecargas térmicas y fallas de arranque prolongado.**
Funciona mediante la medición de la temperatura del motor. **Cuando la temperatura del motor aumenta por encima de un cierto nivel preestablecido, el relé térmico se activa y desconecta la alimentación eléctrica al motor**, evitando daños y prolongando la vida útil del motor.

![[Pasted image 20230425222134.png|600]]
![[Pasted image 20230425222156.png|600]]

![[Pasted image 20230425214531.png|650]]


## El Contactor

Componente electromagnético que tiene por objetivo controlar el flujo de corriente, ya sea en el circuito de potencia o en el circuito de mando, tan pronto se dé tensión a la bobina

Consta de dos partes:

**El conjunto de contactos y la bobina.**
	Está compuesto por dos o más contactos eléctricos que se cierran o abren cuando la bobina se energiza o se desenergiza, respectivamente.


![[Pasted image 20230425214731.png]]

El contactor tiene las siguientes funciones:

- Elemento de control de potencia en un sistema automático
- Produce una separación galvánica entre el circuito de entrada y salida
- Pueden abarcar potencias de valores muy elevados ( 0 a 750 kW )
- La corriente pasa o no pasa, no existen zonas intermedias

![[Pasted image 20230425221632.png|900]]

![[Pasted image 20230425221704.png]]
![[Pasted image 20230425221726.png]]

1. Al momento de energizar la bobina, se genera un campo magnético de gran magnitud que atrae al núcleo o armadura móvil
2. Esta armadura está unida a los contactos móviles 11, 12, 14, etc ...
3. Cuando la bobina se energiza, el campo generado atrae a la armadura y a los contactos móviles haciendo que el contacto normalmente abierto se cierre, y el normalmente cerrado se abra

### Relés electromagnético:
Se utilizan como un contactor pero de baja potencia, para poder controlar cargas de menor potencia.

- Funciona como un interruptor controlado por un circuito eléctrico
- Por medio de una bobina y un electroimán, se acciona un juego de uno o varios contactos
- Controla un circuito de salida de mayor potencia que el de entrada

![[Pasted image 20230425222116.png]]

## Leds/Pilotos de señalización y pulsadores

![[Pasted image 20230425222302.png]]

## PLC (Programmable Logic Controller/Controlador Lógico Programable)

Es un dispositivo electrónico que se utiliza para **controlar y automatizar diferentes procesos industriales**. El PLC contiene un microprocesador o microcontrolador, entradas y salidas digitales y analógicas, y una memoria para almacenar los programas.

Los PLCs **reciben información de sus entradas y son procesadas por la CPU para luego enviar una respuesta mediante sus salidas**

Está diseñado para **controlar procesos en tiempo real y en ambientes cambiantes** y **agresivos**, es decir, donde hay condiciones de altas temperaturas, precisiones, etc... para **realizar tareas repetitivas con alta precisión y seguridad**

#### **Arquitectura de un PLC**
![[Pasted image 20230425223830.png]]

#### Ventajas y Desventajas PLC
![[Pasted image 20230425224054.png]]

#### Criterios para seleccionar un PLC
![[Pasted image 20230425224509.png]]

#### Clasificación según sus estructura
![[Pasted image 20230425224907.png]]

### Arquitectura Interna de un PLC
![[Pasted image 20230425225222.png]]


- El elemento principal es la **CPU**
- **Memoria de Programa**: donde alojamos el programa. Es no volátil, es decir, que conserva el programa aunque se corte su alimentación
- **Memoria de Datos**: donde se alojan los datos de los procesos. Es volátil, es decir, que si se corta la alimentación, los datos que estén ahí se borrarán.
- **Timers**
- **Contadores**: por ejemplo para determinar la velocidad de giro de un motor, puedo utilizar un contador rápido para que me pueda leer a una elevada frecuencia
- **Memoria de Imagene (Entrada/Salida):

Todo esto se comunica por un bus interno por donde viajan todos los datos

### Componentes de un PLC

1. **Fuente de alimentación:**

	Provee electricidad a la CPU y los módulos de entrada y salida.
	Generalmente las fuentes alimentan con **220V/110V AC** y su salida manda **24V DC**.
	Son diseñadas para soportar pérdidas de energía sin afectar 
	la operación del PLC

![[Pasted image 20230425230114.png]]

2. **Carcasa o bastidor:**

  También llamado Rack o Chasis, es el componente que une todos los elementos del PLC.
  Tiene una placa base en la parte trasera que conecta de manera paralela las tarjetas de CPU y permite la comunicación entre ellas.
  Dependiendo de la aplicación, se irán agregando módulos a la carcasa para que se conecte con el PLC y los demás módulos
  ![[Pasted image 20230425230300.png]]
	
3. **CPU**

	El cerebro del PLC
	Se encarga de recibir información del módulo de entradas, para procesarlas y enviar las respuestas al módulo de salidas

- Vigilar el tiempo de ejecución de programa
- Ejecutar el programa de usuario
- Crear una imagen de entradas y salidas
- Envíar una respuesta de acuerdo al programa implementado

4. **Tipos de Memoria**
	![[Pasted image 20230425230607.png]]

5. **Módulos de expansión:** 

	Es posible agregar o expandir las funcionalidades de un PLC, en las entradas y salidas de este.

	**MODULOS DE COMUNICACIÓN**
	Permite al PLC comunicarse mediante distintos tipos de protocolos como:
	- DEVICENET
	- Ethernet/IP
	- Modbus RTU
	- Modbus TCP
	- Profibus
	- Profinet
	- OPC-UA

	**MODULOS DE ENTRADAS Y SALIDAS**
	Proveen una interface entre los componentes conectados físicamente y el CPU
	
	A través de estos, se hace el intercambio de información, ya sea para obtener datos o para el control de dispositivos en un proceso.

- **Módulos de entrada:** aceptan señales provenientes de pulsadores, sensores digitales o analógicos

	![[Pasted image 20230425231907.png]]

	Los módulos más difundidos son por norma:

**Señal de corriente:** 0 - 20 mA, 4 - 20 mA
**Señal de Voltaje/Tensión:** 0 - 10 V, 0 - 5V, 0 -2V, +- 10V

Lo **más usado son las Señales de Corriente** pues el voltaje tiene la desventaja de presentar caídas cuando se aumenta el largo de la línea de transmisición, esto representa pérdida de información

En corriente se usa el valor 4 - 20 mA como valor estándar porque así es más fácil diferenciar cuando hay o no corriente, pues 4 sería el valor mínimo, y si es menor pues se puede evidenciar algún problema, como que se abrió el cable o algo así.
	

- **Módulos de salida:** envían señales para activar salidas digitales o enviar información analógica

	![[Pasted image 20230425231419.png]]
	![[Pasted image 20230425231443.png]]

	Es la más usada porque al momento que se manda la señal de activación, esta bobina que está dentro del PLC, se energiza, crea el campo magnético y hace que el contacto normalmente abierto, se cierre
	
	Así se puede activar una salida, pues se cierra el circuito dejando pasar la corriente hacia la carga de salida.
	
	ES LA MÁS USADA PORQUE SE PUEDEN CONECTAR YA SEA A AC O DC, PUES SU FUNCIÓN ES MUY SIMPLE, SOLO ABRIR O CERRAR UN CONTACTO

	![[Pasted image 20230425232346.png]]


## Contactos

![[Pasted image 20230425235247.png]]

![[Pasted image 20230425235418.png]]

Parte 2: LADDER
[[LADDER]]
