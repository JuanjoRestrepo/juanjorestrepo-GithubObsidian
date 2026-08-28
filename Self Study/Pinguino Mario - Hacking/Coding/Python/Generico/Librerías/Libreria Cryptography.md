---
title: "Libreria Cryptography"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Ejemplo de cómo encriptar y desencriptar un mensaje con python:

```python
from cryptography.fernet import Fernet

# Obtener la clave para cifrar el mensaje
key = Fernet.generate_key()
f = Fernet(key)

mensaje_encriptado = f.encrypt(b"Mensaje encriptado")

print(mensaje_encriptado) # Esto imprime el mensaje encriptado.

print(f.decrypt(mensaje_encriptado)) # Esto imprime el mensaje desencriptado.
```
![[Pasted image 20230509130115.png]]
### EJECUTAR CÓDIGO CIFRADO

Si queremos ejecutar una instrucción que esté cifrada, podemos hacerlo de esta manera, donde ciframos un comando y lo ejecutamos:
```python
from cryptography.fernet import Fernet
import os

# Obtener la clave para cifrar el mensaje
key = Fernet.generate_key()
f = Fernet(key)

# Crear un mensaje con el comando a ejecutar
mensaje = b'os.mkdir("hola")'

# Cifrar el mensaje
mensaje_cifrado = f.encrypt(mensaje)

# Descifrar el mensaje
mensaje_descifrado = f.decrypt(mensaje_cifrado)

# Ejecutar el mensaje descifrado
exec(mensaje_descifrado.decode())
```
![[Pasted image 20230509130548.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
