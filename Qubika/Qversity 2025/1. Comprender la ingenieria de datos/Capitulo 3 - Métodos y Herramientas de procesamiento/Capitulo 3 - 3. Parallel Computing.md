
## Computación Paralela
- Es un término muy común que se utiliza en Ingeniería de Datos
- Conocida también como procesamiento paralelo
- Constituye la base de casi todas las herramientas de procesamiento de datos
- Necesaria por:
	- Cuestiones de **Memoria**
	- **Potencia de procesamiento**
- Cómo funciona:
	- Cuando las tareas de **procesamiento de Big Data** realizan una tarea de procesamiento, estas se **dividen en subtareas pequeñas**
	- Estas **subtareas se distribuyen entre varios ordenadores**


## Analogía: Tienda de Merchandising de música

- Se requiere **doblar un lote de 1000 camisetas**
- La dependiente **Senior dobla 100 camisas en 15 min**
- Los **Juniors se tardan 30 min**
- Si solo puede trabajar un vendedor a la vez, es lógico elegir al más rápido para terminar el trabajo
- PERO:
	- Si **dividimos el lote en 250 camisas** cada uno, tener a **4 Juniors trabajando en paralelo** es **más beneficioso**
	- En total, **el tiempo empleado será menor** al utilizar a los 4 Juniors en paralelo, que solamente al Senior

![[Pasted image 20250515170755.png]]

## En el Big Data

### Beneficios y Riesgos de la Computación Paralela

- $Los Empleados = Unidades De Procesamiento$

**Ventajas**
- **Potencia adicional** de procesamiento
- **Reduce la huella de memoria por ordenador**.
	- Al **dividir los datos y cargar** los conjuntos **en memorias de distintos** computadores. La huella por ordenador termina siendo pequeña

**Desventajas**
- **Costo de mover los datos**
- Dividir una tarea en subtareas y luego **fusionarlas en un resultado final**
- Requiere **tiempo de comunicación**
	- Al querer separar y volver a unir todos los resultados de los subprocesos

Por lo que, si volvemos a las camisetas:

![[Pasted image 20250515171300.png]]

- Al final, las camisetas dobladas por los Juniors en 1h15, deberán ser acomodadas en un solo conjunto, por lo que este tiempo de reacomodarlas, les tomará un 0h05.
- El **tiempo total para ejecutar esta tarea**, de doblar camisetas, es de **1h30**







