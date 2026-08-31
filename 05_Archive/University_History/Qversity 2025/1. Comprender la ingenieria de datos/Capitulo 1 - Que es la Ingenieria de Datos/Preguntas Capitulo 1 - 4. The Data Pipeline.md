---
tags:
  - Qversity
Created: 2025-05-13
---

**It's not true (No es verdad)**  
El objetivo principal, al establecer canalizaciones de datos, es mejorar la eficacia con la que fluyen los datos, desde su ingesta hasta los usuarios finales.

La mayoría de las opciones siguientes son verdaderas, pero una es falsa. ¿Cuál es?

**Respuestas posibles**  
Selecciona una respuesta

1. Las canalizaciones de datos garantizan un flujo eficaz de los datos a través de la organización.
2. Las canalizaciones de datos automatizan la extracción de datos.
3. **Las canalizaciones de datos incluyen necesariamente un paso de transformación.**
4. ETL significa Extraer, Transformar, Cargar.



---
#### Pipeline (Canalización)

**Una vez que hayas completado con éxito este ejercicio, ¡asegúrate de leer el mensaje de éxito!** 🎶😉

Acabas de ver algunos ejemplos de canalizaciones utilizadas en Spotflix. ¡Hagamos que construyas una!

Nuestra ingeniera de datos, Vivian, está trabajando en la construcción de nuevas canalizaciones para generar un nuevo producto: la _Lista de reproducción semanal_. Es una lista de reproducción que nuestro sistema crea cada día para recomendar nuevas canciones que puedan gustar a los usuarios en función de sus preferencias.

En este ejercicio encontrarás algunos pasos. ¿Puedes ordenar los pasos correctamente para ayudarla a construir la canalización de datos generando una _Lista de reproducción semanal_ para cada usuario? Empecemos con un usuario, y construyamos una canalización de datos para generar una _Lista de reproducción semanal_ para Julian, nuestro científico de datos


**Ordena los pasos cronológicamente (el paso que ocurra primero debe estar arriba y el que ocurra último abajo).**

1. Extrae las canciones que más escuchó Julian el mes pasado 
	_(Se parte del historial de escucha del usuario.)_

2.  **Encuentra también a otros usuarios que escucharon mucho esas mismas canciones**  
    _(Identificamos perfiles similares.)_    
3. **Carga solo las 10 canciones más escuchadas por estos usuarios durante la última semana en una tabla llamada "Perfiles similares"**  
    _(Recolectamos lo más popular entre esos perfiles.)_
    
4. **Extrae solo las canciones que estos otros usuarios escuchan y que son del mismo género que las de las sesiones de escucha de Julian. Estas son nuestras recomendaciones.**  
    _(Filtramos para que las recomendaciones sean relevantes.)_
    
5. **Carga las canciones recomendadas en una nueva tabla. ¡Esa es la lista de reproducción semanal de Julian!**
