---
tags:
  - Qversity
---

# Computación en la Nube para Procesamiento de Datos

**Las empresas pueden procesar datos en su propio centro de datos**, a menudo en sus propias instalaciones

## Servers on premises/Bastidores de Servidores 

- La empresa debe **comprarlos**
- Se necesita un **espacio para almacenarlos** y **transportarlos** si se requiere (transferirlos)
- **Costo de mantenimiento** y factura de luz
- **Suficiente potencia de procesamiento** para los **momentos de mayor actividad**
- Tener en cuenta la **potencia de procesamiento no usada** para los **momentos más tranquilos**
	- Esto tiene que ver con **evitar el desperdicio de recursos**

## Servers on the Cloud/Servidores en la nube

- Se **alquilan los servidores**
- **Bajo costo**
- **No se requiere espacio físico**
- Se utilizan **solo los recursos que se necesitan** en el **momento que se requieran**
- Mayor cercanía con el usuario
	- Menor latencia la usar las aplicaciones
	- Optimizar costos

- Fiabilidad de la Base de Datos (Database Reliability)
- Riesgo con Datos Sensibles

### Ejemplos de proveedores de Cloud Computing Services

![[Pasted image 20250515173548.png]]

## En Spotflix, se usa AWS

- **AWS S3:** para almacenar los álbumes de portada
- **AWS EC2**: para procesar canciones
- **AWS RDS:** para almacenar la información de los empleados

#### NOTA:
No es necesario contratar todos los servicios con el mismo proveedor. Se pueden utilizar varios. Esto se conoce como **LA MULTINUBLE/MULTICLOUD**

## Multicloud

**VENTAJAS**
- **Reducir la dependencia de un único proveedor**
- Eficiencias y **optimización de los costos**
- Cumplimiento de las leyes. **Las leyes locales** pueden **requerir que cierto tipo de datos estén físicamente presentes dentro de un mismo país**
- Mitigar posibles pérdidas en caso de un desastre
	- **2017 Apagón AWS.** Cayó el internet, la mitad de los **100 principales minoristas estaban caídos**
	- Las empresas que tenían Multicloud, pudieron mitigar el impacto


**CONTRAS**
- Los proveedores tratan de atrapar a los consumidores
- Los proveedores **a veces no son compatibles entre sí** 
- Seguridad y gobernanza



