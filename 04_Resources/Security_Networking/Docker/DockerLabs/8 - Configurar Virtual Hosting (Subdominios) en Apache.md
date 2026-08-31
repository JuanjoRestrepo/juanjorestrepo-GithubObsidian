---
title: "8 - Configurar Virtual Hosting (Subdominios) en Apache"
date: 2026-08-27
tags:
  - self-study
  - security-penetration-testing
  - avanzado
status: verified
author: "Juan José Restrepo Rosero"
last_updated: 2026-08-27
---

```bash
FROM ubuntu:latest

# Actualiza los paquetes e instala Apache
RUN apt-get update && apt-get install -y apache2

# Configura Apache para servir el dominio hidden.lab
RUN echo "ServerName hidden.lab" >> /etc/apache2/apache2.conf

# Copia tu página web al directorio de Apache para el dominio hidden.lab
COPY web /var/www/html

# Crea el directorio raíz para dev.hidden.lab
RUN mkdir -p /var/www/dev.hidden.lab

# Copia el archivo index.html para el subdominio dev.hidden.lab
COPY index.html /var/www/dev.hidden.lab/index.html

# Configura el VirtualHost para el subdominio dev.hidden.lab
RUN echo "<VirtualHost *:80>" > /etc/apache2/sites-available/dev.hidden.lab.conf \
    && echo "    ServerName dev.hidden.lab" >> /etc/apache2/sites-available/dev.hidden.lab.conf \
    && echo "    DocumentRoot /var/www/dev.hidden.lab" >> /etc/apache2/sites-available/dev.hidden.lab.conf \
    && echo "</VirtualHost>" >> /etc/apache2/sites-available/dev.hidden.lab.conf

# Configura el VirtualHost para el subdominio dev.hidden.lab
RUN echo "<VirtualHost *:80>" > /etc/apache2/sites-available/hidden.lab.conf \
    && echo "    ServerName hidden.lab" >> /etc/apache2/sites-available/hidden.lab.conf \
    && echo "    DocumentRoot /var/www/html" >> /etc/apache2/sites-available/hidden.lab.conf \
    && echo "</VirtualHost>" >> /etc/apache2/sites-available/hidden.lab.conf

# Habilita el sitio dev.hidden.lab
RUN a2ensite dev.hidden.lab

# Habilita el sitio hidden.lab
RUN a2ensite hidden.lab

# Habilita el módulo de rewrite para redireccionar desde el puerto 80 a hidden.lab
RUN a2enmod rewrite

# Configura la redirección desde el puerto 80 a hidden.lab
RUN echo "<VirtualHost *:80>" > /etc/apache2/sites-available/000-default.conf \
    && echo "    ServerName localhost" >> /etc/apache2/sites-available/000-default.conf \
    && echo "    DocumentRoot /var/www/html" >> /etc/apache2/sites-available/000-default.conf \
    && echo "    Redirect / http://hidden.lab/" >> /etc/apache2/sites-available/000-default.conf \
    && echo "</VirtualHost>" >> /etc/apache2/sites-available/000-default.conf

# Habilita el sitio 000-default
RUN a2ensite 000-default

# Inicia Apache en primer plano
CMD service apache2 start && tail -f /dev/null
```

<!-- self-study-knowledge-context -->
## Contexto de estudio
- Dominio: [[MOC-Self-Study#Security & Penetration Testing|Seguridad y pruebas de penetración]].
- Criterio de producción: Ejecuta técnicas únicamente en activos propios o con autorización explícita, alcance documentado y controles de no afectación.
> [!warning] Uso autorizado
> Este material es exclusivamente educativo y defensivo. Practica en laboratorios aislados, CTFs o sistemas para los que dispongas de autorización previa y explícita.
