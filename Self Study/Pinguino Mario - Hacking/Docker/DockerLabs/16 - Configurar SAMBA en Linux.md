---
title: "16 - Configurar SAMBA en Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

Lo primero será instalar samba:
```bash
apt install samba
```

Y lo siguiente será abrir su archivo de configuración:
```bash
nano /etc/samba/smb.conf
```
Y al final del archivo añadiremos la siguiente configuración, que será un recurso compartido llamado shared:
```bash
[shared]
   path = /srv/samba/shared
   valid users = dylan
   browsable = yes
   writable = yes
   guest ok = no
```
Y ahora creamos el directorio compartido:
```bash
sudo mkdir -p /srv/samba/shared
sudo chown -R dylan:dylan /srv/samba/shared
sudo chmod -R 0755 /srv/samba/shared
```
![[Pasted image 20240527092628.png]]
A continuación, creamos un usuario y lo añadimos a la base de datos de samba:
![[Pasted image 20240527092739.png]]
Si lo quisiéramos eliminar, usamos el mismo comando pero con el parámetro -x:
![[Pasted image 20240527094021.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
