---
tags:
  - Qversity
---

# Whenever, whenever (Para cualquier ocasión)

Mientras almuerzas con el resto del equipo de ciencia de datos, Sasha, la nueva becaria de ingeniería de datos, te cuenta lo siguiente: "La computación paralela es un comodín que puede utilizarse siempre que queramos, para cualquier tarea que deseemos. Solo optimiza la ejecución de cualquier tarea de procesamiento de datos. Deberíamos empezar a aplicarla en toda la canalización. Estoy dispuesta a ayudar a hacerlo".

La afirmación de Sasha es **FALSA**. 

**Explicación**
Si bien la computación paralela puede optimizar significativamente la ejecución de muchas tareas de procesamiento de datos, **no es un comodín que se pueda aplicar de manera efectiva a _cualquier_ tarea**.


## Reflexión

- **Dependencias:** 
	- Algunas tareas deben **ejecutarse en un orden específico** porque **dependen del resultado de la tarea anterior**. Paralelizar estas tareas podría ser imposible o requerir una reestructuración compleja.

- **Sobrecarga:** 
	- La coordinación y comunicación entre los procesos o hilos paralelos introduce una sobrecarga. Para **tareas muy pequeñas o que ya se ejecutan rápidamente**, esta sobrecarga podría superar los beneficios de la paralelización, haciendo que la **ejecución sea incluso más lenta**.

- **Naturaleza de la tarea:** 
	- Algunas tareas son **inherentemente secuenciales** y **no se pueden dividir fácilmente** para su ejecución en paralelo.


---
#### Parallel Universe (Universo paralelo)

Acabas de decirle a Sasha, la ingeniera de datos en prácticas, que aunque es increíblemente eficiente y potente, la computación paralela no es adecuada para todas las situaciones. Tiene sus limitaciones, y a veces es innecesario.

Te gustaría ayudar a Sasha a mejorar su comprensión. Le pides que comparta sus suposiciones sobre la informática paralela: le dirás si tiene razón o no, e intentarás explicarle por qué. ¿Estás preparado para el reto?


**Correcto:**
- La informática paralela se utiliza para proporcionar potencia de procesamiento adicional.
- La informática paralela se basa en unidades de procesamiento.
- Es una buena idea utilizar la computación paralela para codificar las canciones subidas por los artistas al formato .ogg que prefiere Spotflix.

**¡Error!:**
- La computación paralela no puede utilizarse para optimizar el uso de la memoria.
- Es una buena idea utilizar la computación paralela para actualizar la tabla de empleados cada mañana.
- La computación paralela siempre hará las cosas más rápidas.


**Verificación:**
- **Correcto:** Las tres afirmaciones son generalmente verdaderas o representan un buen caso de uso para la computación paralela. Codificar múltiples canciones simultáneamente (la tercera afirmación) es un ejemplo claro donde la paralelización puede ser beneficiosa.
- **¡Error!:**
    - La primera afirmación es falsa; la computación paralela _puede_ optimizar el uso de la memoria en ciertos escenarios (aunque no es su objetivo principal).
    - La segunda afirmación podría no ser ideal. Actualizar una tabla de empleados generalmente implica operaciones de escritura que podrían no beneficiarse significativamente del paralelismo y podrían introducir complejidad.
    - La tercera afirmación es falsa, como discutimos antes; la sobrecarga de la paralelización puede hacer que algunas tareas sean más lentas.


---

#### Obscured by clouds (Oscurecido por las nubes)

Sasha, la nueva becaria ingeniera de datos, está intentando convencerte de que la computación en nube y la computación multicloud no tienen absolutamente ningún inconveniente. No estás de acuerdo: sabes a ciencia cierta que no es cierto. Te hace cuestionarte si realmente se siente cómoda con el tema o no.

Una vez más, te tomas a pecho tu papel de manager e intentas ayudarla a mejorar su comprensión. Le pides que comparta sus suposiciones sobre la computación en nube: le dirás si tiene razón o no, e intentarás explicarle por qué. ¿Estás preparado para el reto?

**Correcto:**
- Una solución multinube reduce la dependencia de un único proveedor.
- La computación en nube engloba soluciones de almacenamiento, bases de datos e informática.
- Aprovechar la nube en lugar de nuestro propio centro de datos en las instalaciones nos permite utilizar solo los recursos que necesitamos, cuando los necesitamos.

**¡Error!:**
- La computación en nube reduce todo tipo de riesgos.
- EC2, S3 y RDS son soluciones ofrecidas por Microsoft Azure.
- Las soluciones multinube reducen los problemas de seguridad y gobernanza.

## Reflexión

- **Correcto:** Las tres afirmaciones son generalmente verdaderas sobre la computación en la nube y las soluciones multinube. Reducir la dependencia de un proveedor, la variedad de servicios que abarca la nube y la escalabilidad según la necesidad son beneficios clave.
- **¡Error!:**
    - La primera afirmación es falsa; la computación en la nube introduce nuevos tipos de riesgos, aunque mitigue otros.
    - La segunda afirmación es falsa; EC2, S3 y RDS son servicios de Amazon Web Services (AWS), no de Microsoft Azure.
    - La tercera afirmación es falsa; las soluciones multinube pueden _aumentar_ la complejidad de la seguridad y la gobernanza debido a la necesidad de gestionar múltiples entornos.

---

#### Somewhere I belong (Un lugar al que pertenezca)

Los ingenieros de datos de Spotflix están preocupados por la dependencia de la empresa de un único proveedor, y están considerando un enfoque multicloud. También creen que podría permitir a Spotflix reducir costes y ser más resistente ante un desastre.

Como acabas de ver, los principales proveedores de nube son AWS, Microsoft Azure y Google Cloud. Juntas, poseen cerca de la mitad de la cuota de mercado de la computación en nube. Tienen diferentes servicios, algunos los has visto en el vídeo, otros estás a punto de descubrirlos. También tienen competidores, algunos de los cuales estás a punto de descubrir también.

¿Puedes ayudar a los ingenieros de datos a clasificar los distintos servicios antes de que empiecen a evaluar alternativas?

**Informática:**
- Máquinas virtuales Azure
- AWS EC2

**Bases de datos:**
- AWS Redshift (almacén de datos)
- Google Cloud Datastore (NoSQL)
- Almacén de datos Snowflake

