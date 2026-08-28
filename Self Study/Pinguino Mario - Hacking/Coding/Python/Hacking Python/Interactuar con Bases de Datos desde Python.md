---
title: "Interactuar con Bases de Datos desde Python"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Lo primero será instalar esta librería de Python para gestionar bases de datos MySQL desde Python:
![[Pasted image 20221217093730.png]]
Y lo primero será establecer la conexión:
![[Pasted image 20221217093748.png]]
![[Pasted image 20221217093755.png]]
Ahora vamos a hacer una consulta:
```python
import mysql.connector

connection = mysql.connector.connect(user='root', password='123123',
                                    host='localhost',
                                    database='hr',
                                    port='3306',)

print(connection)

cursor = connection.cursor()
cursor.execute("SELECT first_name FROM employees")

consulta = cursor.fetchall()
print(consulta)
```
![[Pasted image 20221217093818.png]]
Ahora vamos a procesar esta consulta para volcarla dentro de un documento de texto:
![[Pasted image 20221217093834.png]]
![[Pasted image 20221217093839.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
