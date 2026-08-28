---
title: "Instalar Servicio SSH en Linux"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

El primer paso será instalar ssh de esta forma:
```mixed
sudo apt install openssh-server
```
![[Pasted image 20230106072934.png]]

Después utilizaremos este comando para comprobar el estado de ejecución de SSH; y deberíamos verlo en ejecución:
```mixed
sudo systemctl status ssh
```

![[Pasted image 20230106073030.png]]

Y por último podemos asegurarnos de que permanezca activado con este comando:
![[Pasted image 20230106073115.png]]
Ahora tendremos que configurar el firewall para que permita conexiones por SSH sin problema; y para ello creamos esta regla utilizando este comando:
```mixed
sudo ufw allow ssh
```

![[Pasted image 20230106073309.png]]

Y ahora sólo tenemos que reiniciar el servicio SSH para aplicar todos estos cambios; para ello utilizaremos este comando:
```mixed
sudo service ssh restart
```

![[Pasted image 20230106073355.png]]

Ahora vamos a probarlo desde otro equipo poniendo la IP del equipo donde estamos configurando el servicio SSH y poniendo el username:
![[Pasted image 20230106073456.png]]

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
