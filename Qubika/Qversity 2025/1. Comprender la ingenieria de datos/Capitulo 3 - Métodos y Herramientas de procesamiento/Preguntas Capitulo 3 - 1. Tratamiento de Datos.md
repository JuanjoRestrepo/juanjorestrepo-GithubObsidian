

#### Connect the dots (Une los puntos)

Las canalizaciones de datos se utilizan para procesar datos. Al final del Capítulo 1, aprendiste sobre ETL (Extraer, Transformar, Cargar), uno de los marcos utilizados para construir canalizaciones de datos. Las tareas de tratamiento de datos que acabas de estudiar se ajustan en realidad a ese marco, y corresponden a operaciones de extracción, transformación o carga.

Ten en cuenta que, aunque guardar y cargar suelen considerarse opuestos, en el contexto de la ingeniería de datos son la misma cosa, como habrás podido comprobar. La razón de esto es que cuando estás guardando algo, solo lo estás almacenando en el siguiente paso del proceso.

¿Puedes clasificar correctamente las tareas de tratamiento de datos como operaciones de extracción, transformación o carga?

---
## ETL - Conectar los puntos (Clasificación) 


**Extraer:** 
- Recopilación de datos de Google Analytics sobre nuestra promoción de marketing web que ofrece 3 meses de acceso al nivel premium. 
- Sacar en bucle las 20 canciones más escuchadas por los usuarios. 

**Transformar:**
- Resumir la actividad de escucha anual para indicar a los usuarios cuántas horas han escuchado música en Spotifylix este año. 
- Ordenar las canciones de una lista de reproducción en función de la fecha en que se añadieron. 
- Guardar el nuevo orden de una lista de reproducción que estaba ordenado según la fecha en que se añadieron las canciones, para que siga así la próxima vez que el usuario se conecte. 

**Cargar:** 
- Escribir todos los seguidores de un usuario en una tabla.


## Reflexión

**Extraer:** Esta etapa se trata de obtener los datos de las fuentes originales.

- **Recopilación de datos de Google Analytics:** Esto es claramente una acción de _obtención_ de datos de una fuente externa.
- **Sacar/Obtener en bucle las 20 canciones más escuchadas por los usuarios:** Aunque menciona "sacar", en este contexto, se refiere a _obtener_ esa información del sistema para luego posiblemente cargarla en otro lugar o para un análisis.

**Transformar:** Aquí es donde los datos se limpian, se modifican y se preparan para su uso.

- **Resumir la actividad de escucha anual:** Esto implica _procesar_ los datos de escucha para obtener un resumen.
- **Ordenar las canciones de una lista de reproducción:** Esto es una _modificación_ de la presentación de los datos.

**Cargar:** Esta es la etapa final donde los datos transformados se escriben en el sistema de destino.

- **Escribir todos los seguidores de un usuario en una tabla:** Esto es la acción de _almacenar_ los datos en un lugar específico.
- **Guardar el nuevo orden de una lista de reproducción:** Aunque involucra "guardar", la acción principal aquí es _transformar_ el orden de la lista según las preferencias del usuario.