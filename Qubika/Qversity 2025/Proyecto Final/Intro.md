
![[Pasted image 20250613155557.png]]

Integrar las herramientas durante el track hasta ahora
- Python
- Sql
- hacer un poco de leverage en airflow y dbt
	- integrar todas las tools y generar un pipeline end to end.
	- Desde consumir la data, pre procesarla, limpiarla


### Arquitectura propuesta

![[Pasted image 20250613155703.png]]

- Consumir la data que ellos generan desde n Bucket S3
- Implementar los servicios de airflow
- Posgrest desde un docker
- Ir versionando desde un github
- Finalmente subirlo a un repositorio de github


![[Pasted image 20250613155808.png]]


# Hasta el domingo 22

#### Sugerencias
- Dar acceso apenas se cree el repositorio a los 3 usuarios iniciales
- No cargar el form hasta que todo este terminado, solo cargarlo cuando ya este 100% terminado
- Seguir mejores practicas para que todo sea legible

---

# Instalación de software


## Docker



SILVER:

- DIAGRAMA DE ENTIDAD RELACION (HACERLO)



EL ENTREGABLE ES LA BASE DE DATOS ENTERA Y EL PIPELINE ENTERO

ENTENDER LO QUE HACE CADA CAPA, COMO FUE EL PROCESO DE DESARROLLO

LAS PREGUNTAS SON EN BASE A LO QUE SE HARIA EN UN NEGOCIO, ES COMO UNA VERIFICACION DE AUTORIA, VER HASTA DONDE UNO PUEDE LLEGAR Y TODO



LA DATA ES UN JSON, HAY QUE HACERLE TRANSFORMACION

ES DATA TELEFONICA, OPERADORES