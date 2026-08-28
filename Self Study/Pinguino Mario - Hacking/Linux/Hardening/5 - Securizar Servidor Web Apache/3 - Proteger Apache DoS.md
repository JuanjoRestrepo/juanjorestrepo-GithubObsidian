---
title: "3 - Proteger Apache DoS"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Podemos antes de nada instalar la herramienta hping3 para hacer ataques DoS:
```bash
sudo apt-get install hping3
```
Y a continuación lanzamos el ataque contra nuestro servidor:
```bash
hping3 -S -p 80 --flood localhost
```

## OPCIÓN 1
Si queremos evitar que nos ataquen el servidor, podemos añadir lo siguiente dentro de nuestro archivo de configuración de apache:
```bash
<IfModule mpm_prefork_module>
    MaxRequestWorkers 150
    ServerLimit 150
</IfModule>
```
## OPCIÓN 2
También podemos instalar el módulo de libapache2-mod-evasive:
```bash
sudo apt-get install libapache2-mod-evasive
```
Y editamos el archivo de configuración `etc/apache2/mods-available/evasive.conf`:
```bash
DOSHashTableSize 3097
DOSPageCount 20
DOSSiteCount 100
DOSSiteInterval 1
DOSBlockingPeriod 10
```
Y lo activamos:
```bash
sudo a2enmod evasive
```
## OPCIÓN 3
También podemos activar un fail2ban:
```bash
sudo apt-get install fail2ban
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
